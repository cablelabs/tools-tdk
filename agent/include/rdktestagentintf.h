/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#ifndef __RDK_TEST_AGENT_INTF__
#define __RDK_TEST_AGENT_INTF__

/* System Includes */
#include <json/json.h>
#include <jsonrpc/jsonrpc.h>
#include <iostream>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <stdlib.h>
/* debug message */
typedef enum _DEBUG_LEVEL_
{
	DEBUG_NONE,
	DEBUG_ERROR,
	DEBUG_LOG,
	DEBUG_TRACE
}_DEBUG_LEVEL_t;

#ifdef DEBUG_LEVEL_TRACE
#define DEBUG_ENABLE 3
#endif
#ifdef DEBUG_LEVEL_LOG
#define DEBUG_ENABLE 2
#endif
#ifdef DEBUG_LEVEL_ERROR
#define DEBUG_ENABLE 1
#endif
#ifndef DEBUG_ENABLE
#define DEBUG_ENABLE 1
#endif

#define DEBUG_PRINT(eDebugLevel,pui8Debugmsg...)\
    do{\
            if(eDebugLevel <= DEBUG_ENABLE)\
            {\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y  %T",localtime(&curtime));\
                fprintf(stdout,"\n\n%s: Function Name: %s; Line: %d :- \n",buffer,__FUNCTION__,__LINE__);\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
            }\
        }while(0)


/**************************************************************************************
Description   : This Class provides interface for the module to enable RPC mechanism.

 **************************************************************************************/
class RDKTestAgent
{

	public:
		/* Constructor */
		RDKTestAgent (Json::Rpc::TcpServer *ptrRpcServer)
		{
			m_ptrRPCServer = ptrRpcServer;
		}

		/* Destructor */
		virtual ~RDKTestAgent(){}


/********************************************************************************************************************
Description  :       This function helps to register methods to enable RPC.
Parameters :   
refObj   - Ponter to reference class.
ptrFn     - Pointer to function to be registered as an RPC.
szName - Name of the function to register in RPC mechanism.

Return:                bool  -      Always returning true from this function.

*********************************************************************************************************************/
		template <class T> bool RegisterMethod (T& refObj, bool (T::*ptrFn) (const Json::Value&, Json::Value&), const char* szName )
		{
			DEBUG_PRINT (DEBUG_ERROR, "Registering %s \n", szName);
			m_ptrRPCServer -> AddMethod (new Json::Rpc::RpcMethod <T> (refObj, ptrFn, std::string (szName)));
			return true;
		}


/********************************************************************************************************************
Description  :       This function helps to unregister methods which is registered for RPC mechanism.
Parameters :   
szName - Name of the function as registered in RPC mechanism.

Return:                bool  -      Always returning true from this function.

*********************************************************************************************************************/
		bool UnregisterMethod (const char* szName)
		{
			DEBUG_PRINT (DEBUG_LOG,  "Unregistering %s \n", szName);
			m_ptrRPCServer -> DeleteMethod (szName);
			return true;
		}

	private:
		Json::Rpc::TcpServer  *m_ptrRPCServer;

}; /* End of RDKTestAgent*/

#endif  //__RDK_TEST_AGENT_INTF__


