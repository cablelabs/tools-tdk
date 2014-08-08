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

#ifndef __RDKLOGGER_STUB_H__
#define __RDKLOGGER_STUB_H__

#include <json/json.h>
#include <string.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "rdk_debug.h"
#include "rdk_utils.h"
#include <fstream>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TDK_LOG			"/opt/TDK/logs/AgentConsole.log"
#define TDK_DEBUG_CONF_FILE 	"/opt/TDK/debug.ini"
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
};
        extern "C" RDKLoggerAgent* CreateObject();

#endif //__RDKLOGGER_STUB_H__

