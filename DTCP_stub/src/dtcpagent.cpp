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
#include <list>
#include <sstream>
#include <exception>

static list<DTCP_SESSION_HANDLE> srcSessionHandlerList;
static list<DTCP_SESSION_HANDLE> sinkSessionHandlerList;

DTCPAgent::DTCPAgent()
{
    DEBUG_PRINT(DEBUG_LOG, "DTCPAgent Initialized");
}

/**************************************************************************
Function name : DTCPAgent::initialize

Arguments     : Input arguments are Version string and DTCPAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool DTCPAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_ERROR, "DTCPAgent Initialization");
    ptrAgentObj->RegisterMethod(*this,&DTCPAgent::DTCPAgent_Test_Execute, "TestMgr_DTCP_Test_Execute");

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
    std::list<DTCP_SESSION_HANDLE>::iterator it;
    if(!srcSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of source session handler list");
        for(it = srcSessionHandlerList.begin(); it != srcSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Source Handler: %p ",(void*)*it);
        }
    }

    if(!sinkSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of sink session handler list");
        for(it = sinkSessionHandlerList.begin(); it != sinkSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Sink Handler: %p ",(void*)*it);
        }
    }

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
    std::list<DTCP_SESSION_HANDLE>::iterator it;
    if(!srcSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of source session handler list");
        for(it = srcSessionHandlerList.begin(); it != srcSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Source Handler: %p ",(void*)*it);
        }
    }

    if(!sinkSessionHandlerList.empty()) {
        DEBUG_PRINT(DEBUG_ERROR, "Contents of sink session handler list");
        for(it = sinkSessionHandlerList.begin(); it != sinkSessionHandlerList.end(); it++) {
            DEBUG_PRINT(DEBUG_LOG, "Sink Handler: %p ",(void*)*it);
        }
    }

    return TEST_SUCCESS;
}


/**************************************************************************
Function name : DTCPAgent::DTCPAgent_Test_Execute

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to run test dtcp  module.
**************************************************************************/
bool DTCPAgent::DTCPAgent_Test_Execute(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute --->Entry");

    string functionName = req["funcName"].asString();
    dtcp_result_t returnCode = DTCP_SUCCESS;
    DEBUG_PRINT(DEBUG_LOG,"Received function name: %s", functionName.c_str());

    try
    {
        if (functionName.compare("DTCPMgrInitialize")==0)
        {
	    stringstream details;
            returnCode = DTCPMgrInitialize();
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);
		
    	    if (returnCode != DTCP_SUCCESS)
	    {
		DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrInitialize() Failed to intialize.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrInitialize() Failed. ReturnCode:" << returnCode;
        	response["details"] = details.str();
	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrInitialize() Successfully intialized.");
		response["result"] = "SUCCESS";
		details << "DTCPMgrInitialize() Success. ReturnCode:" << returnCode;
	        response["details"] = details.str();
	    }
        }
        else if (functionName.compare("DTCPMgrStartSource")==0)
        {
            string ifname = req["strParam1"].asString();
            int portNo = req["intParam2"].asInt();
	    stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [ifname:%s portNo:%d]\n",ifname.c_str(),portNo);
            returnCode = DTCPMgrStartSource(&ifname[0],portNo);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);

  	    if (returnCode != DTCP_SUCCESS) 
	    {
		DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrStartSource() Failed to Start Source.");
                response["result"] = "FAILURE";
		details << "DTCPMgrStartSource() Failed. ReturnCode:" << returnCode;
                response["details"] = details.str();
	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrStartSource() Successfully Start Source.");
	        response["result"] = "SUCCESS";
		details << "DTCPMgrStartSource() Success. ReturnCode:" << returnCode;
                response["details"] = details.str();
	    }
        }
        else if (functionName.compare("DTCPMgrStopSource")==0)
        {
            returnCode = DTCPMgrStopSource();
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);
	    stringstream details;

	    if (returnCode != DTCP_SUCCESS)
            {
	    	DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrStopSource() Failed to Stopped Source.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrStopSource() Failed. ReturnCode:" << returnCode;
        	response["details"] = details.str();
 	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrStopSource() Successfully Stopped Source.");
		response["result"] = "SUCCESS";
		details << "DTCPMgrStopSource() Success. ReturnCode:" << returnCode;
		response["details"] = details.str();
	    }
        }
        else if (functionName.compare("DTCPMgrCreateSourceSession")==0)
        {
            string sinkip = req["strParam1"].asString();
            int keylabel = req["intParam2"].asInt();
            int pcppacketsz = req["intParam3"].asInt();
            int maxpacketsz = req["intParam4"].asInt();
	    stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [SinkIp:%s keyLabel:%d pcpPacketSize:%d maxPacketSize:%d]\n",sinkip.c_str(),keylabel,pcppacketsz,maxpacketsz);
            DTCP_SESSION_HANDLE handle;

            returnCode = DTCPMgrCreateSourceSession(&sinkip[0],keylabel,pcppacketsz,maxpacketsz,&handle);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);

	    if(returnCode != DTCP_SUCCESS)
	    {
        	DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrCreateSourceSession() Failed to create source handler.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrCreateSourceSession() Failure. ReturnCode:" << returnCode;
        	response["details"] = details.str();
    	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrCreateSourceSession() Successfully Created Source handler.");
		response["result"] = "SUCCESS";
		details << "DTCPMgrCreateSourceSession() Success. ReturnCode:" << returnCode;
	   	response["details"] = details.str();
                /*Pushing the source session handler on to the sourceList */
                srcSessionHandlerList.push_back(handle);
                DEBUG_PRINT(DEBUG_LOG, "Source Handler (%p) pushed into list",(void*)handle);
	    }
        }
        else if (functionName.compare("DTCPMgrCreateSinkSession")==0)
        {
            string srcip = req["strParam1"].asString();
            int portNo = req["intParam2"].asInt();
            bool uniqueKey = req["intParam3"].asInt();
            int maxpacketsz = req["intParam4"].asInt();
	    stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [SrcIp:%s srcPort:%d uniqueKey:%d maxPacketSize:%d]\n",srcip.c_str(),portNo,uniqueKey,maxpacketsz);
            DTCP_SESSION_HANDLE handle;

            returnCode = DTCPMgrCreateSinkSession(&srcip[0],portNo,uniqueKey,maxpacketsz,&handle);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);
		
	    if(returnCode != DTCP_SUCCESS)
	    {
        	DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrCreateSinkSession() Failed to create sink handler.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrCreateSinkSession() Failed. ReturnCode:" << returnCode;
        	response["details"] = details.str();
    	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrCreateSinkSession() Successfully Created Sink handler.");
		response["result"] = "SUCCESS";
		details << "DTCPMgrCreateSinkSession() Success. ReturnCode:" << returnCode;
		response["details"] = details.str();
                /*Pushing the sink session handler on to the sinkList */
                sinkSessionHandlerList.push_back(handle);
                DEBUG_PRINT(DEBUG_LOG, "Sink Handler (%p) pushed into list",(void*)handle);
	    }
        }
        else if ((functionName.compare("DTCPMgrProcessPacket")==0) || (functionName.compare("DTCPMgrReleasePacket")==0))
        {
            int iDeviceType = req["intParam3"].asInt();
            //unsigned int indexToList = req["intParam2"].asInt();
	    stringstream details;
            DEBUG_PRINT(DEBUG_LOG,"Get last element in list of DeviceType=%d",iDeviceType);

            if(iDeviceType == DTCP_SOURCE)
            {
                if(!srcSessionHandlerList.empty())
                {
                        /*Get the source handler from the list*/
                        DTCP_SESSION_HANDLE pDtcpSession = srcSessionHandlerList.back();
                        DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the source list",(void*)pDtcpSession);
                        
			/*TODO: Need to fill the packet members, Waiting for sujeesh input */
			DTCPIP_Packet *packet=new DTCPIP_Packet;
	
	                returnCode = DTCPMgrProcessPacket(pDtcpSession, packet);
        	        DEBUG_PRINT(DEBUG_LOG, "function DTCPMgrProcessPacket return value %d",(int)returnCode);

			if(DTCP_SUCCESS == returnCode)
                        {
				returnCode = DTCPMgrReleasePacket(packet);
		                DEBUG_PRINT(DEBUG_LOG, "function DTCPMgrReleasePacket return value %d",(int)returnCode);
				
				if(DTCP_SUCCESS == returnCode)
				{
					response["result"]="SUCCESS";
					details << "DTCPMgrReleasePacket() Success. ReturnCode:" << returnCode;
	        	                response["details"]= details.str();
                        	        DEBUG_PRINT(DEBUG_LOG,"DTCP packet released");
				}
				else
				{
					response["result"]="FAILURE";
                                        details << "DTCPMgrReleasePacket() Failed. ReturnCode:" << returnCode;
                                        response["details"]= details.str();
				}
                        }
			else
			{
				response["result"]="FAILURE";
                                details << "DTCPMgrProcessPacket() Failed. ReturnCode:" << returnCode;
                                response["details"]= details.str();
			}
                }
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Source Session List is empty";
		}
            }
            else if(iDeviceType == DTCP_SINK)
            {
                if(!sinkSessionHandlerList.empty())
                {
                        /*Get the sink handler from the list*/
                        DTCP_SESSION_HANDLE pDtcpSession = sinkSessionHandlerList.back();
                        DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the sink list",(void*)pDtcpSession);

			/*TODO: Need to fill the packet members, Waiting for sujeesh input */
			DTCPIP_Packet *packet=new DTCPIP_Packet;

	                returnCode = DTCPMgrProcessPacket(pDtcpSession, packet);
        	        DEBUG_PRINT(DEBUG_LOG, "function DTCPMgrProcessPacket return value %d",(int)returnCode);
			
                        if(DTCP_SUCCESS == returnCode)
                        {
				returnCode = DTCPMgrReleasePacket(packet);
	                        DEBUG_PRINT(DEBUG_LOG, "function DTCPMgrReleasePacket return value %d",(int)returnCode);

                                if(DTCP_SUCCESS == returnCode)
                                {
                                        response["result"]="SUCCESS";
                                        details << "DTCPMgrReleasePacket() Success. ReturnCode:" << returnCode;
                                        response["details"]= details.str();
                                        DEBUG_PRINT(DEBUG_LOG,"DTCP packet released");
                                }
                                else
                                {
                                        response["result"]="FAILURE";
                                        details << "DTCPMgrReleasePacket() Failed. ReturnCode:" << returnCode;
                                        response["details"]= details.str();
                                }
                        }
			else
			{
				response["result"]="FAILURE";
                                details << "DTCPMgrProcessPacket() Failed. ReturnCode:" << returnCode;
                                response["details"]= details.str();
			}
                }
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Sink Session List is empty";
		}
            }
	    else
	    {
	    	DEBUG_PRINT(DEBUG_LOG, "DeviceType %d is invalid",iDeviceType);
	        response["result"]="FAILURE";
		response["details"]="DeviceType is invalid";
	    }
        }
        else if (functionName.compare("DTCPMgrDeleteDTCPSession")==0)
        {
	    int iDeviceType = req["intParam3"].asInt();
	    //unsigned int indexToList = req["intParam2"].asInt();
            stringstream details;
            DEBUG_PRINT(DEBUG_LOG,"Get last element in list of DeviceType=%d",iDeviceType);

	    /*Check for handler to be deleted is for source session*/
	    if(iDeviceType == DTCP_SOURCE)
	    {
		if(!srcSessionHandlerList.empty())
		{
			/*Get the source handler from the list*/
            		DTCP_SESSION_HANDLE pDtcpSession = srcSessionHandlerList.back();
            		DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the source list",(void*)pDtcpSession);
	                returnCode = DTCPMgrDeleteDTCPSession(pDtcpSession);
			if(DTCP_SUCCESS == returnCode)
			{
				srcSessionHandlerList.remove(pDtcpSession);
            			DEBUG_PRINT(DEBUG_LOG,"DTCP session handler deleted and entry removed from source handler list");
				response["result"] = "SUCCESS";
				details << "DTCPMgrDeleteDTCPSession() Success. ReturnCode:" << returnCode;
				response["details"] = details.str();
			}
			else
			{
				DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrDeleteDTCPSession() Failed to delete the Session handler.");
			        response["result"] = "FAILURE";
				details << "DTCPMgrDeleteDTCPSession() Failed. ReturnCode:"<< returnCode;
			        response["details"] = details.str();
			}
		}
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Source Session List is empty";
		}
	    }
            else if(iDeviceType == DTCP_SINK)
	    {
		if(!sinkSessionHandlerList.empty())
		{
			/*Get the sink handler from the list*/
            		DTCP_SESSION_HANDLE pDtcpSession = sinkSessionHandlerList.back();
            		DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the sink list",(void*)pDtcpSession);
	                returnCode = DTCPMgrDeleteDTCPSession(pDtcpSession);
			if(DTCP_SUCCESS == returnCode)
			{
				sinkSessionHandlerList.remove(pDtcpSession);
				DEBUG_PRINT(DEBUG_LOG,"DTCP session handler deleted and entry removed from sink handler list");
                                response["result"] = "SUCCESS";
                                details << "DTCPMgrDeleteDTCPSession() Success. ReturnCode:" << returnCode;
                                response["details"] = details.str();
			}
			else
                        {
                                DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrDeleteDTCPSession() Failed to delete the Session handler.");
                                response["result"] = "FAILURE";
                                details << "DTCPMgrDeleteDTCPSession() Failed. ReturnCode:"<< returnCode;
                                response["details"] = details.str();
                        }
		}
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Sink Session List is empty";
		}
	    }
	    else
	    {
	    	DEBUG_PRINT(DEBUG_LOG, "DeviceType %d is invalid",iDeviceType);
	        response["result"]="FAILURE";
		response["details"]="DeviceType is invalid";
	    }
        }
        else if (functionName.compare("DTCPMgrGetNumSessions")==0)
        {
	    stringstream details;
            int iDeviceType = req["intParam2"].asInt();

            DEBUG_PRINT(DEBUG_LOG,"Input [DeviceType:%d]\n",iDeviceType);
            
	    int numSessions = DTCPMgrGetNumSessions((DTCPDeviceType)iDeviceType);
            DEBUG_PRINT(DEBUG_LOG,"function %s numSessions %d",functionName.c_str(),numSessions);

            if ((numSessions < 0) || (((iDeviceType < DTCP_SOURCE) || (iDeviceType > DTCP_UNKNOWN)) && (numSessions > 0)))
                response["result"] = "FAILURE";
            else
                response["result"] = "SUCCESS";

	    details << numSessions;
            response["details"] = details.str();
        }
        else if (functionName.compare("DTCPMgrGetSessionInfo")==0)
        {
	    int iDeviceType = req["intParam3"].asInt();
            //unsigned int indexToList = req["intParam2"].asInt();
	    stringstream details;
            DEBUG_PRINT(DEBUG_LOG,"Get last element in list of DeviceType=%d",iDeviceType);

            DTCP_SESSION_HANDLE pDtcpSession;
            if(iDeviceType == DTCP_SOURCE)
            {
                if(!srcSessionHandlerList.empty())
                {
                        /*Get the source handler from the list*/
                        pDtcpSession = srcSessionHandlerList.back();
                        DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the source list",(void*)pDtcpSession);
                }
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Source Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Source Session List is empty";
                        DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit");
                        return TEST_FAILURE;
		}	
            }
            else if(iDeviceType == DTCP_SINK)
            {
                if(!sinkSessionHandlerList.empty())
                {
                        /*Get the sink handler from the list*/
                        pDtcpSession = sinkSessionHandlerList.back();
                        DEBUG_PRINT(DEBUG_LOG,"Fetched session handler (%p) from the sink list",(void*)pDtcpSession);
                }
		else
		{
			DEBUG_PRINT(DEBUG_LOG, "Sink Session List is empty");
        		response["result"]="FAILURE";
			response["details"]="Sink Session List is empty";
                        DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit");
                        return TEST_FAILURE;
		}	
            }
	    else
	    {
	    	DEBUG_PRINT(DEBUG_LOG, "DeviceType %d is invalid",iDeviceType);
	        response["result"]="FAILURE";
		response["details"]="DeviceType is invalid";
                DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit");
                return TEST_FAILURE;
	    }

	    DTCPIP_Session sessionInfo;
	    sessionInfo.remote_ip = new char [IPADDR_LEN+1];
            returnCode = DTCPMgrGetSessionInfo(pDtcpSession,&sessionInfo);

	    if(returnCode != DTCP_SUCCESS)
	    {
        	DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrGetSessionInfo() Failed to fetch Session Info.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrGetSessionInfo() Failed. ReturnCode:" << returnCode;
	        response["details"] = details.str();
	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrGetSessionInfo() Successfully fetched session Info for handle %p",(void*)pDtcpSession);
		DEBUG_PRINT(DEBUG_TRACE, "session_handle:%p device_type:%d remote_ip:%s uniqueKey:%d",(void*)sessionInfo.session_handle,sessionInfo.device_type,sessionInfo.remote_ip,sessionInfo.uniqueKey);
		if ((pDtcpSession != sessionInfo.session_handle) || (iDeviceType != sessionInfo.device_type))
                    response["result"] = "FAILURE";
                else
		    response["result"] = "SUCCESS";
	        /*Send session info to script. */
	        details << "DeviceType:" << sessionInfo.device_type << " RemoteIp:" << sessionInfo.remote_ip << " UniqueKey:"<< sessionInfo.uniqueKey;
	        response["details"] = details.str();
            }
            delete [] sessionInfo.remote_ip;
	}
        else if (functionName.compare("DTCPMgrSetLogLevel")==0)
        {
            int level= req["intParam2"].asInt();
	    stringstream details;

            DEBUG_PRINT(DEBUG_LOG,"Input [LogLevel:%d]\n",level);
            returnCode = DTCPMgrSetLogLevel(level);
            DEBUG_PRINT(DEBUG_LOG, "function %s return value %d",functionName.c_str(),(int)returnCode);

	    if(returnCode != DTCP_SUCCESS)
    	    {
	        DEBUG_PRINT(DEBUG_ERROR, "DTCPMgrSetLogLevel() Failed to set.");
	        response["result"] = "FAILURE";
		details << "DTCPMgrSetLogLevel() Failed. ReturnCode:" << returnCode; 
	        response["details"] = details.str();
    	    }
	    else
	    {
		DEBUG_PRINT(DEBUG_TRACE, "DTCPMgrSetLogLevel() Successfully set.");
		response["result"] = "SUCCESS";
		details << "DTCPMgrSetLogLevel() Success. ReturnCode:" << returnCode;
		response["details"] = details.str();
	    }
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR,"Unsupported function call");
            response["details"]= "Unsupported function call";
            response["result"]="FAILURE";
        }
    }
    catch(exception &e)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured during function call");
        DEBUG_PRINT(DEBUG_LOG,"Exception caught is %s", e.what() );
        response["details"]= "Exception occured during function call";
        response["result"]="FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "DTCPAgent_Test_Execute -->Exit");
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
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup");
    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }
    ptrAgentObj->UnregisterMethod("TestMgr_DTCP_Test_Execute");

    return TEST_SUCCESS;
}
/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is DTCPAgent Object

Description   : This function will be used to destory the DTCPAgent object.
**************************************************************************/
extern "C" void DestroyObject(DTCPAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_LOG, "Destroying DTCPAgent Agent object");
    delete stubobj;
}
