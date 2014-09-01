/*
* ============================================================================
* RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file and its contents are the intellectual property of RDK Management, LLC.
* It may not be used, copied, distributed or otherwise  disclosed in whole or in
* part without the express written permission of RDK Management, LLC.
* ============================================================================
* Copyright (c) 2013 RDK Management, LLC. All rights reserved.
* ============================================================================
*/
#ifndef TRM_HELPER_H_
#define TRM_HELPER_H_

#include <arpa/inet.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>

#include <uuid/uuid.h>
#include <list>
#include <vector>
#include <map>
#include <glib.h>
#include <string>

#include "rmf_osal_thread.h"
#include "rmf_osal_util.h"
#include "rmf_osal_init.h"
#include "rdk_debug.h"
#include "rmf_osal_sync.h"

#include "trm/Messages.h"
#include "trm/MessageProcessor.h"
#include "trm/Activity.h"
#include "trm/JsonEncoder.h"
#include "trm/JsonDecoder.h"

using namespace std;

enum Type {
    REQUEST = 0x1234,
    RESPONSE = 0x1800,
    NOTIFICATION = 0x1400,
    UNKNOWN,
};

/*Application shall extend required methods to get events from TRH*/
class TunerReservationEventListener
{
public:
    virtual void reserveSuccess() {};
    virtual void reserveFailed() {};
    virtual void releaseReservationSuccess() {};
    virtual void releaseReservationFailed() {};
    virtual void tunerReleased() {};
    virtual void cancelledRecording() {};
    virtual void cancelledLive() {};
    virtual ~TunerReservationEventListener() {};
};

class TunerReservationHelperImpl
{
public:
    bool getAllTunerStates(void);
    bool getAllTunerIds(void);
    bool getAllReservations(void);
    bool getVersion(void);
    bool validateTunerReservation(const char* device);
    bool reserveTunerForRecord( const char* device, string recordingId, const char* locator, uint64_t startTime=0, uint64_t duration=0);
    bool reserveTunerForLive( const char* device, const char* locator, uint64_t startTime=0, uint64_t duration=0);
    bool releaseTunerReservation(const char* device);
    bool cancelledRecording(); /*This function shall be called by the application once cancelRecording event is handled*/
    bool cancelledLive(const char* locator);

    static void init();

    TunerReservationHelperImpl(TunerReservationEventListener* listener);
    ~TunerReservationHelperImpl();
    const char* getId();
    const std::string& getToken();
    void setToken( const std::string& token);
    TunerReservationEventListener* getEventListener();
    void notifyResrvResponse(bool success);

private:
    TunerReservationHelperImpl* impl;
    bool mRunning;
    TunerReservationEventListener* eventListener;
    static bool inited;
    char guid[64];
    std::string token;
    bool waitForResrvResponse();
    GCond* tunerStopCond;
    GMutex* tunerStopMutex;
    bool reservationSuccess;
    bool resrvResponseRecieved;
};

class RecorderMessageProcessor : public TRM::MessageProcessor
{
public :
    RecorderMessageProcessor();
    void operator() (const TRM::ReserveTunerResponse &msg) ;
    void operator() (const TRM::CancelRecording &msg);
    void operator() (const TRM::CancelLive &msg);
    void operator() (const TRM::NotifyTunerReservationRelease &msg);
    void operator() (const TRM::ReleaseTunerReservationResponse &msg);

    TunerReservationHelperImpl* getTRH( const TRM::MessageBase &msg);
    TunerReservationHelperImpl* getTRH( const string &token);
};

/*Application shall extend required methods to get events from TRH*/
class TunerReservationHelper
{
public:
    bool getAllTunerStates();
    bool getAllTunerIds();
    bool getAllReservations();
    bool getVersion();
    bool validateTunerReservation(const char* device);

    bool reserveTunerForRecord( const char* device, string recordingId, const char* locator, uint64_t startTime=0, uint64_t duration=0);
    bool reserveTunerForLive( const char* device, const char* locator, uint64_t startTime=0, uint64_t duration=0);
    bool releaseTunerReservation(const char* device);
    /*This function shall be called by the application once cancelRecording event is handled*/
    bool cancelledRecording();
    bool cancelledLive(const char* locator);

    static void init();

    TunerReservationHelper(TunerReservationEventListener* listener);
    ~TunerReservationHelper();
private:
    TunerReservationHelperImpl* impl;
};

class TRHListenerImpl : public TunerReservationEventListener
{
public:
    void reserveSuccess();
    void reserveFailed();
    void tunerReleased();
    void cancelledRecording();
    void cancelledLive();
    void releaseReservationSuccess();
    void releaseReservationFailed();
};
#endif
