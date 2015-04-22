/*
* ============================================================================
* RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file and its contents are the intellectual property of RDK Management, LLC.
* It may not be used, copied, distributed or otherwise  disclosed in whole or in
* part without the express written permission of RDK Management, LLC.
* ============================================================================
* Copyright (c) 2014 RDK Management, LLC. All rights reserved.
* ============================================================================
*/

#include "TRMAgentHelper.h"

using namespace std;

static rmf_osal_Mutex g_mutex = 0;
static int trm_socket_fd = -1;
static int isConnectedToTRM = 0;
static const char* ip = "127.0.0.1";
static int port = 9987;
static bool responseReceived = false;
static bool responseSuccess = false;
static char responseStr[OUTPUT_LEN];

// Helper function to connect to TRM server
static int connect_to_trm()
{
    int socket_fd ;
    int socket_error = 0;
    struct sockaddr_in trm_address;

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Entry %s():%d : Connection status (%d)\n",__FUNCTION__, __LINE__, isConnectedToTRM);

    rmf_osal_mutexAcquire( g_mutex);
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

    if (isConnectedToTRM == 0)
    {
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

    rmf_osal_mutexRelease( g_mutex);

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d : Connection status(%d) socket_error(%d)\n",__FUNCTION__, __LINE__, isConnectedToTRM,socket_error);
    return socket_error;
}

// Helper function to post request to TRM server
static bool url_request_post( const char *payload, int payload_length)
{
    bool ret = false;

  try {

    unsigned char *buf = NULL;
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

            /*To create conflicts, TDK agent should act like a recorder.
            Hence send message with clientId 0xFFFFFF00 */
            const unsigned int recorder_connection_id = 0xFFFFFF00;
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "connection id: %02x\n",recorder_connection_id);

            buf[idx++] = (recorder_connection_id & 0xFF000000) >> 24;
            buf[idx++] = (recorder_connection_id & 0x00FF0000) >> 16;
            buf[idx++] = (recorder_connection_id & 0x0000FF00) >> 8;
            buf[idx++] = (recorder_connection_id & 0x000000FF) >> 0;
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
    else {
	RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Not Connected to TRM Server\n", __FUNCTION__, __LINE__);
    }
  }
  catch (...) {
      RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Error occured\n", __FUNCTION__, __LINE__);
  }

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

  try {

    if (buf != NULL)
    {
	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST","Response: \n%s\n", buf);
        formatResponse(buf,len);
        std::vector<uint8_t> response;
        response.insert( response.begin(), buf, buf+len);
        CTRMMonitor recProc;
        TRM::JsonDecoder jdecoder( recProc);
        jdecoder.decode( response);
    }
  }
  catch (...) {
        RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Error occured\n", __FUNCTION__, __LINE__);
  }
}

// Helper function to get Response from TRM server
static void get_response (void* arg)
{

  try {

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
            RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - Not connected - Sleep and retry\n", __FUNCTION__);
            sleep(1);
        }
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
  }
  catch (...) {
        RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Error occured\n", __FUNCTION__, __LINE__);
  }
}

bool waitForTRMResponse()
{
  try {
    int retry_count = 5;
    while ((false == responseReceived) && (retry_count >0))
    {
	sleep(1);
	retry_count --;
    }

    rmf_osal_mutexAcquire( g_mutex);
    if((retry_count == 0) && (false == responseReceived))
    {
	RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Timeout. Failed to get response msg\n", __FUNCTION__);
	responseSuccess = false;
    }
    rmf_osal_mutexRelease( g_mutex);

  }
  catch (...) {
        RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s():%d : Error occured\n", __FUNCTION__, __LINE__);
  }

    return responseSuccess;
}

bool TRMClient::inited = false;
static TRMClient* trmClient = NULL;
std::map<int,TRM::TunerReservation> TRMClient::tunerReservationDb;
static int j = 0;

void TRMClient::init()
{
    if ( false == inited )
    {
        if( ! g_thread_supported() )
            g_thread_init( NULL );
        rdk_logger_init(DEBUG_CONF_FILE);
        rmf_osal_init( NULL, NULL );
        inited = true;
        rmf_Error ret = rmf_osal_mutexNew( &g_mutex);

        if (RMF_SUCCESS != ret ) {
            RDK_LOG( RDK_LOG_ERROR, "LOG.RDK.TEST", "%s() - rmf_osal_mutexNew failed. Error = %d\n", __FUNCTION__, ret);
        } 
        else {
            rmf_osal_ThreadId threadId;
            rmf_osal_threadCreate( get_response, NULL,
                               RMF_OSAL_THREAD_PRIOR_DFLT, RMF_OSAL_THREAD_STACK_SIZE,
                               &threadId,"TunerRes" );

            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s():%d Created thread to get response from TRM\n" , __FUNCTION__, __LINE__);
        }
    }
}

TRMClient::TRMClient()
{
    init();

    tunerStopCond = g_cond_new();
    tunerStopMutex = g_mutex_new ();
    rmf_osal_mutexAcquire( g_mutex);
    trmClient = this;
    rmf_osal_mutexRelease( g_mutex);
}

TRMClient::~TRMClient()
{
    rmf_osal_mutexAcquire( g_mutex);
    trmClient = NULL;
    rmf_osal_mutexRelease( g_mutex);
    g_cond_free(tunerStopCond);
    g_mutex_free( tunerStopMutex);
}

bool TRMClient::waitForResrvResponse()
{
    g_mutex_lock ( tunerStopMutex );
    while (false == resrvResponseReceived )
    {
        g_cond_wait (tunerStopCond, tunerStopMutex);
    }
    g_mutex_unlock (tunerStopMutex);
    return reservationSuccess;
}

void TRMClient::notifyResrvResponse(bool success)
{
    g_mutex_lock ( tunerStopMutex );
    resrvResponseReceived = true;
    reservationSuccess = success;
    g_cond_signal ( tunerStopCond);
    g_mutex_unlock (tunerStopMutex);
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
        ret = url_request_post( (char *) &out[0], len);
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
        ret = url_request_post( (char *) &out[0], len);
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
        ret = url_request_post( (char *) &out[0], len);
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
        ret = url_request_post( (char *) &out[0], len);
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
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Found token: %s\n" ,reservationToken.c_str());
            break;
        }
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
        ret = url_request_post( (char *) &out[0], len);
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
bool TRMClient::reserveTunerForRecord( const string device, const string recordingId, const string locator,
        uint64_t startTime, uint64_t duration, bool hot)
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

    TRM::TunerReservation resrv( device, locator, startTime, duration, activity);
    TRM::ReserveTuner msg(guid, device, resrv);

    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseReceived = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    }
    while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForResrvResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
bool TRMClient::reserveTunerForLive( const string device, const string locator,
        uint64_t startTime, uint64_t duration)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);
    TRM::Activity activity(TRM::Activity::kLive);

    TRM::TunerReservation resrv( device, locator, startTime, duration, activity);
    TRM::ReserveTuner msg(guid, device, resrv);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseReceived = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForResrvResponse();
    }

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
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Found token: %s\n" ,reservationToken.c_str());
            break;
        }
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
        ret = url_request_post( (char *) &out[0], len);
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
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ResponseStatus status(TRM::ResponseStatus::kOk, "Recording Canceled Successfully");
    TRM::CancelRecordingResponse msg(guid, status, reservationToken, true);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
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
    uuid_unparse(value, guid);

    string reservationToken = "";
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if (((*it).second.getActivity() == TRM::Activity::kRecord) && (locator.compare((*it).second.getServiceLocator()) == 0))
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Cancel Recording Token: %s\n" ,reservationToken.c_str());
        }
    }

    TRM::CancelRecording msg(guid, reservationToken);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return ret;
}

bool TRMClient::cancelledLive(string reservationToken, string locator)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ResponseStatus status(TRM::ResponseStatus::kOk, "Live Canceled Successfully");
    TRM::CancelLiveResponse msg(guid, status, reservationToken, locator, true);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

bool TRMClient::cancelLive(string locator)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    string reservationToken = "";
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if (((*it).second.getActivity() == TRM::Activity::kLive) && (locator.compare((*it).second.getServiceLocator()) == 0))
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Cancel Live Token: %s\n" ,reservationToken.c_str());
        }
    }

    TRM::CancelLive msg(guid, locator, reservationToken);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    responseReceived = false;
    responseSuccess = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForTRMResponse();
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);

    return ret;
}

void TRMClient::setToken( const string& token)
{
    this->token = token;
}

bool TRMClient::addToReservationDb(TRM::TunerReservation resv)
{
	//Workaround for RDKTT-162
	if (resv.getReservationToken().empty())
	{
	    RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - Invalid reservation token. Skipping DB update\n",__FUNCTION__);
	    return false;
	}

        TRM::TunerReservation *copyReservation = new TRM::TunerReservation();
        *copyReservation = resv;
        tunerReservationDb[j]=*copyReservation;
        j++;

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
	return true;
}

bool TRMClient::removeFromReservationDb(const string reservationToken)
{
        bool bRetValue = false;
        std::map<int, TRM::TunerReservation >::iterator it = tunerReservationDb.begin();
        while(it != tunerReservationDb.end())
        {
            if ((*it).second.getReservationToken() == reservationToken)
            {
		RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s() - Releasing token: [%s]\n", __FUNCTION__, reservationToken.c_str());
                tunerReservationDb.erase(it++);
                j--;
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
    rmf_osal_mutexAcquire( g_mutex);
    if ( NULL == trmClient )
    {
	RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Matching TRM client not found\n", __FUNCTION__);
    }
    else
    {
        bool success = false;
        TRM::TunerReservation resv = msg.getTunerReservation();
        trmClient->setToken( resv.getReservationToken());
        TRM::ResponseStatus status  = msg.getStatus();
        if ( status == TRM::ResponseStatus::kOk )
        {
	    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - OK response detected\n", __FUNCTION__);
            success = TRMClient::addToReservationDb(resv);
        }
        else if ( status == TRM::ResponseStatus::kUserCancellation )
        {
            RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - NOK. UserCancelled\n", __FUNCTION__);
        }
        else
        {
            int statusCode = status.getStatusCode();
	    RDK_LOG( RDK_LOG_WARN , "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Response NOT OK. statusCode = %d\n", __FUNCTION__, statusCode);
        }
        trmClient->notifyResrvResponse( success );
    }
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelRecording &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    if ( NULL == trmClient )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Matching TRM client not found\n", __FUNCTION__);
    }
    else
    {
	RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Sending cancelledRecording response\n", __FUNCTION__);
        trmClient->cancelledRecording(msg.getReservationToken());
    }
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelLive &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    if ( NULL == trmClient )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelLive) - Matching TRM client not found\n", __FUNCTION__);
    }
    else
    {
	RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelLive) - Sending cancelledLive response\n", __FUNCTION__);
	trmClient->cancelledLive(msg.getReservationToken(), msg.getServiceLocator());
    }
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationRelease &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    string reason = msg.getReason();
    //Remove reservations which get released due to expiration
    TRMClient::removeFromReservationDb(msg.getReservationToken());
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationRelease) - reason:  %s\n",  __FUNCTION__, reason.c_str());
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::ReleaseTunerReservationResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
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
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::ValidateTunerReservationResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
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
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelRecordingResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
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
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::CancelLiveResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    bool isCanceled = msg.isCanceled();

    responseReceived = true;
    responseSuccess = isCanceled;

    if ( true == isCanceled )
    {
        responseSuccess = TRMClient::removeFromReservationDb(msg.getReservationToken());
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(CancelLiveResponse) - Live Canceled\n", __FUNCTION__);
    }
    else
    {
        int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(CancelLiveResponse) - Cancellation failed. statusCode = %d\n", __FUNCTION__,statusCode);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllTunerIdsResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
	responseSuccess = true;
    else
	responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllTunerIdsResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllTunerStatesResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();

    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;

    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllTunerStatesResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::GetAllReservationsResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetAllReservationsResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::GetVersionResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    responseReceived = true;
    int statusCode = msg.getStatus().getStatusCode();
    if (TRM::ResponseStatus::kOk == statusCode)
        responseSuccess = true;
    else
        responseSuccess = false;
    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(GetVersionResponse) StatusCode = %d\n", __FUNCTION__,statusCode);
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationUpdate &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    TRM::TunerReservation resv = msg.getTunerReservation();
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(NotifyTunerReservationUpdate)\nDevice:[%s] Activity:[%s] Locator:[%s] StartTime: [%lld] Duration: [%d] Token:[%s]\n",
                                __FUNCTION__,
                                resv.getDevice().c_str(),
                                (const char *)resv.getActivity().getActivity(),
                                resv.getServiceLocator().c_str(),
				resv.getStartTime(),
				resv.getDuration(),
                                resv.getReservationToken().c_str());
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerReservationConflicts &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    const TRM::ReserveTunerResponse::ConflictCT &conflicts =  msg.getConflicts();
    if (conflicts.size() != 0) {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - FOUND %d CONFLICTS\n", __FUNCTION__,conflicts.size());

        TRM::TunerReservation resv = msg.getTunerReservation();
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Requested Activity:[%s] on [%s] Token:[%s] is in conflict with following activity:\n",
                              (const char *)resv.getActivity().getActivity(),
                              resv.getServiceLocator().c_str(),
                              resv.getReservationToken().c_str());

        TRM::ReserveTunerResponse::ConflictCT::const_iterator it = conflicts.begin();
        for (it = conflicts.begin(); it != conflicts.end(); it++)
        {
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Activity:[%s] Locator:[%s] Token:[%s]\n",
                                                 (const char *)(*it).getActivity().getActivity(),
                                                 (*it).getServiceLocator().c_str(),
                                                 (*it).getReservationToken().c_str());

            // Update Reservation DB
            TRMClient::addToReservationDb(*it);

            /*TODO: Select reservation to cancel between conflict
              Workaround: For now cancel the requested reservation causing conflict
                          because if no action is taken existing reservation will be auto-cancelled
                          by trm after new token timeout causing TDK agent to reset
            string cancelLoc = resv.getServiceLocator();
            int cancelActivity = resv.getActivity().getActivity();
            */

            string cancelLoc = (*it).getServiceLocator();
            int cancelActivity = (*it).getActivity().getActivity();
            string cancelDevice = (*it).getDevice();
            if ( NULL == trmClient )
            {
                RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Matching TRM client not found\n", __FUNCTION__);
            }
            else if (cancelActivity == TRM::Activity::kLive)
            {
                RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Cancel live request causing conflict\n", __FUNCTION__);
                trmClient->releaseTunerReservation(cancelDevice, cancelLoc, cancelActivity);
            }
            else if (cancelActivity == TRM::Activity::kRecord)
            {
                RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - Cancel recording request causing conflict\n", __FUNCTION__);
                trmClient->cancelRecording(cancelLoc);
            }
        }
    }
    else {
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - FOUND NO CONFLICTS\n", __FUNCTION__);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerStatesUpdate &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerStatesUpdate called)\n", __FUNCTION__);
}

void CTRMMonitor::operator() (const TRM::NotifyTunerPretune &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerStatesUpdate called)\n", __FUNCTION__);
}
