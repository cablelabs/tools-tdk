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
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		bool initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		bool OpensourceTestStub_Execute(IN const Json::Value& req, OUT Json::Value& response);
	private:
		string getsummarylogpath(string);
		string getstatus(string);
};

#endif //__OPENSOURCE_TEST_STUB_H_


