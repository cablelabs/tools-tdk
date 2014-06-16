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

#include "IARMBUSAgent.h"

int LastKeyType;
int LastKeyCode;
char LastEvent[40],g_ManagerName[20];

/*These global variables are to check the test app with event handler and BusCall APIS*/
int g_evtData[EVTDATA_MAX_SIZE],g_iter=0;
char g_evtName[EVTDATA_MAX_SIZE];
std::string g_tdkPath = getenv("TDK_PATH");

/**************************************************************************
 *
 * Function Name        : prereqcheck
 * Descrption   : This function will get the existense of pre- requisite app
 *                 nd return SUCESS or FAILURE status to the
 *                caller.
 *
 * @param retval [in] ownerName - owner(manager) to be checked.
 *		 [out]- bool - SUCCESS / FAILURE
 ***************************************************************************/

bool prereqcheck(char *ownerName )
{
	std::string pre_req_chk;
	std::string pre_req_chk_file;
	pre_req_chk_file= g_tdkPath + "/" + PRE_REQ_CHECK;
	pre_req_chk ="pidstat | grep Main >" + pre_req_chk_file;
	int offset;
	std::string line;
	std::ifstream Myfile;
	char *appName = (char*)malloc(sizeof(char*)*20);
	memset(appName , '\0', (sizeof(char)*20));
	if ((strcmp(ownerName, "Daemon")  == 0)||(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME) ==0))
        {
		strcpy(appName,DAEMON_EXE);	
	}
	else if (strcmp(ownerName, "IRMgr")  == 0)
        {
		strcpy(appName,IRMGR_EXE);
	}
	else if (strcmp(ownerName, "PWRMgr")  == 0)
        {
		strcpy(appName,PWRMGR_EXE);
	}
	else if (strcmp(ownerName, "MFRLib")  == 0)
        {
		strcpy(appName,MFRMGR_EXE);
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"Invalid Owner Name\n");
		return TEST_FAILURE;
	}
	
	 //* To handle exception for system call
	try
	{
		system((char *)pre_req_chk.c_str());
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured during pidstat\n");
		DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
		return TEST_FAILURE;
	}
	Myfile.open (pre_req_chk_file.c_str());

	if(Myfile.is_open())
	{
		while(!Myfile.eof())
		{
			getline(Myfile,line);
			if ((offset = line.find(appName, 0)) != std::string::npos) {
				Myfile.close();
				DEBUG_PRINT(DEBUG_LOG,"\nPre-Requisites present\n");
				return TEST_SUCCESS;
			}
		}
		DEBUG_PRINT(DEBUG_ERROR,"\nPre-Requisites not present\n");
		return TEST_FAILURE;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open this file.\n");
		return TEST_FAILURE;
	}
}

/*This is a constructor function for IARMBUSAgent class*/

IARMBUSAgent::IARMBUSAgent()
{
	DEBUG_PRINT(DEBUG_LOG,"IARMBUSAgent Initialized\n");
}


/***************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper function will be used in the 
 *  		  script
 *****************************************************************************/ 

bool IARMBUSAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE,"IARM Initialize\n");
	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_Init, "TestMgr_IARMBUS_Init");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_Term, "TestMgr_IARMBUS_Term");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_BusConnect, "TestMgr_IARMBUS_Connect");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_BusDisconnect, "TestMgr_IARMBUS_Disconnect");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_IsConnected, "TestMgr_IARMBUS_IsConnected");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_RequestResource, "TestMgr_IARMBUS_RequestResource");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_ReleaseResource, "TestMgr_IARMBUS_ReleaseResource");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_RegisterEventHandler, "TestMgr_IARMBUS_RegisterEventHandler");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_UnRegisterEventHandler, "TestMgr_IARMBUS_UnRegisterEventHandler");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_RegisterEvent, "TestMgr_IARMBUS_RegisterEvent");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_RegisterCall, "TestMgr_IARMBUS_RegisterCall");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_BroadcastEvent, "TestMgr_IARMBUS_BroadcastEvent");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_BusCall, "TestMgr_IARMBUS_BusCall");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::get_LastReceivedEventDetails, "TestMgr_IARMBUS_GetLastReceivedEventDetails");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::InvokeSecondApplication, "TestMgr_IARMBUS_InvokeSecondApplication");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSAgent::IARMBUSAgent_GetContext, "TestMgr_IARMBUS_GetContext");
	return TEST_SUCCESS;

}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string IARMBUSAgent::testmodulepre_requisites()
{
	if ((prereqcheck((char*)"Daemon"))== TEST_SUCCESS)
	        return "SUCCESS";
	else
		return "FAILURE<DETAILS> Pre-requisite check failed for Daemon Mgr";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool IARMBUSAgent::testmodulepost_requisites()
{
        return TEST_SUCCESS;
}


/**************************************************************************
 *
 * Function Name	: getResult
 * Descrption	: This function will get the retvalue as input and it returns 
 *		  corresponding SUCCESS or FAILUER status to the 
 *		  wrapper function.
 *
 * @param retval [in] - return value of IARMBUS APIs
 ***************************************************************************/

char* getResult(int retval,char *resultDetails)
{
	if(retval==0)
	{
		strcpy(resultDetails,"NULL");
		return (char*)"SUCCESS";
	}
	else
	{       

		switch(retval)
		{
			case 1: strcpy(resultDetails,"INVALID_PARAM");
				break;
			case 2: strcpy(resultDetails,"INVALID_STATE");
				break;
			case 3: strcpy(resultDetails,"IPCORE_FAIL");
				break;
			case 4: strcpy(resultDetails,"OUT_OF_MEMORY");
				break;
			default :
				strcpy(resultDetails,"Unidentified Error");
				break; 
		}
		return (char*)"FAILURE";
	}

}
/**************************************************************************
 *
 * Function Name	: IARMBUSAgent_Init
 * Descrption	: IARMBUSAgent_Init wrapper function will be used to call IARMBUS 
 API "IARM_Bus_Init".
 *
 * @param [in] req- has "Process_name" which is input to IARM_Bus_Init
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/

bool IARMBUSAgent::IARMBUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_Init --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["Process_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\ncalling IARM_Bus_Init directly from IARMBUSAgent_Init\n");
	/*Calling IARMBUS API IARM_Bus_Init with json req as parameter*/
	retval=IARM_Bus_Init((char *)req["Process_name"].asCString());
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_Init --->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_Term
 * Descrption	: IARMBUSAgent_Term wrapper function will be used to call IARMBUS API "IARM_Bus_Term".
 *
 * @param [in] req- None
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/
bool IARMBUSAgent::IARMBUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_Term --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\ncalling IARM_Bus_Term()\n");
	/*Calling IARMBUS API IARM_Bus_Term  */
	retval=IARM_Bus_Term();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_Term --->Exit\n");
	return TEST_SUCCESS;

}

/**************************************************************************
 * Functio Name	: IARMBUSAgent_BusConnect
 * Descrption	: IARMBUSAgent_BusConnect wrapper function will be used to call IARMBUS API "IARM_Bus_Connect".
 * 
 * @param [in] req- None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BusConnect --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\ncalling IARM_Bus_Connect\n");
	/*Calling IARMBUS API IARM_Bus_Connect  */
	retval=IARM_Bus_Connect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_BusConnect --->Exit\n");
	return TEST_SUCCESS;

}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BusDisconnect
 * Descrption	: IARMBUSAgent_BusDisconnect wrapper function will be used to call 
 IARMBUS API "IARM_Bus_Disconnect".
 *
 * @param [in] req-None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/
bool IARMBUSAgent::IARMBUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BusDisconnect --->Entry\n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\ncalling IARM_Bus_Disconnect\n");
	/*Calling IARMBUS API IARM_Bus_Disconnect  */
	retval=IARM_Bus_Disconnect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_BusDisconnect --->Exit\n");
	return TEST_SUCCESS;

}

/**************************************************************************
 * Function Name	: IARMBUSAgent_IsConnected
 * Description   : IARMBUSAgent_IsConnected wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_IsConnected".
 *
 * @param [in] req- has "member_name" which is input to IARM_Bus_IsConnected
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *****************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_IsConnected(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBus_IsConnected --->Entry \n");
	int isregistered;
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_IsConnected from IARMBus_IsConnected \n");
	if(&req["member_name"]==NULL)
	{
		return TEST_FAILURE;
	}

	/*Calling IARM API IARM_Bus_IsConnected */
	retval=IARM_Bus_IsConnected((char*)req["member_name"].asCString(),&isregistered);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status and success return value*/	
	if(retval == 0)
	{
		response["result"]="SUCCESS";
		if(isregistered==0)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nRegistered\n");
			response["details"]="Process_Not_Registered";
		}
		else if(isregistered==1)
		{
			DEBUG_PRINT(DEBUG_LOG,"\nNot Registered\n");
			response["details"]="Process_Registered";
		}
		else
		{
			response["details"]="NULL";
		}
	}
	else 
	{
		/*Filling json response with FAILURE status and error message*/
		response["result"]="FAILURE";
		switch(retval)
		{
			case 0:	response["details"]="IARM_RESULT_SUCCESS";
				break;
			case 1:	response["details"]="INVALID_PARAM";
				break;
			case 2:	response["details"]="INVALID_STATE";
				break;
			case 3:	response["details"]="IPCCORE_FAIL";
				break;
			case 4:	response["details"]="OUT_OF_MEMORY";
				break;
		}
	}
	free(resultDetails);	
	/*Need to fill the response with isregistered variable*/
	DEBUG_PRINT(DEBUG_TRACE,"\n IARM_Bus_IsConnected --->Exit \n");
	return TEST_SUCCESS;
}
/**************************************************************************
 * Function Name : IARMBUSAgent_RequestResource
 * Description 	: IARMBUSAgent_RequestResource wrapper function will be used to call 
 *		  IARMBUS API "IARM_BusDaemon_RequestOwnership".
 *
 * @param [in] req- contains "resource_type" which is input to IARM_BusDaemon_RequestOwnership
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ****************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_RequestResource(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RequestResource --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["resource_type"]==NULL)
	{
		return TEST_FAILURE;
	}
	int ResrcType_int=req["resource_type"].asInt(); 
	/*Calling IARMBUS API IARM_BusDaemon_RequestOwnership  */
	DEBUG_PRINT(DEBUG_LOG,"\n\n calling IARM_BusDaemon_RequestOwnership from IARMBUSAgent_RequestResource \n");
	retval =IARM_BusDaemon_RequestOwnership((IARM_Bus_ResrcType_t)ResrcType_int);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RequestResource --->Exit \n");
	return TEST_SUCCESS;
}
/**************************************************************************
 * Function Name	: IARMBUSAgent_ReleaseResource
 *
 * Description	: IARMBUSAgent_ReleaseResource wrapper function will be used to call IARMBUS 
 *		  API "IARM_BusDaemon_ReleaseOwnership".
 *
 * @param [in] req- has "resource_type" which is input to IARM_BusDaemon_ReleaseOwnership.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ****************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_ReleaseResource(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_ReleaseResource --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["resource_type"]==NULL)
	{
		return TEST_FAILURE;
	}
	int ResrcType_int=req["resource_type"].asInt(); 

	/*Calling IARMBUS API IARM_BusDaemon_ReleaseOwnership  */
	DEBUG_PRINT(DEBUG_LOG,"\n\n calling IARM_BusDaemon_ReleaseOwnership from IARMBUSAgent_ReleaseResource \n");
	retval =IARM_BusDaemon_ReleaseOwnership((IARM_Bus_ResrcType_t)ResrcType_int);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_ReleaseResource --->Exit \n");
	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name	: get_LastReceivedEventDetails
 * Description	: This function is to get the last received Event details 	
 *
 ***************************************************************************/


bool IARMBUSAgent::get_LastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n get_LastReceivedEventDetails --->Entry \n");
	char details[200]="Event Details:";
	const char *KeyCodedetails=" :: KeyCode : " ;
	const char *KeyTypedetails=" :: KeyType : ";
	char *KeyCodedetails1 =(char*)malloc(sizeof(char)*70); 
	memset(KeyCodedetails1 , '\0', (sizeof(char)*70));
	char *KeyTypedetails1 =(char*)malloc(sizeof(char)*5);
	memset(KeyTypedetails1 , '\0', (sizeof(char)*5));
	strcat(details,LastEvent);
	char *Eventdetails =(char*)malloc(sizeof(char)*20);
	memset(Eventdetails , '\0', (sizeof(char)*20));  
	char *evtdata =(char*)malloc(sizeof(char)*4);     
	memset(evtdata,'\0', (sizeof(char)*4));           
	char *evtName =(char*)malloc(sizeof(char)*1);     
	memset(evtName,'\0', (sizeof(char)*1));  
	if(strcmp(LastEvent,"IARM_BUS_IRMGR_EVENT_IRKEY")==0)
	{
		sprintf(KeyCodedetails1,"%x" , LastKeyCode);
		sprintf(KeyTypedetails1,"%x" , LastKeyType);
		strcat(details,KeyCodedetails);
		strcat(details,KeyCodedetails1);
		strcat(details,KeyTypedetails);
		strcat(details,KeyTypedetails1);
		response["result"]="SUCCESS";
	}
	else if((strcmp(LastEvent,"IARM_BUS_PWRMGR_EVENT_MODECHANGED")==0)||
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOURCEAVAILABLE")==0)||
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOLUTIONCHANGE")==0))
	{
		response["result"]="SUCCESS";
	}
	else if (strcmp(g_ManagerName,"DummyTestMgr")==0)     
	{                                                   
		for(int i=0;i<EVTDATA_MAX_SIZE;i++)         
		{                                           
			sprintf(evtdata,"%d",g_evtData[i]); 
			g_evtData[i]=0;                     
			sprintf(evtName,"%c",g_evtName[i]); 
			g_evtName[i]='\0';                  
			strcat(Eventdetails,evtName);       
			strcat(Eventdetails,":");           
			strcat(Eventdetails,evtdata);       
			DEBUG_PRINT(DEBUG_LOG,"\nevtName:%s\n",evtName);
			DEBUG_PRINT(DEBUG_LOG,"\nevtData:%s\n",evtdata);
			if(i<EVTDATA_MAX_SIZE-1)            
			{                                   
				strcat(Eventdetails,",");   
			}                                   

		}                                           
		response["result"]="SUCCESS";               
		response["details"]=Eventdetails;           
		return true;                                
							      
	}                                             
	else
	{
		response["result"]="FAILURE";

	}
	strcpy(KeyCodedetails1,details);
	response["details"]=KeyCodedetails1;
	free(KeyCodedetails1);
	memset(&(LastEvent) , '\0', (sizeof(char)*20));
	free(KeyTypedetails1);
	free(Eventdetails);
	free(evtName);
	free(evtdata);
	DEBUG_PRINT(DEBUG_TRACE,"\n get_LastReceivedEventDetails --->Exit \n");
	return true;
}

/**************************************************************************
 * Function Name	: fill_LastReceivedKey
 * Description	: fill_LastReceivedKey function is to fill the last recived IR 
 *		  key details in the global variable.
 *
 * @param[in]- keyCode,keyType IR key code and type.
 ***************************************************************************/

void fill_LastReceivedKey(int keyCode ,int keyType)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n fill_LastReceivedKey --->Entry \n");
	LastKeyCode=keyCode;
	LastKeyType=keyType;
	DEBUG_PRINT(DEBUG_TRACE,"\n fill_LastReceivedKey --->Exit \n");
}


/***************************************************************************
 * Function Name : _evtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

/*Hard-coded event handler*/

void _evtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_t *param = (IARM_Bus_PWRMgr_EventData_t *)data;
					DEBUG_PRINT(DEBUG_LOG,"\nEvent IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IARM_Bus_IRMgr_EventData_t *irEventData = (IARM_Bus_IRMgr_EventData_t*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					DEBUG_PRINT(DEBUG_LOG,"\nTest Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					fill_LastReceivedKey(keyCode,keyType);
					strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"\nResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
				}
				break;
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					DEBUG_PRINT(DEBUG_LOG,"\nResolution Change event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
				}
			default:
				break;
		}

	}
	/*The below code block is for handling thr test app scenario*/
	else if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		DEBUG_PRINT(DEBUG_TRACE,"\nInside DummyMgr event handler\n");
		int dummydata=0;
		char evtname;
		strcpy(g_ManagerName,IARM_BUS_DUMMYMGR_NAME);
		/* Handle events here */
		IARM_Bus_DUMMYMGR_EventData_t *eventData = (IARM_Bus_DUMMYMGR_EventData_t *)data;

		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:
			dummydata=eventData->data.dummy0.dummyData;
			evtname='X';
			DEBUG_PRINT(DEBUG_ERROR,"\nReceived i:%d",eventData->data.dummy0.dummyData);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:
			dummydata=eventData->data.dummy1.dummyData;
			evtname='Y';
			DEBUG_PRINT(DEBUG_ERROR,"\nReceived j:%d",eventData->data.dummy1.dummyData);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:
			dummydata=eventData->data.dummy2.dummyData;
			evtname='Z';
			DEBUG_PRINT(DEBUG_ERROR,"\nReceived k:%d",eventData->data.dummy2.dummyData);
			break;
		}
		if(g_iter<EVTDATA_MAX_SIZE)
		{
			g_evtName[g_iter]=evtname;
			g_evtData[g_iter++]=dummydata;
			if(g_iter==EVTDATA_MAX_SIZE)
			{
				g_iter=0;
			}
		}
	}

}

/**************************************************************************
 * Function Name	: IARMBUSAgent_RegisterEventHandler
 * Description	: IARMBUSAgent_RegisterEventHandler wrapper function will be used to call 
 *	          IARMBUS API "IARM_Bus_RegisterEventHandler".
 *
 * @param [in] req- has "event_id" and "owner_name" which are input to IARM_Bus_RegisterEventHandler.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterEventHandler --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL || &req["owner_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	if(prereqcheck(ownerName))
	{
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler from IARMBUSAgent_RegisterEventHandler \n");
	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandler);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterEventHandler --->Exit \n");
	return TEST_SUCCESS;
	}
	else
	{
	response["result"]="FAILURE";
	response["details"]="Pre-Requisite check Failed for the given Owner";
	free(resultDetails);
	DEBUG_PRINT(DEBUG_ERROR,"\n IARMBUSAgent_RegisterEventHandler -- Pre-Requisite check Failed for the given Owner \n");
	return TEST_FAILURE;
	}

}
/**************************************************************************
 * Function Name	: IARMBUSAgent_UnRegisterEventHandler
 * Description	: IARMBUSAgent_UnRegisterEventHandler wrapper function will be used to call IARMBUS API 
 *		  "IARM_Bus_UnRegisterEventHandler".
 *
 * @param [in] req- has "event_id" and "owner_name" which are input to IARM_Bus_UnRegisterEventHandler.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_UnRegisterEventHandler --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL || &req["owner_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	if(prereqcheck(ownerName))
        {
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_UnRegisterEventHandler from IARMBUSAgent_UnRegisterEventHandler \n");
	/*Calling IARMBUS API IARM_Bus_UnRegisterEventHandler */
	retval=IARM_Bus_UnRegisterEventHandler(ownerName,(IARM_EventId_t)eventId);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_UnRegisterEventHandler --->Exit \n");
	return TEST_SUCCESS;
	}
	else
        {
        response["result"]="FAILURE";
        response["details"]="Pre-Requisite check Failed for the given Owner";
        free(resultDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\n IARMBUSAgent_UnRegisterEventHandler -- Pre-Requisite check Failed for the given Owner \n");
        return TEST_FAILURE;
        }
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_GetContext
 * Description	: IARMBUSAgent_GetContext wrapper function will be used to call IARMBUS API
 *		  "IARM_Bus_GetContext".
 *
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *
 *****************************************************************************/

bool IARMBUSAgent::IARMBUSAgent_GetContext(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\nIARMBUSAgent_GetContext --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_INVALID_STATE;
	char *resultDetails;
	void **context=NULL;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_GetContext from IARMBUSAgent_GetContext \n");
	/*Calling IARMBUS API IARM_Bus_GetContext */
	retval=IARM_Bus_GetContext(context);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_GetContext --->Exit \n");
	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name : _ReleaseOwnership
 * Description	: _ReleaseOwnership function will be registered for 
 IARM_BusDaemon_RequestOwnership API .
 ***************************************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
	DEBUG_PRINT(DEBUG_TRACE,"############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\n");
	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	return retCode;
}


/**************************************************************************
 * Function Name : IARMBUSAgent_RegisterCall
 * Description	: IARMBUSAgent_RegisterCall wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_RegisterCall".
 *
 * @param [in] req- has "owner_name" which is input to IARM_Bus_RegisterCall
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_RegisterCall(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterCall --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterCall from IARMBUSAgent_RegisterCall \n");
	if(&req["owner_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	char *ownerName=(char*)req["owner_name"].asCString();
	/*Calling IARMBUS API IARM_Bus_RegisterCall  */
	retval=IARM_Bus_RegisterCall(ownerName,_ReleaseOwnership);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterCall --->Exit \n");
	return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name : IARMBUSAgent_RegisterEvent
 * Description	: IARMBUSAgent_RegisterEvent wrapper function will be used to call 
 *		  IARMBUS API "IARM_Bus_RegisterEvent".
 *
 * @param [in] req- has "max_event" which is input to IARM_Bus_RegisterEvent
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/

bool IARMBUSAgent::IARMBUSAgent_RegisterEvent(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterEvent --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEvent from IARMBUSAgent_RegisterEvent \n");
	if(&req["max_event"]==NULL)
	{
		return TEST_FAILURE;
	}
	int maxevent=req["max_event"].asInt();
	/*Calling IARMBUS API IARM_Bus_RegisterEvent  */
	retval=IARM_Bus_RegisterEvent((IARM_EventId_t)maxevent);
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_RegisterEvent --->Exit \n");
	return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BroadcastEvent
 * Description	: IARMBUSAgent_BroadcastEvent wrapper function will be used to call IARMBUS 
 *		  API "IARM_Bus_BroadcastEvent".
 * @param [in] req- has three types of inputs for three types events such as IR,POWER and 
 *	BUS_DAEMON events.req contains 	
 *	owner_name - Owner of the event.
 *	event_id - The event which is going to be broadcasted.
 *	keyType[IR] , keyCode[IR] - IR key codes.
 *	newState [POWER] - Decoder state will change to state which is mentioned newState. 
 *	resource_type [BUS_BAEMON] - type of resource.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BroadcastEvent --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["event_id"]==NULL ||&req["owner_name"]==NULL || &req["keyType"]==NULL || &req["keyCode"]==NULL || 
	   &req["newState"]==NULL ||&req["resource_type"]==NULL)
	{
		return TEST_FAILURE;
	}
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	if(prereqcheck(ownerName))
        {
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		IARM_Bus_IRMgr_EventData_t eventData;
		eventData.data.irkey.keyType = req["keyType"].asInt();
		eventData.data.irkey.keyCode = req["keyCode"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		IARM_Bus_PWRMgr_EventData_t eventData;
		eventData.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)req["newState"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		IARM_Bus_EventData_t  eventData;
		eventData.resrcType = (IARM_Bus_ResrcType_t)req["resource_type"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_BroadcastEvent from IARMBUSAgent_BroadcastEvent \n");
		/*Calling IARMBUS API IARM_Bus_BroadcastEvent  */
		retval=IARM_Bus_BroadcastEvent(ownerName,(IARM_EventId_t)eventId,(void*)&eventData,sizeof(eventData));
	}
	else if(strcmp(ownerName,"DISKMgr")==0)
	{
		/*
		   HDD events will be handled after IARMBUS code is available for XG1
		 */

	}
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/
	response["result"]=getResult(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BroadcastEvent --->Exit \n");
	return TEST_SUCCESS;
	}
        else
        {
        response["result"]="FAILURE";
        response["details"]="Pre-Requisite check Failed for the given Owner";
        free(resultDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\n IARMBUSAgent_BroadcastEvent -- Pre-Requisite check Failed for the given Owner \n");
        return TEST_FAILURE;
        }
}

/**************************************************************************
 * Function Name	: IARMBUSAgent_BusCall
 * Description	: IARMBUSAgent_BusCall wrapper function will be used to call IARMBUS API "IARM_Bus_Call".
 * @param [in] req- has three types of inputs for three types events such as IR,POWER and BUS_DAEMON events.
 *	req contains 	
 *	owner_name - Owner of the event.
 *       methodName - Name of the RPC method
 *	event_id - The event which is going to be broadcasted.
 *	set_timeout[IR] - keyRepeatInterval.
 *	newState [POWER] - Decoder state will change to state which is mentioned newState. 
 * 	resource_type [BUS_BAEMON] - type of resource.
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of IARMBUS API.
 *
 ***************************************************************************/	

bool IARMBUSAgent::IARMBUSAgent_BusCall(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BusCall --->Entry \n");
	IARM_Result_t retval=IARM_RESULT_SUCCESS;
	char *RepeatInterval=(char*)malloc(sizeof(char)*5);			
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
        if(&req["method_name"]==NULL ||&req["owner_name"]==NULL || &req["set_timeout"]==NULL || &req["newState"]==NULL ||
           &req["resource_type"]==NULL ||&req["testapp_API0_data"]==NULL ||&req["testapp_API1_data"]==NULL)
	{
		return TEST_FAILURE;
	}
	char *ownerName=(char*)req["owner_name"].asCString();
	char *methodName=(char*)req["method_name"].asCString();
	if(prereqcheck(ownerName))
        {
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		IARM_Bus_IRMgr_SetRepeatInterval_Param_t param_Set;
		param_Set.timeout=(unsigned int)req["set_timeout"].asInt();
		IARM_Bus_IRMgr_GetRepeatInterval_Param_t param_Get;
		DEBUG_PRINT(DEBUG_LOG,"\n IR-calling IARM_Bus_Call from IARM_Bus_Call \n");
		/*Calling IARMBUS API IARM_Bus_Call  */
		if(strcmp(methodName,"GetRepeatInterval")==0)
		{		
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Get,sizeof(param_Get));
			if(retval==0)
			{
				sprintf(RepeatInterval,"%d",param_Get.timeout);
				response["details"]= RepeatInterval;
				DEBUG_PRINT(DEBUG_LOG,"\nIR-Current RepeatInterval is :%s\n",RepeatInterval);
			}

		}
		else
		{	
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Set,sizeof(param_Set));
			if(retval==0)
			{
				sprintf(RepeatInterval,"%d",param_Set.timeout);
				response["details"]= RepeatInterval;
				DEBUG_PRINT(DEBUG_LOG,"SetRepeatInterval:%s\n",response["details"].asCString()) ;
			}	
		}
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/	
		response["result"]=getResult(retval,resultDetails);
		if(retval!=0)
		{
			response["details"]=resultDetails;
		}

	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		IARM_Bus_PWRMgr_GetPowerState_Param_t param_Get;
		IARM_Bus_PWRMgr_SetPowerState_Param_t param_Set;
		param_Set.newState = (IARM_Bus_PWRMgr_PowerState_t)req["newState"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"\n PWR-calling IARM_Bus_Call from IARM_Bus_Call \n");
		DEBUG_PRINT(DEBUG_LOG,"\n PWR-New power state is :%d\n",param_Set.newState);
		if(strcmp(methodName,"GetPowerState")==0)
		{		
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Get,sizeof(param_Get));
			switch(param_Get.curState)
			{
				case 0:	response["details"]="POWERSTATE_OFF";
					break;
				case 1:	response["details"]="POWERSTATE_STANDBY";
					break;
				case 2:	response["details"]="POWERSTATE_ON";
					break;
				default:
					response["details"]="Unknown State";			 			
			}
			DEBUG_PRINT(DEBUG_LOG,"\n PWR-Current power state is:%d-%s\n",param_Get.curState,response["details"].asCString());
		}
		else
		{
			retval=IARM_Bus_Call(ownerName,methodName,(void*)&param_Set,sizeof(param_Set));
			switch(param_Set.newState)
			{
				case 0:	response["details"]="POWERSTATE_OFF";
					break;
				case 1:	response["details"]="POWERSTATE_STANDBY";
					break;
				case 2:	response["details"]="POWERSTATE_ON";
					break;
				default:
					response["details"]="Unknown State";			 			
			}
		}
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/
		response["result"]=getResult(retval,resultDetails);
		if(retval!=0)
		{
			response["details"]=resultDetails;
		}


	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		IARM_Bus_EventData_t  eventData;
		eventData.resrcType = (IARM_Bus_ResrcType_t)req["resource_type"].asInt();
		DEBUG_PRINT(DEBUG_LOG,"\n BUS-calling IARM_Bus_Call from IARM_Bus_Call \n");
		/*Calling IARMBUS API IARM_Bus_Call  */
		retval=IARM_Bus_Call(ownerName,methodName,(void*)&eventData,sizeof(eventData));
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/	
		response["result"]=getResult(retval,resultDetails);
		response["details"]=resultDetails;
	}
	else if(strcmp(ownerName,"MFRLib")==0)
	{
		char* mfrdetails=(char*)malloc(sizeof(char)*30);
		memset(mfrdetails , '\0', (sizeof(char)*30));
		DEBUG_PRINT(DEBUG_LOG,"\n MFR-calling IARM_Bus_Call from IARM_Bus_Call \n");
		/*Calling IARMBUS API IARM_Bus_Call  */
		char *pTmpStr;
		int len;
		IARM_Bus_MFRLib_GetSerializedData_Param_t param;	
		param.type = (mfrSerializedType_t)req["mfr_param_type"].asInt();
		retval=IARM_Bus_Call(ownerName,IARM_BUS_MFRLIB_API_GetSerializedData,(void*)&param, sizeof(param));
		len = param.bufLen + 1;
		pTmpStr = (char *)malloc(len);
		memset(pTmpStr,0,len);
		memcpy(pTmpStr,param.buffer,param.bufLen);
		DEBUG_PRINT(DEBUG_LOG,"\nValue:%s\n",pTmpStr);
		strcpy(mfrdetails,pTmpStr);
		free(pTmpStr);
		/*Checking the return value of API*/
		/*Filling json response with SUCCESS status*/
		response["result"]=getResult(retval,resultDetails);
		response["details"]=mfrdetails;


	}
        /*This is for testing the test app with bus call*/
        else if(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME)==0)
        {
		char *dummydata = (char*)malloc(sizeof(char*)*15);
		memset(dummydata , '\0', (sizeof(char)*15));
		char *dummydatadetails = (char*)malloc((sizeof(char*)*30));
		memset(dummydatadetails , '\0', (sizeof(char)*30));
		if(strcmp(methodName,"DummyAPI0")==0)
		{
			IARM_Bus_DUMMYMGR_DummyAPI0_Param_t param;
			param.i =req["testapp_API0_data"].asInt();
			retval = IARM_Bus_Call(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_API_DummyAPI0, &param, sizeof(param));
			sprintf(dummydata,"%x",param.iret);
			DEBUG_PRINT(DEBUG_LOG,"dummydata:%s",dummydata);
			strcpy(dummydatadetails,"DummyAPI0:");
			strcat(dummydatadetails,dummydata);
			DEBUG_PRINT(DEBUG_LOG,"dummydatadetails:%s",dummydatadetails);
			DEBUG_PRINT(DEBUG_ERROR,"\nret value of API-0:%x\n",param.iret);
			response["result"]="SUCCESS";
			response["details"]=dummydatadetails;
		}
		if(strcmp(methodName,"DummyAPI1")==0)
		{
			IARM_Bus_DUMMYMGR_DummyAPI1_Param_t param1;
			param1.j =req["testapp_API1_data"].asInt();
			retval = IARM_Bus_Call(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_API_DummyAPI1, &param1, sizeof(param1));
			sprintf(dummydata,"%x",param1.jret);
			DEBUG_PRINT(DEBUG_LOG,"dummydata:%s",dummydata);
			strcat(dummydatadetails,"DummyAPI1:");
			DEBUG_PRINT(DEBUG_LOG,"dummydatadetails:%s",dummydatadetails);
			strcat(dummydatadetails,dummydata);
			DEBUG_PRINT(DEBUG_ERROR,"\nret value of API-1:%x\n",param1.jret);
			response["result"]="SUCCESS";
			response["details"]=dummydatadetails;
		}
		free(dummydata);
		free(dummydatadetails);
        }

	free(resultDetails);
	free(RepeatInterval);
	DEBUG_PRINT(DEBUG_TRACE,"\n IARMBUSAgent_BusCall --->Exit \n");
	return TEST_SUCCESS;
	}
        else
        {
        response["result"]="FAILURE";
        response["details"]="Pre-Requisite check Failed for the given Owner";
        free(resultDetails);
        DEBUG_PRINT(DEBUG_ERROR,"\n IARMBUSAgent_BusCall -- Pre-Requisite check Failed for the given Owner \n");
        return TEST_FAILURE;
        }
}

/**************************************************************************
 * Function Name	: InvokeSecondApplication
 * Description	: This function is to invoke the second application which does broadcasting 
 different types of events,Requesting and releasing resources.

 ***************************************************************************/
bool IARMBUSAgent::InvokeSecondApplication(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n InvokeSecondApplication --->Entry \n");
        if (&req["appname"]==NULL)
        {
                return TEST_FAILURE;
        }
	const char* appname=(char*)req["appname"].asCString();
	pid_t idChild = vfork();
	std::string path;
	strcpy((char*)path.c_str(),getenv("TDK_PATH"));	
	strcat((char*)path.c_str(),"/");
	strcat((char*)path.c_str(),appname);
	DEBUG_PRINT(DEBUG_ERROR,"\nAppPath:%s\n",path.c_str());
	if(idChild == 0)
	{
		execl(path.c_str(),appname,(char*)NULL);
	}
	else if(idChild <0)
	{
		DEBUG_PRINT(DEBUG_LOG,"failed fork\n");
		response["result"]="second application Execution failed";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\n InvokeSecondApplication --->Exit \n");
	response["result"]="SUCCESS";
	return TEST_SUCCESS;

}
/**************************************************************************
 * Function Name	: CreateObject
 * Description	: This function will be used to create a new object for the
 *		  class "IARMBUSAgent".
 *
 **************************************************************************/

extern "C" IARMBUSAgent* CreateObject()
{
	return new IARMBUSAgent();
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will be used to clean the log details. 
 *
 **************************************************************************/

bool IARMBUSAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"IARMBUSAgent shutting down\n");
	if(ptrAgentObj==NULL)
	{
		return TEST_FAILURE;
	}
	/*unRegister stub function for callback*/
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_Init");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_Term");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_Connect");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_Disconnect");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_IsConnected");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_RequestResource");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_ReleaseResource");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_RegisterEventHandler");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_UnRegisterEventHandler");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_RegisterEvent");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_RegisterCall");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_BroadcastEvent");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_BusCall");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_GetLastReceivedEventDetails");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_InvokeSecondApplication");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUS_GetContext");
	return TEST_SUCCESS;
}


/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/
extern "C" void DestroyObject(IARMBUSAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG,"Destroying IARMBUS Agent object\n");
        delete stubobj;
}

