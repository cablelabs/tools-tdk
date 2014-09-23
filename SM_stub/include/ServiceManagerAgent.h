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
#include "servicemanager.h"

// Includes for services
#include "memoryinfoservice.h"
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

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj) ;
		
};
#endif //__SERVICEMANAGER_AGENT_H__
