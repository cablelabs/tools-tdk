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

static bool inited = false;

TunerReservationHelper *pTrh1 = NULL;
TunerReservationHelper *pTrh2 = NULL;
TRHListenerImpl tRHListenerImpl1, tRHListenerImpl2;

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
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForHybrid, "TestMgr_TRM_TunerReserveForHyBrid"); 

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
    if (false == inited) {
        g_thread_init(NULL);
        rmf_osal_init( NULL, NULL );
        inited = true;
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
        //TunerReservationHelper *pTrh1 = NULL;
        //TRHListenerImpl tRHListenerImpl1;

        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->getAllTunerIds())
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerIds --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

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
        //TunerReservationHelper *pTrh1 = NULL;
        //TRHListenerImpl tRHListenerImpl1;

        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->getAllTunerStates())
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

    response["result"] = "SUCCESS";
    response["details"] = "TRM get all tuner states success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_GetAllReservations

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to fetch reservation for all tuners.
                     Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_GetAllReservations(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Entry\n");

    try
    {
        //TunerReservationHelper *pTrh1 = NULL;
        //TRHListenerImpl tRHListenerImpl1;

        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->getAllReservations())
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllReservations --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

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
        //TunerReservationHelper *pTrh1 = NULL;
        //TRHListenerImpl tRHListenerImpl1;

        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->getVersion())
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

    response["result"] = "SUCCESS";
    response["details"] = "TRM get tuner version success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetVersion -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForRecord

Arguments     : Input argument is recordingId, locator and duration. 
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveForRecord(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string recordingId = req["recordingId"].asString();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->reserveTunerForRecord(recordingId, locator.c_str(), startTime, duration))
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for record success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForRecord --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForLive

Arguments     : Input argument is locator and duration.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for live viewing.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveForLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrh2 = new TunerReservationHelper(&tRHListenerImpl2);
        if ((NULL == pTrh2) || !pTrh2->reserveTunerForLive(locator.c_str(), startTime, duration))
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
    return TEST_SUCCESS;
}


bool TRMAgent::TRMAgent_TunerReserveForHybrid(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string recordingId = req["recordingId"].asString();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
	pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        if ((NULL == pTrh1) || !pTrh1->reserveTunerForRecord(recordingId, locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
            return TEST_FAILURE;
        }

	pTrh2 = new TunerReservationHelper(&tRHListenerImpl2);
        if ((NULL == pTrh2) || !pTrh2->reserveTunerForLive(locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(5);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live viewing and recording success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
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
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveForHyBrid");

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
