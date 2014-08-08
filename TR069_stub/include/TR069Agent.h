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

#ifndef __TR069_STUB_H__
#define __TR069_STUB_H__

#include <json/json.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <sys/sysinfo.h>
#include <sys/utsname.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <net/if.h>


#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define IN
#define OUT

#define BUFF_LENGTH 512
#define CMD ("curl -d '{\"paramList\":[{\"name\":\"")
#define HTTP ("\"}]}' http://127.0.0.1:10999")
#define GET_NUM_OF_ACTIVE_PORTS "cat /proc/net/tcp | awk '$4 == \"0A\" || $4 == \"01\" {print $2" "$3" "$4}' | wc -l"
#define GET_IMAGE_VERSION "cat /version.txt | grep imagename: | cut -d \":\" -f 2"
#define GET_IPV4_ENABLE_STATUS "ifconfig | egrep 'inet addr:' | wc -l"
#define GET_STB_MAC "ifconfig | grep eth1 | head -n 1 | cut -b 39-"

#define TEST_SUCCESS true
#define TEST_FAILURE false


using namespace std;

class RDKTestAgent;
class TR069Agent : public RDKTestStubInterface
{
        public:
                /*Constructor*/
                TR069Agent();

                /*Inherited functions*/
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();

		/*Query Get Parameter Value */
		bool TR069Agent_GetParameterValue(IN const Json::Value& req, OUT Json::Value& response);
		bool TR069Agent_VerifyParameterValue(IN const Json::Value& req, OUT Json::Value& response);
		/*Query Set Parameter Value */
		//bool TR069Agent_SetParameterValue(IN const Json::Value& req, OUT Json::Value& response);
	

};

extern "C" TR069Agent* CreateObject();
#endif 
