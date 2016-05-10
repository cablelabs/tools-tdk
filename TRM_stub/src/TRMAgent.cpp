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

static TRMClient *pTrmClient = NULL;

const char *deviceNames[TOTAL_DEVICE_NUMBER+1] = {
    "Xi3 Room1",
    "Xi3 Room2",
    "Xi3 Room3",
    "Xi3 Room4",
    "Xi3 Room5",
    "Xi3 Room6",
    "Xi3 Room7",
    "Xi3 Room8",
    "Xi3 Room9",
    "Xi3 Room10",
    "Xi3 Room11"
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
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetMaxTuners, "TestMgr_TRM_GetMaxTuners");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllTunerIds, "TestMgr_TRM_GetAllTunerIds");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllTunerStates, "TestMgr_TRM_GetAllTunerStates");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetAllReservations, "TestMgr_TRM_GetAllReservations");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_GetVersion, "TestMgr_TRM_GetVersion");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForRecord, "TestMgr_TRM_TunerReserveForRecord");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForLive, "TestMgr_TRM_TunerReserveForLive");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ReleaseTunerReservation, "TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ValidateTunerReservation, "TestMgr_TRM_ValidateTunerReservation");
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

    pTrmClient = new TRMClient();
    if (NULL == pTrmClient)
    {
        DEBUG_PRINT(DEBUG_ERROR, "Failed to create TRMClient instance\n");
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
    if (NULL != pTrmClient)
    {
       delete pTrmClient;
    }
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetMaxTuners

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the max number of tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetMaxTuners(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetMaxTuners --->Entry\n");
#ifdef NUM_OF_TUNERS
    DEBUG_PRINT(DEBUG_TRACE, "Max number of tuners supported by device = %d\n", NUM_OF_TUNERS);
    response["result"] = "SUCCESS";
    ostringstream details;
    details << NUM_OF_TUNERS;
    response["details"] = details.str();
#else
    DEBUG_PRINT(DEBUG_TRACE, "Max number of tuners supported by device unknown\n");
    response["result"] = "FAILURE";
    response["details"] = "0";
#endif
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetMaxTuners -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllTunerIds

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch Ids for all tuners.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetAllTunerIds(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Entry\n");

    try
    {
        if (!pTrmClient->getAllTunerIds())
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
    char output[OUTPUT_LEN] = {'\0'};

    try
    {
        if (!pTrmClient->getAllTunerStates(output))
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

    DEBUG_PRINT(DEBUG_TRACE, "output length = %d output value = %s\n", strlen(output),output);
    response["result"] = "SUCCESS";
    response["details"] = output;

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
    char output[OUTPUT_LEN] = {'\0'};

    if ((0 <= deviceNo) && (deviceNo <= TOTAL_DEVICE_NUMBER))
    {
	filter = deviceNames[deviceNo];
    }

    try
    {
        if (!pTrmClient->getAllReservations(filter, output))
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

    DEBUG_PRINT(DEBUG_TRACE, "output length = %d output value = %s\n", strlen(output),output);
    response["result"] = "SUCCESS";
    response["details"] = output;
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
        if (!pTrmClient->getVersion())
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
    bool select= req["selectOnConflict"].asInt();
    std::string outToken = "";
    std::string inToken = "";
    if( NULL != &req["token"] )
    {
        inToken = req["token"].asString();
    }

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
        outToken = pTrmClient->reserveTunerForRecord(deviceNames[deviceNo], recordingId, locator, startTime, duration, hot, inToken, select);
        if ("" == outToken)
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
        }
        else if ( (std::string::npos != outToken.find("-")) )
        {
            //Valid token is of format aa-bb-cc-dd-ee
            DEBUG_PRINT(DEBUG_TRACE, "output token = %s \n", outToken.c_str());
            response["result"] = "SUCCESS";
            response["details"] = outToken;
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record with error code = %s\n", outToken.c_str());
            response["result"] = "FAILURE";
            response["details"] = outToken;
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
    bool select= req["selectOnConflict"].asInt();
    std::string outToken = "";
    std::string inToken = "";
    if( NULL != &req["token"] )
    {
        inToken = req["token"].asString();
    }

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
        outToken = pTrmClient->reserveTunerForLive(deviceNames[deviceNo], locator, startTime, duration, inToken, select);
        if ("" == outToken)
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
        }
        else if ( (std::string::npos != outToken.find("-")) )
        {
            //Valid token is of format aa-bb-cc-dd-ee
            DEBUG_PRINT(DEBUG_TRACE, "output token = %s \n", outToken.c_str());
            response["result"] = "SUCCESS";
            response["details"] = outToken;
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live with error code = %s\n", outToken.c_str());
            response["result"] = "FAILURE";
            response["details"] = outToken;
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
        if (!pTrmClient->releaseTunerReservation(deviceNames[deviceNo], locator, activityType))
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
        if (!pTrmClient->validateTunerReservation(deviceNames[deviceNo], locator, activityType))
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
	if (!pTrmClient->cancelRecording(locator))
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

    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetMaxTuners");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllTunerIds");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllTunerStates");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetAllReservations");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_GetVersion");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveForRecord");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveForLive");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ValidateTunerReservation");
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
