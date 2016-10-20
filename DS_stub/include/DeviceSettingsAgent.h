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

#ifndef __DEVICESETTINGS_AGENT_H__
#define __DEVICESETTINGS_AGENT_H__
#include <json/json.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "host.hpp"
#include "videoOutputPort.hpp"
#include "videoOutputPortType.hpp"
#include "videoOutputPortConfig.hpp"
#include "videoDeviceConfig.hpp"
#include "videoResolution.hpp"
#include "manager.hpp"
#include "dsUtl.h"
#include "dsError.h"
#include "list.hpp"
#include "frontPanelConfig.hpp"
#include "frontPanelIndicator.hpp"
#include "frontPanelTextDisplay.hpp"
#include "audioEncoding.hpp"
#include "audioCompression.hpp"
#include "audioStereoMode.hpp"
#include "manager.hpp"
#include "audioOutputPort.hpp"
#include "audioOutputPortType.hpp"
#include "audioOutputPortConfig.hpp"
#include "pixelResolution.hpp"

#include "libIBus.h"
#include "libIBusDaemon.h"
#include "mfrMgr.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_LEN   128
#define LINE_LEN  1024
#define MFRMGR    "mfrMgrMain"

class PowerChangeNotify: public device::PowerModeChangeListener
{
	public:
		void powerModeChanged(int newMode)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nPower Mode Changed to:%d",newMode);
			return;
		}
};

class DispChangeNotify:public device::DisplayConnectionChangeListener
{
	public:
		void displayConnectionChanged(device::VideoOutputPort &port, int newConnectionStatus)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nDisplay Connections status: CONNECTED(0):DISCONNECTED(1):%d",newConnectionStatus);
			return;
		}
};


class RDKTestAgent;
class DeviceSettingsAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		DeviceSettingsAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		bool DSmanagerInitialize(IN const Json::Value& req, OUT Json::Value& response);
		bool DSmanagerDeinitialize(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_setBrightness(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_setState(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_setColor(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_setBlink(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_setScroll(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setLevel(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setDB(IN const Json::Value& req, OUT Json::Value& response);
		bool VD_setDFC(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setEncoding(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setCompression(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setStereoMode(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_setPowerMode(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_setResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getIndicators(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_getSupportedColors(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getTextDisplays(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_setText(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_setTimeFormat(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_setTime(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_loopThru(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_mutedStatus(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPTYPE_getSupportedEncodings(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPTYPE_getSupportedCompressions(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPTYPE_getSupportedStereoModes(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_addPowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_removePowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_isDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_addDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_removeDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_Resolutions(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_isHDCPSupported(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_enableHDCP(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getHDCPStatus(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_isDynamicResolutionSupported(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getAspectRatio(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getDisplayDetails(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_isContentProtected(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_setEnable(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getCPUTemperature(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_setVersion(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_setPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getPreferredSleepMode(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getAvailableSleepModes(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getVideoOutputPorts(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getAudioOutputPorts(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getVideoDevices(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getVideoOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getVideoOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getAudioOutputPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getAudioOutputPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getHostEDID(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_getBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response);
		bool FPI_getColorMode(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_getTextColorMode(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_getTextBrightnessLevels(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_setTextBrightness(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_getTextBrightness(IN const Json::Value& req, OUT Json::Value& response);
		bool FPTEXT_enableDisplay(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getIndicatorFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getIndicatorFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getTextDisplayFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getTextDisplayFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool FPCONFIG_getColors(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_getPorts(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_release(IN const Json::Value& req, OUT Json::Value& response);
		bool AOPCONFIG_load(IN const Json::Value& req, OUT Json::Value& response);
		//bool AOPTYPE_addEncoding(IN const Json::Value& req, OUT Json::Value& response);
		//bool AOPTYPE_addCompression(IN const Json::Value& req, OUT Json::Value& response);
		//bool AOPTYPE_addStereoMode(IN const Json::Value& req, OUT Json::Value& response);
		//bool AOPTYPE_addPort(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setStereoAuto(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getStereoAuto(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getGain(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getOptimalLevel(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getDefaultResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_isActive(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_setDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_hasSurround(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getEDIDBytes(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_getSupportedResolutions(IN const Json::Value& req, OUT Json::Value& response);
		//bool VOPTYPE_addPort(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_getPorts(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_setRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_getRestrictedResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getPixelResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getSSMode(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getVideoResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getFrameRate(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getPortType(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getPortFromName(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getPortFromId(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPCONFIG_getSupportedTypes(IN const Json::Value& req, OUT Json::Value& response);
		//bool VOPCONFIG_release(IN const Json::Value& req, OUT Json::Value& response);
		//bool VOPCONFIG_load(IN const Json::Value& req, OUT Json::Value& response);
		bool VD_setPlatformDFC(IN const Json::Value& req, OUT Json::Value& response);
		bool VD_getSupportedDFCs(IN const Json::Value& req, OUT Json::Value& response);
		//bool VD_addDFC(IN const Json::Value& req, OUT Json::Value& response);
		bool VDCONFIG_getDevices(IN const Json::Value& req, OUT Json::Value& response);
		bool VDCONFIG_getDFCs(IN const Json::Value& req, OUT Json::Value& response);
		bool VDCONFIG_getDefaultDFC(IN const Json::Value& req, OUT Json::Value& response);
		//bool VDCONFIG_release(IN const Json::Value& req, OUT Json::Value& response);
		//bool VDCONFIG_load(IN const Json::Value& req, OUT Json::Value& response);
		bool VR_isInterlaced(IN const Json::Value& req, OUT Json::Value& response);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*DeviceSettingsAgent Wrapper functions*/
};
#endif //__DEVICESETTINGS_AGENT_H__
