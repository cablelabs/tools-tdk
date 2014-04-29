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
#include "mfrMgr.h"
#include "mfrTypes.h"
#include <sys/types.h>
#include <sys/wait.h>
#include "dummytestmgr.h"
#include <fstream>

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false 
#define EVTDATA_MAX_SIZE 3
#define PRE_REQ_CHECK "pre_requisite_chk.txt"
#define DAEMON_EXE "IARMDaemonMain"
#define PWRMGR_EXE "pwrMgrMain"
#define IRMGR_EXE "irMgrMain"
#define MFRMGR_EXE "mfrMgrMain"

class RDKTestAgent;
class IARMBUSAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		IARMBUSAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*IARM Wrapper functions*/
		bool IARMBUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_IsConnected(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RequestResource(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_ReleaseResource(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterCall(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BusCall(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_RegisterEvent(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_GetContext(IN const Json::Value& req, OUT Json::Value& response);
		bool IARMBUSAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
		bool get_LastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response);
		bool InvokeSecondApplication(IN const Json::Value& req, OUT Json::Value& response);
		
};
#endif //__IARM_STUB_H__
