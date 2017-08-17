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

#ifndef __MOCAHAL_STUB_H__
#define __MOCAHAL_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rmh_type.h"
#include "rmh_soc.h"
#include "rdk_moca_hal.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define SUPPORTED_FREQUENCIES_BUFFER 128
#define FREQUENCIES_BUFFER 32
using namespace std;

RMH_Handle rmh;

class RDKTestAgent;
class MocaHalAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                MocaHalAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                bool MocaHal_Initialize(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetMoCALinkUp(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetEnabled(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_SetEnabled(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetLOF(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetFrequencyMask(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetSupportedFrequencies(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetHighestSupportedMoCAVersion(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetMac(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetName(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetMoCAVersion(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetNumNodes(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetSupportedModes(IN const Json::Value& req, OUT Json::Value& response);
                bool MocaHal_GetMode(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" MocaHalAgent* CreateObject();
#endif //__MOCAHAL_STUB_H__
