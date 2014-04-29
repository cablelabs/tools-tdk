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


/* System Includes */
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <dlfcn.h>
#include <map>
#include <typeinfo>
#include <stdio.h>
#include <fstream>
#include <arpa/inet.h>
#include <net/if.h>
#include <ifaddrs.h>
#include <stdio.h>
#include <errno.h>

/* Application Includes */
#include "rpcmethods.h"
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

/* External Variables */
extern 	     std::fstream go_ConfigFile;
extern 	     std::fstream go_PortforwardFile;
extern 	     Json::Rpc::TcpServer go_Server;
bool   	     bBenchmarkEnabled;

/* Constants */
#define LIB_NAME_SIZE 50     // Maximum size of component interface library name
#define COMMAND_SIZE  100    // Maximum size of command
#define ERROR_SIZE    50     // Maximum size of error string
#define BUFFER_SIZE   32     // Maximum size of buffer

#define DEVICE_LIST_FILE     "devicesFile.ini"                 	// File to populate connected devices
#define CRASH_STATUS_FILE    "crashStatus.ini"               	// File to store test details on a device crash
#define REBOOT_CONFIG_FILE   "rebootconfig.ini"            	// File to store the state of test before reboot 

#define GET_DEVICES_SCRIPT   "$TDK_PATH/get_moca_devices.sh"   	// Script to find connected devices
#define SET_ROUTE_SCRIPT     "$TDK_PATH/configure_iptables.sh"  // Script to set port forwarding rules to connected devices
#define SYSSTAT_SCRIPT       "sh $TDK_PATH/runSysStat.sh"	// Script to get system diagnostic info from sar command

typedef void* handler;
typedef std::map <std::string, RDKTestStubInterface*> ModuleMap;

ModuleMap o_gModuleMap;                            // Map to store loaded modules and its handle
ModuleMap::iterator o_gModuleMapIter;

std::fstream so_DeviceFile;

/* Initializations */
int RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;     // Setting status of device as FREE by default

using namespace std;





/********************************************************************************************************************
 Purpose:               This function will return the interface name of corresponding IP address.
 Parameters:   
                             pszIPaddr[IN] - IP address 

 Return:                 Name of the interface if it a valid IP address, else an "NOT VALID" string.

*********************************************************************************************************************/
char* GetHostIPInterface (const char* pszIPaddr)
{
    struct ifaddrs *pAddrs; 
    struct ifaddrs *pAddrIterator;
    int iFlag = FLAG_NOT_SET;
    char szBuffer [BUFFER_SIZE];
    struct sockaddr_in *pSocketAddr;
    std::string strInValid = "NOT VALID";

    getifaddrs(&pAddrs);
	
    /* Going through the linked list to get network interface of correspondin IP address */
    for (pAddrIterator = pAddrs; pAddrIterator != NULL; pAddrIterator = pAddrIterator->ifa_next)
    {
        if ((pAddrIterator->ifa_addr) && 
             (pAddrIterator->ifa_flags & IFF_UP) && 
             (pAddrIterator->ifa_addr->sa_family == AF_INET))
        {
            pSocketAddr = (struct sockaddr_in *) (pAddrIterator->ifa_addr);
            inet_ntop (pAddrIterator->ifa_addr->sa_family, (void *)&(pSocketAddr->sin_addr), szBuffer, sizeof (szBuffer));
            if (!strcmp (pszIPaddr, szBuffer))
            {
                iFlag = FLAG_SET;
                break;
            }
        }
    }
	
    freeifaddrs (pAddrs);
    if (iFlag == FLAG_SET)
    {
        return pAddrIterator->ifa_name;  // Returns the name of interface
    }
    else
    {
        return (char*)strInValid.c_str();   // Returns the string "NOT VALID"
    }
	
} /* End of GetHostIPInterface */





/********************************************************************************************************************
 Purpose:               To dynamically load a module using dlopen. Also, add the module to map for later unloading.
                             It will also invoke "initialize" method of loaded module.
 Parameters:            
                             pszLibName[IN] - Name of the library to be loaded
						
 Return:                 string - string having details of library loading

*********************************************************************************************************************/
std::string RpcMethods::LoadLibrary (char* pszLibName)
{
    void* pvHandle = NULL;
    bool bRet = true;
    char* pszError;
    std::string strLoadLibraryDetails = "Module Loaded Successfully";

    m_iLoadStatus = FLAG_SET;
    pszError = new char [ERROR_SIZE];
    RDKTestStubInterface* (*pfnCreateObject)(void);
    RDKTestStubInterface* pRDKTestStubInterface;
	
    /* Dynamically loading library */
    pvHandle = dlopen (pszLibName, RTLD_LAZY | RTLD_GLOBAL);
    if (!pvHandle)
    {
        pszError = dlerror();
        std::cout << pszError << std::endl;
        std::string strErrorDetails (pszError);
        strLoadLibraryDetails = strErrorDetails; 
		
        m_iLoadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
 
        return strLoadLibraryDetails;        // Return with error details when dlopen fails.
	
    }

    /* Executing  "CreateObject" function of loaded module */
    pfnCreateObject = (RDKTestStubInterface* (*) (void)) dlsym (pvHandle, "CreateObject");
    if ( (pszError = dlerror()) != NULL)
    {
        std::cout << pszError << std::endl;
        strLoadLibraryDetails = "Registering CreateObj Failed";

        m_iLoadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
        return strLoadLibraryDetails;        // Returns with error details when fails to invoke "CreateObject".
		
    }	
    pRDKTestStubInterface = pfnCreateObject();
	
    /* Adding loaded module into map */
    o_gModuleMap.insert (std::make_pair (pszLibName, pRDKTestStubInterface));
	
    /* Executing "initialize" function of loaded module */
    bRet = pRDKTestStubInterface -> initialize ("0.0.1", m_pAgent);
    if(bRet == false)
    {
        strLoadLibraryDetails = "component initialize failed";
	
        m_iLoadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
        return strLoadLibraryDetails;        // Returns with error details when fails to invoke "initialize".
		
    }

    return strLoadLibraryDetails;            // Returns when library loaded successfully.
	
} /* End of LoadLibrary */


/********************************************************************************************************************
 Purpose:              To Unload a module and to remove entry from module map. It will also invoke CleanUp and DestroyObject methods
                            of the module
 Parameters:            
                            pszLibName[IN] - Name of the library to be Unloaded
						
 Return:                string - string having details of library unloading

*********************************************************************************************************************/
std::string RpcMethods::UnloadLibrary (char* pszLibName)
{
    char* pszError;
    bool bRet = true;
    void* pvHandle = NULL;
    std::string strLibName(pszLibName);
    int nMapEntryStatus = FLAG_NOT_SET;
    std::string strUnloadLibraryDetails = "Module Unloaded Successfully";

    void (*pfnDestroyObject) (RDKTestStubInterface*);
    RDKTestStubInterface* pRDKTestStubInterface;
	
    m_iUnloadStatus = FLAG_SET;
    pszError = new char [ERROR_SIZE];	

    /* Parse through module map to find the module */
    for (o_gModuleMapIter = o_gModuleMap.begin(); o_gModuleMapIter != o_gModuleMap.end(); o_gModuleMapIter ++ )
    {
        if (o_gModuleMapIter -> first == strLibName)
        {
            std::cout << "Found Loaded Module : " << strLibName << std::endl;
            nMapEntryStatus = FLAG_SET ;
            break;
        }
    }

    /* Check if module name is present in module map */
    if (nMapEntryStatus == FLAG_NOT_SET)
    {
        std::cout << "Module name not found in Module Map" << std::endl ;
        strUnloadLibraryDetails = "Module name not found in Module Map";
		
        m_iUnloadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
        return strUnloadLibraryDetails;               // Return with error details when module name is not found in module map.

    }


    /* Get the handle of library */
    pvHandle = dlopen (pszLibName, RTLD_LAZY | RTLD_GLOBAL);
    if (!pvHandle)
    {
        pszError = dlerror();
        std::cout << pszError << std::endl ;
        std::string strErrorDetails (pszError);
        strUnloadLibraryDetails = "Load Module for cleanup failed : " + strErrorDetails;
		
        m_iUnloadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
        return strUnloadLibraryDetails;               // Return with error details when dlopen fails.
    }

    /* Calling "DestroyObject" */
    pfnDestroyObject = (void (*)(RDKTestStubInterface*)) dlsym (pvHandle, "DestroyObject");
    if ( (pszError = dlerror()) != NULL)  
    {
        std::cout << pszError << std::endl ;
        std::string strErrorDetails(pszError);
        strUnloadLibraryDetails = "Clean up Failed : " + strErrorDetails;
		
        m_iUnloadStatus = FLAG_NOT_SET;
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
        return strUnloadLibraryDetails;        	
    }
	
    /* Calling CleanUp of module */
    std::cout << "Going to cleanup" << std::endl;
    pRDKTestStubInterface = o_gModuleMapIter -> second;
    bRet = pRDKTestStubInterface -> cleanup ("0.0.1", m_pAgent);
    pfnDestroyObject (pRDKTestStubInterface);

    /* Closing Handle */
    dlclose (pvHandle);
    pvHandle = NULL;
		
    /* Removing map entry */
    o_gModuleMap.erase (o_gModuleMapIter);
	
    return strUnloadLibraryDetails;	

} /* End of UnloadLibrary */


/********************************************************************************************************************
 Purpose:              To store details of test execution in configuration file. So that test agent can report a box crash with these details.
                            It will also set the crash status which would get reset when the test end.
 Parameters:            
                            pszExecId [IN]       - Execution ID
                            pszDeviceId [IN]    - Device ID
                            pszTestCaseId [IN]   - Test Case ID  
						
 Return:                void

*********************************************************************************************************************/
void RpcMethods::SetCrashStatus (const char* pszExecId, const char* pszDeviceId, const char* pszTestCaseId, const char* pszExecDevId )
{
    std::string strEnvPath;
    std::string strFilePath;
    std::ofstream o_CrashStatusFile;

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(CRASH_STATUS_FILE);
    
    o_CrashStatusFile.open (strFilePath.c_str(), ios::out);
		
    /* Writing details into configuration file */ 
    if (o_CrashStatusFile.is_open())
    {
        o_CrashStatusFile << "Crash Status :" << "YES" << std::endl;
        o_CrashStatusFile << "Exec ID :" << pszExecId << std::endl;
        o_CrashStatusFile << "Device ID :" << pszDeviceId << std::endl;
        o_CrashStatusFile << "TestCase ID :" << pszTestCaseId << std::endl;
        o_CrashStatusFile << "ExecDev ID :" << pszExecDevId<< std::endl;
        o_CrashStatusFile.close();
    }
    else
    {
        std::cout << "\nAlert!!! Opening " << SHOW_DEFINE(CRASH_STATUS_FILE) << " failed" << std::endl;
    }

} /* End of SetCrashStatus */



/********************************************************************************************************************
 Purpose:              This finction will reset the crash status in configuration file and delete the configuration file.
                             						
 Return:                void

*********************************************************************************************************************/
void RpcMethods::ResetCrashStatus()
{
    std::string strEnvPath;
    std::string strFilePath;
    std::ofstream o_CrashStatusFile;

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(CRASH_STATUS_FILE);
    
    o_CrashStatusFile.open (strFilePath.c_str(), ios::out);
		
    /* Reseting crash status in configuration file */ 
    if (o_CrashStatusFile.is_open())
    {
        o_CrashStatusFile << "Crash Status :" << "NO" << std::endl;
        o_CrashStatusFile.close();
    }
    else
    {
        std::cout << "\nAlert!!! Opening " << SHOW_DEFINE(CRASH_STATUS_FILE) << " failed" << std::endl;
    }

    /* Delete the configuration file */
    if (remove (strFilePath.c_str()) != 0 )
    {
        std::cout << "\nAlert : Error deleting " << SHOW_DEFINE(CRASH_STATUS_FILE) << " file\n";
    }
    else
    {
        std::cout << std::endl << SHOW_DEFINE(CRASH_STATUS_FILE) << " successfully deleted\n" ;
    }

}/* End of ResetCrashStatus */



/********************************************************************************************************************
 Purpose:               Extract Module name from Json request, load the corresponding module using LoadLibrary() and 
                             send the Json Response. It will also set crash status using SetCrashStatus().
 Parameters:   
                             request [IN]       - Json request to load a module.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE"
 
 Return:                 bool  -      Always returning true from this function, with details in response[result]
 
 Methods of same class used:   LoadLibrary()
                                             SetCrashStatus()

*********************************************************************************************************************/
bool RpcMethods::RPCLoadModule (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    const char* pszExecId = NULL;
    const char* pszDeviceId = NULL;
    const char* pszExecDevId = NULL;
    const char* pszTestCaseId = NULL;
    std::string strLoadModuleDetails;
    char szLibName[LIB_NAME_SIZE];
    const char* pszModuleName = NULL;
    const char* pszBenchMarkingFlag = NULL;
    const char* pszSysDiagFlag = NULL; 
    RpcMethods::sm_nDeviceStatusFlag = DEVICE_BUSY;
    string tdkPath, createNewFile;

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

    std::cout << "\nIn LoadModule\n";
    std::cout << "Received query: " << request << std::endl;
    
    /* Extract module name from json request, construct library name and load that library using LoadLibrary() */
    pszModuleName = request ["param1"].asCString();
    if (NULL != pszModuleName && (LIB_NAME_SIZE - 12) > strlen (pszModuleName))
    {	
	
        sprintf (szLibName, "lib%sstub.so", pszModuleName);
        strLoadModuleDetails = LoadLibrary (szLibName);
    }
    else
    {
        m_iLoadStatus = FLAG_NOT_SET;
        strLoadModuleDetails = "Could not resolve Module Name";
    }

    /* Extracting Execution ID, Device ID and Testcase ID and setting the crash status */   
    if (request["execID"] != Json::Value::null)
    {
        pszExecId = request ["execID"].asCString();    
    }
    if (request["deviceID"] != Json::Value::null)
    {
        pszDeviceId = request ["deviceID"].asCString();    
    }
    if (request["testcaseID"] != Json::Value::null)
    {
        pszTestCaseId = request ["testcaseID"].asCString();    
    }
    if (request["execDevID"] != Json::Value::null)
    {
        pszExecDevId = request ["execDevID"].asCString();    
    }


    /* Construct Json response message with result and details */
    if (m_iLoadStatus == FLAG_SET)
    {
	tdkPath = getenv ("TDK_PATH");	
        if (tdkPath.empty() == 0)
        {
		pszBenchMarkingFlag =  request ["performanceBenchMarkingEnabled"].asCString();
		if (strcmp(pszBenchMarkingFlag,"true")== 0)
		{
             		createNewFile = "cat /dev/null > "+  tdkPath + "/benchmark.log";
               		system(createNewFile.c_str());
               		std::cout << "Creating log file: " << tdkPath << "/benchmark.log" << std::endl;

			bBenchmarkEnabled = true;
		}
		else
		{
			bBenchmarkEnabled = false;
		}

		pszSysDiagFlag =  request ["performanceSystemDiagnosisEnabled"].asCString();
        	if (strcmp(pszSysDiagFlag,"true")== 0)
        	{
			createNewFile = "cat /dev/null > "+  tdkPath + "/systemDiagnostics.log";
               		system(createNewFile.c_str());
               		std::cout << "Creating log file: " << tdkPath << "/systemDiagnostics.log" << std::endl;

			system (SYSSTAT_SCRIPT);
        	}

        	response["result"] = "Success";
        	std::cout << "Module Loaded : " << pszModuleName << std::endl;

        	SetCrashStatus (pszExecId, pszDeviceId, pszTestCaseId, pszExecDevId);
    	}
        else
        {
                std::cout << "Failed to extract environment variable TDK_PATH" << std::endl;
                response["result"] = "FAILURE";
        }
    }	
    else
    {
        response["result"] = "FAILURE";
        std::cout << "Module Loading Failed" << std::endl;
        std::cout << "Failure Details : " << strLoadModuleDetails << std::endl;
    }

    response["details"] = strLoadModuleDetails;
	
    return bRet;
	
} /* End of RPCLoadModule */

/********************************************************************************************************************
 Purpose:               Extract Module name from Json request, Unload the corresponding module using UnloadLibrary() and 
                             send the Json Response.
 Parameters:   
                             request [IN]       - Json request to Unload a specific module.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].
 
 Methods of same class used:   UnloadLibrary()
                                             ResetCrashStatus()

*********************************************************************************************************************/
bool RpcMethods::RPCUnloadModule (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    const char* pszModuleName;
    const char* pszScriptSuiteEnabled;
    char szLibName [LIB_NAME_SIZE];
    std::string strUnloadModuleDetails;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];
 
    std::cout << "\nIn UnloadModule\n";
    std::cout << "Received query: " << request << std::endl;

    /* Extracting module name and constructing corresponding library name */
    pszModuleName = request["param1"].asCString();
    sprintf (szLibName, "lib%sstub.so", pszModuleName);
    std::string strLibName (szLibName);

    /* Invoking UnloadLibrary() to unload module */
    strUnloadModuleDetails = UnloadLibrary (szLibName);

    /* Check the status of unloading and construct corresponding Json response */
    if (m_iUnloadStatus == FLAG_NOT_SET)
    {
        std::cout << "Unloading Module Failed" << std::endl;
        std::cout << "Failure Details : " << strUnloadModuleDetails;
        response["result"] = "FAILURE";
    }	
    else
    {	
        std::cout << "\nModule Unloaded : " << pszModuleName << std::endl;
        response["result"] = "SUCCESS";
    }

    /* Resetting crash status at the end of test */
    ResetCrashStatus();

    response["details"] = strUnloadModuleDetails;

    /* Set device to "FREE" state if ScriptSuiteEnabled is false */
    if (request["ScriptSuiteEnabled"] != Json::Value::null)
    {
        pszScriptSuiteEnabled = request["ScriptSuiteEnabled"].asCString();    
        if (strcmp (pszScriptSuiteEnabled, "true") != 0)
        {
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
        }
    }

    return bRet;
} /* End of RPCUnloadModule */


/********************************************************************************************************************
 Purpose:               To find out currently loaded modules by iterating over the map, add them into configuration
                             file to load them after reboot, unload those modules and reboot the box. 
 Parameters:      
                             request [IN]       - Json request to do a enable box reboot
                             response [OUT]  - Json response with result "SUCCESS/FAILURE"
 
 Return:                 bool  -      Always returning true from this function, with details in response[result]
 
 Methods of same class used:   UnloadLibrary()
                                             ResetCrashStatus()

*********************************************************************************************************************/
bool RpcMethods::RPCEnableReboot (const Json::Value& request, Json::Value& response)
{
    std::cout << "\nGoing to enable box Reboot \n";

    bool bRet = true;
    std::string strEnvPath;
    std::string strFilePath;
    char szLibName [LIB_NAME_SIZE];
    std::string strUnloadModuleDetails;
    std::fstream o_RebootConfigFile;         // File to list the loaded modules before reboot

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = "SUCCESS";

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(REBOOT_CONFIG_FILE);
    
    o_RebootConfigFile.open (strFilePath.c_str(), ios::out);

    /* Iterate over the map to find out currently loaded modules and unload the same */
    for( o_gModuleMapIter = o_gModuleMap.begin(); o_gModuleMapIter != o_gModuleMap.end(); o_gModuleMapIter ++ )
    { 
        sprintf (szLibName, "%s", (o_gModuleMapIter -> first).c_str());
        std::cout << "\nGoing to Unload Library : " << szLibName << std::endl << std::endl; 
        strUnloadModuleDetails = UnloadLibrary (szLibName);
        std::cout << "\nUnload Library Details : " << strUnloadModuleDetails << std::endl;
		
        /* Adding the module names into file */
        if (o_RebootConfigFile.is_open())
        {
            o_RebootConfigFile << szLibName << std::endl;
        }
        else
        {
            std::cout << "Unable to open reboot configuration file" << std::endl;
            response ["result"] = "FAILURE";
            response ["details"] = "Unable to open reboot configuration file";
        }
    }

    o_RebootConfigFile.close();

    /* Resetting crash status before reboot */
    ResetCrashStatus();
	
    response ["result"] = "SUCCESS";
    response ["details"] = "Preconditions  set. Going for a reboot";

    std::cout << "Going for a REBOOT !!!" << std::endl;
    system ("reboot");

    return bRet;
	
} /* End of RPCEnableReboot */


/********************************************************************************************************************
 Purpose:               Get the list of loaded modules from configuration file, load them and delete the configuration file.
                             
 Parameters:      
                             request [IN]       - Json request to do a restore the previous state (state before reboot)
                             response [OUT]  - Json response with result "SUCCESS/FAILURE"
 
 Return:                 bool  -      Always returning true from this function, with details in response[result]
 
 Methods of same class used:   LoadLibrary()

*********************************************************************************************************************/
bool RpcMethods::RPCRestorePreviousState (const Json::Value& request, Json::Value& response)
{
    std::cout << "\n\nRestoring Previous State \n";

    bool bRet = true;
    std::string strEnvPath;
    std::string strFilePath;
    std::string strLineInFile;
    std::string strLoadLibraryDetails;
    std::fstream o_RebootConfigFile;
    char szLibName [LIB_NAME_SIZE];

    const char* pszExecId = NULL;
    const char* pszDeviceId = NULL;
    const char* pszExecDevId = NULL;
    const char* pszTestCaseId = NULL;

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = "SUCCESS";
    response["details"] = "Restored Previous State";

    RpcMethods::sm_nDeviceStatusFlag = DEVICE_BUSY;

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(REBOOT_CONFIG_FILE);
    
    /* Read the module names from configuration file and load those modules */
    o_RebootConfigFile.open (strFilePath.c_str(), ios::in);
    if (o_RebootConfigFile.is_open())
    {
        while (getline (o_RebootConfigFile, strLineInFile))
        {	
            sprintf (szLibName, "%s", strLineInFile.c_str());
            std::cout << "\nGoing to Load Module : " << szLibName << std::endl;
            strLoadLibraryDetails = LoadLibrary (szLibName);	
            std::cout << "\nLoad Module Details : " << strLoadLibraryDetails << std::endl;
        }
		
        o_RebootConfigFile.close();
    }
    else
    {
        std::cout << "Failed to open configuration file" << std::endl;
        response["result"] = "FAILURE";
        response["details"] = "Failed to open configuration file";
    }

    std::cout << "Received query: " << request << std::endl;

    /* Exatracting Ececution ID, Device ID and Testcase ID and setting the crash status after reboot */   
    if (request["execID"] != Json::Value::null)
    {
        pszExecId = request ["execID"].asCString();    
    }
    if (request["deviceID"] != Json::Value::null)
    {
        pszDeviceId = request ["deviceID"].asCString();    
    }
    if (request["testcaseID"] != Json::Value::null)
    {
        pszTestCaseId = request ["testcaseID"].asCString();    
    }
    if (request["execDevID"] != Json::Value::null)
    {
        pszExecDevId = request ["execDevID"].asCString();    
    }

    SetCrashStatus (pszExecId, pszDeviceId, pszTestCaseId,pszExecDevId);

    /* Delete the configuration file */
    if (remove (strFilePath.c_str()) != 0 )
    {
        std::cout << std::endl << "\nAlert : Error in deleting " << SHOW_DEFINE(REBOOT_CONFIG_FILE) ;
    }
    else
    {
        std::cout << std::endl << SHOW_DEFINE(REBOOT_CONFIG_FILE) << " successfully deleted\n\n\n" ;
    }
		
    return bRet;
	
} /* End of RPCRestorePreviousState */




/********************************************************************************************************************
 Purpose:               This function will send the status of the device for getStatus json query.
 
 Parameters:   
                             request [IN]       - Json request to get the status of device.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

 Other Methods used: 
                             GetHostIPInterface()
                             getIP()

*********************************************************************************************************************/
bool RpcMethods::RPCGetHostStatus (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    char* pszInterface;
    std::string strEnvPath;
    std::string strFilePath;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
	
    /* Finding Test Manager IP and box name from JSON message */
    if ( (request["managerIP"] != Json::Value::null) && 
          (strcmp((request["managerIP"].asCString()),"NULL") != 0) )
    {		
        RpcMethods::sm_szManagerIP = (request["managerIP"].asCString());	
    }

    if ( (request["boxName"] != Json::Value::null) &&
          (strcmp((request["boxName"].asCString()),"NULL") != 0) )
    {		
        RpcMethods::sm_szBoxName = (request["boxName"].asCString());
    }

    /* For the first status query, Test Manager IP address, Box name and connected box interface will
        be written into configuration file */
    if ( (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET) &&
          (strcmp ( (request["boxName"].asCString()), "NULL") != 0) && 
          (strcmp ( (request["managerIP"].asCString()), "NULL") != 0) )
    {	
        /* Fetching the connected box IP address */
        RpcMethods::sm_strBoxIP = go_Server.getIP();
		
        /* Getting corresponding network interface */
        pszInterface = GetHostIPInterface (RpcMethods::sm_strBoxIP.c_str());
        if (strcmp (pszInterface, "NOT VALID"))
        {
            RpcMethods::sm_szBoxInterface = pszInterface;

            /* Extracting file path */
            strEnvPath = getenv ("TDK_PATH");
            strFilePath.append(strEnvPath);
            strFilePath.append("/");
            strFilePath.append(CONFIGURATION_FILE);
			
            /* Writing details into configuration file */
            go_ConfigFile.open (strFilePath.c_str(), ios::out);
            if (go_ConfigFile.is_open())
            {
                go_ConfigFile << "Manager IP:" << RpcMethods::sm_szManagerIP << std::endl;
                go_ConfigFile << "Box Name :" << RpcMethods::sm_szBoxName << std::endl;
                go_ConfigFile << "Box Interface:" << RpcMethods::sm_szBoxInterface << std::endl;
                go_ConfigFile.close();
            }
        }
        else
        {
            std::cout << "\nInterface or Box IP not Valid!!! " << std::endl;
        }
	
        RpcMethods::sm_nStatusQueryFlag = FLAG_SET;
    }
		
    /* Sending the device status */	
    if (RpcMethods::sm_nDeviceStatusFlag == DEVICE_FREE)
    {
        response["result"] = "Device Free";
    }
    else if (RpcMethods::sm_nDeviceStatusFlag == DEVICE_BUSY)
    {
        response["result"] = "Device Busy";
    }
	
    return bRet;
	
} /* End of RPCGetHostStatus */



/********************************************************************************************************************
 Purpose:               To reset agent when there is a timeout. It will send custom signal (SIGUSR1) to agent process.
 Parameters:   
                             request [IN]       - Json request to get the list of connected devices.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function.

*********************************************************************************************************************/
bool RpcMethods::RPCResetAgent (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    int nReturnValue ;
    std::string strEnableReset;
    const char* pszEnableReset = NULL;

    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

    if (request["enableReset"] != Json::Value::null)
    {
        pszEnableReset = request ["enableReset"].asCString();  
        strEnableReset = std::string(pszEnableReset);
    }

    /* Restart Agent if true */
    if (strEnableReset == "true")
    {
	std::cout << "\n\nAgent Restarting...\n";
        nReturnValue = kill (RpcMethods::sm_nAgentPID, SIGKILL);
        if (nReturnValue == RETURN_SUCCESS)
        {
            response["result"] = "SUCCESS";
        }
        else
        {
            std::cout << "Alert!!! Unable to restart agent" << std::endl;
            response["result"] = "FAILURE";
        }
    }
    /* Set device state to FREE on script exits abruptly */
    else if (strEnableReset == "false")
    {
        response["result"] = "SUCCESS";
        nReturnValue = kill (RpcMethods::sm_nAgentPID, SIGUSR2);
        if (nReturnValue == RETURN_SUCCESS)
        {
            response["result"] = "SUCCESS";
        }
        
    }
    else
    {
        std::cout << "Alert!!! Unable to reset Agent..Unknown Parameter" << std::endl;
        response["result"] = "FAILURE";
    }

    if (nReturnValue != RETURN_SUCCESS)
    {
        std::cout << "Alert!!! Unable to reset Agent" << std::endl;
        std::cout << "Details : ";
        switch(errno)
        {
            case EINVAL :
                        std::cout << "The value of sig is incorrect or is not the number of a supported signal" << std::endl; 
                        break;
				
            case EPERM :
                        std::cout << "The caller does not have permission to send the signal to any process specified by pid" << std::endl;
                        break;
    
            case ESRCH : 
	                 std::cout << "No processes or process groups correspond to pid" << std::endl;  
                        break;
        }
         
        response["result"] = "FAILURE";
		
    }
        
    return bRet;

}/* End of RPCResetAgent */


/********************************************************************************************************************
 Purpose:               
 
 Parameters:   
                             request [IN]       - Json request.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

 Other Methods used: 

*********************************************************************************************************************/
bool RpcMethods::RPCPerformanceBenchMarking (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    string tdkPath, logPath;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];
 
    std::cout << "\nIn RPCPerformanceBenchMarking\n";
    std::cout << "Received query: " << request << std::endl;

    tdkPath = getenv ("TDK_PATH");
    logPath = tdkPath+"/benchmark.log";

    if (std::ifstream(logPath.c_str()))
    {
        response["result"]  = "SUCCESS";
    }
    else
    {
        std::cout << "Error!!! benchmark.log not found" << std::endl;
        response["result"]  = "FAILURE";
    }

    response["logpath"] = logPath.c_str();

    return bRet;
	
} /* End of RPCPerformanceBenchMarking */



/********************************************************************************************************************
 Purpose:               
 
 Parameters:   
                             request [IN]       - Json request.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

 Other Methods used: 

*********************************************************************************************************************/
bool RpcMethods::RPCPerformanceSystemDiagnostics (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    string tdkPath, logPath;	

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];

    std::cout << "\nIn RPCPerformanceSystemDiagnostics\n";
    std::cout << "Received query: " << request << std::endl;
    	
    tdkPath = getenv ("TDK_PATH");
    logPath = tdkPath+"/systemDiagnostics.log";

    if (std::ifstream(logPath.c_str()))
    {
       	response["result"]  = "SUCCESS";
    }
    else
    {
       	std::cout << "Error!!! systemDiagnostics.log not found" << std::endl;
       	response["result"]  = "FAILURE";
    }

    response["logpath"] = logPath.c_str();
    
    return bRet;
	
} /* End of RPCPerformanceSystemDiagnostics */




/* To enable port forwarding. In gateway boxes only  */
#ifdef PORT_FORWARD


/********************************************************************************************************************
 Purpose:               This function calls a script to get the MAC address of all connected client devices.
 Parameters:   
                             request [IN]       - Json request to get the list of connected devices.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

*********************************************************************************************************************/
bool RpcMethods::RPCGetConnectedDevices (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    std::string strEnvPath;
    std::string strFilePath;
    std::string strClientMAC;
    std::string strDeviceList = "DEVICES=";
    std::string strDelimiter = ",";
    char szCommand[COMMAND_SIZE];

    /* Extracting file path */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(DEVICE_LIST_FILE);

    /* Constructing the command to invoke script */
    sprintf (szCommand, "%s %s", SHOW_DEFINE(GET_DEVICES_SCRIPT), DEVICE_LIST_FILE); //Constructing Command

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

    if (RpcMethods::sm_nGetDeviceFlag == FLAG_NOT_SET)
    {
        RpcMethods::sm_nGetDeviceFlag = FLAG_SET;
        system (szCommand); //Calling the getdevices script
        sleep (2);

        /* Parsing the device list file to get the mac address of connected devices */
        so_DeviceFile.open (strFilePath.c_str(),ios::in);
        if (so_DeviceFile.is_open())
        {
            while (getline (so_DeviceFile, strClientMAC))
            {
                strDeviceList += strClientMAC;
                strDeviceList += strDelimiter;
            }
			
            /* Sending mac addresses to Test Manager */
            response["result"] = strDeviceList;
        }
        else
        {
            response["result"] = "NO_DEVICES";
        }

        so_DeviceFile.close();
        RpcMethods::sm_nGetDeviceFlag = FLAG_NOT_SET;
    }
    else
    {
        response["result"] = "FAILURE";
    }
	
    return bRet;

} /* End of RPCGetConnectedDevices */


/********************************************************************************************************************
 Purpose:               This function calls a script to set the route to client device.
 Parameters:   
                             request [IN]       - Json request to set the route to connected client device.
                             response [OUT]  - Json response with result "SUCCESS/FAILURE".
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

*********************************************************************************************************************/
bool RpcMethods::RPCSetClientRoute (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    std::string strEnvPath;
    std::string strFilePath;
    const char* pszAgentPort;
    const char* pszStatusPort;
    const char* pszLogTransferPort;
    const char* pszAgentMonitorPort;
    const char* pszClientMAC = NULL;
    char szCommand[COMMAND_SIZE];

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

    if (RpcMethods::sm_nRouteSetFlag == FLAG_NOT_SET)
    {
        /* Getting MAC address and port numbers from Test Manager */
        RpcMethods::sm_nRouteSetFlag = FLAG_SET;	
        if (request["MACaddr"] != Json::Value::null)
        {		
            pszClientMAC = request["MACaddr"].asCString();
        }
        if (request["agentPort"] != Json::Value::null)
        {			
            pszAgentPort = request["agentPort"].asCString();
        }
        if (request["statusPort"] != Json::Value::null)
        {		
            pszStatusPort = request["statusPort"].asCString();
        }
        if (request["logTransferPort"] != Json::Value::null)
        {		
            pszLogTransferPort = request["logTransferPort"].asCString();
        }
        if (request["agentMonitorPort"] != Json::Value::null)
        {		
            pszAgentMonitorPort = request["agentMonitorPort"].asCString();
        }

        /* Constructing command */
        sprintf (szCommand, "%s %s %s %s %s %s", SHOW_DEFINE(SET_ROUTE_SCRIPT), pszClientMAC, pszAgentPort, pszStatusPort, pszLogTransferPort, pszAgentMonitorPort); 

        /* Extracting path to file */
        strEnvPath = getenv ("TDK_PATH");
        strFilePath.append(strEnvPath);
        strFilePath.append("/");
        strFilePath.append(PORT_FORWARD_RULE_FILE);
    
        /* Adding command to configuration file to set route accross reboot */
        go_PortforwardFile.open (strFilePath.c_str(), ios::out | ios::app);
        if (go_PortforwardFile.is_open())
        {
            go_PortforwardFile << pszClientMAC << "=" << szCommand << std::endl;
            go_PortforwardFile.close();
        }
        else
        {
            std::cout << "\nAlert!!! Opening " << SHOW_DEFINE(PORT_FORWARD_RULE_FILE) << " failed" << std::endl;
        }

        std::cout << "Setting route for " << pszClientMAC << std::endl;
	
        system (szCommand); //Calling script
		
        response["result"] = "SUCCESS";
        RpcMethods::sm_nRouteSetFlag = FLAG_NOT_SET;	
    }
    else
    {
        response["result"] = "FAILURE";		
    }

    return bRet;
} /* End of RPCSetClientRoute */


#endif /* PORT_FORWARD */



/* End of rpcmethods */



