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

#include "libIBus.h"
#include "libIBusDaemon.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

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
		bool FP_setBrightness(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setState(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setColor(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setBlink(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setScroll(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setLevel(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setDB(IN const Json::Value& req, OUT Json::Value& response);
		bool VD_setDFC(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setEncoding(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setCompression(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_setStereoMode(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_setPowerMode(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_setResolution(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_getIndicators(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_getSupportedColors(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_getTextDisplays(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setText(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setTimeFormat(IN const Json::Value& req, OUT Json::Value& response);
		bool FP_setTime(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_loopThru(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_mutedStatus(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getSupportedEncodings(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getSupportedCompressions(IN const Json::Value& req, OUT Json::Value& response);
		bool AOP_getSupportedStereoModes(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_addPowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_removePowerModeListener(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_isDisplayConnected(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_addDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_removeDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_Resolutions(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_HDCPSupport(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_DTCPSupport(IN const Json::Value& req, OUT Json::Value& response);
		bool VOPTYPE_isDynamicResolutionSupported(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getAspectRatio(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_getDisplayDetails(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_isContentProtected(IN const Json::Value& req, OUT Json::Value& response);
		bool VOP_setEnable(IN const Json::Value& req, OUT Json::Value& response);
		bool HOST_getCPUTemperature(IN const Json::Value& req, OUT Json::Value& response);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*DeviceSettingsAgent Wrapper functions*/
};
#endif //__DEVICESETTINGS_AGENT_H__
