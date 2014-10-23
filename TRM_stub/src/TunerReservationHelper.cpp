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

#include "TunerReservationHelper.h"

static rmf_osal_Mutex g_mutex = 0;
static int trm_socket_fd = -1;
static int isConnectedToTRM = 0;
static const char* ip = "127.0.0.1";
static int port = 9987;
static bool responseReceived = false;
static bool responseSuccess = false;

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
    unsigned char *buf = NULL;
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
            static unsigned int recorder_connection_id = 0XFFFFF000;

	    //RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "connection id: %02x\n",recorder_connection_id);

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

    return ret;
}

void processBuffer( const char* buf, int len)
{
    if (buf != NULL)
    {
	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST","Response: \n%s\n", buf);
        std::vector<uint8_t> response;
        response.insert( response.begin(), buf, buf+len);
        RecorderMessageProcessor recProc;
        TRM::JsonDecoder jdecoder( recProc);
        jdecoder.decode( response);
    }
}

// Helper function to get Response from TRM server
static void get_response (void* arg)
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
            RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s() - Not connected - Sleep and retry\n", __FUNCTION__);
            sleep(1);
        }
    }

    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
}

bool waitForTRMResponse()
{
    int retry_count = 5;
    while ((false == responseReceived) && (retry_count >0))
    {
	sleep(1);
	retry_count --;
    }

    rmf_osal_mutexAcquire( g_mutex);
    if((retry_count == 0) && (false == responseReceived))
	responseSuccess = false;
    rmf_osal_mutexRelease( g_mutex);
    return responseSuccess;
}

bool TunerReservationHelperImpl::inited = false;
static list<TunerReservationHelperImpl*> gTrhList;
std::map<int,TRM::TunerReservation> TunerReservationHelperImpl::tunerReservationDb;
static int j = 0;

void TunerReservationHelperImpl::init()
{
    rmf_osal_ThreadId threadId;
    rmf_Error ret;

    if ( false == inited )
    {
        inited = true;
        ret = rmf_osal_mutexNew( &g_mutex);
        if (RMF_SUCCESS != ret )
        {
            RDK_LOG( RDK_LOG_ERROR, "LOG.RDK.TEST", "%s() - rmf_osal_mutexNew failed. Error = %d\n", __FUNCTION__, ret);
            return;
        }

        rmf_osal_threadCreate( get_response, NULL,
                               RMF_OSAL_THREAD_PRIOR_DFLT, RMF_OSAL_THREAD_STACK_SIZE,
                               &threadId,"TunerRes" );

        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s():%d Created thread to get response from TRM\n" , __FUNCTION__, __LINE__);
    }
}

TunerReservationHelperImpl::TunerReservationHelperImpl()
{
    init();

    tunerStopCond = g_cond_new();
    tunerStopMutex = g_mutex_new ();
    rmf_osal_mutexAcquire( g_mutex);
    gTrhList.push_back(this);
    rmf_osal_mutexRelease( g_mutex);
}

TunerReservationHelperImpl::~TunerReservationHelperImpl()
{
    rmf_osal_mutexAcquire( g_mutex);
    gTrhList.remove(this);
    rmf_osal_mutexRelease( g_mutex);
    g_cond_free(tunerStopCond);
    g_mutex_free( tunerStopMutex);
}

bool TunerReservationHelperImpl::waitForResrvResponse()
{
    g_mutex_lock ( tunerStopMutex );
    while (false == resrvResponseReceived )
    {
        g_cond_wait (tunerStopCond, tunerStopMutex);
    }
    g_mutex_unlock (tunerStopMutex);
    return reservationSuccess;
}

void TunerReservationHelperImpl::notifyResrvResponse(bool success)
{
    g_mutex_lock ( tunerStopMutex );
    resrvResponseReceived = true;
    reservationSuccess = success;
    g_cond_signal ( tunerStopCond);
    g_mutex_unlock (tunerStopMutex);
}

bool TunerReservationHelperImpl::getAllTunerStates(void)
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

    return ret;
}

bool TunerReservationHelperImpl::getAllTunerIds(void)
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

bool TunerReservationHelperImpl::getAllReservations(void)
{
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::GetAllReservations msg(guid, "");
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

bool TunerReservationHelperImpl::getVersion(void)
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

bool TunerReservationHelperImpl::validateTunerReservation(const char* device)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ValidateTunerReservation msg( guid, device, token);
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
bool TunerReservationHelperImpl::reserveTunerForRecord( const char* device, string recordingId, const char* locator,
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
bool TunerReservationHelperImpl::reserveTunerForLive( const char* device, const char* locator,
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

bool TunerReservationHelperImpl::releaseTunerReservation(const char* device)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ReleaseTunerReservation msg(guid, device, token);
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

bool TunerReservationHelperImpl::cancelledRecording(string reservationToken)
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

bool TunerReservationHelperImpl::cancelRecording(string locator)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    string reservationToken = token;
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if (((*it).second.getActivity() == TRM::Activity::kRecord) && (locator.compare((*it).second.getServiceLocator()) == 0))
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Cancel recording token: %s\n" ,reservationToken.c_str());
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

bool TunerReservationHelperImpl::cancelledLive(string reservationToken, string locator)
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

bool TunerReservationHelperImpl::cancelLive(string locator)
{
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    string reservationToken = token;
    std::map<int, TRM::TunerReservation >::iterator it;
    for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
    {
        if (((*it).second.getActivity() == TRM::Activity::kLive) && (locator.compare((*it).second.getServiceLocator()) == 0))
        {
            reservationToken = (*it).second.getReservationToken();
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Cancel live token: %s\n" ,reservationToken.c_str());
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

const char* TunerReservationHelperImpl::getId()
{
    return guid;
}

const string& TunerReservationHelperImpl::getToken()
{
    return token;
}

void TunerReservationHelperImpl::setToken( const string& token)
{
    this->token = token;
}

void TunerReservationHelperImpl::addToReservationDb(TRM::TunerReservation resv)
{
        TRM::TunerReservation *copyReservation = new TRM::TunerReservation();
        *copyReservation = resv;
        tunerReservationDb[j]=*copyReservation;
        j++;

	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nPrinting TunerReservation Db after entry insert\n");
	std::map<int, TRM::TunerReservation >::iterator it;
	for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
	{
	    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nNum:[%d] Device:[%s] Activity:[%s] Locator:[%s] Token:[%s]\n",
				(*it).first,
				(*it).second.getDevice().c_str(),
				(const char *)(*it).second.getActivity().getActivity(),
				(*it).second.getServiceLocator().c_str(),
				(*it).second.getReservationToken().c_str());
	}
}

void TunerReservationHelperImpl::removeFromReservationDb(const string reservationToken)
{
        std::map<int, TRM::TunerReservation >::iterator it;
        for(it = tunerReservationDb.begin(); it != tunerReservationDb.end();)
        {
            if (((*it).second.getReservationToken().c_str()) == reservationToken)
            {
		RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nReleasing token: [%s]\n", reservationToken.c_str());
                tunerReservationDb.erase(it++);
                j--;
            }
            else
            {
                ++it;
            }
        }

	RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nPrinting TunerReservation Db after entry removal\n");
        for(it = tunerReservationDb.begin(); it != tunerReservationDb.end(); it++)
        {
		RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "\nNum:[%d] Device:[%s] Activity:[%s] Locator:[%s] Token:[%s]\n",
				(*it).first,
				(*it).second.getDevice().c_str(),
				(const char *)(*it).second.getActivity().getActivity(),
				(*it).second.getServiceLocator().c_str(),
				(*it).second.getReservationToken().c_str());
        }
}

RecorderMessageProcessor::RecorderMessageProcessor()
{
}

TunerReservationHelperImpl* RecorderMessageProcessor::getTRH( const TRM::MessageBase &msg)
{
    TunerReservationHelperImpl* trh = NULL;
    list<TunerReservationHelperImpl*>::iterator i;
    for(i=gTrhList.begin(); i != gTrhList.end(); ++i)
    {
        string id = msg.getUUID();
        trh = *i;
        string temp_id = trh->getId();
        if ( 0 == temp_id.compare(id))
        {
            break;
        }
        trh = NULL;
    }
    return trh;
}

TunerReservationHelperImpl* RecorderMessageProcessor::getTRH( const string &token)
{
    TunerReservationHelperImpl* trh = NULL;
    list<TunerReservationHelperImpl*>::iterator i;
    for(i=gTrhList.begin(); i != gTrhList.end(); ++i)
    {
        trh = *i;
        string temp_token = trh->getToken();
        if ( 0 == temp_token.compare(token))
        {
            break;
        }
        trh = NULL;
    }
    return trh;
}

void RecorderMessageProcessor::operator() (const TRM::ReserveTunerResponse &msg)
{
    TunerReservationHelperImpl* trh;

    rmf_osal_mutexAcquire( g_mutex);
    trh =  getTRH(msg);
    if ( NULL == trh )
    {
	RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Matching TRH could not be found\n", __FUNCTION__);
    }
    else
    {
        bool success;
        TRM::TunerReservation resv = msg.getTunerReservation();
        trh->setToken( resv.getReservationToken());
        TRM::ResponseStatus status  = msg.getStatus();
        if ( status == TRM::ResponseStatus::kOk )
        {
	    RDK_LOG( RDK_LOG_INFO, "LOG.RDK.TEST", "%s(ReserveTunerResponse) - OK response detected\n", __FUNCTION__);
            success = true;
	    TunerReservationHelperImpl::addToReservationDb(resv);
        }
        else
        {
            int statusCode = status.getStatusCode();
	    RDK_LOG( RDK_LOG_WARN , "LOG.RDK.TEST", "%s(ReserveTunerResponse) - Response NOT OK. statusCode = %d\n", __FUNCTION__, statusCode);
            success = false;
        }
        trh->notifyResrvResponse( success );
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::CancelRecording &msg)
{
    TunerReservationHelperImpl* trh;

    rmf_osal_mutexAcquire( g_mutex);
    const string token = msg.getReservationToken();
    trh =  getTRH(token);
    if ( NULL == trh )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Matching TRH could not be found\n", __FUNCTION__);
        responseReceived = true;
	responseSuccess = false;
    }
    else
    {
	RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelRecording) - Sending cancelledRecording response\n", __FUNCTION__);
        trh->cancelledRecording(token);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::CancelLive &msg)
{
    TunerReservationHelperImpl* trh;

    rmf_osal_mutexAcquire( g_mutex);
    const string token = msg.getReservationToken();
    const string locator = msg.getServiceLocator();

    trh =  getTRH(token);
    if ( NULL == trh )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelLive) - Matching TRH could not be found\n", __FUNCTION__);
        responseReceived = true;
        responseSuccess = false;
    }
    else
    {
	RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(CancelLive) - Sending cancelledLive response\n", __FUNCTION__);
	trh->cancelledLive(token, locator);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::NotifyTunerReservationRelease &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    string token = msg.getReservationToken();
    string reason = msg.getReason();
    //Remove reservations which get released due to expiration
    TunerReservationHelperImpl::removeFromReservationDb(token);
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationRelease) - reason:  %s\n",  __FUNCTION__, reason.c_str());
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::ReleaseTunerReservationResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    bool isReleased = msg.isReleased();
    string token = msg.getReservationToken();

    responseReceived = true;
    responseSuccess = isReleased;

    if ( true == isReleased )
    {
	TunerReservationHelperImpl::removeFromReservationDb(token);
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(ReleaseTunerReservationResponse) - Tuner released\n", __FUNCTION__);
    }
    else
    {
	int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(ReleaseTunerReservationResponse) - Tuner release failed. statusCode=%d\n", __FUNCTION__,statusCode);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::ValidateTunerReservationResponse &msg)
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

void RecorderMessageProcessor::operator() (const TRM::CancelRecordingResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    bool isCanceled = msg.isCanceled();
    string token = msg.getReservationToken();

    responseReceived = true;
    responseSuccess = isCanceled;

    if ( true == isCanceled )
    {
	TunerReservationHelperImpl::removeFromReservationDb(token);
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(CancelRecordingResponse) - Recording Canceled\n", __FUNCTION__);
    }
    else
    {
        int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(CancelRecordingResponse) - Cancellation failed. statusCode = %d\n", __FUNCTION__,statusCode);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::CancelLiveResponse &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    bool isCanceled = msg.isCanceled();
    string token = msg.getReservationToken();

    responseReceived = true;
    responseSuccess = isCanceled;

    if ( true == isCanceled )
    {
	TunerReservationHelperImpl::removeFromReservationDb(token);
        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(CancelLiveResponse) - Live Canceled\n", __FUNCTION__);
    }
    else
    {
        int statusCode = msg.getStatus().getStatusCode();
        RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TEST", "%s(CancelLiveResponse) - Cancellation failed. statusCode = %d\n", __FUNCTION__,statusCode);
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::GetAllTunerIdsResponse &msg)
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

void RecorderMessageProcessor::operator() (const TRM::GetAllTunerStatesResponse &msg)
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

void RecorderMessageProcessor::operator() (const TRM::GetAllReservationsResponse &msg)
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

void RecorderMessageProcessor::operator() (const TRM::GetVersionResponse &msg)
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

void RecorderMessageProcessor::operator() (const TRM::NotifyTunerReservationUpdate &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    TRM::TunerReservation resv = msg.getTunerReservation();
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s(NotifyTunerReservationUpdate)\nDevice:[%s] Activity:[%s] Locator:[%s] StartTime: [%lld] Duration: [%d] Token:[%s]\n",
                                resv.getDevice().c_str(),
                                (const char *)resv.getActivity().getActivity(),
                                resv.getServiceLocator().c_str(),
				resv.getStartTime(),
				resv.getDuration(),
                                resv.getReservationToken().c_str());
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::NotifyTunerReservationConflicts &msg)
{
    rmf_osal_mutexAcquire( g_mutex);
    {
        TRM::TunerReservation resv = msg.getTunerReservation();
        const TRM::ReserveTunerResponse::ConflictCT &conflicts =  msg.getConflicts();

        if (conflicts.size() != 0) {
            RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - FOUND CONFLICTS\n", __FUNCTION__);
        }
        else {
            RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerReservationConflicts) - FOUND NO CONFLICTS\n", __FUNCTION__);
        }
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::NotifyTunerStatesUpdate &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerStatesUpdate called)\n", __FUNCTION__);
}

void RecorderMessageProcessor::operator() (const TRM::NotifyTunerPretune &msg)
{
    RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TEST", "%s(NotifyTunerStatesUpdate called)\n", __FUNCTION__);
}

// Implementation of TunerReservationHelper methods
void TunerReservationHelper::init()
{
    TunerReservationHelperImpl::init();
}

TunerReservationHelper::TunerReservationHelper()
{
    impl = new TunerReservationHelperImpl();
}

TunerReservationHelper::~TunerReservationHelper()
{
    delete impl;
}

bool TunerReservationHelper::getAllTunerStates( )
{
    return impl->getAllTunerStates();
}

bool TunerReservationHelper::getAllTunerIds ()
{
    return impl->getAllTunerIds();
}

bool TunerReservationHelper::getAllReservations()
{
    return impl->getAllReservations();
}

bool TunerReservationHelper::getVersion()
{
    return impl->getVersion();
}

bool TunerReservationHelper::validateTunerReservation(const char* device)
{
    return impl->validateTunerReservation(device);
}

bool TunerReservationHelper::reserveTunerForRecord( const char* device, string recordingId, const char* locator,
        uint64_t startTime, uint64_t duration, bool hot)
{
    return impl->reserveTunerForRecord( device, recordingId.c_str(), locator,
                                        startTime, duration, hot);
}

bool TunerReservationHelper::reserveTunerForLive( const char* device, const char* locator,
        uint64_t startTime, uint64_t duration)
{
    return impl->reserveTunerForLive( device, locator, startTime, duration );
}

bool TunerReservationHelper::releaseTunerReservation(const char* device )
{
    return impl->releaseTunerReservation(device);
}

bool TunerReservationHelper::cancelRecording(string locator)
{
    return impl->cancelRecording(locator);
}

bool TunerReservationHelper::cancelLive(string locator)
{
    return impl->cancelLive(locator);
}
