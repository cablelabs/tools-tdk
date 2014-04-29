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

#ifndef RPC_METHODS_H
#define RPC_METHODS_H 

/* System Includes */
#include <json/json.h>

/* Application Includes */
#include "rdktestagentintf.h"

/* Constants */
#define DEVICE_FREE 0
#define DEVICE_BUSY 1
#define FLAG_SET 0
#define FLAG_NOT_SET 1
#define RETURN_SUCCESS 0
#define RETURN_FAILURE -1
#define CONFIGURATION_FILE "tdkconfig.ini"
#define PORT_FORWARD_RULE_FILE "forwardRule.ini"

#define STR(x)   #x
#define SHOW_DEFINE(x) STR(x)


/**************************************************************************************
 Description   : This Class provides RPC methods. Test Manager can invoke these 
                      RPC methods to do some operations in the box.
 
 **************************************************************************************/
class RpcMethods
{
	
    public:
        static int sm_nAgentPID;
        static int sm_nDeviceStatusFlag;
        static int sm_nStatusQueryFlag;
        static int sm_nRouteSetFlag;
        static int sm_nGetDeviceFlag;
        static const char* sm_szManagerIP;
        static const char* sm_szBoxName;
        static const char* sm_szBoxInterface;
        static std::string sm_strBoxIP;

        /* Constructor */
        RpcMethods (RDKTestAgent *pAgent)
        {
            m_pAgent = pAgent;
        }
		
        bool RPCLoadModule (const Json::Value& request, Json::Value& response);
        bool RPCUnloadModule (const Json::Value& request, Json::Value& response);
        bool RPCEnableReboot (const Json::Value& request, Json::Value& response);
        bool RPCRestorePreviousState (const Json::Value& request, Json::Value& response);
        bool RPCGetHostStatus (const Json::Value& request, Json::Value& response);
        bool RPCResetAgent (const Json::Value& request, Json::Value& response);
        bool RPCPerformanceSystemDiagnostics (const Json::Value& request, Json::Value& response);
        bool RPCPerformanceBenchMarking (const Json::Value& request, Json::Value& response);


        /* Below methods are applicable only for Gateway boxes */
        #ifdef PORT_FORWARD

        bool RPCGetConnectedDevices (const Json::Value& request, Json::Value& response);
        bool RPCSetClientRoute (const Json::Value& request, Json::Value& response);

        #endif /* End of PORT_FORWARD */

    private:
        RDKTestAgent *m_pAgent;
        int m_iLoadStatus;
        int m_iUnloadStatus;

        std::string LoadLibrary (char* pszLibName);
        std::string UnloadLibrary (char* pszLibName);
        void SetCrashStatus (const char* pszExecId, const char* pszDeviceId, const char* pszTestCaseId, const char* pszExecDevId);
        void ResetCrashStatus();     
	 
}; /* End of RpcMethods */

#endif /* End of RPC_METHODS_H */

