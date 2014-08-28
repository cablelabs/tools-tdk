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

#include "gstPluginsRdkAgent.h"

/*************************************************************************
Function name : gstPluginsRdkAgent::gstPluginsRdkAgent()

Arguments     : NULL

Description   : Constructor for gstPluginsRdkAgent class
 ***************************************************************************/
gstPluginsRdkAgent::gstPluginsRdkAgent()
{
	DEBUG_PRINT(DEBUG_LOG, "gstPluginsRdkAgent Initialized.\n");
}
/**************************************************************************
Function name : gstPluginsRdkAgent::testmodulepre_requisites

Arguments     : None

Description   : Setting Pre-requisites needed to execute gstPluginsRdkAgent tests

***************************************************************************/
std::string gstPluginsRdkAgent::testmodulepre_requisites()
{
        return "SUCCESS";
}
/**************************************************************************
Function name : gstPluginsRdkAgent::testmodulepost_requisites

Arguments     : None

Description   : Setting post-requisites needed to execute gstPluginsRdkAgent tests

***************************************************************************/
bool gstPluginsRdkAgent::testmodulepost_requisites()
{
        return true;
}


/**************************************************************************
Function name : readGstCheckLog

Arguments     : None

Description   : Helper function to read the result of gstcheck from log file.

***************************************************************************/
int readGstCheckLog(OUT Json::Value& response)
{

	ifstream inFile;
	int numOfLines = 0;
	string line,data;

	inFile.open("gstCheckLog");
	/*Read the lines from the file and decide SUCCESS or FAILURE*/
	while (getline(inFile,line))	
	{
		numOfLines++;
		if(numOfLines == 2)
		{
			data = line;
			DEBUG_PRINT(DEBUG_TRACE, "Content in loop: %s\n",data.c_str());
		}
	}
		
	DEBUG_PRINT(DEBUG_TRACE, "Number of Lines: %d\n",numOfLines);
	DEBUG_PRINT(DEBUG_TRACE, "Content: %s\n",data.c_str());
	
	/*Number of lines equal to 0. Then, gstcheck failed to run. */
	if(numOfLines == 0)
	{
		DEBUG_PRINT(DEBUG_LOG, "gst-check failed to run\n");
		response["result"] = "FAILURE";
		response["details"] = "gst-check failed to run";
	
		return TEST_FAILURE;
	}
	/*Number of lines equal to 1. Then, setting the property Succcess. */
	else if(numOfLines == 1)	
	{
		DEBUG_PRINT(DEBUG_LOG, "Setting the property SUCCESS\n");
		response["result"] = "SUCCESS";
		response["details"] = "Get/Set property SUCCESS";
	
		return TEST_SUCCESS;
	}
	/*Number of lines is more than 1. Then, Failure send the error messages to TM. */
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Setting the property FAILED\n");
		response["result"] = "FAILURE";
		response["details"] = data;

		return TEST_FAILURE;
	}

	inFile.close();	

	return 0;
}

/**************************************************************************
Function name : gstPluginsRdkAgent::initialize

Arguments     : Input arguments are Version string and gstPluginsRdkAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/
bool gstPluginsRdkAgent::initialize (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent Initialize----->Entry\n");
	
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Aesdecrypt_SetProp_DecryptionEnable, "TestMgr_Aesdecrypt_DecryptEnable_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Aesdecrypt_GetProp_DecryptionEnable, "TestMgr_Aesdecrypt_DecryptEnable_Get_Prop");

	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Aesencrypt_SetProp_EncryptionEnable, "TestMgr_Aesencrypt_EncryptEnable_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Aesencrypt_GetProp_EncryptionEnable, "TestMgr_Aesencrypt_EncryptEnable_Get_Prop");

	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_RecordId, "TestMgr_Dvrsrc_RecordId_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_RecordId, "TestMgr_Dvrsrc_RecordId_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_Segmentname, "TestMgr_Dvrsrc_SegmentName_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Segmentname, "TestMgr_Dvrsrc_SegmentName_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Ccivalue, "TestMgr_Dvrsrc_Ccivalue_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_Rate, "TestMgr_Dvrsrc_Rate_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Rate, "TestMgr_Dvrsrc_Rate_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_StartTime, "TestMgr_Dvrsrc_StartTime_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Duration, "TestMgr_Dvrsrc_Duration_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_PlayStartPosition, "TestMgr_Dvrsrc_PlayStartPosition_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_PlayStartPosition, "TestMgr_Dvrsrc_PlayStartPosition_Get_Prop");

	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_SetProp_RecordId, "TestMgr_Dvrsink_RecordId_Set_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_GetProp_RecordId, "TestMgr_Dvrsink_RecordId_Get_Prop");
	ptrAgentObj->RegisterMethod(*this,&gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_GetProp_Ccivalue, "TestMgr_Dvrsink_Ccivalue_Get_Prop");


        return TEST_SUCCESS;
}


bool gstPluginsRdkAgent::gstPluginsRdkAgent_Aesdecrypt_SetProp_DecryptionEnable(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesdecrypt_SetProp_DecryptionEnable ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_decryption_enable_prop_set ";	
	int setAesdecryptProp = req["propValue"].asInt();
	oss << setAesdecryptProp;
	string propValue = oss.str();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesdecrypt_SetProp_DecryptionEnable ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Aesdecrypt_GetProp_DecryptionEnable(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesdecrypt_GetProp_DecryptionEnable ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_decryption_enable_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesdecrypt_GetProp_DecryptionEnable ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Aesencrypt_SetProp_EncryptionEnable(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesencrypt_SetProp_EncryptionEnable ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_encryption_enable_prop_set ";	
	int setAesencryptProp = req["propValue"].asInt();
	oss << setAesencryptProp;
	string propValue = oss.str();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesencrypt_SetProp_EncryptionEnable ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Aesencrypt_GetProp_EncryptionEnable(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesencrypt_GetProp_EncryptionEnable ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_encryption_enable_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Aesencrypt_GetProp_EncryptionEnable ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_RecordId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_RecordId ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_recordid_prop_set ";	
	string propValue = req["propValue"].asString();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_RecordId ----->Exit\n");

        return TEST_SUCCESS;
}


bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_RecordId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_RecordId ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_recordid_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Recordid ----->Exit\n");

        return TEST_SUCCESS;
}


bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_Segmentname(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_Segmentname ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_segmentname_prop_set ";	
	int setSegmentNameProp = req["propValue"].asInt();
	oss << setSegmentNameProp;
	string propValue = oss.str();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_Segmentname ----->Exit\n");

        return TEST_SUCCESS;
}


bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Segmentname(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Segmentname ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_segmentname_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Segmentname ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Ccivalue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Ccivalue ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_ccivalue_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Ccivalue ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_Rate(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_Rate ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_rate_prop_set ";	
	float setRateProp = req["propValue"].asFloat();
	oss << setRateProp;
	string propValue = oss.str();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_Rate ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Rate(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Rate ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_rate_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Rate ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_StartTime(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_StartTime ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_starttime_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_StartTime ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_Duration(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Duration ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_duration_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_Duration ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_SetProp_PlayStartPosition(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_PlayStartPosition ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_playstartposition_prop_set ";	
	float setStartPosProp = req["propValue"].asFloat();
	oss << setStartPosProp;
	string propValue = oss.str();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_SetProp_PlayStartPosition ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsrc_GetProp_PlayStartPosition(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_PlayStartPosition ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsrc_playstartposition_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsrc_GetProp_PlayStartPosition ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_SetProp_RecordId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_SetProp_RecordId ----->Entry\n");
	ostringstream oss;	
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsink_recordid_prop_set ";	
	string propValue = req["propValue"].asString();
	cmd.append(propValue); 
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_SetProp_RecordId ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_GetProp_RecordId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_GetProp_RecordId ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsink_recordid_prop_get ";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_GetProp_Recordid ----->Exit\n");

        return TEST_SUCCESS;
}

bool gstPluginsRdkAgent::gstPluginsRdkAgent_Dvrsink_GetProp_Ccivalue(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_GetProp_Ccivalue ----->Entry\n");
	
	string searchPattern = SEARCH_PATTERN;
	string cmd = "/opt/TDK/gstpluginsrdkcheck test_dvrsink_ccivalue_prop_get";	
	cmd.append(searchPattern);

	DEBUG_PRINT(DEBUG_TRACE,"The Complete Cmd: %s \n",cmd.c_str());
#if 1	
	if (-1 == system(cmd.c_str()))
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error on exceuting gstcheck\n");
		response["result"] = "FAILURE";
		response["deatils"] = "Error on exceuting gstcheck";

		return TEST_FAILURE;
	}
	sleep(2);
#endif
	readGstCheckLog(response);

	DEBUG_PRINT(DEBUG_TRACE, "gstPluginsRdkAgent_Dvrsink_GetProp_Ccivalue ----->Exit\n");

        return TEST_SUCCESS;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "gstPluginsRdkAgent".
**************************************************************************/
extern "C" gstPluginsRdkAgent* CreateObject ()
{
	return new gstPluginsRdkAgent();
}


/**************************************************************************
  Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool gstPluginsRdkAgent::cleanup (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_ERROR, "cleaningup\n");

	
	if(NULL == ptrAgentObj)
	{
		return TEST_FAILURE;
	}

	ptrAgentObj->UnregisterMethod("TestMgr_Aesdecrypt_DecryptEnable_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Aesdecrypt_DecryptEnable_Get_Prop");

	ptrAgentObj->UnregisterMethod("TestMgr_Aesencrypt_EncryptEnable_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Aesencrypt_EncryptEnable_Get_Prop");

	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_RecordId_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_RecordId_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_SegmentName_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_SegmentName_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_Ccivalue_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_Rate_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_Rate_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_StartTime_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_Duration_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_PlayStartPosition_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsrc_PlayStartPosition_Get_Prop");

	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsink_RecordId_Set_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsink_RecordId_Get_Prop");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvrsink_Ccivalue_Get_Prop");

	return TEST_SUCCESS;
}
	
/**************************************************************************
  Function Name : DestroyObject

Arguments     : Input argument is gstPluginsRdkAgent Object

Description   : This function will be used to destory the gstPluginsRdkAgent object.
 **************************************************************************/
extern "C" void DestroyObject (gstPluginsRdkAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_LOG, "Destroying gstPluginsRdk stub object\n");
	delete stubobj;

}


// End of file gstPluginsRdkAgent.cpp.
