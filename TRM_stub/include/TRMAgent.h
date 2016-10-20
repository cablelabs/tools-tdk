/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

#ifndef __TRM_STUB_H__
#define __TRM_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <sstream>
#include "TRMAgentHelper.h"

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
    bool TRMAgent_CancelRecording(IN const Json::Value& req, OUT Json::Value& response);

};
extern "C" TRMAgent* CreateObject();

#endif //__TRM_STUB_H__
