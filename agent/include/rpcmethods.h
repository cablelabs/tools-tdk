/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
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
#define NULL_LOG "/dev/null"
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
        static FILE *sm_pLogStream;
        static int sm_nConsoleLogFlag;
        static int sm_nAgentPID;
        static int sm_nModuleCount;
        static int sm_nRouteSetFlag;
        static int sm_nGetDeviceFlag;
        static int sm_nStatusQueryFlag;
        static int sm_nDeviceStatusFlag;
		
        static const char* sm_szManagerIP;
        static const char* sm_szBoxName;
        static const char* sm_szBoxInterface;
		
        static std::string sm_strBoxIP;
        static std::string sm_strResultId;
        static std::string sm_strLogFolderPath;
        static std::string sm_strTDKPath;
        static std::string sm_strConsoleLogPath;

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
        bool RPCCallEnableTDK(const Json::Value& request, Json::Value& response);
        bool RPCCallDisableTDK(const Json::Value& request, Json::Value& response);
        bool RPCResetAgent (const Json::Value& request, Json::Value& response);
        bool RPCRebootBox (const Json::Value& request, Json::Value& response);
        bool RPCGetRDKVersion (const Json::Value& request, Json::Value& response);
        bool RPCGetAgentConsoleLogPath(const Json::Value& request, Json::Value& response);
        bool RPCPerformanceSystemDiagnostics (const Json::Value& request, Json::Value& response);
        bool RPCPerformanceBenchMarking (const Json::Value& request, Json::Value& response);
        bool RPCExecuteLoggerScript (const Json::Value& request, Json::Value& response);
	bool RPCRemoveLogs (const Json::Value& request, Json::Value& response);
	bool RPCPushLog (const Json::Value& request, Json::Value& response);
	bool RPCUploadLog (const Json::Value& request, Json::Value& response);
	bool RPCGetImageName (const Json::Value& request, Json::Value& response);

        /* Below methods are applicable only for Gateway boxes */
        #ifdef PORT_FORWARD

        bool RPCGetConnectedDevices (const Json::Value& request, Json::Value& response);
        bool RPCSetClientRoute (const Json::Value& request, Json::Value& response);
        bool RPCGetClientMocaIpAddress (const Json::Value& request, Json::Value& response);

        #endif /* End of PORT_FORWARD */

    private:
        RDKTestAgent *m_pAgent;
        int m_iLoadStatus;
        int m_iUnloadStatus;

        void SignalFailureDetails();
        std::string LoadLibrary (char* pszLibName);
        std::string UnloadLibrary (char* pszLibName);
        char* GetHostIPInterface (const char* pszIPaddr);
        bool DeleteModuleFromFile (std::string strLibName);
        void CallReboot();
        void ResetCrashStatus();
        void SetCrashStatus (const char* pszExecId, const char* pszDeviceId, const char* pszTestCaseId, const char* pszExecDevId, const char* pszResultId);
	 
}; /* End of RpcMethods */

#endif /* End of RPC_METHODS_H */

