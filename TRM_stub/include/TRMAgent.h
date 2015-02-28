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

#ifndef __TRM_STUB_H__
#define __TRM_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rdk_utils.h"
#include <sstream>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TOTAL_DEVICE_NUMBER 10

using namespace std;

class RDKTestAgent;
class TRMAgent : public RDKTestStubInterface
{
public:
    //Constructor
    TRMAgent();

    //Inherited functions
    bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

    bool cleanup(const char*, RDKTestAgent*);
    string testmodulepre_requisites();
    bool testmodulepost_requisites();

    //TRMAgent Wrapper functions
    bool TRMAgent_GetMaxTuners(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_GetAllTunerIds(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_GetAllTunerStates(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_GetAllReservations(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_GetVersion(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_TunerReserveForRecord(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_TunerReserveForLive(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_ReleaseTunerReservation(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_ValidateTunerReservation(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_CancelLive(IN const Json::Value& req, OUT Json::Value& response);
    bool TRMAgent_CancelRecording(IN const Json::Value& req, OUT Json::Value& response);

};
extern "C" TRMAgent* CreateObject();

#endif //__TRM_STUB_H__
