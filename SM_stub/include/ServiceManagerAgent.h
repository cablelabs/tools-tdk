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
#include <unistd.h>
#include <json/json.h>
#include <json/value.h>
#include <QByteArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "servicemanager.h"
#include "servicelistener.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>
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
#ifdef ENABLE_HDCP_PROFILE
#include "hdcpprofileservice.h"
#endif
#ifdef LOGGING_PREFERENCE_MASK
#include "loggingpreferencesservice.h"
#endif
#ifdef HAS_FRONT_PANEL
#include "frontpanelservice.h"
#include "frontPanelIndicator.hpp"
#include "frontPanelConfig.hpp"
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
#ifdef HAS_API_DEVICEDIAGNOSTICS
#include "devicediagnosticsservice.h"
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
#if defined(USE_STORAGE_MANAGER_API) || defined(USE_RDK_STORAGE_MANAGER_V2)
#include "storagemanagerservice.h"
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

#define BUFF_LENGTH 512
#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_DETAILS_20  20
#define STR_DETAILS_30  30
#define STR_DETAILS_50  50
#define STR_DETAILS_100 100
#define STR_DETAILS_200 200
#define SM_MIN_PARAMS 1

class RDKTestAgent;
//class ServiceManagerAgent : public RDKTestStubInterface
class ServiceManagerAgent : public RDKTestStubInterface , public AbstractServer<ServiceManagerAgent>
{
	public:
		ServiceManagerAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <ServiceManagerAgent>(ptrRpcServer)
                {
		  // ServiceManager APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_RegisterService", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_RegisterService);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_UnRegisterService", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_UnRegisterService);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_DoesServiceExist", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_DoesServiceExist);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetRegisteredServices", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_GetRegisteredServices);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetGlobalService", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_GetGlobalService);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetSetting", PARAMS_BY_NAME, JSON_STRING, "service_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_GetSetting);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_CreateService", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_CreateService);
		  // Services common APIs
		  this->bindAndAddMethod(Procedure("TestMgr_Services_GetName", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_Services_GetName);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_SetAPIVersion", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, "apiVersion",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_Services_SetAPIVersion);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_RegisterForEvents", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, "event_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_Services_RegisterForEvents);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_UnRegisterForEvents", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, "event_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_Services_UnRegisterForEvents);
		  // HomeNetworking Service callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_EnableMDVR", PARAMS_BY_NAME,JSON_STRING, "enable",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HN_EnableMDVR);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_EnableVPOP", PARAMS_BY_NAME, JSON_STRING, "enable",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HN_EnableVPOP);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_SetDeviceName", PARAMS_BY_NAME,JSON_STRING, "device_name",JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_SetDeviceName);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_IsVPOPEnabled",PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_IsVPOPEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_IsMDVREnabled", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_IsMDVREnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_GetDeviceName", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_GetDeviceName);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_IsUpnpEnabled", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_IsUpnpEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_SetUpnpEnabled", PARAMS_BY_NAME,JSON_STRING, "enable",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HN_SetUpnpEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_IsVidiPathEnabled", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HN_IsVidiPathEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HN_SetVidiPathEnabled", PARAMS_BY_NAME,JSON_STRING, "enable",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HN_SetVidiPathEnabled);
		  // DisplaySettings Service callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_DisplaySetting_SetZoomSettings", PARAMS_BY_NAME,JSON_STRING, "videoDisplay",JSON_STRING, "zoomLevel",JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_SetZoomSettings);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_DisplaySetting_SetCurrentResolution", PARAMS_BY_NAME,JSON_STRING, "videoDisplay",JSON_STRING, "resolution",JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_SetCurrentResolution);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetConnectedAudioPorts", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_GetConnectedAudioPorts);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetSupportedAudioPorts", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_GetSupportedAudioPorts);
		  this->bindAndAddMethod(Procedure("SM_DisplaySetting_GetSoundMode", PARAMS_BY_NAME,JSON_STRING, "portName",JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_GetSoundMode);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_SetSoundMode", PARAMS_BY_NAME,JSON_STRING, "portName",JSON_STRING, "audioMode",JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_SetSoundMode);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_GetSupportedAudioModes", PARAMS_BY_NAME,JSON_STRING, "portName",JSON_STRING, NULL), &ServiceManagerAgent::SM_DisplaySetting_GetSupportedAudioModes);
		  // DeviceSettingService callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_DeviceSetting_GetDeviceInfo", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_DeviceSetting_GetDeviceInfo);
	          // ScreenCaptureService callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_ScreenCapture_Upload", PARAMS_BY_NAME,JSON_STRING, "url",JSON_STRING, NULL), &ServiceManagerAgent::SM_ScreenCapture_Upload);
        	  // WebSocketService callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_WebSocket_GetUrl", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_WebSocket_GetUrl);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_WebSocket_GetReadyState", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_WebSocket_GetReadyState);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_WebSocket_GetBufferedAmount", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_WebSocket_GetBufferedAmount);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_WebSocket_GetProtocol", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_WebSocket_GetProtocol);
        	  //HdmiCecService API's
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_SetEnabled", PARAMS_BY_NAME,JSON_STRING, "valueToSetEnabled",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HdmiCec_SetEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_GetEnabled", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_GetEnabled);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_SetName", PARAMS_BY_NAME,JSON_STRING, "nameToSet",JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_SetName);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_GetName", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_GetName);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_GetConnectedDevices", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_GetConnectedDevices);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_SendMessage", PARAMS_BY_NAME,JSON_STRING, "messageToSend",JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_SendMessage);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_OnMessage", PARAMS_BY_NAME,JSON_STRING, "onMessage",JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_OnMessage);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_GetCECAddresses", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_GetCECAddresses);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_ClearCecLog", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_ClearCecLog);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_CheckStatus", PARAMS_BY_NAME,JSON_STRING, "pattern",JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_CheckStatus);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_FlushCecData", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_FlushCecData);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_HdmiCec_CheckCecData", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_HdmiCec_CheckCecData);
		  //ApplicationService APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AppService_GetAppInfo", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_AppService_GetAppInfo);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AppService_setConnectionReset", PARAMS_BY_NAME,JSON_STRING, "applicationID",JSON_STRING, "connectionID",JSON_STRING, "connectionResetLevel",JSON_STRING, NULL), &ServiceManagerAgent::SM_AppService_SetConnectionReset);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AppService_Restore_rmfconfig", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_AppService_Restore_rmfconfig);
   	          //AVInputService APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AVInputService_GetNumberOfInputs", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_AVInputService_GetNumberOfInputs);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AVInputService_GetCurrentVideoMode", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_AVInputService_GetCurrentVideoMode);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_AVInputService_IsContentProtected", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_AVInputService_IsContentProtected);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_RunSMEvent_QtApp", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, "event_name",JSON_STRING, "event_param",JSON_STRING, NULL), &ServiceManagerAgent::SM_RunSMEvent_QtApp);
		  //VideoApplicationEventsService APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_VideoApplicationEventsService_SetEnable", PARAMS_BY_NAME,JSON_STRING, "valueToSetEnabled",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_VideoApplicationEventsService_SetEnable);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_VideoApplicationEventsService_IsEnableEvent", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_VideoApplicationEventsService_IsEnableEvent);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_VideoApplicationEventsService_SetApplications", PARAMS_BY_NAME,JSON_STRING, "appString",JSON_STRING, "count",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_HdmiCec_OnMessage);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_VideoApplicationEventsService_GetApplications", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_VideoApplicationEventsService_GetApplications);
		  //Device Diagnistics Service APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_DDS_GetConfiguration", PARAMS_BY_NAME,JSON_STRING, "names",JSON_STRING, NULL), &ServiceManagerAgent::SM_DDS_GetConfiguration);
         	  //Front Panel Service APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_GetBrightness", PARAMS_BY_NAME,JSON_STRING, "LEDName",JSON_STRING, NULL), &ServiceManagerAgent::SM_FP_GetBrightness);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_SetBrightness", PARAMS_BY_NAME,JSON_STRING, "LEDName",JSON_STRING, "LEDBrightness",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_SetBrightness);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_SetLED", PARAMS_BY_NAME,JSON_STRING, "LEDName",JSON_STRING, "LEDBrightness",JSON_INTEGER, "LEDColorRed",JSON_INTEGER, "LEDColorBlue",JSON_INTEGER, "LEDColorGreen",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_SetLED);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_SetAPIVersion", PARAMS_BY_NAME,JSON_STRING, "apiVersion",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_SetAPIVersion);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_SetPreferences", PARAMS_BY_NAME, JSON_STRING, "LEDName",JSON_STRING, "LEDBrightness",JSON_INTEGER, "LEDColorRed",JSON_INTEGER, "LEDColorBlue",JSON_INTEGER, "LEDColorGreen",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_SetPreferences);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_GetPreferences", PARAMS_BY_NAME, JSON_STRING, "LEDName",JSON_STRING, NULL), &ServiceManagerAgent::SM_FP_GetPreferences);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_SetBlink", PARAMS_BY_NAME,JSON_STRING, "LEDName",JSON_STRING, "LEDBrightness",JSON_STRING, "LEDColorRed",JSON_STRING, "LEDColorBlue",JSON_STRING, "LEDColorGreen",JSON_STRING, "BlinkDuration",JSON_STRING, "IterationCount",JSON_INTEGER, "SequenceCount",JSON_STRING, NULL), &ServiceManagerAgent::SM_FP_SetBlink);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_Set_24_Hour_Clock", PARAMS_BY_NAME,JSON_STRING, "is24hour",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_Set_24_Hour_Clock);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_FP_Is_24_Hour_Clock", PARAMS_BY_NAME,JSON_STRING, NULL), &ServiceManagerAgent::SM_FP_Is_24_Hour_Clock);
         	  //Generic Stub for callMethod APIs
		  this->bindAndAddMethod(Procedure("TestMgr_SM_Generic_CallMethod", PARAMS_BY_NAME,JSON_STRING, "service_name",JSON_STRING, "method_name",JSON_STRING, "inputCount",JSON_INTEGER, NULL), &ServiceManagerAgent::SM_FP_SetPreferences);
		  this->bindAndAddMethod(Procedure("TestMgr_SM_ExecuteCmd", PARAMS_BY_NAME,JSON_STRING, "command",JSON_STRING, NULL), &ServiceManagerAgent::SM_ExecuteCmd);
                }

		/*Ctor*/
		//ServiceManagerAgent();

		/*inherited functions*/
		/*ServiceManagerAgent Wrapper functions*/
		bool initialize(IN const char* szVersion);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

		// ServiceManager APIs
		void SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response);
		void SM_UnRegisterService(IN const Json::Value& req, OUT Json::Value& response);
		void SM_DoesServiceExist(IN const Json::Value& req, OUT Json::Value& response);
		void SM_GetRegisteredServices (IN const Json::Value& req, OUT Json::Value& response);
		void SM_GetGlobalService (IN const Json::Value& req, OUT Json::Value& response);
		void SM_GetSetting(IN const Json::Value& req, OUT Json::Value& response);
		void SM_CreateService(IN const Json::Value& req, OUT Json::Value& response);
		// Services common APIs
		void SM_Services_GetName(IN const Json::Value& req, OUT Json::Value& response);
		void SM_Services_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response);
		void SM_Services_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response);
		void SM_Services_UnRegisterForEvents(IN const Json::Value& req, OUT Json::Value& response);
		// HomeNetworking Service callMethod APIs
		void SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HN_IsMDVREnabled(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_IsVPOPEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_GetDeviceName(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_IsUpnpEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_SetUpnpEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_IsVidiPathEnabled(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HN_SetVidiPathEnabled(IN const Json::Value& req, OUT Json::Value& response);
		// DisplaySettings Service callMethod APIs
		void SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response);
		void SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response);
                void SM_DisplaySetting_GetConnectedAudioPorts(IN const Json::Value& req, OUT Json::Value& response);
                void SM_DisplaySetting_GetSupportedAudioPorts(IN const Json::Value& req, OUT Json::Value& response);
                void SM_DisplaySetting_GetSupportedAudioModes(IN const Json::Value& req, OUT Json::Value& response);
                void SM_DisplaySetting_GetSoundMode(IN const Json::Value& req, OUT Json::Value& response);
                void SM_DisplaySetting_SetSoundMode(IN const Json::Value& req, OUT Json::Value& response);
        	// DeviceSettingService callMethod APIs
		void SM_DeviceSetting_GetDeviceInfo(IN const Json::Value& req, OUT Json::Value& response);
		// ScreenCaptureService callMethod APIs
		void SM_ScreenCapture_Upload(IN const Json::Value& req, OUT Json::Value& response);
        	// WebSocketService callMethod APIs
		void SM_WebSocket_GetUrl(IN const Json::Value& req, OUT Json::Value& response);
		void SM_WebSocket_GetReadyState(IN const Json::Value& req, OUT Json::Value& response);
		void SM_WebSocket_GetBufferedAmount(IN const Json::Value& req, OUT Json::Value& response);
		void SM_WebSocket_GetProtocol(IN const Json::Value& req, OUT Json::Value& response);
		/*HdmiCecService API's*/
		void SM_HdmiCec_SetEnabled(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_GetEnabled(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_SetName(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_GetName(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_SendMessage(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_OnMessage(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_GetCECAddresses(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_CheckStatus(IN const Json::Value& req, OUT Json::Value& response);
		void SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HdmiCec_FlushCecData(IN const Json::Value& req, OUT Json::Value& response);
                void SM_HdmiCec_CheckCecData(IN const Json::Value& req, OUT Json::Value& response);
                /*ApplicationService APIs*/
                void SM_AppService_GetAppInfo(IN const Json::Value& req, OUT Json::Value& response);
                void SM_AppService_SetConnectionReset(IN const Json::Value& req, OUT Json::Value& response);
                void SM_AppService_Restore_rmfconfig(IN const Json::Value& req, OUT Json::Value& response);
                /*AVInputService APIs*/
                void SM_AVInputService_GetNumberOfInputs(IN const Json::Value& req, OUT Json::Value& response);
                void SM_AVInputService_GetCurrentVideoMode(IN const Json::Value& req, OUT Json::Value& response);
                void SM_AVInputService_IsContentProtected(IN const Json::Value& req, OUT Json::Value& response);
		void SM_RunSMEvent_QtApp(IN const Json::Value& req, OUT Json::Value& response);
		/*VideoApplicationEventsService APIs*/
		void SM_VideoApplicationEventsService_SetEnable(IN const Json::Value& req, OUT Json::Value& response);
		void SM_VideoApplicationEventsService_IsEnableEvent(IN const Json::Value& req, OUT Json::Value& response);
		void SM_VideoApplicationEventsService_SetApplications(IN const Json::Value& req, OUT Json::Value& response);
		void SM_VideoApplicationEventsService_GetApplications(IN const Json::Value& req, OUT Json::Value& response);
		/*DeviceDiagnosticsService APIs*/
		void SM_DDS_GetConfiguration(IN const Json::Value& req, OUT Json::Value& response);
                 /*Front panel Service APIs*/
                void SM_FP_SetBrightness(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_GetBrightness(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_SetLED(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_SetPreferences(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_GetPreferences(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_SetBlink(IN const Json::Value& req, OUT Json::Value& response);

                void SM_FP_Set_24_Hour_Clock(IN const Json::Value& req, OUT Json::Value& response);
                void SM_FP_Is_24_Hour_Clock(IN const Json::Value& req, OUT Json::Value& response);

		/* Generic Stub for callMethod*/
		void SM_Generic_CallMethod (IN const Json::Value& req, OUT Json::Value& response);

                void SM_ExecuteCmd (IN const Json::Value& req, OUT Json::Value& response);
			

		bool cleanup(IN const char* szVersion) ;
		
};

class HdmiListener : public ServiceListener 
{
public:
	HdmiListener();
	void onServiceEvent(const QString& event, ServiceParams params);
};
 
#endif //__SERVICEMANAGER_AGENT_H__
