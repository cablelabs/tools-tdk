/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#ifndef __SERVICEMANAGER_AGENT_H__
#define __SERVICEMANAGER_AGENT_H__
#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
/*Added QGraphicsView to avoid error from SM component*/
#include <QGraphicsView>
#include "servicemanager.h"
#include "homenetworkingservice.h"
#include "screencaptureservice.h"
#include "displaysettingsservice.h"
#include "devicesettingservice.h"
#include "servicelistener.h"
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false 
class RDKTestAgent;
class ServiceManagerAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		ServiceManagerAgent();

		/*inherited functions*/
		/*ServiceManagerAgent Wrapper functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		bool SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_UnRegisterService(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DoesServiceExist(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_GetRegisteredServices (IN const Json::Value& req, OUT Json::Value& response);
		bool SM_GetGlobalService (IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response);
		     
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj) ;
		
};
#endif //__SERVICEMANAGER_AGENT_H__
