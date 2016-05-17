/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include "TRMAgentHelper.h"

using namespace std;

static pthread_mutex_t helper_mutex;
static int trm_socket_fd = -1;
static int isConnectedToTRM = 0;
static const char* ip = "127.0.0.1";
static int port = 9987;
static bool responseReceived = false;
static bool responseSuccess = false;
static bool resrvResponseReceived = false;
static string reservationSuccess = "";
static char responseStr[OUTPUT_LEN];
static char cancelRecReqId[GUID_LEN];
static const unsigned int kRecorderClientId = 0xFFFFFF00;
static const unsigned int kTestAppClientId = 0xFFFFFFEF;
static bool bSelectNewOnConflict = false;

bool TRMClient::inited = false;
static TRMClient* trmClient = NULL;
std::map<int,TRM::TunerReservation> TRMClient::tunerReservationDb;
static int dbCount = 0;

// Helper function to connect to TRM server
static int connect_to_trm()
{
    int socket_fd ;
    int socket_error = 0;
    struct sockaddr_in trm_address;

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Entry %s():%d : Connection status (%d)\n",__FUNCTION__, __LINE__, isConnectedToTRM);

    pthread_mutex_lock( &helper_mutex);

    if (isConnectedToTRM == 0)
    {
        if (trm_socket_fd == -1 )
        {
            trm_address.sin_family = AF_INET;
            trm_address.sin_addr.s_addr = inet_addr(ip);
            trm_address.sin_port = htons(port);

            socket_fd = socket(AF_INET, SOCK_STREAM, 0);
        }
        else
        {
            socket_fd = trm_socket_fd;
        }

        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s():%d : Connecting to remote...\n" , __FUNCTION__, __LINE__);
        while(1)
        {
            int retry_count = 10;
            socket_error = connect(socket_fd, (struct sockaddr *) &trm_address, sizeof(struct sockaddr_in));
            if (socket_error == ECONNREFUSED  && retry_count > 0)
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d : TRM Server is not started...retry to connect\n" , __FUNCTION__, __LINE__);
                sleep(2);
                retry_count--;
            }
            else
            {
                break;
            }
        }

        if (socket_error == 0)
        {
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s():%d : Connected\n" , __FUNCTION__, __LINE__);

            int current_flags = fcntl(socket_fd, F_GETFL, 0);
            current_flags &= (~O_NONBLOCK);
            fcntl(socket_fd, F_SETFL, current_flags);
            trm_socket_fd = socket_fd;
            isConnectedToTRM = 1;
        }
        else
        {
            RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Failed to connect. socket_error %d, closing socket\n" , __FUNCTION__, __LINE__, socket_error);
            close(socket_fd);
            trm_socket_fd = -1;
        }
    }

    pthread_mutex_unlock( &helper_mutex);

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d : Connection status(%d) socket_error(%d)\n",__FUNCTION__, __LINE__, isConnectedToTRM,socket_error);
    return socket_error;
}

// Helper function to post request to TRM server
static bool url_request_post( const char *payload, int payload_length, unsigned int clientId)
{
    bool ret = false;

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    if ( isConnectedToTRM == 0)
        connect_to_trm();

    if ( isConnectedToTRM )
    {
        if (payload_length != 0)
        {
            /* First prepend header */
            static int message_id = 0x1000;
            const int header_length = 16;
            unsigned char *buf = NULL;
            buf = (unsigned char *) malloc(payload_length + header_length);
            int idx = 0;
            /* Magic Word */
            buf[idx++] = 'T';
            buf[idx++] = 'R';
            buf[idx++] = 'M';
            buf[idx++] = 'S';
            /* Type, set to UNKNOWN, as it is not used right now*/
            buf[idx++] = (UNKNOWN & 0xFF000000) >> 24;
            buf[idx++] = (UNKNOWN & 0x00FF0000) >> 16;
            buf[idx++] = (UNKNOWN & 0x0000FF00) >> 8;
            buf[idx++] = (UNKNOWN & 0x000000FF) >> 0;
            /* Message id */
            ++message_id;

            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "CONNECTION CLIENTID: %02x\n",clientId);

            buf[idx++] = (clientId & 0xFF000000) >> 24;
            buf[idx++] = (clientId & 0x00FF0000) >> 16;
            buf[idx++] = (clientId & 0x0000FF00) >> 8;
            buf[idx++] = (clientId & 0x000000FF) >> 0;
            /* Payload length */
            buf[idx++] = (payload_length & 0xFF000000) >> 24;
            buf[idx++] = (payload_length & 0x00FF0000) >> 16;
            buf[idx++] = (payload_length & 0x0000FF00) >> 8;
            buf[idx++] = (payload_length & 0x000000FF) >> 0;

            for (int i =0; i< payload_length; i++)
                buf[idx+i] = payload[i];
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "====== REQUEST MSG ======\n[");
            for (idx = 0; idx < (header_length); idx++) {
                printf( "%02x", buf[idx]);
            }
            printf("]\n\n");

            for (; idx < (payload_length + header_length); idx++) {
                printf("%c", buf[idx]);
            }
            printf("\n\n");

            /* Write payload from fastcgi to TRM */
            int write_trm_count = write(trm_socket_fd, buf, payload_length + header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Send to TRM %d vs expected %d\n", write_trm_count, payload_length + header_length);
            free(buf);
            buf = NULL;

            if (write_trm_count == 0)
            {
                isConnectedToTRM = 0;
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d : write_trm_count 0\n", __FUNCTION__, __LINE__);
                /* retry connect after write failure*/
            }
            else
            {
                ret = true;
            }
        }
    }
    else
    {
	RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Not Connected to TRM Server\n", __FUNCTION__, __LINE__);
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return ret;
}

static void formatResponse(const char* buf, int len)
{
    memset(responseStr,'\0',OUTPUT_LEN);
    //Reduce the size of response msg by removing special characters added for indentation
    for (int i=0,j=0; i<len && j<OUTPUT_LEN; i++)
    {
        if ( !((buf[i] == '\n') || (buf[i] == '\t') || (buf[i] == ' ') || (buf[i] == '\"')) )
        {
            responseStr[j] = buf[i];
            j++;
        }
    }
}

void processBuffer( const char* buf, int len)
{
    if (buf != NULL)
    {
	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "====== RESPONSE PAYLOAD ====== \n%s\n", buf);
        formatResponse(buf,len);
        std::vector<uint8_t> response;
        response.insert( response.begin(), buf, buf+len);
        CTRMMonitor recProc;
        TRM::JsonDecoder jdecoder( recProc);
        jdecoder.decode( response);
    }
}

// Helper function to get Response from TRM server
static void* get_response (void* arg)
{
    int read_trm_count = 0;
    char *buf = NULL;
    const int header_length = 16;
    int idx = 0;
    int payload_length = 0;
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    while (1)
    {
	if ( isConnectedToTRM == 0)
            connect_to_trm();

        if ( isConnectedToTRM )
        {
            buf = (char *) malloc(header_length);
            if (buf == NULL)
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d :  Malloc failed for %d bytes \n", __FUNCTION__, __LINE__, header_length);
                continue;
            }
            /* Read Response from TRM, read header first, then payload */
            read_trm_count = read(trm_socket_fd, buf, header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Read Header from TRM %d vs expected %d\n", read_trm_count, header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "====== RESPONSE HEADER ======\n[");

            for (idx = 0; idx < (header_length); idx++) {
                printf( "%02x", buf[idx]);
            }
            printf("]\n");

            if (read_trm_count == header_length)
            {
                int payload_length_offset = 12;
                payload_length =((((unsigned char)(buf[payload_length_offset+0])) << 24) |
                                 (((unsigned char)(buf[payload_length_offset+1])) << 16) |
                                 (((unsigned char)(buf[payload_length_offset+2])) << 8 ) |
                                 (((unsigned char)(buf[payload_length_offset+3])) << 0 ));
                if (payload_length > 0)
                {
                    free( buf);
                    buf = NULL;
                    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRM Response payloads is %d and header %d\n", payload_length, header_length);
                    fflush(stderr);

                    buf = (char *) malloc(payload_length+1);
                    read_trm_count = read(trm_socket_fd, buf, payload_length);
                    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Read Payload from TRM %d vs expected %d\n", read_trm_count, payload_length);

                    if (read_trm_count != 0)
                    {
                        buf[payload_length] = '\0';
                        processBuffer(buf, read_trm_count);
                        free(buf);
                        buf = NULL;
                    }
                    else
                    {
                        /* retry connect after payload-read failure*/
                        isConnectedToTRM = 0;
                        free(buf);
                        buf = NULL;
                        RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d : read_trm_count = 0\n", __FUNCTION__, __LINE__);
                    }
                }
                else
                {
                    /* retry connect after payload-read failure*/
                    isConnectedToTRM = 0;
                    free(buf);
                    buf = NULL;
                    RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d : read_trm_count = 0\n", __FUNCTION__, __LINE__);
                }
            }
            else
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s():%d : read_trm_count = %d\n", __FUNCTION__, __LINE__, read_trm_count);
                free(buf);
                buf = NULL;
                /* retry connect after header-read failure */
                isConnectedToTRM = 0;
            }
        }
        else
        {
            RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - Not Connected to TRM Server - Sleep and Retry\n", __FUNCTION__);
            sleep(1);
        }
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return NULL;
}

bool waitForTRMResponse()
{
    int retry_count = 0;
    while ((false == responseReceived) && (retry_count < MAX_RETRY))
    {
	sleep(1);
	retry_count++;
    }

    if( false == responseReceived )
    {
        RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Timeout. Failed to get response msg within %d sec(s)\n", __FUNCTION__, retry_count);
    }
    else
    {
        RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Received response in %d sec(s)\n", __FUNCTION__, retry_count);
    }

    return responseSuccess;
}


string waitForResrvResponse()
{
    int retry_count = 0;
    while ((false == resrvResponseReceived) && (retry_count < MAX_RETRY))
    {
        sleep(1);
        retry_count++;
    }

    if( false == resrvResponseReceived )
    {
        RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Timeout. Failed to get response msg within %d sec(s)\n", __FUNCTION__, retry_count);
    }
    else
    {
        RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Received response in %d sec(s)\n", __FUNCTION__, retry_count);
    }

    return reservationSuccess;
}


void TRMClient::init()
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRMClient::init = %d\n" , inited);
    if ( false == inited )
    {
        /*Connect To TRM */
        connect_to_trm();

        rdk_logger_init(DEBUG_CONF_FILE);

        /*Mutex Init*/
        pthread_mutex_init(&helper_mutex, NULL);

        /* Create a Thread to Process TRM Response */
        pthread_t trm_thread;
	int ret = pthread_create(&trm_thread, NULL, get_response, (void *)trm_socket_fd);
        if( ret ) {
		RDK_LOG( RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d pthread_create returned error code: %d\n", __FUNCTION__, __LINE__, ret);
     	}
	else {
        	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s():%d Created thread to get response from TRM\n" , __FUNCTION__, __LINE__);
	}

	inited = true;
    }
}

TRMClient::TRMClient()
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRMClient Constr Entry Addr = %p\n" , this);

    init();

    pthread_mutex_lock( &helper_mutex);
    trmClient = this;
    pthread_mutex_unlock( &helper_mutex);

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRMClient Constr Exit\n");
}

TRMClient::~TRMClient()
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRMClient Destr Entry Addr = %p\n", trmClient);
    pthread_mutex_lock ( &helper_mutex );
    responseReceived = true;
    responseSuccess = false;
    resrvResponseReceived = true;
    reservationSuccess = "";
    bSelectNewOnConflict = false;
    trmClient = NULL;
    pthread_mutex_unlock( &helper_mutex);
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TRMClient Destr Exit\n");
}

bool TRMClient::getAllTunerStates(char *output)
{
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::GetAllTunerStates msg(guid, "");
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    if (ret == true)
    {
        strncpy(output,responseStr,strlen(responseStr));
    }

    return ret;
}

bool TRMClient::getAllTunerIds(void)
{
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::GetAllTunerIds msg(guid, "");
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    return ret;
}

bool TRMClient::getAllReservations(string filterDevice, char*output)
{
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::GetAllReservations msg(guid, filterDevice);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    if (ret == true)
    {
        strncpy(output,responseStr,strlen(responseStr));
    }

    return ret;
}

bool TRMClient::getVersion(void)
{
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::GetVersion msg(guid, "");
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    return ret;
}

bool TRMClient::validateTunerReservation(string device, string locator, int activityType)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    //Identify unique token Id using deviceName, locator and activity type
    string reservationToken = "";
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if ( (device.compare((*it).second.getDevice()) == 0) &&
             (locator.compare((*it).second.getServiceLocator()) == 0) &&
             (activityType == (*it).second.getActivity().getActivity()) )
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Found token: %s\n" ,__FUNCTION__, reservationToken.c_str());
            break;
        }
    }

    if ( reservationToken.empty() )
    {
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Matching token not found\n",__FUNCTION__);
    }

    TRM::ValidateTunerReservation msg( guid, device, reservationToken);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        if (TRM::Activity::kRecord == activityType)
        {
            ret = url_request_post( (char *) &out[0], len, kRecorderClientId);
        }
        else
        {
            ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        }
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
string TRMClient::reserveTunerForRecord( const string device, const string recordingId, const string locator,
        uint64_t startTime, uint64_t duration, bool hot, const string token, bool conflict)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);
    TRM::Activity activity(TRM::Activity::kRecord);
    activity.addDetail("recordingId", recordingId);
    if (false == hot)
        activity.addDetail("hot", "false");
    else if (true == hot)
        activity.addDetail("hot", "true");

    bSelectNewOnConflict = conflict;

    TRM::TunerReservation resrv( device, locator, startTime, duration, activity, token);
    TRM::ReserveTuner msg(guid, device, resrv);

    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseReceived = false;
    reservationSuccess = "";

    do
    {
        ret = url_request_post( (char *) &out[0], len, kRecorderClientId);
        retry_count --;
    }
    while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        waitForResrvResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return reservationSuccess;
}

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
string TRMClient::reserveTunerForLive( const string device, const string locator,
        uint64_t startTime, uint64_t duration, const string token, bool conflict)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);
    TRM::Activity activity(TRM::Activity::kLive);
    bSelectNewOnConflict = conflict;

    TRM::TunerReservation resrv( device, locator, startTime, duration, activity, token);
    TRM::ReserveTuner msg(guid, device, resrv);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseReceived = false;
    reservationSuccess = "";

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        waitForResrvResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return reservationSuccess;
}

bool TRMClient::cancelLiveReservation(TRM::TunerReservation resrv)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ReserveTuner msg(guid, resrv.getDevice(), resrv);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

bool TRMClient::releaseTunerReservation(string device, string locator, int activityType)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    //Identify unique token Id using deviceName, locator and activity type
    string reservationToken = "";
    std::map<int, TRM::TunerReservation >::iterator it;

    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if ( (device.compare((*it).second.getDevice()) == 0) &&
             (locator.compare((*it).second.getServiceLocator()) == 0) &&
             (activityType == (*it).second.getActivity().getActivity()) )
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Found token: %s\n" ,__FUNCTION__, reservationToken.c_str());
            break;
        }
    }

    if ( reservationToken.empty() )
    {
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Matching token not found\n",__FUNCTION__);
    }

    TRM::ReleaseTunerReservation msg(guid, device, reservationToken);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

bool TRMClient::cancelledRecording(string reservationToken)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;

    TRM::ResponseStatus status(TRM::ResponseStatus::kOk, "Recording Canceled Successfully");
    TRM::CancelRecordingResponse msg(cancelRecReqId, status, reservationToken, true);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kRecorderClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

bool TRMClient::cancelRecording(string locator)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, cancelRecReqId);

    string reservationToken = "";
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if (((*it).second.getActivity() == TRM::Activity::kRecord) && (locator.compare((*it).second.getServiceLocator()) == 0))
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Found token: %s\n" ,__FUNCTION__, reservationToken.c_str());
        }
    }

    if ( reservationToken.empty() )
    {
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(): Matching token not found\n",__FUNCTION__);
    }

    TRM::CancelRecording msg(cancelRecReqId, reservationToken);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return ret;
}

bool TRMClient::cancelRecordingReservation(string reservationToken)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, cancelRecReqId);

    TRM::CancelRecording msg(cancelRecReqId, reservationToken);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len, kTestAppClientId);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return ret;
}

string TRMClient::addToReservationDb(TRM::TunerReservation resv)
{
	if (resv.getReservationToken().empty())
	{
	    RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - Invalid reservation entry. Skipping DB update\n",__FUNCTION__);
	    return "";
	}

        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Adding token: [%s]\n", __FUNCTION__, resv.getReservationToken().c_str());
        TRM::TunerReservation *copyReservation = new TRM::TunerReservation();
        *copyReservation = resv;
        tunerReservationDb[dbCount]=*copyReservation;
        dbCount++;

	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TunerReservationDB after entry insertion\n");
	std::map<int, TRM::TunerReservation >::iterator it;
	for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
	{
	    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nACTIVITY:[%s] DEVICE:[%s] LOCATOR:[%s] TOKEN:[%s]\n",
				(const char *)(*it).second.getActivity().getActivity(),
				(*it).second.getDevice().c_str(),
				(*it).second.getServiceLocator().c_str(),
				(*it).second.getReservationToken().c_str());
	}
	return resv.getReservationToken();
}

bool TRMClient::removeFromReservationDb(const string reservationToken)
{
        bool bRetValue = false;
        std::map<int, TRM::TunerReservation >::iterator it = tunerReservationDb.begin();
        while(it != tunerReservationDb.end())
        {
            if ((*it).second.getReservationToken() == reservationToken)
            {
		RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Removing token: [%s]\n", __FUNCTION__, reservationToken.c_str());
                tunerReservationDb.erase(it++);
                dbCount--;
                bRetValue = true;
            }
            else
            {
                ++it;
            }
        }

        if (tunerReservationDb.empty())
        {
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TunerReservationDB is empty\n");
        }
        else
        {
	    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "TunerReservationDB after entry removal\n");
            for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
            {
		RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nACTIVITY:[%s] DEVICE:[%s] LOCATOR:[%s] TOKEN:[%s]\n",
				(const char *)(*it).second.getActivity().getActivity(),
				(*it).second.getDevice().c_str(),
				(*it).second.getServiceLocator().c_str(),
				(*it).second.getReservationToken().c_str());
            }
        }
        return bRetValue;
}

CTRMMonitor::CTRMMonitor()
{
}

void CTRMMonitor::operator() (const TRM::ReserveTunerResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);

    resrvResponseReceived = true;
    reservationSuccess = "";

    if ( NULL == trmClient )
    {
	RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Matching TRM client not found\n", __FUNCTION__);
    }
    else
    {
        TRM::ResponseStatus status = msg.getStatus();
        TRM::TunerReservation resv = msg.getTunerReservation();
        if ( status == TRM::ResponseStatus::kOk )
        {
            RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Status OK\n", __FUNCTION__);

            const TRM::ReserveTunerResponse::ConflictCT &conflicts =  msg.getConflicts();
            if (conflicts.size() != 0)
            {
                RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Activity:[%s] Locator:[%s] Token:[%s]\n",
                                                 (const char *)resv.getActivity().getActivity(),
                                                 resv.getServiceLocator().c_str(),
                                                 resv.getReservationToken().c_str());

                RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Found %d Conflict(s) with: \n", __FUNCTION__,conflicts.size());

                TRM::ReserveTunerResponse::ConflictCT::const_iterator it = conflicts.begin();
                for (it = conflicts.begin(); it != conflicts.end(); it++)
                {
                        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Activity:[%s] Locator:[%s] Token:[%s]\n",
                                                 (const char *)(*it).getActivity().getActivity(),
                                                 (*it).getServiceLocator().c_str(),
                                                 (*it).getReservationToken().c_str());
                }
            }
            else
            {
                if (resv.getReservationToken().empty())
                {
                    RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - No tuner reservation\n",__FUNCTION__);
                }
                else
                {
                    reservationSuccess = TRMClient::addToReservationDb(resv);
                }
            }
        }
        else
        {
            int statusCode = status.getStatusCode();
            RDK_LOG( RDK_LOG_WARN , "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Status NOT OK. statusCode = %d\n", __FUNCTION__, statusCode);

            if ( status == TRM::ResponseStatus::kGeneralError )
                reservationSuccess = "GeneralError";
            else if ( status == TRM::ResponseStatus::kMalFormedRequest )
                reservationSuccess = "MalFormedRequest";
            else if ( status == TRM::ResponseStatus::kUnRecognizedRequest )
                reservationSuccess = "UnRecognizedRequest";
            else if ( status == TRM::ResponseStatus::kInvalidToken )
                reservationSuccess = "InvalidToken";
            else if ( status == TRM::ResponseStatus::kInvalidState )
                reservationSuccess = "InvalidState";
            else if ( status == TRM::ResponseStatus::kUserCancellation )
                reservationSuccess = "UserCancellation";
            else if ( status == TRM::ResponseStatus::kInsufficientResource )
                reservationSuccess = "InsufficientResource";
        }
    }
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelRecording &msg)
{
    pthread_mutex_lock( &helper_mutex);
    if ( NULL == trmClient )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Matching TRM client not found\n", __FUNCTION__);
    }
    else
    {
	RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Sending cancelledRecording response\n", __FUNCTION__);
        trmClient->cancelledRecording(msg.getReservationToken());
    }
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationRelease &msg)
{
    pthread_mutex_lock( &helper_mutex);
    string reason = msg.getReason();
    //Remove reservations which get released due to expiration
    TRMClient::removeFromReservationDb(msg.getReservationToken());
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationRelease) - reason:  %s\n",  __FUNCTION__, reason.c_str());
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::ReleaseTunerReservationResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    bool isReleased = msg.isReleased();

    responseReceived = true;
    responseSuccess = isReleased;

    if ( true == isReleased )
    {
        responseSuccess = TRMClient::removeFromReservationDb(msg.getReservationToken());
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(ReleaseTunerReservationResponse) - Tuner released\n", __FUNCTION__);
    }
    else
    {
	int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(ReleaseTunerReservationResponse) - Tuner release failed. statusCode=%d\n", __FUNCTION__,statusCode);
    }
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::ValidateTunerReservationResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    bool isValid = msg.isValid();

    responseReceived = true;
    responseSuccess = isValid;

    if ( true == isValid )
    {
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(ValidateTunerReservationResponse) - Reservation valid\n", __FUNCTION__);
    }
    else
    {
        int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(ValidateTunerReservationResponse) - Reservation not valid. statusCode = %d\n", __FUNCTION__,statusCode);
    }
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelRecordingResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    bool isCanceled = msg.isCanceled();

    responseReceived = true;
    responseSuccess = isCanceled;

    if ( true == isCanceled )
    {
        responseSuccess = TRMClient::removeFromReservationDb(msg.getReservationToken());
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(CancelRecordingResponse) - Recording Canceled\n", __FUNCTION__);
    }
    else
    {
        int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(CancelRecordingResponse) - Cancellation failed. statusCode = %d\n", __FUNCTION__,statusCode);
    }
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllTunerIdsResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
	responseSuccess = true;
    else
	responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllTunerIdsResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllTunerStatesResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();

    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;

    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllTunerStatesResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllReservationsResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllReservationsResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::GetVersionResponse &msg)
{
    pthread_mutex_lock( &helper_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetVersionResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationUpdate &msg)
{
    pthread_mutex_lock( &helper_mutex);
    TRM::TunerReservation resv = msg.getTunerReservation();
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(NotifyTunerReservationUpdate)\nDevice:[%s] Activity:[%s] Locator:[%s] StartTime: [%lld] Duration: [%d] Token:[%s]\n",
                                __FUNCTION__,
                                resv.getDevice().c_str(),
                                (const char *)resv.getActivity().getActivity(),
                                resv.getServiceLocator().c_str(),
				resv.getStartTime(),
				resv.getDuration(),
                                resv.getReservationToken().c_str());
    pthread_mutex_unlock( &helper_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationConflicts &msg)
{
    pthread_mutex_lock( &helper_mutex);

    string cancelLoc;
    TRM::TunerReservation cancelResv;
    const TRM::ReserveTunerResponse::ConflictCT &conflicts =  msg.getConflicts();
    if (conflicts.size() != 0)
    {
        TRM::TunerReservation resv = msg.getTunerReservation();
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Existing Activity:[%s] Locator:[%s] Token:[%s]\n",
                                                 (const char *)resv.getActivity().getActivity(),
                                                 resv.getServiceLocator().c_str(),
                                                 resv.getReservationToken().c_str());

        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Found %d conflict(s) with new:\n", __FUNCTION__,conflicts.size());

        TRM::ReserveTunerResponse::ConflictCT::const_iterator it = conflicts.begin();
        for (it = conflicts.begin(); it != conflicts.end(); it++)
        {
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Activity:[%s] Locator:[%s] Token:[%s]\n",
                                                 (const char *)(*it).getActivity().getActivity(),
                                                 (*it).getServiceLocator().c_str(),
                                                 (*it).getReservationToken().c_str());
            if ( NULL == trmClient )
            {
                RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "NotifyTunerReservationConflicts - Matching TRM client not found\n");
            }
            else
            {
                // Update local reservation DB
                TRMClient::addToReservationDb(*it);

                //Select which reservation to keep between conflict
                //bSelectNewOnConflict = false (select existing reservation, cancel new reservation), [DEFAULT action]
                //                     = true  (select new reservation, cancel existing reservation)
                //Get the user's choice to either cancel new Recording or cancel existing Live
                RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "NotifyTunerReservationConflicts - select new reservation = %d \n", bSelectNewOnConflict);
                cancelLoc = (*it).getServiceLocator();
                if (bSelectNewOnConflict)
                {
                    RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "User selected new recording reservation and cancel existing live reservation to resolve conflict\n");
                    cancelResv = resv;
                }
                else
                {
                    RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "User selected existing live reservation and cancel new recording reservation to resolve conflict\n");
                    cancelResv = *it;
                }
            }
        }
    }
    else
    {
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Found no conflict\n", __FUNCTION__);
    }
    pthread_mutex_unlock( &helper_mutex);

    if (cancelResv.getActivity().getActivity() == TRM::Activity::kLive)
    {
         RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Cancelling live\n", __FUNCTION__);
         cancelResv.setServiceLocator(cancelLoc);
         trmClient->cancelLiveReservation(cancelResv);
    }
    else if (cancelResv.getActivity().getActivity() == TRM::Activity::kRecord)
    {
        RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Cancelling recording\n", __FUNCTION__);
        trmClient->cancelRecordingReservation(cancelResv.getReservationToken());
    }
}

void CTRMMonitor::operator() (const TRM::NotifyTunerStatesUpdate &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerStatesUpdate called)\n", __FUNCTION__);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerPretune &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerPretune called)\n", __FUNCTION__);
}

void CTRMMonitor::operator() (const TRM::CancelLive &msg)
{
    RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelLive called)\n", __FUNCTION__);
}

void CTRMMonitor::operator() (const TRM::CancelLiveResponse &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(CancelLiveResponse called)\n", __FUNCTION__);
}
