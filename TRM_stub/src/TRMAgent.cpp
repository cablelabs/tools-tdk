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

#include "TRMAgent.h"

static bool agentInited = false;

TunerReservationHelper *pTrh = NULL;

const char *deviceNames[TOTAL_DEVICE_NUMBER+1] = {
    "Xi3 Family Room",
    "Xi3 Living Room",
    "Xi3 Bedroom",
    "Xi3 Kitchen",
    "Xi3 Dining Room",
    "Xi3 Gym"
};

/*************************************************************************
Function name : TRMAgent::TRMAgent

Arguments     : NULL

Description   : Constructor for TRMAgent class
***************************************************************************/

TRMAgent::TRMAgent()
{
    DEBUG_PRINT(DEBUG_LOG, "TRMAgent Initialized\n");
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "TRMAgent".
**************************************************************************/

extern "C" TRMAgent* CreateObject()
{
    return new TRMAgent();
}

/**************************************************************************
Function name : TRMAgent::initialize

Arguments     : Input arguments are Version string and TRMAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool TRMAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_ERROR, "TRMAgent Initialization\n");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllTunerIds, "TestMgr_TRM_GetAllTunerIds");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllTunerStates, "TestMgr_TRM_GetAllTunerStates");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllReservations, "TestMgr_TRM_GetAllReservations");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetVersion, "TestMgr_TRM_GetVersion");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForRecord, "TestMgr_TRM_TunerReserveForRecord");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForLive, "TestMgr_TRM_TunerReserveForLive");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ReleaseTunerReservation, "TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ValidateTunerReservation, "TestMgr_TRM_ValidateTunerReservation");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_CancelLive, "TestMgr_TRM_CancelLive");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_CancelRecording, "TestMgr_TRM_CancelRecording");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

string TRMAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Entry\n");
    if (false == agentInited) {
        g_thread_init(NULL);
	rdk_logger_init(DEBUG_CONF_FILE);
        rmf_osal_init( NULL, NULL );
        agentInited = true;
    }

    pTrh = new TunerReservationHelper();
    if (NULL == pTrh)
    {
        DEBUG_PRINT(DEBUG_ERROR, "Failed to create TunerReservationHelper instance\n");
        return "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "TRM testmodule pre_requisites --> Exit\n");
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool TRMAgent::testmodulepost_requisites()
{
    if (NULL != pTrh)
    {
       delete pTrh;
    }
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllTunerIds

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch states for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetAllTunerIds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Entry\n");

    try
    {
        if (!pTrh->getAllTunerIds())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners Ids";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners Ids\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all tuner Ids";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all tuner Ids\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get all tuner Ids success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllTunerStates

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch states for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetAllTunerStates(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Entry\n");

    try
    {
        if (!pTrh->getAllTunerStates())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners states";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners states\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all tuner states";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all tuner states\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get all tuner states success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllReservations

Arguments     : Input argument is deviceNo. If deviceNo is default value(-1) send NULL filter value
                to get reservations for all tuners.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch reservation for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetAllReservations(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Entry\n");
    int deviceNo = req["deviceNo"].asInt();
    string filter = "";
    if ((0 <= deviceNo) && (deviceNo <= TOTAL_DEVICE_NUMBER))
    {
	filter = deviceNames[deviceNo];
    }

    try
    {
        if (!pTrh->getAllReservations(filter))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners reservations";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners reservations\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting all reservations";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting all reservations\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get all tuner reservations success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetVersion

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch tuner version.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetVersion(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Entry\n");

    try
    {
        if (!pTrh->getVersion())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get tuner version";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get tuner version\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while getting version";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while getting version\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM get tuner version success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForRecord

Arguments     : Input argument is deviceNo, recordingId, locator,
				  duration, startTime, hot.
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveForRecord(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Entry\n");

    struct timeval tv;
    unsigned long long startTime = 0, duration = 0;

    int deviceNo = req["deviceNo"].asInt();
    string recordingId = req["recordingId"].asString();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();
    unsigned long long startTimeAdd = req["startTime"].asDouble();
    bool hot = req["hot"].asInt();

    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
	response["result"] = "FAILURE";
	response["details"] = "Device Number out of range.";
	DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
	DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
	return TEST_FAILURE;
    }

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec + startTimeAdd) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        if (!pTrh->reserveTunerForRecord(deviceNames[deviceNo], recordingId, locator, startTime, duration, hot))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while reserving tuner for recording";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while reserving tuner for recording\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
        return TEST_FAILURE;
    }

    //sleep (2);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for record success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForLive

Arguments     : Input argument is deviceNo, locator, duration, startTime.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for live viewing.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveForLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Entry\n");

    struct timeval tv;
    unsigned long long startTime = 0, duration = 0;

    int deviceNo = req["deviceNo"].asInt();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();
    unsigned long long startTimeAdd = req["startTime"].asDouble();

    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
        return TEST_FAILURE;
    }

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec + startTimeAdd) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        if (!pTrh->reserveTunerForLive(deviceNames[deviceNo], locator, startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while reserving tuner for live";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while reserving tuner for live\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
        return TEST_FAILURE;
    }

    //sleep (2);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ReleaseTunerReservation

Arguments     : Input argument is deviceNo, locator and activityType(Live:1/Record:2).
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to release a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_ReleaseTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Entry\n");

    int activityType = req["activity"].asInt();
    string locator = req["locator"].asString();
    int deviceNo = req["deviceNo"].asInt();
    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    try
    {
        if (!pTrh->releaseTunerReservation(deviceNames[deviceNo], locator, activityType))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to release tuner reservation";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to release tuner reservation\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while releasing tuner reservation";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while releasing tuner reservation\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM release tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ValidateTunerReservation

Arguments     : Input argument is deviceNo, locator and activityType(Live:1/Record:2).
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to validate a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_ValidateTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Entry\n");

    int activityType = req["activity"].asInt();
    string locator = req["locator"].asString();
    int deviceNo = req["deviceNo"].asInt();
    if (TOTAL_DEVICE_NUMBER < deviceNo)
    {
        response["result"] = "FAILURE";
        response["details"] = "Device Number out of range.";
        DEBUG_PRINT(DEBUG_ERROR,"Device Number out of range.\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    try
    {
        if (!pTrh->validateTunerReservation(deviceNames[deviceNo], locator, activityType))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to validate tuner reservation";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to validate tuner reservation\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while validating tuner reservation";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while validating tuner reservation\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM validate tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_CancelLive

Arguments     : Input argument is locator. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to cancel live viewing.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_CancelLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Entry\n");

    string locator = req["locator"].asString();

    try
    {
        if (!pTrh->cancelLive(locator))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to cancel live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to cancel live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while cancelling live";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while cancelling live\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM cancel live success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_CancelRecording

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to cancel a recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_CancelRecording(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Entry\n");

    string locator = req["locator"].asString();

    try
    {
	if (!pTrh->cancelRecording(locator))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to cancel recording";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to cancel recording\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while cancelling recording";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured while cancelling recording\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
        return TEST_FAILURE;
    }

    response["result"] = "SUCCESS";
    response["details"] = "TRM cancel recording success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool TRMAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }

    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllTunerIds");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllTunerStates");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllReservations");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetVersion");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveForRecord");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveForLive");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ValidateTunerReservation");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_CancelLive");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_CancelRecording");

    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is TRMAgent Object

Description   : This function will be used to destory the TRMAgent object.
**************************************************************************/
extern "C" void DestroyObject(TRMAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying TRM Agent object\n");
    delete stubobj;
}
