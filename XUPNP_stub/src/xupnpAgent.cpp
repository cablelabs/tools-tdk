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

#include "xupnpAgent.h"
#include <string.h>
#include <fstream>

#ifdef __cplusplus
extern "C" {
#include "xdiscovery.h"
#include "libIBus.h"
#include "libIARMCore.h"
#include "sysMgr.h"
}
#endif

string g_tdkPath = getenv("TDK_PATH");
static bool wareHouseModeEnabled = false;

bool readLogFile(const char *filename, const string parameter)
{
    string line;
    ifstream logFile(filename);
    if(logFile.is_open())
    {
        while(logFile.good())
        {
            getline(logFile,line);
            if (line.find(parameter) != string::npos)
            {
                DEBUG_PRINT(DEBUG_LOG,"Parameter found: %s\n",line.c_str());
                logFile.close();
                return true;
            }
        }
        logFile.close();
        DEBUG_PRINT(DEBUG_ERROR,"Error! No Log found for parameter %s\n", parameter.c_str());
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Unable to open file %s\n", filename);
    }
    return false;
}

bool enableWareHouseMode(const char *filename)
{
    bool ret = false;
    char strCmd[128] = {'\0'};
    string localConfFile = g_tdkPath + "/" + TDK_XDEVICE_CONF_FILE;

    //Create temp conf file
    sprintf(strCmd,"sed -e '/\\[Flags\\]/a\\wareHouseMode=true' %s > %s",filename, localConfFile.c_str());
    if (-1 != system(strCmd)) {
        DEBUG_PRINT(DEBUG_TRACE,"Successfully created temp file %s\n",localConfFile.c_str());
        memset(strCmd,'\0',sizeof(strCmd));
        sprintf(strCmd,"mv %s %s",localConfFile.c_str(),filename);
        if (-1 != system(strCmd)) {
            DEBUG_PRINT(DEBUG_TRACE,"Successfully modified %s\n",filename);
            ret = true;
        }
        else {
            DEBUG_PRINT(DEBUG_ERROR,"Failed to modify %s\n",filename);
        }
    }
    else {
        DEBUG_PRINT(DEBUG_ERROR,"Failed to create temp file %s\n",localConfFile.c_str());
    }

    return ret;
}

/*************************************************************************
Function name : XUPNPAgent::XUPNPAgent

Arguments     : NULL

Description   : Constructor for XUPNPAgent class
***************************************************************************/

XUPNPAgent::XUPNPAgent()
{
    DEBUG_PRINT(DEBUG_LOG, "XUPNPAgent Initialized\n");
}

/**************************************************************************
Function name : XUPNPAgent::initialize

Arguments     : Input arguments are Version string and XUPNPAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool XUPNPAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent Initialization Entry\n");

    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_GetUpnpResult, "TestMgr_XUPNP_GetUpnpResult");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_ReadXDiscOutputFile, "TestMgr_XUPNP_ReadXDiscOutputFile");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_CheckXDiscOutputFile, "TestMgr_XUPNP_CheckXDiscOutputFile");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_ModifyBasicDeviceXml, "TestMgr_XUPNP_ModifyBasicDeviceXml");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_CheckXMLRestoration, "TestMgr_XUPNP_CheckXMLRestoration");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_ReadXcalDeviceLogFile, "TestMgr_XUPNP_ReadXcalDeviceLogFile");
    ptrAgentObj->RegisterMethod(*this,&XUPNPAgent::XUPNPAgent_BroadcastEvent, "TestMgr_XUPNP_BroadcastEvent");

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent Initialization Exit\n");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                Checks that xdiscovery process is running in the system
 *****************************************************************************/

std::string XUPNPAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule pre_requisites --> Entry\n");

    if (-1 != system("pidstat | grep xdiscovery")) {
        DEBUG_PRINT(DEBUG_TRACE, "%s process is running\n",XDISCOVERY);
    }
    else {
        DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule pre_requisites --> Exit\n");
        return "FAILURE:xdiscovery process is not running";
    }

    if (!wareHouseModeEnabled) {
        //Set wareHouseMode flag in xdevice.conf / xdevice_hybrid.conf
        bool xDevCnf = enableWareHouseMode(XCALDEVCONFIG);
        bool xDevHybCnf = enableWareHouseMode(XCALDEVHYBCONFIG);

        if (xDevCnf || xDevHybCnf) {
            DEBUG_PRINT(DEBUG_TRACE, "Re-starting xupnp script after xdevice conf modification\n");
            system(STARTUPCMD);
            sleep(5);
        }
        else if(!xDevCnf && !xDevHybCnf) {
            DEBUG_PRINT(DEBUG_TRACE, "IP Client Box. Not enabling wareHouseMode\n");
        }
        wareHouseModeEnabled = true;
        DEBUG_PRINT(DEBUG_TRACE, "WareHouseMode Enabled\n");
    }
    else {
        DEBUG_PRINT(DEBUG_TRACE, "WareHouseMode already enabled\n");
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNP testmodule pre_requisites --> Exit\n");
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool XUPNPAgent::testmodulepost_requisites()
{
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_GetUpnpResult

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the basestreamingurl is present in the json message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_GetUpnpResult(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_GetUpnpResult --->Entry\n");

    string parameter = req["paramName"].asString();
    IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
    IARM_Bus_SYSMGR_GetXUPNPDeviceInfo_Param_t *param = NULL;

    //Allocate enough to store the structure, the message and one more byte for the string terminator
    iarmResult = IARM_Malloc(IARM_MEMTYPE_PROCESSLOCAL,
                             sizeof(IARM_Bus_SYSMGR_GetXUPNPDeviceInfo_Param_t) + MAX_DATA_LEN + 1,
                             (void**)&param);

    if(iarmResult != IARM_RESULT_SUCCESS)
    {
        DEBUG_PRINT(DEBUG_ERROR, "Error allocating shared mem for gw device data\n");
        response["result"] = "FAILURE";
        response["details"] = "Error allocating shared mem for data";
    }
    else
    {
        param->bufLength = MAX_DATA_LEN;

        iarmResult = IARM_Bus_Call(_IARM_XUPNP_NAME,IARM_BUS_XUPNP_API_GetXUPNPDeviceInfo,
                                   (void *)param,
                                   sizeof(IARM_Bus_SYSMGR_GetXUPNPDeviceInfo_Param_t) + MAX_DATA_LEN + 1);

        if(iarmResult != IARM_RESULT_SUCCESS)
        {
            DEBUG_PRINT(DEBUG_ERROR, "IARM_Bus_Call to GetXUPNPDeviceInfo failed\n");
            response["result"] = "FAILURE";
            response["details"] = "IARM_Bus_Call to GetXUPNPDeviceInfo failed";
        }
        else if ((!param->pBuffer) || (param->pBuffer[0] == '\0')) {
            DEBUG_PRINT(DEBUG_ERROR, "GetXUPNPDeviceInfo IARM_Bus_Call return NULL buffer pointer\n");
            response["result"] = "FAILURE";
            response["details"] = "GetXUPNPDeviceInfo IARM_Bus_Call return NULL buffer pointer";
        }
        else if (strstr(param->pBuffer,"null")) {
            DEBUG_PRINT(DEBUG_ERROR, "GetXUPNPDeviceInfo IARM_Bus_Call returned buffer with value null\n");
            response["result"] = "FAILURE";
            response["details"] = "GetXUPNPDeviceInfo IARM_Bus_Call returned buffer with value null";
        }
        else {
            DEBUG_PRINT(DEBUG_TRACE, "GetXUPNPDeviceInfo IARM_Bus_Call successful\n");
            char *subStr;
            if ((subStr = strstr(param->pBuffer,parameter.c_str())))
            {
                DEBUG_PRINT(DEBUG_LOG,"Parameter found: %s\n",subStr);
                response["result"] = "SUCCESS";
                response["details"] = subStr;
            }
            else {
                DEBUG_PRINT(DEBUG_ERROR,"Requested param (%s) not found in upnp result %s\n",parameter.c_str(),param->pBuffer);
                response["result"] = "FAILURE";
                response["details"] = "Parameter not found in upnp result";
            }
        }
        IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_GetUpnpResult -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_ReadXDiscOutputFile

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the basestreamingurl is present in the json message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_ReadXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ReadXDiscOutputFile --->Entry\n");

    string parameter = req["paramName"].asString();
    string value;

    DEBUG_PRINT(DEBUG_TRACE, "Reading parameter %s in file %s\n",parameter.c_str(),XDISC_OUTPUT_FILE);

    ifstream outputFile(XDISC_OUTPUT_FILE);
    if(outputFile.is_open())
    {
        string line;
        size_t start = 0;
        int numberOfOccurence = 0;
        while(outputFile.good())
        {
            getline(outputFile,line);
            if ((start = line.find(parameter)) != string::npos)
            {
                DEBUG_PRINT(DEBUG_LOG,"Parameter found: %s\n",line.c_str());
                value += line;
                start += parameter.length();
                numberOfOccurence++;
            }
        }
        outputFile.close();

        if (!numberOfOccurence) {
            //Parameter not found, print the output file
            DEBUG_PRINT(DEBUG_ERROR,"Requested param (%s) not found in %s file \n",parameter.c_str(),XDISC_OUTPUT_FILE);
            value.assign("Parameter not found in file "XDISC_OUTPUT_FILE);
            system("cat "XDISC_OUTPUT_FILE);
        }
        else {
            DEBUG_PRINT(DEBUG_TRACE, "Param value  = %s\n",value.c_str());
            response["result"] = "SUCCESS";
            response["details"] = value;
            DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ReadXDiscOutputFile -->Exit\n");
            return TEST_SUCCESS;
        }
    }
    else
    {
        value.assign("Unable to open output file "XDISC_OUTPUT_FILE);
        DEBUG_PRINT(DEBUG_ERROR,"Unable to open file %s\n",XDISC_OUTPUT_FILE);
    }

    DEBUG_PRINT(DEBUG_TRACE, "%s is not present in file %s\n",parameter.c_str(),XDISC_OUTPUT_FILE);
    response["result"] = "FAILURE";
    response["details"] = value;

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ReadXDiscOutputFile -->Exit\n");
    return TEST_FAILURE;
}

/**************************************************************************
Function name : XUPNPAgent_CheckXDiscOutputFile

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to check the JSON messsage is present or not.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_CheckXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_CheckXDiscOutputFile --->Entry\n");
    char stringDetails[DETAILS_LEN] = {'\0'};

    // Check if xdiscovery output file is created
    ifstream xdiscOutFile(XDISC_OUTPUT_FILE);
    if (xdiscOutFile.good()) {
        xdiscOutFile.close();
        sprintf(stringDetails,"%s file found", XDISC_OUTPUT_FILE);
        DEBUG_PRINT(DEBUG_TRACE, "%s file found\n",XDISC_OUTPUT_FILE);
        response["result"] = "SUCCESS";
        response["details"] = stringDetails;
    }
    else {
        sprintf(stringDetails,"xdiscovery output file %s file not found", XDISC_OUTPUT_FILE);
        DEBUG_PRINT(DEBUG_TRACE, "xdiscovery output file %s file not found\n",XDISC_OUTPUT_FILE);
        response["result"] = "FAILURE";
        response["details"] = stringDetails;
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_CheckXDiscOutputFile -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_ModifyBasicDeviceXml

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to modify the xml file and check the behavior message.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_ModifyBasicDeviceXml(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ModifyBasicDeviceXml --->Entry\n");

    char strCmd[128] = {'\0'};
    string localConfFile = g_tdkPath + "/tdk_BasicDevice.xml";

    //Create temp BasicDevice.xml file
    sprintf(strCmd,"sed '7,9d' %s > %s",BASICDEVXML_FILE,localConfFile.c_str());
    if (-1 != system(strCmd)) {
        DEBUG_PRINT(DEBUG_TRACE,"Successfully created temp file %s\n",localConfFile.c_str());
        memset(strCmd,'\0',sizeof(strCmd));
        //Modify /opt/xupnp/BasicDevice.xml file
        sprintf(strCmd,"mv %s %s",localConfFile.c_str(),BASICDEVXML_FILE);
        if (-1 != system(strCmd)) {
            DEBUG_PRINT(DEBUG_TRACE,"Successfully modified %s\n",BASICDEVXML_FILE);
            // Restart upnp service after modification
            if (-1 != system(STARTUPCMD)) {
                sleep(5);
                DEBUG_PRINT(DEBUG_TRACE, "Successfully restarted upnp service\n");
                //Read restored BasicDevice.xml from /opt/xupnp location
                if (true == readLogFile(BASICDEVXML_FILE, "deviceType"))
                {
                    DEBUG_PRINT(DEBUG_TRACE, "BasicDevice.xml file restored in /opt/xupnp from /etc/xupnp\n");
                    response["result"] = "SUCCESS";
                    response["details"] = "BasicDevice.xml file restored in /opt/xupnp from /etc/xupnp";
                }
                else
                {
                    DEBUG_PRINT(DEBUG_TRACE, "BasicDevice.xml file not restored in /opt/xupnp from /etc/xupnp\n");
                    response["result"] = "FAILURE";
                    response["details"] = "BasicDevice.xml file not restored in /opt/xupnp from /etc/xupnp";
                }
            }
            else {
                DEBUG_PRINT(DEBUG_ERROR,"Error in restarting upnp service\n");
                response["result"] = "FAILURE";
                response["details"] = "Error in restarting upnp service";
            }
        }
        else {
            DEBUG_PRINT(DEBUG_ERROR,"Failed to modify %s\n",BASICDEVXML_FILE);
            response["result"] = "FAILURE";
            response["details"] = "Error in modifying /opt/xupnp/BasicDevice.xml";
            //Delete temp BasicDevice.xml file
            memset(strCmd,'\0',sizeof(strCmd));
            sprintf(strCmd,"rm %s",localConfFile.c_str());
            system(strCmd);
        }
    }
    else {
        DEBUG_PRINT(DEBUG_ERROR,"Failed to create temp file %s\n",localConfFile.c_str());
        response["result"] = "FAILURE";
        response["details"] = "Error in creating temp BasicDevice.xml file";
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ModifyBasicDeviceXml -->Exit\n");

    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_CheckXMLRestoration

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to remove all the  xml files refered by the process xcal-device and xdiscovery and check the behavior message.
                /etc/xupnp contents
                BasicDevice.xml DiscoverFriendlies.xml
                xdiscovery.conf for XI3
                BasicDevice.xml DiscoverFriendlies.xml RemoteUIServer.xml RemoteUIServerDevice.xml
                xdiscovery.conf xdevice.conf xdevice_hybrid.conf for XG1
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_CheckXMLRestoration(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_CheckXMLRestoration --->Entry\n");

    const char *cmdRemoveXml = (const char *)"rm /opt/xupnp/*.xml";
    try
    {
        system(cmdRemoveXml);
        system(STARTUPCMD);
        sleep(5);
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Error in restarting upnp service\n");
        response["result"] = "FAILURE";
        response["details"] = "Error in restarting upnp service";
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_CheckXMLRestoration ---> Exit\n");
        return TEST_FAILURE;
    }

    //Read BasicDevice.xml from /opt/xupnp location
    if (true == readLogFile(BASICDEVXML_FILE, "deviceType"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "XML files restored in /opt/xupnp from /etc/xupnp\n");
        response["result"] = "SUCCESS";
        response["details"] = "XML files restored in /opt/xupnp from /etc/xupnp";
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "XML files not restored in /opt/xupnp from /etc/xupnp\n");
        response["result"] = "FAILURE";
        response["details"] = "XML files not restored in /opt/xupnp from /etc/xupnp";
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_CheckXMLRestoration -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_ReadXcalDeviceLogFile

Arguments     : Input argument : 2 , evtName and evtValue
		Output argument : "SUCCESS"  is TRUE
			  	  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_ReadXcalDeviceLogFile(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ReadXcalDeviceLogFile --->Entry\n");

    if (false == readLogFile(XCALDEV_LOG_FILE, "WareHouse Mode recvid"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "WareHouse Mode not updated in %s\n", XCALDEV_LOG_FILE);
        response["result"] = "FAILURE";
        response["details"] = "WareHouse Mode not updated in xcal-device log";
    }
    else if(false == readLogFile(XCALDEV_LOG_FILE, "Received Serial Number"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "Serial Number not updated in %s\n", XCALDEV_LOG_FILE);
        response["result"] = "FAILURE";
        response["details"] = "Serial Number not updated in xcal-device log";
    }
    else if (false == readLogFile(XCALDEV_LOG_FILE, "Received controller id"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "controller id not updated in %s\n", XCALDEV_LOG_FILE);
        response["result"] = "FAILURE";
        response["details"] = "Controller id not updated in xcal-device log";
    }
    else if (false == readLogFile(XCALDEV_LOG_FILE, "BasicDevice.xml"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "Dev XML File Name not updated in %s\n", XCALDEV_LOG_FILE);
        response["result"] = "FAILURE";
        response["details"] = "Dev XML File Name not updated in xcal-device log";
    }
    else if (false == readLogFile(XCALDEV_LOG_FILE, "Received channel map id"))
    {
        DEBUG_PRINT(DEBUG_TRACE, "Channel map id not updated in %s\n", XCALDEV_LOG_FILE);
        response["result"] = "FAILURE";
        response["details"] = "Channel map id not updated in xcal-device log";
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "%s is updated with services\n", XCALDEV_LOG_FILE);
        response["result"] = "SUCCESS";
        response["details"] = "xcal-device log is updated with services";
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_ReadXcalDeviceLogFile --> Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : XUPNPAgent_BroadcastEvent

Arguments     : Input argument : 2 , evtName and evtValue
		Output argument : "SUCCESS"  is TRUE
			  	  "FAILURE"  is FALSE

Description   : Common function to receive the request from Test Manager to check the sysmgrs events triggered from iarmbus is received or not.
**************************************************************************/
bool XUPNPAgent::XUPNPAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_BroadcastEvent --->Entry\n");

    IARM_Bus_SYSMgr_EventData_t eventData;
    int stateId = req["stateId"].asInt();
    string eventLog = req["eventLog"].asString();

    DEBUG_PRINT(DEBUG_TRACE, "stateId = %d eventLog = %s\n",stateId,eventLog.c_str());

    switch(stateId) {
    case IARM_BUS_SYSMGR_SYSSTATE_TUNEREADY:
        eventData.data.systemStates.state = req["state"].asInt();
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_STB_SERIAL_NO:
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_CHANNELMAP:
        eventData.data.systemStates.state = req["state"].asInt();
        eventData.data.systemStates.error = req["error"].asInt();
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_DAC_ID:
        eventData.data.systemStates.state = req["state"].asInt();
        eventData.data.systemStates.error = req["error"].asInt();
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_PLANT_ID:
        eventData.data.systemStates.state = req["state"].asInt();
        eventData.data.systemStates.error = req["error"].asInt();
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_VOD_AD:
        eventData.data.systemStates.stateId = IARM_BUS_SYSMGR_SYSSTATE_VOD_AD;
        eventData.data.systemStates.state = req["state"].asInt();
        eventData.data.systemStates.error = req["error"].asInt();
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    case IARM_BUS_SYSMGR_SYSSTATE_TIME_ZONE:
        eventData.data.systemStates.state = req["state"].asInt();
        eventData.data.systemStates.error = req["error"].asInt();
        strcpy(eventData.data.systemStates.payload, req["payload"].asString().c_str());
        break;
    default:
        DEBUG_PRINT(DEBUG_ERROR, "Unsupported state id value\n");
        response["result"] = "FAILURE";
        response["details"] = "Unsupported state id value";
        DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_BroadcastEvent --->Exit\n");
        return TEST_FAILURE;
    }

    IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE,(void*)&eventData,sizeof(eventData));
    bool result = readLogFile(XCALDEV_LOG_FILE, eventLog);
    if (result)
    {
        response["result"] = "SUCCESS";
        response["details"] = "Event received by xcal-device process";
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "Event not received by xcal-device process";
    }

    DEBUG_PRINT(DEBUG_TRACE, "XUPNPAgent_BroadcastEvent --->Exit\n");
    return TEST_SUCCESS;
}

/****ee********************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "XUPNPAgent".
**************************************************************************/

extern "C" XUPNPAgent* CreateObject()
{
    return new XUPNPAgent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool XUPNPAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }

    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_GetUpnpResult");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_ReadXDiscOutputFile");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_CheckXDiscOutputFile");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_ModifyBasicDeviceXml");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_CheckXMLRestoration");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_ReadXcalDeviceLogFile");
    ptrAgentObj->UnregisterMethod("TestMgr_XUPNP_BroadcastEvent");

    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is XUPNPAgent Object

Description   : This function will be used to destory the XUPNPAgent object.
**************************************************************************/
extern "C" void DestroyObject(XUPNPAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying RDKLogger Agent object\n");
    delete stubobj;
}
