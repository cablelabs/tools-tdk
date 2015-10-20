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

#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "servicemanager.h"
using namespace std;

// Includes for services
#ifdef HAS_MEMORY_INFO
#include "memoryinfoservice.h"
#endif
#ifdef SCREEN_CAPTURE
#include "screencaptureservice.h"
#endif
#ifdef HAS_API_HOME_NETWORKING
#include "homenetworkingservice.h"
#endif
#ifdef ENABLE_WEBSOCKET_SERVICE
#include "websocketservice.h"
#endif
#ifdef HAS_FRONT_PANEL
#include "frontpanelservice.h"
#endif
#ifdef HAS_STATE_OBSERVER
#include "stateobserverservice.h"
#endif
#ifdef USE_DISPLAY_SETTINGS
#include "displaysettingsservice.h"
#endif
#ifdef BROWSER_SETTINGS
#include "browsersettingsservice.h"
#endif
#ifdef USE_DEVICE_SETTINGS_SERVICE
#include "devicesettingservice.h"
#endif
#ifdef MSO_PAIRING
#include "msopairingservice.h"
#endif
#ifdef HAS_API_RFREMOTE
#include "rfremoteservice.h"
#endif
#ifdef WAREHOUSE_API
#include "warehouseservice.h"
#endif
#ifdef HAS_API_AVINPUT
#include "avinputservice.h"
#endif
#ifdef HAS_API_SYSTEM
#include "systemservice.h"
#endif
#ifdef USE_TSB_SETTINGS
#include "tsbsettingsservice.h"
#endif
#if defined(ENABLE_VREX_SERVICE)
#include "vrexmanagerservice.h"
#endif
#ifdef USE_STORAGE_MANAGER_API
#include "storagemanagerapi.h"
#endif
#ifdef HAS_API_HDMI_CEC
#include "hdmicecservice.h"
#define ENABLE_CECLOG   "scripts/servicemanager_hdmicec_enable_debuglog.sh"
#endif

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_DETAILS_20  20
#define STR_DETAILS_30  30
#define STR_DETAILS_50  50
#define STR_DETAILS_100 100
#define STR_DETAILS_200 200

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

		// ServiceManager APIs
		bool SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_UnRegisterService(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DoesServiceExist(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_GetRegisteredServices (IN const Json::Value& req, OUT Json::Value& response);
		bool SM_GetGlobalService (IN const Json::Value& req, OUT Json::Value& response);
		bool SM_GetSetting(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_CreateService(IN const Json::Value& req, OUT Json::Value& response);
		// Services common APIs
		bool SM_Services_GetName(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_Services_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_Services_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response);
		// HomeNetworking Service callMethod APIs
		bool SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response);
		// DisplaySettings Service callMethod APIs
		bool SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response);
        	// DeviceSettingService callMethod APIs
		bool SM_DeviceSetting_GetDeviceInfo(IN const Json::Value& req, OUT Json::Value& response);
		// ScreenCaptureService callMethod APIs
		bool SM_ScreenCapture_Upload(IN const Json::Value& req, OUT Json::Value& response);
        	// WebSocketService callMethod APIs
		bool SM_WebSocket_GetUrl(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_WebSocket_GetReadyState(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_WebSocket_GetBufferedAmount(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_WebSocket_GetProtocol(IN const Json::Value& req, OUT Json::Value& response);
		/*HdmiCecService API's*/
		bool SM_HdmiCec_SetEnabled(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_GetEnabled(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_SetName(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_GetName(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_SendMessage(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_OnMessage(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_CheckStatus(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj) ;
		
};
#endif //__SERVICEMANAGER_AGENT_H__
