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

#include "TR069Agent.h"

/*************************************************************************
  Function name : TR069Agent::TR069Agent

Arguments     : NULL

Description   : Constructor for TR069Agent class
 ***************************************************************************/

TR069Agent::TR069Agent()
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent Initialized\n");
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string TR069Agent::testmodulepre_requisites()
{
	return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool TR069Agent::testmodulepost_requisites()
{
	return true;
}

/***************************************************************************
 *Function name : GetHostIP
 *Arguments	: interfaceName 
 *Descrption    : Returns the ip address for the interface name passed as argument.
 *                
 *****************************************************************************/
std::string GetHostIP (const char* szInterface)
{
	struct ifaddrs* pIfAddrStruct = NULL;
	struct ifaddrs* pIfAddrIterator = NULL;
	void* pvTmpAddrPtr = NULL;
	char szAddressBuffer [INET_ADDRSTRLEN];
	getifaddrs (&pIfAddrStruct);

	for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next)
	{
		if (pIfAddrIterator->ifa_addr->sa_family == AF_INET)
		{
			// check it is a valid IP4 Address
			pvTmpAddrPtr = & ( (struct sockaddr_in *)pIfAddrIterator->ifa_addr )-> sin_addr;
			inet_ntop (AF_INET, pvTmpAddrPtr, szAddressBuffer, INET_ADDRSTRLEN);

			if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
			{
				break;
			}
		}
	}

	DEBUG_PRINT(DEBUG_TRACE, "Found IP: %s\n",szAddressBuffer);

	if (pIfAddrStruct != NULL)
	{
		freeifaddrs (pIfAddrStruct);
	}

	return szAddressBuffer;

} /* End of GetHostIP */


/**************************************************************************
Function name : TR069Agent::initialize

Arguments     : Input arguments are Version string and TR069Agent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool TR069Agent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent Initialize----->Entry\n");

	ptrAgentObj->RegisterMethod(*this,&TR069Agent::TR069Agent_GetParameterValue, "TestMgr_GetParameterValue");
	ptrAgentObj->RegisterMethod(*this,&TR069Agent::TR069Agent_VerifyParameterValue, "TestMgr_VerifyParameterValue");

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent Initialize----->Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : TR069Agent::TR069Agent_GetParameterValue

Arguments     : Input arguments are json request object and json response object

Description   : This method queries for the parameter requested through curl and returns the value.
***************************************************************************/
bool TR069Agent::TR069Agent_GetParameterValue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_GetParameterValue -->Entry\n");

	string profilePath = req["path"].asCString();	
	FILE *fp = NULL;
	char readRespBuff[BUFF_LENGTH];

	DEBUG_PRINT(DEBUG_TRACE, "Requesting Parameter Value is: %s\n",profilePath.c_str());

	/*Frame the command  */
	string path = CMD;
	path.append(profilePath);
	path.append(HTTP);

	DEBUG_PRINT(DEBUG_TRACE, "Curl Request Framed: %s\n",path.c_str());

	fp = popen(path.c_str(),"r");

	/*Check for popen failure*/	
	if(fp == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "popen() failure";
		DEBUG_PRINT(DEBUG_ERROR, "popen() failure\n");

		return TEST_FAILURE;
	}

	/*copy the response to a buffer */
	while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
	{
		DEBUG_PRINT(DEBUG_TRACE, "Curl Response:\n");
		cout<<readRespBuff<<endl;
	}

	pclose(fp);	

	/*Check for the failure case, if curl request fails  */
	if(NULL != (strcasestr(readRespBuff,"curl:")))
	{
		string curlResp(readRespBuff);
		response["result"] = "FAILURE";
		response["details"] = curlResp;
		DEBUG_PRINT(DEBUG_ERROR, "Curl Error: %s\n",curlResp.c_str());

		return TEST_FAILURE;
	}
	
	string respResult(readRespBuff);
	DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
	int pos = respResult.find("\"value\":");
	string valueString,finalString;

	if (pos != -1)
	{
		valueString = respResult.substr(pos+8);
		finalString = valueString.substr(0,valueString.length()-3);

		DEBUG_PRINT(DEBUG_LOG, "Final Value: %s\n",finalString.c_str());

		response["result"] = "SUCCESS";
		response["details"] = finalString;
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Empty No Response";

		DEBUG_PRINT(DEBUG_ERROR, "Empty No Response\n");
	}


	DEBUG_PRINT(DEBUG_LOG, "Execution success\n");

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_GetParameterValue -->Exit\n");
	return TEST_SUCCESS;

}


/**************************************************************************
Function name : TR069Agent::TR069Agent_VerifyParameterValue

Arguments     : Input arguments are json request object and json response object

Description   : This method verifies the value for the parameter name and returns SUCCESS or FAILURE. 
***************************************************************************/
bool TR069Agent::TR069Agent_VerifyParameterValue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_VerifyParameterValue -->Entry\n");

	string profilePath = req["path"].asCString();

	if (profilePath ==  "Device.IP.ActivePortNumberOfEntries")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		int noOfActivePorts = 0;

		fp = popen(GET_NUM_OF_ACTIVE_PORTS,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return TEST_FAILURE;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%d",&noOfActivePorts);
		}

		string activePorts = req["paramValue"].asCString();
		int value = atoi(activePorts.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "NumberOfActiveports: %d\n",noOfActivePorts);

		if (value == noOfActivePorts)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}

		pclose(fp);
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_FirmwareFilename")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		char imageName[128] = {'\0'};

		fp = popen(GET_IMAGE_VERSION,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return TEST_FAILURE;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%s",imageName);
		}

		pclose(fp);

		string firmwareName(imageName);
		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and FirmwareName: %s\n",value.c_str(),firmwareName.c_str());

		if(value == firmwareName)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.MemoryStatus.Total")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		unsigned int freeMemory = (unsigned int)(sys_info.totalram *(unsigned long long)sys_info.mem_unit / 1024);
		string freeValue = req["paramValue"].asCString();
		unsigned int value = atoi(freeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and TotalMemory: %d\n",value,freeMemory);

		if(freeMemory == value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.MemoryStatus.Free")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		unsigned int freeMemory = (unsigned int)(sys_info.freeram *(unsigned long long)sys_info.mem_unit / 1024);
		string freeValue = req["paramValue"].asCString();
		unsigned int value = atoi(freeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and freeMemory: %d\n",value,freeMemory);

		if(freeMemory >= value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.Processor.1.Architecture")
	{
		struct utsname  utsName;
		uname(&utsName);

		string architecture(utsName.machine);

		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and Processor Architecture: %s\n",value.c_str(),architecture.c_str());

		if(value == architecture)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.IP.InterfaceNumberOfEntries")
	{
		struct if_nameindex *ifname = NULL, *ifnp = NULL;
		int noOfIPInterfaces = 0;

		//retrieve the current interfaces
		if ((ifname = if_nameindex()) == NULL)
		{
			response["result"] = "FAILURE";
			response["details"] = "if_name index error";

			DEBUG_PRINT(DEBUG_ERROR, "if_name index error\n");

			return TEST_FAILURE;
		}

		for (ifnp = ifname; ifnp->if_index != 0; ifnp++)
		{
			noOfIPInterfaces++;
		}

		if (ifname)
		{
			if_freenameindex(ifname); /* free the dynamic memory */
			ifname = NULL;            /* prevent use after free  */
		}

		string num = req["paramValue"].asCString();
		int value = atoi(num.c_str());
		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and Number of IP Interfaces: %d\n",value,noOfIPInterfaces);

		if(value == noOfIPInterfaces)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if((profilePath == "Device.IP.IPv4Enable") || (profilePath == "Device.IP.IPv4Status" ))
	{

		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		int numIf = 0;

		fp = popen(GET_IPV4_ENABLE_STATUS,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return TEST_FAILURE;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%d",&numIf);
		}

		pclose(fp);

		string num = req["paramValue"].asCString();

		if (numIf == 0)
		{
			if (profilePath == "Device.IP.IPv4Enable")
			{

				if (num == "false")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}	
			}

			if (profilePath == "Device.IP.IPv4Status")
			{
				if (num == "Disabled")	
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}
		}
		else
		{
			if (profilePath == "Device.IP.IPv4Enable")
			{
				if (num == "true")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}

			if (profilePath == "Device.IP.IPv4Status")
			{
				if (num == "Enabled")
				{
					response["result"] = "SUCCESS";
					response["details"] = "Verification Success";

					DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "Verification Failure";

					DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
				}
			}

		}
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_STB_IP")
	{
		string value = req["paramValue"].asCString();
		string ip = GetHostIP("eth1");	

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and IPAddress: %s\n",value.c_str(),ip.c_str());

		if(value == ip)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.X_COMCAST-COM_STB_MAC")
	{
		FILE *fp = NULL;
		char resultBuff[256] = {'\0'};
		char macAddr[128] = {'\0'};

		fp = popen(GET_STB_MAC,"r");

		if(fp == NULL)
		{
			DEBUG_PRINT(DEBUG_ERROR, "popen failed\n");

			response["result"] = "FAILURE";
			response["details"] = "popen failed";

			return TEST_FAILURE;
		}

		if(fgets(resultBuff, sizeof(resultBuff), fp)!=NULL)
		{
			sscanf(resultBuff,"%s",macAddr);
		}

		pclose(fp);

		string macAddre(macAddr);
		string value = req["paramValue"].asCString();

		DEBUG_PRINT(DEBUG_TRACE, "Value: %s and MACAddress: %s\n",value.c_str(),macAddre.c_str());

		if(value == macAddre)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else if(profilePath == "Device.DeviceInfo.UpTime")
	{
		struct sysinfo sys_info;

		sysinfo (&sys_info);
		int time = (int) sys_info.uptime;
		string timeValue = req["paramValue"].asCString();
		int value = atoi(timeValue.c_str());

		DEBUG_PRINT(DEBUG_TRACE, "Value: %d and upTime: %d\n",value,time);

		if(time == value)
		{
			response["result"] = "SUCCESS";
			response["details"] = "Verification Success";

			DEBUG_PRINT(DEBUG_LOG, "Verification Success\n");

		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Verification Failure";

			DEBUG_PRINT(DEBUG_ERROR, "Verification Failure\n");
		}
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Verification Failure";

		DEBUG_PRINT(DEBUG_LOG, "Profile Path not supported\n");
	}

	DEBUG_PRINT(DEBUG_TRACE, "TR069Agent_VerifyParameterValue -->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "TR069Agent".
 **************************************************************************/

extern "C" TR069Agent* CreateObject()
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating TR069 Agent Object\n");

	return new TR069Agent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool TR069Agent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");

	if(NULL == ptrAgentObj)
	{
		return TEST_FAILURE;
	}

	ptrAgentObj->UnregisterMethod("TestMgr_GetParameterValue");
	ptrAgentObj->UnregisterMethod("TestMgr_VerifyParameterValue");

	DEBUG_PRINT(DEBUG_TRACE, "cleaningup done\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is TR069Agent Object

Description   : This function will be used to destory the TR069Agent object.
 **************************************************************************/
extern "C" void DestroyObject(TR069Agent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying TR069Agent object\n");
	delete stubobj;
}
