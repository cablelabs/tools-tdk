/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include "DeviceSettingsAgent.h"

/*creating Objects for power and display classes*/
PowerChangeNotify power_obj;
DispChangeNotify display_obj;

/***************************************************************************
 *Function name	: DeviceSettingsAgent 
 *Descrption	: This is a constructor function for DeviceSettingsAgent class. 
 *****************************************************************************/ 
DeviceSettingsAgent::DeviceSettingsAgent()
{
	DEBUG_PRINT(DEBUG_LOG,"DeviceSettingsAgent Initialized");
}

/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 *****************************************************************************/ 

bool DeviceSettingsAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"DeviceSettingsAgent Initialize");
	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::DSmanagerInitialize, "TestMgr_DS_managerInitialize");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::DSmanagerDeinitialize, "TestMgr_DS_managerDeinitialize");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setBrightness, "TestMgr_DS_FP_setBrightness");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setState, "TestMgr_DS_FP_setState");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setColor, "TestMgr_DS_FP_setColor");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setBlink, "TestMgr_DS_FP_setBlink");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setScroll, "TestMgr_DS_FP_setScroll");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_setLevel, "TestMgr_DS_AOP_setLevel");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_setDB, "TestMgr_DS_AOP_setDB");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VD_setDFC, "TestMgr_DS_VD_setDFC");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_setEncoding, "TestMgr_DS_AOP_setEncoding");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_setCompression, "TestMgr_DS_AOP_setCompression");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_setStereoMode, "TestMgr_DS_AOP_setStereoMode");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_setPowerMode, "TestMgr_DS_HOST_setPowerMode");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_setResolution, "TestMgr_DS_VOP_setResolution");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_getIndicators, "TestMgr_DS_FP_getIndicators");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_getSupportedColors, "TestMgr_DS_FP_FP_getSupportedColors");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_getTextDisplays, "TestMgr_DS_FP_getTextDisplays");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setText, "TestMgr_DS_FP_setText");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setTimeFormat, "TestMgr_DS_FP_setTimeForamt");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::FP_setTime, "TestMgr_DS_FP_setTime");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_loopThru, "TestMgr_DS_AOP_loopThru");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_mutedStatus, "TestMgr_DS_AOP_mutedStatus");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_getSupportedEncodings, "TestMgr_DS_AOP_getSupportedEncodings");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_getSupportedCompressions, "TestMgr_DS_AOP_getSupportedCompressions");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::AOP_getSupportedStereoModes, "TestMgr_DS_AOP_getSupportedStereoModes");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_addPowerModeListener, "TestMgr_DS_HOST_addPowerModeListener");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_removePowerModeListener, "TestMgr_DS_HOST_removePowerModeListener");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_isDisplayConnected, "TestMgr_DS_VOP_isDisplayConnected");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_addDisplayConnectionListener, "TestMgr_DS_HOST_addDisplayConnectionListener");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_removeDisplayConnectionListener, "TestMgr_DS_HOST_removeDisplayConnectionListener");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_Resolutions, "TestMgr_DS_HOST_Resolutions");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOPTYPE_isHDCPSupported, "TestMgr_DS_VOPTYPE_isHDCPSupported");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOPTYPE_enableHDCP, "TestMgr_DS_VOPTYPE_enableHDCP");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_getHDCPStatus, "TestMgr_DS_VOP_getHDCPStatus");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOPTYPE_DTCPSupport, "TestMgr_DS_VOPTYPE_DTCPSupport");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOPTYPE_isDynamicResolutionSupported, "TestMgr_DS_VOPTYPE_isDynamicResolutionSupported");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_getAspectRatio, "TestMgr_DS_VOP_getAspectRatio");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_getDisplayDetails, "TestMgr_DS_VOP_getDisplayDetails");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_isContentProtected, "TestMgr_DS_VOP_isContentProtected");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::VOP_setEnable, "TestMgr_DS_VOP_setEnable");
	ptrAgentObj->RegisterMethod(*this,&DeviceSettingsAgent::HOST_getCPUTemperature, "TestMgr_DS_HOST_getCPUTemperature");

	/*initializing IARMBUS library */
	IARM_Result_t retval;
	retval=IARM_Bus_Init("agent");
	DEBUG_PRINT(DEBUG_LOG,"\nInit retval:%d\n",retval);
	if(retval==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully initializes the IARMBUS library\n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application failed to initializes the IARMBUS library\n");
	}	
	DEBUG_PRINT(DEBUG_LOG,"\n Calling IARM_BUS_Connect\n");
	/*connecting application with IARM BUS*/
	IARM_Bus_Connect();
	DEBUG_PRINT(DEBUG_LOG,"\n Application Successfully connected with IARMBUS \n");

	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string DeviceSettingsAgent::testmodulepre_requisites()
{
	return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the 
 *                pre-requisites that are set
 *                
 *****************************************************************************/

bool DeviceSettingsAgent::testmodulepost_requisites()
{
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: DSmanagerInitialize
 *Descrption	: This function is to initialize device settings library.
 *****************************************************************************/ 
bool DeviceSettingsAgent::DSmanagerInitialize(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n managerInitialize ---->Entry\n");
	try
	{
		device::Manager::Initialize();
		response["result"]= "SUCCESS"; 
		response["details"]="device::Manager::Initialize SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in DSmanagerinitialize\n");
		response["result"]= "FAILURE";
		response["details"]="device::Manager::Initialize FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n managerInitialize ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: DSmanagerDeinitialize
 *Descrption	: This function is to DeInitialize device settings library.
 *****************************************************************************/ 
bool DeviceSettingsAgent::DSmanagerDeinitialize(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n managerDeinitialize ---->Entry\n");
	try
	{
		device::Manager::DeInitialize();
		response["result"]= "SUCCESS"; 
		response["details"]="device::Manager::DeInitialize SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in DSmanagerDeinitialize\n");
		response["result"]= "FAILURE";
		response["details"]="device::Manager::DeInitialize FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n managerDeinitialize ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: FP_setBrightness
 *Descrption	: This function is to check the functionality of setBrightness and getBrightness APIs
 *@param  [in]	: req- 	indicator_name: indicator name for which the Brightness will be set and get.
			    brightness: brightness level
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setBrightness ---->Entry\n");
	char brightnessDetails[30] = {'\0'};
	int setVal = req["brightness"].asInt();
	bool getOnly = req["get_only"].asInt();
	std::string message = req["text"].asCString();
	int getVal;

	try
	{
            if(message.empty()) // frontPanelConfig
            {
		std::string indicator_name=req["indicator_name"].asCString();
                if (false == getOnly) {
                    DEBUG_PRINT(DEBUG_LOG,"\nCalling setBrightness with value(%d)\n", setVal);
                    device::FrontPanelIndicator::getInstance(indicator_name).setBrightness(setVal);
                }

                DEBUG_PRINT(DEBUG_LOG,"\nCalling getBrightness\n");
                device::FrontPanelIndicator::getInstance(indicator_name).setState(true);
                getVal = device::FrontPanelIndicator::getInstance(indicator_name).getBrightness();
            }
	    else // frontPanelTextDisplay
	    {
		if (false == getOnly) {
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling setText with value (%s)\n", message.c_str());
		    device::FrontPanelTextDisplay::getInstance("Text").setText(message);
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling setTextBrightness with value(%d)\n", setVal);
		    device::FrontPanelTextDisplay::getInstance("Text").setTextBrightness(setVal);
		}

		DEBUG_PRINT(DEBUG_LOG,"\nCalling getTextBrightness\n");
		getVal = device::FrontPanelTextDisplay::getInstance("Text").getTextBrightness();
	    }

	    DEBUG_PRINT(DEBUG_LOG,"\nBrightness: get value(%d)\n", getVal);
	    sprintf(brightnessDetails,"%d",getVal);
	    response["details"]= brightnessDetails;

            if ((false == getOnly) && (setVal != getVal))
	    {
                response["result"]= "FAILURE";
            }
	    else
            {
		response["result"]= "SUCCESS";
	    }
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setBrightness\n");
		response["details"]= "Exception Caught in FP_setBrightness";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setBrightness ---->Exit\n");
	return TEST_SUCCESS;	
}

/***************************************************************************
 *Function name : FP_setState
 *Descrption    : This function is to check the functionality of FrontPanel setState API
 *@param  [in]  : indicator_name: indicator name for which the state will be set.
                  state: 0 (OFF) / 1 (ON)
 *****************************************************************************/
bool DeviceSettingsAgent::FP_setState(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"FP_setState ---->Entry\n");
        char details[30] = {'\0'};
        bool state = req["state"].asInt();
	std::string indicator_name = req["indicator_name"].asCString();

        try
        {
            device::FrontPanelIndicator::getInstance(indicator_name).setState(state);
            DEBUG_PRINT(DEBUG_LOG,"\nState set to %d\n", state);
            sprintf(details,"State set to %d",state);
            response["details"]= details;
            response["result"]= "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setState\n");
                response["details"]= "Exception Caught in FP_setState";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"FP_setState ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: FP_setColor
 *Descrption	: This function is to check the functionality of setColor and getColor APIs
 *@param  [in]	: req- 	indicator_name: indicator name for which the color will be set and get.
				 color: color id.
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setColor(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setColor ---->Entry\n");
	if(&req["indicator_name"]==NULL || &req["color"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string indicator_name=req["indicator_name"].asCString();
	char colorDetails1[20]="Color:";
	int color=req["color"].asInt();
	DEBUG_PRINT(DEBUG_LOG,"\ncolor to set:%d\n",color);
	char *colorDetails = (char*)malloc(sizeof(char)*20);
	memset(colorDetails , '\0', (sizeof(char)*20));
	int colorid;
	/*Creating object for Color*/
	device::FrontPanelIndicator::Color c(color);
	try
	{
		/*calling setcolor*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setColor\n");
		device::FrontPanelConfig::getInstance().getIndicator(indicator_name).setColor(c);
		/*calling getcolor*/
		//colorid=device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getColor().getId();
		colorid=device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getColor();
		DEBUG_PRINT(DEBUG_LOG,"\ncolor id is:%d\n",colorid);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getColor\n");
		sprintf(colorDetails,"%d",colorid);
		strcat(colorDetails1,colorDetails);
		DEBUG_PRINT(DEBUG_LOG,"\ncolor details:%s\n",(char*)colorDetails1);
		response["details"]= colorDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setColor\n");
		response["details"]= "Exception Caught in FP_setColor";
		response["result"]= "FAILURE";
	}
	free(colorDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setColor ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: FP_setBlink
 *Descrption	: This function is to check the functionality of setBlink and 
 getBlink APIs
 *@param [in]	: req- 	indicator_name: indicator name for which the Blink rate 
					will be set and get.
			blink_interval: blink rate.
		       blink_iteration: Number of iteration for the blink.
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setBlink(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setBlink ---->Entry\n");
	if(&req["indicator_name"]==NULL || &req["blink_interval"]==NULL || &req["blink_iteration"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string indicator_name=req["indicator_name"].asCString();
	char blinkDetails1[20]="Blink Rate:";
	int interval=req["blink_interval"].asInt();
	int iteration=req["blink_iteration"].asInt();
	char *blinkInterval = (char*)malloc(sizeof(char)*20);
	memset(blinkInterval,'\0', (sizeof(char)*20));
	char *blinkIteration = (char*)malloc(sizeof(char)*20);
	memset(blinkIteration,'\0', (sizeof(char)*20));
	/*Creating object for blink*/
	try
	{
		/*calling setBlink*/
		device::FrontPanelIndicator::Blink p(interval,iteration);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setBlink\n");
		device::FrontPanelConfig::getInstance().getIndicator(indicator_name).setBlink(p);
		/*calling getBlink*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getBlink\n");
		p=device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getBlink();
		sprintf(blinkInterval,"%d",p.getInterval());
		DEBUG_PRINT(DEBUG_LOG,"\nblinkInterval:%d\n",p.getInterval());
		sprintf(blinkIteration,"%d",p.getIteration());
		DEBUG_PRINT(DEBUG_LOG,"\nblinkIteration:%d\n",p.getIteration());
		strcat(blinkDetails1,blinkInterval);
		strcat(blinkDetails1,"::");
		strcat(blinkDetails1,blinkIteration);
		response["details"]= blinkDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setBlink\n");
		response["details"]= "Exception Caught in FP_setBlink";
		response["result"]= "FAILURE";
	}
	free(blinkInterval);
	free(blinkIteration);
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setBlink ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: FP_setScroll
 *Descrption  	: This function is to check the functionality of setScroll and 
 getScroll APIs
 *@param  [in]	: req- 	text: input for scrolling the text in the 7-segment LEDs for 
                              the given iterations.
	       hold_duration: Duration for scroll hold
               hiteration   : Number of Horizontal Iterations
               viteration   : Number of Vertical Iterations
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setScroll(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setScroll ---->Entry\n");
	if(&req["text"]==NULL||&req["viteration"]==NULL||&req["hiteration"]==NULL||&req["hold_duration"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string text_display=req["text"].asCString();
	char scrollDetails1[20]="Scroll :: ";
	int viteraion=req["viteration"].asInt();
	int hiteraion=req["hiteration"].asInt();
	int holdDuration=req["hold_duration"].asInt();
	char *viterationDetails = (char*)malloc(sizeof(char)*20);
	memset(viterationDetails,'\0', (sizeof(char)*20));
	char *hIterationsDetails = (char*)malloc(sizeof(char)*20);
	memset(hIterationsDetails,'\0', (sizeof(char)*20));
	char *holdDurationDetails = (char*)malloc(sizeof(char)*20);
	memset(holdDurationDetails,'\0', (sizeof(char)*20));
	try
	{
		/*Creating object for Scroll*/
		device::FrontPanelTextDisplay::Scroll s(viteraion,hiteraion,holdDuration);
		device::FrontPanelTextDisplay::Scroll s_obj;
		/*calling setScroll info*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setScroll\n");
		device::FrontPanelConfig::getInstance().getTextDisplay(text_display).setScroll(s);
		/*calling getScroll info*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getScroll\n");
		s_obj=device::FrontPanelConfig::getInstance().getTextDisplay(text_display).getScroll();
		sprintf(viterationDetails,"%d",s_obj.getVerticalIteration());
		sprintf(hIterationsDetails,"%d",s_obj.getHorizontalIteration());
		sprintf(holdDurationDetails,"%d",s_obj.getHoldDuration());
		strcat(scrollDetails1,viterationDetails);
		strcat(scrollDetails1,":");
		strcat(scrollDetails1,hIterationsDetails);
		strcat(scrollDetails1,":");
		strcat(scrollDetails1,holdDurationDetails);
		response["details"]= scrollDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setScroll\n");
		response["details"]= "Exception Caught in FP_setScroll";
		response["result"]= "FAILURE";
	}
	free(viterationDetails);
	free(hIterationsDetails);
	free(holdDurationDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setScroll ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: AOP_setLevel
 *Descrption	: This function is to check the functionality of setLevel and 
                  getLevel APIs
 *@param [in]	: req- 	port_name: video port(corresponding audio) for which audio level will be set and get.
                      audio_level: audio level for a given output audio port
 *****************************************************************************/ 
bool DeviceSettingsAgent::AOP_setLevel(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setLevel ---->Entry\n");
	if(&req["port_name"]==NULL || &req["audio_level"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char levelDetails1[20] ="Audio Level:";
	float level=req["audio_level"].asFloat();
	printf("\nLevel:%f\n\n",level);
	float audio_level;
	char *levelDetails = (char*)malloc(sizeof(char)*20);
	memset(levelDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setLevel\n");
		aPort.setLevel(level);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getLevel\n");
		audio_level=aPort.getLevel();
		sprintf(levelDetails,"%.3f",audio_level);
		strcat(levelDetails1,levelDetails);
		response["details"]= levelDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setLevel\n");
		response["details"]= "Exception Caught in AOP_setLevel";
		response["result"]= "FAILURE";
	}
	free(levelDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setLevel ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: AOP_setDB 
 *Descrption 	: This function is to check the functionality of setDB and 
                  getDB APIs.This also checks maximum and minimum DB values
 *@param  [in]	: req- 	port_name: video port( corresponding audio) for which audio DB value will be set and get.
                         db_level: audio DB level for a given output audio port
 *****************************************************************************/ 

bool DeviceSettingsAgent::AOP_setDB(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setDB ---->Entry\n");
	if(&req["port_name"]==NULL||&req["db_level"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char dBDetails1[60] ="DB:";
	char maxDBDetails1[20] ="maxDB:";
	char minDBDetails1[20] ="minDB:";
	float maxDB,minDB;
	float dBValue = req["db_level"].asFloat();
	float dBval;
	char *dBDetails = (char*)malloc(sizeof(char)*20);
	memset(dBDetails,'\0', (sizeof(char)*20));
	char *maxDBDetails = (char*)malloc(sizeof(char)*20);
	memset(maxDBDetails,'\0', (sizeof(char)*20));
	char *minDBDetails = (char*)malloc(sizeof(char)*20);
	memset(minDBDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setDB\n");
		aPort.setDB(dBValue);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getDB\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetDB:%f\n",aPort.getDB());
		dBval = aPort.getDB();
		sprintf(dBDetails,"%f",dBval);
		strcat(dBDetails1,dBDetails);
		/*getting maxDB and minDB of audio*/
		maxDB=aPort.getMaxDB();
		minDB=aPort.getMinDB();
		sprintf(maxDBDetails,"%f",maxDB);
		strcat(maxDBDetails1,maxDBDetails);
		sprintf(minDBDetails,"%f",minDB);
		strcat(minDBDetails1,minDBDetails);
		strcat(dBDetails1,",");
		strcat(dBDetails1,maxDBDetails1);
		strcat(dBDetails1,",");
		strcat(dBDetails1,minDBDetails1);
		/*Copying the audio DB details to json details parameter*/
		response["details"]= dBDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setDB\n");
		response["details"]= "Exception Caught in AOP_setDB";
		response["result"]= "FAILURE";
	}
	free(dBDetails);
	free(maxDBDetails);
	free(minDBDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setDB ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VD_setDFC 
 *Descrption 	: This function is to check the functionality of setDFC and 
                  getDFC APIs.
 *@param  [in]	: req- 	zoom_setting: new zoom setting for the video device.
 *****************************************************************************/ 

bool DeviceSettingsAgent::VD_setDFC(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVD_setDFC ---->Entry\n");
	if(&req["zoom_setting"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string zoomSetting=req["zoom_setting"].asCString();
	char zoomDetails1[35] ="Zoom Setting:";
	char platformDFCDetails1[25] ="Platform DFC:";
	char *zoomDetails = (char*)malloc(sizeof(char)*20);
	memset(zoomDetails,'\0', (sizeof(char)*20));
	char *platformDFCDetails = (char*)malloc(sizeof(char)*20);
	memset(platformDFCDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting video decoder instance*/
		device::VideoDevice decoder =device::Host::getInstance().getVideoDevices().at(0);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setDFC\n");
		decoder.setDFC(zoomSetting);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getDFC\n");
		strcpy(zoomDetails,(char*)decoder.getDFC().getName().c_str());
		strcat(zoomDetails1,zoomDetails);
		decoder.setPlatformDFC();
		strcpy(platformDFCDetails,(char*)decoder.getDFC().getName().c_str());
		strcat(platformDFCDetails1,platformDFCDetails);
		strcat(zoomDetails1,",");
		strcat(zoomDetails1,platformDFCDetails1);
		response["details"]= zoomDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VD_setDFC\n");
		response["details"]= "Exception Caught in VD_setDFC";
		response["result"]= "FAILURE";
	}
	free(zoomDetails);
	free(platformDFCDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nVD_setDFC ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: AOP_setEncoding
 *Descrption	: This function is to check the functionality of setEncoding and 
                  getEncoding APIs.
 *@param [in]	: req- 	port_name: video port (corresponding audio port) Encoding format will be set and get.
                  encoding_format: encoding format to be set for audio port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::AOP_setEncoding(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setEncoding ---->Entry\n");
	if(&req["port_name"]==NULL||&req["encoding_format"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char encodingDetails1[30] ="Encoding Format:";
	std::string encodingFormat=req["encoding_format"].asCString();
	char *encodingDetails = (char*)malloc(sizeof(char)*20);
	memset(encodingDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setEncoding\n");
		aPort.setEncoding(encodingFormat);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getEncoding\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetEncoding::%s\n",aPort.getEncoding().getName().c_str());
		sprintf(encodingDetails,"%s",aPort.getEncoding().getName().c_str());
		strcat(encodingDetails1,encodingDetails);
		response["details"]= encodingDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setEncoding\n");
		response["details"]= "Exception Caught in AOP_setEncoding";
		response["result"]= "FAILURE";
	}
	free(encodingDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_setEncoding ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: AOP_setCompression
 *Descrption	: This function is to check the functionality of setCompression and 
                  getCompression APIs.
 *@param retval : req- 	port_name: port for which compression format will be set and get.
               compression_format: compression format to be set for audio port.
 ***************************************************************************/
bool DeviceSettingsAgent::AOP_setCompression(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setCompression ---->Entry\n");
	if(&req["port_name"]==NULL||&req["compression_format"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char compressionDetails1[60] ="Compression format:";
	std::string compressionFormat=req["compression_format"].asCString();
	char *compressionDetails = (char*)malloc(sizeof(char)*200);
	memset(compressionDetails,'\0', (sizeof(char)*200));
	try
	{
		printf("\ncompressionDetails1:%s\n",compressionDetails1);
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setCompression\n");
		aPort.setCompression(compressionFormat);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getCompression\n");
		DEBUG_PRINT(DEBUG_LOG,"\nGetCompression:%s\n",aPort.getCompression().getName().c_str());
		sprintf(compressionDetails,"%s",aPort.getCompression().getName().c_str());
		printf("\ncompressionDetails1:%s\n",compressionDetails1);
		strcat(compressionDetails1,compressionDetails);
		response["details"]= compressionDetails1; 
		response["result"]="SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setCompression\n");
		response["details"]= "Exception Caught in AOP_setCompression";
		response["result"]= "FAILURE";
	}

	free(compressionDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setCompression ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: AOP_setStereoMode
 *Descrption	: This function is to check the functionality of setStereoMode and 
                  getStereoMode APIs.
 *@param [in]	: req- 	port_name: port for which StereoModes will be set and get.
                      stereo_mode: stereo mode to be set for audio port.
 ***************************************************************************/
bool DeviceSettingsAgent::AOP_setStereoMode(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setStreoeMode ---->Entry\n");
	if(&req["port_name"]==NULL||&req["stereo_mode"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char stereoModeDetails1[60] ="Stereo Mode:";
	std::string stereoMode=req["stereo_mode"].asCString();
	char *stereoModeDetails = (char*)malloc(sizeof(char)*20);
	memset(stereoModeDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setStereoMode\n");
		aPort.setStereoMode(stereoMode);
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getStereoMode\n");
		DEBUG_PRINT(DEBUG_LOG,"\ngetStereroMode:%s\n",aPort.getStereoMode().getName().c_str());
		sprintf(stereoModeDetails,"%s",aPort.getStereoMode().getName().c_str());
		strcat(stereoModeDetails1,stereoModeDetails);
		response["details"]= stereoModeDetails1; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_setStreoeMode\n");
		response["details"]= "Exception Caught in AOP_setStreoeMode";
		response["result"]= "FAILURE";
	}
	free(stereoModeDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_setStreoeMode ---->Exit\n");
	return TEST_SUCCESS;
}



/***************************************************************************
 *Function name	: HOST_setPowerMode
 *Descrption	: This function is to check the functionality of setPowerMode and 
                  getPowerMode APIs.
 *@param [in]	: req- 	new_power_state: new power state to be set for decoder.
		  POWER_ON=1, POWER_STANDBY=2, POWER_OFF=3
 ***************************************************************************/
bool DeviceSettingsAgent::HOST_setPowerMode(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPowerMode ---->Entry\n");
	if(&req["new_power_state"]==NULL)
	{
		return TEST_FAILURE;
	}
	int power_state=req["new_power_state"].asInt();
	try
	{
		DEBUG_PRINT(DEBUG_LOG,"\nCalling setPowerMode\n");
		device::Host::getInstance().setPowerMode(power_state);
		response["details"]= "Power Mode Set"; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_setPowerMode\n");
		response["details"]= "Exception Caught in HOST_setPowerMode";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_setPowerMode ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VOP_setResolution
 *Descrption	: This function is to check the functionality of setResolution and 
                  getResolution APIs.
 *@param [in]	: req- 	resolution: new resolution for the given video port.
                        port_name : the port for which the resolution will be 
                                    set and get.
 ***************************************************************************/
bool DeviceSettingsAgent::VOP_setResolution(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n VOP_setResolution  ---->Entry\n");
	char getValue[30] = {'\0'};
	if(&req["port_name"]==NULL || &req["resolution"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	std::string setValue=req["resolution"].asCString();
	bool getOnly = req["get_only"].asInt();

	try
	{	/*getting video port instance*/
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		if (false == getOnly) {
		    /*setting VOP resoultion*/
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling setResolution with value (%s)\n", setValue.c_str());
		    vPort.setResolution(setValue.c_str());
		}
		/*getting VOP resoultion*/
		DEBUG_PRINT(DEBUG_LOG,"\nCalling getResolution\n");
		/*Need to check the return string value with test apps*/
		sprintf(getValue,"%s",(char*)vPort.getResolution().getName().c_str());
		response["details"]= getValue;
		DEBUG_PRINT(DEBUG_LOG,"\nResolution get value(%s)\n", getValue);
		if ((false == getOnly) && strncmp(setValue.c_str(), getValue, strlen(setValue.c_str())) != 0)
		{
			response["result"]= "FAILURE";
		}
		else
		{
			response["result"]= "SUCCESS";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in setResolution\n");
		response["details"]= "Exception Caught in setResolution";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n setResolution ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Functiion name	: FP_getIndicators
 *Descrption		: This function is wrapper function to get the list of indicators 
                          supported in the FrontPanel.
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_getIndicators(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getIndicators  ---->Entry\n");
	/*get list of Indicators supported in the FrontPanel*/
	char *indicatorDetails = (char*)malloc(sizeof(char)*100);
	memset(indicatorDetails,'\0', (sizeof(char)*100));
	char *indicator = (char*)malloc(sizeof(char)*200);
	memset(indicator,'\0', (sizeof(char)*200));
	try
	{
		strcpy(indicator,"Text Panel:");
		DEBUG_PRINT(DEBUG_LOG,"\n\nindicator size:%d\n",device::FrontPanelConfig::getInstance().getIndicators().size());
		for (size_t i = 0; i < device::FrontPanelConfig::getInstance().getIndicators().size(); i++)
		{	
			strcpy(indicatorDetails,(char*)device::FrontPanelConfig::getInstance().getIndicators().at(i).getName().c_str());
			DEBUG_PRINT(DEBUG_LOG,"\nIndicator:%s\n",indicatorDetails);
			strcat(indicator,indicatorDetails);
			if(i< device::FrontPanelConfig::getInstance().getIndicators().size()-1)
			{
				strcat(indicator,",");
			}
		}
		response["details"]=indicator;
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_getIndicators\n");
		response["details"]= "Exception Caught in FP_getIndicators";
		response["result"]= "FAILURE";
	}
	free(indicatorDetails);
	free(indicator);
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getIndicators  ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: FP_getSupportedColors 
 *Descrption	: This function is wrapper function to get the list of colors 
                  supported for a LED in the FrontPanel.
 *parameter[in]	: req- indicator_name: indicator name
 *****************************************************************************/ 

bool DeviceSettingsAgent::FP_getSupportedColors(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getSupportedColors ---->Entry\n");
	/*get list of colors supported in the FrontPanel LEDs*/
	char *colorDetails = (char*)malloc(sizeof(char)*100);
	memset(colorDetails,'\0', (sizeof(char)*100));
	char *color = (char*)malloc(sizeof(char)*200);
	memset(color,'\0', (sizeof(char)*200));
	std::string indicator_name=req["indicator_name"].asCString();
	try
	{
		strcpy(color,"Supported Colors:");
		DEBUG_PRINT(DEBUG_LOG,"\nNo.of supported color:%d\n",device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getSupportedColors().size());

		for (size_t i = 0; i < device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getSupportedColors().size(); i++)
		{

			strcpy(colorDetails,(char*)device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getSupportedColors().at(i).getName().c_str());
			strcat(color,colorDetails);
			if(i < device::FrontPanelConfig::getInstance().getIndicator(indicator_name).getSupportedColors().size()-1)
			{
				strcat(color,",");
			}
		}
		response["details"]=color;
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_getSupportedColors\n");
		response["details"]= "Exception Caught in FP_getSupportedColors";
		response["result"]= "FAILURE";
	}
	free(colorDetails);
	free(color);
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getSupportedColors ---->Exit\n");
	return TEST_SUCCESS;
}




/***************************************************************************
 *Function name	: FP_getTextDisplays
 *Descrption	: This function is wrapper function to get a list of text display 
                  subpanels on the front panel.
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_getTextDisplays(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getTextDisplays ---->Entry\n");
	/*get list of texts supported in the FrontPanel text display */
	char *textDisplayDetails = (char*)malloc(sizeof(char)*200);
	memset(textDisplayDetails,'\0', (sizeof(char)*200));
	char *textDisplay = (char*)malloc(sizeof(char)*200);
	memset(textDisplay,'\0', (sizeof(char)*200));
	try
	{
		strcpy(textDisplay,"Text Panel:");
		for (size_t i = 0; i < device::FrontPanelConfig::getInstance().getTextDisplays().size(); i++)
		{
			strcpy(textDisplayDetails,(char*)device::FrontPanelConfig::getInstance().getTextDisplays().at(i).getName().c_str());
			strcat(textDisplay,textDisplayDetails);
		}
		response["details"]=textDisplay;
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_getTextDisplays \n");
		response["details"]= "Exception Caught in FP_getTextDisplays";
		response["result"]= "FAILURE";
	}
	free(textDisplayDetails);
	free(textDisplay);
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_getTextDisplays  ---->Exit\n");
	return TEST_SUCCESS;
}



/***************************************************************************
 *Function name	: FP_setText
 *Descrption	: This function will set text in the text panel.
 *@param [in]   : req-	text_display: Text to be displayed.
                               text : Name of the Text LED in the Front panel
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setText(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_setText ---->Entry\n");
	if(&req["text_display"]==NULL || &req["text"]==NULL)
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\nCalling setText\n");
	std::string textDisplay=req["text_display"].asCString();
	std::string text=req["text"].asCString();
	try
	{
		/*setting text in the Device front panel text display area*/
		device::FrontPanelConfig::getInstance().getTextDisplay(text).setText(textDisplay);
		response["result"]= "SUCCESS"; 
		response["details"]="setText SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setText\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in FP_setText";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_setText ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: FP_setTimeFormat
 *Descrption	: This function will check the functionality of setTimeFormat and
                  currentTimeFormat APIs.
 *@param [in]   : req-	time_format : time format (12Hrs or 24Hrs or string type)
                               text : Name of the Text LED in the Front panel
 *****************************************************************************/ 


bool DeviceSettingsAgent::FP_setTimeFormat(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_setTimeFormat ---->Entry\n");
	if(&req["text"]==NULL || &req["time_format"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string text=req["text"].asCString();
	int timeFormat=req["time_format"].asInt();
	char TimeFormatDetails[30] ="CurrentTimeFormat:";
	char *timeDetails = (char *)malloc(sizeof(char)*5);
	memset(timeDetails,'\0', (sizeof(char)*5));
	try
	{
		device::FrontPanelConfig::getInstance().getTextDisplay(text).setTimeFormat(timeFormat);	
		timeFormat=device::FrontPanelConfig::getInstance().getTextDisplay(text).getCurrentTimeForamt();
		sprintf(timeDetails,"%d",timeFormat);
		strcat(TimeFormatDetails,timeDetails);
		response["details"]= TimeFormatDetails; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setTimeFormat\n");
		response["details"]= "Exception Caught in FP_setTimeFormat";
		response["result"]= "FAILURE";
	}
	free(timeDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nFP_setTimeFormat ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: FP_setTime
 *Descrption	: This function will set time in the text panel.
 *@param [in]   : req-	time_hrs: Hours.
                       time_mins: Minutes
                           text : Name of the Text LED in the Front panel
 *****************************************************************************/ 
bool DeviceSettingsAgent::FP_setTime(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setTime ---->Entry\n");
	if(&req["time_hrs"]==NULL || &req["time_mins"]==NULL)
	{
		return TEST_FAILURE;
	}
	int time_hrs=req["time_hrs"].asInt();
	int time_mins=req["time_mins"].asInt();
	try
	{
		/*setting the time in HRS:MINS format*/
		device::FrontPanelTextDisplay::getInstance("Text").setTime(time_hrs,time_mins);
		response["result"]= "SUCCESS"; 
		response["details"]="setTime SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in FP_setTime \n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in FP_setTime";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n FP_setTime ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: AOP_loopThru
 *Descrption	: This function will enable and check status of LoopThru.
 *@param [in]   : req-	port_name: name of the video port.
                        loop_thru: new loopThru status(true/false)
 *****************************************************************************/ 
bool DeviceSettingsAgent::AOP_loopThru(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_loopThru ---->Entry\n");
	if(&req["port_name"]==NULL||&req["loop_thru"]==NULL)
	{
		return TEST_FAILURE;
	}

	std::string portName=req["port_name"].asCString();
	char loopThruDetails1[40] ="LoopThru Set Status :";
	int loop =req["loop_thru"].asInt();
	bool loopthru=false;
	if(loop==0)
	{
		loopthru=false;
	}
	else if(loop==1)
	{
		loopthru=true;
	}
	char *loopThruDetails = (char*)malloc(sizeof(char)*20);
	memset(loopThruDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		/*Enable loop thru*/
		aPort.setLoopThru(loopthru);
		/*checking loop thru status*/
		loopthru=aPort.isLoopThru();
		if(loopthru==true)
		{
			sprintf(loopThruDetails,"%d",1);
			response["result"]= "SUCCESS"; 
		}
		else if(loopthru==false)
		{
			sprintf(loopThruDetails,"%d",0);
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(loopThruDetails1,loopThruDetails);
		response["details"]=loopThruDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_loopThru\n");
		response["details"]= "Exception Caught in AOP_loopThru";
		response["result"]= "FAILURE";
	}
	free(loopThruDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_loopThru ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : AOP_mutedStatus
 *Descrption    : This function will enable and check status of mute for
                  a given audio port.
 *@param [in]   : req-  port_name: name of the video port(associated audio port mute 
                                   status will be checked).
                        loop_thru: new loopThru status(true/false)
 *****************************************************************************/

bool DeviceSettingsAgent::AOP_mutedStatus(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_mutedStatus ---->Entry\n");
	if(&req["port_name"]==NULL||&req["mute_status"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char muteDetails1[30] ="Mute Set Status :";
	int mute_status =req["mute_status"].asInt();
	bool mute=false;
	if(mute_status==0)
	{
		mute=false;
	}
	else if(mute_status==1)
	{
		mute=true;
	}
	char *muteDetails = (char*)malloc(sizeof(char)*20);
	memset(muteDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		/*Enable mute */
		aPort.setMuted(mute);
		/*checking mute status*/
		mute=aPort.isMuted();
		if(mute==true)
		{
			sprintf(muteDetails,"%d",1);
			response["result"]= "SUCCESS"; 
		}
		else if(mute==false)
		{
			sprintf(muteDetails,"%d",0);
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(muteDetails1,muteDetails);
		response["details"]=muteDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_mutedStatus\n");
		response["details"]= "Exception Caught in AOP_mutedStatus";
		response["result"]= "FAILURE";
	}
	free(muteDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n AOP_mutedStatus ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : AOP_getSupportedEncodings
 *Descrption    : This function will list the supported encoding formats for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/
bool DeviceSettingsAgent::AOP_getSupportedEncodings(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedEncodings ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedEncodingDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedEncodingDetails,'\0', (sizeof(char)*100));
	char *supportedEncoding = (char*)malloc(sizeof(char)*200);
	memset(supportedEncoding,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedEncoding,"Supported Encoding:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		for (size_t i = 0; i < aPort.getSupportedEncodings().size(); i++) 
		{
			strcpy(supportedEncodingDetails,(char*)aPort.getSupportedEncodings().at(i).getName().c_str());
			DEBUG_PRINT(DEBUG_LOG,"\nSupported Encoding:%s\n",supportedEncodingDetails);
			strcat(supportedEncoding,supportedEncodingDetails);
			if(i < aPort.getSupportedEncodings().size()-1)
			{
				strcat(supportedEncoding,",");
			}
		}
		response["result"]= "SUCCESS"; 
		response["details"]=supportedEncoding; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedEncodings\n");
		response["details"]= "Exception Caught in AOP_getSupportedEncodings";
		response["result"]= "FAILURE";
	}
	free(supportedEncodingDetails);
	free(supportedEncoding);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedEncodings ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : AOP_getSupportedCompression
 *Descrption    : This function will list the supported compression formats for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::AOP_getSupportedCompressions(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedCompression ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedCompressionDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedCompressionDetails,'\0', (sizeof(char)*100));
	char *supportedCompression = (char*)malloc(sizeof(char)*200);
	memset(supportedCompression,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedCompression,"Supported Compression:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		for (size_t i = 0; i < aPort.getSupportedCompressions().size(); i++)
		{
			strcpy(supportedCompressionDetails,(char*)aPort.getSupportedCompressions().at(i).getName().c_str());
			strcat(supportedCompression,supportedCompressionDetails);
			if(i < aPort.getSupportedCompressions().size()-1)
			{
				strcat(supportedCompression,",");
			}
		}
		response["details"]=supportedCompression; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedCompression\n");
		response["details"]= "Exception Caught in AOP_getSupportedCompression";
		response["result"]= "FAILURE";
	}
	free(supportedCompressionDetails);
	free(supportedCompression);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedCompression ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : AOP_getSupportedStereoModes
 *Descrption    : This function will list the supported stereo modes for the audio port.
 *@param [in]   : req-  port_name: name of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::AOP_getSupportedStereoModes(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedStereoModes ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char *supportedStereoModesDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedStereoModesDetails,'\0', (sizeof(char)*100));
	char *supportedStereoModes = (char*)malloc(sizeof(char)*200);
	memset(supportedStereoModes,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedStereoModes,"Supported StereoModes:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting instance for audio ports*/	
		device::AudioOutputPort aPort = vPort.getAudioOutputPort();
		for (size_t i = 0; i < aPort.getSupportedStereoModes().size(); i++)
		{
			strcpy(supportedStereoModesDetails,(char*)aPort.getSupportedStereoModes().at(i).getName().c_str());
			strcat(supportedStereoModes,supportedStereoModesDetails);
			if(i < aPort.getSupportedStereoModes().size()-1)
			{
				strcat(supportedStereoModes,",");
			}
		}
		response["details"]=supportedStereoModes; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in AOP_getSupportedStereoModes\n");
		response["details"]= "Exception Caught in AOP_getSupportedStereoModes";
		response["result"]= "FAILURE";
		return TEST_FAILURE;
	}
	free(supportedStereoModesDetails);
	free(supportedStereoModes);
	DEBUG_PRINT(DEBUG_TRACE,"\nAOP_getSupportedStereoModes ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: HOST_addPowerModeListener
 *Descrption	: This function will add the listener for the power mode change event.
 *****************************************************************************/ 
bool DeviceSettingsAgent::HOST_addPowerModeListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addPowerModeListener ---->Entry\n");
	try
	{
		device::Host::getInstance().addPowerModeListener(&power_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_addPowerModeListener\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in HOST_addPowerModeListener";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addPowerModeListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]="HOST_addPowerModeListener - SUCCESS";
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: HOST_removePowerModeListener
 *Descrption	: This function will remove the listener for the power mode change event.
 *****************************************************************************/ 
bool DeviceSettingsAgent::HOST_removePowerModeListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removePowerModeListener ---->Entry\n");
	try
	{
		device::Host::getInstance().removePowerModeChangeListener(&power_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_removePowerModeListener\n");
		response["result"]= "FAILURE";
		response["details"]="Exception Caught in HOST_removePowerModeListener";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removePowerModeListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]="HOST_removePowerModeListener - SUCCESS";
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VOP_isDisplayConnected
 *Descrption	: This function will check for display connection status for the given 
                  video port.
 *parameter [in]: req-	display_status - new status of display connection.(true/false)
 *****************************************************************************/ 

bool DeviceSettingsAgent::VOP_isDisplayConnected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isDisplayConnected ---->Entry\n");
	if(&req["port_name"]==NULL || &req["display_status"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	/*getting instance for video ports*/
	char displayDetails1[40] ="DisplayConnection Status :";
	bool display_connect=false;
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking DisplayConnection status*/
		display_connect=vPort.isDisplayConnected();
		if(display_connect==true)
		{
			strcat(displayDetails1,"TRUE");
			response["result"]= "SUCCESS"; 
		}
		else if(display_connect==false)
		{
			strcat(displayDetails1,"FALSE");
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		response["details"]=displayDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_isDisplayConnected\n");
		response["details"]= "Exception Caught in VOP_isDisplayConnected";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isDisplayConnected ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: HOST_addDisplayConnectionListener
 *Descrption	: This function will add the listener for the display connection
 *****************************************************************************/ 
bool DeviceSettingsAgent::HOST_addDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addDisplayConnectionListener ---->Entry\n");
	try
	{
		device::Host::getInstance().addDisplayConnectionListener(&display_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_addDisplayConnectionListener \n");
		response["result"]= "FAILURE";
		response["details"]= "Exception Caught in HOST_addDisplayConnectionListener";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_addDisplayConnectionListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]= "HOST_addDisplayConnectionListener - SUCCESS";
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: HOST_removeDisplayConnectionListener
 *Descrption	: This function will remove the listener for the display connection
 *****************************************************************************/ 
bool DeviceSettingsAgent::HOST_removeDisplayConnectionListener(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removeDisplayConnectionListener ---->Entry\n");
	try
	{
		device::Host::getInstance().removeDisplayConnectionListener(&display_obj);
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_removeDisplayConnectionListener \n");
		response["result"]= "FAILURE";
		response["details"]= "Exception Caught in HOST_removeDisplayConnectionListener";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_removeDisplayConnectionListener ---->Exit\n");
	response["result"]="SUCCESS";
	response["details"]= "HOST_removeDisplayConnectionListener - SUCCESS";
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name	: HOST_Resolutions
 *Descrption	: This function will give the supported and current resolution 
                  suppported by the given video port.
 *parameter [in]: req-	port_name - name of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::HOST_Resolutions(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_Resolutions ---->Entry\n");
	std::string portName=req["port_name"].asCString();
	char defaultResolutionDetails1[50]="Default Resolution:";
	char *defaultResolutionDetails = (char*)malloc(sizeof(char)*20);
	memset(defaultResolutionDetails,'\0', (sizeof(char)*20));
	char *supportedResolutionsDetails = (char*)malloc(sizeof(char)*100);
	memset(supportedResolutionsDetails,'\0', (sizeof(char)*100));
	char *supportedResolutions = (char*)malloc(sizeof(char)*200);
	memset(supportedResolutions,'\0', (sizeof(char)*200));
	try
	{
		strcpy(supportedResolutions,"supported Resolutions:");
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		strcpy(defaultResolutionDetails,(char*)vPort.getDfeaultResolution().getName().c_str());
		DEBUG_PRINT(DEBUG_LOG,"\ndefaultResolution:%s\n",vPort.getDfeaultResolution().getName().c_str());
		strcat(defaultResolutionDetails1,defaultResolutionDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nsupportedResolutions::size:%d\n",vPort.getType().getSupportedResolutions().size());
		for (size_t i = 0; i < vPort.getType().getSupportedResolutions().size(); i++)
		{
			strcpy(supportedResolutionsDetails,(char*)vPort.getType().getSupportedResolutions().at(i).getName().c_str());
			DEBUG_PRINT(DEBUG_LOG,"\nsupportedResolutions::%s\n",vPort.getType().getSupportedResolutions().at(i).getName().c_str());
			strcat(supportedResolutions,supportedResolutionsDetails);
			if(i < vPort.getType().getSupportedResolutions().size()-1)
			{
				strcat(supportedResolutions,",");
			}
		}
		strcat(supportedResolutions,"::");
		strcat(supportedResolutions,defaultResolutionDetails1);
		response["details"]= supportedResolutions; 
		response["result"]= "SUCCESS"; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in HOST_Resolutions\n");
		response["details"]= "Exception Caught in HOST_Resolutions";
		response["result"]= "FAILURE";
	}
	free(supportedResolutionsDetails);
	free(supportedResolutions);
	free(defaultResolutionDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nHOST_Resolutions ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VOPTYPE_isHDCPSupported
 *Descrption	: This function will check if HDCP is supported for the given port.
 *parameter [in]: req-	port_id: id of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::VOPTYPE_isHDCPSupported(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isHDCPSupported ---->Entry\n");
	std::string portName=req["port_name"].asCString();

	try
	{
		/*getting instance for video ports*/
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking HDCP support*/
		bool HDCPEnable = vPort.getType().isHDTPSupported();
		DEBUG_PRINT(DEBUG_LOG,"\nIs HDCP Supported: %d\n", vPort.getType().isHDTPSupported());
		if(true == HDCPEnable)
		{
			response["result"]= "SUCCESS";
			response["details"]= "HDCP Support: TRUE";
		}
		else
		{
			response["result"]= "SUCCESS";
			response["details"]= "HDCP Support: FALSE";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_isHDCPSupported\n");
		response["details"]= "Exception Caught in VOPTYPE_isHDCPSupported";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isHDCPSupported ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : VOPTYPE_enableHDCP
 *Descrption    : This function enables HDCP for HDMI.
 *parameter [in]: protectContent
 *                hdcpKey
 *                keySize
 *                portName (hardcoded to type HDMI in RDK)
 *****************************************************************************/
bool DeviceSettingsAgent::VOPTYPE_enableHDCP(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_enableHDCP ---->Entry\n");

        //std::string portName=req["port_name"].asCString();
        bool protectContent = req["protectContent"].asInt();
        string key = req["hdcpKey"].asCString();
        int keySize = req["keySize"].asInt();
        bool useMfrKey = req["useMfrKey"].asInt();
        char *hdcpKey = 0;

        try
        {
                if (useMfrKey)
                {
                        int IsMfrDataRead = false;
                        int retry_count = 0;
                        protectContent = true;
                        IARM_Bus_MFRLib_GetSerializedData_Param_t param_, *param = &param_;

                        do
                        {
                                IsMfrDataRead = false;
                                /* Initialize the struct */
                                memset(param, 0, sizeof(*param));
                                /* Get Key */
                                param->type = mfrSERIALIZED_TYPE_HDMIHDCP;
                                param->bufLen = MAX_SERIALIZED_BUF;

                                int ret = IARM_Bus_Call(IARM_BUS_MFRLIB_NAME,IARM_BUS_MFRLIB_API_GetSerializedData,
                                          (void *)param, sizeof(IARM_Bus_MFRLib_GetSerializedData_Param_t));

                                if(ret != IARM_RESULT_SUCCESS)
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call failed for %s: error code:%d\n","IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP",ret);
                                }
                                else
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"IARM_Bus_Call success for %s\n", "IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP");
                                        keySize = param->bufLen;
                                        hdcpKey = param->buffer;

                                        if ((hdcpKey[0] == 0) && (hdcpKey[1] == 0) && (hdcpKey[2] == 0) &&
                                            (hdcpKey[3] == 0) && (hdcpKey[4] == 0) && (hdcpKey[5] == 0))
                                        {
                                                DEBUG_PRINT(DEBUG_TRACE,"Invalid MFR Data !! Wait for MFR data to be ready..Retry after 10 sec\n");
                                                sleep(10);
                                        }
                                        else
                                        {
                                                DEBUG_PRINT(DEBUG_TRACE,"Received [%d] bytes from %s\n", param->bufLen,"IARM_BUS_MFR_SERIALIZED_TYPE_HDMIHDCP");
                                                IsMfrDataRead = true;
                                        }
                                }

                                retry_count ++;

                        } while((false == IsMfrDataRead) && (retry_count < 6));

                        if (false == IsMfrDataRead)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to get MfrData for enabling HDCP\n");
                                response["result"] = "FAILED";
                                response["details"] = "Failed to get MfrData for enabling HDCP";
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"protectContent:%d hdcpKeyAddr:%p keySize:%d\n", protectContent,hdcpKey,keySize);
                                /* Enable HDCP */
                                device::VideoOutputPortType::getInstance(device::VideoOutputPortType::kHDMI).enabledHDCP(protectContent,hdcpKey,keySize);
                                response["result"] = "SUCCESS";
                                response["details"] = "Enable HDCP done";
                        }
                }
                else
                {
                        hdcpKey = &key[0];
                        DEBUG_PRINT(DEBUG_TRACE,"protectContent:%d hdcpKeyAddr:%p hdcpKey:%s keySize:%d\n", protectContent,hdcpKey,hdcpKey,keySize);
                        /* Enable HDCP */
                        device::VideoOutputPortType::getInstance(device::VideoOutputPortType::kHDMI).enabledHDCP(protectContent,hdcpKey,keySize);
                        response["result"] = "SUCCESS";
                        response["details"] = "Enable HDCP done";
                }
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_enableHDCP\n");
                response["details"]= "Exception Caught in VOPTYPE_enableHDCP";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_enableHDCP ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : VOP_getHDCPStatus
 *Descrption    : This function gets the status of HDCP authentication.
 *parameter [in]: portName
 *****************************************************************************/
bool DeviceSettingsAgent::VOP_getHDCPStatus(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getHDCPStatus ---->Entry\n");
        std::string portName=req["port_name"].asCString();

        try
        {
                char details[30] = {'\0'};
                // getting instance for video port
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
                // checking HDCP status
                int hdcpStatus = vPort.getHDCPStatus();
                DEBUG_PRINT(DEBUG_ERROR,"PortName: %s hdcpStatus: %d\n", portName.c_str(), hdcpStatus);
                // Verify the status value
                if ((hdcpStatus < dsHDCP_STATUS_UNPOWERED) || (hdcpStatus >= dsHDCP_STATUS_MAX))
                {
                    response["result"] = "FAILURE";
                    sprintf(details,"InvalidStatus(%d)",hdcpStatus);
                }
                else
                {
                    response["result"] = "SUCCESS";
                    switch(hdcpStatus)
                    {
                        case dsHDCP_STATUS_UNPOWERED:
                            sprintf(details,"Unpowered(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_UNAUTHENTICATED:
                            sprintf(details,"Unauthenticated(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_AUTHENTICATED:
                            sprintf(details,"Authenticated(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_AUTHENTICATIONFAILURE:
                            sprintf(details,"AuthenticationFailure(%d)",hdcpStatus);
                            break;
                        case dsHDCP_STATUS_INPROGRESS:
                            sprintf(details,"InProgress(%d)",hdcpStatus);
                    }
                }
                response["details"] = details;
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getHDCPStatus\n");
                response["details"]= "Exception Caught in VOP_getHDCPStatus";
                response["result"]= "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getHDCPStatus ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VOPTYPE_DTCPSupport
 *Descrption	: This function will enable and check for the DTCP support for
                  the given port.
 *parameter [in]: req-	port_id: id of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::VOPTYPE_DTCPSupport(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_DTCPSupport ---->Entry\n");
	if(&req["port_id"]==NULL )
	{
		return TEST_FAILURE;
	}
	int portID=req["port_id"].asInt();
	char DTCPSupportDetails1[30] ="DTCP set Status :";
	bool DTCPEnable=false;
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portID);
		/*Enable DTCP support */
		vPort.getType().getInstance(portID).enabledDTCP();	
		/*checking DTCP status*/
		DTCPEnable=vPort.getType().isDTCPSupported();
		if(DTCPEnable==true)
		{
			strcat(DTCPSupportDetails1,"TRUE");
			response["result"]= "SUCCESS"; 
		}
		else if(DTCPEnable==false)
		{
			strcat(DTCPSupportDetails1,"FALSE");
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		response["details"]=DTCPSupportDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_DTCPSupport\n");
		response["details"]= "Exception Caught in VOPTYPE_DTCPSupport";
		response["result"]= "FAILURE";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_DTCPSupport ---->Exit\n");
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name	: VOPTYPE_isDynamicResolutionSupported
 *Descrption	: This function will check for the DynamicResolution support for
                  the given port.
 *parameter [in]: req-	port_name: name of the video port.
 *****************************************************************************/ 
bool DeviceSettingsAgent::VOPTYPE_isDynamicResolutionSupported(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n VOPTYPE_isDynamicResolutionSupported ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	std::string portName=req["port_name"].asCString();
	char dynamicResolutionDetails1[40] ="isDynamicResolutionSupported :";
	bool dynamicResolutionSupport=false;
	char *dynamicResolutionSupportDetails = (char*)malloc(sizeof(char)*20);
	memset(dynamicResolutionSupportDetails,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*checking for DynamicResolution supported*/
		dynamicResolutionSupport=vPort.isDynamicResolutionSupported();
		if(dynamicResolutionSupport==true)
		{
			sprintf(dynamicResolutionSupportDetails,"%s","TRUE");
			response["result"]= "SUCCESS"; 
		}
		else if(dynamicResolutionSupport==false)
		{
			sprintf(dynamicResolutionSupportDetails,"%s","FALSE");
			response["result"]= "SUCCESS"; 
		}
		else
		{
			response["result"]= "FAILURE"; 
		}
		strcat(dynamicResolutionDetails1,dynamicResolutionSupportDetails);
		response["details"]=dynamicResolutionDetails1; 
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOPTYPE_isDynamicResolutionSupported\n");
		response["details"]= "Exception Caught in VOPTYPE_isDynamicResolutionSupported";
		response["result"]= "FAILURE";
	}
	free(dynamicResolutionSupportDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOPTYPE_isDynamicResolutionSupported ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name : VOP_isContentProtected
 *Descrption    : This function is to check content protect status.
 *parameter [in]: req-  port_name: video port name.
 *****************************************************************************/
bool DeviceSettingsAgent::VOP_isContentProtected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isContentProtected ---->Entry\n");
	std::string portName=req["port_name"].asCString();

	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		bool cpSupport = vPort.isContentProtected();
		DEBUG_PRINT(DEBUG_LOG,"\nIs Content Protected: %d\n",vPort.isContentProtected());
		if(true == cpSupport)
		{
			response["details"]= "Content Protected: TRUE";
			response["result"]= "SUCCESS";
		}
		else
		{
			response["details"]= "Content Protected: FALSE";
			response["result"]= "SUCCESS";
		}
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_isContentProtected\n");
		response["details"]= "Exception Caught in VOP_isContentProtected";
		response["result"]= "FAILURE";
	}

	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_isContentProtected ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name	: VOP_getAspectRatio
 *Descrption	: This function is to get the AspectRatio of the video port.
 *parameter [in]: req-	port_name: video port name.
 *****************************************************************************/ 
bool DeviceSettingsAgent::VOP_getAspectRatio(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getAspectRatio ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	char aspectRatioDetails1[30] ="AspectRatio:";
	char *aspectRatioDetails = (char*)malloc(sizeof(char)*20);
	memset(aspectRatioDetails,'\0', (sizeof(char)*20));
	std::string portName=req["port_name"].asCString();
	char *aspectRatio=(char*)malloc(sizeof(char)*20);
	memset(aspectRatio,'\0', (sizeof(char)*20));
	try
	{
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting AspectRation for a given video ports*/	
		strcpy(aspectRatio,(char*)vPort.getDisplay().getAspectRatio().getName().c_str());
		strcpy(aspectRatioDetails,aspectRatio);
		strcat(aspectRatioDetails1,aspectRatioDetails);
		response["details"]=aspectRatioDetails1;
		response["result"]="SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getAspectRatio\n");
		response["details"]= "Exception Caught in VOP_getAspectRatio";
		response["result"]= "FAILURE";
	}
	free(aspectRatioDetails);
	free(aspectRatio);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getAspectRatio ---->Exit\n");
	return TEST_SUCCESS;
}



/***************************************************************************
 *Function name	: VOP_getDisplayDetails
 *Descrption	: This function is to get the list of details about video port.
 *parameter [in]: req-	port_name: video port name.
 *****************************************************************************/ 
bool DeviceSettingsAgent::VOP_getDisplayDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getDisplayDetails ---->Entry\n");
	if(&req["port_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	char *displayDetails1 = (char*)malloc(sizeof(char)*200);
	memset(displayDetails1,'\0', (sizeof(char)*200));
	char *displayDetails = (char*)malloc(sizeof(char)*20);
	memset(displayDetails,'\0', (sizeof(char)*20));
	char *weekDetails =(char*)malloc(sizeof(char)*20);
	memset(weekDetails,'\0', (sizeof(char)*20));
	char *yearDetails =(char*)malloc(sizeof(char)*20);
	memset(yearDetails,'\0', (sizeof(char)*20));
	char *pcodeDetails =(char*)malloc(sizeof(char)*20);
	memset(pcodeDetails,'\0', (sizeof(char)*20));
	char *pnumberDetails =(char*)malloc(sizeof(char)*20);
	memset(pnumberDetails,'\0', (sizeof(char)*20));
	std::string portName=req["port_name"].asCString();
	try
	{
		strcpy(displayDetails1,"Display Details:");
		/*getting instance for video ports*/	
		device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
		/*getting list of details for a given video ports*/	
		sprintf(weekDetails,"%d",vPort.getDisplay().getManufacturerWeek());
		strcat(displayDetails1,"ManufacturerWeek:");
		strcat(displayDetails1,weekDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nManufacturer Week:%s\n",weekDetails);
		sprintf(yearDetails,"%d",vPort.getDisplay().getManufacturerYear());
		strcat(displayDetails1,",ManufacturerYear:");
		strcat(displayDetails1,yearDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nManufacturer Year:%s\n",yearDetails);
		sprintf(pcodeDetails,"%x",vPort.getDisplay().getProductCode());
		strcat(displayDetails1,",ProductCode:");
		strcat(displayDetails1,pcodeDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nProductCode:%s\n",pcodeDetails);
		sprintf(pnumberDetails,"%x",vPort.getDisplay().getSerialNumber());
		strcat(displayDetails1,",ProductSerialNumber:");
		strcat(displayDetails1,pnumberDetails);
		DEBUG_PRINT(DEBUG_LOG,"\nProductCode:%s\n",pnumberDetails);
		response["details"]=displayDetails1;
		response["result"]="SUCCESS";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in VOP_getDisplayDetails\n");
		response["details"]= "Exception Caught in VOP_getDisplayDetails";
		response["result"]= "FAILURE";
	}
	free(displayDetails);
	free(displayDetails1);
	free(weekDetails);
	free(yearDetails);
	free(pcodeDetails);
	free(pnumberDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nVOP_getDisplayDetails ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : VOP_setEnable
 *Descrption    : This function enables or disables the specified video port.
 *parameter [in]: port_name: video port name
		  enable: true to enable, false to disable
 *****************************************************************************/
bool DeviceSettingsAgent::VOP_setEnable(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setEnable  ---->Entry\n");
        char details[30] = {'\0'};
        std::string portName=req["port_name"].asCString();
        bool enable = req["enable"].asInt();

        try
        {       /*getting video port instance*/
                device::VideoOutputPort vPort = device::Host::getInstance().getVideoOutputPort(portName);
                if (true == enable)
		{
                    /*setting VOP to enable*/
                    DEBUG_PRINT(DEBUG_LOG,"\nCalling VideoOutputPort enable\n");
		    vPort.enable();
                }
		else
		{
		    /*setting VOP to disable*/
		    DEBUG_PRINT(DEBUG_LOG,"\nCalling VideoOutputPort disable\n");
		    vPort.disable();
		}

		if (vPort.isEnabled() == enable)
		{
		    response["result"]="SUCCESS";
		}
		else
		{
		    response["result"]="FAILURE";
		}
		sprintf(details,"Port enable status:%d", vPort.isEnabled());
		response["details"]=details;
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\n Exception Caught in setEnable\n");
                response["details"]= "Exception Caught in setEnable";
                response["result"]= "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"VOP_setEnable ---->Exit\n");
        return TEST_SUCCESS;
}

bool DeviceSettingsAgent::HOST_getCPUTemperature(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getCPUTemperature ---->Entry\n");
        try
        {
                char details[30] = {'\0'};
                float cpuTemp = device::Host::getInstance().getCPUTemperature();
                DEBUG_PRINT(DEBUG_LOG,"Current CPU temperature: %+7.2fC\n", cpuTemp);
                sprintf(details,"%5.2f",cpuTemp);
                response["details"] = details;
                response["result"] = "SUCCESS";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nException Caught in HOST_getCPUTemperature\n");
                response["details"] = "Exception Caught in HOST_getCPUTemperature";
                response["result"] = "FAILURE";
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nHOST_getCPUTemperature ---->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "DeviceSettingsAgent".
 *
 **************************************************************************/

extern "C" DeviceSettingsAgent* CreateObject()
{
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Entry\n");
	return new DeviceSettingsAgent();
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Exit\n");
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool DeviceSettingsAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"\n DeviceSettingsAgent shutting down \n");
        if(ptrAgentObj==NULL)
        {
                return TEST_FAILURE;
        }

	IARM_Result_t retval;
	retval=IARM_Bus_Disconnect();
	if(retval==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Application Disconnected from IARMBUS \n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Application failed to Disconnect from IARMBUS \n");
		return TEST_FAILURE;
	}
	//IARM_Bus_Term(); //Commented for RDKTT-152
	ptrAgentObj->UnregisterMethod("TestMgr_DS_managerInitialize");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_managerDeinitialize");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setBrightness");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setState");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setColor");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setBlink");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setScroll");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_setLevel");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_setDB");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VD_setDFC");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_setEncoding");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_setCompression");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_setStereoMode");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_setPowerMode");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_setResolution");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_getIndicators");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_FP_getSupportedColors");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_getTextDisplays");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setText");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setTimeForamt");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_FP_setTime");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_loopThru");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_mutedStatus");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_getSupportedEncodings");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_getSupportedCompressions");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_AOP_getSupportedStereoModes");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_addPowerModeListener");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_removePowerModeListener");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_isDisplayConnected");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_addDisplayConnectionListener");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_removeDisplayConnectionListener");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_Resolutions");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOPTYPE_isHDCPSupported");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOPTYPE_enableHDCP");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_getHDCPStatus");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOPTYPE_DTCPSupport");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOPTYPE_isDynamicResolutionSupported");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_getAspectRatio");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_getDisplayDetails");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_isContentProtected");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_VOP_setEnable");
	ptrAgentObj->UnregisterMethod("TestMgr_DS_HOST_getCPUTemperature");

	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(DeviceSettingsAgent *agentobj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"Destroying DeviceSettings Agent object");
	delete agentobj;
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Exit\n");
}

