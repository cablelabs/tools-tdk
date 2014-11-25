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
#include <glib.h>

#include <list>
#include <vector>
#include <map>
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

enum Type {
    REQUEST = 0x1234,
    RESPONSE = 0x1800,
    NOTIFICATION = 0x1400,
    UNKNOWN,
};

class TunerReservationHelperImpl
{
public:
    bool getAllTunerStates(void);
    bool getAllTunerIds(void);
    bool getAllReservations(std::string filterDevice);
    bool getVersion(void);
    bool validateTunerReservation(std::string device, std::string locator, int activityType);
    bool reserveTunerForRecord( std::string device, std::string recordingId, std::string locator, uint64_t startTime=0, uint64_t duration=0, bool hot=false);
    bool reserveTunerForLive( std::string device, std::string locator, uint64_t startTime=0, uint64_t duration=0);
    bool releaseTunerReservation(std::string device, std::string locator, int activityType);
    bool cancelledRecording(std::string reservationToken); /*This function shall be called by the application once cancelRecording event is handled*/
    bool cancelRecording(std::string locator);
    bool cancelledLive(std::string reservationToken, std::string locator); /*This function shall be called by the application once cancelRecording event is handled*/
    bool cancelLive(std::string locator);

    static void init();

    TunerReservationHelperImpl();
    ~TunerReservationHelperImpl();
    const char* getId();
    const std::string& getToken();
    void setToken( const std::string& token);
    void notifyResrvResponse(bool success);

    static void addToReservationDb(TRM::TunerReservation resv);
    static void removeFromReservationDb(const std::string token);

private:
    TunerReservationHelperImpl* impl;
    static bool inited;
    char guid[64];
    std::string token;
    bool waitForResrvResponse();
    GCond* tunerStopCond;
    GMutex* tunerStopMutex;
    bool reservationSuccess;
    bool resrvResponseReceived;
    static std::map<int,TRM::TunerReservation> tunerReservationDb;
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
    void operator() (const TRM::ValidateTunerReservationResponse &msg);
    void operator() (const TRM::CancelRecordingResponse &msg);
    void operator() (const TRM::CancelLiveResponse &msg);
    void operator() (const TRM::GetAllTunerIdsResponse &msg);
    void operator() (const TRM::GetAllTunerStatesResponse &msg);
    void operator() (const TRM::GetAllReservationsResponse &msg);
    void operator() (const TRM::GetVersionResponse &msg);
    void operator() (const TRM::NotifyTunerReservationUpdate &msg);
    void operator() (const TRM::NotifyTunerReservationConflicts &msg);
    void operator() (const TRM::NotifyTunerStatesUpdate &msg);
    void operator() (const TRM::NotifyTunerPretune &msg);

    TunerReservationHelperImpl* getTRH();
};

class TunerReservationHelper
{
public:
    bool getAllTunerStates();
    bool getAllTunerIds();
    bool getAllReservations(std::string filterDevice);
    bool getVersion();
    bool validateTunerReservation(std::string device, std::string locator, int activityType);
    bool reserveTunerForRecord( std::string device, std::string recordingId, std::string locator, uint64_t startTime=0, uint64_t duration=0, bool hot=false);
    bool reserveTunerForLive( std::string device, std::string locator, uint64_t startTime=0, uint64_t duration=0);
    bool releaseTunerReservation(std::string device, std::string locator, int activityType);
    bool cancelRecording(std::string locator);
    bool cancelLive(std::string locator);

    static void init();

    TunerReservationHelper();
    ~TunerReservationHelper();
private:
    TunerReservationHelperImpl* impl;
};
#endif
