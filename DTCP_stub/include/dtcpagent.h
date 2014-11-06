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

#ifndef __DTCP_STUB_H__
#define __DTCP_STUB_H__

#include <json/json.h>
#include <string.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "dtcpmgr.h"
#include <fstream>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false


using namespace std;

class RDKTestAgent;
class DTCPAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                DTCPAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //DTCPAgent Wrapper functions
		bool DTCPAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
};
        extern "C" DTCPAgent* CreateObject();

#endif //__DTCP_STUB_H__

