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

static const char* ip ="127.0.0.1";
static int  port = 9987;

static int is_connected = 0;
static list<TunerReservationHelperImpl*> gTrhList;

static int connect_to_trm()
{
    int socket_fd ;
    int socket_error = 0;
    struct sockaddr_in trm_address;

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
    if (is_connected == 0)
    {
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "%s:%d : Connecting to remote\n" , __FUNCTION__, __LINE__);
        while(1)
        {
            int retry_count = 10;
            socket_error = connect(socket_fd, (struct sockaddr *) &trm_address, sizeof(struct sockaddr_in));
            if (socket_error == ECONNREFUSED  && retry_count > 0)
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d : TRM Server is not started...retry to connect\n" , __FUNCTION__, __LINE__);
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
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "%s:%d : Connected\n" , __FUNCTION__, __LINE__);

            int current_flags = fcntl(socket_fd, F_GETFL, 0);
            current_flags &= (~O_NONBLOCK);
            fcntl(socket_fd, F_SETFL, current_flags);
            trm_socket_fd = socket_fd;
            is_connected = 1;
        }
        else
        {
            RDK_LOG(RDK_LOG_ERROR, "LOG.RDK.TRH", "%s:%d : socket_error %d, closing socket\n" , __FUNCTION__, __LINE__, socket_error);
            close(socket_fd);
            trm_socket_fd = -1;
        }
    }
    rmf_osal_mutexRelease( g_mutex);
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "%s:%d : returning %d\n",__FUNCTION__, __LINE__, socket_error);
    return socket_error;
}

static bool url_request_post( const char *payload, int payload_length)
{
    unsigned char *buf = NULL;
    bool ret = false;
    connect_to_trm();
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Connection status to TRM  %d\n", is_connected);

    if (is_connected )
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
            static unsigned int recorder_connection_id = 0XFFFFFF00;
            //static unsigned int recorder_connection_id = 0XFFFFF001;
            //recorder_connection_id += 1;

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
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "======== REQUEST MSG ========\n[");
            for (idx = 0; idx < (header_length); idx++) {
                printf( "%02x", buf[idx]);
            }
	    printf("]\n");

            for (; idx < (payload_length + header_length); idx++) {
                printf("%c", buf[idx]);
            }
	    printf("\n");

            /* Write payload from fastcgi to TRM */
            int write_trm_count = write(trm_socket_fd, buf, payload_length + header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Send to TRM  %d vs expected %d\n", write_trm_count, payload_length + header_length);
            free(buf);
            buf = NULL;

            if (write_trm_count == 0)
            {
                is_connected = 0;
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d : write_trm_count 0\n", __FUNCTION__, __LINE__);
                /* retry connect after write failure*/
            }
            else
            {
                ret = true;
            }
        }
    }
    return ret;
}

void processBuffer( const char* buf, int len)
{
    if (buf != NULL)
    {
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH","Response: \n%s\n", buf);
        std::vector<uint8_t> response;
        response.insert( response.begin(), buf, buf+len);
        RecorderMessageProcessor recProc;
        TRM::JsonDecoder jdecoder( recProc);
        jdecoder.decode( response);
    }
}

static void get_response (void* arg)
{
    int read_trm_count = 0;
    char *buf = NULL;
    const int header_length = 16;
    int idx = 0;
    int payload_length = 0;
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    while (1)
    {
        connect_to_trm();
        if ( is_connected )
        {
            buf = (char *) malloc(header_length);
            if (buf == NULL)
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d :  Malloc failed for %d bytes \n", __FUNCTION__, __LINE__, header_length);
                continue;
            }
            /* Read Response from TRM, read header first, then payload */
            read_trm_count = read(trm_socket_fd, buf, header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Read Header from TRM %d vs expected %d\n", read_trm_count, header_length);
            RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "===== RESPONSE HEADER ======\n[");

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
                    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "TRM Response payloads is %d and header %d\n", payload_length, header_length);
                    fflush(stderr);

                    buf = (char *) malloc(payload_length+1);
                    read_trm_count = read(trm_socket_fd, buf, payload_length);
                    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Read Payload from TRM %d vs expected %d\n", read_trm_count, payload_length);

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
                        is_connected = 0;
                        free(buf);
                        buf = NULL;
                        RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d : read_trm_count 0\n", __FUNCTION__, __LINE__);
                    }
                }
                else
                {
                    /* retry connect after payload-read failure*/
                    is_connected = 0;
                    free(buf);
                    buf = NULL;
                    RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d : read_trm_count 0\n", __FUNCTION__, __LINE__);

                }
            }
            else
            {
                RDK_LOG(RDK_LOG_WARN, "LOG.RDK.TRH", "%s:%d : read_trm_count %d\n", __FUNCTION__, __LINE__, read_trm_count);
                free(buf);
                buf = NULL;
                /* retry connect after header-read failure */
                is_connected = 0;
            }

        }
        else
        {
            RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TRH", "%s - Not connected- Sleep and retry\n", __FUNCTION__);
            sleep(1);
        }
    }
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
}

bool  TunerReservationHelperImpl::inited = false;

void TunerReservationHelperImpl::init()
{
    rmf_osal_ThreadId threadId;
    rmf_Error ret;
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);

    if ( false == inited )
    {
        inited = true;
        ret = rmf_osal_mutexNew( &g_mutex);
        if (RMF_SUCCESS != ret )
        {
            RDK_LOG( RDK_LOG_ERROR, "LOG.RDK.TRH", "%s - rmf_osal_mutexNew failed.\n", __FUNCTION__);
            return;
        }

        rmf_osal_threadCreate( get_response, NULL,
                               RMF_OSAL_THREAD_PRIOR_DFLT, RMF_OSAL_THREAD_STACK_SIZE,
                               &threadId,"TunerRes" );
        RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    }
}

TunerReservationHelperImpl::TunerReservationHelperImpl(TunerReservationEventListener* listener) :
    eventListener(listener)
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
    RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TRH", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
    mRunning = false;
    rmf_osal_mutexAcquire( g_mutex);
    gTrhList.remove(this);
    rmf_osal_mutexRelease( g_mutex);
    g_cond_free(tunerStopCond);
    g_mutex_free( tunerStopMutex);
}

bool TunerReservationHelperImpl::waitForResrvResponse()
{
    g_mutex_lock ( tunerStopMutex );
    while (false == resrvResponseRecieved )
    {
        g_cond_wait (tunerStopCond,
                     tunerStopMutex);
    }
    g_mutex_unlock (tunerStopMutex);
    return reservationSuccess;
}

void TunerReservationHelperImpl::notifyResrvResponse(bool success)
{
    g_mutex_lock ( tunerStopMutex );
    resrvResponseRecieved = true;
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

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

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

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

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

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

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

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    return ret;
}

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
bool TunerReservationHelperImpl::reserveTunerForRecord( string recordingId, const char* locator,
        uint64_t startTime, uint64_t duration)
{
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);
    TRM::Activity activity(TRM::Activity::kRecord);
    activity.addDetail("recordingId", recordingId);

    TRM::TunerReservation resrv( "xg1", locator, startTime, duration, activity);
    TRM::ReserveTuner msg(guid, "xg1", resrv);

    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseRecieved = false;

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

    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}


//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
bool TunerReservationHelperImpl::reserveTunerForLive( const char* locator,
        uint64_t startTime, uint64_t duration)
{
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);
    TRM::Activity activity(TRM::Activity::kLive);

    TRM::TunerReservation resrv( "xg1", locator, startTime, duration, activity);
    TRM::ReserveTuner msg(guid, "xg1", resrv);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;
    resrvResponseRecieved = false;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    if (ret == true)
    {
        ret = waitForResrvResponse();
    }

    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

bool TunerReservationHelperImpl::releaseTunerReservation( )
{
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::ReleaseTunerReservation msg( guid, "xg1", token);
    JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}


bool TunerReservationHelperImpl::canceledRecording()
{
    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Enter %s():%d \n" , __FUNCTION__, __LINE__);
    bool ret = false;
    std::vector<uint8_t> out;
    uuid_t value;
    uuid_generate(value);
    uuid_unparse(value, guid);

    TRM::CancelRecordingResponse msg(guid, TRM::ResponseStatus::kOk ,token, true);
    TRM::JsonEncode(msg, out);
    out.push_back(0);
    int len = strlen((const char*)&out[0]);
    int retry_count = 10;

    do
    {
        ret = url_request_post( (char *) &out[0], len);
        retry_count --;
    } while ((ret == false) && (retry_count >0));

    RDK_LOG(RDK_LOG_TRACE1, "LOG.RDK.TRH", "Exit %s():%d \n" , __FUNCTION__, __LINE__);
    return ret;
}

TunerReservationEventListener* TunerReservationHelperImpl::getEventListener()
{
    return eventListener;
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
    TunerReservationEventListener* el;

    rmf_osal_mutexAcquire( g_mutex);
    trh =  getTRH(msg);
    if ( NULL == trh )
    {
        std::cout << "\nMatching TRH could not be found" << std::endl;
    }
    else
    {
        bool success;
        TRM::TunerReservation resv = msg.getTunerReservation();
        trh->setToken( resv.getReservationToken());
        el = trh->getEventListener();
        TRM::ResponseStatus status  = msg.getStatus();
        if ( status == TRM::ResponseStatus::kOk )
        {
            std::cout << "\nOK response detected" << std::endl;
            if ( el )
            {
                el->reserveSuccess();
            }
            success = true;
        }
        else
        {
            int statusCode = status.getStatusCode();
            std::cout << "\nResponse not OK statusCode " << statusCode << std::endl;
            el->reserveFailed();
            success = false;
        }
        trh->notifyResrvResponse( success);
    }
    rmf_osal_mutexRelease( g_mutex);
}


void RecorderMessageProcessor::operator() (const TRM::CancelRecording &msg)
{
    TunerReservationHelperImpl* trh;
    TunerReservationEventListener* el;

    const string token = msg.getReservationToken();

    rmf_osal_mutexAcquire( g_mutex);
    trh =  getTRH(token);
    if ( NULL == trh )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TRH", "%s -Matching TRH couldnot be found\n", __FUNCTION__);
    }
    else
    {
        el = trh->getEventListener();
        if ( el )
        {
            el->cancelRecording();
        }
    }
    rmf_osal_mutexRelease( g_mutex);
}


void RecorderMessageProcessor::operator() (const TRM::NotifyTunerReservationRelease &msg)
{
    TunerReservationHelperImpl* trh;
    TunerReservationEventListener* el;
    string token = msg.getReservationToken();

    rmf_osal_mutexAcquire( g_mutex);
    trh =  getTRH(token);
    if ( NULL == trh )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TRH", "NotifyTunerReservationRelease -Matching TRH couldnot be found\n", __FUNCTION__);
    }
    else
    {
        string reason  = msg.getReason();

        RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TRH", "NotifyTunerReservationRelease -reason:  %s\n",  reason.c_str());
        el = trh->getEventListener();
        if ( el )
        {
            el->tunerReleased();
        }
    }
    rmf_osal_mutexRelease( g_mutex);
}

void RecorderMessageProcessor::operator() (const TRM::ReleaseTunerReservationResponse &msg)
{
    TunerReservationHelperImpl* trh;
    TunerReservationEventListener* el;
    bool isReleased;
    string token = msg.getReservationToken();

    rmf_osal_mutexAcquire( g_mutex);
    trh =  getTRH(token);
    if ( NULL == trh )
    {
        RDK_LOG( RDK_LOG_ERROR , "LOG.RDK.TRH", "NotifyTunerReservationRelease -Matching TRH couldnot be found\n", __FUNCTION__);
    }
    else
    {
        isReleased = msg.isReleased();
        el = trh->getEventListener();
        if ( true == isReleased )
        {
            RDK_LOG( RDK_LOG_INFO , "LOG.RDK.TRH", "ReleaseTunerReservationResponse -Tuner released\n", __FUNCTION__);
            if(el)
                el->releaseReservationSuccess();
        }
        else
        {
            RDK_LOG( RDK_LOG_WARN, "LOG.RDK.TRH", "ReleaseTunerReservationResponse -Tuner release failed\n", __FUNCTION__);
            if(el)
                el->releaseReservationFailed();
        }
    }
    rmf_osal_mutexRelease( g_mutex);
}


void TunerReservationHelper::init()
{
    TunerReservationHelperImpl::init();
}

TunerReservationHelper::TunerReservationHelper(TunerReservationEventListener* listener)
{
    impl = new TunerReservationHelperImpl(listener);
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

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
bool TunerReservationHelper::reserveTunerForRecord( string recordingId, const char* locator,
        uint64_t startTime, uint64_t duration)
{
    return impl->reserveTunerForRecord( recordingId.c_str(), locator,
                                        startTime, duration);
}

//startTime: start time of the reservation in milliseconds from the epoch.
//duration: reservation period measured from the start in milliseconds.
bool TunerReservationHelper::reserveTunerForLive( const char* locator,
        uint64_t startTime, uint64_t duration)
{
    return impl->reserveTunerForLive( locator, startTime, duration);
}

bool TunerReservationHelper::releaseTunerReservation( )
{
    return impl->releaseTunerReservation();
}

bool TunerReservationHelper::canceledRecording()
{
    return impl->canceledRecording();
}

void TRHListenerImpl::reserveSuccess()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
/*
        if (this == &tRHListenerLiveImpl)
        {
                RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "%s:%d this = %p Cancelling live reservation\n",__FUNCTION__,__LINE__,this);
                trhLive->releaseTunerReservation();
        }
*/
}

void TRHListenerImpl::reserveFailed()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
}

void TRHListenerImpl::tunerReleased()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
}

void TRHListenerImpl::cancelRecording()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
}

void TRHListenerImpl::releaseReservationSuccess()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
}

void TRHListenerImpl::releaseReservationFailed()
{
        RDK_LOG(RDK_LOG_INFO, "LOG.RDK.TEST", "Enter %s:%d this = %p\n",__FUNCTION__,__LINE__,this);
}
