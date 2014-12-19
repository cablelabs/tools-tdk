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

#ifndef __XUPNP_STUB_H__
#define __XUPNP_STUB_H__

#include <json/json.h>
#include <string.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <fstream>
#include <cstdlib>
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define TDK_XUPNP_JSON_FILE 	"/opt/output.json"

using namespace std;

class RDKTestAgent;
class XUPNPAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                XUPNPAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //XUPNPAgent Wrapper functions
		bool XUPNPAgent_checkjson(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_checkSTRurl(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_checkSerialNo(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_checkPBurl(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_recordId(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_ModBasicDevice(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_removeXmls(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtCheck(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evttuneready(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtChannelMap(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtControllerID(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtPlantID(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtvodID(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_evtTimezone(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_IFDown(IN const Json::Value& req, OUT Json::Value& response);
		bool XUPNPAgent_IPIFDown(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" XUPNPAgent* CreateObject();

#endif //__XUPNP_STUB_H__

