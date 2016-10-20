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

#ifndef __IARM_STUB_H__
#define __IARM_STUB_H__
#include <json/json.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "libIBus.h"
#include "rdktestagentintf.h"
#include "libIBusDaemon.h"
#include "libIARM.h"
#include "libIBus.h"
#include "irMgr.h"
#include "pwrMgr.h"
#include "sysMgr.h"
#include "diskMgr.h"
#include "mfrMgr.h"
#include "mfrTypes.h"
#include <sys/types.h>
#include <sys/wait.h>
#include "dummytestmgr.h"
#include "keyeventdata.h" /*Performance test include*/
#include <fstream>
#include <sstream>
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false
#define STR_LEN                128
#define LINE_LEN               1024
#define EVTDATA_MAX_SIZE 3
#define PRE_REQ_CHECK "pre_requisite_chk.txt"
#define DAEMON_EXE "IARMDaemonMain"
#define PWRMGR_EXE "pwrMgrMain"
#define IRMGR_EXE "irMgrMain"
#define MFRMGR_EXE "mfrMgrMain"
#define SYSMGR_EXE "sysMgrMain"
#define DISKMGR_EXE "diskMgrMain"

class RDKTestAgent;
class IARMBUSAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		IARMBUSAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		/*IARM Wrapper functions*/
		bool IARMBUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_IsConnected(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RequestResource(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_ReleaseResource(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RemoveEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterCall(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusCall(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterEvent(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_GetContext(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
		bool get_LastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response);
		bool InvokeSecondApplication(IN const Json::Value& req, OUT Json::Value& response);
		bool SyncSecondApplication(IN const Json::Value& req, OUT Json::Value& response);
		/*IARMBus Performance test Wrapper functions*/
                bool RegisterMultipleEventHandlers (IN const Json::Value& req, OUT Json::Value& response);
                bool GetLastReceivedEventPerformanceDetails(IN const Json::Value& req, OUT Json::Value& response);
                bool InvokeEventTransmitterApp(IN const Json::Value& req, OUT Json::Value& response);
                std::string testenvPath;
                int keyCode, keyType;

};
#endif //__IARM_STUB_H__
