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

#ifndef __OPENSOURCE_TEST_STUB_H__
#define __OPENSOURCE_TEST_STUB_H__
#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#define IN
#define OUT
#include <string.h>
#include <fstream>
#include <sys/wait.h>
#include <stdlib.h>

#define LOGGERFILE_NAME "LOGPATH_INFO"
#define SUITESTATUSFILE_NAME "SUITE_STATUS"
#define MASTERSUITE_NAME "SuiteExecuter.sh"
using namespace std;

class RDKTestAgent;
class OpensourceTestStub : public RDKTestStubInterface
{
	public:
		OpensourceTestStub();
		bool initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		bool OpensourceTestStub_Execute(IN const Json::Value& req, OUT Json::Value& response);
	private:
		string getsummarylogpath(string);
		string getstatus(string);
};

#endif //__OPENSOURCE_TEST_STUB_H_


