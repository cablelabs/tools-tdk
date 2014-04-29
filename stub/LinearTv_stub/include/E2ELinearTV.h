/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
 * ============================================================================
 */

#ifndef __E2ELinearTV_STUB_H__
#define __E2ELinearTV_STUB_H__
#include <json/json.h>
#include "rdkteststubintf.h"
#include <string.h>
#define IN
#define OUT
#define CMAF_MAX_NAME_LEN 64

#define TEST_SUCCESS true
#define TEST_FAILURE false 

using namespace std;
#define NUMBER_OCAPID 10

class RDKTestAgent;
class E2ELinearTVStub : public RDKTestStubInterface
{
	public:
		void* E2ELinearTVhandle;

		/*Ctor*/
		E2ELinearTVStub();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*LinearTV Wrapper functions*/
                bool E2ELinearTVstubGetURL(IN const Json::Value& req, OUT Json::Value& response);
                bool E2ELinearTVstubPlayURL(IN const Json::Value& req, OUT Json::Value& response);
                bool E2ELinearTVstubKillPlayer(IN const Json::Value& req, OUT Json::Value& response);
		bool E2ELinearTVstubT2pTuning(IN const Json::Value& request, OUT Json::Value& response);
		bool E2ELinearTVstubT2pTrickplay(IN const Json::Value& request, OUT Json::Value& response);
 
};



#endif //__E2ELinearTV_Stub
