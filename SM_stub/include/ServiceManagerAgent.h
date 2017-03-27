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
#include "servicelistener.h"
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
#define FLUSH_CECDATA   "scripts/servicemanager_hdmicec_flush_cecdata.sh"
#define CHECK_CECDATA   "scripts/servicemanager_hdmicec_check_cecdata.sh"

#if defined(HAS_PERSISTENT_IN_HDD)
#define CEC_SETTING_ENABLED_FILE "/tmp/mnt/diska3/persistent/ds/cecData"
#elif defined(HAS_PERSISTENT_IN_FLASH)
#define CEC_SETTING_ENABLED_FILE "/opt/persistent/ds/cecData"
#else
#define CEC_SETTING_ENABLED_FILE "/opt/ds/cecData"
#endif

#endif
#ifdef HAS_API_APPLICATION
#include "applicationservice.h"
#include "libIBus.h"
#define CONFIG_FILE "/opt/rmfconfig.ini"
#define IARM_BUS_TDK_NAME "TDK_Agent"
#define OCAP_LOG "/opt/logs/ocapri_log.txt"
#define IP_FILE "/opt/ip.txt"
#endif
#define QT_APP "/opt/TDK/SMEventApp"

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
#include "videoapplicationeventsservice.h"
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
		bool SM_Services_UnRegisterForEvents(IN const Json::Value& req, OUT Json::Value& response);
		// HomeNetworking Service callMethod APIs
		bool SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response);
		// DisplaySettings Service callMethod APIs
		bool SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_DisplaySetting_GetConnectedAudioPorts(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_DisplaySetting_GetSupportedAudioPorts(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_DisplaySetting_GetSupportedAudioModes(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_DisplaySetting_GetSoundMode(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_DisplaySetting_SetSoundMode(IN const Json::Value& req, OUT Json::Value& response);
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
		bool SM_HdmiCec_GetCECAddresses(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_CheckStatus(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_HdmiCec_FlushCecData(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_HdmiCec_CheckCecData(IN const Json::Value& req, OUT Json::Value& response);
                /*ApplicationService APIs*/
                bool SM_AppService_GetAppInfo(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_AppService_SetConnectionReset(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_AppService_Restore_rmfconfig(IN const Json::Value& req, OUT Json::Value& response);
                /*AVInputService APIs*/
                bool SM_AVInputService_GetNumberOfInputs(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_AVInputService_GetCurrentVideoMode(IN const Json::Value& req, OUT Json::Value& response);
                bool SM_AVInputService_IsContentProtected(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_RunSMEvent_QtApp(IN const Json::Value& req, OUT Json::Value& response);
		/*VideoApplicationEventsService APIs*/
		bool SM_VideoApplicationEventsService_SetEnable(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_VideoApplicationEventsService_IsEnableEvent(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_VideoApplicationEventsService_SetApplications(IN const Json::Value& req, OUT Json::Value& response);
		bool SM_VideoApplicationEventsService_GetApplications(IN const Json::Value& req, OUT Json::Value& response);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj) ;
		
};

class HdmiListener : public ServiceListener 
{
public:
	HdmiListener();
	void onServiceEvent(const QString& event, ServiceParams params);
};
 
#endif //__SERVICEMANAGER_AGENT_H__
