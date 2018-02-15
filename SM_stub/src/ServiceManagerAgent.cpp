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

#include "ServiceManagerAgent.h"

Json::Value convertQHashToJson (QVariant qHash) ;
QVariantHash convertObjectToQList (Json::Value jData);

/******************************************************************************
 *Function name : convertQVariantToJson
 *Description   : Function to check the QVariant data type and convert it to
 *                json value
 *Input         : qData - QVariant data to be converted to json value
 *Return        : Returns the resultant json value
 ******************************************************************************/
Json::Value convertQVariantToJson (QVariant qData) {

	Json::Value jValue;
	DEBUG_PRINT (DEBUG_TRACE, "convertQVariantToJson --->Entry\n");

        if (QVariant::String == qData.type()) {
        	jValue = qData.toString().toStdString();
	}
        else if (QVariant::Int == qData.type()) {
		 jValue = qData.toInt();
        }
        else if (QVariant::Bool == qData.type()) {
		jValue = qData.toBool();
        }
	else if(QVariant::ByteArray == qData.type()) {
		jValue = qData.toByteArray().data();
	}
  	else if(QVariant::Double == qData.type()) {
                jValue = qData.toDouble();
        }
        else if(QMetaType::Float == qData.type()) {
                jValue = qData.toFloat();
        }
	else if(QVariant::LongLong == qData.type()) {
                jValue = qData.toLongLong();
	}
	
	DEBUG_PRINT (DEBUG_TRACE, "convertQVariantToJson --->Exit\n");
	return jValue;
}

/******************************************************************************
 *Function name : convertQListToJson
 *Description   : Function to convert QVariantList elements to corresponding 
 *                Json array
 *Input         : qList - QVariantList to be converted to json array
 *Return        : Returns the resultant json array
 ******************************************************************************/
Json::Value convertQListToJson (QVariantList qList) {

        DEBUG_PRINT (DEBUG_TRACE, "convertQListToJson --->Entry\n");
	Json::Value jArray;
        int itr;
        for (itr = 0;itr < qList.size();itr++) {
                if ((QVariant::Hash == qList[itr].type()) || (QVariant::Map == qList[itr].type())) {
		        jArray[itr] = convertQHashToJson (qList[itr]);
                }
                else if (QVariant::List == qList[itr].type()) {
			jArray[itr] = convertQListToJson (qList[itr].toList());

                }
                else {
			jArray[itr] = convertQVariantToJson (qList[itr]);
                }
		
        }

        DEBUG_PRINT (DEBUG_TRACE, "convertQListToJson --->Exit\n");
	return jArray;
}

/******************************************************************************
 *Function name : convertQHashToJson
 *Description   : Function to check the QVariant data(QHash/QMap) and convert it
 *                to json object
 *Input         : qHash - QVariant data to be converted to json object
 *Return        : Returns the resultant json object
 ******************************************************************************/
Json::Value convertQHashToJson (QVariant qHash) {

	DEBUG_PRINT (DEBUG_TRACE, "convertQHashToJson --->Entry\n");

	Json::Value qObject;
        QVariantHash::const_iterator itr = qHash.toHash().constBegin();
	QVariantHash::const_iterator endItr = qHash.toHash().constEnd();
	if (qHash.type() == QVariant::Map) {
                QVariantMap::const_iterator itr = qHash.toMap().constBegin();
		QVariantMap::const_iterator endItr = qHash.toMap().constEnd();
        }

	for ( ; itr != endItr; itr++) {
		if (QVariant::List == itr.value().type()) {
			qObject[itr.key().toStdString()] = convertQListToJson (itr.value().toList());
		    }
		    else if ((QVariant::Hash == itr.value().type()) || (QVariant::Map == itr.value().type())){
			qObject[itr.key().toStdString()] = convertQHashToJson (itr.value());
		    }
		    else {
			qObject[itr.key().toStdString()] = convertQVariantToJson (itr.value());
		    }
	}

	DEBUG_PRINT (DEBUG_TRACE, "convertQHashToJson --->Exit\n");
	return qObject;
}

/******************************************************************************
 *Function name : convertValueToQVariant
 *Description   : Function to check the Json::Value type and convert it to
 *                QVariant
 *Input         : jData - Json::Value data to be converted to QVariant
 *Return        : Returns the resultant QVariant
 *******************************************************************************/
QVariant convertValueToQVariant (Json::Value jData) {

	DEBUG_PRINT (DEBUG_TRACE, "convertValueToQVariant --->Entry\n");
	QVariant jValue;
	if (jData.isString()) {
		jValue = jData.asCString();
	}
	else if (jData.isBool()) {
		jValue = jData.asBool();
	}
	else if (jData.isInt()) {
		jValue = jData.asInt();
	}
	else if (jData.isUInt()) {
		jValue = jData.asUInt();
	}
	else if (jData.isDouble()) {
		jValue = jData.asDouble();
	}

	DEBUG_PRINT (DEBUG_TRACE, "convertValueToQVariant --->Exit\n");
	return jValue;
        
}

/******************************************************************************
 *Function name : convertArrayToQList
 *Description   : Function to check the Json array elements type and convert it to
 *                QVariantList
 *Input         : jData - Json array to be converted to QVariantList
 *Return        : Returns the resultant QVariantList
 *******************************************************************************/
QVariantList convertArrayToQList (Json::Value jData) {

	DEBUG_PRINT (DEBUG_TRACE, "convertArrayToQList --->Entry\n");
	QVariantList qList;
	int itr;
	for (itr = 0;itr < jData.size();itr++) {
		if (jData[itr].isObject()) {
			qList << convertObjectToQList (jData[itr]);
		}
		else if (jData[itr].isArray()) {
			qList << convertArrayToQList (jData[itr]);
		}
		else {
			qList << convertValueToQVariant (jData[itr]);
		}
	}
	
	DEBUG_PRINT (DEBUG_TRACE, "convertArrayToQList --->Exit\n");
	return qList;
}
/******************************************************************************
 *Function name : convertObjectToQList
 *Description   : Function to check the Json object and convert it to
 *                QVariantList
 *Input         : jData - Json object to be converted to QVariantList
 *Return        : Returns the resultant QVariantHash
 *******************************************************************************/
QVariantHash convertObjectToQList (Json::Value jData) {

	DEBUG_PRINT (DEBUG_TRACE, "convertObjectToQList --->Entry\n");
	QVariantHash qHash;
	string key;
	qHash.clear();
	foreach (key, jData.getMemberNames()) {
		if (jData.get(key, Json::Value()).isString()) {
			qHash.insert(key.c_str(), jData.get(key, Json::Value()).asCString());
		}
		else if (jData.get(key, Json::Value()).isInt()) {
			qHash.insert(key.c_str(), jData.get(key, Json::Value()).asInt());
		}
	 	else if (jData.get(key, Json::Value()).isBool()) {
			qHash.insert(key.c_str(), jData.get(key, Json::Value()).asBool());
		}
		else if (jData.get(key, Json::Value()).isDouble()) {
			qHash.insert(key.c_str(), jData.get(key, Json::Value()).asDouble());
		}
		else if (jData.get(key, Json::Value()).isArray()) {
			qHash.insert(key.c_str(), convertArrayToQList (jData.get(key, Json::Value())));
		}
		else if (jData.get(key, Json::Value()).isObject()) {
			qHash.insert(key.c_str(), convertObjectToQList (jData.get(key, Json::Value())));
		}
		else if (jData.get(key, Json::Value()).isNull()) {
			qHash.insert(key.c_str(), QVariant());
		}
	}
	
	DEBUG_PRINT (DEBUG_TRACE, "convertObjectToQList --->Exit\n");
	return qHash;
}


#ifdef HAS_API_APPLICATION
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

#ifdef HAS_FRONT_PANEL
static FrontPanelService *pFPService = NULL;
 bool startFPService(void)
 {
         bool bReturn = false;
         DEBUG_PRINT(DEBUG_TRACE,"Create new instance of Front Panel Service\n");
         if (ServiceManager::getInstance()->doesServiceExist(FrontPanelService::SERVICE_NAME))
         {
               pFPService = dynamic_cast<FrontPanelService*>(ServiceManager::getInstance()->createService(FrontPanelService::SERVICE_NAME));
               if (pFPService != NULL)
               {
                       DEBUG_PRINT(DEBUG_LOG,"pFPService = %p\n", pFPService);
                       bReturn = true;
               }
               else
               {
                       DEBUG_PRINT(DEBUG_ERROR,"Failed to create instance of Front Panel Service\n");
               }
       }
       else
       {
               DEBUG_PRINT(DEBUG_ERROR,"Front Panel Service does not exist");
       }
       return bReturn;
 }
 #endif

#ifdef HAS_API_HDMI_CEC
std::string rdkLogPath = getenv("RDK_LOG_PATH");
std::string tdkPath = getenv("TDK_PATH");
std::string cecRdkLogFile = "cec_log.txt";
std::string cecTdkLogFile = "cec_tdk.log";
static bool gDebugLogEnabled = false;
static HdmiCecService *pHdmiService = NULL;
static HdmiListener *pHdmiListener = NULL;

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

/***************************************************************************
 *Function name	: HdmiListener 
 *Descrption	: This is a constructor function for HdmiListener class. 
 *****************************************************************************/ 
HdmiListener::HdmiListener()
{
	DEBUG_PRINT(DEBUG_LOG,"HdmiListener Initialized");
}

void HdmiListener::onServiceEvent(const QString& event, ServiceParams params)
{
	DEBUG_PRINT(DEBUG_TRACE, "onServiceEvent Entry");
	if (event == HdmiCecService::EVENT_ON_CEC_ADDRESS_CHANGE)
	{
		DEBUG_PRINT(DEBUG_LOG, "Received \"cecAddressesChanged\" event");
        	QByteArray data;
        	QVariantHash CECAddresses;
        	QVariantHash logicalAddress;

        	CECAddresses = params;
        	logicalAddress = CECAddresses["logicalAddresses"].toHash();
       	 	data = CECAddresses["physicalAddress"].toByteArray();
        	DEBUG_PRINT(DEBUG_LOG, "Physical Address : %x : %x :%x :%x \n", data.at(0),data.at(1),data.at(2),data.at(3));
        	DEBUG_PRINT(DEBUG_LOG, "device type=%s, logical address = %d \n",logicalAddress["deviceType"].toString().toStdString().c_str(),logicalAddress["logicalAddress"].toInt());
    	}
		
}
#endif

/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 *****************************************************************************/ 

bool ServiceManagerAgent::initialize(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE,"ServiceManagerAgent Initialize");
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


void ServiceManagerAgent::SM_RegisterService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterService ---->Skipping the registration as it is handled in Service Manager itself. \n");
        
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_RegisterService ---->Entry\n");
	char stringDetails[STR_DETAILS_50] = {'\0'};
	bool status = false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return;
        }
	/*Name of the service to be registered with service manager*/
	std::string serviceName=req["service_name"].asCString();
	response["result"]="SUCCESS";
        sprintf(stringDetails,"Service registration skipped");
#ifdef HAS_API_HDMI_CEC
        if (QString::fromStdString(serviceName) == HdmiCecService::SERVICE_NAME)
        {
                DEBUG_PRINT(DEBUG_LOG,"\nCreating Hdmicec handle\n");
                status = startHdmiCecService();
                if (true == status)
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nHdmiCec handle Creation Success\n");
                        response["result"]="SUCCESS";
                        sprintf(stringDetails,"HdmiCec handle creation success");
                }
                else
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nHdmiCec handle Creation failed\n");
                        response["result"]="FAILURE";
                        sprintf(stringDetails,"HdmiCec handle creation failed");
                }
        }
#endif
#ifdef HAS_FRONT_PANEL
        if (QString::fromStdString(serviceName) == FrontPanelService::SERVICE_NAME)
        {
                DEBUG_PRINT(DEBUG_LOG,"\nCreating frontpanel handle\n");
                status = startFPService();
                if (true == status)
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nFront panel handle creation Success\n");
                        response["result"]="SUCCESS";
                        sprintf(stringDetails,"Front panel handle creation success");
                }
                else
                {
                        DEBUG_PRINT(DEBUG_LOG,"\nFront panel handle creation failed\n");
                        response["result"]="FAILURE";
                        sprintf(stringDetails,"Front panel handle creation failed");
                }
        }
#endif
        response["details"] = stringDetails;
	return; 
}

/***************************************************************************
 *Function name : SM_UnRegisterService 
 *Descrption    : This function will unregister the given service from the serviceManger component. 
 *parameter [in]: req-  service_name- Name of the service.
 *****************************************************************************/ 

void ServiceManagerAgent::SM_UnRegisterService(IN const Json::Value& req, OUT Json::Value& response)
{
	 DEBUG_PRINT(DEBUG_TRACE,"\nSM_UnRegisterService ---->Skipping the unregistration as it is handled in Service Manager itself. \n");
        /*
        Skipping the service registration due to recent changes (RDKTT-661). If required we will enable later
        */
        std::string serviceName=req["service_name"].asCString();
#ifdef HAS_API_HDMI_CEC
        if (QString::fromStdString(serviceName) == HdmiCecService::SERVICE_NAME)
        {
                stopHdmiCecService();
        }
#endif
        response["result"]="SUCCESS";
        response["details"]="un register skipped";

	return ;
}


/***************************************************************************
 *Function name : SM_DoesServiceExist
 *Descrption    : This will check the existence of the given service in the list of registered services.
 *parameter [in]: req-  service_name-Name of the service.
 *****************************************************************************/ 

void ServiceManagerAgent::SM_DoesServiceExist(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DoesServiceExist ---->Entry\n");
	bool exist=false;
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return; 
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
	return;
}


/***************************************************************************
 *Function name : SM_GetRegisteredServices
 *Descrption    : This will return the list of registered services with the serviceManger component.
 *parameter [in]: NULL
 *****************************************************************************/ 
void ServiceManagerAgent::SM_GetRegisteredServices(IN const Json::Value& req, OUT Json::Value& response)
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
	return;
}


/***************************************************************************
 *Function name : SM_GetGlobalService 
 *Descrption    : This will return the name of the given service.
 *parameter [in]: req-  service_name-Name of the service.
 *****************************************************************************/ 
void ServiceManagerAgent::SM_GetGlobalService(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_GetGlobalService ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return ;
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
	return ;
}

void ServiceManagerAgent::SM_GetSetting(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_GetSetting ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
		response["details"]="service name is NULL";
                return ;
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
        return;
}

void ServiceManagerAgent::SM_CreateService(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_CreateService ---->Entry\n");
        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="service name is NULL";
                return ;
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
        return ;
}

/***************************************************************************
 *Function name : SM_HN_EnableMDVR
 *Descrption    : This function will enable/disable MDVR staus.
 *parameter [in]: req-  enable - Parameter to be passed to callMethod API.
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_EnableMDVR(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableMDVR ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["enable"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="enable value is NULL";
                return;
        }
        int enable=req["enable"].asInt();
        ServiceParams inParams,resultParams;
        QVariantList list;
        Service* ptrService=NULL;

        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        list.append(enable);
                        inParams["params"] = list;

                        /*Enabling MDVR by calling callMethod with METHOD_HN_SET_MDVR_ENABLED*/
                        resultParams = ptrService->callMethod(METHOD_HN_SET_MDVR_ENABLED,inParams);

                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable MDVR success");
                                response["details"] = "Set Enable MDVR success";
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable MDVR failed");
                                response["details"] = "Set Enable MDVR failed";
                                response["result"]="FAILURE";
                        }
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"getGlobalService failed\n");
                        response["details"] = "getGlobalService failed";
                        response["result"] = "FAILURE";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home Networking service does not exist\n");
                response["details"] = "Home Networking service does not exist";
                response["result"] = "FAILURE";
        }

#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="Home Networking Service unsupported";
#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableMDVR ---->Exit\n");
        return ;
}

/***************************************************************************
 *Function name : SM_HN_IsMDVREnabled
 *Descrption    : This function will check if MDVR status is enabled/disabled.
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_IsMDVREnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_IsMDVREnabled ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        /*Checking MDVR by calling callMethod with METHOD_HN_IS_MDVR_ENABLED*/
                        resultParams=ptrService->callMethod(METHOD_HN_IS_MDVR_ENABLED,inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                char enableStatus[STR_DETAILS_20] = {'\0'};
                                DEBUG_PRINT(DEBUG_TRACE,"MDVR enable status retrieved");
                                sprintf(enableStatus,"%d",resultParams["enabled"].toBool());
                                response["details"] = enableStatus;
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve MDVR enable status");
                                response["details"] = "Failed to retrieve MDVR enable status";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home networking service does not exist\n");
                response["details"] = "Home networking service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home networking service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_IsMDVREnabled---->exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HN_EnableVPOP 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_HN_SET_VPOP_ENABLED and METHOD_HN_IS_VPOP_ENABLED method as
		  parameters.
 *parameter [in]: req-  enable - Parameter to be passed to callMethod API
 *****************************************************************************/ 
void ServiceManagerAgent::SM_HN_EnableVPOP(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_EnableVPOP ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["enable"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="enable value is NULL";
                return;
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
		return;
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
	return;
}

/***************************************************************************
 *Function name : SM_HN_IsVPOPEnabled
 *Descrption    : This function will check if VPOP status is enabled/disabled.
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_IsVPOPEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_IsVPOPEnabled ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        resultParams=ptrService->callMethod(METHOD_HN_IS_VPOP_ENABLED,inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                char enableStatus[STR_DETAILS_20] = {'\0'};
                                DEBUG_PRINT(DEBUG_TRACE,"VPOP enable status retrieved");
                                sprintf(enableStatus,"%d",resultParams["enabled"].toBool());
                                response["details"] = enableStatus;
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve VPOP enable status");
                                response["details"] = "Failed to retrieve VPOP enable status";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home networking service does not exist\n");
                response["details"] = "Home networking service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home networking service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_IsVPOPEnabled---->exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HN_SetVidiPathEnabled
 *Descrption    : This function will enable/disable Vidi path
 *parameter [in]: req - enable - value corresponding Vidi path enable/disable
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_SetVidiPathEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_SetVidiPathEnabled---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        QVariantList inList;
        bool valueToSetEnabled = req["enable"].asInt();
        if (ServiceManager::getInstance()->doesServiceExist(HOME_NETWORKING_SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HOME_NETWORKING_SERVICE_NAME));
                if (ptrService != NULL)
                {
                        inList.append(valueToSetEnabled);
                        inParams["params"] = inList;

                        resultParams = ptrService->callMethod(METHOD_HN_SET_VIDI_PATH_ENABLED, inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Vidi Enable success");
                                response["details"] = "Set Vidi Enable success";
                                response["result"]="SUCCESS";
                                return ;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Vidi Enable failed");
                                response["details"] = "Set Vidi Enable failed";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home Networking Service does not exist\n");
                response["details"] = "Home networking Service does not exist";
                response["result"] = "FAILURE";
        }

#else
        DEBUG_PRINT(DEBUG_TRACE,"Home Networking Service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home Networking not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_SetVidiPathEnabled---->Exit\n");
        return ;
}

/***************************************************************************
 *Function name : SM_HN_IsVidiPathEnabled
 *Descrption    : This function will check if VidiPath is enabled/disabled
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_IsVidiPathEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_IsVidiPathEnabled---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(HOME_NETWORKING_SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HOME_NETWORKING_SERVICE_NAME));
                if (ptrService != NULL)
                {
                        resultParams = ptrService->callMethod(METHOD_HN_IS_VIDI_PATH_ENABLED, inParams);
                        bool status = resultParams["success"].toBool();
                        printf("ENABLE STATUS: %d\n", status);
                        if(status)
                        {
                                char enableStatus[STR_DETAILS_20] = {'\0'};
                                DEBUG_PRINT(DEBUG_TRACE,"Vidi path enable status retrieved");
                                sprintf(enableStatus,"%d",resultParams["enabled"].toBool());
                                response["details"] = enableStatus;
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve Vidi path enable data");
                                response["details"] = "Failed to retrieve vidi path enable data";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home networking service does not exist\n");
                response["details"] = "Home networking service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home networking service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_IsVidiPathEnabled---->exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HN_SetUpnpEnabled
 *Descrption    : This function will enable/disable the upnp status.
 *parameter [in]: req-  enable - Parameter to be passed to callMethod API.
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_SetUpnpEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetUpnpEnabled ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["enable"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="enable value is NULL";
                return;
        }
        int enable=req["enable"].asInt();
        ServiceParams inParams,resultParams;
        QVariantList list;
        Service* ptrService=NULL;

        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        list.append(enable);
                        inParams["params"] = list;

                        /*Enabling Upnp by calling callMethod with METHOD_HN_SET_UPNP_ENABLED*/
                        resultParams = ptrService->callMethod(METHOD_HN_SET_UPNP_ENABLED, inParams);

                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable Upnp success");
                                response["details"] = "Set Enable Upnp success";
                                response["result"]="SUCCESS";
                                return ;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable Upnp failed");
                                response["details"] = "Set Enable Upnp failed";
                                response["result"]="FAILURE";
                        }
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"getGlobalService failed\n");
                        response["details"] = "getGlobalService failed";
                        response["result"] = "FAILURE";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home Networking service does not exist\n");
                response["details"] = "Home Networking service does not exist";
                response["result"] = "FAILURE";
        }

#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="Home Networking Service unsupported";
#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetUpnpEnabled ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HN_IsUpnpEnabled
 *Descrption    : This function will check if Upnp status is enabled/disabled.
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_IsUpnpEnabled(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_IsUpnpEnabled ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        /*Checking Upnp by calling callMethod with METHOD_HN_IS_UPNP_ENABLED*/
                        resultParams=ptrService->callMethod(METHOD_HN_IS_UPNP_ENABLED,inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                char enableStatus[STR_DETAILS_20] = {'\0'};
                                DEBUG_PRINT(DEBUG_TRACE,"Upnp enable status retrieved");
                                sprintf(enableStatus,"%d",resultParams["enabled"].toBool());
                                response["details"] = enableStatus;
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve Upnp enable status");
                                response["details"] = "Failed to retrieve Upnp enable status";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home networking service does not exist\n");
                response["details"] = "Home networking service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home networking service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_IsUpnpEnabled---->exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HN_GetDeviceName
 *Descrption    : This function will retrieve the device name
 *****************************************************************************/
void ServiceManagerAgent::SM_HN_GetDeviceName(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_GetDeviceName ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(HomeNetworkingService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(HomeNetworkingService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        resultParams=ptrService->callMethod(METHOD_HN_GET_DEVICE_NAME,inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                char deviceNameDetail[STR_DETAILS_200]= "";
                                sprintf(deviceNameDetail,"%s",resultParams["deviceName"].toString().toUtf8().constData());
                                DEBUG_PRINT(DEBUG_LOG,"%s",deviceNameDetail);
                                response["details"] = deviceNameDetail;
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve device name details");
                                response["details"] = "Failed to retrieve device name details";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Home networking service does not exist\n");
                response["details"] = "Home networking service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Home networking service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Home networking service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HN_GetDeviceName---->exit\n");
        return;
}


/***************************************************************************
 *Function name : SM_DisplaySetting_SetZoomSettings 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_DISPLAY_SETTINGS_SET_ZOOM_SETTING and METHOD_DISPLAY_SETTINGS_GET_ZOOM_SETTING method as
		  parameters.
 *parameter [in]: req- 	videoDisplay - name of the videoDisplay
			zoomLevel - Level for Zoom 
 *****************************************************************************/ 
void ServiceManagerAgent::SM_DisplaySetting_SetZoomSettings(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetZoomSettings ---->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        if(&req["videoDisplay"]==NULL || &req["zoomLevel"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="videoDisplay or zoomLevel is NULL";
                return;
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
	return;
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
void ServiceManagerAgent::SM_DisplaySetting_SetCurrentResolution(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetCurrentResolution ---->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        if(&req["videoDisplay"]==NULL || &req["resolution"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="videoDisplay or resolution is NULL";
                return;
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
	return;
}


/***************************************************************************
 *Function name : SM_DisplaySetting_GetConnectedAudioPorts
 *Descrption    : This function returns the available Audio Output Ports
 *parameter     : none
 *****************************************************************************/
void ServiceManagerAgent::SM_DisplaySetting_GetSupportedAudioPorts(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetSupportedAudioPorts--->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        QVariantList portList;
        Service* ptr_service=NULL;
        ServiceParams inParams, resultParams;
        QString details;

        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
        if(ptr_service != NULL)
        {
                resultParams = ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_SUPPORTED_AUDIO_PORTS, inParams);
                portList = resultParams["supportedAudioPorts"].toList();
                if( !portList.isEmpty() )
                {
                        for(int i=0; i<portList.size(); i++)
                        {
                                details += portList[i].toString();
                                details += " ";
                        }
                        DEBUG_PRINT(DEBUG_TRACE,"Supported Ports are: %s \nlist size is: %d",details.toUtf8().constData(), portList.size());
                        response["details"] = details.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return ;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"No Supported Ports\n");
                        response["result"]="FAILURE";
                        response["details"]="Empty connected port list";
                }
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
        }
#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetSupportedAudioPorts--->Exit\n");
        return;
}


/***************************************************************************
 *Function name : SM_DisplaySetting_GetConnectedAudioPorts
 *Descrption    : This function will returns the Audio Output Ports that is connected at the moment
                  METHOD_DISPLAY_SETTINGS_GET_CONNECTED_AUDIO_PORTSd 
                  parameters.
 *parameter [in]: req-  videoDisplay - name of the videoDisplay
                        resolution - video resolution 
 *****************************************************************************/
void ServiceManagerAgent::SM_DisplaySetting_GetConnectedAudioPorts(IN const Json::Value& req, OUT Json::Value& response)
{

        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetConnectedAudioPorts--->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        QVariantList portList;
        Service* ptr_service=NULL;
        ServiceParams inParams, resultParams;
        QString details, audMode;

        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
        if(ptr_service != NULL)
        {
                resultParams = ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_CONNECTED_AUDIO_PORTS, inParams);
                portList = resultParams["connectedAudioPorts"].toList();

                if( !portList.isEmpty() )
                {
                        for(int i=0; i<portList.size(); i++)
                        {
                                details += portList[i].toString();
                                details += " ";
                        }
                        DEBUG_PRINT(DEBUG_TRACE,"Connected Ports are: %s \nlist size is: %d",details.toUtf8().constData(), portList.size());
                        response["details"] = details.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return;
                }
                else
                        DEBUG_PRINT(DEBUG_TRACE,"No Connected Ports\n");
                        response["result"]="FAILURE";
                        response["details"]="Empty connected port list";
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
        }

#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetConnectedAudioPorts--->Exit\n");
        return;
}


/***************************************************************************
 *Function name : SM_DisplaySetting_GeSoundMode
 *Descrption    : This function will return the audio output mode of the given port.
                  METHOD_DISPLAY_SETTINGS_GET_SOUND_MODE 
 *parameter [in]: req-  audioport - name of the audioport
 *****************************************************************************/
void ServiceManagerAgent::SM_DisplaySetting_GetSoundMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetSoundMode--->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        QVariantList inList;
        Service* ptr_service=NULL;
        ServiceParams inParams, resultParams;
        QString details, audMode;

        std::string portName = req["portName"].asCString();
        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
        if(ptr_service != NULL)
        {
                ptr_service->setApiVersionNumber(5);

                inList.append(QString::fromStdString(portName));
                inParams["params"] = inList;
                resultParams = ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_SOUND_MODE, inParams);
                audMode = resultParams["soundMode"].toString();

                DEBUG_PRINT(DEBUG_TRACE,"for audio port %s audio mode is %s",portName.c_str(), audMode.toUtf8().constData());
                if(!audMode.isEmpty())
                {
                        response["details"] = audMode.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return;
                }
                else
                {
                        response["details"] = "Audio mode returned as empty";
                        response["result"]="FAILURE";
                }
        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
        }

#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetSoundMode ---->Exit\n");
        return;
}


/*******************************************************************************************
 *Function name : SM_DisplaySetting_SetSoundMode
 *Descrption    : This function will set the given audio mode on the given port.
                  METHOD_DISPLAY_SETTINGS_SET_SOUND_MODE 
 *parameter [in]: req-  audioport - name of the audioport audiomode - the mode to be set
 *******************************************************************************************/
void ServiceManagerAgent::SM_DisplaySetting_SetSoundMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetSoundMode--->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        QVariantList inList;
        Service* ptr_service=NULL;
        ServiceParams inParams, resultParams;
        QString details, audMode;
        bool result;

        std::string portName = req["portName"].asCString();
        std::string setMode = req["audioMode"].asCString();
        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
        if(ptr_service != NULL)
        {
                ptr_service->setApiVersionNumber(5);

                inList.append(QString::fromStdString(portName));
                inList.append(QString::fromStdString(setMode));
                inParams["params"] = inList;
                resultParams = ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_SET_SOUND_MODE, inParams);
                result = resultParams["success"].toBool();

                if(result)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"AudioMode set successfully");
                        response["details"] = "Audio mode set suuccessfully";
                        response["result"]="SUCCESS";
                        return;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"setAudioMode failed");
                        response["details"] = "setAudioMode failed";
                        response["result"]="FAILURE";
                }

        }
        else
        {
                response["result"]="FAILURE";
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
        }

#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_SetSoundMode ---->Exit\n");
        return ;
}


void ServiceManagerAgent::SM_DisplaySetting_GetSupportedAudioModes(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GGetSupportedAudioModes-->Entry\n");

#ifdef USE_DISPLAY_SETTINGS
        QVariantList inList, supportedAudMode;
        Service* ptr_service=NULL;
        ServiceParams inParams, resultParams;
        QString details ;

        std::string portName = req["portName"].asCString();
        /*Calling getGlobalService API to get the service instance*/
        ptr_service = ServiceManager::getInstance()->getGlobalService(DISPLAY_SETTINGS_SERVICE_NAME);
        if(ptr_service != NULL)
        {
                inList.append(QString::fromStdString(portName));
                inParams["params"] = inList;
                ptr_service->setApiVersionNumber(5);
                resultParams = ptr_service->callMethod(METHOD_DISPLAY_SETTINGS_GET_SUPPORTED_AUDIO_MODES, inParams);
                supportedAudMode = resultParams["supportedAudioModes"].toList();
                if( !supportedAudMode.isEmpty())
                {
                        for(int i=0; i<supportedAudMode.size(); i++)
                        {
                                details += supportedAudMode[i].toString();
                                details += " ";
                        }

                        DEBUG_PRINT(DEBUG_TRACE,"for audio port %s audio mode is %s",portName.c_str(), details.toUtf8().constData());
                        response["details"] = details.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"RETURNED EMPTY LIST\n");
                        response["details"] = "supportedAudioModes list empty";
                }
        }
        else
        {
                response["details"]="SM getGlobalService failed";
                DEBUG_PRINT(DEBUG_ERROR,"\nSM getGlobalService failed\n");
        }
        response["result"]="FAILURE";

#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_DisplaySetting_GetSoundMode ---->Exit\n");
        return ;
}


/***************************************************************************
 *Function name : SM_HN_SetDeviceName 
 *Descrption    : This function will check the functionality of callMethod API with 
		  METHOD_HN_SET_DEVICE_NAME and METHOD_HN_GET_DEVICE_NAME method as
		  parameters.
 *parameter [in]: device_name - name of the device.
 *****************************************************************************/ 
void ServiceManagerAgent::SM_HN_SetDeviceName(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_HN_SetDeviceName ---->Entry\n");

#ifdef HAS_API_HOME_NETWORKING
        if(&req["device_name"]==NULL )
        {
		response["result"]="FAILURE";
		response["details"]="device_name is NULL";
                return;
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
	return ;
}

void ServiceManagerAgent::SM_Services_GetName(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_GetName ---->Entry\n");

        if(&req["service_name"]==NULL)
        {
                response["result"]="FAILURE";
		response["details"]="service_name is NULL";
                return ;
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
	return;
}

/***************************************************************************
 *Function name : SM_Services_SetAPIVersion
 *Descrption    : This will check the functionality of getApiVersionNumber and 
		  setApiVersionNumber APIs.
 *parameter [in]: req-  service_name-Name of the service.
			apiVersion - Parameter to be passed to callMethod API.
 *****************************************************************************/ 
void ServiceManagerAgent::SM_Services_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_SetAPIVersion ---->Entry\n");
        if(&req["service_name"]==NULL || &req["apiVersion"] == NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service_name or apiVersion is NULL";
                return ;
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
			return ;
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
	return ;
}


/***************************************************************************
 *Function name : SM_Services_RegisterForEvents
 *Descrption    : This function will check the functionality of registerForEvents
                  and unregisterEvents APIs.
 *parameter [in]: service_name - Name of the service.
		  event_name - event to be registered.
 *****************************************************************************/ 
void ServiceManagerAgent::SM_Services_RegisterForEvents(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_RegisterForEvents ---->Entry\n");
        if(&req["service_name"]==NULL || &req["event_name"]==NULL)
        {
		response["result"]="FAILURE";
		response["details"]="service_name or event_name is NULL";
                return;
        }
	std::string serviceName=req["service_name"].asCString();
	std::string eventName=req["event_name"].asCString();
	QList<QString> event_list;
	event_list.append(QString::fromStdString(eventName));
	//ServiceParams params;
	ServiceListener *listener=NULL;
	Service* ptr_service=NULL;
	bool register_flag=false;
#ifdef HAS_API_HDMI_CEC
        if (QString::fromUtf8(serviceName.c_str()) == HdmiCecService::SERVICE_NAME)
        {
		ptr_service = pHdmiService;
		pHdmiListener = new HdmiListener();
		listener = pHdmiListener;
        }
	else
	{
		/*Calling getGlobalService API to get the service instance*/
		ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	}
#else
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
#endif
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
	return;
}



/***************************************************************************
 *Function name : SM_Services_UnRegisterForEvents
 *Descrption    : This function will check the functionality of unregisterEvents APIs.
 *parameter [in]: service_name - Name of the service.
                  event_name - event to be registered.
 *****************************************************************************/
void ServiceManagerAgent::SM_Services_UnRegisterForEvents(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_UnRegisterForEvents ---->Entry\n");
        if(&req["service_name"]==NULL || &req["event_name"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="service_name or event_name is NULL";
                return;
        }
        std::string serviceName=req["service_name"].asCString();
        std::string eventName=req["event_name"].asCString();
        QList<QString> event_list;
        event_list.append(QString::fromStdString(eventName));
        //ServiceParams params;
        ServiceListener *listener=NULL;
	Service* ptr_service=NULL;
        bool unregister_flag=false;
#ifdef HAS_API_HDMI_CEC
        if (QString::fromUtf8(serviceName.c_str()) == HdmiCecService::SERVICE_NAME)
        {
		ptr_service = pHdmiService;
		listener = pHdmiListener;
        }
	else
	{
		/*Calling getGlobalService API to get the service instance*/
		ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
	}
#else
	ptr_service = ServiceManager::getInstance()->getGlobalService(QString::fromStdString(serviceName));
#endif
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
#ifdef HAS_API_HDMI_CEC
	if(pHdmiListener != NULL)
	{
		delete pHdmiListener;
		pHdmiListener = NULL;
                DEBUG_PRINT(DEBUG_LOG,"Delete %p\n", pHdmiListener);
	}
#endif
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_UnRegisterForEvents ---->Exit\n");
        return;
}


/***************************************************************************
 *Function name : SM_DeviceSetting_GetDeviceInfo
 *Descrption    : This function will check the functionality of GetDeviceInfo
                  of DeviceSettingService.
 *parameter [in]: methodType - Supported device parameter.
 *****************************************************************************/
void ServiceManagerAgent::SM_DeviceSetting_GetDeviceInfo(IN const Json::Value& req, OUT Json::Value& response)
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
                method_list << "ecm_ip" << "boxIP" << "estb_ip" << "macAddress" << "estb_mac" << "ecm_mac" << "ethernet_mac" << "MODEL_NUM" << "imageVersion" << "BUILD_TYPE" << "DAC_INIT_TIMESTAMP" << "downloadIP" ;
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
                        details+=QString::fromUtf8(stringDetails);
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
                return ;
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
        return ;
}


/***************************************************************************
 *Function name : SM_ScreenCapture_Upload
 *Descrption    : This function will check the functionality of Upload url call method
                  of ScreenCaptureService.
 *parameter [in]: URL of web page.
 *****************************************************************************/
void ServiceManagerAgent::SM_ScreenCapture_Upload(IN const Json::Value& req, OUT Json::Value& response)
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
	return ;
}

/***************************************************************************
 *Function name : SM_WebSocket_GetUrl
 *Descrption    : This function will check the functionality of GetUrl
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/                
void ServiceManagerAgent::SM_WebSocket_GetUrl(IN const Json::Value& req, OUT Json::Value& response)
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
		
	return;
}
              
/***************************************************************************
 *Function name : SM_WebSocket_GetReadyState
 *Descrption    : This function will check the functionality of GetReadyState
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/
void ServiceManagerAgent::SM_WebSocket_GetReadyState(IN const Json::Value& req, OUT Json::Value& response)
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

	return ;
}
         
/***************************************************************************
 *Function name : SM_WebSocket_GetBufferedAmount
 *Descrption    : This function will check the functionality of GetBufferedAmount
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/       
void ServiceManagerAgent::SM_WebSocket_GetBufferedAmount(IN const Json::Value& req, OUT Json::Value& response)
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

	return ;
}

/***************************************************************************
 *Function name : SM_WebSocket_GetProtocol
 *Descrption    : This function will check the functionality of GetProtocol
                  of WebSocketService.
 *parameter [in]: NONE
 *****************************************************************************/
void ServiceManagerAgent::SM_WebSocket_GetProtocol(IN const Json::Value& req, OUT Json::Value& response)
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

	return ;
}

/***************************************************************************
 *Function name : SM_HdmiCec_ClearCecLog
 *Descrption    : This will ClearCecLog and new log entry be done.
 *parameter [in]: NONE.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_ClearCecLog(IN const Json::Value& req, OUT Json::Value& response)
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
	return ;
}

/***************************************************************************
 *Function name : SM_HdmiCec_CheckStatus
 *Descrption    : This will search for the pattern in the cec log.
 *parameter [in]: pattern - string.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_CheckStatus(IN const Json::Value& req, OUT Json::Value& response)
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
			if( getline(cecTDKLogIn,lineMatching))
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
	return ;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SetEnabled
 *Descrption    : This will enable the Cec service.
 *parameter [in]: req - set true or false.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_SetEnabled(IN const Json::Value& req, OUT Json::Value& response)
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
	return;
}


/***************************************************************************
 *Function name : SM_HdmiCec_GetEnabled
 *Descrption    : This will get current state (whether it is enabled or disabled) of Cec service.
 *parameter [in]: NONE.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_GetEnabled(IN const Json::Value& req, OUT Json::Value& response)
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
	return;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SetName
 *Descrption    : This will sets the name of the STB device..
 *parameter [in]: req - name to be set to STB device as string.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_SetName(IN const Json::Value& req, OUT Json::Value& response)
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
        return;
}

/***************************************************************************
 *Function name : SM_HdmiCec_GetName
 *Descrption    : This will get current STB device name.
 *parameter [in]: NONE.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_GetName(IN const Json::Value& req, OUT Json::Value& response)
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
        return;
}

/***************************************************************************
 *Function name : SM_HdmiCec_GetConnectedDevices
 *Descrption    : This will get the number of devices connected to STB.
 *parameter [in]: NONE.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response)
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
        return;
}

/***************************************************************************
 *Function name : SM_HdmiCec_SendMessage
 *Descrption    : This will send the message to connected STB.
 *parameter [in]: req - message.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_SendMessage(IN const Json::Value& req, OUT Json::Value& response)
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
                        if (messageToSend.length() == 5)
                        {
                            const int msgLength = 2;
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
        return ;
}

/***************************************************************************
 *Function name : SM_HdmiCec_GetCECAddresses
 *Descrption    : This will get the logical and physical addresses of connected devices 
 *parameter [in]: NONE.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_GetCECAddresses(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetCECAddresses ---->Entry\n");

#ifdef HAS_API_HDMI_CEC
	HdmiCecService *ptr_service = pHdmiService;
        if(ptr_service != NULL)
        {	
		char physAddr[STR_DETAILS_20] = {'\0'};
                QVariantHash CECAddresses;
		QByteArray  physicalAddr;
		QVariantHash logicalAddr;
		QString addr = "{" ;	
		CECAddresses = ptr_service->getCECAddresses();
		physicalAddr = CECAddresses["physicalAddress"].toByteArray();
		logicalAddr = CECAddresses["logicalAddress"].toHash();
		sprintf(physAddr,"%x%x%x%x", physicalAddr.at(0), physicalAddr.at(1), physicalAddr.at(2), physicalAddr.at(3));
		addr += "\"physicalAddress\":\"";
		addr +=  physAddr;
		addr += "\",";
		addr += "\"logicalAddress\":\"" + logicalAddr["logicalAddress"].toString() + "\",";
		addr += "\"deviceType\":\"" + logicalAddr["deviceType"].toString() + "\"";
		addr += "}";
		DEBUG_PRINT(DEBUG_TRACE,"CECAddress details: %s\n", addr.toUtf8().constData());
                response["result"]="SUCCESS";
                response["details"]=addr.toUtf8().constData();
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

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_GetCECAddresses ---->Exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_HdmiCec_OnMessage
 *Descrption    : This will be fired when a message is sent from an HDMI device to STB.
 *parameter [in]: req - message.
 *****************************************************************************/
void ServiceManagerAgent::SM_HdmiCec_OnMessage(IN const Json::Value& req, OUT Json::Value& response)
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
        return ;
}

void ServiceManagerAgent::SM_HdmiCec_FlushCecData(IN const Json::Value& req, OUT Json::Value& response)
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
        return ;
}

void ServiceManagerAgent::SM_HdmiCec_CheckCecData(IN const Json::Value& req, OUT Json::Value& response)
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
                if(strstr(output, "NOFILE") != NULL)
                {
                        response["result"]="FAILURE";
                        response["details"]="CEC Persistent Data Not Found";
                }
                else
                {
                        response["result"]="SUCCESS";
                        response["details"]=output;
                }
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"HdmiCec Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="HdmiCec Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_HdmiCec_CheckCecData ---->Exit\n");
        return ;
}

void ServiceManagerAgent::SM_AppService_GetAppInfo(IN const Json::Value& req, OUT Json::Value& response)
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
                                return ;
                        }
                        conInfo = listToString(conInfoList);
                        DEBUG_PRINT(DEBUG_TRACE,"APPINFO: \n %s \n",conInfo.toUtf8().constData());

                        response["details"] = conInfo.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return ;
                }
                else
                        response["details"] = "AppService creation failed";
        }
        else
                response["details"] = "AppService not registered";

        response["result"] = "FAILURE";
#endif
        return;
}


void ServiceManagerAgent::SM_AppService_SetConnectionReset(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AppService_setConnectionReset--->Entry\n");

#ifdef HAS_API_APPLICATION

        IARM_Bus_Init(IARM_BUS_TDK_NAME);
        IARM_Bus_Connect();

        if(&req["applicationID"]==NULL || &req["connectionID"]==NULL || &req["connectionResetLevel"]==NULL)
        {
                response["result"]="FAILURE";
                response["details"]="App details not provided";
                return ;
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
								        IARM_Bus_Disconnect();
								        IARM_Bus_Term();
                                                                        return;
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

        IARM_Bus_Disconnect();
        IARM_Bus_Term();
#endif
        return ;
}

/*this function serves as ths post-requisite of recorder-stub, to restore rmfconfig.ini to its actual form*/
void ServiceManagerAgent::SM_AppService_Restore_rmfconfig(IN const Json::Value& req, OUT Json::Value& response)
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
        return;
}

void ServiceManagerAgent::SM_AVInputService_GetNumberOfInputs(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_GetNumberOfInputs---->Entry\n");

#ifdef HAS_API_AVINPUT
        DEBUG_PRINT(DEBUG_TRACE,"After HAS_API_AVINPUT\n");
        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(AVInputService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(AVInputService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        ServiceParams params;
                        QString inputCount;

                        ServiceParams result  = ptrService->callMethod("numberOfInputs", params);
                        inputCount = result["numberOfInputs"].toString();
                        DEBUG_PRINT(DEBUG_TRACE,"AVInputs: \n %s \n",inputCount.toUtf8().constData());

                        response["details"] = inputCount.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return ;
                }

        }
        else
                response["details"] = "AVInput Service does not exist";
        response["result"] = "FAILURE";
#else
        DEBUG_PRINT(DEBUG_TRACE,"AVInput Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="AVInput Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_GetNumberOfInputs---->Exit\n");
        return;
}

void ServiceManagerAgent::SM_AVInputService_GetCurrentVideoMode(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_GetCurrentVideoMode---->Entry\n");

#ifdef HAS_API_AVINPUT
        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(AVInputService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(AVInputService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        ServiceParams params;
                        QString videoMode;

                        ServiceParams result  = ptrService->callMethod("currentVideoMode", params);
                        videoMode = result["currentVideoMode"].toString();
                        DEBUG_PRINT(DEBUG_TRACE,"AVInputs: \n %s \n",videoMode.toUtf8().constData());

                        response["details"] = videoMode.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return;
                }

        }
        else
                response["details"] = "AVInput Service does not exist";
        response["result"] = "FAILURE";
#else
        DEBUG_PRINT(DEBUG_TRACE,"AVInput Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="AVInput Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_GetCurrentVideoMode---->Exit\n");
        return ;
}


void ServiceManagerAgent::SM_AVInputService_IsContentProtected(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_IsContentProtected---->Entry\n");

#ifdef HAS_API_AVINPUT
        Service* ptrService = NULL;
        if (ServiceManager::getInstance()->doesServiceExist(AVInputService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(AVInputService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        ServiceParams params;
                        QString contentProtected;

                        ServiceParams result  = ptrService->callMethod("contentProtected", params);
                        contentProtected = result["isContentProtected"].toString();
                        DEBUG_PRINT(DEBUG_TRACE,"Content protected: \n %s \n",contentProtected.toUtf8().constData());

                        response["details"] = contentProtected.toUtf8().constData();
                        response["result"]="SUCCESS";
                        return;
                }

        }
        else
                response["details"] = "AVInput Service does not exist";
        response["result"] = "FAILURE";
#else
        DEBUG_PRINT(DEBUG_TRACE,"AVInput Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="AVInput Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_AVInputService_IsContentProtected---->Exit\n");
        return ;
}


/***************************************************************************
 *Function name : SM_VideoApplicationEventsService_SetEnable 
 *Descrption    : This function will enable/disable Video Application Events
 *parameter [in]: req - valueToSetEnabled - value corresponding event enable/disable
 *****************************************************************************/
void ServiceManagerAgent::SM_VideoApplicationEventsService_SetEnable(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_SetEnable---->Entry\n");

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        QVariantList inList;
        bool valueToSetEnabled = req["valueToSetEnabled"].asInt();
        if (ServiceManager::getInstance()->doesServiceExist(VideoApplicationEventsService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(VideoApplicationEventsService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        inList.append(valueToSetEnabled);
                        inParams["params"] = inList;

                        resultParams = ptrService->callMethod("setEnabled", inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable event success");
                                response["details"] = "Set Enable event success";
                                response["result"]="SUCCESS";
                                return ;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Set Enable event failed");
                                response["details"] = "Set Enable event failed";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
        	DEBUG_PRINT(DEBUG_TRACE,"Video Application Events Service does not exist\n");
                response["details"] = "Video Application Events Service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Video Application Events Service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Video Application Events Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_SetEnable---->Exit\n");
        return ;
}


/***************************************************************************
 *Function name : SM_VideoApplicationEventsService_IsEnableEvent
 *Descrption    : This function will check if Video Application Events are enabled or not
 *****************************************************************************/
void ServiceManagerAgent::SM_VideoApplicationEventsService_IsEnableEvent(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_IsEnableEvent---->Entry\n");

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        if (ServiceManager::getInstance()->doesServiceExist(VideoApplicationEventsService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(VideoApplicationEventsService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        resultParams = ptrService->callMethod("isEnabled", inParams);
                        bool status = resultParams["success"].toBool();
			printf("ENABLE STATUS: %d\n", status);
                        if(status)
                        {
				char enableStatus[STR_DETAILS_20] = {'\0'};
                                DEBUG_PRINT(DEBUG_TRACE,"Event enable data retrieved");
                                sprintf(enableStatus,"%d",resultParams["enabled"].toBool());
                                response["details"] = enableStatus;
                                response["result"]="SUCCESS";
                                return ;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Failed to retrieve event enable data");
                                response["details"] = "Failed to retrieve event enable data";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
        	DEBUG_PRINT(DEBUG_TRACE,"Video application events service does not exist\n");
                response["details"] = "Video application events service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Video application events service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Video application events service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_IsEnableEvent---->exit\n");
        return;
}


/***************************************************************************
 *Function name : SM_VideoApplicationEventsService_SetApplications
 *Description    : This function will set the Application Filter
 *parameter [in]: req - appString - String corresponding to the application filter
 *parameter [in]: req - count - Filter count
 *****************************************************************************/
void ServiceManagerAgent::SM_VideoApplicationEventsService_SetApplications(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_SetApplications---->entry\n");

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        QVariantList inList, appList;
        QHash<QString,QVariant> appDetails;

        std::string appString = req["appString"].asCString();
        int count  = req["count"].asInt();
        char str[500] = {'\0'};
        strcpy(str, appString.c_str());
        printf("appString to cstring %s\n", str);
        char * token = NULL;
        char * paramList[30] = {NULL};
        int i = 0, j=0;
        token = strtok(str, ",");
        while (token)
        {
                paramList[i] = token;
                printf("TOKEN:%d -> %s\n",i, paramList[i]);
                i++;
                token = strtok(NULL, ",");
        }
        int length = i;
        printf("length: %d\n",length);
        printf("count: %d\n",count);
        if (length == count*3)
        {
                while (count > 0)
                {
                        appDetails["applicationName"] = paramList[j++];
                        appDetails["maxRandomDelay"] = paramList[j++];
                        appDetails["filters"] = paramList[j++];
                        printf("Parameters set\n");
                        count--;
                       appList << appDetails;
                }
        }
        else
        {
                printf("Parameter parsing failed\n");
                DEBUG_PRINT(DEBUG_TRACE,"Application set failed");
                response["details"] = "Application set failed";
                response["result"]="FAILURE";
                return ;
        }
        DEBUG_PRINT(DEBUG_TRACE,"Video application events service supported\n");
        response["result"] = "SUCCESS";
        response["details"] = "Video application events service supported";

        if (ServiceManager::getInstance()->doesServiceExist(VideoApplicationEventsService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(VideoApplicationEventsService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        inList.insert(0, appList);
                        inParams["params"] = inList;

                        resultParams = ptrService->callMethod("setApplications", inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Applications set successfully");
                                response["details"] = "Applications set successfully";
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Application set failed");
                                response["details"] = "Application set failed";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Video application events service does not exist\n");
                response["details"] = "Video application events service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Video application events service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Video application events service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_SetApplications-------->exit\n");
        return;
}

/***************************************************************************
 *Function name : SM_VideoApplicationEventsService_GetApplications
 *Descrption    : This function retrieves the Application Filter
 *****************************************************************************/
void ServiceManagerAgent::SM_VideoApplicationEventsService_GetApplications(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_GetApplications---->entry\n");

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        Service* ptrService = NULL;
        ServiceParams inParams, resultParams;
        QVariantList inList, appList;

        if (ServiceManager::getInstance()->doesServiceExist(VideoApplicationEventsService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(VideoApplicationEventsService::SERVICE_NAME));
                if (ptrService != NULL)
                {
                        resultParams = ptrService->callMethod("getApplications", inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"applications retrieved successfully\n");
                                char appData[STR_DETAILS_200] = {'\0'};
                                QVariantList appArray;
                                QHash<QString,QVariant> appDetails;
                                QString appString;

                                appArray = resultParams["applications"].toList();
                                int  k = 0 ;
                                if(0 != appArray.size())
                                {       appString = "";
                                        for(k = 0; k < appArray.size(); k++)
                                        {
                                                appDetails = appArray.at(k).toHash();
                                                sprintf(appData,"%s,%d,%s", appDetails["applicationName"].toString().toStdString().c_str(), appDetails["maxRandomDelay"].toInt(), appDetails["filters"].toString().toStdString().c_str());
                                                printf("%s,%d,%s", appDetails["applicationName"].toString().toStdString().c_str(), appDetails["maxRandomDelay"].toInt(), appDetails["filters"].toString().toStdString().c_str());
                                                appString += appData;
                                                appString += ",";
                                        }
                                }

                                response["details"] = appString.toUtf8().constData();
                                response["result"]="SUCCESS";
                                return;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Application get failed");
                                response["details"] = "Application get failed";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Video application events service does not exist\n");
                response["details"] = "Video application events service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Video application events service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Video application events service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_VideoApplicationEventsService_GetApplications---->exit\n");
        return ;
}

/***************************************************************************
 *Function name : SM_DDS_GetConfiguration
 *Descrption    : This function will get the configuration values for the TR-181 objects
 *parameter [in]: req - names -List of objects whose configuration values to be retrieved
 *****************************************************************************/
void ServiceManagerAgent::SM_DDS_GetConfiguration(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_DDS_GetConfiguration---->Entry\n");

#ifdef HAS_API_DEVICEDIAGNOSTICS
        Service* ptrService = NULL;
        QVariantList nameList;
        std::string names = req["names"].asCString();
        char str[500] = {'\0'};
        strcpy(str, names.c_str());
        char * token = NULL;
        token = strtok(str, ",");
        while (token)
        {
                printf("TOKEN IS:%s\n",token);
                nameList << token;
                token = strtok(NULL, ",");
        }
        if (ServiceManager::getInstance()->doesServiceExist(DeviceDiagnosticsService::SERVICE_NAME))
        {
                ptrService = (ServiceManager::getInstance()->getGlobalService(DeviceDiagnosticsService::SERVICE_NAME));
                if (ptrService != NULL)
                {
			QVariantList inList, deviceDiagnosticsResult;
        		ServiceParams inParams, resultParams;
			QString deviceDiagnosticsinfo;
                        
			inList.insert(0,nameList);
                        inParams["params"] = inList;

                        resultParams = ptrService->callMethod("getConfiguration", inParams);
                        bool status = resultParams["success"].toBool();
                        if(status)
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Get configuration success");
				deviceDiagnosticsResult = resultParams["parameters"].toList();
				deviceDiagnosticsinfo = listToString(deviceDiagnosticsResult);
				DEBUG_PRINT(DEBUG_TRACE,"Device Diagnostics Info: \n %s \n",deviceDiagnosticsinfo.toUtf8().constData());
                        	response["details"] = deviceDiagnosticsinfo.toUtf8().constData();
                                response["result"]="SUCCESS";
                                return ;
                        }
                        else
                        {
                                DEBUG_PRINT(DEBUG_TRACE,"Get configuration failed");
                                response["details"] = "Get configuration failed";
                                response["result"]="FAILURE";
                        }
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Device Diagnostic Service does not exist\n");
                response["details"] = "Device Diagnostic Service does not exist";
                response["result"] = "FAILURE";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"Device Diagnostic Service not supported\n");
        response["result"] = "FAILURE";
        response["details"] = "Device Diagnostic Service not supported";
#endif

        DEBUG_PRINT(DEBUG_TRACE,"SM_DDS_GetConfiguration---->Exit\n");
        return;
}



/***************************************************************************
 *Function name : SM_RunSMEvent_QtApp
 *Descrption    : This function will execute the QT application SMEventApp to test a given event's propagation
 *parameter [in]: req - service_name - name of SM service whose event is to be tested
			event_name   - event name to be tested
			event_param  - parameter to be passed to the event
 *****************************************************************************/
void ServiceManagerAgent::SM_RunSMEvent_QtApp(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_RunSMEvent_QtApp--->Entry\n");

        std::string service_name = req["service_name"].asCString();
        std::string event_name = req["event_name"].asCString();
        int event_param = req["event_param"].asInt();
        char cmnd[100] = {'\0'};
        sprintf(cmnd, "%s %s %s %d", QT_APP, service_name.c_str(), event_name.c_str(), event_param);

        DEBUG_PRINT(DEBUG_TRACE, "cmnd recieved is %s", cmnd);

        if (~(service_name.empty() || event_name.empty()))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Received non-empty params\n");
                if(!system(cmnd))
                {
                        response["details"] = "QAPP started";
                        response["result"] = "SUCCESS";
                        DEBUG_PRINT(DEBUG_TRACE, "QApp started\n");
                        return ;
                }
        }

        response["details"] = "QAPP execution failed";
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_TRACE, "QApp returned error \n");
        return;
}
/***************************************************************************
 *Function name : SM_FP_SetBrightness
 *Descrption    : This will sets the brightness of the front panel LED..
 *parameter [in]: req - name of the LED and Brightness value to be set.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_SetBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_SetBrightness ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                QString LEDName = QString::fromStdString(req["LEDName"].asCString());
                int LEDBrightness = req["LEDBrightness"].asInt();
                ServiceParams params, resultParams;
                QVariantList list;
                bool ReturnValue ;
                DEBUG_PRINT(DEBUG_TRACE,"Calling setBrightness to LED : %s to brightness : %d\n",LEDName.toUtf8().constData(),LEDBrightness);
                list.append(LEDName);
                list.append(LEDBrightness);
                params["params"]=list;
                resultParams = ptr_service->callMethod("setBrightness", params);
                ReturnValue = resultParams["success"].toBool();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setBrightness() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="Front Panel Service setBrightness success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setBrightness() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service setBrightness call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}

/***************************************************************************
 *Function name : SM_FP_GetBrightness
 *Descrption    : This will gets the brightness of the front panel LED..
 *parameter [in]: req - name of the LED .
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_GetBrightness(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_GetBrightness ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                QString LEDName = QString::fromStdString(req["LEDName"].asCString());
                ServiceParams params, resultParams;
                QVariantList list;
                bool ReturnValue ;
                int LEDBrightness;
                char *brightnessDetails = (char*)malloc(sizeof(char)*5);
                memset(brightnessDetails , '\0', (sizeof(char)*5));
                char BrightnessDetail[STR_DETAILS_20]= "Brightness:";
                DEBUG_PRINT(DEBUG_TRACE,"Calling getBrightness to LED : %s \n",LEDName.toUtf8().constData());
                list.append(LEDName);
                params["params"]=list;
                resultParams = ptr_service->callMethod("getBrightness", params);
                ReturnValue = resultParams["success"].toBool();
                LEDBrightness = resultParams["brightness"].toInt();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service getBrightness() call Success.\n");
                        response["result"]="SUCCESS";
                        sprintf(brightnessDetails , "%d",LEDBrightness);
                        strcat(BrightnessDetail,brightnessDetails);
                        response["details"]=BrightnessDetail;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service getBrightness() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service getBrightness call failed";
                }
                free(brightnessDetails);
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}

/***************************************************************************
 *Function name : SM_FP_SetLED
 *Descrption    : This will sets the color and Brightness of the front panel LED..
 *parameter [in]: req - name of the LED and Brightness value to be set.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_SetLED(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_SetLED ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                QString LEDName = QString::fromStdString(req["LEDName"].asCString());
                int LEDBrightness = req["LEDBrightness"].asInt();
                int LEDColorRed = req["LEDColorRed"].asInt();
                int LEDColorBlue = req["LEDColorBlue"].asInt();
                int LEDColorGreen = req["LEDColorGreen"].asInt();
                ServiceParams params, resultParams;
                QVariantList list;
                QVariantHash properties;
                properties.insert("ledIndicator", LEDName);
                properties.insert("brightness", LEDBrightness);
                properties.insert("red",LEDColorRed);
                properties.insert("blue",LEDColorBlue);
                properties.insert("green",LEDColorGreen);
                list.append(properties);

                bool ReturnValue ;
                DEBUG_PRINT(DEBUG_TRACE,"Calling setLED to LED : %s to brightness : %d\n",LEDName.toUtf8().constData(),LEDBrightness);
                params["params"]=list;
                resultParams = ptr_service->callMethod("setLED", params);
                ReturnValue = resultParams["success"].toBool();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setLED() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="Front Panel Service setLED success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setLED() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service setLED call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}
/***************************************************************************
 *Function name : SM_FP_SetAPIVersion
 *Descrption    : This will check the functionality of getApiVersionNumber and
                  setApiVersionNumber APIs.
 *parameter [in]: req-  service_name-Name of the service.
                        apiVersion - Parameter to be passed to callMethod API.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_SetAPIVersion(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_Services_SetAPIVersion ---->Entry\n");
#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;

        if( &req["apiVersion"] == NULL)
        {
                response["result"]="FAILURE";
                response["details"]=" apiVersion is NULL";
                return ;
        }
        int setApiVersion=req["apiVersion"].asInt();
        //ServiceParams params;
        int getApiVersion=0;
        char apiVersion[STR_DETAILS_20]= "API_VERSION:";
        char *versionDetails = (char*)malloc(sizeof(char)*STR_DETAILS_20);
        memset(versionDetails , '\0', (sizeof(char)*STR_DETAILS_20));
        if(ptr_service != NULL)
        {
                getApiVersion =ptr_service->getApiVersionNumber();
                if(setApiVersion==getApiVersion)
                {
                        response["result"]="SUCCESS";
                        response["details"]="SAME_DATA_ALREADY_ENTERED";
                        return;
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
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
        free(versionDetails);
        DEBUG_PRINT(DEBUG_TRACE,"\nSM_FP_SetAPIVersion ---->Exit\n");
        return ;
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif

}

/***************************************************************************
 *Function name : SM_FP_SetPreferences
 *Descrption    : This will sets the color and Brightness of the front panel LED..
 *parameter [in]: req - name of the LED and Brightness value to be set.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_SetPreferences(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_SetPreferences ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                std::string LEDName = req["LEDName"].asCString();
                int LEDBrightness = req["LEDBrightness"].asInt();
                int LEDColorRed = req["LEDColorRed"].asInt();
                int LEDColorBlue = req["LEDColorBlue"].asInt();
                int LEDColorGreen = req["LEDColorGreen"].asInt();
                ServiceParams params, resultParams;
                QVariantList list;
                QVariantHash properties , setpref;
                properties.insert("brightness", LEDBrightness);
                properties.insert("red",LEDColorRed);
                properties.insert("blue",LEDColorBlue);
                properties.insert("green",LEDColorGreen);
                setpref.insert(LEDName.c_str(),properties);
                list.append(setpref);

                bool ReturnValue ;
                DEBUG_PRINT(DEBUG_TRACE,"Calling setPreferences to LED \n");
                params["params"]=list;
                resultParams = ptr_service->callMethod("setPreferences", params);
                ReturnValue = resultParams["success"].toBool();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setPreferences() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="Front Panel Service setPreferences success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setPreferences() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service setPreferences call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}
/***************************************************************************
 *Function name : SM_FP_GetPreferences
 *Descrption    : This will sets the color and Brightness of the front panel LED..
 *parameter [in]: req - name of the LED and Brightness value to be set.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_GetPreferences(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_GetPreferences ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                std::string LEDName = req["LEDName"].asCString();
                char getprefdetails[STR_DETAILS_50] = {'\0'};
                ServiceParams params, resultParams;
                QVariantList list;
                QVariantHash properties , getpref;

                bool ReturnValue ;
                DEBUG_PRINT(DEBUG_TRACE,"Calling getPreferences to LED \n");
                params["params"]=list;
                resultParams = ptr_service->callMethod("getPreferences", params);
                ReturnValue = resultParams["success"].toBool();
                getpref = resultParams["preferences"].toHash();
                properties = getpref[LEDName.c_str()].toHash();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service getPreferences() call Success.\n");
                        DEBUG_PRINT(DEBUG_TRACE,"LED:%s,Brightness:%d,Red:%d,Green:%d,Blue:%d",LEDName.c_str(),properties["brightness"].toInt(),properties["red"].toInt(),properties["green"].toInt(),properties["blue"].toInt());
                        sprintf(getprefdetails,"LED:%s,Brightness:%d,Red:%d,Green:%d,Blue:%d",LEDName.c_str(),properties["brightness"].toInt(),properties["red"].toInt(),properties["green"].toInt(),properties["blue"].toInt());
                        response["result"]="SUCCESS";
                        response["details"]=getprefdetails;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service getPreferences() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service getPreferences call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}
/***************************************************************************
 *Function name : SM_FP_SetBlink
 *Descrption    : This will sets the Blink pattern of the front panel LED..
 *parameter [in]: req - name of the LED and Brightness value to be set.
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_SetBlink(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_SetBlink ---->Entry\n");

#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                std::string LEDName = req["LEDName"].asCString();
                std::string LEDBrightness = req["LEDBrightness"].asCString();
                std::string LEDColorRed = req["LEDColorRed"].asCString();
                std::string LEDColorBlue = req["LEDColorBlue"].asCString();
                std::string LEDColorGreen = req["LEDColorGreen"].asCString();
                std::string BlinkDuration = req["BlinkDuration"].asCString();
                std::string delimiter = ",";
                int iterationcount = req["IterationCount"].asInt();
                int sequencecount = req["SequenceCount"].asInt();
                ServiceParams params, resultParams;
                QVariantList Blinklist,patternlist;
                QVariantHash blinkinfo , pattern[sequencecount];
                blinkinfo.insert("ledIndicator", LEDName.c_str());
                blinkinfo.insert("iterations",iterationcount);
                size_t pos = 0;
                std::string token;
                int brightness, red, green, blue,duration;
                for (int i = 0; i < sequencecount ;  i++)
                {
                        token = LEDBrightness.substr(0, LEDBrightness.find(delimiter));
                        std::cout << token << std::endl;
                        LEDBrightness.erase(0, LEDBrightness.find(delimiter) + delimiter.length());
                        stringstream convert(token);
                        convert>>brightness;
                        pattern[i].insert("brightness",brightness);
                        token = LEDColorRed.substr(0, LEDColorRed.find(delimiter));
                        std::cout << token << std::endl;
                        LEDColorRed.erase(0, LEDColorRed.find(delimiter) + delimiter.length());
                        stringstream convert1(token);
                        convert1>>red;
                        pattern[i].insert("red",red);
                        token = LEDColorGreen.substr(0, LEDColorGreen.find(delimiter));
                        std::cout << token << std::endl;
                        LEDColorGreen.erase(0, LEDColorGreen.find(delimiter) + delimiter.length());
                        stringstream convert2(token);
                        convert2>>green;
                        pattern[i].insert("green",green);
                        token = LEDColorBlue.substr(0, LEDColorBlue.find(delimiter));
                        std::cout << token << std::endl;
                        LEDColorBlue.erase(0, LEDColorBlue.find(delimiter) + delimiter.length());
                        stringstream convert3(token);
                        convert3>>blue;
                        pattern[i].insert("blue",blue);
                        token = BlinkDuration.substr(0, BlinkDuration.find(delimiter));
                        std::cout << token << std::endl;
                        BlinkDuration.erase(0, BlinkDuration.find(delimiter) + delimiter.length());
                        stringstream convert4(token);
                        convert4>>duration;
                        pattern[i].insert("duration",duration);
                        patternlist << pattern[i];
                        DEBUG_PRINT(DEBUG_TRACE,"duration:%d,Brightness:%d,Red:%d,Green:%d,Blue:%d",duration,brightness,red,green,blue);
                }
                blinkinfo.insert("pattern",patternlist);
                Blinklist.append(blinkinfo);
                bool ReturnValue ;
                DEBUG_PRINT(DEBUG_TRACE,"Calling setBlink to LED \n");
                params["params"]=Blinklist;
                resultParams = ptr_service->callMethod("setBlink", params);
                ReturnValue = resultParams["success"].toBool();
                if (ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setBlink() call Success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="Front Panel Service setBlink success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service setBlink() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service setBlink call failed";
                }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel Service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
}


                                                                                                       
/***************************************************************************
 *Function name : SM_FP_Set_24_Hour_Clock
 *Descrption    : This will set 24hour clock..
 *parameter [in]: req - bool .
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_Set_24_Hour_Clock(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_Set_24_Hour_Clock ---->Entry\n");
#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                bool is24hour= req["is24hour"].asInt();
                if((is24hour==0) || (is24hour==1))
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Calling Front panel Service set24HourClock with value %d\n",is24hour);

                        QVariantList list;
                        ServiceParams params, resultParams;
                        list.append(is24hour);
                        params["params"] = list;
                        bool  ReturnValue ;
                        try
                        {
                                resultParams= ptr_service->callMethod("set24HourClock", params);
                                ReturnValue = resultParams["success"].toBool();
                                if (ReturnValue)
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service set24HourClock() call Success.\n");
                                        response["result"]="SUCCESS";
                                        response["details"]="Front Panel Service set24HourClock value call success";
                                }
                                else
                                {
                                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service set24HourClock() call Failure.\n");
                                        response["result"]="FAILURE";
                                        response["details"]="Front Panel Service set24HourClock call failed";
                                }
                        }
                        catch(...)
                        {
                                 DEBUG_PRINT(DEBUG_ERROR,"Exception occured while calling set24HourClock \n");
                                 response["result"]="FAILURE";
                                response["details"]="Failed to call set24HourClock";
                        }

                }
                else
                {
                        DEBUG_PRINT(DEBUG_ERROR,"Invalid parameters  is passed to set24HourClock \n");
                        response["result"]="FAILURE";
                        response["details"]="Failed to call set24HourClock";
                }

        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"Failed to create Front Panel Service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front Panel Service handler";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";


#endif
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_Set_24_Hour_Clock ---->Exit\n");
        return ;
}
/***************************************************************************
 *Function name : SM_FP_Is_24_Hour_Clock
 *Descrption    : This will get current time format (whether 24hourclock is enabled/disabled)
 *parameter [in]: none .
 *****************************************************************************/
void ServiceManagerAgent::SM_FP_Is_24_Hour_Clock(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_Is_24_Hour_Clock ---->Entry\n");
#ifdef HAS_FRONT_PANEL
        FrontPanelService *ptr_service = pFPService;
        if(ptr_service != NULL)
        {
                QVariantList list;
                ServiceParams params, resultParams;
                params["params"] = list;
                bool ReturnValue;
           try
           {
                resultParams = ptr_service->callMethod("is24HourClock", params);
                ReturnValue = resultParams["success"].toBool();
                if(ReturnValue)
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service is24HourClock() call success.\n");
                        response["result"]="SUCCESS";
                        response["details"]="Front Panel Service is24HourClock success";
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE,"Front Panel Service is24HourClock() call Failure.\n");
                        response["result"]="FAILURE";
                        response["details"]="Front Panel Service is24HourClock call failed";
                }
           }
           catch(...)
           {
               DEBUG_PRINT(DEBUG_ERROR,"Exception occured while calling is24HourClock \n");
               response["result"]="FAILURE";
               response["details"]="Failed to call is24HourClock";
          }
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR, "Failed to create Front panel service handler.\n");
                response["result"]="FAILURE";
                response["details"]="Failed to create Front panel service handler.";
        }
#else
        DEBUG_PRINT(DEBUG_TRACE,"FP Service not supported\n");
        response["result"]="FAILURE";
        response["details"]="FP Service not supported";
#endif
        DEBUG_PRINT(DEBUG_TRACE,"SM_FP_Is_24_Hour_Clock ---->Exit\n");
        return ;
}

/***************************************************************************
 *Function name : SM_Generic_CallMethod
 *Descrption    : A Generic Stub function for invoking callMethod for all
 *		  services
 *parameter [in]: Servicename : name of the service to be invoked
 *                methodName : API to be invoked
 *		  parameters : List of parameters to be passed to the service
 *****************************************************************************/
void ServiceManagerAgent::SM_Generic_CallMethod (IN const Json::Value& req, 
						 OUT Json::Value& response) {

        DEBUG_PRINT(DEBUG_TRACE,"SM_Generic_CallMethod ---->Entry\n");

        bool ReturnValue = TEST_FAILURE;
  	int count = 0;
        int listPos = 0;
        Json::Value jsonValue;
        Json::ValueIterator paramsItr;
	string serviceName, methodName;
	QVariantList qList;
	Service *ptrService = NULL;
	QVariantHash::iterator successPos;
	ServiceParams inputParams, outputParams;
	       
        if ((NULL == &req["service_name"]) || (NULL == &req["method_name"]) || (NULL == &req["inputCount"])) {
		response["result"]="FAILURE";
		response["details"]="Invalid Parameters";
                return;
        }

        serviceName = req["service_name"].asCString();
        methodName = req["method_name"].asCString();
  	count = req["inputCount"].asInt();

#ifdef HAS_API_HDMI_CEC
	if (QString::fromStdString(serviceName) == HdmiCecService::SERVICE_NAME) {
		ptrService = pHdmiService;
	}
        else
#endif   
#ifdef HAS_FRONT_PANEL
          if (QString::fromStdString(serviceName) == FrontPanelService::SERVICE_NAME) {
		ptrService = pFPService;
	}
	else
#endif
        {
		ptrService = ServiceManager::getInstance()->getGlobalService (QString::fromStdString(serviceName)); 
	}
        if (NULL != ptrService) {

           if (SM_MIN_PARAMS == count) {
                jsonValue = req["params"];
           }
           else if (count > SM_MIN_PARAMS) {
                paramsItr = req["params"].begin();
                jsonValue = *(paramsItr);
           }
           for (  ;count > 0;count--, listPos++) {
                if (jsonValue.isArray()) {
                        qList.insert(listPos, convertArrayToQList (jsonValue));
                }
                else if (jsonValue.isObject()) {
                        qList.insert(listPos, convertObjectToQList(jsonValue));
                }
                else {
                        qList.insert(listPos, convertValueToQVariant(jsonValue));
                }
                if (count > SM_MIN_PARAMS) {
                        paramsItr++;
                        jsonValue = *(paramsItr);
                }
           }
           inputParams["params"] = qList;
          
           try {
		/*
		 *Call the Service manager calllMethod API
		 */
                outputParams = ptrService->callMethod(QString::fromStdString(methodName), inputParams);
                ReturnValue = (outputParams["success"].isNull())?TEST_FAILURE:outputParams["success"].toBool();
                if ((outputParams.isEmpty()) || ((TEST_FAILURE == ReturnValue) && !(outputParams["success"].isNull()))) {
                        DEBUG_PRINT (DEBUG_TRACE,"%s call Failure.\n", methodName.c_str());
                        response["result"] = "FAILURE";
                        response["details"] = methodName + " call failed";
                }
                else {
                        DEBUG_PRINT (DEBUG_TRACE,"%s call success.\n", methodName.c_str());
                        response["result"] = "SUCCESS";
			if ((outputParams.contains("success")) && (outputParams.size() == SM_MIN_PARAMS)) { 
				response["details"] =  methodName + " call success";
			}
			else {
                                /*
                                 *Skip success field
                                 */
                                successPos = outputParams.find("success");
                                if (successPos !=  outputParams.end()) {
                                    outputParams.erase (successPos);
                                }
                                listPos = 0;
                                foreach (QVariant value, outputParams) {
                                    if ((QVariant::Hash == value.type()) || (QVariant::Map == value.type())) {
                                        jsonValue = convertQHashToJson (value);
                                    }
                                    else if (QVariant::List == value.type()) {
                                        jsonValue = convertQListToJson (value.toList());
                                    }
                                    else {
                                        jsonValue = convertQVariantToJson (value);
                                    }
                                    if (outputParams.size() > SM_MIN_PARAMS) {
                                        response["details"][listPos] = jsonValue;
                                        listPos++;
                                    }
                                    else {
                                        response["details"] = jsonValue;
                                    }
                                }
                        }
                }
           }
           catch(...) {
               DEBUG_PRINT (DEBUG_ERROR,"Exception occured while calling %s\n", methodName.c_str());
               response["result"] = "FAILURE";
               response["details"] = "Failed to call " + methodName;
          }
        }
        else {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to create %s service handler.\n", serviceName.c_str());
                response["result"] = "FAILURE";
                response["details"] = "Failed to create " + serviceName + " service handler.";
        }

        DEBUG_PRINT (DEBUG_TRACE,"SM_Generic_CallMethod ---->Exit\n");
        return;
}

/**************************************************************************
 * Function name : ServiceManagerAgent::SM_ExecuteCmd()
 *
 * Arguments     : Input arguments are command to execute in box
 *
 * Description   : This will execute linux commands in box
 * ***************************************************************************/
void ServiceManagerAgent::SM_ExecuteCmd(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "SM_ExecuteCmd ---> Entry\n");
        string fileinfo = request["command"].asCString();
        FILE *fp = NULL;
        char readRespBuff[BUFF_LENGTH];
        string popenBuff;

        /*Frame the command  */
        string path = "";
        path.append(fileinfo);

        DEBUG_PRINT(DEBUG_TRACE, "Command Request Framed: %s\n",path.c_str());

        fp = popen(path.c_str(),"r");

        /*Check for popen failure*/
        if(fp == NULL)
        {
                response["result"] = "FAILURE";
                response["details"] = "popen() failure";
                DEBUG_PRINT(DEBUG_ERROR, "popen() failure for %s\n", path.c_str());

                return ;
        }

        /*copy the response to a buffer */
        while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
                popenBuff += readRespBuff;
        }

        pclose(fp);

        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
        response["result"] = "SUCCESS";
        response["details"] = popenBuff;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "SM_ExecuteCmd -->Exit\n");
        return ;

}

/**************************************************************************
 * Function Name: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "ServiceManagerAgent".
 *
 **************************************************************************/

extern "C" ServiceManagerAgent* CreateObject(TcpSocketServer &ptrtcpServer)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Entry\n");
	return new ServiceManagerAgent(ptrtcpServer);
	DEBUG_PRINT(DEBUG_TRACE,"\nCreateObject ---->Exit\n");
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool ServiceManagerAgent::cleanup(IN const char* szVersion)
{
	DEBUG_PRINT(DEBUG_TRACE,"\ncleanup ---->Entry\n");
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

