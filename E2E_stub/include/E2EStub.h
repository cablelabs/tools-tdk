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

#ifndef __E2E_STUB_H__
#define __E2E_STUB_H__
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
class E2EStub : public RDKTestStubInterface
{
	public:
		void* E2EStubhandle;

		/*Ctor*/
		E2EStub();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*E2Estub Wrapper functions*/
                bool E2EStubGetURL(IN const Json::Value& req, OUT Json::Value& response);
                bool E2EStubPlayURL(IN const Json::Value& req, OUT Json::Value& response);
                bool E2EStubGetRecURLS(IN const Json::Value& request, OUT Json::Value& response);
                
};



#endif //__E2E_Stub
