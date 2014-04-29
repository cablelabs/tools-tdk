/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
 * ============================================================================
 */

#ifndef __RDKLOGGER_STUB_H__
#define __RDKLOGGER_STUB_H__

#include <json/json.h>
#include <string.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

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

                //RDKLoggerAgent Wrapper functions
		bool RDKLoggerAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Log(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_Dbg_Enabled_Status(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGet(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetNum(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetValueFromNum(IN const Json::Value& req, OUT Json::Value& response);
		bool RDKLoggerAgent_EnvGetModFromNum(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" RDKLoggerAgent* CreateObject();

#endif //__RDKLOGGER_STUB_H__

