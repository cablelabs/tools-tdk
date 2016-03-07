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

#ifdef HAS_API_APPLICATION
#define OCAP_LOG "/opt/logs/ocapri_log.txt"
#define IP_FILE "/opt/ip.txt"

QString listToString(QVariantList conInfo);

/*parses and returns contents of QVariantMap as QStrings*/
QString mapToString(QVariantMap infoMap)
{
        QString details;

        QVariantMap::const_iterator itr;
        for(itr = infoMap.constBegin(); itr != infoMap.constEnd(); itr++)
        {
                details += itr.key();
                details += ": ";
                if(itr.value().type() == QVariant::String)
                        details += itr.value().toString();
                else if(itr.value().type() == QVariant::List)
                        details += listToString(itr.value().toList());
                details += "; ";
        }
        return details;
}


/*parses and returns contents of QVariantList as QStrings*/
QString listToString(QVariantList conInfo)
{
        QString details;

        details += "[ ";
        for(int i=0; i<conInfo.size(); i++)
        {
                if(conInfo[i].type() == QVariant::Map)
                        details += mapToString(conInfo[i].toMap());
                else if(conInfo[i].type() == QVariant::String)
                {
                        details += conInfo[i].toString();
                        details += " ";
                }
        }
        details += " ]";
        return details;
}
#endif
#ifdef HAS_API_HDMI_CEC
std::string rdkLogPath = getenv("RDK_LOG_PATH");
std::string tdkPath = getenv("TDK_PATH");
std::string cecRdkLogFile = "cec_log.txt";
std::string cecTdkLogFile = "cec_tdk.log";
static bool gDebugLogEnabled = false;
static HdmiCecService *pHdmiService = NULL;

static void checkDebugLogEnabled(void)
{
        if(false == gDebugLogEnabled)
        {
                // Enable debug log in platform before invoking sendMessage
                string enableCecLogCmd = "source " + tdkPath + "/" + ENABLE_CECLOG;
                try
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Command to enable debug log: %s\n", enableCecLogCmd.c_str());
                        system((char *)enableCecLogCmd.c_str());
                        gDebugLogEnabled = true;
                        DEBUG_PRINT(DEBUG_TRACE, "CEC Debug Log enabled\n");
                }
                catch(...)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Failed to enable cec debug log\n");
                }
        }
        else
        {
            DEBUG_PRINT(DEBUG_TRACE, "CEC Debug Log already enabled\n");
        }
}

bool startHdmiCecService(void)
{
        bool bReturn = false;
        DEBUG_PRINT(DEBUG_TRACE,"Create new instance of HdmiCec Service\n");
        if (ServiceManager::getInstance()->doesServiceExist(HdmiCecService::SERVICE_NAME))
        {
                pHdmiService = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->createService(HdmiCecService::SERVICE_NAME));
                if (pHdmiService != NULL)
                {
                        DEBUG_PRINT(DEBUG_LOG,"pHdmiService = %p\n", pHdmiService);
                        bReturn = true;
                        bool getEnabledResult = pHdmiService->getEnabled();
                        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getEnabled value: %d\n",getEnabledResult);
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Failed to create instance of HdmiCecService\n");
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service does not exist");
        }

        return bReturn;
}

void stopHdmiCecService(void)
{
        DEBUG_PRINT(DEBUG_TRACE,"Delete instance of HdmiCec Service\n");
        if (pHdmiService != NULL)
        {
                DEBUG_PRINT(DEBUG_LOG,"Delete %p\n", pHdmiService);
                delete pHdmiService;
                pHdmiService = NULL;
                DEBUG_PRINT(DEBUG_LOG,"\nDeleted service successfully\n");
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service does not exist");
        }
}
#endif

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
        ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_Services_UnRegisterForEvents,"TestMgr_SM_UnRegisterForEvents");
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
        ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_FlushCecData,"TestMgr_SM_HdmiCec_FlushCecData");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HdmiCec_CheckCecData,"TestMgr_SM_HdmiCec_CheckCecData");
        /*ApplicationService APIs*/
        ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_AppService_GetAppInfo,"TestMgr_SM_AppService_GetAppInfo");
        ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_AppService_SetConnectionReset,"TestMgr_SM_AppService_setConnectionReset");
        ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_AppService_Restore_rmfconfig,"TestMgr_SM_AppService_Restore_rmfconfig");

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

#ifdef HAS_API_HDMI_CEC
	/*Check if the environment variables are set or not */
        if( rdkLogPath.empty() )
        {
                DEBUG_PRINT(DEBUG_ERROR,"Environment variable not set for RDK_LOG_PATH\n");
                return "FAILURE<DETAILS>Environment variable not set for \"RDK_LOG_PATH\"";
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"RDK_LOG_PATH=%s\n",rdkLogPath.c_str());
        }

        if( tdkPath.empty() )
        {
                DEBUG_PRINT(DEBUG_ERROR,"Environment variable not set for TDK_PATH\n");
                return "FAILURE<DETAILS>Environment variable not set for \"TDK_PATH\"";
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"TDK_PATH=%s\n",tdkPath.c_str());
        }
#endif

#ifdef HAS_API_APPLICATION
        IARM_Bus_Init(IARM_BUS_TDK_NAME);
        IARM_Bus_Connect();
#endif

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

#ifdef HAS_API_APPLICATION
        IARM_Bus_Disconnect();
        IARM_Bus_Term();
#endif	
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
#ifdef HAS_API_APPLICATION
        else if (serviceName == ApplicationService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createApplicationService;
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

#ifdef HAS_API_HDMI_CEC
        if (serviceName == HdmiCecService::SERVICE_NAME)
        {
                DEBUG_PRINT(DEBUG_LOG,"\n%s create hdmicec handle\n", serviceName.toUtf8().constData());
                registerStatus = startHdmiCecService();
        }
#endif

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
#ifdef HAS_API_HDMI_CEC
                if (QString::fromStdString(serviceName) == HdmiCecService::SERVICE_NAME)
                {
                        //stopHdmiCecService();
                }
#endif
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
	bool register_flag=false;
	Service* ptr_service=NULL;
	/*Calling getGlobalService API to get the service instance*/
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	if(ptr_service != NULL)
	{
		/*registering events for a given service*/
		register_flag =ptr_service->registerForEvents(event_list,listener);
		/*deregistering events for a given service*/
		//unregister_flag =ptr_service->unregisterEvents(listener);	
		if(register_flag == 1 )
		{
			DEBUG_PRINT(DEBUG_LOG,"\nEvent are registered successfully\n");
			response["result"]="SUCCESS";
			response["details"]="Events Registered ";
		}
		else
		{
			DEBUG_PRINT(DEBUG_LOG,"\nFailed to register events\n");
			response["result"]="FAILURE";
			response["details"]="Failed to register events";
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
 *Function name : SM_Services_UnRegisterForEvents
 *Descrption    : This function will check the functionality of unregisterEvents APIs.
 *parameter [in]: service_name - Name of the service.
                  event_name - event to be registered.
 *****************************************************************************/
bool ServiceManagerAgent::SM_Services_UnRegisterForEvents(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_UnRegisterForEvents ---->Entry\n");
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
        bool unregister_flag=false;
        Service* ptr_service=NULL;
        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
        if(ptr_service != NULL)
        {
                /*registering events for a given service*/
                //#register_flag =ptr_service->registerForEvents(event_list,listener);
                /*deregistering events for a given service*/
                unregister_flag =ptr_service->unregisterEvents(listener);
                if(unregister_flag==1)
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nEvent are unregistered successfully\n");
                        response["result"]="SUCCESS";
                        response["details"]="Events unRegistered";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nFailed to unregister events\n");
                        response["result"]="FAILURE";
                        response["details"]="Failed to unregister events";
                }
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
        }
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_UnRegisterForEvents ---->Exit\n");
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
               QList<QString> method_list;
                method_list << "downloadIP" << "ecm_ip" << "boxIP" << "estb_ip" << "macAddress" << "estb_mac" << "ecm_mac" << "ethernet_mac" << "MODEL_NUM" << "imageVersion" << "BUILD_TYPE" << "DAC_INIT_TIMESTAMP" ;
                QVariantList paramList;
                ServiceParams inParams;
                ServiceParams outResult;
                QString methodType;
//              QString methodType = "ecm_mac";
                //QString methodType = "estb_mac";
                char stringDetails[STR_DETAILS_50] = {'\0'};
                QString details;

		/*invoke METHOD_DEVICE_GET_DEVICE_INFO with each method type in method_list*/
                for(int i=0; i<method_list.size(); i++)
                {
                        methodType = method_list.at(i);
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

                        sprintf(stringDetails,"%s: %s ", methodType.toUtf8().constData(), data.toUtf8().constData());
                        details.append(stringDetails);
                        printf("method and o/p is %s\n", stringDetails);
                        paramList.clear();
                        inParams.clear();
                        outResult.clear();
                }

                printf("Details: %s \n", details.toUtf8().constData());
                details.remove('\n');
                response["details"] = details.toUtf8().constData();
                if (details.isEmpty())
               {
                        response["details"] = "device info is empty";
                }
                response["result"]="SUCCESS";
                return TEST_SUCCESS;
            }
            else
            {
                response["details"]="Failed to get serviceManager instance using getGlobalService";
            }
        }
        else
        {
                response["details"]="Service does not exists";
        }
#else
        response["details"]="DeviceSetting Service unsupported";
#endif
        DEBUG_PRINT(DEBUG_TRACE,"SM_DeviceSetting_GetDeviceInfo ---->Exit\n");
        response["result"]="FAILURE";
        return TEST_FAILURE;
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

/***************************************************************************
 *Function name : SM_HdmiCec_ClearCecLog
 *Descrption    : This will ClearCecLog and new log entry be done.
 *parameter [in]: NONE.
 *****************************************************************************/
bool ServiceManagerAgent::SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SM_HdmiCec_ClearCecLog ---> Entry\n");

#ifdef HAS_API_HDMI_CEC
	string cecRdkLog = rdkLogPath + "/" + cecRdkLogFile;
	string clearLogCmd = "cat /dev/null > " + cecRdkLog;

	DEBUG_PRINT(DEBUG_TRACE, "clearLogCmd: %s\n",clearLogCmd.c_str());
	try
	{
		system((char *)clearLogCmd.c_str());
        	DEBUG_PRINT(DEBUG_TRACE,"Clear Cec Log Success\n");
        	response["result"]="SUCCESS";
        	response["details"]="Cleared Cec Log";
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured while clearing Cec Log\n");
	        response["result"]="FAILURE";
	        response["details"]="Failed to clear Cec Log";
	}
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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
	string cecRdkLog = rdkLogPath + "/" + cecRdkLogFile;
	/* Checking for the pattern from cec_log.txt*/
	string lineMatching;
	ifstream cecTDKLogIn;
	cecTDKLogIn.open(cecRdkLog.c_str());
	if (cecTDKLogIn.is_open())
	{
		DEBUG_PRINT(DEBUG_TRACE,"Successfully opened file: %s for searching pattern: %s\n", cecRdkLog.c_str(), pattern.c_str());

		// Assign default value to response
                response["result"] = "FAILURE";
                response["details"] = "No Pattern found in Log file";
                response["log-path"] = cecRdkLog.c_str();
		while ( cecTDKLogIn.good() )
                {
			if( getline(cecTDKLogIn,lineMatching) > 0 )
			{
				if ( lineMatching.find(pattern) != string::npos )
				{
					response["result"] = "SUCCESS";
					response["details"] = lineMatching.c_str();
					DEBUG_PRINT(DEBUG_TRACE,"Matching pattern found in log file\n");
					break;
				}
			}
		}
		cecTDKLogIn.close();
	}
	else
	{
		DEBUG_PRINT(DEBUG_TRACE,"Failed to open file: %s for searching pattern: %s\n", cecRdkLog.c_str(), pattern.c_str());
                response["result"] = "FAILURE";
                response["details"] = "Unable to open the tdk cec log file for searching message";
	}
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
	//HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
	if(ptr_service != NULL)
        {
		bool valueToSetEnabled = req["valueToSetEnabled"].asInt();
		DEBUG_PRINT(DEBUG_TRACE,"Calling HdmiCec Service setEnabled with value %d\n",valueToSetEnabled);
		ptr_service->setEnabled(valueToSetEnabled);
		bool getEnabledResult = ptr_service->getEnabled();
		DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getEnabled returned value: %d\n",getEnabledResult);
		if (valueToSetEnabled == getEnabledResult)
		{
			DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setEnabled() call Success.\n");
                	response["result"]="SUCCESS";
	                response["details"]="HdmiCec Service setEnabled value call success";
		}
		else
		{
			DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setEnabled() call Failure.\n");
	                response["result"]="FAILURE";
        	        response["details"]="HdmiCec Service setEnabled call failed";
		}
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {
		char stringDetails[STR_DETAILS_20] = {'\0'};
                bool getEnabledResult = ptr_service->getEnabled();
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getEnabled() returned value: %d\n", getEnabledResult);
		sprintf(stringDetails,"%d",getEnabledResult);
                response["result"]="SUCCESS";
                response["details"]=stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
	if(ptr_service != NULL)
        {
        	QString nameToSet = QString::fromStdString(req["nameToSet"].asCString());
        	DEBUG_PRINT(DEBUG_TRACE,"Calling setName with value : %s\n",nameToSet.toUtf8().constData());
                ptr_service->setName(nameToSet);
                QString getNameResult = ptr_service->getName();
                DEBUG_PRINT(DEBUG_TRACE,"getName returned value: %s\n",getNameResult.toUtf8().constData());
                if (nameToSet == getNameResult)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setName() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="HdmiCec Service setName call success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service setName() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="HdmiCec Service setName call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {
		char stringDetails[STR_DETAILS_100] = {'\0'};
                QString getNameResult = ptr_service->getName();
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCecService Device getName = %s\n", getNameResult.toUtf8().constData());
		sprintf(stringDetails,"%s", getNameResult.toUtf8().constData());
                response["result"]="SUCCESS";
                response["details"]=stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {
		char stringDetails[STR_DETAILS_20] = {'\0'};
                QVariantList listOfDevicesConnected = ptr_service->getConnectedDevices();
		DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service getConnectedDevices size = %d\n", listOfDevicesConnected.size());
                for(int j = 0; j < listOfDevicesConnected.size(); j++)
		{
			DEBUG_PRINT(DEBUG_TRACE,"ConnectedDevice:%d Address: %d\n", j+1, listOfDevicesConnected.value(j).toInt());
		}

		sprintf(stringDetails,"%d",listOfDevicesConnected.size());
                response["result"]="SUCCESS";
                response["details"]=stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {
                checkDebugLogEnabled();
        	if(false == gDebugLogEnabled)
        	{
                        response["result"]="FAILURE";
                	response["details"]="Failed to enable debug cec log";
		}
		else
		{
			std::string messageToSend = req["messageToSend"].asCString();
			DEBUG_PRINT(DEBUG_TRACE,"Message to Send: %s\n", messageToSend.c_str());
			DEBUG_PRINT(DEBUG_TRACE,"Length of message received: %d\n", messageToSend.length());
                        if (messageToSend.length() == 20)
                        {
                            const int msgLength = 7;
                            uint8_t *buf = new uint8_t [msgLength];
                            istringstream bufferStr(messageToSend);
                            DEBUG_PRINT(DEBUG_TRACE,"Hex stream input: ");
                            for (unsigned int i = 0; i < msgLength; i++)
                            {
                                unsigned int value;
                                bufferStr >> std::hex >> value;
                                buf[i] = value & 0xff;
                                printf("%x ", buf[i]);
                            }
                            printf("\n");

                            // Convert hex stream to Base64 Qbyte array for sendMessage
                            QByteArray byte_array = QByteArray((const char*)buf,msgLength);
                            ptr_service->sendMessage(byte_array.toBase64());

                            if (buf) {
                                delete [] buf;
                                buf = NULL;
                            }
	              	    response["result"]="SUCCESS";
                	    response["details"]="HdmiCec Service sendMessage call success";
                        }
                        else
                        {
                            response["result"]="FAILURE";
                            response["details"]="Message length not equal to 7 bytes";
                        }
		}
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
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

#ifdef HAS_API_HDMI_CEC
//	HdmiCecService *ptr_service = dynamic_cast<HdmiCecService*>(ServiceManager::getInstance()->getGlobalService(HdmiCecService::SERVICE_NAME));
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {
        	QString onMessage = QString::fromStdString(req["onMessage"].asCString());
        	DEBUG_PRINT(DEBUG_TRACE,"Value passed to onMessage: %s \n",onMessage.toUtf8().constData());
                ptr_service->onMessage(onMessage);
                DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service onMessage() call Success.\n");
                response["result"]="SUCCESS";
                response["details"]="HdmiCec Service onMessage call success.";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create HdmiCec Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create HdmiCec Service handler.";
        }
#else
	DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_OnMessage ---->Exit\n");
        return TEST_SUCCESS;
}

bool ServiceManagerAgent::SM_HdmiCec_FlushCecData(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_FlushCecData ---->Entry\n");

#ifdef HAS_API_HDMI_CEC
        // Flush CEC Persistant data in platform
        string flushCecDataCmd = "source " + tdkPath + "/" + FLUSH_CECDATA + " " + CEC_SETTING_ENABLED_FILE;
        try
        {
                DEBUG_PRINT(DEBUG_TRACE,"Command to flush CEC Persistant data: %s\n", flushCecDataCmd.c_str());
                system((char *)flushCecDataCmd.c_str());
                response["result"]="SUCCESS";
                response["details"]="Successfully flushed CEC Persistant Data";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_TRACE,"Exception caught while flushing CEC Persistant data\n");
                response["result"]="FAILURE";
                response["details"]="Exception caught while flushing CEC Persistant data";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_FlushCecData ---->Exit\n");
        return TEST_SUCCESS;
}

bool ServiceManagerAgent::SM_HdmiCec_CheckCecData(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckCecData ---->Entry\n");

#ifdef HAS_API_HDMI_CEC
        // Check if CEC Persistant data is present in platform
        string checkCecDataCmd = "source " + tdkPath + "/" + CHECK_CECDATA + " " + CEC_SETTING_ENABLED_FILE;
        DEBUG_PRINT(DEBUG_TRACE,"Command to check if CEC Persistant data is present: %s\n", checkCecDataCmd.c_str());
        FILE *pipe = popen(checkCecDataCmd.c_str(), "r");
        if (!pipe)
        {
                DEBUG_PRINT(DEBUG_TRACE,"Error occured in creating pipe to check CEC persistant data\n");
                response["result"]="FAILURE";
                response["details"]="Error occured in creating pipe to check CEC persistant data";
        }
        else
        {
                char output[1024] = {'\0'};
                /* Read the output */
                while (fgets(output, sizeof(output)-1, pipe) != NULL) {
                        DEBUG_PRINT(DEBUG_TRACE, "line output: %s\n",output);
                }
                pclose(pipe);

                DEBUG_PRINT(DEBUG_TRACE, "CheckCecData output: %s\n",output);
                if(strstr(output, "FOUND") != NULL)
                {
                        response["result"]="SUCCESS";
                        response["details"]="CEC Persistent Data Found";
                }
                else
                {
                        response["result"]="FAILURE";
                        response["details"]="CEC Persistent Data Not Found";
                }
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckCecData ---->Exit\n");
        return TEST_SUCCESS;
}

bool ServiceManagerAgent::SM_AppService_GetAppInfo(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AppService_GetAppInfo---->Entry\n");

#ifdef HAS_API_APPLICATION
        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(ApplicationService::SERVICE_NAME))
        {
                ptrService = ServiceManager::getInstance()->getGlobalService(ApplicationService::SERVICE_NAME);
                if (ptrService != NULL)
                {
                        ServiceParams inParams;
                        QVariantList conInfoList;
                        QString conInfo;

                        ServiceParams outResult = ptrService->callMethod("getAppInfo", inParams);
                        conInfoList = outResult["appConnectionInfo"].toList();
                        if(conInfoList.isEmpty())
                        {
                                response["result"]="FAILURE";
                                response["details"]="appConnectionInfo is empty";
                                return TEST_FAILURE;
                        }
                        conInfo = listToString(conInfoList);
                        DEBUG_PRINT(DEBUG_TRACE,"APPINFO: \n %s \n",conInfo.toUtf8().constData());

                        response["details"] = conInfo.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return TEST_SUCCESS;
                }
                else
                        response["details"] = "AppService creation failed";
        }
        else
                response["details"] = "AppService not registered";

        response["result"] = "FAILURE";
#endif
        return TEST_FAILURE;
}


bool ServiceManagerAgent::SM_AppService_SetConnectionReset(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AppService_setConnectionReset--->Entry\n");

#ifdef HAS_API_APPLICATION
        if(&req["applicationID"]==NULL || &req["connectionID"]==NULL || &req["connectionResetLevel"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="App details not provided";
                return TEST_FAILURE;
        }

        char cmd[100] = {'\0'};
        char cmd_ip[200] = {'\0'};
        char ip[20] = {'\0'};
        FILE* fp;
        QString appId = req["applicationID"].asCString();
        QString conId = req["connectionID"].asCString();
        QString resetLevel = req["connectionResetLevel"].asCString();

        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(ApplicationService::SERVICE_NAME))
        {
                ptrService = ServiceManager::getInstance()->getGlobalService(ApplicationService::SERVICE_NAME);
                if (ptrService != NULL)
                {
                        ServiceParams inParams;
                        ServiceParams outParams;
                        QVariantList inList;

                        inList << appId << conId << resetLevel;
                        inParams["params"] = inList;
                        outParams = ptrService->callMethod("setConnectionReset", inParams);

                        if(outParams["resetSent"].toBool() && outParams["success"].toBool())
                        {
                                sprintf(cmd, "tail -n 100 %s | grep -i \"Disconnect connection\"", OCAP_LOG);
                                /*reset request is handled asynchronously by streamer, hence have to wait for those logs*/
                                for(int i=0; i<10; i++)
                                {
                                        if(!system(cmd))
                                        {
                                                sprintf(cmd_ip, "tail -n 100 %s | grep -i \"Connected to\" | cut -d '(' -f2 |  cut -d ')' -f1 > %s", OCAP_LOG, IP_FILE);
                                                if(!system(cmd_ip))
                                                {
                                                        fp = fopen(IP_FILE, "r");
                                                        if(fp)
                                                        {
                                                                if(fgets(ip, sizeof(ip), fp) != NULL)
                                                                {
                                                                        int j = 0;
                                                                        while(ip[j] != '\n' && ip[j] != '\0')
                                                                                j++;
                                                                        if(ip[j] == '\n')
                                                                                ip[j] = '\0';
                                                                        printf("ip is: %s\n", ip);
                                                                        DEBUG_PRINT(DEBUG_TRACE,"Connection reset succesfully in %d\n",i);
                                                                        response["details"] = ip;
                                                                        printf("ip is: %s\n", ip);
                                                                        response["result"]="SUCCESS";
                                                                        return TEST_SUCCESS;
                                                                }
                                                        }
                                                }
                                                break;
                                        }
                                        sleep(1);
                                }
                                DEBUG_PRINT(DEBUG_TRACE,"Connection reset failed, cmd= %s \n", cmd);
                                response["details"] = "setConnectionReset failed";
                        }
                        else
                                response["details"] = "setConnectionReset failed";
                }
                else
                        response["details"] = "AppService creation failed";
        }
        else
                response["details"] = "AppService not registered";

        response["result"] = "FAILURE";
#endif
        return TEST_FAILURE;
}

/*this function serves as ths post-requisite of recorder-stub, to restore rmfconfig.ini to its actual form*/
bool ServiceManagerAgent::SM_AppService_Restore_rmfconfig(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AppService_Restore_rmfconfig--->Entry\n");

#ifdef HAS_API_APPLICATION
        char cmd[30] = {'\0'};

        sprintf(cmd, "rm %s", CONFIG_FILE);
        if( !system(cmd) )
        {
                response["details"] = "REBOOT";
                response["result"] = "SUCCESS";
                DEBUG_PRINT(DEBUG_TRACE,"rmfconfig removed from opt, cmd = %s\n", cmd);
        }
        else
        {
                response["details"] = "config not in opt";
                response["result"] = "SUCCESS";
                DEBUG_PRINT(DEBUG_TRACE,"rmfconfig not in opt\n");
        }
#endif
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
        ptrAgentObj->UnregisterMethod("TestMgr_SM_UnRegisterForEvents");
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
        ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_FlushCecData");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HdmiCec_CheckCecData");
        /*ApplicationService APIs*/
        ptrAgentObj->UnregisterMethod("TestMgr_SM_AppService_GetAppInfo");
        ptrAgentObj->UnregisterMethod("TestMgr_SM_AppService_SetConnectionReset");
        ptrAgentObj->UnregisterMethod("TestMgr_SM_AppService_Restore_rmfconfig");

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

