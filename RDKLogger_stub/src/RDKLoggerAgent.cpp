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

#include "RDKLoggerAgent.h"
#include "rdk_debug.h"
#include "rdk_utils.h"

using namespace std;

/**
 * Converts a log level name to the correspodning log level enum value.
 *
 * @param name Log level name, which must be uppercase.
 * @param Corresponding enumeration value or -1 on error.
 */
static int logNameToEnum(const char *name)
{
    int i = 0;
    while (i < ENUM_RDK_LOG_COUNT)
    {
        if (strcmp(name, rdk_logLevelStrings[i]) == 0)
        {
            return i;
        }
        i++;
    }

    return -1;
}

/**
 * Checks if a particular log is enabled for a module.
 *
 * @param module Module in which this message belongs to.
 * @param level  Log level of the log message Log level of the log message supported for a module
 * @return     	 1 if log level is supported for a module
 *		 0 if log level is not supported for a module
 *		 -1 on error.
 */
int dbgFinder( const char *module, const char *level)
{
    int 	find_result = 0;
    const int 	line_buf_len = 256;
    char 	lineBuffer[line_buf_len];
    FILE	*f;

    /* Open the env file */
    if ((f = fopen( DEBUG_CONF_FILE,"r")) == NULL)
    {
        printf("** TDK ERROR!  Could not open configuration file!    **\n");
        return -1;
    }
    printf("%s: Conf file %s open success\n", __FUNCTION__, DEBUG_CONF_FILE);    

    /* Read each line of the file */
    while (fgets(lineBuffer,line_buf_len,f) != NULL)
    {
        /* Ignore comment lines */
        if (lineBuffer[0] == '#')
            	continue;
	/* Check if module name and log level is present */
	if(((strstr(lineBuffer, module)) != NULL) && ((strstr(lineBuffer, level)) != NULL)) {
		find_result++;
		break;
	}
    }
	
    if(f) {
	fclose(f);
    }

    return find_result;
}


/*************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent

Arguments     : NULL

Description   : Constructor for RDKLoggerAgent class
***************************************************************************/

RDKLoggerAgent::RDKLoggerAgent()
{
        DEBUG_PRINT(DEBUG_LOG, "RDKLoggerAgent Initialized\n");
}

/**************************************************************************
Function name : RDKLoggerAgent::initialize

Arguments     : Input arguments are Version string and RDKLoggerAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool RDKLoggerAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
        DEBUG_PRINT(DEBUG_ERROR, "RDKLoggerAgent Initialization\n");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_Init, "TestMgr_RDKLogger_Init");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_Log, "TestMgr_RDKLogger_Log");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status, "TestMgr_RDKLogger_Dbg_Enabled_Status");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_EnvGet, "TestMgr_RDKLogger_EnvGet");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_EnvGetNum, "TestMgr_RDKLogger_EnvGetNum");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum, "TestMgr_RDKLogger_EnvGetValueFromNum");
	ptrAgentObj->RegisterMethod(*this,&RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum, "TestMgr_RDKLogger_EnvGetModFromNum");

        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string RDKLoggerAgent::testmodulepre_requisites()
{
        return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool RDKLoggerAgent::testmodulepost_requisites()
{
        return TEST_SUCCESS;
}


/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Init

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to initialize RDK debug manager module.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init --->Entry\n");

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init -->Exit\n");
                return TEST_FAILURE;
        }

      	response["result"] = "SUCCESS";
	response["details"] = "rdk logger init success";
     	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Init -->Exit\n");
       	return TEST_SUCCESS;
}


/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Log

Arguments     : Input argument is "module", "level". 
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to add a log message.
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/

bool RDKLoggerAgent::RDKLoggerAgent_Log(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log --->Entry\n");

        int logLevel = -1;
        char rdkMod[20] = {'\0'};

        string module = req["module"].asString();
        string level = req["level"].asString();

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log -->Exit\n");
                return TEST_FAILURE;
        }

        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());
        logLevel = logNameToEnum(level.c_str());

	DEBUG_PRINT(DEBUG_TRACE, "Module: %s Level: %s Message: %s\n", rdkMod, level.c_str(), "Test Message from RDKLoggerAgent");
	RDK_LOG ( (rdk_LogLevel) logLevel, rdkMod, "Test Message from RDKLoggerAgent\n" );

	response["result"] = "SUCCESS";
	response["details"] = "rdk logging success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Log -->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status

Arguments     : Input argument is "module" and "level". 
		Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check if a specified log level 
		of a module is enabled.
                Gets the response from RDKLogger element and send it to the Test Manager. 
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_Dbg_Enabled_Status(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status --->Entry\n");

	int logLevel = -1;
	char rdkMod[20] = {'\0'};
	char stringDetails[10] = {'\0'};

	string module = req["module"].asString();
	string level = req["level"].asString();

	rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
		DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
        	response["result"] = "FAILURE";
        	response["details"] = "Failed to init rdk logger";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status -->Exit\n");
		return TEST_FAILURE;
        }

        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());
        logLevel = logNameToEnum(level.c_str());
	
	bool rdkStatus = rdk_dbg_enabled( rdkMod, (rdk_LogLevel)logLevel);
	bool dbgFindStatus = dbgFinder( rdkMod, level.c_str());

        if (dbgFindStatus == rdkStatus)
        {
        	if (TRUE == rdkStatus)
		{
                	DEBUG_PRINT(DEBUG_TRACE, "%s %s Enabled.\n", rdkMod, level.c_str());
			snprintf(stringDetails, strlen("Enabled") + 1, "%s", "Enabled");
		}
		else
		{
			DEBUG_PRINT(DEBUG_TRACE, "%s %s Disabled.\n", rdkMod, level.c_str());
			snprintf(stringDetails, strlen("Disabled") + 1, "%s", "Disabled");
		}
		response["result"] = "SUCCESS";
		response["details"] = stringDetails;
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status -->Exit\n");
		return TEST_SUCCESS;
        }

	DEBUG_PRINT(DEBUG_TRACE, "Failed to get %s %s log status\n", rdkMod, level.c_str()); 
	DEBUG_PRINT(DEBUG_TRACE, "rdk_dbg_enabled result = %d dbgFinder result = %d\n", rdkStatus, dbgFindStatus);
	response["result"] = "FAILURE";
	response["details"] = "Failed to get dbg enable status";

	DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_Dbg_Enabled_Status -->Exit\n");
	return TEST_FAILURE;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGet

Arguments     : Input argument is "module". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the logging level value of the 
		specified environment variable
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_EnvGet(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet --->Entry\n");

        char rdkMod[20] = {'\0'};
        char stringDetails[256] = {'\0'};
        const char* envVar = NULL;

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet -->Exit\n");
                return TEST_FAILURE;
        }

        string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

        envVar = rdk_logger_envGet(rdkMod);
        if ((envVar != NULL) && (envVar[0] != 0))
        {
                DEBUG_PRINT(DEBUG_TRACE, "%s logging levels: %s\n", rdkMod, envVar);
                snprintf(stringDetails, strlen(envVar) + 1, "%s", envVar);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "%s logging disabled!\n", rdkMod);
		response["result"] = "FAILURE";
                response["details"] = "Logging disabled for module";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet -->Exit\n");
                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
	response["details"] = "rdk logger env get success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGet -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetNum

Arguments     : Input argument is "module". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the registered number of the
                specified environment variable
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_EnvGetNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum --->Entry\n");

        char rdkMod[20] = {'\0'};
	char stringDetails[5] = {'\0'};
	int modNum = -1;

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum -->Exit\n");
                return TEST_FAILURE;
        }

	string module = req["module"].asString();
        sprintf(rdkMod, "LOG.RDK.%s", module.c_str());

    	modNum = rdk_logger_envGetNum(rdkMod);
	DEBUG_PRINT(DEBUG_TRACE, "Module: %s Module number = %d\n", rdkMod, modNum);
    	if (modNum < 0)
    	{
                response["result"] = "FAILURE";
                response["details"] = "Unknown module specified";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum -->Exit\n");
                return TEST_FAILURE;
    	}

      	sprintf(stringDetails, "%d", modNum);
      	response["details"] = stringDetails;

        response["result"] = "SUCCESS";
	response["details"] = "rdk logger env get num success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetNum -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum

Arguments     : Input argument is "number". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the logging level value of the 
		specified environment variable based on its registered number
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_EnvGetValueFromNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum --->Entry\n");

        char stringDetails[256] = {'\0'};
        const char *envVarValue = NULL;
        int modNum = -1;

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum -->Exit\n");
                return TEST_FAILURE;
        }

        /** Get the logging level from registered number **/
	modNum = req["number"].asInt();
        envVarValue = rdk_logger_envGetValueFromNum(modNum);
        if ((envVarValue != NULL) && (envVarValue[0] != '\0'))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Registered Number = %d, Logging level value = %s\n", modNum, envVarValue);
                snprintf(stringDetails, strlen(envVarValue) + 1, "%s", envVarValue);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "No logging level value for number = %d\n", modNum);
		response["result"] = "FAILURE";
		response["details"] = "No logging level value for number";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum -->Exit\n");
		return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
	response["details"] = "rdk logger env get value from num success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetValueFromNum -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum

Arguments     : Input argument is "number". Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the module name of the
                specified environment variable based on its registered number
                Gets the response from RDKLogger element and send it to the Test Manager.
**************************************************************************/
bool RDKLoggerAgent::RDKLoggerAgent_EnvGetModFromNum(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum --->Entry\n");

        char stringDetails[50] = {'\0'};
        int modNum = -1;
	const char *envMod = NULL;

        rdk_Error ret = rdk_logger_init(DEBUG_CONF_FILE);
        if ( RDK_SUCCESS != ret)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Failed to init rdk logger. err = %d\n", ret);
                response["result"] = "FAILURE";
                response["details"] = "Failed to init rdk logger";
                DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum -->Exit\n");
                return TEST_FAILURE;
        }

	modNum = req["number"].asInt();
        envMod = rdk_logger_envGetModFromNum(modNum);
        if ((envMod != NULL) && (envMod[0] != '\0'))
        {
                DEBUG_PRINT(DEBUG_TRACE, "Registered Number = %d, Module = %s\n", modNum, envMod);
                snprintf(stringDetails, strlen(envMod) + 1, "%s", envMod);
                response["details"] = stringDetails;
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "No module for number(%d)\n", modNum);
		response["result"] = "FAILURE";
		response["details"] = "No module for number";
		DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum -->Exit\n");
		return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
	response["details"] = "rdk logger env get mod from num success";
        DEBUG_PRINT(DEBUG_TRACE, "RDKLoggerAgent_EnvGetModFromNum -->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "RDKLoggerAgent".
**************************************************************************/

extern "C" RDKLoggerAgent* CreateObject()
{
        return new RDKLoggerAgent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool RDKLoggerAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
        DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
        if(NULL == ptrAgentObj)
        {
                return TEST_FAILURE;
        }
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_Init");
 	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_Log");
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_Dbg_Enabled_Status");
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_EnvGet");
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_EnvGetNum");
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_EnvGetValueFromNum");
	ptrAgentObj->UnregisterMethod("TestMgr_RDKLogger_EnvGetModFromNum");

        return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is RDKLoggerAgent Object

Description   : This function will be used to destory the RDKLoggerAgent object.
**************************************************************************/
extern "C" void DestroyObject(RDKLoggerAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying RDKLogger Agent object\n");
        delete stubobj;
}

