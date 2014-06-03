/*
* ============================================================================
* COMCAST CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file and its contents are the intellectual property of Comcast.  It may
* not be used, copied, distributed or otherwise  disclosed in whole or in part
* without the express written permission of Comcast.
* ============================================================================
* Copyright (c) 2013 Comcast. All rights reserved.
* ============================================================================
*/

#include "ServiceManagerAgent.h"

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
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_RegisterService,"TestMgr_SM_RegisterService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_UnRegisterService,"TestMgr_SM_UnRegisterService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DoesServiceExist,"TestMgr_SM_DoesServiceExist");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_GetRegisteredServices,"TestMgr_SM_GetRegisteredServices");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_GetGlobalService,"TestMgr_SM_GetGlobalService");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_EnableMDVR,"TestMgr_SM_HN_EnableMDVR");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_EnableVPOP,"TestMgr_SM_HN_EnableVPOP");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DisplaySetting_SetZoomSettings,"TestMgr_SM_DisplaySetting_SetZoomSettings");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_DisplaySetting_SetCurrentResolution,"TestMgr_SM_DisplaySetting_SetCurrentResolution");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_HN_SetDeviceName,"TestMgr_SM_HN_SetDeviceName");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_SetAPIVersion,"TestMgr_SM_SetAPIVersion");
	ptrAgentObj->RegisterMethod(*this,&ServiceManagerAgent::SM_RegisterForEvents,"TestMgr_SM_RegisterForEvents");

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

bool ServiceManagerAgent::SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterService ---->Entry\n");
       	ServiceStruct hnServiceStruct;
	bool register_service=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	/*Name of the service to be registered with service manager*/
	std::string serviceName=req["service_name"].asCString();
	/*Regsitering HomeNetworking service*/
#if 0
	if(strcmp(serviceName.c_str(),HOME_NETWORKING_SERVICE_NAME.toUtf8().constData())==0)
	{
		ServiceStruct hnServiceStruct;
		hnServiceStruct.createFunction = &createHomeNetworkingService;
		hnServiceStruct.serviceName = HOME_NETWORKING_SERVICE_NAME;
		register_service=ServiceManager::getInstance()->registerService(HOME_NETWORKING_SERVICE_NAME, hnServiceStruct);
		DEBUG_PRINT(DEBUG_LOG,"\nHomeNetworking service registered\n");
	}
#endif
	/*Registering ScreenCapture service*/
	if(strcmp(serviceName.c_str(),ScreenCaptureService::NAME.toUtf8().constData())==0)
	{
		ServiceStruct scrCapServiceStruct;
		scrCapServiceStruct.createFunction = &ScreenCaptureService::create;
		scrCapServiceStruct.serviceName = ScreenCaptureService::NAME;
		register_service=ServiceManager::getInstance()->registerService(ScreenCaptureService::NAME, scrCapServiceStruct);
		DEBUG_PRINT(DEBUG_LOG,"\nScreenCapture service registered\n");
	}
	/*Registering DeviceSettings service*/
	else if(strcmp(serviceName.c_str(),DEVICE_SETTING_SERVICE_NAME.toUtf8().constData())==0)
	{
		ServiceStruct devServiceStruct;
		devServiceStruct.createFunction = &createDeviceSettingService;
		devServiceStruct.serviceName = DEVICE_SETTING_SERVICE_NAME;
		register_service=ServiceManager::getInstance()->registerService(DEVICE_SETTING_SERVICE_NAME, devServiceStruct);
		DEBUG_PRINT(DEBUG_LOG,"\nDeviceSettings service registered\n");
	}
	else
	{
		register_service = 0;
		DEBUG_PRINT(DEBUG_ERROR,"\nUnKnown service\n");
		response["result"]="FAILURE";
	}
	/*Checking the return value*/
	if(register_service==1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nRegister service Success\n");
		response["result"]="SUCCESS";
	}
	else if(register_service==0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nRegister service Failed\n");
		response["result"]="FAILURE";
	}
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
	bool unregister_service=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	/*calling unregisterService API for DeRegistering the service*/
	unregister_service=ServiceManager::getInstance()->unregisterService(QString::fromStdString(serviceName));
	if(unregister_service==1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nUnRegister service Success\n");
		response["result"]="SUCCESS";
	}
	else if(unregister_service==0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nUnRegister service failed\n");
		response["result"]="FAILURE";
	}
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
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	/*Checking the service existence in service manager component*/
	exist=ServiceManager::getInstance()->doesServiceExist(QString::fromStdString(serviceName));
        if(exist==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n service NotExist\n");
		response["result"]="SUCCESS";
		response["details"]="NOT EXIST";
	}
        else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n service Exist\n");
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
	char services[200]="Service:" ;
	char *list_services = (char*)malloc(sizeof(char)*30);
	memset(list_services , '\0', (sizeof(char)*30));
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
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	char services[50]= "Service:";
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
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n SM_GetGlobalService ---->Exit\n");
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
        if(&req["enable"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	int enable=req["enable"].asInt();
	bool enable_flag=false;
	ServiceParams params,resultParams;
	char enableDetail[20]= "Enable:";
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
        if(&req["enable"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	int enable=req["enable"].asInt();
	bool enable_flag=false;
	ServiceParams params,resultParams;
	char enableDetail[20]= "Enable:";
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
        if(&req["videoDisplay"]==NULL || &req["zoomLevel"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	std:: string videoDisplay=req["videoDisplay"].asCString();
	std:: string zoomLevel=req["zoomLevel"].asCString();
	ServiceParams params,resultParams;
	char zoomLevelDetail[200]= "zoomLevel";
	QVariantList list;
	char *zoomDetails = (char*)malloc(sizeof(char)*100);
	memset(zoomDetails , '\0', (sizeof(char)*100));
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
        if(&req["videoDisplay"]==NULL || &req["resolution"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	std:: string videoDisplay=req["videoDisplay"].asCString();
	std:: string resolution=req["resolution"].asCString();
	ServiceParams params,resultParams;
	char curResolutionDetail[200]= "Resolution";
	QVariantList list;
	char *resolutionDetails = (char*)malloc(sizeof(char)*100);
	memset(resolutionDetails , '\0', (sizeof(char)*100));
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
        if(&req["device_name"]==NULL )
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
        std::string deviceName=req["device_name"].asCString();
        ServiceParams params,resultParams;
        char deviceNameDetail[200]= "DeviceName:";
        QVariantList list;
        char *nameDetails = (char*)malloc(sizeof(char)*100);
	memset(nameDetails , '\0', (sizeof(char)*100));
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
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	free(nameDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetDeviceName ---->Exit\n");
	return TEST_SUCCESS;	
}

/***************************************************************************
 *Function name : SM_SetAPIVersion 
 *Descrption    : This will check the functionality of getApiVersionNumber and 
		  setApiVersionNumber APIs.
 *parameter [in]: req-  service_name-Name of the service.
			apiVersion - Parameter to be passed to callMethod API.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_SetAPIVersion ---->Entry\n");
        if(&req["service_name"]==NULL || &req["apiVersion"] == NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	int setApiVersion=req["apiVersion"].asInt();
	ServiceParams params;
	int getApiVersion=0;
	char apiVersion[20]= "API_VERSION:";
	char *versionDetails = (char*)malloc(sizeof(char)*20);
	memset(versionDetails , '\0', (sizeof(char)*20));
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
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	free(versionDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_SetAPIVersion ---->Exit\n");
	return TEST_SUCCESS;	
}


/***************************************************************************
 *Function name : SM_RegisterForEvents
 *Descrption    : This function will check the functionality of registerForEvents
                  and unregisterEvents APIs.
 *parameter [in]: service_name - Name of the service.
		  event_name - event to be registered.
 *****************************************************************************/ 
bool ServiceManagerAgent::SM_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterForEvents ---->Entry\n");
        if(&req["service_name"]==NULL || &req["event_name"]==NULL)
        {
		response["result"]="FAILURE";
                return TEST_FAILURE;
        }
	std::string serviceName=req["service_name"].asCString();
	std::string eventName=req["event_name"].asCString();
	QList<QString> event_list;
	event_list.append(QString::fromStdString(eventName));
	ServiceParams params;
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
		DEBUG_PRINT(DEBUG_ERROR,"\n SM getGlobalService failed\n");
	}
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterForEvents ---->Exit\n");
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

	ptrAgentObj->UnregisterMethod("TestMgr_SM_RegisterService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_UnRegisterService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DoesServiceExist");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_GetRegisteredServices");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_GetGlobalService");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_EnableMDVR");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_EnableVPOP");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DisplaySetting_SetZoomSettings");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_DisplaySetting_SetCurrentResolution");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_HN_SetDeviceName");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_SetAPIVersion");
	ptrAgentObj->UnregisterMethod("TestMgr_SM_RegisterForEvents");
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

