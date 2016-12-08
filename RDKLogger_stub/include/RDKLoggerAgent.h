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

#ifndef __RDKLOGGER_STUB_H__
#define __RDKLOGGER_STUB_H__

#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rdk_debug.h"
#include "rdk_utils.h"
#include <fstream>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TDKAGENT_LOG		"AgentConsole.log"
#define DEBUG_CONF		"debug.ini"
#define SIZE    		256

using namespace std;

class RDKTestAgent;
class RDKLoggerAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                RDKLoggerAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //RDKLoggerAgent Wrapper functions
		bool RDKLoggerAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Dbg_Enabled_Status(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGet(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetNum(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetValueFromNum(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetModFromNum(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_CheckMPELogEnabled(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log_All(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log_None(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log_Trace(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log_InverseTrace(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log_Msg(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_SetLogLevel(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_GetLogLevel(IN const Json::Value& req, OUT Json::Value& response);
                //bool RDKLoggerAgent_Log_MPEOSDisabled(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" RDKLoggerAgent* CreateObject();

#endif //__RDKLOGGER_STUB_H__

