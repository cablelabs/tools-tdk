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
static int dtcpinitialized = 0;


/*************************************************************************
Function name : searchPattern

Arguments     : file path

return       : return string

Description   : used to check  the ipaddress in the file.
***************************************************************************/
string searchPattern(const char* filepath)
{
    string line;
    string retString;
    ifstream in(filepath);
    DEBUG_PRINT(DEBUG_LOG,"\nInside the search pattern file name is %s \n",filepath);

    std::stringstream buffer;
    buffer<<in.rdbuf();	
    string test = buffer.str();
    DEBUG_PRINT(DEBUG_LOG,"\n content of the file is %s \n",(char*)test.c_str());
    
    return test;
   
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
	DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent testmodule pre_requisites --> Entry\n");

        system ("ifconfig eth1 | grep inet | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g' > /opt/TDK/dtcptestIPaddress.txt");
     
	DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent testmodule pre_requisites --> Exit\n");
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
	DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent testmodule post_requisites --> Entry\n");

	DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent testmodule post requisites --> Exit");

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
        dtcp_result_t returnType;
        int ret=1;
        string resultdetails;
	DEBUG_PRINT(DEBUG_LOG, "Recieved function name %s \n", functionName.c_str());
        char outputJsonpath[64]= {'\0'};
        sprintf(outputJsonpath, "%s", "/opt/TDK/dtcptestIPaddress.txt");
        string ipaddress ;
        ipaddress= searchPattern(outputJsonpath);

	try
	{
	    	if (functionName.compare("DTCPMgrInitialize")==0)
       		{
                  if (dtcpinitialized == 0)
        	{
                	printf("initialized Manager\n");
	                dtcpinitialized = 1;
        	}
        	else
        	{	
                	printf("Already initialized\n");
        	}
        	returnType = DTCPMgrInitialize();
		}
			
	    	if (functionName.compare("DTCPMgrStartSource")==0)
	       	{
	        char ifname[64] = {'\0'};
                string par1= req["param1"].asString();
	        sprintf(ifname,"%s",par1.c_str());
                if (ifname == NULL) 
	        sprintf(ifname,"%s",ipaddress.c_str());
                if(dtcpinitialized != 1)
		DTCPMgrInitialize();
		int portNo = req["param2"].asInt();
		returnType = DTCPMgrStartSource(ifname,portNo);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		
		DTCPMgrStopSource();
		}
	   	
		if (functionName.compare("DTCPMgrStopSource")==0)
	       	{ 
			if (dtcpinitialized == 1)
        		{
	                printf("stopped DTCP Manager\n");
	                 dtcpinitialized = 0;
			}
       			 else
        		{
                		printf ("Already stopped\n");
        		}

	         returnType = DTCPMgrStopSource();
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		}
	    	
		if (functionName.compare("DTCPMgrCreateSourceSession")==0)
	       	{
	        char ipname[64] = {'\0'};
		string sinkip = req["param1"].asString();
	        sprintf(ipname, "%s",sinkip.c_str());
	        int keylabel=req["param2"].asInt();
	        int pcppacketsz = req["param3"].asInt();
	        int maxpacketsz = req["param4"].asInt();
		DTCP_SESSION_HANDLE *handle =new DTCP_SESSION_HANDLE ;
		returnType = DTCPMgrCreateSourceSession(ipname,keylabel,pcppacketsz,maxpacketsz,handle);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
                }

	    	if (functionName.compare("DTCPMgrCreateSinkSession")==0)
	       	{
	        char ipname[64] = {'\0'};
		string srcip =req["param1"].asString();
	        sprintf(ipname, "%s",srcip.c_str());
	        int portNo=req["param2"].asInt();
		DEBUG_PRINT(DEBUG_LOG, "Before calling the  p3\n");
	        BOOLEAN p3=(BOOLEAN)req["param3"].asInt();
	        int maxpacketsz = req["param4"].asInt();
		DTCP_SESSION_HANDLE *handle =new DTCP_SESSION_HANDLE;
		returnType = DTCPMgrCreateSinkSession(ipname,portNo,p3,maxpacketsz,handle);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		delete handle;
 		}
		
		if (functionName.compare("DTCPMgrProcessPacket")==0)
	       	{
		DTCP_SESSION_HANDLE session;
	        //session= (DTCP_SESSION_HANDLE)req["param1"].asInt();
		DTCPIP_Packet *packet=new DTCPIP_Packet;	 	
		returnType = DTCPMgrProcessPacket( session, packet);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		}
		
		if (functionName.compare("DTCPMgrReleasePacket")==0)
	       	{
		DTCPIP_Packet *packet=new DTCPIP_Packet;	 	
		returnType = DTCPMgrReleasePacket( packet);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
                delete packet;
		}

		if (functionName.compare("DTCPMgrDeleteDTCPSession")==0)
	       	{
		DTCP_SESSION_HANDLE session;
		returnType = DTCPMgrDeleteDTCPSession(session);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		}

		if (functionName.compare("DTCPMgrGetNumSessions")==0)
	       	{
		DTCPDeviceType deviceType;
		ret = DTCPMgrGetNumSessions(deviceType);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),ret);
		}

		if (functionName.compare("DTCPMgrGetSessionInfo")==0)
	       	{
		DTCP_SESSION_HANDLE handle;
	        //handle= (DTCP_SESSION_HANDLE)req["param1"].asInt();
		DTCPIP_Session *session=new DTCPIP_Session;	 	
		returnType = DTCPMgrGetSessionInfo(handle,session);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
                delete session;
		}

		if (functionName.compare("DTCPMgrSetLogLevel")==0)
	       	{
		int level= req["param2"].asInt();
		returnType = DTCPMgrSetLogLevel(level);
		DEBUG_PRINT(DEBUG_LOG, "function %s return value %d \n",functionName.c_str(),(int)returnType);
		}


	}
	catch(exception &e)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured during function call ");
                DEBUG_PRINT(DEBUG_LOG,"Exception catched is %s ", e.what() );
                response["details"]= "FAILURE:Exception occured during function call "+req["funcName"].asString();
       		response["result"]="FAILURE";
		return TEST_FAILURE;
        }

               
	DEBUG_PRINT(DEBUG_LOG, "Before updating the details function %s return value %d \n",functionName.c_str(),(int)returnType);
	char resval[10] = {'\0'};
	if(ret !=1)        
	sprintf(resval, "%d",(int)returnType);
	else
	sprintf(resval, "%d",ret);
        response["details"]= resval;
     	DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Init -->Exit\n");
       	response["result"]="SUCCESS";
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
