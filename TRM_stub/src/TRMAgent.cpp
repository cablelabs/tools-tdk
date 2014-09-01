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

TunerReservationHelper *pTrhRec = NULL;
TRHListenerImpl tRHListenerImplRec;

TunerReservationHelper *pTrhLive = NULL;
TRHListenerImpl tRHListenerImplLive;

// To test max number of tuners
TunerReservationHelper *pTrh1 = NULL;
TunerReservationHelper *pTrh2 = NULL;
TunerReservationHelper *pTrh3 = NULL;
TunerReservationHelper *pTrh4 = NULL;
TunerReservationHelper *pTrh5 = NULL;

TRHListenerImpl tRHListenerImpl1;
TRHListenerImpl tRHListenerImpl2;
TRHListenerImpl tRHListenerImpl3;
TRHListenerImpl tRHListenerImpl4;
TRHListenerImpl tRHListenerImpl5;

const char *deviceNames[TOTAL_DEVICE_NUMBER] = {
    "Xi3 Family Room",
    "Xi3 Living Room",
    "Xi3 Bedroom",
    "Xi3 Kitchen",
    "Xi3 Dining Room"
};

const char *locatorNames[TOTAL_LOCATOR_NUMBER] = {
    "ocap://0xCNN",
    "ocap://0xABC",
    "ocap://0xCBS",
    "ocap://0xNBC",
    "ocap://0xFOX",
    "ocap://0xHBO",
    "ocap://QVC",
};

const char *recordingIds[TOTAL_LOCATOR_NUMBER] = {
    "CNN",
    "ABC",
    "CBS",
    "NBC",
    "FOX",
    "HBO",
    "QVC",
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
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveForHybrid, "TestMgr_TRM_TunerReserveForHyBrid"); 
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ReleaseTunerReservation, "TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_ValidateTunerReservation, "TestMgr_TRM_ValidateTunerReservation");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_CancelLive, "TestMgr_TRM_CancelLive");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_CancelRecording, "TestMgr_TRM_CancelRecording");
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveAllForRecord, "TestMgr_TRM_TunerReserveAllForRecord");    
    ptrAgentObj->RegisterMethod(*this,&TRMAgent::TRMAgent_TunerReserveAllForLive, "TestMgr_TRM_TunerReserveAllForLive");

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
	rdk_logger_init(DEBUG_CONF_FILE);
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
	TunerReservationHelper *pTrh = NULL;
	TRHListenerImpl tRHListenerImpl;

        pTrh = new TunerReservationHelper(&tRHListenerImpl);
        if ((NULL == pTrh) || !pTrh->getAllTunerIds())
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
        TunerReservationHelper *pTrh = NULL;
        TRHListenerImpl tRHListenerImpl;

        pTrh = new TunerReservationHelper(&tRHListenerImpl);
        if ((NULL == pTrh) || !pTrh->getAllTunerStates())
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
        TunerReservationHelper *pTrh = NULL;
        TRHListenerImpl tRHListenerImpl;

        pTrh = new TunerReservationHelper(&tRHListenerImpl);
        if ((NULL == pTrh) || !pTrh->getAllReservations())
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
        TunerReservationHelper *pTrh = NULL;
        TRHListenerImpl tRHListenerImpl;

        pTrh = new TunerReservationHelper(&tRHListenerImpl);
        if ((NULL == pTrh) || !pTrh->getVersion())
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
        pTrhRec = new TunerReservationHelper(&tRHListenerImplRec);
        if ((NULL == pTrhRec) || !pTrhRec->reserveTunerForRecord(deviceNames[0], recordingId, locator.c_str(), startTime, duration))
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

    sleep(10);

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
        pTrhLive = new TunerReservationHelper(&tRHListenerImplLive);
        if ((NULL == pTrhLive) || !pTrhLive->reserveTunerForLive(deviceNames[1], locator.c_str(), startTime, duration))
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

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForLive --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveForHybrid

Arguments     : Input argument is recordingId, locator and duration.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve tuner for 
		live viewing and recording the channel at the same time.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
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
        pTrhLive = new TunerReservationHelper(&tRHListenerImplLive);
        if ((NULL == pTrhLive) || !pTrhLive->reserveTunerForLive(deviceNames[2], locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
            return TEST_FAILURE;
        }

	pTrhRec = new TunerReservationHelper(&tRHListenerImplRec);
        if ((NULL == pTrhRec) || !pTrhRec->reserveTunerForRecord(deviceNames[2], recordingId, locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
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

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live viewing and recording success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveForHybrid --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ReleaseTunerReservation

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to release a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_ReleaseTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrhLive = new TunerReservationHelper(&tRHListenerImplLive);
        if ((NULL == pTrhLive) || !pTrhLive->reserveTunerForLive(deviceNames[1], locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
            return TEST_FAILURE;
        }

        if ((NULL == pTrhLive) || !pTrhLive->releaseTunerReservation(deviceNames[1]))
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM release tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ReleaseTunerReservation --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_ValidateTunerReservation

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to validate a reservation.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_ValidateTunerReservation(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrhLive = new TunerReservationHelper(&tRHListenerImplLive);
        if ((NULL == pTrhLive) || !pTrhLive->reserveTunerForLive(deviceNames[1], locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
            return TEST_FAILURE;
        }

        if ((NULL == pTrhLive) || !pTrhLive->validateTunerReservation(deviceNames[1]))
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
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM validate tuner reservation success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_ValidateTunerReservation --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_CancelLive

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to cancel live viewing.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_CancelLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrhLive = new TunerReservationHelper(&tRHListenerImplLive);
        if ((NULL == pTrhLive) || !pTrhLive->reserveTunerForLive(deviceNames[1], locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
            return TEST_FAILURE;
        }

        if ((NULL == pTrhLive) || !pTrhLive->getAllTunerStates())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners states";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners states\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
            return TEST_FAILURE;
        }

        sleep (1);

        if ((NULL == pTrhLive) || !pTrhLive->cancelledLive(locator.c_str()))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to cancel live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to cancel live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
            return TEST_FAILURE;
        }

	sleep (1);

        if ((NULL == pTrhLive) || !pTrhLive->getAllTunerStates())
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
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelLive --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

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

    struct timeval tv;
    long long startTime = 0, duration = 0;

    string recordingId = req["recordingId"].asString();
    string locator = req["locator"].asString();
    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrhRec = new TunerReservationHelper(&tRHListenerImplRec);
        if ((NULL == pTrhRec) || !pTrhRec->reserveTunerForRecord(deviceNames[0], recordingId, locator.c_str(), startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
            return TEST_FAILURE;
        }
       
        if ((NULL == pTrhRec) || !pTrhRec->getAllTunerStates())
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to get all tuners states";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to get all tuners states\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_GetAllTunerStates --->Exit\n");
            return TEST_FAILURE;
        }

        sleep (1);

	if ((NULL == pTrhRec) || !pTrhRec->cancelledRecording()) 
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to cancel recording";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to cancel recording\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
            return TEST_FAILURE;
        }

        if ((NULL == pTrhRec) || !pTrhRec->getAllTunerStates())
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
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM cancel recording success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_CancelRecording --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveAllForRecord

Arguments     : Input argument is recordingId, locator and duration.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve all the tuners 
		for recording.
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveAllForRecord(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        pTrh2 = new TunerReservationHelper(&tRHListenerImpl2);
        pTrh3 = new TunerReservationHelper(&tRHListenerImpl3);
        pTrh4 = new TunerReservationHelper(&tRHListenerImpl4);
        pTrh5 = new TunerReservationHelper(&tRHListenerImpl5);

        if (!pTrh1->reserveTunerForRecord(deviceNames[0], recordingIds[0], locatorNames[0], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh2->reserveTunerForRecord(deviceNames[1],recordingIds[1],locatorNames[1],startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh3->reserveTunerForRecord(deviceNames[2],recordingIds[2],locatorNames[2],startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh4->reserveTunerForRecord(deviceNames[3], recordingIds[3],locatorNames[3], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh5->reserveTunerForRecord(deviceNames[4], recordingIds[4],locatorNames[4], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for record";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for record\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for record success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForRecord --->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : TRMAgent::TRMAgent_TunerReserveAllForLive

Arguments     : Input argument is locator and duration.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to reserve all the tuners
                for live viewing
                Gets the response from TRM server and sent to the Test Manager.
**************************************************************************/
bool TRMAgent::TRMAgent_TunerReserveAllForLive(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Entry\n");

    struct timeval tv;
    long long startTime = 0, duration = 0;

    duration = req["duration"].asDouble();

    gettimeofday( &tv, 0 );
    startTime = ((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000;

    try
    {
        pTrh1 = new TunerReservationHelper(&tRHListenerImpl1);
        pTrh2 = new TunerReservationHelper(&tRHListenerImpl2);
        pTrh3 = new TunerReservationHelper(&tRHListenerImpl3);
        pTrh4 = new TunerReservationHelper(&tRHListenerImpl4);
        pTrh5 = new TunerReservationHelper(&tRHListenerImpl5);

        if (!pTrh1->reserveTunerForLive(deviceNames[0], locatorNames[0], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh2->reserveTunerForLive(deviceNames[1],locatorNames[1],startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live viewing";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live viewing\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh3->reserveTunerForLive(deviceNames[2],locatorNames[2],startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live viewing";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live viewing\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh4->reserveTunerForLive(deviceNames[3], locatorNames[3], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live viewing";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live viewing\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
            return TEST_FAILURE;
        }
        else if (!pTrh5->reserveTunerForLive(deviceNames[4], locatorNames[4], startTime, duration))
        {
            response["result"] = "FAILURE";
            response["details"] = "TRM failed to reserve tuner for live viewing";
            DEBUG_PRINT(DEBUG_ERROR,"TRM failed to reserve tuner for live viewing\n");
            DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(...)
    {
        response["result"] = "FAILURE";
        response["details"] = "Exception occured while executing command";
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
        return TEST_FAILURE;
    }

    sleep(10);

    response["result"] = "SUCCESS";
    response["details"] = "TRM reserve tuner for live viewing success";
    DEBUG_PRINT(DEBUG_TRACE, "TRMAgent_TunerReserveAllForLive --->Exit\n");
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
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ReleaseTunerReservation");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_ValidateTunerReservation");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_CancelLive");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_CancelRecording");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveAllForRecord");
    ptrAgentObj->UnregisterMethod("TestMgr_TRM_TunerReserveAllForLive");

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
