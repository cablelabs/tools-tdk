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

#include "dtcpagent.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <exception>

#define RESULT_LEN	100

#if 0
/*************************************************************************
Function name : getIpAddress

Arguments     : file path

return       : return string

Description   : used to check  the ipaddress in the file.
***************************************************************************/
std::string getIpAddress()
{
    char *cmd = "ifconfig eth1 | grep inet | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'";
    char ipAddress[128] = {'\0'};
    FILE *ptr;

    if ((ptr = popen(cmd, "r")) != NULL) {
        while (fgets(ipAddress, 128, ptr) != NULL)
            DEBUG_PRINT(DEBUG_LOG,"IP Address is %s \n",ipAddress);
        pclose(ptr);
    }

    return std::string(ipAddress);
}
#endif

dtcp_result_t createDTCPSinkSession(DTCP_SESSION_HANDLE *handle)
{
    char* srcIpAddress = (char*)"127.0.0.1";
    int srcIpPort = 5000;
    int maxPacketSize = 4096;
    dtcp_result_t returnCode = DTCPMgrCreateSinkSession(srcIpAddress, srcIpPort, false, maxPacketSize, handle);
    DEBUG_PRINT(DEBUG_LOG, "%s(): returnCode(%d)\n",__FUNCTION__,(int)returnCode);
    return returnCode;
}

dtcp_result_t createDTCPSourceSession(DTCP_SESSION_HANDLE *handle)
{
    char* sinkIpAddress = (char*)"0.0.0.0";
    int keyLabel = 0;
    int pcpPacketSize = 0;
    int maxPacketSize = 4096;
    dtcp_result_t returnCode = DTCPMgrCreateSourceSession(sinkIpAddress,keyLabel,pcpPacketSize,maxPacketSize,handle);
    DEBUG_PRINT(DEBUG_LOG, "%s(): returnCode(%d)\n",__FUNCTION__,(int)returnCode);
    return returnCode;
}

DTCPAgent::DTCPAgent()
{
    DEBUG_PRINT(DEBUG_LOG, "DTCPAgent Initialized\n");
}

/**************************************************************************
Function name : DTCPAgent::initialize

Arguments     : Input arguments are Version string and DTCPAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool DTCPAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_ERROR, "DTCPAgent Initialization\n");
    ptrAgentObj->RegisterMethod(*this,&DTCPAgent::DTCPAgent_Init, "TestMgr_DTCPAgent_Init");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string DTCPAgent::testmodulepre_requisites()
{
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool DTCPAgent::testmodulepost_requisites()
{
    return TEST_SUCCESS;
}


/**************************************************************************
Function name : DTCPAgent::DTCPAgent_Init

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to initialize dtcp module.
**************************************************************************/
bool DTCPAgent::DTCPAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Init --->Entry\n");

    string functionName = req["funcName"].asString();
    dtcp_result_t returnCode = DTCP_SUCCESS;
    char resultDetails[RESULT_LEN] = {'\0'};
    DEBUG_PRINT(DEBUG_LOG,"Received function name: %s\n", functionName.c_str());

    try
    {
        if (functionName.compare("DTCPMgrInitialize")==0)
        {
            returnCode = DTCPMgrInitialize();
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
        }
        else if (functionName.compare("DTCPMgrStartSource")==0)
        {
            string ifname = req["param1"].asString();
            int portNo = req["param2"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [ifname:%s portNo:%d]\n",ifname.c_str(),portNo);
            returnCode = DTCPMgrStartSource(&ifname[0],portNo);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
        }
        else if (functionName.compare("DTCPMgrStopSource")==0)
        {
            returnCode = DTCPMgrStopSource();
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
        }
        else if (functionName.compare("DTCPMgrCreateSourceSession")==0)
        {
            string sinkip = req["param1"].asString();
            int keylabel = req["param2"].asInt();
            int pcppacketsz = req["param3"].asInt();
            int maxpacketsz = req["param4"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [SinkIp:%s keyLabel:%d pcpPacketSize:%d maxPacketSize:%d]\n",sinkip.c_str(),keylabel,pcppacketsz,maxpacketsz);
            DTCP_SESSION_HANDLE *handle = new DTCP_SESSION_HANDLE;
            returnCode = DTCPMgrCreateSourceSession(&sinkip[0],keylabel,pcppacketsz,maxpacketsz,handle);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
            delete handle;
        }
        else if (functionName.compare("DTCPMgrCreateSinkSession")==0)
        {
            string srcip = req["param1"].asString();
            int portNo = req["param2"].asInt();
            bool uniqueKey = req["param3"].asInt();
            int maxpacketsz = req["param4"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [SrcIp:%s srcPort:%d uniqueKey:%d maxPacketSize:%d]\n",srcip.c_str(),portNo,uniqueKey,maxpacketsz);
            DTCP_SESSION_HANDLE *handle =new DTCP_SESSION_HANDLE;
            returnCode = DTCPMgrCreateSinkSession(&srcip[0],portNo,uniqueKey,maxpacketsz,handle);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
            delete handle;
        }
        else if (functionName.compare("DTCPMgrProcessPacket")==0)
        {
            //Create DTCPSinkSession
            DTCP_SESSION_HANDLE pDtcpSession = 0;
            returnCode = createDTCPSinkSession(&pDtcpSession);
            if(DTCP_SUCCESS == returnCode)
            {
                DTCPIP_Packet *packet=new DTCPIP_Packet;
                returnCode = DTCPMgrProcessPacket(pDtcpSession, packet);
                DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
                delete packet;
            }
            else
            {
                DEBUG_PRINT(DEBUG_ERROR, "Failed to create session for DTCPMgrProcessPacket (%d)\n",(int)returnCode);
            }
        }
        else if (functionName.compare("DTCPMgrReleasePacket")==0)
        {
            DTCPIP_Packet *packet=new DTCPIP_Packet;
            returnCode = DTCPMgrReleasePacket( packet);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
            delete packet;
        }
        else if (functionName.compare("DTCPMgrDeleteDTCPSession")==0)
        {
            //Create DTCPSinkSession
            DTCP_SESSION_HANDLE pDtcpSession = 0;
            returnCode = createDTCPSinkSession(&pDtcpSession);
            if(DTCP_SUCCESS == returnCode)
            {
                returnCode = DTCPMgrDeleteDTCPSession(pDtcpSession);
                DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
            }
            else
            {
                DEBUG_PRINT(DEBUG_ERROR, "Failed to create session for DTCPMgrDeleteDTCPSession (Error:%d)\n",(int)returnCode);
            }
        }
        else if (functionName.compare("DTCPMgrGetNumSessions")==0)
        {
            int iDeviceType = req["param2"].asInt();
            if (((DTCPDeviceType)iDeviceType < DTCP_SOURCE) or ((DTCPDeviceType)iDeviceType > DTCP_UNKNOWN))
                iDeviceType = (DTCPDeviceType)DTCP_UNKNOWN;

            DEBUG_PRINT(DEBUG_LOG,"Input [DTCPDeviceType:%d]\n",iDeviceType);
            int numSessions = DTCPMgrGetNumSessions((DTCPDeviceType)iDeviceType);
            DEBUG_PRINT(DEBUG_LOG,"function %s return value %d numSessions %d \n",functionName.c_str(),(int)returnCode,numSessions);
        }
        else if (functionName.compare("DTCPMgrGetSessionInfo")==0)
        {
            //Create DTCPSinkSession
            DTCP_SESSION_HANDLE handle = 0;
            returnCode = createDTCPSinkSession(&handle);
            if(DTCP_SUCCESS == returnCode)
            {
                DTCPIP_Session *session=new DTCPIP_Session;
                returnCode = DTCPMgrGetSessionInfo(handle,session);
                delete session;
                DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
            }
            else
            {
                DEBUG_PRINT(DEBUG_ERROR, "Failed to create handle for DTCPMgrGetSessionInfo (Error:%d)\n",(int)returnCode);
            }
        }
        else if (functionName.compare("DTCPMgrSetLogLevel")==0)
        {
            int level= req["param2"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [LogLevel:%d]\n",level);
            returnCode = DTCPMgrSetLogLevel(level);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnCode);
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"Unsupported function call\n");
            response["details"]= "Unsupported function call";
            response["result"]="FAILURE";
            DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Init -->Exit\n");
            return TEST_FAILURE;
        }
    }
    catch(exception &e)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured during function call\n");
        DEBUG_PRINT(DEBUG_LOG,"Exception caught is %s\n", e.what() );
        response["details"]= "Exception occured during function call";
        response["result"]="FAILURE";
        return TEST_FAILURE;
    }

    // Update details and result in response msg
    sprintf(resultDetails,"Function:%s ReturnCode:%d",functionName.c_str(),(int)returnCode);
    response["details"]= resultDetails;

    if (DTCP_SUCCESS != returnCode)
        response["result"]="FAILURE";
    else
        response["result"]="SUCCESS";

    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Init -->Exit\n");
    return TEST_SUCCESS;
}
/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "DTCPAgent".
**************************************************************************/

extern "C" DTCPAgent* CreateObject()
{
    return new DTCPAgent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool DTCPAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }
    ptrAgentObj->UnregisterMethod("TestMgr_DTCPAgent_Init");

    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is DTCPAgent Object

Description   : This function will be used to destory the DTCPAgent object.
**************************************************************************/
extern "C" void DestroyObject(DTCPAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying DTCPAgent Agent object\n");
    delete stubobj;
}
