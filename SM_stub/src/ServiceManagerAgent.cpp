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

#include "ServiceManagerAgent.h"

char *rdkLogP = getenv("RDK_LOG_PATH");
char *tdkP = getenv("TDK_PATH");

string rdkLogPath;
string tdkPath;

/***************************************************************************
 *Function name	: ServiceManagerAgent 
 *Descrption	: This is a constructor function for ServiceManagerAgent class. 
 *****************************************************************************/ 
ServiceManagerAgent::ServiceManagerAgent()
{
	DEBUG_PRINT(DEBUG_LOG,"ServiceManagerAgent Initialized");
}

/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 *****************************************************************************/ 

bool ServiceManagerAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"ServiceManagerAgent Initialize");
	/*Register stub function for callback*/
	// ServiceManager APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_RegisterService,"TestMgr_SM_RegisterService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_UnRegisterService,"TestMgr_SM_UnRegisterService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DoesServiceExist,"TestMgr_SM_DoesServiceExist");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_GetRegisteredServices,"TestMgr_SM_GetRegisteredServices");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_GetGlobalService,"TestMgr_SM_GetGlobalService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_GetSetting,"TestMgr_SM_GetSetting");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_CreateService,"TestMgr_SM_CreateService");
	// Services common APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_Services_GetName,"TestMgr_Services_GetName");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_Services_SetAPIVersion,"TestMgr_SM_SetAPIVersion");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_Services_RegisterForEvents,"TestMgr_SM_RegisterForEvents");
	// HomeNetworking Service callMethod APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_EnableMDVR,"TestMgr_SM_HN_EnableMDVR");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_EnableVPOP,"TestMgr_SM_HN_EnableVPOP");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_SetDeviceName,"TestMgr_SM_HN_SetDeviceName");
	// DisplaySettings Service callMethod APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DisplaySetting_SetZoomSettings,"TestMgr_SM_DisplaySetting_SetZoomSettings");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DisplaySetting_SetCurrentResolution,"TestMgr_SM_DisplaySetting_SetCurrentResolution");
	// DeviceSettingService callMethod APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DeviceSetting_GetDeviceInfo,"TestMgr_SM_DeviceSetting_GetDeviceInfo");
	// ScreenCaptureService callMethod APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_ScreenCapture_Upload,"TestMgr_SM_ScreenCapture_Upload");
	// WebSocketService callMethod APIs
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_WebSocket_GetUrl,"TestMgr_SM_WebSocket_GetUrl");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_WebSocket_GetReadyState,"TestMgr_SM_WebSocket_GetReadyState");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_WebSocket_GetBufferedAmount,"TestMgr_SM_WebSocket_GetBufferedAmount");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_WebSocket_GetProtocol,"TestMgr_SM_WebSocket_GetProtocol");
	/*HdmiCecService API's*/
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_SetEnabled,"TestMgr_SM_HdmiCec_SetEnabled");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_GetEnabled,"TestMgr_SM_HdmiCec_GetEnabled");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_SetName,"TestMgr_SM_HdmiCec_SetName");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_GetName,"TestMgr_SM_HdmiCec_GetName");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_GetConnectedDevices,"TestMgr_SM_HdmiCec_GetConnectedDevices");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_SendMessage,"TestMgr_SM_HdmiCec_SendMessage");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_OnMessage,"TestMgr_SM_HdmiCec_OnMessage");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_ClearCecLog,"TestMgr_SM_HdmiCec_ClearCecLog");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_CheckStatus,"TestMgr_SM_HdmiCec_CheckStatus");

	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string ServiceManagerAgent::testmodulepre_requisites()
{
        DEBUG_PRINT(DEBUG_TRACE,"testmodulepre_requisites() ---> Entry\n");

	/*Check for the environment variable set or not */
        if(rdkLogP == NULL)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nEnvironment variable not set for RDK_LOG_PATH\n");
                return "FAILURE<DETAILS>Environment variable not set for \"RDK_LOG_PATH\"";
        }
        else
        {
                rdkLogPath.assign(rdkLogP);
                DEBUG_PRINT(DEBUG_TRACE,"\n RDK_LOG_PATH=%s\n",rdkLogPath.c_str());
        }

        if(tdkP == NULL)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nEnvironment variable not set for TDK_PATH\n");
                return "FAILURE<DETAILS>Environment variable not set for \"TDK_PATH\"";
        }
        else
        {
                tdkPath.assign(tdkP);
                DEBUG_PRINT(DEBUG_TRACE,"\n TDK_PATH=%s\n",tdkPath.c_str());
        }

        DEBUG_PRINT(DEBUG_TRACE,"testmodulepre_requisites() ---> Exit\n");

        return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool ServiceManagerAgent::testmodulepost_requisites()
{
        return TEST_SUCCESS;
}


/***************************************************************************
 *Function name : SM_RegisterService 
 *Descrption    : This function will register the given service with the serviceManger component
 *parameter [in]: req-  service_name-Name of the service.
 *****************************************************************************/ 
bool registerServices(QString serviceName, ServiceStruct &serviceStruct)
{
	bool registerStatus = false;

        if (serviceName.isEmpty())
        {
                DEBUG_PRINT(DEBUG_ERROR,"%s: serviceName is NULL\n", __FUNCTION__);
                return registerStatus;
	}
#ifdef HAS_MEMORY_INFO
        else if(serviceName == MemoryInfoService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createMemoryInfoService;
        }
#endif
#ifdef HAS_FRONT_PANEL
        else if (serviceName == FrontPanelService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createFrontPanelService;
        }
#endif
#ifdef HAS_API_SYSTEM
        else if (serviceName == SYSTEM_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createSystemService;
        }
#endif
#ifdef HAS_STATE_OBSERVER
        else if (serviceName == StateObserverService::STATE_OBSERVER_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createStateObserverService;
        }
#endif
#ifdef MSO_PAIRING
        else if (serviceName == CMSOPairingService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createMSOPairingService;
        }
#endif
#ifdef HAS_API_AVINPUT
        else if (serviceName == AVInputService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createAVInputService;
        }
#endif
#ifdef USE_DISPLAY_SETTINGS
        else if (serviceName == DISPLAY_SETTINGS_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createDisplaySettingsService;
        }
#endif
#ifdef WAREHOUSE_API
        else if(serviceName == WarehouseService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createWarehouseService;
        }
#endif
#ifdef USE_STORAGE_MANAGER_API
        else if(serviceName == StorageManagerService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createStorageManagerService;
        }
#endif
#ifdef ENABLE_VREX_SERVICE
        else if(serviceName == VREXManagerService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createVREXManagerService;
        }
#endif
#ifdef USE_TSB_SETTINGS
        else if(serviceName == TSB_SETTINGS_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createTsbSettingsService;
        }
#endif
#ifdef BROWSER_SETTINGS
        else if (serviceName == BrowserSettingsService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createBrowserSettingsService;
        }
#endif
#ifdef HAS_API_HOME_NETWORKING
        else if(serviceName == HOME_NETWORKING_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createHomeNetworkingService;
        }
#endif
#ifdef HAS_API_RFREMOTE
        else if (serviceName == CRFRemoteService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createRFRemoteService;
        }
#endif
#ifdef SCREEN_CAPTURE
        else if(serviceName == ScreenCaptureService::NAME)
        {
                serviceStruct.createFunction = &ScreenCaptureService::create;
        }
#endif
#ifdef USE_DEVICE_SETTINGS_SERVICE
        else if(serviceName == DEVICE_SETTING_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createDeviceSettingService;
        }
#endif
#ifdef ENABLE_WEBSOCKET_SERVICE
        else if (serviceName == WebSocketService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createWebSocketService;
        }
#endif
#ifdef HAS_API_HDMI_CEC
        else if (serviceName == HdmiCecService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createHdmiCecService;
        }
#endif
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nUnsupported service %s\n", serviceName.toUtf8().constData());
		return registerStatus;
	}

        serviceStruct.serviceName = serviceName;
        registerStatus = ServiceManager::getInstance()->registerService(serviceName, serviceStruct);
        DEBUG_PRINT(DEBUG_LOG,"\n%s registration status = %d\n", serviceName.toUtf8().constData(), registerStatus);

        return registerStatus;
}

bool ServiceManagerAgent::SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterService ---->Entry\n");
	char stringDetails[STR_DETAILS_50] = {'\0'};
	bool register_service=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
	/*Name of the service to be registered with service manager*/
	std::string serviceName=req["service_name"].asCString();

	ServiceStruct serviceStruct;
	register_service = registerServices(QString::fromStdString(serviceName), serviceStruct);

	/*Checking the return value*/
	if(true == register_service)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n%s Registration Success\n", serviceName.c_str());
		response["result"]="SUCCESS";
		sprintf(stringDetails,"%s registration success", serviceName.c_str());
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"%s registration failed\n", serviceName.c_str());
		response["result"]="FAILURE";
		sprintf(stringDetails,"%s registration failed", serviceName.c_str());
	}
	response["details"]=stringDetails;

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterService ---->Exit\n");
	return TEST_SUCCESS;	
}

/***************************************************************************
 *Function name : SM_UnRegisterService 
 *Descrption    : This function will unregister the given service from the serviceManger component. 
 *parameter [in]: req-  service_name- Name of the service.
 *****************************************************************************/ 

bool ServiceManagerAgent::SM_UnRegisterService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_UnRegisterService ---->Entry\n");
	char stringDetails[STR_DETAILS_50] = {'\0'};
	bool unregister_service=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	/*calling unregisterService API for DeRegistering the service*/
	unregister_service=ServiceManager::getInstance()->unregisterService(QString::fromStdString(serviceName));
	if(true == unregister_service)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n%s UnRegistration Success\n", serviceName.c_str());
		response["result"]="SUCCESS";
		sprintf(stringDetails,"%s unregistration success", serviceName.c_str());
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n%s UnRegistration failed\n", serviceName.c_str());
		response["result"]="FAILURE";
		sprintf(stringDetails,"%s unregistration failed", serviceName.c_str());
	}
	response["details"]=stringDetails;

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_UnRegisterService ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_DoesServiceExist
 *Descrption    : This will check the existence of the given service in the list of registered services.
 *parameter [in]: req-  service_name-Name of the service.
 *****************************************************************************/ 

bool ServiceManagerAgent::SM_DoesServiceExist(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DoesServiceExist ---->Entry\n");
	bool exist=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	/*Checking the service existence in service manager component*/
	exist=ServiceManager::getInstance()->doesServiceExist(QString::fromStdString(serviceName));
        if(false == exist)
	{
		DEBUG_PRINT(DEBUG_LOG,"%s does not exists\n", serviceName.c_str());
		response["result"]="SUCCESS";
		response["details"]="NOT EXIST";
	}
        else
	{
		DEBUG_PRINT(DEBUG_LOG,"%s service exists\n", serviceName.c_str());
		response["result"]="SUCCESS";
		response["details"]="PRESENT";
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DoesServiceExist ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_GetRegisteredServices
 *Descrption    : This will return the list of registered services with the serviceManger component.
 *parameter [in]: NULL
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_GetRegisteredServices(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_GetRegisteredServices ---->Entry\n");
	char services[STR_DETAILS_200]="Service:" ;
	char *list_services = (char*)malloc(sizeof(char)*STR_DETAILS_30);
	memset(list_services , '\0', (sizeof(char)*STR_DETAILS_30));
	/*calling getRegisteredServices API to get the list of reistered services*/
        QList<QString> list= ServiceManager::getInstance()->getRegisteredServices();
        for(int i=0;i<list.count();i++)
        {
                DEBUG_PRINT(DEBUG_LOG,"\nservice:%s\n",list.at(i).toUtf8().constData());
		/*coverting QString to String*/
		strcpy(list_services,list.at(i).toUtf8().constData());
		strcat(services,list_services);
		if(i < list.count()-1)
                {
	                strcat(services,",");
        	}
        }
	DEBUG_PRINT(DEBUG_LOG,"Services:%s",services);
	response["result"]="SUCCESS";
	response["details"]=services;
	free(list_services);
	DEBUG_PRINT(DEBUG_TRACE,"\n SM_GetRegisteredServices  ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_GetGlobalService 
 *Descrption    : This will return the name of the given service.
 *parameter [in]: req-  service_name-Name of the service.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_GetGlobalService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_GetGlobalService ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	char services[STR_DETAILS_50]= "Service:";
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	if(ptr_service != NULL)
	{
		/*Getting the name for the service instance*/
		strcat(services,ptr_service->getName().toUtf8().constData());
		DEBUG_PRINT(DEBUG_LOG,"%s",services);
		response["result"]="SUCCESS";
		response["details"]=services;
	}
	else
	{
		response["result"]="FAILURE";
		response["details"]="ServiceManager failed to get GlobalService Pointer";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n SM_GetGlobalService ---->Exit\n");
	return TEST_SUCCESS;	
}

bool ServiceManagerAgent::SM_GetSetting(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_GetSetting ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
        std::string serviceName=req["service_name"].asCString();

	QString returnValue;
	QString setting;
	char stringDetails[STR_DETAILS_50] = {'\0'};

        returnValue = ServiceManager::getInstance()->getSetting(QString::fromStdString(serviceName), setting);

    	if (returnValue.isEmpty() || returnValue.isNull()) 
	{
		sprintf(stringDetails,"%s getSetting is null", serviceName.c_str());
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getSetting failed\n");
	}
        else if(setting.isEmpty() || setting.isNull())
        {
		sprintf(stringDetails,"%s setting is null", serviceName.c_str());
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getSetting failed\n");
        }
        else
        {
		sprintf(stringDetails,"%s getSetting=%s",serviceName.c_str(),returnValue.toStdString().c_str());
                response["result"]="SUCCESS";
                DEBUG_PRINT(DEBUG_LOG,"\n SM getSetting success\n");
		
        }
	response["details"]=stringDetails;

        DEBUG_PRINT(DEBUG_TRACE,"\n SM_GetSetting ---->Exit\n");
        return TEST_SUCCESS;
}

bool ServiceManagerAgent::SM_CreateService(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_CreateService ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="service name is NULL";
                return TEST_FAILURE;
        }
        std::string serviceName=req["service_name"].asCString();

	Service* ptrService = NULL;
    	if (ServiceManager::getInstance()->doesServiceExist(QString::fromStdString(serviceName)))
    	{
        	ptrService = ServiceManager::getInstance()->createService(QString::fromStdString(serviceName));
		char stringDetails[STR_DETAILS_100] = {'\0'};
        	if (ptrService != NULL)
        	{
			sprintf(stringDetails,"GetName from created service: %s", ptrService->getName().toUtf8().constData());
			response["result"]="SUCCESS";
			DEBUG_PRINT(DEBUG_LOG,"\nCreated %s successfully\n", serviceName.c_str());
			// Delete the created service
        		delete ptrService;
        		ptrService = NULL;
			DEBUG_PRINT(DEBUG_LOG,"\nDeleted %s successfully\n", serviceName.c_str());
        	}
		else
		{
			sprintf(stringDetails,"Failed to create service: %s", serviceName.c_str());
			response["result"]="FAILURE";
			DEBUG_PRINT(DEBUG_ERROR,"\nSM_CreateService failed");
		}
		response["details"]=stringDetails;
    	}
	else
	{
                response["result"]="FAILURE";
                response["details"]="Service does not exists";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM_CreateService failed. Service does not exist\n");
        }

        DEBUG_PRINT(DEBUG_TRACE,"\nSM_CreateService ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HN_EnableMDVR 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_HN_SET_MDVR_ENABLED and METHOD_HN_IS_MDVR_ENABLED method as
		  parameters.
 *parameter [in]: req-  enable - Parameter to be passed to callMethod API.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableMDVR ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["enable"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="enable value is NULL";
                return TEST_FAILURE;
        }
	int enable=req["enable"].asInt();
	bool enable_flag=false;
	ServiceParams params,resultParams;
	char enableDetail[STR_DETAILS_20]= "Enable:";
	QVariantList list;
	Service* ptr_service=NULL;
	if(enable==1)
	{
		enable_flag= true;
	}
	else if(enable==0)
	{
		enable_flag=false;
	}	
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nEnter enable/disable in 'enable' field\n");
		response["result"]="FAILURE";
		response["details"]="Enter 'enable' field correctly";
		return TEST_FAILURE;
	}

	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(HOME_NETWORKING_SERVICE_NAME);
	if(ptr_service != NULL)
	{
		char *mdvrDetails = (char*)malloc(sizeof(char)*5);
		memset(mdvrDetails , '\0', (sizeof(char)*5));
		list.append(enable_flag);
		params["params"] = list;
		/*Enabling MDVR by calling callMethod with METHOD_HN_SET_MDVR_ENABLED*/
		ptr_service->callMethod(METHOD_HN_SET_MDVR_ENABLED,params); 
		/*Checking MDVR by calling callMethod with METHOD_HN_IS_MDVR_ENABLED*/
		resultParams=ptr_service->callMethod(METHOD_HN_IS_MDVR_ENABLED,params);
		sprintf(mdvrDetails,"%d",resultParams["enabled"].toBool());
		strcat(enableDetail,mdvrDetails);
		DEBUG_PRINT(DEBUG_LOG,"%s",enableDetail);
		free(mdvrDetails);
		response["result"]="SUCCESS";
		response["details"]=enableDetail;
	}
	else
	{
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
#else
	response["result"]="FAILURE";
	response["details"]="Home Networking Service unsupported";
#endif
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableMDVR ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_HN_EnableVPOP 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_HN_SET_VPOP_ENABLED and METHOD_HN_IS_VPOP_ENABLED method as
		  parameters.
 *parameter [in]: req-  enable - Parameter to be passed to callMethod API
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableVPOP ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["enable"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="enable value is NULL";
                return TEST_FAILURE;
        }
	int enable=req["enable"].asInt();
	bool enable_flag=false;
	ServiceParams params,resultParams;
	char enableDetail[STR_DETAILS_20]= "Enable:";
	QVariantList list;
	Service* ptr_service=NULL;
	if(enable==1)
	{
		enable_flag= true;
	}
	else if(enable==0)
	{
		enable_flag=false;
	}	
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nEnter enable/disable in 'enable' field\n");
		response["result"]="FAILURE";
		response["details"]="Enter 'enable' field correctly";
		return TEST_FAILURE;
	}
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(HOME_NETWORKING_SERVICE_NAME);
	if(ptr_service != NULL)
	{
		char *vpopDetails = (char*)malloc(sizeof(char)*5);
		memset(vpopDetails , '\0', (sizeof(char)*5));
		list.append(enable_flag);
		params["params"] = list;
		/*Enabling VPOP by calling callMethod with METHOD_HN_SET_VPOP_ENABLED*/
		ptr_service->callMethod(METHOD_HN_SET_VPOP_ENABLED,params); 
		/*Checking VPOP by calling callMethod with METHOD_HN_IS_VPOP_ENABLED*/
		resultParams=ptr_service->callMethod(METHOD_HN_IS_VPOP_ENABLED,params);
		sprintf(vpopDetails,"%d",resultParams["enabled"].toBool());
		strcat(enableDetail,vpopDetails);
		DEBUG_PRINT(DEBUG_LOG,"%s",enableDetail);
		free(vpopDetails);
		response["result"]="SUCCESS";
		response["details"]=enableDetail;
	}
	else
	{
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
#else
	response["result"]="FAILURE";
        response["details"]="Home Networking Service unsupported";
#endif
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableVPOP ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_DisplaySetting_SetZoomSettings 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_DISPLAY_SETTINGS_SET_ZOOM_SETTING and METHOD_DISPLAY_SETTINGS_GET_ZOOM_SETTING method as
		  parameters.
 *parameter [in]: req- 	videoDisplay - name of the videoDisplay
			zoomLevel - Level for Zoom 
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetZoomSettings ---->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        if(&req["videoDisplay"]==NULL || &req["zoomLevel"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="videoDisplay or zoomLevel is NULL";
                return TEST_FAILURE;
        }
	std:: string videoDisplay=req["videoDisplay"].asCString();
	std:: string zoomLevel=req["zoomLevel"].asCString();
	ServiceParams params,resultParams;
	char zoomLevelDetail[STR_DETAILS_200]= "zoomLevel";
	QVariantList list;
	char *zoomDetails = (char*)malloc(sizeof(char)*STR_DETAILS_100);
	memset(zoomDetails , '\0', (sizeof(char)*STR_DETAILS_100));
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
	if(ptr_service != NULL)
	{
		list.append(QString::fromStdString(videoDisplay));
		list.append(QString::fromStdString(zoomLevel));
		params["params"] = list;
		/*setting zoom level by calling callMethod with METHOD_DISPLAY_SETTINGS_SET_ZOOM_SETTING*/
		/*This is not yet implemented,cause segmentation fault. This will be added once implementaion done
		  in the component*/
		//ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_SET_ZOOM_SETTING,params); 
		/*getting zoom level by calling callMethod with METHOD_DISPLAY_SETTINGS_GET_ZOOM_SETTING*/
		/*This is not yet implemented,cause segmentation fault. This will be added once implementaion done
		  in the component*/
		//resultParams=ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_ZOOM_SETTING,params);
		/*result param will be filled once the implemetation for get and set zoomSettings APIs are done*/
		//sprintf(zoomDetails,"%d",resultParams["zoomLevel"]);
		//strcat(zoomLevelDetail,zoomDetails);
		//DEBUG_PRINT(DEBUG_LOG,"%s",zoomLevelDetail);
		response["details"]=zoomLevelDetail;
		/*Implementation from component is not done , so this will return FAILURE*/
		response["result"]="FAILURE";
	}
	else
	{
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	free(zoomDetails);
#else
	response["result"]="FAILURE";
	response["details"]="DisplaySettings Service unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetZoomSettings ---->Exit\n");
	return TEST_SUCCESS;	
}

/***************************************************************************
 *Function name : SM_DisplaySetting_SetCurrentResolution 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_DISPLAY_SETTINGS_GET_CURRENT_RESOLUTION and 
		  METHOD_DISPLAY_SETTINGS_SET_CURRENT_RESOLUTION
		  parameters.
 *parameter [in]: req- 	videoDisplay - name of the videoDisplay
			resolution - video resolution 
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetCurrentResolution ---->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        if(&req["videoDisplay"]==NULL || &req["resolution"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="videoDisplay or resolution is NULL";
                return TEST_FAILURE;
        }
	std:: string videoDisplay=req["videoDisplay"].asCString();
	std:: string resolution=req["resolution"].asCString();
	ServiceParams params,resultParams;
	char curResolutionDetail[STR_DETAILS_200]= "Resolution";
	QVariantList list;
	char *resolutionDetails = (char*)malloc(sizeof(char)*STR_DETAILS_100);
	memset(resolutionDetails , '\0', (sizeof(char)*STR_DETAILS_100));
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
	if(ptr_service != NULL)
	{
		list.append(QString::fromStdString(videoDisplay));
		list.append(QString::fromStdString(resolution));
		params["params"] = list;
		/*setting resolution by calling callMethod with METHOD_DISPLAY_SETTINGS_SET_CURRENT_RESOLUTION*/
		/*This is not yet implemented,cause segmentation fault. This will be added once implementaion done
		  in the component*/
		//ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_SET_CURRENT_RESOLUTION,params); 
		/*getting resolution by calling callMethod with METHOD_DISPLAY_SETTINGS_GET_CURRENT_RESOLUTION*/
		/*This is not yet implemented,cause segmentation fault. This will be added once implementaion done
		  in the component*/
		//resultParams=ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_CURRENT_RESOLUTION,params);
		/*result param will be filled once the implemetation for get and set resolution APIs are done*/
		//sprintf(resolutionDetails,"%d",resultParams["resolution"])
		//strcat(curResolutionDetail,resolutionDetails);
		//DEBUG_PRINT(DEBUG_LOG,"%s",curResolutionDetail);
		response["details"]=curResolutionDetail;
		/*Implementation from component is not done , so this will return FAILURE*/
		response["result"]="FAILURE";
	}
	else
	{
		response["result"]="FAILURE";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	free(resolutionDetails);
#else
	response["result"]="FAILURE";
	response["details"]="DisplaySettingsService unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetCurrentResolution ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_HN_SetDeviceName 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_HN_SET_DEVICE_NAME and METHOD_HN_GET_DEVICE_NAME method as
		  parameters.
 *parameter [in]: device_name - name of the device.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetDeviceName ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["device_name"]==NULL )
        {
		response["result"]="FAILURE";
		response["details"]="device_name is NULL";
                return TEST_FAILURE;
        }
        std::string deviceName=req["device_name"].asCString();
        ServiceParams params,resultParams;
        char deviceNameDetail[STR_DETAILS_200]= "DeviceName:";
        QVariantList list;
        char *nameDetails = (char*)malloc(sizeof(char)*STR_DETAILS_100);
	memset(nameDetails , '\0', (sizeof(char)*STR_DETAILS_100));
        Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(HOME_NETWORKING_SERVICE_NAME);
	if(ptr_service != NULL)
	{
		list.append(QString::fromStdString(deviceName));
		params["params"] = list;
		/*setting device name by calling callMethod with METHOD_HN_SET_DEVICE_NAME*/
		ptr_service->callMethod(METHOD_HN_SET_DEVICE_NAME,params);
		/*getting device name by calling callMethod with METHOD_HN_GET_DEVICE_NAME*/
		resultParams=ptr_service->callMethod(METHOD_HN_GET_DEVICE_NAME,params);
		strcpy(nameDetails,resultParams["deviceName"].toString().toUtf8().constData());
		strcat(deviceNameDetail,nameDetails);
		DEBUG_PRINT(DEBUG_LOG,"%s",deviceNameDetail);
		response["result"]="SUCCESS";
		response["details"]=deviceNameDetail;
	}
	else
	{
		response["result"]="FAILURE";
		response["details"]="SM getGlobalService failed";
		DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
	}
	free(nameDetails);
#else
        response["result"]="FAILURE";
        response["details"]="Home Networking Service unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetDeviceName ---->Exit\n");
	return TEST_SUCCESS;	
}

bool ServiceManagerAgent::SM_Services_GetName(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_GetName ---->Entry\n");

        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
		response["details"]="service_name is NULL";
                return TEST_FAILURE;
        }
        std::string serviceName=req["service_name"].asCString();

	/*Calling getGlobalService API to get the service instance*/
        Service* ptr_service=NULL;
        ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
        if(ptr_service != NULL)
        {
		if(QString::fromStdString(serviceName) == ptr_service->getName())
		{
                	DEBUG_PRINT(DEBUG_LOG,"GetName: %s", ptr_service->getName().toUtf8().constData());
                	response["result"]="SUCCESS";
                	response["details"]="GetName value from service name succesfull";
		}
		else
		{
			DEBUG_PRINT(DEBUG_ERROR,"GetName: %s", ptr_service->getName().toUtf8().constData());
			response["result"]="FAILURE";
			response["details"]="GetName value not matching service name";
		}
        }
        else
        {
                response["result"]="FAILURE";
		response["details"]="Failed to get GlobalService pointer from service name";
                DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
        }

	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_GetName ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_Services_SetAPIVersion
 *Descrption    : This will check the functionality of getApiVersionNumber and 
		  setApiVersionNumber APIs.
 *parameter [in]: req-  service_name-Name of the service.
			apiVersion - Parameter to be passed to callMethod API.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_Services_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_SetAPIVersion ---->Entry\n");
        if(&req["service_name"]==NULL || &req["apiVersion"] == NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service_name or apiVersion is NULL";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	int setApiVersion=req["apiVersion"].asInt();
	//ServiceParams params;
	int getApiVersion=0;
	char apiVersion[STR_DETAILS_20]= "API_VERSION:";
	char *versionDetails = (char*)malloc(sizeof(char)*STR_DETAILS_20);
	memset(versionDetails , '\0', (sizeof(char)*STR_DETAILS_20));
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	if(ptr_service != NULL)
	{
		getApiVersion =ptr_service->getApiVersionNumber();	
		if(setApiVersion==getApiVersion)
		{
			response["result"]="SUCCESS";
			response["details"]="SAME_DATA_ALREADY_ENTERED";
			return TEST_SUCCESS;	
		}
		/*set API version by calling setApiVersionNumber API*/
		ptr_service->setApiVersionNumber(setApiVersion);
		/*get API version by calling getApiVersionNumber API*/
		getApiVersion =ptr_service->getApiVersionNumber();	
		sprintf(versionDetails,"%d",getApiVersion);
		strcat(apiVersion,versionDetails);
		DEBUG_PRINT(DEBUG_LOG,"Services:%s",apiVersion);
		response["result"]="SUCCESS";
		response["details"]=apiVersion;
	}
	else
	{
		response["result"]="FAILURE";
		response["details"]="SM getGlobalService failed";
		DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
	}
	free(versionDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_SetAPIVersion ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_Services_RegisterForEvents
 *Descrption    : This function will check the functionality of registerForEvents
                  and unregisterEvents APIs.
 *parameter [in]: service_name - Name of the service.
		  event_name - event to be registered.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_Services_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_RegisterForEvents ---->Entry\n");
        if(&req["service_name"]==NULL || &req["event_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service_name or event_name is NULL";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	std::string eventName=req["event_name"].asCString();
	QList<QString> event_list;
	event_list.append(QString::fromStdString(eventName));
	//ServiceParams params;
	ServiceListener *listener=NULL;
	bool register_flag=false,unregister_flag=false;
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	if(ptr_service != NULL)
	{
		/*registering events for a given service*/
		register_flag =ptr_service->registerForEvents(event_list,listener);
		/*deregistering events for a given service*/
		unregister_flag =ptr_service->unregisterEvents(listener);	
		if(register_flag == 1 && unregister_flag==1)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nEvent are registered and unregistered successfully\n");
			response["result"]="SUCCESS";
			response["details"]="Events Registered and unRegistered";
		}
		else
		{
			DEBUG_PRINT(DEBUG_LOG,"\nFailed to register and unregister events\n");
			response["result"]="FAILURE";
			response["details"]="Failed to register and unregister events";
		}
	}
	else
	{
		response["result"]="FAILURE";
		response["details"]="SM getGlobalService failed";
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_RegisterForEvents ---->Exit\n");
	return TEST_SUCCESS;	
}

/***************************************************************************
 *Function name : SM_DeviceSetting_GetDeviceInfo
 *Descrption    : This function will check the functionality of GetDeviceInfo
                  of DeviceSettingService.
 *parameter [in]: methodType - Supported device parameter.
 *****************************************************************************/
bool ServiceManagerAgent::SM_DeviceSetting_GetDeviceInfo(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_DeviceSetting_GetDeviceInfo ---->Entry\n");

#ifdef USE_DEVICE_SETTINGS_SERVICE
        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(DEVICE_SETTING_SERVICE_NAME))
        {
	    ptrService = ServiceManager::getInstance()->getGlobalService(DEVICE_SETTING_SERVICE_NAME);
            if (ptrService != NULL)
            {
		QVariantList paramList;
                ServiceParams inParams;
		ServiceParams outResult;
  		QString methodType = "ecm_mac";
		//QString methodType = "estb_mac";
		char stringDetails[STR_DETAILS_50] = {'\0'};

		paramList.append(methodType);
		inParams["params"] = paramList;
                outResult = ptrService->callMethod(DeviceSettingService::METHOD_DEVICE_GET_DEVICE_INFO, inParams);

		QString data;
                foreach (QVariant value, outResult)
                {
		    if (!(value.toString().isNull() || value.toString().isEmpty()))
		    {
                        data += value.toString();
                        data += "  ";
		    }
                }

		if (data.isEmpty())
		{
		    response["result"]="FAILURE";
		}
		else
		{
              	    response["result"]="SUCCESS";
		}

		sprintf(stringDetails,"%s: %s", methodType.toUtf8().constData(), data.toUtf8().constData());
		response["details"]=stringDetails;
            }
	    else
	    {
		response["result"]="FAILURE";
		response["details"]="Failed to get serviceManager instance using getGlobalService";
            }
        }
	else
	{
		response["result"]="FAILURE";
		response["details"]="Service does not exists";
	}
#else
	response["result"]="FAILURE";
	response["details"]="DeviceSetting Service unsupported";
#endif
	DEBUG_PRINT(DEBUG_TRACE,"SM_DeviceSetting_GetDeviceInfo ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_ScreenCapture_Upload
 *Descrption    : This function will check the functionality of Upload url call method
                  of ScreenCaptureService.
 *parameter [in]: URL of web page.
 *****************************************************************************/
bool ServiceManagerAgent::SM_ScreenCapture_Upload(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_ScreenCapture_Upload ---->Entry\n");

#ifdef SCREEN_CAPTURE
        Service* ptrService = NULL;
     	ptrService = ServiceManager::getInstance()->getGlobalService(ScreenCaptureService::NAME);
        if (ptrService != NULL)
        {
		char stringDetails[STR_DETAILS_50] = {'\0'};	
		QVariantList paramList;
                ServiceParams inParams;

		std::string urlString = req["url"].asCString();
                paramList.append(QString::fromStdString(urlString));
                inParams["params"] = paramList;

		DEBUG_PRINT(DEBUG_TRACE,"Attempting to load the following web page: %s\n", urlString.c_str());
                ServiceParams outResult = ptrService->callMethod(ScreenCaptureService::METHOD_UPLOAD, inParams);

       		//bool ok = outResult[ScreenCaptureService::PARAM_STATUS].toBool();
        	//QString errorMsg = outResult[ScreenCaptureService::PARAM_MESSGAGE].toString();
        	//QString callGUID = outResult[ScreenCaptureService::PARAM_CALL_GUID].toString();
		bool status = outResult["success"].toBool();
                if (false == status)
                {
                    response["result"]="FAILURE";
                }
                else
                {
                    response["result"]="SUCCESS";
                }

                QString data;
                foreach (QVariant value, outResult)
                {
                    if (!(value.toString().isNull() || value.toString().isEmpty()))
                    {
                        data += value.toString();
                        data += "  ";
                    }
                }
		sprintf(stringDetails,"status = %s", data.toUtf8().constData());
		response["details"]=stringDetails;
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="Failed to get serviceManager instance using getGlobalService";
        }
#else
	response["result"]="FAILURE";
	response["details"]="ScreenCapture Service unsupported";
#endif
	DEBUG_PRINT(DEBUG_TRACE,"SM_ScreenCapture_Upload ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_WebSocket_GetUrl
 *Descrption    : This function will check the functionality of GetUrl
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/                
bool ServiceManagerAgent::SM_WebSocket_GetUrl(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetUrl ---->Entry\n");

#ifdef ENABLE_WEBSOCKET_SERVICE
        Service* ptrService = NULL;
        ptrService = ServiceManager::getInstance()->getGlobalService(WebSocketService::SERVICE_NAME);
        if (ptrService != NULL)
        {
                QUrl url = dynamic_cast<WebSocketService *>(ptrService)->requestUrl();
		if (url.isEmpty())
		{
			DEBUG_PRINT(DEBUG_ERROR,"Failed to get request url\n");
			response["result"]="FAILURE";
			response["details"]="Failed to get request url";
		}
		else
		{
			DEBUG_PRINT(DEBUG_LOG,"Url: %s\n", url.toString().toUtf8().constData());
                	response["result"]="SUCCESS";
			response["details"]=url.toString().toUtf8().constData();
		}
        }
	else
	{
		response["result"]="FAILURE";
		response["details"]="Failed to get serviceManager instance using getGlobalService";
	}
#else
        response["result"]="FAILURE";
        response["details"]="WebSocket Service unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetUrl ---->Exit\n");
		
	return TEST_SUCCESS;
}
              
/***************************************************************************
 *Function name : SM_WebSocket_GetReadyState
 *Descrption    : This function will check the functionality of GetReadyState
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/
bool ServiceManagerAgent::SM_WebSocket_GetReadyState(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetReadyState ---->Entry\n");

#ifdef ENABLE_WEBSOCKET_SERVICE
	Service* ptrService = NULL;
	ptrService = ServiceManager::getInstance()->getGlobalService(WebSocketService::SERVICE_NAME);
	
        if (ptrService != NULL)
        {
                WebSocketService::ReadyState state = WebSocketService::ReadyStateUnknown;
		state = dynamic_cast<WebSocketService *>(ptrService)->readyState();
                if (WebSocketService::ReadyStateUnknown == state)
                {
                        DEBUG_PRINT(DEBUG_ERROR,"Failed to get ready state\n");
                        response["result"]="FAILURE";
                        response["details"]="ReadyStateUnknown";
                }
                else
                {
                        char stringDetails[10] = {'\0'};
                        sprintf(stringDetails,"State=%d", state);
                        DEBUG_PRINT(DEBUG_LOG,"ReadyState: %d\n", state);
                        response["result"]="SUCCESS";
                        response["details"]=stringDetails;
                }
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="Failed to get serviceManager instance using getGlobalService";
        }
#else
        response["result"]="FAILURE";
        response["details"]="WebSocket Service unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetReadyState ---->Exit\n");

	return TEST_SUCCESS;
}
         
/***************************************************************************
 *Function name : SM_WebSocket_GetBufferedAmount
 *Descrption    : This function will check the functionality of GetBufferedAmount
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/       
bool ServiceManagerAgent::SM_WebSocket_GetBufferedAmount(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetBufferedAmount ---->Entry\n");

#ifdef ENABLE_WEBSOCKET_SERVICE
        Service* ptrService = NULL;
        ptrService = ServiceManager::getInstance()->getGlobalService(WebSocketService::SERVICE_NAME);

        if (ptrService != NULL)
        {
                qint64 buffAmt = 0;
                buffAmt = dynamic_cast<WebSocketService *>(ptrService)->bufferedAmount();
		char stringDetails[STR_DETAILS_50] = {'\0'};
		sprintf(stringDetails,"BufferedAmount=%lld", buffAmt);
		response["result"]="SUCCESS";
		response["details"]=stringDetails;
		DEBUG_PRINT(DEBUG_LOG,"BufferedAmount: %lld\n", buffAmt);		
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="Failed to get serviceManager instance using getGlobalService";
        }
#else
        response["result"]="FAILURE";
        response["details"]="WebSocket Service unsupported";
#endif

	DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetBufferedAmount ---->Exit\n");

	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_WebSocket_GetProtocol
 *Descrption    : This function will check the functionality of GetProtocol
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/
bool ServiceManagerAgent::SM_WebSocket_GetProtocol(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetProtocol ---->Entry\n");

#ifdef ENABLE_WEBSOCKET_SERVICE
        Service* ptrService = NULL;
        ptrService = ServiceManager::getInstance()->getGlobalService(WebSocketService::SERVICE_NAME);
        if (ptrService != NULL)
        {
                QString protocol = dynamic_cast<WebSocketService *>(ptrService)->protocol();
                if (protocol.isEmpty())
                {
                        DEBUG_PRINT(DEBUG_ERROR,"Failed to get protocol\n");
                        response["result"]="FAILURE";
                        response["details"]="Failed to get protocol";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_LOG,"Protocol: %s\n", protocol.toUtf8().constData());
                        response["result"]="SUCCESS";
                        response["details"]=protocol.toUtf8().constData();
                }
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="Failed to get serviceManager instance using getGlobalService";
        }
#else
        response["result"]="FAILURE";
        response["details"]="WebSocket Service unsupported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_WebSocket_GetProtocol ---->Exit\n");

	return TEST_SUCCESS;
}

#ifdef HAS_API_HDMI_CEC
/*static HdmiCecService *ptr_service=NULL;*/
#endif

/***************************************************************************
 *Function name : SM_HdmiCec_ClearCecLog
 *Descrption    : This will ClearCecLog and new log entry be done.
 *parameter [in]: NONE.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SM_HdmiCec_ClearCecLog ---> Entry\n");
#ifdef HAS_API_HDMI_CEC
	string cecLogPath = rdkLogPath + "/" + "cec.txt";
	string clearLogCmd = "cat /dev/null > " + cecLogPath;

	DEBUG_PRINT(DEBUG_TRACE, "clearLogCmd: %s\n",clearLogCmd.c_str());
	try
	{
		system((char *)clearLogCmd.c_str());
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured not able to Clear Cec Log\n");
                DEBUG_PRINT(DEBUG_TRACE, "SM_HdmiCec_ClearCecLog ---> Exit\n");
	        response["result"]="FAILURE";
	        response["details"]="Exception occured not able to Clear Cec Log";
		
		return TEST_FAILURE;
	}
	
	DEBUG_PRINT(DEBUG_TRACE,"Clear Cec Log Success\n");
	response["result"]="SUCCESS";
        response["details"]="Clear Cec Log Success";
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif
        DEBUG_PRINT(DEBUG_TRACE, "SM_HdmiCec_ClearCecLog ---> Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_CheckStatus
 *Descrption    : This will search for the pattern in the cec log.
 *parameter [in]: pattern - string.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_CheckStatus(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckStatus ---> Entry\n");

#ifdef HAS_API_HDMI_CEC 
	string pattern = req["pattern"].asCString();
	string cecLogPath = rdkLogPath + "/" + "cec.txt";
	string cecTdkLog = "cecTdkLog.txt";
	string tdkLogPath = tdkPath + "logs/" + cecTdkLog;
	string cecTdkLogCpCmd = "cp -r " + cecLogPath + " " + tdkLogPath;
	string setPermission = "chmod -R 777 " + tdkLogPath;	
	
	DEBUG_PRINT(DEBUG_TRACE,"Cec Tdk Log Path: %s\n",cecTdkLogCpCmd.c_str());
	DEBUG_PRINT(DEBUG_TRACE,"SetPermissionPath: %s\n",setPermission.c_str());
	
	/*Copy Cec.log to TDK folder and handling exception for system call*/
	try
	{	
		system((char *)cecTdkLogCpCmd.c_str());
                system((char*)setPermission.c_str());
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured, Failed to copy Cec.log to TDK folder\n");
		response["result"]="FAILURE";
	        response["details"]="Exception occured, Failed to copy Cec.log to TDK folder";
                return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_TRACE,"Successfully copied Cec.txt to TDK folder\n");
	
	/* Checking for the pattern from Cec.txt*/
	ifstream cecLogFile;
	string lineMatching;
	DEBUG_PRINT(DEBUG_TRACE,"File Open for searching the pattern: %s\n",tdkLogPath.c_str());
	DEBUG_PRINT(DEBUG_TRACE,"Pattern to be searched: %s\n",pattern.c_str());
	cecLogFile.open(tdkLogPath.c_str());
	if (cecLogFile.is_open())
	{
		while (!cecLogFile.eof())
                {
			if(getline(cecLogFile,lineMatching)>0)
			{
				if (lineMatching.find(pattern) != string::npos)
				{
					response["result"] = "SUCCESS";
					response["details"] = lineMatching.c_str();
					response["log-path"]= tdkLogPath.c_str();
					break;
				}
			}
			else
			{
                                response["result"] = "FAILURE";
                                response["details"] = "No Pattern found in Log file";
                                response["log-path"]= tdkLogPath.c_str();
				return TEST_FAILURE;
			}
			
		}
		cecLogFile.close();
		response["result"] = "SUCCESS";
	}
	else
	{
		DEBUG_PRINT(DEBUG_TRACE,"Unable to open %s\n", tdkLogPath.c_str());
                DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckStatus ---> Exit\n");
                response["result"] = "FAILURE";
                response["details"] = "Unable to open the log file";
		return TEST_FAILURE;
	}
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif		
	DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckStatus ---> Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SetEnabled
 *Descrption    : This will enable the Cec service.
 *parameter [in]: req - set true or false.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_SetEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_SetEnabled ---->Entry\n");

	bool valueToSetEnabled = req["valueToSetEnabled"].asInt();
	bool getEnabledResult = false;

	DEBUG_PRINT(DEBUG_TRACE,"Value passed to setEnabled: %d (true - 1, false - 0)\n",valueToSetEnabled);

#ifdef HAS_API_HDMI_CEC
	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");

	if(ptr_service != NULL)
        {
		ptr_service->setEnabled(valueToSetEnabled);
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setEnabled called.\n");
		
		getEnabledResult = ptr_service->getEnabled();
		if (valueToSetEnabled == getEnabledResult)
		{
			DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setEnabled() call Success.\n");
                	response["result"]="SUCCESS";
	                response["details"]="HdmiCec Service setEnabled() call Success.";
		}
		else
		{
			DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setEnabled() call Failure.\n");
	                response["result"]="FAILURE";
        	        response["details"]="HdmiCec Service setEnabled() call Failure.";
			
			return TEST_FAILURE;
		}
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
	
		return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_SetEnabled ---->Exit\n");
	return TEST_SUCCESS;
}


/***************************************************************************
 *Function name : SM_HdmiCec_GetEnabled
 *Descrption    : This will get current state (whether it is enabled or disabled) of Cec service.
 *parameter [in]: NONE.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_GetEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetEnabled ---->Entry\n");
	std::stringstream details;	
	/*Default value - false*/
        bool getEnabledResult = false;

#ifdef HAS_API_HDMI_CEC

	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");

        if(ptr_service != NULL)
        {
                getEnabledResult = ptr_service->getEnabled();
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getEnabled called.\n");

                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getEnabled() call Success.\n");
		details << "Cec: "<<getEnabledResult;
                response["result"]="SUCCESS";
                response["details"]=details.str();
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetEnabled ---->Exit\n");
	return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SetName
 *Descrption    : This will sets the name of the STB device..
 *parameter [in]: req - name to be set to STB device as string.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_SetName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_SetName ---->Entry\n");
        std::stringstream details;
	QString nameToSet = QString::fromStdString(req["nameToSet"].asCString());
	QString getNameResult;

	DEBUG_PRINT(DEBUG_TRACE,"Value passed to setName: %s \n",nameToSet.toUtf8().constData());

#ifdef HAS_API_HDMI_CEC
	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");
        
	if(ptr_service != NULL)
        {
                ptr_service->setName(nameToSet);
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setName called.\n");

                getNameResult = ptr_service->getName();
                if (nameToSet == getNameResult)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setName() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="HdmiCec Service setName() call Success.";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setName() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="HdmiCec Service setName() call Failure.";

                        return TEST_FAILURE;
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetEnabled ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_GetName
 *Descrption    : This will get current STB device name.
 *parameter [in]: NONE.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_GetName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetName ---->Entry\n");
        std::stringstream details;
	QString getNameResult;

#ifdef HAS_API_HDMI_CEC
	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");

        if(ptr_service != NULL)
        {
                getNameResult = ptr_service->getName();
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getName called.\n");

                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getName() call Success.\n");
                details << "Cec: "<<getNameResult.toUtf8().constData();
                response["result"]="SUCCESS";
                response["details"]=details.str();
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetName ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_GetConnectedDevices
 *Descrption    : This will get the number of devices connected to STB.
 *parameter [in]: NONE.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetConnectedDevices ---->Entry\n");
        std::stringstream details;
	QVariantList listOfDevicesConnected;

#ifdef HAS_API_HDMI_CEC

	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");
        if(ptr_service != NULL)
        {
                listOfDevicesConnected = ptr_service->getConnectedDevices();
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getConnectedDevices called.\n");

                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getConnectedDevices() call Success.\n");
                details << "Cec: "<<listOfDevicesConnected.count();
                response["result"]="SUCCESS";
                response["details"]=details.str();
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetConnectedDevices ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SendMessage
 *Descrption    : This will send the message to connected STB.
 *parameter [in]: req - message.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_SendMessage(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_SendMessage ---->Entry\n");
        std::stringstream details;
	QString messageToSend = QString::fromStdString(req["messageToSend"].asCString());
	
	DEBUG_PRINT(DEBUG_TRACE,"Value passed to sendMessage: %s \n",messageToSend.toUtf8().constData());

#ifdef HAS_API_HDMI_CEC
	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");
        if(ptr_service != NULL)
        {
                ptr_service->sendMessage(messageToSend);
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service sendMessage() called.\n");

                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service sendMessage() call Success.\n");
                response["result"]="SUCCESS";
                response["details"]="HdmiCec Service sendMessage() call Success.";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_SendMessage ---->Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : SM_HdmiCec_OnMessage
 *Descrption    : This will be fired when a message is sent from an HDMI device to STB.
 *parameter [in]: req - message.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_OnMessage(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_OnMessage ---->Entry\n");
        std::stringstream details;
        QString onMessage = QString::fromStdString(req["onMessage"].asCString());

        DEBUG_PRINT(DEBUG_TRACE,"Value passed to onMessage: %s \n",onMessage.toUtf8().constData());

#ifdef HAS_API_HDMI_CEC
	QString serviceName = HdmiCecService::SERVICE_NAME;
	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(serviceName));
	DEBUG_PRINT(DEBUG_TRACE,"After: HdmiCecService new created with dynamic cast\n");
        if(ptr_service != NULL)
        {
                ptr_service->onMessage(onMessage);
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service onMessage() called.\n");

                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service onMessage() call Success.\n");
                response["result"]="SUCCESS";
                response["details"]="HdmiCec Service onMessage() call Success.";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";

                return TEST_FAILURE;
        }
#else
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_OnMessage ---->Exit\n");
        return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "ServiceManagerAgent".
 *
 **************************************************************************/

extern "C" ServiceManagerAgent* CreateObject()
{
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Entry\n");
	return new ServiceManagerAgent();
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Exit\n");
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool ServiceManagerAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"\n ServiceManagerAgent shutting down \n");
        if(ptrAgentObj==NULL)
        {
                return TEST_FAILURE;
        }

	// ServiceManager APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_RegisterService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_UnRegisterService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DoesServiceExist");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_GetRegisteredServices");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_GetGlobalService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_GetSetting");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_CreateService");
	// Services common APIs
	ptrAgentObj->UnregisterMethod("TestMgr_Services_GetName");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_SetAPIVersion");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_RegisterForEvents");
	// HomeNetworking Service callMethod APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_EnableMDVR");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_EnableVPOP");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_SetDeviceName");
	// DisplaySettings Service callMethod APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DisplaySetting_SetZoomSettings");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DisplaySetting_SetCurrentResolution");
        // DeviceSettingService callMethod APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DeviceSetting_GetDeviceInfo");
	// ScreenCaptureService callMethod APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_ScreenCapture_Upload");
	// WebSocketService callMethod APIs
	ptrAgentObj->UnregisterMethod("TestMgr_SM_WebSocket_GetUrl");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_WebSocket_GetReadyState");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_WebSocket_GetBufferedAmount");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_WebSocket_GetProtocol");
	/*HdmiCecService API's*/
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_SetEnabled");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_GetEnabled");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_SetName");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_GetName");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_GetConnectedDevices");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_SendMessage");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_OnMessage");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_ClearCecLog");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_CheckStatus");

	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(ServiceManagerAgent *agentobj)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Entry\n");
	DEBUG_PRINT(DEBUG_LOG,"Destroying ServiceManagerAgent object");
	delete agentobj;
	DEBUG_PRINT(DEBUG_TRACE,"\n DestroyObject ---->Exit\n");
}

