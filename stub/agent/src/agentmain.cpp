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
#include <stdio.h>
#include <error.h>
#include <csignal>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <fstream>
#include <net/if.h>
#include <setjmp.h>
#include <ifaddrs.h>
#include <iostream>
#include <pthread.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <jsonrpc/jsonrpc.h>

/* Application Includes */
#include "rpcmethods.h"
#include "rdktestagentintf.h"

/* Constants */
#define DEVICE_INFO_SUCCESS 0
#define DEVICE_INFO_FAILURE 1

#define ANY_ADDR "0.0.0.0"
#define RDK_TEST_AGENT_PORT 8087
#define RDK_DEVICE_INFO_PORT 8089
#define RDK_DEVICE_STATUS_PORT 8088
#define RDK_AGENT_MONITOR_PORT 8090

#define INFO_STRING_SIZE 100
#define STATUS_QUERY_TIMEOUT 120

#define CRASH_STATUS_FILE "crashStatus.ini"
#define FLUSH_IP_TABLE "sh $TDK_PATH/flush_iptables.sh"
#define START_TFTP_SERVER "udpsvd -vE 0.0.0.0 69 tftpd"

using namespace std;
using namespace Json;


jmp_buf g_JumpBuffer;  //  Declaring global jmp_buf variable to be used by both main and signal handler

static volatile bool s_bAgentMonitorRun = true;  //  Variable to run agent monitor. Set to false to stop monitoring.
static volatile bool s_bAgentRun = true;              // Variable to run agent. Set to false to stop agent.
static volatile bool s_bAgentReset = true;           // Variable to enable agent reset.

std::fstream go_ConfigFile;
std::fstream go_PortforwardFile;

pthread_t deviceStatusThreadId;
pthread_t deviceDetailsThreadId;
pthread_t crashDetailsThreadId;
pthread_t agentExecuterThreadId;

Json::Rpc::TcpServer go_Server (ANY_ADDR, RDK_TEST_AGENT_PORT);

/* Initialization */
int RpcMethods::sm_nAgentPID = 0;
int RpcMethods::sm_nRouteSetFlag = FLAG_NOT_SET;
int RpcMethods::sm_nGetDeviceFlag = FLAG_NOT_SET;
int RpcMethods::sm_nStatusQueryFlag = FLAG_NOT_SET;

string RpcMethods::sm_strBoxIP = "";
const char* RpcMethods::sm_szBoxName = NULL;
const char* RpcMethods::sm_szManagerIP = NULL;
const char* RpcMethods::sm_szBoxInterface = NULL;



/********************************************************************************************************************
 Purpose:               To get a substring seperated by a delimiter.
 
 Parameters:   
                             strLine [IN]    - Line of string to get seperated.
                             strDelimiter [IN]  - delimiter 
 
 Return:                 string    - substring

*********************************************************************************************************************/
std::string GetSubString (std::string strLine, std::string strDelimiter)
{
    size_t nPos = 0;
    std::string strToken;

    while ( (nPos = strLine.find (strDelimiter)) != std::string::npos)
    {
        strToken = strLine.substr (0, nPos);
        strLine.erase (0, nPos + strDelimiter.length());
    }
	
    return strLine;
	
} /* End of GetSubString */


/********************************************************************************************************************
 Purpose:               To get the Host's IP Address by querrying the network Interface.
 
 Parameters:   
                             szInterface [IN]    - Interface used to communicate.
 
 Return:                 string    - IP address of corresponding interface.

*********************************************************************************************************************/
std::string GetHostIP (const char* szInterface)
{
    struct ifaddrs* pIfAddrStruct = NULL;
    struct ifaddrs* pIfAddrIterator = NULL;
    void* pvTmpAddrPtr = NULL;
    char szAddressBuffer [INET_ADDRSTRLEN];
    getifaddrs (&pIfAddrStruct);

    for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next) 
    {
        if (pIfAddrIterator->ifa_addr->sa_family == AF_INET) 
        {
            // check it is a valid IP4 Address
            pvTmpAddrPtr = & ( (struct sockaddr_in *)pIfAddrIterator->ifa_addr )-> sin_addr;
            inet_ntop (AF_INET, pvTmpAddrPtr, szAddressBuffer, INET_ADDRSTRLEN);
    
            if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
            {
                break;
            }		
        } 
    }	
	
    std::cout << "Found IP: " << szAddressBuffer << std::endl;

    if (pIfAddrStruct != NULL) 
    {
        freeifaddrs (pIfAddrStruct);
    }

    return szAddressBuffer;
	
} /* End of GetHostIP */


/********************************************************************************************************************
 Purpose:               A function to send information from the box to manager. It will extract 
                        manager IP address from configuration file
 
 Parameters:   
                             strStringToSend [IN] - data to send
                             nStringSize [IN]  - size of data
 
 Return:                 int    -  Success/Failure

 Other Methods used:     
                                    GetSubString()

*********************************************************************************************************************/
int SendInfo (char* strStringToSend, int nStringSize)
{
    int nValue = 0;
    int nDestination;
    int nInfoSockDesc;    
    void *pvReturnValue;    
    std::string strEnvPath;
    std::string strFilePath;
    std::string strManagerIP;
    
    int nReturnValue = DEVICE_INFO_SUCCESS;
    struct sockaddr_in o_Addr;

    nInfoSockDesc = socket (AF_INET, SOCK_STREAM, 0);
    if (nInfoSockDesc < 0)
    {
        perror("\nAlert!!! Failed to create socket ");
		
        return DEVICE_INFO_FAILURE;     // Return when failed to create socket
        
    }	

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    if (strEnvPath.empty() == 0)
    {
        strFilePath.append(strEnvPath);
        strFilePath.append("/");
    	 strFilePath.append(CONFIGURATION_FILE);
    }
    else
    {
        std::cout << "Failed to extract environment variable TDK_PATH" << std::endl;
	
        return DEVICE_INFO_FAILURE;     // Return when failed to get environment path
    }
	
    /* Open the configuration file and extracts Test manager IP address */
    go_ConfigFile.open (strFilePath.c_str(), ios::in);
    if (go_ConfigFile.is_open())
    {
        std::cout << "\nConfiguration file " << SHOW_DEFINE (CONFIGURATION_FILE) << " found" << std::endl;
		
        /* Parsing configuration file to get manager IP */
        pvReturnValue = getline (go_ConfigFile, strManagerIP); 
        go_ConfigFile.close();
        if (pvReturnValue)
        {
            strManagerIP = GetSubString (strManagerIP, ":");
            RpcMethods::sm_szManagerIP = strManagerIP.c_str();
            std::cout << "Test Manager IP is " << RpcMethods::sm_szManagerIP << std::endl;
        }
        else
        {
            std::cout << "Failed to extract Test Manager IP Address" << std::endl;

            return DEVICE_INFO_FAILURE;     // Return when failed to extract Test Manager IP Address
		 
        }

    }
    else
    {
        std::cout << "\nAlert!!! Configuration file " << SHOW_DEFINE(CONFIGURATION_FILE) << " not found" << std::endl;
        	
        return DEVICE_INFO_FAILURE;     // Return when failed to open configuration file
        
    }

    inet_pton (AF_INET, RpcMethods::sm_szManagerIP, (void *)&nDestination);
    o_Addr.sin_family = AF_INET ;
    o_Addr.sin_port = htons (RDK_DEVICE_INFO_PORT);
    o_Addr.sin_addr.s_addr = nDestination;

    /* Connecting to Test Manager */
    nValue = connect (nInfoSockDesc, (struct sockaddr *) &o_Addr, sizeof(o_Addr));
    if (nValue < 0)
    {
        perror("\nAlert!!! Failed to connect Test Manager ");
        	
        return DEVICE_INFO_FAILURE;     // Return when failed to connect to Test Manager
        
    }

    /* Sending data to Test Manager */
    nValue = write (nInfoSockDesc, (void *)strStringToSend, nStringSize);
    if (nValue < 0)
    {
        perror("\nAlert!!! Failed to send data to Test Manager ");
        	
        return DEVICE_INFO_FAILURE;     // Return when failed to send data to Test Manager
        
    }
	
    close (nInfoSockDesc);
	
    return nReturnValue;
	
} /* End of SendInfo */



/********************************************************************************************************************
 Purpose:               Signal Handler. Handles signals and jump to the jumpbuffer to keep application active.
 
 Parameters:   
                             nCode [IN] - Signal number
                             
 Return:                 void

 Other Methods used:     
                                    SendInfo()

*********************************************************************************************************************/
static void SignalHandler (int nCode)
{
    switch(nCode)
    {
        case SIGINT    :
        case SIGTERM :
            std::cout << "\nAgent Shutttingdown...\n";
            s_bAgentMonitorRun = false;
            s_bAgentRun = false;
            s_bAgentReset = false;
            break;
			
        case SIGABRT :
            std::cout << std::endl << "Alert!!! Agent caught an Abort signal! Attempting recovery.." << std::endl;
            longjmp (g_JumpBuffer,0);
            break;
			
        case SIGSEGV :
            std::cout << std::endl << "Alert!!! Segmentation fault signal caught! Attempting recovery.." << std::endl;
            s_bAgentRun = false;
            longjmp (g_JumpBuffer,0);
            break;

        /* User Defined signal for setting device state to FREE */
        case SIGUSR2 :
            RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
            break;
			
        default :
            break;
			
    }
	
} /* End of SignalHandler */



/********************************************************************************************************************
 Purpose:               To send box details such as box ip address and box name to test manager using SendInfo()
                             after reading box name from configuration file.
 
 Parameters:   
                             null
 
 Return:                 int    -  Success/Failure

 Other Methods used:    
                                    SendInfo() 
                                    GetSubString()

*********************************************************************************************************************/
int SendDetailsToManager()
{
    void *pvReturnValue;
    char szBoxInfo[INFO_STRING_SIZE];
    int nSendInfoStatus = 0;
    std::string strBoxName;
    std::string strEnvPath;
    std::string strFilePath;

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(CONFIGURATION_FILE);
    
    go_ConfigFile.open (strFilePath.c_str(), ios::in);
    if (go_ConfigFile.is_open())
    {
        std::cout << "\nConfiguration file " << SHOW_DEFINE (CONFIGURATION_FILE) << " found" << std::endl;
			
        /* Parsing configuration file to get box name */
        for (int i=0; i<2; i++)
        {
            pvReturnValue = getline (go_ConfigFile, strBoxName);

            if (!pvReturnValue)
            {
                std::cout << "Unable to find device name" << std::endl;

                nSendInfoStatus =  DEVICE_INFO_FAILURE;     // Info failure when failed to retrieve device name
                break;
            }
			
        }

        go_ConfigFile.close();

        /* Sending details to Test Manager */
        if (pvReturnValue)
        {
            strBoxName = GetSubString (strBoxName, ":");		
            RpcMethods::sm_szBoxName = strBoxName.c_str();
            std::cout << "Box Name is " << RpcMethods::sm_szBoxName << std::endl;
			        
            /* Sending the box name and box ip address to Test Manager */
            szBoxInfo[0] = '\0';
            strcat(szBoxInfo, RpcMethods::sm_szBoxName);
            strcat(szBoxInfo, ",");
            strcat(szBoxInfo, RpcMethods::sm_strBoxIP.c_str());
		
            nSendInfoStatus = SendInfo (szBoxInfo, strlen(szBoxInfo)); 
        }	
        
    }
    else
    {
        std::cout << "\nAlert!!! Configuration file " << SHOW_DEFINE(CONFIGURATION_FILE) << " not found" << std::endl;
        nSendInfoStatus = DEVICE_INFO_FAILURE;
    }

    return nSendInfoStatus;
	
} /* End of SendDetailsToManager */



/********************************************************************************************************************
 Purpose:               To Check if device had a crash during last power cycle. If it had, send Test casedetails such as execution ID, 
                             device ID and Test case ID to test manager using SendInfo()
 
 Parameters:   
                             null
 
 Return:                 int    -  Success/Failure

 Other Methods used:    
                                    SendInfo() 
                                    GetSubString()

*********************************************************************************************************************/
void* ReportCrash (void*)
{
    void *pvReturnValue;
    int nCount = 0;
    int nCrashFlag = FLAG_SET;
    std::string strExecId;
    std::string strEnvPath;
    std::string strFilePath;
    std::string strDeviceId;
    std::string strTestcaseId;
    std::string strCrashStatus;
    std::string strExecDeviceId;
    std::fstream o_CrashStatusFile;
    char szCrashDetails [INFO_STRING_SIZE];
    int nSendInfoStatus = RETURN_SUCCESS;

    std::cout << "\nStarting Crash Details Processing..\n";

    /* Extracting path to file */	
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(CRASH_STATUS_FILE);
  	
    o_CrashStatusFile.open (strFilePath.c_str(), ios::in);
    if (o_CrashStatusFile.is_open())
    {
        std::cout << "\nConfiguration file " << SHOW_DEFINE (CRASH_STATUS_FILE) << " found" << std::endl;
		
        /* Parsing configuration file to get crash status */
        pvReturnValue = getline (o_CrashStatusFile, strCrashStatus); 
        if (!pvReturnValue)
        {
            std::cout << "Failed to retrieve status on crash" << std::endl;
            nCrashFlag = FLAG_NOT_SET ;
        }
        else
        {
            strCrashStatus = GetSubString (strCrashStatus, ":");
        }

        if ((strCrashStatus == "YES") && (nCrashFlag == FLAG_SET))
        {
            std::cout << "\nAlert !!! Crash occured in previous execution. Trying to send test details to Test Manager... " << std::endl;
            std::cout << "Test Details :  ";
	
            /* Parsing configuration file to get execution ID */
            pvReturnValue = getline (o_CrashStatusFile, strExecId); 
            if (!pvReturnValue)
            {
                std::cout << "Failed to retrieve execution ID" << std::endl;
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strExecId = GetSubString (strExecId, ":");
                if (strExecId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
		
            /* Parsing configuration file to get Device ID */
            pvReturnValue = getline (o_CrashStatusFile, strDeviceId);
            if (!pvReturnValue)
            {
                std::cout << "Failed to retrieve Device ID" << std::endl;
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strDeviceId = GetSubString (strDeviceId, ":");
                if (strDeviceId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
            
            /* Parsing configuration file to get Testcase ID */
            pvReturnValue = getline (o_CrashStatusFile, strTestcaseId); 
            if (!pvReturnValue)
            {
                std::cout << "Failed to retrieve Testcase ID" << std::endl;
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strTestcaseId = GetSubString (strTestcaseId, ":");
                if (strTestcaseId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
			
            /* Parsing configuration file to get Execution Device ID */
            pvReturnValue = getline (o_CrashStatusFile, strExecDeviceId); 
            if (!pvReturnValue)
            {
                std::cout << "Failed to retrieve Execution Device ID" << std::endl;
                nCrashFlag = FLAG_NOT_SET ;
            }
            else
            {
                strExecDeviceId = GetSubString (strExecDeviceId, ":");
                if (strExecDeviceId == "")  (nCrashFlag = FLAG_NOT_SET);
            }
			
            o_CrashStatusFile.close();

            /* Sending the test details to Test Manager */
            if (nCrashFlag == FLAG_SET)
            {
                std::cout << std::endl << "    Execution ID : " << strExecId << std::endl;
                std::cout << "    Device ID    : " << strDeviceId << std::endl;
                std::cout << "    Testcase ID  : " << strTestcaseId << std::endl;
                std::cout << "    Execution Device ID  : " << strExecDeviceId << std::endl;
				
                szCrashDetails[0] = '\0';
                strcat(szCrashDetails, "CRASH_");			
                strcat(szCrashDetails, strExecId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strDeviceId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strTestcaseId.c_str());
                strcat(szCrashDetails, ",");
                strcat(szCrashDetails, strExecDeviceId.c_str());
            
                /* Waiting to get a status query */
                while (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
                {
                    sleep(1);	
                    nCount ++;
                    if (nCount == STATUS_QUERY_TIMEOUT)
                    {
                        break;
                    }
                }
		
                nSendInfoStatus = SendInfo (szCrashDetails, strlen (szCrashDetails)); 
                if (nSendInfoStatus == DEVICE_INFO_SUCCESS)
                {
                    std::cout << "Sent crash details to Test Manager successfully" << std::endl;
				
                }
            }
            else
            {
                std::cout << "Not found" << std::endl;
            }

            /* Delete the configuration file */
            if (remove (strFilePath.c_str()) != 0 )
            {
                std::cout << "\nAlert : Unable to delete " << SHOW_DEFINE(CRASH_STATUS_FILE) << " file\n";
            }
            else
            {
                std::cout << std::endl << SHOW_DEFINE(CRASH_STATUS_FILE) << " successfully deleted\n" ;
            }
			
        }

        else
        {
            std::cout << "Unable to report crash to Test Manager" << std::endl;
        }
		
    }

    pthread_exit (NULL);	

} /* End of ReportCrash */



/********************************************************************************************************************
 Purpose:               To check the device status, whether the execution is in progress or box is free for execution. (Thread Function)
 
 Parameters:          null
 
 Return:                 null

*********************************************************************************************************************/
void *CheckStatus (void *)
{
    std::cout << "\nStarting Device Status Monitoring..\n";

    Json::Rpc::TcpServer o_Status (ANY_ADDR, RDK_DEVICE_STATUS_PORT);
    RpcMethods o_RpcMethods (NULL);

    if (!networking::init())
    {
        std::cerr << "Alert!!! Device Status Monitoring Network initialization failed" << std::endl;
    }

    if (!o_Status.Bind())
    {
        std::cout << "Alert!!! Device Status Monitoring Bind failed" << std::endl;
    }

    if (!o_Status.Listen())
    {
        std::cout << "Alert!!! Device Status Monitoring Listen failed" << std::endl;
    }

    /* Registering methods to status server */
    o_Status.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCGetHostStatus, std::string("getHostStatus")));

    /* To set route to client devices. For gateway boxes only */
    #ifdef PORT_FORWARD
    o_Status.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCSetClientRoute, std::string("setClientRoute")));
    o_Status.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCGetConnectedDevices, std::string("getConnectedDevices")));
    #endif /* End of PORT_FORWARD  */
		
    while (s_bAgentRun)
    {
        /* Status server waiting indefinitely */
        o_Status.WaitMessage(1000);
    }

    /* clean up and exit */
    std::cout << "\nExiting Device Status Monitoring..\n";
    o_Status.Close();
    networking::cleanup();
    pthread_exit (NULL);
	
} /* End of CheckStatus */



/********************************************************************************************************************
 Purpose:               To check whether a status query is received, if not send the device details to test manager. (Thread Function)
 
 Parameters:          null
 
 Return:                 null

 Other Methods used: 
                                    GetSubString()
                                    GetHostIP()
                                    SendDetailsToManager()

*********************************************************************************************************************/
void *ProcessDeviceDetails (void *)
{
    int nCount = 0;
    void *pvReturnValue;
    std::string strEnvPath;
    std::string strFilePath;
    int nDeviceInfoStatus = 0;
    std::string strBoxInterface;	

    std::cout << "\nStarting Device Details Processing..\n";
		
    /* Waiting to get a status query */
    while (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
    {
        sleep(1);	
        nCount ++;

        if (nCount == STATUS_QUERY_TIMEOUT)
        {
            break;
        }
    }

    /* If status query flag not set, then send box name and IP address to Test Manager */
    if (RpcMethods::sm_nStatusQueryFlag == FLAG_NOT_SET)
    {
        /* Extracting path to file */
        strEnvPath = getenv ("TDK_PATH");
        strFilePath.append(strEnvPath);
        strFilePath.append("/");
    	 strFilePath.append(CONFIGURATION_FILE);
	
        go_ConfigFile.open (strFilePath.c_str(), ios::in);
        if (go_ConfigFile.is_open())
        {
            std::cout << "\nConfiguration file " << SHOW_DEFINE(CONFIGURATION_FILE) << " found" << std::endl;

            /* Finding the box interface from configuration file */
            for (int i=0; i<3; i++)
            {
                pvReturnValue = getline (go_ConfigFile, strBoxInterface);
                if (!pvReturnValue)
                {
                    std::cout << "Unable to find device network interface" << std::endl;
                    break;
                }

            }

            go_ConfigFile.close();

            /* Communicate with Test Manager after retrieveng device IP address */
            if (pvReturnValue)
            {
                strBoxInterface = GetSubString (strBoxInterface, ":");	
                RpcMethods::sm_szBoxInterface = strBoxInterface.c_str();
                std::cout << "\nBox interface is " << RpcMethods::sm_szBoxInterface << std::endl;
            
                /* Getting box IP address of corresponding interface */
                RpcMethods::sm_strBoxIP = GetHostIP (RpcMethods::sm_szBoxInterface);
			
                /* Sending box details to test manager */
                nDeviceInfoStatus = SendDetailsToManager();
                if (nDeviceInfoStatus == DEVICE_INFO_FAILURE)
                {
                    std::cout << "\nAlert!!! Agent not able to communicate with Test Manager" << std::endl;
                }
			
            }
			
        }
        else
        {
            std::cout << "\nAlert!!! Configuration file " << SHOW_DEFINE(CONFIGURATION_FILE) << " not found" << std::endl;
        }
			
    }
		
    pthread_exit (NULL);
	
} /* End of ProcessDeviceDetails */



/********************************************************************************************************************
 Description:           Agent Application. It enables RPC communication with test manager. 
 
 Parameters:          null
 
 Return:                 int - Success/Failure

 Other Methods used: 
                                    GetSubString()
                                    GetHostIP()
                                    SendDetailsToManager()

*********************************************************************************************************************/
int Agent()
{
    char * pszCommand;
    std::string strEnvPath;
    std::string strFilePath;
    std::string strCommand;
    int nReturnValue = RETURN_SUCCESS;
    int nCrashReportStatus = RETURN_SUCCESS;

    if (!networking::init())
    {
        std::cerr << "Alert!!! Networking initialization failed" << std::endl;
		
        return RETURN_FAILURE;  // Returns failure if Networking initialization failed 
    }
	
    /* Registering signals to signal handler */	
    if (signal (SIGUSR2, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGUSR2 will not be handled" << std::endl;
    }
	
    if (signal (SIGTERM, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGTERM will not be handled" << std::endl;
    }
	
    if (signal (SIGINT, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGINT will not be handled" << std::endl;
    }
	
    if (signal (SIGSEGV, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGSEGV will not be handled" << std::endl;
    }

    if (signal (SIGABRT, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGABRT will not be handled" << std::endl;
    }

    /* Create AgentObj */
    RDKTestAgent o_Agent(&go_Server);

    if (!go_Server.Bind())
    {
        std::cout << "Alert!!! Test Agent Bind failed" << std::endl;
		
        return RETURN_FAILURE;   // Returns failure if Bind failed
        
    }

    if (!go_Server.Listen())
    {
        std::cout << "Alert!!! Test Agent Listen failed" << std::endl;
		
        return RETURN_FAILURE;   // Returns failure if Listen failed
        
    }

    RpcMethods o_RpcMethods(&o_Agent);
	
    /* Registering RPC methods to server */
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCLoadModule, std::string("LoadModule")));
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCUnloadModule, std::string("UnloadModule")));
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCEnableReboot, std::string("EnableReboot")));
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCRestorePreviousState, std::string("RestorePreviousState")));
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCPerformanceBenchMarking, std::string("PerformanceBenchMarking")));
    go_Server.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCPerformanceSystemDiagnostics, std::string("PerformanceSystemDiagnostics")));


    /* To set route to client devices. For gateway boxes only */
    #ifdef PORT_FORWARD

    /* Extracting path to file */
    strEnvPath = getenv ("TDK_PATH");
    strFilePath.append(strEnvPath);
    strFilePath.append("/");
    strFilePath.append(PORT_FORWARD_RULE_FILE);

    /* Set iptable rules that was set in previous power cycle from the details in file */
    go_PortforwardFile.open(strFilePath.c_str(), ios::in);
    if (go_PortforwardFile.is_open())
    {
        std::cout << std::endl << SHOW_DEFINE(PORT_FORWARD_RULE_FILE) << " found" << std::endl;
        while (getline (go_PortforwardFile, strCommand))
        {
            strCommand = GetSubString (strCommand, "=");
            pszCommand = new char[strCommand.length() + 1];
            strcpy (pszCommand, strCommand.c_str());
            system (pszCommand); // Executing port forward script
        }
        go_PortforwardFile.close();
    }
	
    #endif /* End of PORT_FORWARD  */

    RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
    RpcMethods::sm_nStatusQueryFlag = FLAG_NOT_SET;
    
    /* Starting new thread for Device Status Monitoring */
    nReturnValue = pthread_create (&deviceStatusThreadId, NULL, CheckStatus, NULL);
    if(nReturnValue != RETURN_SUCCESS)
    {
        std::cout << "\nAlert!!! Failed to start Device Status Monitoring\n" << nReturnValue;
    }
			
    /* Starting new thread for sending box information to Test Manager */
    nReturnValue = pthread_create (&deviceDetailsThreadId, NULL, ProcessDeviceDetails, NULL);
    if (nReturnValue != RETURN_SUCCESS)
    {
        std::cout << "\nAlert!!! Failed to start Box Details Processing\n" << nReturnValue;
    }

    /* Report if a crash occured on previous execution */
    nReturnValue = pthread_create (&crashDetailsThreadId, NULL, ReportCrash, NULL);
    if (nReturnValue != RETURN_SUCCESS)
    {
        std::cout << "\nAlert!!! Failed to start Crash Details Processing\n" << nReturnValue;
    }
		
    /* Agent going for test execution */	
    sleep(1);
    std::cout << "\n\nAgent Ready for Execution..." << std::endl;

    /* Agent Recovery from seg fault and abort signal */
    nReturnValue = 0;
    nReturnValue = setjmp (g_JumpBuffer); // Setting the jump buffer for agent recovery
    if (nReturnValue)
    {
        std::cout << "Agent Recovering...\n";
    }

    /* Msg loop */
    while (s_bAgentRun)
    {
        try
        {
            waitpid (-1, NULL, WNOHANG | WUNTRACED);
					
            /* Server waiting indefinitely */
            go_Server.WaitMessage (1000);
        }
        catch(...)
        {
            /* Agent Recovery from termination */
            std::cout << "\nAlert!!! Termination caught.. Agent Attempting Recovery...\n";
    //        RpcMethods::sm_nDeviceStatusFlag = DEVICE_FREE;
        }
        
    }

    /* cleanup and exit */
    go_Server.Close();
    networking::cleanup();
    pthread_join (deviceStatusThreadId, NULL);

    /* To set route to client devices. For gateway boxes only */
    #ifdef PORT_FORWARD
		
    system (FLUSH_IP_TABLE);
		
    #endif /* End of PORT_FORWARD  */
	
    return RETURN_SUCCESS;
	
} /* End of Agent */




/********************************************************************************************************************
 Description:           To execute Agent. It helps to restart agent on receiving a ResetAgent message from TM.
 
 Parameters:          null
 
 Return:                 void

 Other Methods used: Agent()
 
*********************************************************************************************************************/
void *AgentExecuter (void *)
{
    int nReturnValue = RETURN_SUCCESS;
    int nPID = RETURN_SUCCESS;

    /* Restart the agent if s_bAgentReset is true */
    while(s_bAgentReset)
    {
        nPID = fork();
        if (nPID == RETURN_SUCCESS)
        {
            waitpid (-1, NULL, WNOHANG | WUNTRACED);
            nReturnValue = Agent();
            if(nReturnValue == RETURN_FAILURE)
            {
                s_bAgentReset = false;
            }

            sleep(3);
            exit(0);
        }
        else if (nPID < RETURN_SUCCESS)
        {
            std::cout << "\n Alert!!!Failed to spawn process for Agent execution\n";
        }
        else
        {
            RpcMethods::sm_nAgentPID = nPID;
            waitpid (RpcMethods::sm_nAgentPID, NULL, 0);	
            sleep(2);
        }
    }

}/* End of AgentExecuter */



/********************************************************************************************************************
 Description:           Start and monitor agent execution. Invoke the corresponding rpc method on 
                        receiving "AgentResest" message from Test Manager. It also starts TFTP server
                        for log transferring. 
 
 Parameters:          null
 
 Return:                 int - Success/Failure

 Other Methods used:     AgentExecuter()
 
*********************************************************************************************************************/
int AgentMonitor()
{
    int nPID = RETURN_SUCCESS;
    int nReturnValue = RETURN_SUCCESS;

    std::cout << "\nStarting Agent Monitoring..\n";

    /* Registering signals to signal handler */
    if (signal (SIGTERM, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGTERM will not be handled" << std::endl;
    }
	
    if (signal (SIGINT, SignalHandler) == SIG_ERR)
    {
        std::cout << "Alert!!! Error signal SIGINT will not be handled" << std::endl;
    }

    /* Create AgentMonitorObj */
    Json::Rpc::TcpServer o_Monitor (ANY_ADDR, RDK_AGENT_MONITOR_PORT);
    RpcMethods o_RpcMethods (NULL);

    if (!networking::init())
    {
        std::cerr << "Alert!!! Agent Monitoring Network initialization failed" << std::endl;
		
        return RETURN_FAILURE;  // Returns failure if Networking initialization failed
        
    }

    if (!o_Monitor.Bind())
    {
        std::cout << "Alert!!! Agent Monitoring Bind failed" << std::endl;

        return RETURN_FAILURE;   // Returns failure if Bind failed
        
    }

    if (!o_Monitor.Listen())
    {
        std::cout << "Alert!!! Agent Monitoring Listen failed" << std::endl;

        return RETURN_FAILURE;   // Returns failure if Listen failed
		
    }

    /* Registering methods to agent monitor */
    o_Monitor.AddMethod (new Json::Rpc::RpcMethod<RpcMethods> (o_RpcMethods, &RpcMethods::RPCResetAgent, std::string("ResetAgent")));

    /* Starting a thread for agent execution */
    nReturnValue = pthread_create (&agentExecuterThreadId, NULL, AgentExecuter, NULL);
    if(nReturnValue != RETURN_SUCCESS)
    {
        std::cout << "\nAlert!!! Failed to start execute Agent " << nReturnValue << std::endl;

        return RETURN_FAILURE;   // Returns failure if failed to start agent execution thread
		
    }
	
    /* Start tftp server for logfile transfer */
    nPID = fork();
    if (nPID == RETURN_SUCCESS)
    {
        system (START_TFTP_SERVER);
    }
    else if (nPID < RETURN_SUCCESS)
    {
        std::cout << "\n Alert!!! Couldnot start tftp server for logfile transfer\n";
    }
    else
    {
        while (s_bAgentMonitorRun)
        {
            /* server waiting indefinitely */
            o_Monitor.WaitMessage(1000);
        }

        /* clean up and exit */
        std::cout << "\nExiting Agent Monitoring..\n";
        o_Monitor.Close();
        networking::cleanup();
    }

    return RETURN_SUCCESS;

} /* End of AgentMonitor */



/********************************************************************************************************************
 Description:           main function. Starts agent monitoring.
 
 Parameters:          null
 
 Return:                 int - Success/Failure

 Other Methods used: AgentMonitor()
 
*********************************************************************************************************************/
int main()
{
    char* pszPath;
    int nReturnValue = RETURN_SUCCESS;
	
    /* Checking environment variable TDK_PATH */
    pszPath = getenv ("TDK_PATH");
    if (pszPath != NULL)
    {
        std::cout << "TDK_PATH : " << pszPath << std::endl;
    }
    else
    {
        std::cout << "Alert!!! TDK_PATH not exported " << std::endl;
		
        return RETURN_FAILURE;   // Returns failure if TDK_PATH not exported
    }
	
    nReturnValue = AgentMonitor();
	
    return nReturnValue;
	
} /* End of main */



/* End of agentmain */




