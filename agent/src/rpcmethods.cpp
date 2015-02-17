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
#include <errno.h>
#include <algorithm>

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
#define LIB_NAME_SIZE 50       // Maximum size of component interface library name
#define COMMAND_SIZE  100    // Maximum size of command
#define ERROR_SIZE    50         // Maximum size of error string
#define BUFFER_SIZE   32        // Maximum size of buffer

#define DEVICE_LIST_FILE     "devicesFile.ini"                 	// File to populate connected devices
#define CRASH_STATUS_FILE    "crashStatus.ini"               	// File to store test details on a device crash
#define REBOOT_CONFIG_FILE   "rebootconfig.ini"            	// File to store the state of test before reboot 
#define MODULE_LIST_FILE     "modulelist.ini"            	// File to store list of loaded modules 
#define BENCHMARKING_FILE    "benchmark.log"
#define SYSDIAGNOSTIC_FILE   "systemDiagnostics.log"
#define SYSSTATAVG_FILE      "sysStatAvg.log"

#define GET_DEVICES_SCRIPT   "$TDK_PATH/get_moca_devices.sh"      // Script to find connected devices
#define SET_ROUTE_SCRIPT     "$TDK_PATH/configure_iptables.sh"        // Script to set port forwarding rules to connected devices
#define SYSSTAT_SCRIPT       "sh $TDK_PATH/runSysStat.sh"	          // Script to get system diagnostic info from sar command
#define NULL_LOG_FILE        "cat /dev/null > "

#ifndef RDKVERSION
#define RDKVERSION "NOT_DEFINED"       
#endif

/* Structure to hold module details */
struct sModuleDetails 
{
    std::string strModuleName;
    RDKTestStubInterface* pRDKTestStubInterface;
};

using namespace std;

typedef void* handler;
typedef std::map <int, sModuleDetails> ModuleMap;

ModuleMap o_gModuleMap;                            // Map to store loaded modules and its handle
ModuleMap::iterator o_gModuleMapIter;

/* To enable port forwarding. In gateway boxes only  */
#ifdef PORT_FORWARD

    /* Map to hold details of client devices */
    typedef std::map <std::string, std::string> ClientDeviceMap;
    extern ClientDeviceMap o_gClientDeviceMap;
    extern ClientDeviceMap::iterator o_gClientDeviceMapIter;

#endif /* PORT_FORWARD */


/* Initializations */
static int nModuleId = 0;  
std::fstream so_DeviceFile;
int RpcMethods::sm_nModuleCount = 0;                                  // Setting Module count to 0 
std::string RpcMethods::sm_strResultId = "0000";
int RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;        // Setting status of device as FREE by default
std::string RpcMethods::sm_strConsoleLogPath = "";


/********************************************************************************************************************
 Purpose:               This function will return the interface name of corresponding IP address.
 Parameters:   
                             pszIPaddr[IN] - IP address 

 Return:                 Name of the interface if it a valid IP address, else an "NOT VALID" string.

*********************************************************************************************************************/
char* RpcMethods::GetHostIPInterface (const char* pszIPaddr)
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
 Purpose:               To print details for the failure of raising a signal.
 
 Parameters:          Nil
                          
 Return:                 Nil

*********************************************************************************************************************/
void RpcMethods::SignalFailureDetails()
{

    DEBUG_PRINT (DEBUG_TRACE, "\nSignal Failure Details --> Entry\n");
	
    DEBUG_PRINT (DEBUG_ERROR, "Details : ");
    switch(errno)
    {
        case EINVAL :
                    DEBUG_PRINT (DEBUG_ERROR, "The value of sig is incorrect or is not the number of a supported signal \n");
                    break;
				
        case EPERM :
                    DEBUG_PRINT (DEBUG_ERROR, "The caller does not have permission to send the signal to any process specified by pid \n");
                    break;
    
        case ESRCH : 
                    DEBUG_PRINT (DEBUG_ERROR, "No processes or process groups correspond to pid \n");  
                    break;
    }

    DEBUG_PRINT (DEBUG_TRACE, "\nSignal Failure Details --> Exit\n");
         	
} /* End of SignalFailureDetails */



/********************************************************************************************************************
 Purpose:               To delete a module name from module list file
 
 Parameters:            
                             strLibName[IN] - Name of the library to be deleted from file.
						
 Return:                 bool - true/false

*********************************************************************************************************************/
bool RpcMethods::DeleteModuleFromFile (std::string strLibName)
{
    bool bRet = true;
    std::string strLine;
    std::string strFilePath;
    std::string strTempFilePath;
    std::ifstream o_ModuleListFile;
    std::ofstream o_TempFile;
	
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(MODULE_LIST_FILE);
    strTempFilePath.append("temp.txt");
	
    o_ModuleListFile.open (strFilePath.c_str());
    o_TempFile.open (strTempFilePath.c_str());

    while (getline(o_ModuleListFile, strLine))
    {
        if (strLine != strLibName)
        {
            o_TempFile << strLine << std::endl;
        }
    }
	
    o_ModuleListFile.close();
    o_TempFile.close();
    remove(strFilePath.c_str());
    rename(strTempFilePath.c_str(), strFilePath.c_str());

    return bRet;

}



/********************************************************************************************************************
 Purpose:               To dynamically load a module using dlopen. Also, add the module to map for later unloading.
                             It will also invoke "initialize" method of loaded module.
 Parameters:            
                             pszLibName[IN] - Name of the library to be loaded
						
 Return:                 string - string having details of library loading

*********************************************************************************************************************/
std::string RpcMethods::LoadLibrary (char* pszLibName)
{
    size_t nPos = 0;
    char* pszError;
    bool bRet = true;
    void* pvHandle = NULL;
    int nMapEntryStatus = FLAG_NOT_SET;
    std::string strFilePath;
    std::string strDelimiter;
    std::fstream o_ModuleListFile;
    std::string strPreRequisiteStatus;
    std::string strPreRequisiteDetails;
    std::string strLibName(pszLibName);
    std::string strLoadLibraryDetails = "Module Loaded Successfully";

    DEBUG_PRINT (DEBUG_TRACE, "\nLoad Library --> Entry\n");

    m_iLoadStatus = FLAG_SET;
    pszError = new char [ERROR_SIZE];
    RDKTestStubInterface* (*pfnCreateObject)(void);
    RDKTestStubInterface* pRDKTestStubInterface;

    do
    {   
        /* Dynamically loading library */
        pvHandle = dlopen (pszLibName, RTLD_LAZY | RTLD_GLOBAL);		
        if (!pvHandle)
        {
            pszError = dlerror();
            DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
            std::string strErrorDetails (pszError);
            strLoadLibraryDetails = strErrorDetails; 
		
            m_iLoadStatus = FLAG_NOT_SET;
			
            break;                                            // Return with error details when dlopen fails.
        }

        /* Executing  "CreateObject" function of loaded module */
        pfnCreateObject = (RDKTestStubInterface* (*) (void)) dlsym (pvHandle, "CreateObject");
        if ( (pszError = dlerror()) != NULL)
        {
            DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
            strLoadLibraryDetails = "Registering CreateObj Failed";

            m_iLoadStatus = FLAG_NOT_SET;
			
            break;                                         // Returns with error details when fails to invoke "CreateObject".
		
        }	
		
        pRDKTestStubInterface = pfnCreateObject();
		
        /* Executing "testmodulepre_requisites" function of loaded module to enable pre-requisites */
        strPreRequisiteDetails = pRDKTestStubInterface -> testmodulepre_requisites ();
	 std::transform(strPreRequisiteDetails.begin(), strPreRequisiteDetails.end(), strPreRequisiteDetails.begin(), ::toupper);

        if (strPreRequisiteDetails.find("SUCCESS") != std::string::npos) 
        {
            DEBUG_PRINT (DEBUG_LOG, "Pre-Requisites set successfully \n");
        }
        else
        {
            strDelimiter = "<DETAILS>";
            while ( (nPos = strPreRequisiteDetails.find (strDelimiter)) != std::string::npos)
            {
                strPreRequisiteStatus = strPreRequisiteDetails.substr (0, nPos);
                strPreRequisiteDetails.erase (0, nPos + strDelimiter.length());
            }

            DEBUG_PRINT (DEBUG_LOG, "Setting Pre-Requisites Failed \n");
            DEBUG_PRINT (DEBUG_LOG, "Details : %s \n", strPreRequisiteDetails.c_str());

            strLoadLibraryDetails = strPreRequisiteDetails;
	
            m_iLoadStatus = FLAG_NOT_SET;

            break;                                        // Returns with error details when fails to invoke "testmodulepre_requisites".

        }

        nModuleId = nModuleId + 1;
        sModuleDetails o_ModuleDetails;
        o_ModuleDetails.strModuleName = pszLibName;
        o_ModuleDetails.pRDKTestStubInterface = pRDKTestStubInterface;
        o_gModuleMap.insert (std::make_pair (nModuleId, o_ModuleDetails));
	
        /* Executing "initialize" function of loaded module */
        bRet = pRDKTestStubInterface -> initialize ("0.0.1", m_pAgent);
        if (bRet == false)
        {
            strLoadLibraryDetails = "component initialize failed";
	
            m_iLoadStatus = FLAG_NOT_SET;

            break;                                        // Returns with error details when fails to invoke "initialize".
		
        }

        RpcMethods::sm_nModuleCount = RpcMethods::sm_nModuleCount + 1;    // Incrementing module count

        /* Extracting path to file */
        strFilePath = RpcMethods::sm_strTDKPath;
        strFilePath.append(MODULE_LIST_FILE);
 
        o_ModuleListFile.open (strFilePath.c_str(), ios::out | ios::app);

        /* Adding the module names into file */
        if (o_ModuleListFile.is_open())
        {
            o_ModuleListFile << pszLibName << std::endl;
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "Unable to open Module List file \n");
        }
   
        o_ModuleListFile.close();    
		
    }while(0);
	
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
    DEBUG_PRINT (DEBUG_TRACE, "\nUnload Library --> Entry\n");

    char* pszError;
    bool bRet = true;
    void* pvHandle = NULL;
    std::string strFilePath;
    std::string strLibName(pszLibName);
    int nMapEntryStatus = FLAG_NOT_SET;
    std::string strUnloadLibraryDetails = "Module Unloaded Successfully";

    void (*pfnDestroyObject) (RDKTestStubInterface*);
    RDKTestStubInterface* pRDKTestStubInterface;
	
    m_iUnloadStatus = FLAG_SET;
    pszError = new char [ERROR_SIZE];	

    do
    {
        sModuleDetails o_ModuleDetails;
   
        /* Parse through module map to find the module */
        for (o_gModuleMapIter = o_gModuleMap.begin(); o_gModuleMapIter != o_gModuleMap.end(); o_gModuleMapIter ++ )
        {
            o_ModuleDetails = o_gModuleMapIter -> second;
            if (o_ModuleDetails.strModuleName == strLibName)
            {
                DEBUG_PRINT (DEBUG_LOG, "Found Loaded Module : %s \n", strLibName.c_str());
		  pRDKTestStubInterface = o_ModuleDetails.pRDKTestStubInterface;
                nMapEntryStatus = FLAG_SET ;
                break;
            }
        }
		
        /* Check if module name is present in module map */
        if (nMapEntryStatus == FLAG_NOT_SET)
        {
            DEBUG_PRINT (DEBUG_ERROR, "Module name not found in Module Map \n");
            strUnloadLibraryDetails = "Module name not found in Module Map";
		
            m_iUnloadStatus = FLAG_NOT_SET;
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
            break;               // Return with error details when module name is not found in module map.

        }

        RpcMethods::sm_nModuleCount = RpcMethods::sm_nModuleCount - 1;    // Decrementing module count

        /* Get the handle of library */
        pvHandle = dlopen (pszLibName, RTLD_LAZY | RTLD_GLOBAL);
        if (!pvHandle)
        {
            pszError = dlerror();
            DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
            std::string strErrorDetails (pszError);
            strUnloadLibraryDetails = "Load Module for cleanup failed : " + strErrorDetails;
		
            m_iUnloadStatus = FLAG_NOT_SET;
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
            break;               // Return with error details when dlopen fails.
        }

        /* Calling "DestroyObject" */
        pfnDestroyObject = (void (*)(RDKTestStubInterface*)) dlsym (pvHandle, "DestroyObject");
        if ( (pszError = dlerror()) != NULL)  
        {
            DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
            std::string strErrorDetails(pszError);
            strUnloadLibraryDetails = "Clean up Failed : " + strErrorDetails;
		
            m_iUnloadStatus = FLAG_NOT_SET;
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
		
            break;        	
        }
	
        /* Calling CleanUp of module */
        DEBUG_PRINT (DEBUG_LOG, "Going to cleanup \n");
        bRet = pRDKTestStubInterface -> testmodulepost_requisites();
        bRet = pRDKTestStubInterface -> cleanup ("0.0.1", m_pAgent);
        pfnDestroyObject (pRDKTestStubInterface);

        bRet = DeleteModuleFromFile(strLibName);

        /* Closing Handle */
        dlclose (pvHandle);
        pvHandle = NULL;
		
        /* Removing map entry */
        o_gModuleMap.erase (o_gModuleMapIter);


    }while(0);	

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
void RpcMethods::SetCrashStatus (const char* pszExecId, const char* pszDeviceId, const char* pszTestCaseId, const char* pszExecDevId, const char* pszResultId)
{
    std::string strFilePath;
    std::ofstream o_CrashStatusFile;

    DEBUG_PRINT (DEBUG_TRACE, "\nSet Crash Status --> Entry\n");

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
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
        o_CrashStatusFile << "Result ID :" << pszResultId << std::endl;
        o_CrashStatusFile.close();
    }
    else
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Opening %s failed \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
    }

} /* End of SetCrashStatus */



/********************************************************************************************************************
 Purpose:              This finction will reset the crash status in configuration file and delete the configuration file.
                             						
 Return:                void

*********************************************************************************************************************/
void RpcMethods::ResetCrashStatus()
{
    std::string strFilePath;
    std::ofstream o_CrashStatusFile;

    DEBUG_PRINT (DEBUG_TRACE, "\nReset Crash Status --> Entry\n");

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
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
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Opening %s failed \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
    }

    /* Delete the configuration file */
    if (remove (strFilePath.c_str()) != 0 )
    {
        DEBUG_PRINT (DEBUG_ERROR, "\nAlert : Error deleting %s file \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "\n%s successfully deleted \n", SHOW_DEFINE(CRASH_STATUS_FILE) );
    }

}/* End of ResetCrashStatus */


/********************************************************************************************************************
 Purpose:              To reboot device.
                             						
 Return:                void

*********************************************************************************************************************/
void RpcMethods::CallReboot()
{
    DEBUG_PRINT (DEBUG_ERROR, "Going for a REBOOT !!!\n\n");
    system ("sleep 10 && reboot &");
	
} /* End of CallReboot */



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

    std::string strFilePath;
    std::string strLoadModuleDetails;
    std::string strNullLog;

    char szLibName[LIB_NAME_SIZE];
    char szCommand[COMMAND_SIZE];
	
    const char* pszExecId = NULL;
    const char* pszResultId = NULL;
    const char* pszDeviceId = NULL;
    const char* pszExecDevId = NULL;
    const char* pszTestCaseId = NULL;
    const char* pszSysDiagFlag = NULL; 
    const char* pszModuleName = NULL;
    const char* pszBenchMarkingFlag = NULL;
	
    RpcMethods::sm_nDeviceStatusFlag = DEVICE_BUSY;

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

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
    if (request["resultID"] != Json::Value::null)
    {
        pszResultId = request ["resultID"].asCString();    
    }

    strNullLog = std::string(NULL_LOG_FILE) + RpcMethods::sm_strTDKPath;
    strNullLog.append(BENCHMARKING_FILE);
    system(strNullLog.c_str());

    strNullLog = std::string(NULL_LOG_FILE) + RpcMethods::sm_strTDKPath;
    strNullLog.append(SYSDIAGNOSTIC_FILE);
    system(strNullLog.c_str());

    strNullLog = std::string(NULL_LOG_FILE) + RpcMethods::sm_strTDKPath;
    strNullLog.append(SYSSTATAVG_FILE);
    system(strNullLog.c_str());

	
    /* Check whether sm_nConsoleLogFlag is set, if it is set the redirect console log to a file */
    if(RpcMethods::sm_nConsoleLogFlag ==FLAG_SET)
    {
        /* Redirecting stderr buffer to stdout */
        dup2(fileno(stdout), fileno(stderr));

        /* Checking if it is a new execution, If it is new clear old logfile and create a new one */
        if (strcmp (pszResultId, RpcMethods::sm_strResultId.c_str()) != 0)
        {
            /* Copying result id to a static variable */
            RpcMethods::sm_strResultId = pszResultId;
	
            /* Clear old log files */
            sprintf (szCommand, "rm -rf %s/*", RpcMethods::sm_strLogFolderPath.c_str()); //Constructing Command
            system (szCommand);
            sleep(1);

            /* Constructing path to new log file */
            strFilePath = RpcMethods::sm_strLogFolderPath;
            strFilePath.append("AgentConsole.log");

            RpcMethods::sm_strConsoleLogPath = strFilePath;

            /* Redirecting stdout buffer to logfile */
            if((RpcMethods::sm_pLogStream = freopen(RpcMethods::sm_strConsoleLogPath.c_str(), "w", stdout)) == NULL)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to redirect console logs\n");
            }	
        }
        else
        {
            /* If it is an existing execution, Append to the existing file */
            if((RpcMethods::sm_pLogStream = freopen(RpcMethods::sm_strConsoleLogPath.c_str(), "a", stdout)) == NULL)
            {
                DEBUG_PRINT (DEBUG_ERROR, "Failed to redirect console logs\n");
            }
        }
    }	
	
    fprintf(stdout,"\nStarting Execution..\n");
	
    DEBUG_PRINT (DEBUG_LOG, "\nRPC Load Module --> Entry \n");
    //DEBUG_PRINT (DEBUG_LOG, "Received query: %s \n", request.asCString().c_str());
    cout << "Received query: \n" << request << endl;
    
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

    /* Construct Json response message with result and details */
    if (m_iLoadStatus == FLAG_SET)
    {
        pszBenchMarkingFlag =  request ["performanceBenchMarkingEnabled"].asCString();
        if (strcmp(pszBenchMarkingFlag,"true") == 0)
        {
                bBenchmarkEnabled = true;
        }
        else
        {
                bBenchmarkEnabled = false;
        }

        pszSysDiagFlag =  request ["performanceSystemDiagnosisEnabled"].asCString();
        if (strcmp(pszSysDiagFlag,"true") == 0)
        {
    		system (SYSSTAT_SCRIPT);
        }
			
        response["result"] = "Success";
        DEBUG_PRINT (DEBUG_LOG, "Module Loaded : %s \n",pszModuleName);

        SetCrashStatus (pszExecId, pszDeviceId, pszTestCaseId, pszExecDevId, pszResultId);
    }
    else
    {
        response["result"] = "FAILURE";
        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
        DEBUG_PRINT (DEBUG_ERROR, "Module Loading Failed \n");
        DEBUG_PRINT (DEBUG_ERROR, "Failure Details : %s", strLoadModuleDetails.c_str());
    }

    response["details"] = strLoadModuleDetails;

    DEBUG_PRINT (DEBUG_LOG, "\nRPC Load Module --> Exit \n"); 
	
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
    void* pvHandle = NULL;
    const char* pszModuleName;
    const char* pszScriptSuiteEnabled;
    char szLibName [LIB_NAME_SIZE];
    std::string strUnloadModuleDetails;
    int nReturnValue = RETURN_SUCCESS;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];
 
    DEBUG_PRINT (DEBUG_LOG, "\nRPC Unload Module --> Entry\n");
    //DEBUG_PRINT (DEBUG_LOG, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;
	
    /* Extracting module name and constructing corresponding library name */
    pszModuleName = request["param1"].asCString();
    sprintf (szLibName, "lib%sstub.so", pszModuleName);
    std::string strLibName (szLibName);

    /* Invoking UnloadLibrary() to unload module */
    strUnloadModuleDetails = UnloadLibrary (szLibName);

    /* Check the status of unloading and construct corresponding Json response */
    if (m_iUnloadStatus == FLAG_NOT_SET)
    {
        DEBUG_PRINT (DEBUG_ERROR, "Unloading Module Failed \n");
        DEBUG_PRINT (DEBUG_ERROR, "Failure Details : %s \n", strUnloadModuleDetails.c_str());
        response["result"] = "FAILURE";
    }	
    else
    {	
        DEBUG_PRINT (DEBUG_LOG, "\nModule Unloaded : %s \n", pszModuleName);
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

    DEBUG_PRINT (DEBUG_LOG, "\nRPC Unload Module --> Exit \n"); 

    /* Check whether sm_nConsoleLogFlag is set, if it is set then close console log output file */
    if (RpcMethods::sm_nConsoleLogFlag == FLAG_SET)
    {
        if(RpcMethods::sm_nModuleCount == 0)  // Checking if all loaded modules are unloaded
        {
            fclose(RpcMethods::sm_pLogStream);
            RpcMethods::sm_pLogStream = freopen (NULL_LOG, "w", stdout);
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
    DEBUG_PRINT (DEBUG_TRACE, "\nRPC Enable Reboot --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

    DEBUG_PRINT (DEBUG_LOG, "\nGoing to enable box Reboot \n");

    bool bRet = true;
    std::string strFilePath;
    char szLibName [LIB_NAME_SIZE];
    std::string strUnloadModuleDetails;
    std::fstream o_RebootConfigFile;         // File to list the loaded modules before reboot

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = "SUCCESS";

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(REBOOT_CONFIG_FILE);

    o_RebootConfigFile.open (strFilePath.c_str(), ios::out);

    /* Iterate over the map to find out currently loaded modules and unload the same */

   sModuleDetails o_ModuleDetails;
   
   /* Parse through module map to find the module */
   for (o_gModuleMapIter = o_gModuleMap.begin(); o_gModuleMapIter != o_gModuleMap.end(); o_gModuleMapIter ++ )
   {
        o_ModuleDetails = o_gModuleMapIter -> second;
        sprintf (szLibName, "%s", o_ModuleDetails.strModuleName.c_str());
   
        DEBUG_PRINT (DEBUG_LOG, "\nGoing to Unload Library : %s \n\n", szLibName); 
        strUnloadModuleDetails = UnloadLibrary (szLibName);
        DEBUG_PRINT (DEBUG_LOG, "\nUnload Library Details : %s \n", strUnloadModuleDetails.c_str());
		
        /* Adding the module names into file */
        if (o_RebootConfigFile.is_open())
        {
            o_RebootConfigFile << szLibName << std::endl;
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "Unable to open reboot configuration file \n");
            response ["result"] = "FAILURE";
            response ["details"] = "Unable to open reboot configuration file";
        }
    }

    o_RebootConfigFile.close();

    /* Resetting crash status before reboot */
    ResetCrashStatus();
	
    response ["result"] = "SUCCESS";
    response ["details"] = "Preconditions  set. Going for a reboot";

    CallReboot();

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
    bool bRet = true;
    std::string strFilePath;
    std::string strLineInFile;
    std::string strLoadLibraryDetails;
    std::fstream o_RebootConfigFile;
    char szLibName [LIB_NAME_SIZE];
    int nReturnValue = RETURN_SUCCESS;

    const char* pszExecId = NULL;
    const char* pszResultId = NULL;
    const char* pszDeviceId = NULL;
    const char* pszExecDevId = NULL;
    const char* pszTestCaseId = NULL;

    /* Prepare JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = "SUCCESS";
    response["details"] = "Restored Previous State";

    RpcMethods::sm_nDeviceStatusFlag = DEVICE_BUSY;

    /* Extracting Ececution ID, Device ID and Testcase ID */   
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
    if (request["resultID"] != Json::Value::null)
    {
        pszResultId = request ["resultID"].asCString();    
    }

    /*Check whether sm_nConsoleLogFlag is set, if it is set then redirect console log to a file */
    if (RpcMethods::sm_nConsoleLogFlag == FLAG_SET)
    {
        /* Extracting file to log file */
        strFilePath = RpcMethods::sm_strLogFolderPath;
        strFilePath.append("AgentConsole.log");

        RpcMethods::sm_strConsoleLogPath = strFilePath;

        /* After reboot, copy result id to static variable */
        RpcMethods::sm_strResultId = pszResultId;
    
        /* Redirecting stderr buffer to stdout */
        dup2 (fileno(stdout), fileno(stderr));
	
        /* Redirecting stdout buffer to log file */
        if((RpcMethods::sm_pLogStream = freopen(RpcMethods::sm_strConsoleLogPath.c_str(), "a", stdout)) == NULL)
        {
            DEBUG_PRINT (DEBUG_ERROR, "Failed to redirect console logs\n");
        }

        fprintf(stdout,"\nRestoring previous state after box reboot..\n");
    }

    DEBUG_PRINT (DEBUG_TRACE, "\nRPC Restore Previouse State --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

    /* Extracting path to file */
    strFilePath = RpcMethods::sm_strTDKPath;
    strFilePath.append(REBOOT_CONFIG_FILE);
    
    /* Read the module names from configuration file and load those modules */
    o_RebootConfigFile.open (strFilePath.c_str(), ios::in);
    if (o_RebootConfigFile.is_open())
    {
        while (getline (o_RebootConfigFile, strLineInFile))
        {	
            sprintf (szLibName, "%s", strLineInFile.c_str());
            DEBUG_PRINT (DEBUG_LOG, "\nGoing to Load Module : %s \n", szLibName);
            strLoadLibraryDetails = LoadLibrary (szLibName);	
            DEBUG_PRINT (DEBUG_LOG, "\nLoad Module Details : %s \n", strLoadLibraryDetails.c_str());
        }
		
        o_RebootConfigFile.close();
    }
    else
    {
        DEBUG_PRINT (DEBUG_ERROR, "Failed to open configuration file \n");
        response["result"] = "FAILURE";
        response["details"] = "Failed to open configuration file";
    }

    /* Setting the crash status after reboot */
    SetCrashStatus (pszExecId, pszDeviceId, pszTestCaseId, pszExecDevId, pszResultId);

    /* Deleting configuration file */
    nReturnValue = remove (strFilePath.c_str());
		
    return bRet;
	
} /* End of RPCRestorePreviousState */



/********************************************************************************************************************
 Purpose:               RPC call to reboot device under test on Agent monitor crash.
 Parameters:   
                             request [IN]       - Json request
                             response [OUT]  - Json response with result "SUCCESS"
 
 Return:                 bool  -      Always returning true from this function, with details in response[result]
 
 Methods of same class used:   callReboot()

*********************************************************************************************************************/
bool RpcMethods::RPCRebootBox(const Json::Value& request, Json::Value& response)
{

    bool bRet = true;

    DEBUG_PRINT (DEBUG_TRACE, "\nRPC Reboot STB --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

    CallReboot(); // Calling box reboot function.

    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = "Success";

    return bRet;
	
}



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
    std::string strFilePath;

    //DEBUG_PRINT (DEBUG_TRACE, "\nRPCGetHostStatus --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    //cout << "Received query: \n" << request << endl;

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
            strFilePath = RpcMethods::sm_strTDKPath;
            strFilePath.append(CONFIGURATION_FILE);
			
            /* Writing details into configuration file */
            go_ConfigFile.open (strFilePath.c_str(), ios::out);
            if (go_ConfigFile.is_open())
            {
                go_ConfigFile << "Manager IP@" << RpcMethods::sm_szManagerIP << std::endl;
                go_ConfigFile << "Box Name @" << RpcMethods::sm_szBoxName << std::endl;
                go_ConfigFile << "Box Interface@" << RpcMethods::sm_szBoxInterface << std::endl;
                go_ConfigFile.close();
            }
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "\nInterface or Box IP not Valid!!! \n");
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
    char* pszError;
    bool bRet = true;
    int nReturnValue;
    std::string strFilePath;
    void* pvHandle = NULL;
    std::string strLineInFile;
    std::string strEnableReset;
    int nPID = RETURN_SUCCESS;
    int nPgid = RETURN_SUCCESS;
    std::fstream o_ModuleListFile;
    char szLibName [LIB_NAME_SIZE];
    const char* pszEnableReset = NULL;

    pszError = new char [ERROR_SIZE];
    RDKTestStubInterface* (*pfnCreateObject)(void);
    RDKTestStubInterface* pRDKTestStubInterface;
    void (*pfnDestroyObject) (RDKTestStubInterface*);

    fprintf(stdout,"\nResetting Agent..\n");
    DEBUG_PRINT (DEBUG_TRACE, "\nRPCResetAgent --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

    /* Extracting path to file */
    strFilePath= getenv ("TDK_PATH");
    strFilePath.append("/");
    strFilePath.append(MODULE_LIST_FILE);

    /* Read the module names from configuration file and load those modules for setting postrequsites */
    o_ModuleListFile.open (strFilePath.c_str(), ios::in);
    if (o_ModuleListFile.is_open())
    {
        while (getline (o_ModuleListFile, strLineInFile))
        {	
            sprintf (szLibName, "%s", strLineInFile.c_str());
            bRet = DeleteModuleFromFile (strLineInFile);

            /* Dynamically loading library */
            pvHandle = dlopen (szLibName, RTLD_LAZY | RTLD_GLOBAL);
            if (!pvHandle)
            {
                pszError = dlerror();
                DEBUG_PRINT (DEBUG_ERROR, "Failed to get handle for component : %s \n", pszError);
                break;
            }

            /* Executing  "CreateObject" function of loaded module */
            pfnCreateObject = (RDKTestStubInterface* (*) (void)) dlsym (pvHandle, "CreateObject");
            if ( (pszError = dlerror()) != NULL)
            {
                DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
		  break;
            }	
            pRDKTestStubInterface = pfnCreateObject();

            /* Calling Post requisites for module */
            DEBUG_PRINT (DEBUG_LOG, "Executing Post requisites for %s \n", szLibName);
            bRet = pRDKTestStubInterface -> testmodulepost_requisites();
 
            /* Calling "DestroyObject" */
            pfnDestroyObject = (void (*)(RDKTestStubInterface*)) dlsym (pvHandle, "DestroyObject");
            if ( (pszError = dlerror()) != NULL)  
            {
                DEBUG_PRINT (DEBUG_ERROR, "%s \n", pszError);
                break;
            }
	
            pfnDestroyObject (pRDKTestStubInterface);

/* TO DO : Segmentation fault while closing stub handle */			
#if 0
            /* Closing Handle */
            dlclose (pvHandle);
            pvHandle = NULL;		
#endif		

        }
		
        o_ModuleListFile.close();
		
    }
    else
    {
        DEBUG_PRINT (DEBUG_ERROR, "Failed to get list of loaded modules \n");
    }

    /* Delete the Module list file */
    if (remove (strFilePath.c_str()) != 0 )
    {
        DEBUG_PRINT (DEBUG_ERROR, "\n\nAlert : Error in deleting %s \n", SHOW_DEFINE(MODULE_LIST_FILE) );
    }
    else
    {
        DEBUG_PRINT (DEBUG_TRACE, "\n %s successfully deleted\n\n\n", SHOW_DEFINE(MODULE_LIST_FILE)); 
    }

    /* Constructing JSON response */
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
        DEBUG_PRINT (DEBUG_LOG, "\n\nAgent Restarting...\n");

        /* Find group id for agent process */
        nPgid = getpgid(RpcMethods::sm_nAgentPID);

        /* Ignore SIGINT signal in agent monitor process */
	sighandler_t sigIgnoreHandle = signal (SIGINT, SIG_IGN);

	/* Send SIGINT signal to all process in the group */
        nReturnValue = kill ( (-1 * nPgid), SIGINT);
        if (nReturnValue == RETURN_SUCCESS)
        {
            DEBUG_PRINT (DEBUG_TRACE, "Sent SIGINT signal to all process in group successfully \n");
        }
        else
        {
            DEBUG_PRINT (DEBUG_TRACE, "Alert!!! Unable to send SIGINT signal to all process in the group \n");
        }

        /* Set SIGINT signal status to default */
        signal (SIGINT, SIG_DFL);
        sleep(2);	

        /* Start tftp server for logfile transfer */
        nPID = fork();
        if (nPID == RETURN_SUCCESS)
        {
            system (START_TFTP_SERVER);
            exit(0);
        }
        else if (nPID < RETURN_SUCCESS)
        {
            DEBUG_PRINT (DEBUG_ERROR, "\n Alert!!! Couldnot start tftp server for logfile transfer \n");
        }

        {
            /* Restart Agent */
            nReturnValue = kill (RpcMethods::sm_nAgentPID, SIGKILL);
            if (nReturnValue == RETURN_SUCCESS)
            {
                response["result"] = "SUCCESS";
            }
            else
            {
                DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Unable to restart agent \n");
                SignalFailureDetails();
                response["result"] = "FAILURE";
            }
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
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "Failed to set device status \n");
            SignalFailureDetails();
            response["result"] = "FAILURE";
        }
        
    }
    else
    {
        DEBUG_PRINT (DEBUG_ERROR, "Alert!!! Unable to reset Agent..Unknown Parameter");
        response["result"] = "FAILURE";
    }

    /* Check whether sm_nConsoleLogFlag is set, if it is set then close console log output file */
    if (RpcMethods::sm_nConsoleLogFlag == FLAG_SET)
    {
       fclose(RpcMethods::sm_pLogStream);
       RpcMethods::sm_pLogStream = freopen (NULL_LOG, "w", stdout);
    }
	
    return bRet;

}/* End of RPCResetAgent */




/********************************************************************************************************************
 Purpose:               Returns RDK version for which TDK package is built.
 Parameters:   
                             request [IN]       - Json request.
                             response [OUT]  - Json response with result RDK version.
 
 Return:                 bool  -      Always returning true from this function.

*********************************************************************************************************************/
bool RpcMethods::RPCGetRDKVersion (const Json::Value& request, Json::Value& response)
{

    bool bRet = true;

    DEBUG_PRINT (DEBUG_TRACE, "\nRPCGetRDKVersion --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    //cout << "Received query: \n" << request << endl;

    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = RDKVERSION;

    return bRet;

}/* End of RPCGetRDKVersion */




/********************************************************************************************************************
 Purpose:               Returns log path where agent console logs are present.
 Parameters:   
                             request [IN]       - Json request.
                             response [OUT]  - Json response with result log path.
 
 Return:                 bool  -      Always returning true from this function.

*********************************************************************************************************************/
bool RpcMethods::RPCGetAgentConsoleLogPath(const Json::Value& request, Json::Value& response)
{
    bool bRet = true;

    /* Preparing JSON Response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];
    response["result"] = RpcMethods::sm_strLogFolderPath;

    return bRet;

}/* End of RPCGetAgentConsoleLogPath */



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
    std::string strLogPath;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];
 
    DEBUG_PRINT (DEBUG_TRACE, "\nRPCPerformanceBenchMarking --> Entry\n");
    std::cout << "Received query: " << request << std::endl;

    /* Extracting log file path */
    strLogPath = RpcMethods::sm_strTDKPath;
    strLogPath.append(BENCHMARKING_FILE);

    if (std::ifstream(strLogPath.c_str()))
    {
        response["result"]  = "SUCCESS";
    }
    else
    {
	DEBUG_PRINT (DEBUG_ERROR, "\nError!!! %s not found\n", BENCHMARKING_FILE);
        response["result"]  = "FAILURE";
    }

    response["logpath"] = strLogPath.c_str();

    DEBUG_PRINT (DEBUG_TRACE, "\nRPCPerformanceBenchMarking --> Exit \n");

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
    std::string strLogPath;	

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"]	= request["id"];

    DEBUG_PRINT (DEBUG_TRACE, "\nRPCPerformanceSystemDiagnostics --> Entry \n");
    std::cout << "Received query: " << request << std::endl;
    
    /* Extracting log file path */
    strLogPath = RpcMethods::sm_strTDKPath;
    strLogPath.append(SYSDIAGNOSTIC_FILE);
	
    if (std::ifstream(strLogPath.c_str()))
    {
       	response["result"]  = "SUCCESS";
    }
    else
    {
	DEBUG_PRINT (DEBUG_ERROR, "\nError!!! %s not found\n", SYSDIAGNOSTIC_FILE);
       	response["result"]  = "FAILURE";
    }

    response["logpath"] = strLogPath.c_str();
   
    DEBUG_PRINT (DEBUG_TRACE, "\nRPCPerformanceSystemDiagnostics --> Exit \n");
 
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
    std::string strFilePath;
    std::string strClientMAC;
    std::string strDeviceList = "DEVICES=";
    std::string strDelimiter = ",";
    char szCommand[COMMAND_SIZE];

    //DEBUG_PRINT (DEBUG_TRACE, "\nRPCGetConnectedDevices --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    //cout << "Received query: \n" << request << endl;

    /* Extracting file path */
    strFilePath = RpcMethods::sm_strTDKPath;
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
    std::string strFilePath;
    const char* pszAgentPort;
    const char* pszStatusPort;
    const char* pszLogTransferPort;
    const char* pszAgentMonitorPort;
    const char* pszClientMAC = NULL;
    char szCommand[COMMAND_SIZE];
    int nClientExistFlag = FLAG_NOT_SET;

    DEBUG_PRINT (DEBUG_TRACE, "\nRPCSetClientRoute --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

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

        /* Parse through Device map to find the client device already exists or not */
        for (o_gClientDeviceMapIter = o_gClientDeviceMap.begin(); o_gClientDeviceMapIter != o_gClientDeviceMap.end(); o_gClientDeviceMapIter ++ )
        {
            if (o_gClientDeviceMapIter -> first == pszClientMAC)
            {
                nClientExistFlag = FLAG_SET;
                break;
            }
        }

        /* If client already exist, remove that entry from map */
        if (nClientExistFlag == FLAG_SET)
        {
            /* Removing map entry */
            o_gClientDeviceMap.erase (o_gClientDeviceMapIter);
        }

        /* Add client to map */
        o_gClientDeviceMap.insert (std::make_pair (pszClientMAC, szCommand));

        /* Extracting path to file */
        strFilePath = RpcMethods::sm_strTDKPath;
        strFilePath.append(PORT_FORWARD_RULE_FILE);
    
        /* Adding command to configuration file to set route accross reboot */
        go_PortforwardFile.open (strFilePath.c_str(), ios::out);
        if (go_PortforwardFile.is_open())
        {
            /* Parse through map to find the client devices to update configuration file */
            for (o_gClientDeviceMapIter = o_gClientDeviceMap.begin(); o_gClientDeviceMapIter != o_gClientDeviceMap.end(); o_gClientDeviceMapIter ++ )
            {
                go_PortforwardFile << o_gClientDeviceMapIter -> first << "=" << o_gClientDeviceMapIter -> second << std::endl;
            }
            go_PortforwardFile.close();	
        }
        else
        {
            DEBUG_PRINT (DEBUG_ERROR, "\nAlert!!! Opening %s failed \n", SHOW_DEFINE(PORT_FORWARD_RULE_FILE) );
        }

        DEBUG_PRINT (DEBUG_ERROR, "\nSetting route for %s \n", pszClientMAC);
	
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



/********************************************************************************************************************
 Purpose:               This function is used to get MoCA ip address of a client device.
 Parameters:   
                             request [IN]       - Json request to set the route to connected client device.
                             response [OUT]  - Json response with result moca ip address
 
 Return:                 bool  -      Always returning true from this function, with details in response[result].

*********************************************************************************************************************/
bool RpcMethods::RPCGetClientMocaIpAddress (const Json::Value& request, Json::Value& response)
{
    bool bRet = true;
    char szBuffer[128];
    std::string strIPaddr = "";
    const char* pszClientMAC = NULL;
    char szCommand[COMMAND_SIZE];

    DEBUG_PRINT (DEBUG_TRACE, "\nRPCGetClientMocaIpAddress --> Entry\n");
    //DEBUG_PRINT (DEBUG_TRACE, "Received query: %s \n", request.asCString());
    cout << "Received query: \n" << request << endl;

    /* Constructing JSON response */
    response["jsonrpc"] = "2.0";
    response["id"] = request["id"];

    /* Getting MAC address and port numbers from Test Manager */
    if (request["MACaddr"] != Json::Value::null)
    {		
        pszClientMAC = request["MACaddr"].asCString();
    }

    /* Constructing command to get IP address of corresponding MAC */
    sprintf (szCommand, "arp -i eth1 -n |grep %s |cut -d'(' -f2 | cut -d')' -f1",  pszClientMAC); 

    /* Creating pipe to fetch ip address */ 	
    FILE* pipe = popen(szCommand, "r");
    if (!pipe)
    {
        strIPaddr = "Error in creating pipe to fetch ip address";
        response["result"] = strIPaddr.c_str();
        DEBUG_PRINT (DEBUG_TRACE, "\nError in creating pipe to fetch ip address\n");
    }
    else
    {
        while(!feof(pipe)) 
        {
            if(fgets(szBuffer, 128, pipe) != NULL)
            {
                strIPaddr += szBuffer;
            }
        }
	
        pclose(pipe);
	
        strIPaddr.erase(std::remove(strIPaddr.begin(), strIPaddr.end(), '\n'), strIPaddr.end());

        DEBUG_PRINT (DEBUG_TRACE, "\nMoca IP address of %s is %s\n", pszClientMAC, strIPaddr.c_str());
    }

    /* Sending ip address or error message with json response message */	
    response["result"] = strIPaddr.c_str();

    return bRet;

}/* End of RPCGetClientMocaIpAddress */

#endif /* PORT_FORWARD */



/* End of rpcmethods */



