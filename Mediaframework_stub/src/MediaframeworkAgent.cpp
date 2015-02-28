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

#include "MediaframeworkAgent.h"

char *rdkLogP = getenv("RDK_LOG_PATH");
char *tdkP = getenv("TDK_PATH");

string rdkLogPath = "NULL";
string tdkPath = "NULL";
#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int , char *, int );
#endif


/*helper functions for DVR sink*/
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


/*
	Convert the IP Address from string to long.
*/
long convertIPStrToLong(const char *ip_addr_str)
{
        long ipAddr, ip1, ip2, ip3, ip4;
        sscanf(ip_addr_str, "%4ld.%4ld.%4ld.%4ld", &ip1, &ip2, &ip3, &ip4);
	DEBUG_PRINT(DEBUG_TRACE, "ip1 = %ld, ip2 = %ld, ip3 = %ld, ip4 = %ld\n",ip1, ip2, ip3, ip4);
        ipAddr = ((ip1 << 24) & 0xFF000000) | ((ip2 << 16) & 0x00FF0000) | ((ip3 << 8) & 0x0000FF00) | (ip4 & 0x000000FF);
        return ipAddr;
}


static long long getCurrentTime()
{
	struct timeval tv;
	long long currentTime;

	gettimeofday( &tv, 0 );

	currentTime= (((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000);

	return currentTime;
}

/* Create test recording spec */
void createTestRecordingSpec (string recordingId, string playUrl, RecordingSpec &spec)
{
	char work[TITLE_LEN] = {'\0'};
	sprintf( work, "{\"title\":\"Test Recording for %s\"}", recordingId.c_str());

        spec.setRecordingId(recordingId);
	spec.addLocator( playUrl );
	spec.setProperties( work );
        spec.setStartTime( getCurrentTime());
        spec.setDuration(REC_DURATION);
        spec.setDeletePriority(PRIORITY);
        spec.setBitRate( RecordingBitRate_high );
}

std::string fetchStreamingInterface()
{
	DEBUG_PRINT(DEBUG_TRACE, "Fetch Streaming Interface function --> Entry\n");
	ifstream interfacefile;
	string Fetch_Streaming_interface_cmd, Streaming_Interface_name,line;
	Streaming_Interface_name = g_tdkPath + "/" + FETCH_STREAMING_INT_NAME;
/*	//Fetch_Streaming_interface_cmd = g_tdkPath + "/" + FETCH_STREAMING_INT_SCRIPT;
	//string fetch_streaming_int_chk= "source "+Fetch_Streaming_interface_cmd;
	//try
	{
		system((char*)fetch_streaming_int_chk());
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of streaming ip fetch script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE<DETAILS>Exception occured execution of streaming ip fetch script";
	
	}
*/

	interfacefile.open(Streaming_Interface_name.c_str());
	if(interfacefile.is_open())
	{
		if(getline(interfacefile,line)>0);
                {
                        interfacefile.close();
                        DEBUG_PRINT(DEBUG_LOG,"\nStreaming IP fetched fetched\n");
                        DEBUG_PRINT(DEBUG_TRACE, "Fetch Streaming Interface function--> Exit\n");
                        return line;
                }
                interfacefile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\nStreaming IP fetched not fetched\n");
                return "FAILURE<DETAILS>Proper result is not found in the streaming interface name file";
	}
	else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the streaming interface file.\n");
                return "FAILURE<DETAILS>Unable to open the streaming interface  file";
        }


}

IRMFMediaSource* createHNSrc(const std::string& url)
{
	RMFResult result= RMF_RESULT_SUCCESS;
	RMFMediaSourceBase *pSrc= 0;

	pSrc= new HNSource();
	if ( pSrc == 0 )
	{
		DEBUG_PRINT(DEBUG_ERROR, "createHNSrc: Error: unable to create HNSrc\n");
	}
	else
	{
		result= pSrc->init();
		if ( result != RMF_RESULT_SUCCESS )
		{
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc init failed with rc=0x%X\n", (unsigned int)result);
		}
		else
		{
			string streamingip;
			string streaming_interface;
		        size_t pos = 0;
			size_t found;
		        streaming_interface=fetchStreamingInterface();
		        found=streaming_interface.find("FAILURE");
		        if (found!=std::string::npos)
		        {
        			std::string delimiter = "<FAILURE>";
		                std::string token;
                		while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
		                	token = streaming_interface.substr(0, pos);
                	        	std::cout << token << std::endl;
	                        	streaming_interface.erase(0, pos + delimiter.length());
                 	}
				pSrc=0;
			}
			else
			{
				const char * streaming_interface_name = streaming_interface.c_str();
				streamingip=GetHostIP(streaming_interface_name);
        			string urlIn = url;
        			string http = "http://";
        			http.append(streamingip);
		        	cout<<"IP: "<<streamingip<<endl;
		       		size_t pos = 0;
        			pos = urlIn.find(":8080");
       	 			if (pos!=std::string::npos)
        			{
		                	urlIn = urlIn.replace(0,pos,http);
        			}	

        			cout<<"Final URL passed to Open(): "<<urlIn<<endl;
				result= pSrc->open( urlIn.c_str(), 0 );
				if ( result != RMF_RESULT_SUCCESS )
				{
					DEBUG_PRINT(DEBUG_ERROR, "HNSrc open(%s) failed with rc=0x%X", url.c_str(), (unsigned int) result );
				}
			}	
		}
	}

        if ( result != RMF_RESULT_SUCCESS )
        {
                if ( pSrc )
                {
                        delete pSrc;
                        pSrc= 0;
                }
        }

	return pSrc;
}

/*Helper function for QAMSource*/
static bool gThreadFlag = false;
static void getGthreadInstance()
{
	if(false == gThreadFlag)
	{
		if( ! g_thread_supported() )
			g_thread_init(NULL);
		gThreadFlag = true;
		DEBUG_PRINT(DEBUG_TRACE, "g_thread_init called and gThreadFlag is set to true\n");
	}

	DEBUG_PRINT(DEBUG_TRACE, "g_thread_init is up already\n");
}

string qamsrcpre_requisites()
{
        DEBUG_PRINT(DEBUG_TRACE, "QAM src pre_requisites --> Entry\n");
        ifstream logfile;
        string MF_testmodule_PR_cmd, MF_testmodule_PR_log,line;
        MF_testmodule_PR_cmd= g_tdkPath + "/" + QAM_PRE_REQUISITE_FILE;
        MF_testmodule_PR_log= g_tdkPath + "/" + QAM_PRE_REQUISITE_LOG_PATH;
        string pre_req_chk= MF_testmodule_PR_cmd;
        try
        {
                system((char *)pre_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of qam  pre-requisite script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE";
        }
        logfile.open(MF_testmodule_PR_log.c_str());
        if(logfile.is_open())
        {
                if(getline(logfile,line)>0);
                {
                        logfile.close();
                        DEBUG_PRINT(DEBUG_LOG,"\n qamsrc Pre-Requisites set\n");
                        DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Exit\n");
                        return line;
                }
                logfile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\n qamsrc Pre-Requisites not set\n");
                return "FAILURE";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the qamsrc pre-requisites log file.\n");
                return "FAILURE";
        }

        DEBUG_PRINT(DEBUG_TRACE, "QAM src pre_requisites --> Entry\n");
        return "FAILURE";
}


/**************************************************************************
Function name : MediaframeworkAgent::testmodulepre_requisites

Arguments     : None

Description   : Setting Pre-requisites needed to execute Mediaframework tests

***************************************************************************/
std::string MediaframeworkAgent::testmodulepre_requisites()
{
	#ifdef USE_SOC_INIT
        //Initialize SOC
        soc_init(1, "tdk_agent", 1);
	#endif
        DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Entry\n");
        ifstream logfile;
        string MF_testmodule_PR_cmd, MF_testmodule_PR_log,line;
        MF_testmodule_PR_cmd= g_tdkPath + "/" + PRE_REQUISITE_FILE;
        MF_testmodule_PR_log= g_tdkPath + "/" + PRE_REQUISITE_LOG_PATH;
        string pre_req_chk= "source "+MF_testmodule_PR_cmd;

	/*Check for the environment variable set or not */
	if(rdkLogP == NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nEnvironment variable not set for RDK_LOG_PATH\n");
		return "FAILURE<DETAILS>Environment variable not set for \"RDK_LOG_PATH\"";
	}
	else
	{
		rdkLogPath.assign(rdkLogP);		
		DEBUG_PRINT(DEBUG_TRACE,"\n RDK_LOG_PATH=%s\n",rdkLogPath.c_str());
	}
	
	if(tdkP == NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nEnvironment variable not set for TDK_PATH\n");
		return "FAILURE<DETAILS>Environment variable not set for \"TDK_PATH\"";
	}
	else
	{
		tdkPath.assign(tdkP);		
		DEBUG_PRINT(DEBUG_TRACE,"\n TDK_PATH=%s\n",tdkPath.c_str());
	}
	

        try
        {
                system((char *)pre_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of pre-requisite script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE<DETAILS>Exception occured execution of pre-requisite script";
        }
        logfile.open(MF_testmodule_PR_log.c_str());
        if(logfile.is_open())
        {
                if(getline(logfile,line)>0);
                {
                        logfile.close();
                        DEBUG_PRINT(DEBUG_LOG,"\nPre-Requisites set\n");
                        DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Exit\n");
                        return line;
                }
                logfile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\nPre-Requisites not set\n");
                return "FAILURE<DETAILS>Proper result is not found in the log file";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
                return "FAILURE<DETAILS>Unable to open the log file";
        }
	
	return "SUCCESS<DETAILS>SUCCESS";
}


/*************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent

Arguments     : NULL

Description   : Constructor for MediaframeworkAgent class
 ***************************************************************************/

MediaframeworkAgent::MediaframeworkAgent()
{
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent Initialized\n");
}

typedef std::list<std::pair<float, float> > range_list_t;

/**************************************************************************
  Function name : MediaframeworkAgent::initialize

Arguments     : Input arguments are Version string and MediaframeworkAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/

bool MediaframeworkAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Mediaframework Initialize----->Entry\n");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute, "TestMgr_MPSink_SetGetMute");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume, "TestMgr_MPSink_SetGetVolume");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges, "TestMgr_HNSrc_GetBufferedRanges");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State, "TestMgr_HNSrcMPSink_Video_State");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute, "TestMgr_HNSrcMPSink_Video_MuteUnmute");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume, "TestMgr_HNSrcMPSink_Video_Volume");

	/*DVR Recording List*/
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List, "TestMgr_DVR_Rec_List");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVR_CreateNewRecording, "TestMgr_DVR_CreateNewRecording");

	/*DVR sink*/
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm, "TestMgr_DVRSink_init_term");
	/*DVR Manager*/
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace, "TestMgr_DVRManager_GetSpace");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount, "TestMgr_DVRManager_GetRecordingCount");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex, "TestMgr_DVRManager_GetRecordingInfoByIndex");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex, "TestMgr_DVRManager_CheckRecordingInfoByIndex");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById, "TestMgr_DVRManager_GetRecordingInfoById");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoById, "TestMgr_DVRManager_CheckRecordingInfoById");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress, "TestMgr_DVRManager_GetIsRecordingInProgress");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize, "TestMgr_DVRManager_GetRecordingSize");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration, "TestMgr_DVRManager_GetRecordingDuration");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime, "TestMgr_DVRManager_GetRecordingStartTime");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration, "TestMgr_DVRManager_GetDefaultTSBMaxDuration");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB, "TestMgr_DVRManager_CreateTSB");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording, "TestMgr_DVRManager_ConvertTSBToRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording, "TestMgr_DVRManager_CreateRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording, "TestMgr_DVRManager_UpdateRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording, "TestMgr_DVRManager_DeleteRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount, "TestMgr_DVRManager_GetSegmentsCount");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex, "TestMgr_DVRManager_GetRecordingSegmentInfoByIndex");

#if 1
/*Optimised Code*/	

	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_CheckAudioVideoStatus,"TestMgr_CheckAudioVideoStatus");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_CheckRmfStreamerCrash,"TestMgr_CheckRmfStreamerCrash");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_ClearLogFile,"TestMgr_ClearLogFile");


	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementCreateInstance,"TestMgr_RmfElementCreateInstance");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementRemoveInstance,"TestMgr_RmfElementRemoveInstance");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementInit,"TestMgr_RmfElementInit");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementTerm,"TestMgr_RmfElementTerm");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementOpen,"TestMgr_RmfElementOpen");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementClose,"TestMgr_RmfElementClose");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementPlay,"TestMgr_RmfElementPlay");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementPause,"TestMgr_RmfElementPause");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementSetSpeed,"TestMgr_RmfElementSetSpeed");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetSpeed,"TestMgr_RmfElementGetSpeed");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementSetMediaTime,"TestMgr_RmfElementSetMediaTime");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaTime,"TestMgr_RmfElementGetMediaTime");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaInfo,"TestMgr_RmfElementGetMediaInfo");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetState,"TestMgr_RmfElementGetState");


	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_SinkSetSource,"TestMgr_RmfElement_Sink_SetSource");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle,"TestMgr_RmfElement_MpSink_SetVideoRectangle");

	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error,"TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init,"TestMgr_RmfElement_QAMSrc_RmfPlatform_Init");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit,"TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform,"TestMgr_RmfElement_QAMSrc_InitPlatform");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform,"TestMgr_RmfElement_QAMSrc_UninitPlatform");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods,"TestMgr_RmfElement_QAMSrc_UseFactoryMethods");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetTSID,"TestMgr_RmfElement_QAMSrc_GetTSID");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID,"TestMgr_RmfElement_QAMSrc_GetLTSID");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement,"TestMgr_RmfElement_QAMSrc_GetLowLevelElement");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement,"TestMgr_RmfElement_QAMSrc_FreeLowLevelElement");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI,"TestMgr_RmfElement_QAMSrc_ChangeURI");


	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_InitPlatform,"TestMgr_RmfElement_HNSink_InitPlatform");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_UninitPlatform,"TestMgr_RmfElement_HNSink_UninitPlatform");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetProperties,"TestMgr_RmfElement_HNSink_SetProperties");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetSourceType,"TestMgr_RmfElement_HNSink_SetSourceType");

#endif	
	return TEST_SUCCESS;
}


#if 1

static RMFQAMSrc* qamSource=NULL;
static RMFQAMSrc* new_qamsrc = NULL;
static DVRSource* dvrSource=NULL;
static HNSource* hnSource=NULL;
static MediaPlayerSink* mpSink=NULL;
static HNSink* hnSink=NULL;
static RMFQAMSrc *qamSrcs[7];

/*QAMSrc rmf platform instance */
static rmfPlatform *mPlatform = NULL;
static void* lowSrcElement = NULL;


bool MediaframeworkAgent::MediaframeworkAgent_CheckAudioVideoStatus(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckAudioVideoStatus -->Entry\n");
        char buffer[128];
	string script = req["audioVideoStatus"].asCString();	
        string result = "";
	FILE* pipe = NULL;

	cout<<"Checking for "<<script<<endl;
	pipe = popen(script.c_str(), "r");

        if (!pipe)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Error in opening pipe \n");
        	response["result"] = "FAILURE";
               	response["details"] = "Error in opening pipe";

                return TEST_FAILURE;
        }
        while(!feof(pipe)) {
                if(fgets(buffer, 128, pipe) != NULL)
                        result += buffer;
        }
        pclose(pipe);
        DEBUG_PRINT(DEBUG_TRACE, "Script Output: %s \n", script.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "Script Result: %s\n", result.c_str());
        std::cout << "Status: "<<result <<std::endl;


        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckAudoVideoStatus -->Exit\n");

        if (result.find("SUCCESS") != string::npos)
	{
        	response["result"] = "SUCCESS";
               	response["details"] = "Audio/Video playing SUCCESS";

                return TEST_SUCCESS;
	}
        else
	{
        	response["result"] = "FAILURE";
               	response["details"] = "Audio/Video playing FAILURE";

                return TEST_FAILURE;	
	}
}

bool MediaframeworkAgent::MediaframeworkAgent_ClearLogFile(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_ClearLogFile -->Entry\n");
	string logFileToClear = req["logFileToClear"].asCString();
	string logFilePath = ">" + rdkLogPath + "/" + logFileToClear;
        DEBUG_PRINT(DEBUG_LOG,"Log_deletion is %s\n", logFilePath.c_str());

        /* To handle exception for system call*/
        try
        {
                system((char *)logFilePath.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                response["result"] = "FAILURE";
		response["details"] = "Clearing the log file failed!!!";
		
		return TEST_FAILURE;
        }

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_ClearLogFile -->Exit\n");
	response["details"] = "Log file cleared";
        response["result"] = "SUCCESS";
	
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_CheckRmfStreamerCrash(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckRmfStreamerCrash -->Entry\n");
	
	string ocapLogFile = req["logFile"].asCString();
	string ocapLogToTdkFolder = req["FileNameToCpTdkPath"].asCString();
	string patternToSearch = req["patternToSearch"].asCString();
	
	DEBUG_PRINT(DEBUG_LOG,"TDK_PATH: %s\n", tdkPath.c_str());
	DEBUG_PRINT(DEBUG_LOG,"RDK_LOG_PATH: %s\n", rdkLogPath.c_str());
	
	/*Copying the file form /opt/logs to /opt/TDK and setting the permission for the file copied. */
	string logFileCopy = "cp -r " + rdkLogPath + "/" + ocapLogFile+ " " + tdkPath + "/" + ocapLogToTdkFolder;
	string setPerm = "chmod 777 " + tdkPath + "/" + ocapLogToTdkFolder;

	DEBUG_PRINT(DEBUG_LOG,"copying is %s\n", logFileCopy.c_str());
        DEBUG_PRINT(DEBUG_LOG,"chmod is %s\n", setPerm.c_str());

        string RecorderLogFilePath = tdkPath + "/" + ocapLogToTdkFolder;
	string line_Recorder_Log;
	

	DEBUG_PRINT(DEBUG_LOG,"File Name: %s\n", RecorderLogFilePath.c_str());
	if(system((char *)logFileCopy.c_str()) == 0 && system((char*)setPerm.c_str()) == 0)
	{
        	ifstream RecorderLogFile;
	        RecorderLogFile.open(RecorderLogFilePath.c_str());
	        if(RecorderLogFile.is_open())
        	{
			DEBUG_PRINT(DEBUG_LOG,"File %s open success \n", RecorderLogFilePath.c_str());
                	while (!RecorderLogFile.eof())
	                {
        	                if(getline(RecorderLogFile,line_Recorder_Log)>0)
                	        {
                        	        if(line_Recorder_Log.find(patternToSearch.c_str()) != string::npos)
                                	{
                	                                response["result"] = "SUCCESS";
                        	                        response["details"] = "Pattern found in Log file";

							DEBUG_PRINT(DEBUG_LOG,"Pattern found in Log file.\n");

							RecorderLogFile.close();
        						DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckRmfStreamerCrash -->Exit\n");
							return TEST_SUCCESS;
        	                        }
                	        }
                        	else
	                        {
        	                        response["result"] = "FAILURE";
                	                response["details"] = "Pattern not found in Log file";
					
					DEBUG_PRINT(DEBUG_LOG,"Pattern not found in Log file.\n");
					
					RecorderLogFile.close();
        				DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckRmfStreamerCrash -->Exit\n");
					return TEST_FAILURE;
                        	}
	                }
        	}
	}
	else
	{
		cout<<"Copy of log file or setting permission failure!!!!"<<endl;
		response["result"] = "FAILURE";
		response["details"] = "Copy of log file or setting permission failure!!!!";

        	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckRmfStreamerCrash -->Exit\n");
		return TEST_FAILURE;
	}

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_CheckRmfStreamerCrash -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementCreateInstance(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementCreateInstance -->Entry\n");
	
	string rmfInstance = req["rmfElement"].asCString();	
	string factoryFlag = req["factoryEnable"].asCString();
	const char *qamUrl = req["qamSrcUrl"].asCString();
	string newQamInsFlag = req["newQamSrc"].asCString();
	const char *newQamUrl = req["newQamSrcUrl"].asCString();
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Insatnce: %s\n",rmfInstance.c_str());

	if(rmfInstance == "QAMSrc")
	{	
		//RMFQAMSrc::disableCaching();
		cout<<"inside qamsrc"<<endl;
		if(factoryFlag == "true")
		{	
			cout<<"inside qamsrc factory method true"<<endl;
			if(newQamInsFlag == "false")
			{
				cout<<"inside qamsrc new flag false"<<endl;
				qamSource = RMFQAMSrc::getQAMSourceInstance(qamUrl);
				cout<<"inside qamsrc new flag false after"<<endl;
        			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc instance created by using getQAMSourceInstance() \n");
			}
			else
			{
				switch(numberOfTimeChannelChange)
				{
				case 0:
					cout<<"inside qamsrc new flag true"<<endl;
					new_qamsrc = RMFQAMSrc::getQAMSourceInstance(newQamUrl);
					cout<<"inside qamsrc new flag true after"<<endl;
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new %d instance created by using getQAMSourceInstance() \n",numberOfTimeChannelChange);
					break;
				case 1: 
				case 2: 
				case 3: 
				case 4: 
				case 5: 
				case 6: 
					qamSrcs[numberOfTimeChannelChange - 1] = RMFQAMSrc::getQAMSourceInstance(newQamUrl);
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new %d instance created by using getQAMSourceInstance() \n",numberOfTimeChannelChange);
					break;
				default:
					break;
				}
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
			}
		}
		else
		{	
			qamSource = new RMFQAMSrc();
        		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new instance created \n");
		}
		
		if (!qamSource)
		{
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc instance creation failed";
        	        DEBUG_PRINT(DEBUG_ERROR, "QAMSrc instance creation failed \n");

	                return TEST_FAILURE;
		}

        	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc instance created \n");
		response["details"] = "QAMSrc instance creation successful";
	}
	if(rmfInstance == "DVRSrc")
	{
		dvrSource = new DVRSource();
		if ( NULL == dvrSource )
	        {
        	        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create DVRSrc\n");
        	        response["result"] = "FAILURE";
               		response["details"] = "Error: unable to create DVRSrc";

	                return TEST_FAILURE;
        	}
        	DEBUG_PRINT(DEBUG_TRACE, "DVRSrc is created \n");
		response["details"] = "DVR instance creation successful";
	}
	if(rmfInstance == "HNSrc")
	{
		hnSource = new HNSource();
                if ( NULL == hnSource )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create HNSrc\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Error: unable to create HNSrc";

                        return TEST_FAILURE;
                }
        	DEBUG_PRINT(DEBUG_TRACE, "HNSrc is created \n");
                response["details"] = "HNSrc instance creation successful";
	}
	if(rmfInstance == "MPSink")
	{
		mpSink = new MediaPlayerSink();
                if ( NULL == mpSink )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create MediaPlayerSink\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Error: unable to create MediaPlayerSink";

                        return TEST_FAILURE;
                }
        	DEBUG_PRINT(DEBUG_TRACE, "MediaPlayerSink is created \n");
                response["details"] = "MediaPlayerSink instance creation successful";
	}
	if(rmfInstance == "HNSink")
	{
		hnSink = new HNSink;
                if ( NULL == hnSink )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create hnSink\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Error: unable to create hnSink";

                        return TEST_FAILURE;
                }
        	DEBUG_PRINT(DEBUG_TRACE, "HNSink is created \n");
                response["details"] = "HNSink instance creation successful";
	}
	if(rmfInstance == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be created\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be created";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementCreateInstance -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementRemoveInstance(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementRemoveInstance -->Entry\n");

	string rmfInstance = req["rmfElement"].asCString();	
	string factoryFlag = req["factoryEnable"].asCString();
	string newQamInsFlag = req["newQamSrc"].asCString();
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();
	
        DEBUG_PRINT(DEBUG_TRACE, "RMF Insatnce: %s\n",rmfInstance.c_str());

	if(rmfInstance == "QAMSrc")
	{
		if(factoryFlag == "true")		
		{
			if (newQamInsFlag == "false")
			{
				RMFQAMSrc::freeQAMSourceInstance(qamSource);
        			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc instance freed using freeQAMSourceInsatnce() \n");
			}
			else
			{
				cout<<"inside qamsrc new flag true"<<endl;
				switch(numberOfTimeChannelChange)
				{
				case 0:
					RMFQAMSrc::freeQAMSourceInstance(new_qamsrc);
                	                DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new %d instance freed using freeQAMSourceInsatnce() \n",numberOfTimeChannelChange);
					break;
				case 1:
				case 2:
				case 3:
				case 4:
				case 5:
				case 6:
					RMFQAMSrc::freeQAMSourceInstance(qamSrcs[numberOfTimeChannelChange - 1]);
                	                DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new %d instance freed using freeQAMSourceInsatnce() \n",numberOfTimeChannelChange);
					break;
				default: break;
				}
			}
			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
		}
		else
		{
			delete qamSource;	
        		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc instance deleted \n");
		}
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc is deleted \n");
		response["details"] = "QAMSrc instance deleted successful";
	}
	if(rmfInstance == "DVRSrc")
	{
		delete dvrSource;
        	
		DEBUG_PRINT(DEBUG_TRACE, "DVRSrc is deleted \n");
		response["details"] = "DVR instance deleted successful";
	}
	if(rmfInstance == "HNSrc")
	{
		delete hnSource;
        	
		DEBUG_PRINT(DEBUG_TRACE, "HNSrc is deleted \n");
                response["details"] = "HNSrc instance deleted successful";
	}
	if(rmfInstance == "MPSink")
	{
		delete mpSink;
        	
		DEBUG_PRINT(DEBUG_TRACE, "MediaPlayerSink is deleted \n");
                response["details"] = "MediaPlayerSink instance deleted successful";
	}
	if(rmfInstance == "HNSink")
	{
		delete hnSink;
        	
		DEBUG_PRINT(DEBUG_TRACE, "HNSink is deleted \n");
                response["details"] = "HNSink instance deleted successful";
	}
	if(rmfInstance == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be deleted\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be deleted";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementRemoveInstance -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementInit(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementInit -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	
	if(rmfComponent == "QAMSrc")
	{
		retResult = qamSource->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc init() FAILURE";
			
			delete qamSource;
			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc init successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc init() FAILURE";
			
			delete dvrSource;
			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc init successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc init() FAILURE";

			delete hnSource;
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc init() successful";
	}
	if(rmfComponent == "MPSink")
	{
		retResult = mpSink->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MediaPlayerSink init() FAILURE";

			delete mpSink;
			DEBUG_PRINT(DEBUG_ERROR, "MediaPlayerSink init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MediaPlayerSink init() successful";
	}
	if(rmfComponent == "HNSink")
	{
		retResult = hnSink->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSink init() FAILURE";

			delete hnSink;
			DEBUG_PRINT(DEBUG_ERROR, "HNSink init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSink init() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate init()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate init()";
                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementInit -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementTerm(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementTerm -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "QAMSrc")
	{
		retResult = qamSource->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc term() successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc term() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc term() successful";
	}
	if(rmfComponent == "MPSink")
	{
		retResult = mpSink->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MediaPlayerSink term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "MediaPlayerSink term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MediaPlayerSink term() successful";
	}
	if(rmfComponent == "HNSink")
	{
		retResult = hnSink->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSink term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSink term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSink term() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate term()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate term()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementTerm -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementOpen(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementOpen -->Entry\n");
	
        string streamingip;
	
	string streaming_interface;
	size_t pos = 0;
	size_t found;
	streaming_interface=fetchStreamingInterface();
	found=streaming_interface.find("FAILURE");
	if (found!=std::string::npos)
	{
        	std::string delimiter = "<FAILURE>";
		std::string token;
                while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
		     	token = streaming_interface.substr(0, pos);
                       	std::cout << token << std::endl;
	              	streaming_interface.erase(0, pos + delimiter.length());
                 }
                 response["result"] = "FAILURE";
                 response["details"] = token;
                 return TEST_FAILURE;
	}

	const char * streaming_interface_name = streaming_interface.c_str();
	streamingip=GetHostIP(streaming_interface_name);
	string urlIn = req["url"].asCString();
	string http = "http://";

        http.append(streamingip);

	cout<<"After append relace string: "<<http<<endl;

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());


	pos = urlIn.find(":8080");
	if (pos!=std::string::npos)
	{	
		urlIn = urlIn.replace(0,pos,http);
	}	
	
	cout<<"Final URL passed to Open(): "<<urlIn<<endl;

	if(rmfComponent == "QAMSrc")
	{
		retResult = qamSource->open(req["url"].asCString(),0);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE"; 
	                response["details"] = "QAMSrc open() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc open() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc open() successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->open(req["url"].asCString(),0);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE"; 
	                response["details"] = "DVRSrc open() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc open() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc open() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->open(urlIn.c_str(),0);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc open() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc open() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc open() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate open()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate open()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementOpen -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementClose(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementClose -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());

	if(rmfComponent == "QAMSrc")
	{
		retResult = qamSource->close();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc close() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc close() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc close() successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->close();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc close() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc close() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc close() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->close();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc close() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc close() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc close() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate close()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate close()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementClose -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementPause(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPause -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		
	string newQamInsFlag = req["newQamSrc"].asCString();	
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	
	if(rmfComponent == "QAMSrc")
	{
		if(newQamInsFlag == "false")
		{
			retResult = qamSource->pause();	
			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc old pause()\n");
		}
		else
		{
			switch(numberOfTimeChannelChange)
			{
			case 0:
				retResult = new_qamsrc->pause();
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new pause()\n");
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance pause called \n",numberOfTimeChannelChange);
				break;
			case 1:
			case 2:
			case 3:
			case 4:
			case 5:
			case 6:
				retResult = qamSrcs[numberOfTimeChannelChange - 1]->pause();
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new pause()\n");
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance pause called \n",numberOfTimeChannelChange);
				break;
			default:
				break;
			}
			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
		}

		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc pause() FAILURE";

			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc pause() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc pause() successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->pause();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc pause() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc pause() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc pause() successful";
	}

	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->pause();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc pause() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc pause() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc pause() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to initiate pause()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to initiate pause()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPause -->Exit\n");
	return TEST_SUCCESS;
}


bool MediaframeworkAgent::MediaframeworkAgent_RmfElementPlay(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPlay -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();	
	string newQamInsFlag = req["newQamSrc"].asCString();	
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();
	
	/* 0 - default, play without passing speed and mediaTime arguments.
           1 - play with passing speed and mediaTime arguments */
        int playArgs = req["defaultPlay"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	
	if(rmfComponent == "QAMSrc")
	{
		if(1 == playArgs)
		{
			float speed = req["playSpeed"].asFloat();
		        double time = req["playTime"].asDouble();
			if(newQamInsFlag == "false")
			{
				retResult = qamSource->play(speed,time);	
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc play() with speed and time\n");
			}
			else
			{
				switch(numberOfTimeChannelChange)
				{
				case 0:	
					retResult = new_qamsrc->play(speed,time);	
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new play() with speed and time\n");	
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance play called \n",numberOfTimeChannelChange);
					break;	
				case 1:
				case 2:	
				case 3:	
				case 4:	
				case 5:	
				case 6:	
					retResult = qamSrcs[numberOfTimeChannelChange - 1]->play(speed,time);	
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc new play() with speed and time\n");	
					DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance play called \n",numberOfTimeChannelChange);
					break;
				default:
					break;	
				}
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
			}
		}
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "QAMSrc play() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc play() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "QAMSrc play() successful";
	}
	if(rmfComponent == "DVRSrc")
	{
		if(0 == playArgs)
		{
			retResult = dvrSource->play();	
		}
		else
		{
			float speed = req["playSpeed"].asFloat();
		        double time = req["playTime"].asDouble();
			retResult = dvrSource->play(speed,time);	
			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc play() with speed and time\n");
			
		}
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc play() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc play() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc play() successful";
	}
	//int retValue;
	//double mediaTime;
	if(rmfComponent == "HNSrc")
	{

		//Video length unknown.So, passing zero.
	        retResult = hnSource->setVideoLength(0);
		cout<<"HNSrc setVideoLength() return value "<<retResult<<endl;

		if(0 == playArgs)
                {
                        retResult = hnSource->play();

/*
			sleep(5);
        		retValue=hnSource->setMediaTime(0);
        		cout<<"Return of Set Media time "<<retValue<<endl;
        		sleep(5);
        		retValue = hnSource->getMediaTime(mediaTime);
        		cout<<"Return of get Media time "<<retValue<<endl;
        		cout<<"get Media time value"<<mediaTime<<endl;
*/
	
                }
                else
                {

                        float speed = req["playSpeed"].asFloat();
                        double time = req["playTime"].asDouble();
                        retResult = hnSource->play(speed,time);
/*
			sleep(5);	
        		retValue = hnSource->setMediaTime(0);
        		cout<<"Return of Set Media time "<<retValue<<endl;
        		sleep(5);
        		retValue = hnSource->getMediaTime(mediaTime);
        		cout<<"Return of get Media time "<<retValue<<endl;
        		cout<<"get Media time value"<<mediaTime<<endl;
*/
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc play() with speed and time\n");
                }
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc play() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc play() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc play() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate play()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate play()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPlay -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementSetSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetSpeed -->Entry\n");

        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
        float playSpeed = req["playSpeed"].asFloat();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s \n",rmfComponent.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "SeSpeed: %f \n",playSpeed);
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->setSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc setSpeed() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc setSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "DVRSrc setSpeed() successful";
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->setSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
		 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc setSpeed() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc setSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "HNSrc setSpeed() successful";
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to setSpeed()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to setSpeed()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetSpeed -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetSpeed -->Entry\n");

        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream details;

        float playSpeed;

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc getSpeed() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc getSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
		details << "DVRSrc getSpeed() successful, Speed:" << playSpeed;
                response["details"] = details.str();
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc getSpeed() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc getSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
		details << "HNSrc getSpeed() successful, Speed:" << playSpeed;
                response["details"] = details.str();
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to getSpeed()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to getSpeed()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetSpeed -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_SinkSetSource(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SinkSetSource -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfSrcComponent = req["rmfSourceElement"].asCString();	
	string rmfSinkComponent = req["rmfSinkElement"].asCString();
	string newQamInsFlag = req["newQamSrc"].asCString();
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Src Component: %s\n",rmfSrcComponent.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "RMF Sink Component: %s\n",rmfSinkComponent.c_str());
	
	if(rmfSrcComponent == "DVRSrc" && rmfSinkComponent == "MPSink")
	{
		if(dvrSource == NULL || mpSink == NULL)
		{
			response["result"] = "FAILURE";
	                response["details"] = "Create DVRSrc/MPSink  instances first";

			DEBUG_PRINT(DEBUG_ERROR, "Create DVRSrc/MPSink Instance \n");
			return TEST_FAILURE;

		}
		retResult = mpSink->setSource(dvrSource);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MPSink setSource() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MPSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "MPSink setSource() successful\n");
	}

	if(rmfSrcComponent == "HNSrc" && rmfSinkComponent == "MPSink")
	{
		if(hnSource == NULL || mpSink == NULL)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Create HNSrc/MPSink  instances first";

                        DEBUG_PRINT(DEBUG_ERROR, "Create HNSrc/MPSink Instance \n");
                        return TEST_FAILURE;

                }
                retResult = mpSink->setSource(hnSource);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "MPSink setSource() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "MPSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "MPSink setSource() successful\n");
	}
	if(rmfSrcComponent == "QAMSrc" && rmfSinkComponent == "MPSink")
	{
		if(qamSource == NULL || mpSink == NULL)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Create QAMSrc/MPSink instances first";

                        DEBUG_PRINT(DEBUG_ERROR, "Create QAMSrc/MPSink Instance \n");
                        return TEST_FAILURE;

                }
		if(newQamInsFlag == "false")
		{
	                retResult = mpSink->setSource(qamSource);
		}
		else
		{
			switch(numberOfTimeChannelChange)
			{
			case 0:
		                retResult = mpSink->setSource(new_qamsrc);
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance setSource set \n",numberOfTimeChannelChange);
				break;
			case 1:
			case 2:
			case 3:
			case 4:
			case 5:
			case 6:
		                retResult = mpSink->setSource(qamSrcs[numberOfTimeChannelChange - 1]);
				DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance setSource set \n",numberOfTimeChannelChange);
				break;
			default:
				break;	
			}
			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
		}

                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "mpSink setSource() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "mpSink setSource() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "mpSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "mpSink setSource() successful\n");
	}
	if(rmfSrcComponent == "QAMSrc" && rmfSinkComponent == "HNSink")
	{
		if(qamSource == NULL || hnSink == NULL)
                {
				
				
		}

                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "mpSink setSource() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "mpSink setSource() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "mpSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "mpSink setSource() successful\n");
	}
	if(rmfSrcComponent == "QAMSrc" && rmfSinkComponent == "HNSink")
	{
		if(qamSource == NULL || hnSink == NULL)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Create QAMSrc/HNSink instances first";

                        DEBUG_PRINT(DEBUG_ERROR, "Create QAMSrc/HNSink Instance \n");
                        return TEST_FAILURE;

                }
                retResult = hnSink->setSource(qamSource);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "hnSink setSource() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "hnSink setSource() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "hnSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "hnSink setSource() successful\n");
	}
	if(rmfSrcComponent == "" && rmfSinkComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be used\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be used";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SinkSetSource -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	bool applyNow = req["apply"].asInt();
	unsigned x = req["X_Value"].asInt();
	unsigned y = req["Y_Value"].asInt();
	unsigned height = req["height"].asInt();
	unsigned width = req["width"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value x: %u\n",x);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value y: %u\n",y);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value height: %u\n",height);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value width: %u\n",width);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value apply: %d\n",applyNow);
		
	if(mpSink == NULL)	
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Create the Mediaframework Instance\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Create the Mediaframework Instance";

                return TEST_FAILURE;
	}
	
	retResult = mpSink->setVideoRectangle(x, y, width, height,applyNow);	
	if(RMF_RESULT_SUCCESS != retResult)
	{
		response["result"] = "FAILURE";
	        response["details"] = "MPSink setVideoRectangle() FAILURE";

		DEBUG_PRINT(DEBUG_ERROR, "MPSink setVideoRectangle() FAILURE\n");
		return TEST_FAILURE;
	}
	response["details"] = "MPSink setVideoRectangle() SUCCESS";
	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SetVideoRectangle -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementSetMediaTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetMediaTime -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
        double mediaTime = req["mediaTime"].asDouble();

        DEBUG_PRINT(DEBUG_TRACE, "Media Time: %f\n",mediaTime);

        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->setMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                {
  	                response["result"] = "FAILURE";
                        response["details"] = "DVRSrc SetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc SetMediaTime() FAILURE\n");
                        return TEST_SUCCESS;
                }
                response["details"] = "DVRSrc SetMediaTime() successful";
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->setMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc SetMediaTime() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc SetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "HNSrc SetMediaTime() successful";
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to SetMediaTime()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to SetMediaTime()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetMediaTime -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaTime -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream detail_string;
        double mediaTime;


        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());

        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"DVRSrc GetMediaTime() successful, MediaTime:"<< mediaTime;
                response["details"] = detail_string.str();
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc GetMediaTime() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"HNSrc GetMediaTime() successful, MediaTime:"<<mediaTime;
                response["details"] = detail_string.str();
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to GetMediaTime()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to GetMediaTime()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaTime -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaInfo(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaInfo -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream detail_string;
	RMFMediaInfo mediaInfo;        

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getMediaInfo(mediaInfo);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"DVRSrc GetMediaInfo() successful, MediaStartTime:"<< mediaInfo.m_startTime <<" MediaDuration:"<<mediaInfo.m_duration;
                response["details"] = detail_string.str();
        }
        
	if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to GetMediaInfo()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to GetMediaInfo()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaInfo -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetState(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetState -->Entry\n");
        RMFStateChangeReturn retResult = RMF_STATE_CHANGE_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	RMFState currentState;
        
        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	
	if(rmfComponent == "QAMSrc")
	{
		retResult = qamSource->getState(&currentState,NULL);
		if(RMF_STATE_CHANGE_FAILURE == retResult)
		{
			response["result"] = "FAILURE";
			response["details"] = "QAMSrc GetState() FAILURE";
			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc GetState() FAILURE\n");

			return TEST_FAILURE;
		}
		switch(currentState)
		{
			case RMF_STATE_VOID_PENDING: 
				 response["details"] = "QAMSrc GetState() successful, Current State is: VOID";
				 break;
			case RMF_STATE_NULL:
				 response["details"] = "QAMSrc GetState() successful, Current State is: NULL";
				 break;
			case RMF_STATE_READY:
				 response["details"] = "QAMSrc GetState() successful, Current State is: READY";
				 break;
			case RMF_STATE_PAUSED: 
				 response["details"] = "QAMSrc GetState() successful, Current State is: PAUSED";
				 break;
			case RMF_STATE_PLAYING:
				 response["details"] = "QAMSrc GetState() successful, Current State is: PLAYING";
				 break;
			default: 
				 response["details"] = "QAMSrc GetState() successful, Current State is: INVALID";
				 break;
		}
	}
	if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getState(&currentState,NULL);
                if(RMF_STATE_CHANGE_FAILURE == retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetState() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetState() FAILURE\n");
                        return TEST_FAILURE;
                }
		switch(currentState)
		{
			case RMF_STATE_VOID_PENDING: 
 	        	    	 response["details"] = "DVRSrc GetState() successful, Current State is: VOID";
	 			 break;
			case RMF_STATE_NULL:
				 response["details"] = "DVRSrc GetState() successful, Current State is: NULL";
				 break;
			case RMF_STATE_READY:
				 response["details"] = "DVRSrc GetState() successful, Current State is: READY";
				 break;
			case RMF_STATE_PAUSED: 
				 response["details"] = "DVRSrc GetState() successful, Current State is: PAUSED";
				 break;
			case RMF_STATE_PLAYING:
				 response["details"] = "DVRSrc GetState() successful, Current State is: PLAYING";
				 break;
			default: 
				 response["details"] = "DVRSrc GetState() successful, Current State is: INVALID";
				 break;
		}
        }

        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getState(&currentState,NULL);
                if(RMF_STATE_CHANGE_FAILURE == retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc GetState() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc GetState() FAILURE\n");
                        return TEST_FAILURE;
                }
		switch(currentState)
		{
			case RMF_STATE_VOID_PENDING: 
				 response["details"] = "HNSrc GetState() successful, Current State is: VOID";
				 break;
			case RMF_STATE_NULL:
				 response["details"] = "HNSrc GetState() successful, Current State is: NULL";
				 break;
			case RMF_STATE_READY:
				 response["details"] = "HNSrc GetState() successful, Current State is: READY";
				 break;
			case RMF_STATE_PAUSED: 
				 response["details"] = "HNSrc GetState() successful, Current State is: PAUSED";
				 break;
			case RMF_STATE_PLAYING:
				 response["details"] = "HNSrc GetState() successful, Current State is: PLAYING";
				 break;
			default: 
				 response["details"] = "HNSrc GetState() successful, Current State is: INVALID";
				 break;
		}
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to GetState()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to GetState()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetState -->Exit\n");
        return TEST_SUCCESS;
}

#if 1
bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error -->Entry\n");
	string logPath = req["logPath"].asCString();
	
	string cmd = "cat " + logPath + " | grep -i \"SPTSRead: Event time\"";
	//cout<<"Cmd:"<<cmd<<endl;

	if(system(cmd.c_str()) == 0)
	{
		cout<<"SUCCESS: Pattern matched!!!!"<<endl;
		response["result"] = "SUCCESS";
		response["details"] = "Pattern matched";
	}
	else
	{
		cout<<"FAILURE: Pattern not found!!!!"<<endl;
		response["result"] = "FAILURE";
		response["details"] = "Pattern not found";
	}
	

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPatform_Init -->Entry\n");
	int platformRes = RMF_SUCCESS;

#if 1
	string result;
	result = qamsrcpre_requisites();
	/*Checking for pre_requisites*/
	if(result == "FAILURE")
	{
                response["result"] = "FAILURE";
                response["details"] = "Mediaframework, QAMSrc related pre_requisites failed";
                DEBUG_PRINT(DEBUG_ERROR, "Mediaframework, QAMSrc related pre_requisites failed\n");

                return TEST_FAILURE;
	}
#endif

	/* Initialzing the gthread instance */
	getGthreadInstance();
		
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);			
	
        if(RMF_SUCCESS != platformRes)
        {
                response["result"] = "FAILURE";
                response["details"] = "RMF Platform init failed";
                DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        response["details"] = "RMF Platform init success";
        DEBUG_PRINT(DEBUG_TRACE, "RMF Platform init success and result is %d\n",platformRes);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPatform_Uninit -->Entry\n");
	int platformRes = RMF_SUCCESS;

	platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

        if(RMF_SUCCESS != platformRes)
        {
                response["result"] = "FAILURE";
                response["details"] = "RMF Platform uninit failed";
                DEBUG_PRINT(DEBUG_ERROR, "RMF Platform uninit failed and result is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
        response["result"] = "SUCCESS";
        response["details"] = "RMF Platform uninit success";
        DEBUG_PRINT(DEBUG_TRACE, "RMF Platform uninit success and result is %d\n",platformRes);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform -->Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;

	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc init_platform success";
        DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform success and result is %ld\n",retResultQAMSource);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_InitPlatform -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform -->Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;

	retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc uninit_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc uninit_platform failed and result is %ld\n",retResultQAMSource);

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc uninit_platform success";
        DEBUG_PRINT(DEBUG_ERROR, "QAMSrc uninit_platform success and result is %ld\n",retResultQAMSource);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_UninitPlatform -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods -->Entry\n");
	bool useFactory, rmfUseFactory;
	FILE *fp = NULL;
        char resultBuffer[BUFFER_LENGTH] = {'\0'};

	useFactory = RMFQAMSrc::useFactoryMethods();

	/*Reading the rmfconfig.ini file check whether the flag is set to true or false */
	fp = popen(CMD,"r");
	if(fp == NULL)
        {
                response["result"] = "FAILURE";
                response["details"] = "Popen error, popen failed to open";
                DEBUG_PRINT(DEBUG_ERROR, "Popen error, popen failed to open\n");

                return TEST_FAILURE;
        }
	if(fgets(resultBuffer,BUFFER_LENGTH,fp)!= NULL)
        {
                DEBUG_PRINT(DEBUG_TRACE, "In /etc/rmfconfig.ini, QAMSRC.FACTORY.ENABLED=%s \n",resultBuffer);
        }
        else
        {
                response["result"] = "FAILURE";
                response["details"] = "Cannot read /etc/rmfconfig.ini";
                DEBUG_PRINT(DEBUG_ERROR, "Cannot read /etc/rmfconfig.ini\n");

                return TEST_FAILURE;
        }
	pclose(fp);
	
	if (strncmp("TRUE",resultBuffer,strlen(resultBuffer)))
	{
		rmfUseFactory = true;
	}
	else
	{
		rmfUseFactory = false;
	}
	
	if(rmfUseFactory == useFactory)
	{
                response["result"] = "SUCCESS";
                response["details"] = "QAMSrc useFactoryMethods() successful";

        	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc useFactoryMethods() successful\n");
	}
	else
	{
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc useFactoryMethods() failure";

        	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc useFactoryMethods() failure\n");
		return TEST_FAILURE;
	}

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetTSID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetTSID -->Entry\n");
	unsigned int tsID;
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;

        retResultQAMSource = qamSource->getTSID(tsID);
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc getTSID is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc getTSID failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getTSID failed and result is %ld\n",retResultQAMSource);

                return TEST_FAILURE;
        }

	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getTSID value: %u\n",tsID);

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc getTSID success";
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getTSID success and result is %ld\n",retResultQAMSource);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetTSID -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID -->Entry\n");
	unsigned char ltsID;
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;

        retResultQAMSource = qamSource->getLTSID(ltsID);
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc getLTSID is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc getLTSID failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getLTSID failed and result is %ld\n",retResultQAMSource);

                return TEST_FAILURE;
        }

	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getLTSID value is %u\n",(unsigned) ltsID);

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc getLTSID success";
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getLTSID success and result is %ld\n",retResultQAMSource);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement -->Entry\n");

	lowSrcElement = RMFQAMSrc::getLowLevelElement();

        if (NULL == lowSrcElement)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc getLowlevelelement failure";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getLowlevelelement failure\n");

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc getLowLevelElement() success";
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getLowLevelElement() success \n");

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement -->Entry\n");

	RMFQAMSrc::freeLowLevelElement(lowSrcElement);

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc freeLowLevelElement() success";
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeLowLevelElement() success\n");

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI -->Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	const char *new_ocaplocator = req["url"].asCString();
	bool newInstance;
	int numberOfTimeChannelChange = req["numOfTimeChannelChange"].asInt();
        //RMFQAMSrc *new_qamsrc = new RMFQAMSrc();
	
	switch(numberOfTimeChannelChange)
	{
	case 0:
		retResultQAMSource = RMFQAMSrc::changeURI(new_ocaplocator,qamSource,&new_qamsrc,newInstance);
	        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc changeURI is %ld\n",retResultQAMSource);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance changeURI called \n",numberOfTimeChannelChange);
		break;
	case 1: 		
		retResultQAMSource = RMFQAMSrc::changeURI(new_ocaplocator,new_qamsrc,&qamSrcs[numberOfTimeChannelChange - 1],newInstance);
	        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc changeURI is %ld\n",retResultQAMSource);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance changeURI called \n",numberOfTimeChannelChange);
		break;
	case 2: 		
	case 3: 		
	case 4: 		
	case 5: 		
	case 6: 		
		retResultQAMSource = RMFQAMSrc::changeURI(new_ocaplocator,qamSrcs[numberOfTimeChannelChange - 2],&qamSrcs[numberOfTimeChannelChange - 1],newInstance);
	        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc changeURI is %ld\n",retResultQAMSource);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc %d instance changeURI called \n",numberOfTimeChannelChange);
		break;
	default: break;
	}
	
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc switch exit\n");
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
        	response["result"] = "FAILURE";
	        response["details"] = "QAMSrc changeURI() failed";
	        DEBUG_PRINT(DEBUG_ERROR, "QAMSrc changeURI() failed and result is %ld\n",retResultQAMSource);
		
		return TEST_FAILURE;
	}
	
        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc changeURI() success";
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc changeURI() success and result is %ld\n",retResultQAMSource);

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetProperties(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_SetProperties -->Entry\n");
	
	HNSinkProperties_t hnProps;
	memset( &hnProps, 0, sizeof(hnProps) );

	string urlIn = req["url"].asCString();
	string dtcpFlag = req["dctpEnable"].asCString();
        int socketId = req["socketId"].asInt();
        string streamIp = req["streamIp"].asCString();
	int type = req["typeFlag"].asInt();
	string useChunk	= req["useChunkTransfer"].asCString();

	string streamingIp;
        std::size_t found;
	
	if( dtcpFlag == "true")
	{
		hnProps.dtcp_enabled = true;
		cout << "in dtcp true"<<endl;
	}
	else
	{
		hnProps.dtcp_enabled = false;
		cout << "in dtcp false"<<endl;
	}
        hnProps.dtcp_cci = 0x01; //Get EMI value from the source stream CCI. Setting to Copy-No-More as default.

	if( useChunk == "true")
	{
		hnProps.use_chunked_transfer = true;
		cout << "in useChunkTransfer true"<<endl;
	}
	else
	{
		hnProps.use_chunked_transfer = false;
		cout << "in useChunkTransfer false"<<endl;
	}

	/*Positive Test Case*/
	if(type == 0)
	{	

	        hnProps.socketId = socketId;
		cout<<"SocketId:"<<hnProps.socketId<<endl;
		std::string streaming_interface;	
		
		streaming_interface=fetchStreamingInterface();
		found=streaming_interface.find("FAILURE");
 		if (found!=std::string::npos)
		{
			std::string delimiter = "<FAILURE>";
			size_t pos = 0;
			std::string token;
			while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
    				token = streaming_interface.substr(0, pos);
    				std::cout << token << std::endl;
    				streaming_interface.erase(0, pos + delimiter.length());
			}
			response["result"] = "FAILURE";
        		response["details"] = token;
			return TEST_FAILURE; 
		}
		else
		{
			 
			const char * streaming_interface_name = streaming_interface.c_str();
			/* Set remoteIp as eth1 interface Ip*/
			streamingIp = GetHostIP(streaming_interface_name);
	        	hnProps.remote_ip = convertIPStrToLong(streamingIp.c_str());
	        	DEBUG_PRINT(DEBUG_TRACE, "HNSink setHNSinkProperties() remoteIp: %ld\n",hnProps.remote_ip);

			string hnUrl = "http://" + streamingIp + "/vldms/tuner?ocap_locator=" + urlIn;
			DEBUG_PRINT(DEBUG_TRACE, "HNSink setHNSinkProperties() url: %s\n",hnUrl.c_str());
			strncpy(hnProps.url,hnUrl.c_str(), sizeof(hnProps.url));
			hnProps.url[sizeof(hnProps.url)-1] = 0;

			/* Using setSourceType to set source type */
			strncpy(hnProps.source_type,"QAM_SRC",sizeof(hnProps.source_type));
	        	hnSink->setHNSinkProperties( hnProps );
		}
	}
	else
	{
	        hnProps.socketId = socketId;

	        hnProps.remote_ip = convertIPStrToLong(streamIp.c_str());
	        DEBUG_PRINT(DEBUG_TRACE, "HNSink setHNSinkProperties() remoteIp: %ld\n",hnProps.remote_ip);

		string hnUrl = "http://" + streamIp + "/vldms/tuner?ocap_locator=" + urlIn;
		DEBUG_PRINT(DEBUG_TRACE, "HNSink setHNSinkProperties() url: %s\n",hnUrl.c_str());
		strncpy(hnProps.url,hnUrl.c_str(), sizeof(hnProps.url));
		hnProps.url[sizeof(hnProps.url)-1] = 0;
		
		/* Using setSourceType to set source type */
		strncpy(hnProps.source_type,"QAM_SRC",sizeof(hnProps.source_type));
	        hnSink->setHNSinkProperties( hnProps );
	}
	
        DEBUG_PRINT(DEBUG_TRACE, "HNSink setHNSinkProperties() success\n");
        response["result"] = "SUCCESS";
        response["details"] = "HNSink setHNSinkProperties() success";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_SetProperties -->Exit\n");
	return TEST_SUCCESS;
}


bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetSourceType(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_SetSourceType -->Entry\n");

	const char *rmfSrc = req["rmfElement"].asCString();
	char rmfSource[16];

	strcpy(rmfSource,rmfSrc);

	/* Source suppose to be in QAM_SRC,HN_SRC,DVR_SRC */	
        DEBUG_PRINT(DEBUG_TRACE, "RMF Src : %s\n",rmfSource);

	hnSink->setSourceType(rmfSource);

        DEBUG_PRINT(DEBUG_TRACE, "HNSink setSourceType() success\n");
        response["result"] = "SUCCESS";
        response["details"] = "HNSink setSourceType() success";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_SetSourceType -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_InitPlatform(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_InitPlatform -->Entry\n");
	RMFResult retResult = RMF_RESULT_SUCCESS;	
	
	retResult = HNSink::init_platform();	
	if (RMF_RESULT_SUCCESS != retResult)
	{
        	DEBUG_PRINT(DEBUG_ERROR, "HNSink init_platform() failed\n");
        	response["result"] = "FAILURE";
               	response["details"] = "HNSink init_platform() failed";

                return TEST_FAILURE;
	}

        DEBUG_PRINT(DEBUG_TRACE, "HNSink init_platform() success\n");

        response["result"] = "SUCCESS";
        response["details"] = "HNSink init_platform() success";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_InitPlatform -->Exit\n");

	return TEST_SUCCESS; 
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_UninitPlatform -->Entry\n");
	RMFResult retResult = RMF_RESULT_SUCCESS;	
	
	retResult = HNSink::uninit_platform();	
	if (RMF_RESULT_SUCCESS != retResult)
	{

        	DEBUG_PRINT(DEBUG_ERROR, "HNSink uninit_platform() failed\n");
        	response["result"] = "FAILURE";
               	response["details"] = "HNSink uninit_platform() failed";

                return TEST_FAILURE;
	}


        DEBUG_PRINT(DEBUG_TRACE, "HNSink uninit_platform() success\n");

        response["result"] = "SUCCESS";
        response["details"] = "HNSink uninit_platform() success";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_HNSink_UninitPlatform -->Exit\n");

	return TEST_SUCCESS; 
}

#endif

#endif

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List

Arguments     : Input argument is None. Output argument is "SUCCESS" or "FAILURE". 

Description   : Receives the request from Test Manager to get total number of recording avaliable.
Gets the response from dvr manager and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List(IN const Json::Value& req, OUT Json::Value& response)
{
	DVRManager *dvm= DVRManager::getInstance();
	long long recDuration = 0;
	ofstream recordDetails;
	int count = 0;		
	long long segmentName;
	
	/* Get Total recording List */
	count = dvm->getRecordingCount();
	
	char *absPath;
	char finalPath[64];
	
	/* Fetch the TDK path from environment variable "TDK_PATH" */
	absPath = getenv("TDK_PATH");
	
	if(absPath == NULL)
	{
		response["log-path"]= "NULL";	
		response["result"] = "FAILURE";
		response["details"] = "Enable to find: /opt/TDK/ path to create recordDetails.txt file";
		DEBUG_PRINT(DEBUG_ERROR, "Enable to find: /opt/TDK/ path to create recordDetails.txt file");

		return TEST_FAILURE;
	}
	
	strcpy(finalPath,absPath);
	strcat(finalPath,"/");
	strcat(finalPath,RECORD_DETAILS_TXT);	

        DEBUG_PRINT(DEBUG_TRACE, "Absolute Path: %s\n",absPath);
        DEBUG_PRINT(DEBUG_TRACE, "Absolute FinalPath: %s\n",finalPath);
	
	/*Open a file*/
	recordDetails.open(finalPath, ios::out | ios::trunc);
	if (recordDetails.is_open())
	{
        	DEBUG_PRINT(DEBUG_TRACE, "Number of recordings: %d\n",count);
		recordDetails << "Total Recording: " << count << endl;

		for( int ii= 0; ii < count; ++ii )
		{
		      RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex( ii );

	              DEBUG_PRINT(DEBUG_TRACE, "Record: %d id: %s \n",ii,pRecInfo->recordingId.c_str());
		      recordDetails << "Record: " << ii << " id: " << pRecInfo->recordingId.c_str();
		
		      if (NULL == pRecInfo->title)
		      {
        	      		DEBUG_PRINT(DEBUG_TRACE, "title: (NULL)\n");
				recordDetails << " title: (NULL)";
		      }
		      else
		      {
              			DEBUG_PRINT(DEBUG_TRACE, "title: %s\n", pRecInfo->title);
				recordDetails << " title: " << pRecInfo->title;
	      	      }
	
		      recDuration = dvm->getRecordingDuration(pRecInfo->recordingId.c_str());
	              DEBUG_PRINT(DEBUG_TRACE, " Duration: %lld\n", recDuration);
		      recordDetails << " Duration: " << recDuration;

                      for (int i = 0;i < pRecInfo->segmentCount && i != 1; i++)
		      {
	                        RecordingSegmentInfo *pSegInfo= pRecInfo->segments[i];
				segmentName = pSegInfo->segmentName;
	                        DEBUG_PRINT(DEBUG_TRACE, "SegmentName: %lld\n", segmentName);
				recordDetails << " SegmentName: " << segmentName << endl;
		      }

	              DEBUG_PRINT(DEBUG_TRACE, " Seg Count: %d\n", pRecInfo->segmentCount);
		      if (0 == pRecInfo->segmentCount)
		      {
				recordDetails << " SegmentName: 0" << endl;
		      }
		}
		recordDetails.close();
        	DEBUG_PRINT(DEBUG_TRACE, "Writing into a file succeess\n");
	}
	else
	{
		response["log-path"]= "NULL";	
		response["result"] = "FAILURE";
		response["details"] = "File Creation Failed";
		DEBUG_PRINT(DEBUG_ERROR, "File Creation Failed");
		return TEST_FAILURE;
	}

        DEBUG_PRINT(DEBUG_TRACE, "logpath: Absolute Path: %s\n",finalPath);

	response["log-path"]= finalPath;	
	response["result"] = "SUCCESS";
	response["details"] = "Recording List File Created Successfully";
	DEBUG_PRINT(DEBUG_TRACE, "Success");

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVR_Rec_List -->Exit\n");
	return TEST_SUCCESS;
}


bool MediaframeworkAgent::MediaframeworkAgent_DVR_CreateNewRecording(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVR_CreateNewRecording -->Entry\n");	

	#if 1
	string completeCmd = "/opt/TDK/tdkRmfApp ";
	string recordCmd = "record";
	string recordId = req["recordId"].asCString();
	string duration = req["recordDuration"].asCString();
	string title = req["recordTitle"].asCString();
	string ocap = "ocap://";
	string ocapId = req["ocapId"].asCString();
	ocap.append(ocapId);
	
	/*Framing the command to record using tdkRmfApp*/
	completeCmd.append(recordCmd);
	completeCmd.append(" ");
	completeCmd.append(recordId);
	completeCmd.append(" ");
	completeCmd.append(duration);
	completeCmd.append(" ");
	completeCmd.append(title);
	completeCmd.append(" ");
	completeCmd.append(ocap);
	
	#endif
	
        DEBUG_PRINT(DEBUG_TRACE, "The Complete Command: %s \n",completeCmd.c_str());

	if(-1 == (system(completeCmd.c_str())))
	{
                DEBUG_PRINT(DEBUG_ERROR, "Error: tdkRmfApp failed to record.\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: tdkRmfApp failed to record.";
                return TEST_FAILURE;
	}


        DEBUG_PRINT(DEBUG_TRACE, "tdkRmfApp recorded successfully.\n");
        response["result"] = "SUCCESS";
        response["details"] = "tdkRmfApp recorded successfully. \n";

	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVR_CreateNewRecording -->Exit\n");	
        return TEST_SUCCESS;
}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute.

Arguments     : Input argument is none. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Set and Get Mute state. 
Gets the response from MPSink element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetMute --->Entry\n");
#ifdef ENABLE_DVRSRC_MPSINK

	int res_MPSinkterm, res_MPSinkinit;
	bool res_GetMute, res_afterSetMute;

	MediaPlayerSink* pSink = new MediaPlayerSink();

	res_MPSinkinit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Initialize is %d\n",res_MPSinkinit);

	if(0 == res_MPSinkinit)
	{
		res_GetMute = pSink->getMuted();
		if(0 == res_GetMute)
		{
			res_GetMute = 1;
		}
		else
		{
			res_GetMute = 0;
		}
		pSink->setMuted(res_GetMute);
		res_afterSetMute = pSink->getMuted();
		res_MPSinkterm = pSink->term();
		DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n",res_MPSinkterm);

		if(res_afterSetMute == res_GetMute)
		{
			if(0 == res_MPSinkterm)
			{
				DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink_SetGetMute is Success\n" );	
				response["result"] = "SUCCESS";
				return TEST_SUCCESS;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "SetgetMute is success but failed to terminate MPSink";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
				return TEST_FAILURE;
			}
		}
		else
		{
			response["details"] = "SetgetMute is failed";
			response["result"] = "FAILURE";
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
			return TEST_FAILURE;
		}	
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Initialization of MPSink is failed";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
		return TEST_FAILURE;
	}
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif
}
/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume

Arguments     : Input argument is Volume.  Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Set and Get Volume.
Gets the response from MPSink element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetVolume --->Entry\n");
#ifdef ENABLE_DVRSRC_MPSINK

	int res_MPSinkterm, res_MPSinkinit;
	float res_GetVolume;
	float volume = req["Volume"].asFloat();

	MediaPlayerSink* pSink = new MediaPlayerSink();

	res_MPSinkinit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Initialize is %d\n", res_MPSinkinit);

	if(0 == res_MPSinkinit)
	{
		res_GetVolume = pSink->getVolume();
		if(volume == res_GetVolume)
		{
			res_MPSinkterm = pSink->term();
			DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n", res_MPSinkterm);
			if(0 == res_MPSinkterm)
			{
				response["result"] = "FAILURE";
				response["details"] = "Get value and entered values are same, Please enter a different value";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "Get value and entered values are same and failed to do terminate MPSink";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}
		}
		else
		{
			pSink->setVolume(volume);
			res_GetVolume = pSink->getVolume();
			DEBUG_PRINT(DEBUG_LOG, "Result of GetVolume after setting is %f\n", res_GetVolume);

			res_MPSinkterm = pSink->term();
			DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n", res_MPSinkterm);

			if(res_GetVolume == volume)
			{
				if(0 == res_MPSinkterm)
				{
					response["result"] = "SUCCESS";
					DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
					return TEST_SUCCESS;
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "SetgetVoulme is Success but failed to terminate MPSink";
					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
					return TEST_FAILURE;
				}
			}
			else
			{
				response["details"] = "SetgetVoulme is Failed";
				response["result"] = "FAILURE";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}	
		}
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
		return TEST_FAILURE;
	}
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Get Buffer range supported by HNSource.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrc_Getbufferrange --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

        int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay;
        int res_HNSrcGetState, res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
        unsigned x, y, height, width;
        bool applyNow;
        int applynow;
        string streamingip;
        MediaPlayerSink* pSink = new MediaPlayerSink();
        HNSource* pSource = new HNSource();
        RMFState cur_state;
        std::size_t found;

        x = req["X"].asInt();
        y = req["Y"].asInt();
        height = req["H"].asInt();
        width = req["W"].asInt();
        applynow = req["apply"].asInt();

        if(0 == applynow)
        {
                applyNow = false;
        }
        else if(1 == applynow)
        {
                applyNow = true;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
        }

        res_HNSrcInit = pSource->init();
        DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

        if(0 != res_HNSrcInit)
        {
                response["result"] = "FAILURE";
                response["details"] = "Failed to Initialize hnsource";
                return TEST_FAILURE;
        }
		string streaming_interface;
        	size_t pos = 0;
	        streaming_interface=fetchStreamingInterface();
                found=streaming_interface.find("FAILURE");
                if (found!=std::string::npos)
                {
                        std::string delimiter = "<FAILURE>";
                        std::string token;
                        while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
                                token = streaming_interface.substr(0, pos);
                                std::cout << token << std::endl;
                                streaming_interface.erase(0, pos + delimiter.length());
                        }
                        response["result"] = "FAILURE";
                        response["details"] = token;
                        return TEST_FAILURE;
                }

	const char * streaming_interface_name = streaming_interface.c_str();
        streamingip=GetHostIP(streaming_interface_name);
        string urlIn = req["playuri"].asCString();
        string http = "http://";
        http.append(streamingip);
        cout<<"IP:"<<streamingip;


        pos = urlIn.find(":8080");
        if (pos!=std::string::npos)
        {
                urlIn = urlIn.replace(0,pos,http);
        }

        cout<<"Final URL passed to Open(): "<<urlIn<<endl;

        res_HNSrcOpen = pSource->open(urlIn.c_str(), 0);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

        if(0 != res_HNSrcOpen)
        {
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to open hnsource";
                return TEST_FAILURE;
        }

        res_MPSinkInit = pSink->init();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

        if(0 != res_MPSinkInit)
        {
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to Initialize MPSink";
                return TEST_FAILURE;
        }

        res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

        if(0 != res_MPSinksetrect)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to set video resolution";
                return TEST_FAILURE;
        }

        res_MPSinksetsrc = pSink->setSource(pSource);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);

        if(0 != res_MPSinksetsrc)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to set source";
                return TEST_FAILURE;
        }

        res_HNSrcPlay = pSource->play();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

        if(0 != res_HNSrcPlay)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to play hnsource";
                return TEST_FAILURE;
        }

        sleep(10);

        res_HNSrcGetState = pSource->getState(&cur_state, NULL);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of GstState is %d\n", res_HNSrcGetState);

        if(1 != res_HNSrcGetState)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to Get Video State";
                return TEST_FAILURE;
        }

        if (cur_state != RMF_STATE_PLAYING)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                DEBUG_PRINT(DEBUG_ERROR, "Get State API is returning Success, but current state is not RMF_STATE_PLAYING");
                response["result"] = "FAILURE";
                response["details"] = "Get State API is returning Success, but current state is not RMF_STATE_PLAYING";
                return TEST_FAILURE;
        }

        DEBUG_PRINT(DEBUG_LOG, "Get Video state is success. Video is playing and showing state as RMF_STATE_PLAYING\n");
        int res_HNSrcGetbuffrange;
        range_list_t ranges;
        res_HNSrcGetbuffrange = pSource->getBufferedRanges(ranges);
        if(1 != res_HNSrcGetbuffrange)
        {
                pSink->term();
                pSource->close();
                pSource->term();
                response["result"] = "FAILURE";
                response["details"] = "Failed to Get Video State";
                return TEST_FAILURE;
         }
        DEBUG_PRINT(DEBUG_LOG, "Result of Get buffered ranges is %d\n", res_HNSrcGetbuffrange);
/*
        int retValue;
        double mediaTime;
        retValue=pSource->setMediaTime(0);
        cout<<"Return of Set Media time "<<retValue<<endl;
        sleep(5);
        retValue = pSource->getMediaTime(mediaTime);
        cout<<"Return of get Media time "<<retValue<<endl;
        cout<<"get Media time value"<<mediaTime<<endl;
*/

        res_MPSinkTerm = pSink->term();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

        res_HNSrcClose = pSource->close();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

        res_HNSrcTerm = pSource->term();
        DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

        if(0 != res_MPSinkTerm)
        {
                response["result"] = "FAILURE";
                response["details"] = "Get Video state is success, but failed to Terminate MPSink";
                return TEST_FAILURE;
        }

        if(0 != res_HNSrcClose)
        {
                response["result"] = "FAILURE";
                response["details"] = "Get Video state is success, but failed to close hnsource";
                return TEST_FAILURE;
        }

        if(0 != res_HNSrcTerm)
        {
                response["result"] = "FAILURE";
                response["details"] = "Get Video state is success, but failed to Terminate hnsource";
                return TEST_FAILURE;
        }
        response["result"] = "SUCCESS";
        response["details"] = "Bufferranges is success";
        return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the state of video.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_State --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay;
	int res_HNSrcGetState, res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;
	string streamingip;
	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;

	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}
	string streaming_interface;
        size_t pos = 0;
	size_t found;
        streaming_interface=fetchStreamingInterface();
        found=streaming_interface.find("FAILURE");
        if (found!=std::string::npos)
        {
        	std::string delimiter = "<FAILURE>";
                std::string token;
                while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
                	token = streaming_interface.substr(0, pos);
                        std::cout << token << std::endl;
                        streaming_interface.erase(0, pos + delimiter.length());
                 }
                 response["result"] = "FAILURE";
                 response["details"] = token;
                 return TEST_FAILURE;
         }

	const char * streaming_interface_name = streaming_interface.c_str();
	streamingip=GetHostIP(streaming_interface_name);
	string urlIn = req["playuri"].asCString();
	string http = "http://";
	http.append(streamingip);
	cout<<"IP:"<<streamingip;
	
	
	pos = urlIn.find(":8080");
        if (pos!=std::string::npos)
        {
                urlIn = urlIn.replace(0,pos,http);
        }

        cout<<"Final URL passed to Open(): "<<urlIn<<endl;
		
	res_HNSrcOpen = pSource->open(urlIn.c_str(), 0);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetsrc = pSink->setSource(pSource);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);

	if(0 != res_MPSinksetsrc)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}	

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{	
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(20);

	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of GstState is %d\n", res_HNSrcGetState);

	if(1 != res_HNSrcGetState)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Get Video State";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		DEBUG_PRINT(DEBUG_ERROR, "Get State API is returning Success, but current state is not RMF_STATE_PLAYING");
		response["result"] = "FAILURE";
		response["details"] = "Get State API is returning Success, but current state is not RMF_STATE_PLAYING";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Get Video state is success. Video is playing and showing state as RMF_STATE_PLAYING\n");
/*	
int retValue;
        double mediaTime;
        retValue=pSource->setMediaTime(0);
        cout<<"Return of Set Media time "<<retValue<<endl;
        sleep(5);
        retValue = pSource->getMediaTime(mediaTime);
        cout<<"Return of get Media time "<<retValue<<endl;
        cout<<"get Media time value"<<mediaTime<<endl;
*/

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to verify Mute and Unmute functionality.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay, res_HNSrcGetState; 
	int res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;
	bool res_MPSinkGetMute, res_afterSetMute;

	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;
        //RMFResult retResult = RMF_RESULT_SUCCESS;
	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}	

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}
	string streamingip;
	string streaming_interface;
        size_t pos = 0;
	size_t found;
        streaming_interface=fetchStreamingInterface();
        found=streaming_interface.find("FAILURE");
        if (found!=std::string::npos)
        {
        	std::string delimiter = "<FAILURE>";
                std::string token;
                while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
                	token = streaming_interface.substr(0, pos);
                        std::cout << token << std::endl;
                        streaming_interface.erase(0, pos + delimiter.length());
                 }
                 response["result"] = "FAILURE";
                 response["details"] = token;
                 return TEST_FAILURE;
	}

	const char * streaming_interface_name = streaming_interface.c_str();
 	streamingip=GetHostIP(streaming_interface_name);
        string urlIn = req["playuri"].asCString();
        string http = "http://";
        http.append(streamingip);
        cout<<"IP:"<<streamingip;


        pos = urlIn.find(":8080");
        if (pos!=std::string::npos)
        {
                urlIn = urlIn.replace(0,pos,http);
        }

        cout<<"Final URL passed to Open(): "<<urlIn<<endl;

        res_HNSrcOpen = pSource->open(urlIn.c_str(), 0);	
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetsrc = pSink->setSource(pSource);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);

	if(0 != res_MPSinksetsrc)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(10);
	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Play API call is Success, but Video is not playing";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}						

	DEBUG_PRINT(DEBUG_LOG, "Video is playing\n");

	res_MPSinkGetMute = pSink->getMuted();
	if(0 == res_MPSinkGetMute)
	{
		res_MPSinkGetMute = 1;
	}
	else
	{
		res_MPSinkGetMute = 0;
	}

	pSink->setMuted(res_MPSinkGetMute);
	res_afterSetMute = pSink->getMuted();

	if(res_afterSetMute != res_MPSinkGetMute)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to do Mute and Unmute";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Mute Unmute is success\n");

/*
	int retValue;
        double mediaTime;
        retValue=pSource->setMediaTime(0);
        cout<<"Return of Set Media time "<<retValue<<endl;
        sleep(5);
        retValue = pSource->getMediaTime(mediaTime);
        cout<<"Return of get Media time "<<retValue<<endl;
        cout<<"Media time value "<<mediaTime<<endl;
*/

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif
}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Get the volume of Video.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_Volume --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay, res_HNSrcGetState; 
	int res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	float volume, res_GetVolume;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;

	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;

	volume = req["Volume"].asFloat();
	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	string streamingip;
	string streaming_interface;
        size_t pos = 0;
	size_t found;
        streaming_interface=fetchStreamingInterface();
        found=streaming_interface.find("FAILURE");
        if (found!=std::string::npos)
        {
        	std::string delimiter = "<FAILURE>";
                std::string token;
                while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
                	token = streaming_interface.substr(0, pos);
                        std::cout << token << std::endl;
                        streaming_interface.erase(0, pos + delimiter.length());
                 }
                 response["result"] = "FAILURE";
                 response["details"] = token;
                 return TEST_FAILURE;
	}

	const char * streaming_interface_name = streaming_interface.c_str();
	streamingip=GetHostIP(streaming_interface_name);
        string urlIn = req["playuri"].asCString();
        string http = "http://";
        http.append(streamingip);
        cout<<"IP:"<<streamingip;


        pos = urlIn.find(":8080");
        if (pos!=std::string::npos)
        {
                urlIn = urlIn.replace(0,pos,http);
        }

        cout<<"Final URL passed to Open(): "<<urlIn<<endl;

        res_HNSrcOpen = pSource->open(urlIn.c_str(), 0);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetsrc = pSink->setSource(pSource);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);

	if(0 != res_MPSinksetsrc)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(10);

	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		DEBUG_PRINT(DEBUG_ERROR, "Play API call is Success, but Video is not playing");
		response["result"] = "FAILURE";
		response["details"] = "Play API call is Success, but Video is not playing";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}							

	DEBUG_PRINT(DEBUG_LOG, "Video is playing\n");

	res_GetVolume = pSink->getVolume();
	if(res_GetVolume == volume)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Volime entered is same as the existing Volume, Please enter a different value";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;

	}

	pSink->setVolume(volume);
	res_GetVolume = pSink->getVolume();
	DEBUG_PRINT(DEBUG_LOG, "Result of GetVolume after setting is %f\n", res_GetVolume);

	if(res_GetVolume != volume)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to do set get volume";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Set Get Volume is Success\n");

/*	
	int retValue;
        double mediaTime;
        retValue=pSource->setMediaTime(0);        
        cout<<"Return of Set Media time "<<retValue<<endl;
        sleep(5);
        retValue = pSource->getMediaTime(mediaTime);
        cout<<"Return of get Media time "<<retValue<<endl;
        cout<<"Media time Value"<<mediaTime<<endl;
*/

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}	

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_InitTerm

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Initialize and Termination of the QAMSource Element.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_OpenClose

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Open and Close the QAMSource Component
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
	
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Play

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Play the Live content
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Pause

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Pause the Live content
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetTsId

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get transferstream id from PAT the QAMSource Component
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetLtsId

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get LTSID corresponding to the QAMSource Instance
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Init_Uninit_Platform

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Initialize and Uninitialize platform dependent functionalities.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetUseFactoryMethods

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Check if factory methods are to be used by the client. By Calling Init_Platform to read rmfconfig.ini and set the useFactory class varible.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get unused low level element of qamsrc.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetQAMSourceInstance

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to gets a RMFQAMSrc instance from QAMSrc factory corresponding to ocaplocator
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_ChangeURI

Arguments     : Input argument is OCAPLOCATOR and new OCAPLOCATOR to change. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Update URI of existing qam instance with new one if possible.If not possible, gets a new instance and returns it.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm

Arguments     : Input argument is RecordingId and playUrl. Output argument is "SUCCESS" or "FAILURE". 

Description   : Receives the request from Test Manager to Initialize, get recording Id and Termination of the DVRSink Element.
Gets the response from DVRSink element and send it to the Test Manager.
 **************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->Entry\n");

	RMFResult res_DVRSinkterm = RMF_RESULT_FAILURE;
	RMFResult res_DVRSinkinit = RMF_RESULT_FAILURE;
	RMFResult res_DVR = RMF_RESULT_FAILURE;

	string recordingId = req["recordingId"].asString();
	DEBUG_PRINT(DEBUG_LOG, "RecordingId input: %s\n", recordingId.c_str());
	string playUrl = req["playUrl"].asString();
	DEBUG_PRINT(DEBUG_LOG, "Play URL input: %s\n", playUrl.c_str());

	IRMFMediaSource *src = 0;
	DVRSink *dvrSink = 0;

	if ( playUrl.compare( 0, 7, "http://" ) == 0 )
	{
		src = createHNSrc(playUrl);
		if ( !src )
		{
			response["result"] = "FAILURE";
			response["details"] = "Failed to create HNSrc for recording";
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Failed to create HNSrc. Exit\n");
			return TEST_FAILURE;
		}		
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Unsupported src locator type";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->Source creation success\n");

	// Create recording
	RecordingSpec spec;
	createTestRecordingSpec (recordingId, playUrl, spec);
	res_DVR = DVRManager::getInstance()->createRecording( spec );
	if (( DVRResult_ok != res_DVR) && (DVRResult_alreadyExists != res_DVR))
	{
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->createRecording failed\n");
		response["result"] = "FAILURE";
		response["details"] = "Failed to create recording";

		if ( src )
		{
			src->term();
			delete src;
			src = 0;
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
		}

		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->createRecording success\n");

	// Create DVRSink instance
	dvrSink = new DVRSink(recordingId);

	if (0 == dvrSink)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to create DVRSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->DVRSink creation success\n");

		res_DVRSinkinit = dvrSink->init();
		DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink Initialization: %d\n", (int)res_DVRSinkinit);

		if(RMF_RESULT_SUCCESS == res_DVRSinkinit)
		{
			char stringDetails[75] = {'\0'};
			dvrSink->setSource(src);

			string rec_id = dvrSink->getRecordingId();
			DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink GetRecordingId: %s\n", rec_id.c_str());

			res_DVRSinkterm = dvrSink->term();
			DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink Termination: %d\n", (int)res_DVRSinkterm);

			if(RMF_RESULT_SUCCESS == res_DVRSinkterm)
			{
				if(rec_id == recordingId)
				{
					sprintf(stringDetails,"RecordingId:%s", rec_id.c_str());
					response["details"] = stringDetails;
					response["result"] = "SUCCESS";

					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> GetRecordingId success\n");

					if ( src )
					{
						src->term();
						delete src;
						src = 0;
						DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
					}

					res_DVR = DVRManager::getInstance()->deleteRecording ( recordingId );
					DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", (int)res_DVR);
                                	if ( DVRResult_ok != res_DVR )
                                	{
                                        	response["result"] = "FAILURE";
                                        	response["details"] = "MediaframeworkAgent_DVRSink_InitTerm -> Failed to delete recording";

						src->term();
						delete src;
						src = 0;

                                        	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRSink_InitTerm --> Exit\n");
                                        	return TEST_FAILURE;
                                	}

					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_Init&term --->Exit\n");
					return TEST_SUCCESS;	
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "DVRSink term is success but failed to get recording Id";
					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> GetRecordingId failed\n");
				}
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "DVRSink Initialization is success but failed to do terminate";
			}
		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Initialization of DVRSink is failed";
		}
	}

	if ( src )
	{
		src->term();
		delete src;
		src = 0;
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
	}

	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_Init&term --->Exit\n");
	return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get TotalSpace and FreeSpace.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                long long totalSpace= dvm->getTotalSpace();
                long long freeSpace= dvm->getFreeSpace();
                char stringDetails[75] = {'\0'};

                DEBUG_PRINT(DEBUG_LOG, "Total Space: %lld bytes\n", totalSpace);
                DEBUG_PRINT(DEBUG_LOG, "Free Space: %lld bytes\n", freeSpace );

                if((0 == totalSpace) || (totalSpace < freeSpace))
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get total/free space";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Exit\n");
                        return TEST_FAILURE;
                }

                sprintf(stringDetails,"TotalSpace:%lld bytes,FreeSpace:%lld bytes", totalSpace, freeSpace);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;

                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get total/free space";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingCount.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[25] = {'\0'};
                int count= dvm->getRecordingCount();

                DEBUG_PRINT(DEBUG_LOG, "Number of recordings = %d\n", count);
                sprintf(stringDetails, "RecordingCount:%d", count);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get recording count";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount -->Exit\n");
        return TEST_FAILURE;

}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex

Arguments     : Input argument is 'index'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoByIndex.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex --->Entry\n");

        char stringDetails[75] = {'\0'};
        int index = req["index"].asInt();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                RecordingInfo *pRecInfo = dvm->getRecordingInfoByIndex( index );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Recording Index: %d not found \n", index);

			// Pre-condition: Create test recording
                        RecordingSpec spec;
                        int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();

                        char sRecId[25] = {'\0'};
                        int iRecId = rand() % 10000 + 2000;

                        sprintf(sRecId, "%d", iRecId);
			std::string randRecId(sRecId);
                        spec.setRecordingId(randRecId);

                        createTestRecordingSpec (randRecId, playUrl, spec);
			DEBUG_PRINT(DEBUG_TRACE, "Creating new recording:%s\n", randRecId.c_str());
                        dvrres= dvm->createRecording( spec );

                        if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to create recording for GetRecordingInfoByIndex";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                                return TEST_FAILURE;
                        }

			pRecInfo = dvm->getRecordingInfoByIndex( index );
			if ( !pRecInfo )
			{
				response["result"] = "FAILURE";
				response["details"] = "Failed to get RecordingInfoByIndex";
				DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
				return TEST_FAILURE;
			}

			DEBUG_PRINT(DEBUG_TRACE, "Index:%d, RecordingId:%s, Title:%s\n", index, pRecInfo->recordingId.c_str(), pRecInfo->title);
			sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( randRecId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetRecordingInfoByIndex";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }
		else
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Index:%d, RecordingId:%s, Title:%s\n", index, pRecInfo->recordingId.c_str(), pRecInfo->title);
                        sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );

                       	response["result"] = "SUCCESS";
                       	response["details"] = stringDetails;
                       	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                       	return TEST_SUCCESS;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex

Arguments     : Input argument is 'index'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoByIndex.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex --->Entry\n");

        char stringDetails[75] = {'\0'};
        int index = req["index"].asInt();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                int count = dvm->getRecordingCount();
                DEBUG_PRINT(DEBUG_TRACE, "RecordingCount: %d\n", count);

                for( int i= 0; i < count; ++i )
                {
                        RecordingInfo *pRecInfoTmp = dvm->getRecordingInfoByIndex( i );
                        DEBUG_PRINT( DEBUG_TRACE, "recording %d id %s title \"%s\"\n", i, pRecInfoTmp->recordingId.c_str(), pRecInfoTmp->title );
                }

                if (index >= count)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfo. Index not found";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex -->Exit\n");
                        return TEST_FAILURE;
                }

                RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex( index );
                if ( pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Index:%d, RecordingId:%s, Title:%s\n", index, pRecInfo->recordingId.c_str(), pRecInfo->title);
                        sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfo by Index";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get RecordingInfo by Index";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoById.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById --->Entry\n");

        char stringDetails[75] = {'\0'};
        string recordingId = req["recordingId"].asString();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId: %s not found \n", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId: %s\n", recordingId.c_str());
                        // Pre-condition: Create test recording
                        RecordingSpec spec;
			int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to create recording for GetRecordingInfoById";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                                return TEST_FAILURE;
                        }

			pRecInfo = dvm->getRecordingInfoById( recordingId );
			if ( !pRecInfo )
			{
				response["result"] = "FAILURE";
				response["details"] = "Failed to get RecordingInfoById";
				DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
				return TEST_FAILURE;
			}
			
			sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetRecordingInfoById";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, Title:%s\n", pRecInfo->recordingId.c_str(), pRecInfo->title );
                if (recordingId == pRecInfo->recordingId)
                {
			sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );

                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfoById";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoById

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoById.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoById(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoById --->Entry\n");

        char stringDetails[75] = {'\0'};
        string recordingId = req["recordingId"].asString();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, Title:%s\n", pRecInfo->recordingId.c_str(), pRecInfo->title );
                        if (recordingId == pRecInfo->recordingId)
                        {
                                sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoById -->Exit\n");
                                return TEST_SUCCESS;
                        }
                        else
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoById -->Exit\n");
                                return TEST_FAILURE;
                        }
                }
                else
                {
                        DEBUG_PRINT(DEBUG_ERROR, "No record found with requested Id\n");
                        response["result"] = "FAILURE";
                        response["details"] = "No record found with requested Id";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoById -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CheckRecordingInfoById -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the status RecordingInProgress.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[30] = {'\0'};
                string recordingId = req["recordingId"].asString();

                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s not found \n", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId:%s\n", recordingId.c_str());
                        // Pre-condition: Create test recording
                        RecordingSpec spec;
			int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "RecordingId not found. Failed to create test recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
                                return TEST_FAILURE;
                        }

			pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for GetIsRecordingInProgress";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
                                return TEST_FAILURE;
                        }

                	bool recStatus = dvm->isRecordingInProgress( recordingId );
                	DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, IsRecordingInProgress: %d\n", recordingId.c_str(), recStatus);

                	if (true == recStatus)
                	{
                        	sprintf(stringDetails, "%s", "Recording IS InProgress");
                	}
                	else
                	{
                        	sprintf(stringDetails, "%s", "Recording IS NOT InProgress");
                	}

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetIsRecordingInProgress";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                bool recStatus = dvm->isRecordingInProgress( recordingId );
                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, IsRecordingInProgress: %d\n", recordingId.c_str(), recStatus);

                if (true == recStatus)
                {
                        sprintf(stringDetails, "%s", "Recording IS InProgress");
                }
                else
                {
                        sprintf(stringDetails, "%s", "Recording IS NOT InProgress");
                }

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingSize.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();

                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s not found \n", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId:%s\n", recordingId.c_str());

                        // Pre-condition: Create test recording
                        RecordingSpec spec;
			int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "RecordingId not found. Failed to create test recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
                                return TEST_FAILURE;
                        }

			pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for GetRecordingSize";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
                                return TEST_FAILURE;
                        }

			long long recSize = dvm->getRecordingSize( recordingId );
                	DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingSize: %lld\n", recordingId.c_str(), recSize);
                	sprintf(stringDetails, "RecordingSize: %lld", recSize);

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetRecordingSize";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                long long recSize = dvm->getRecordingSize( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingSize: %lld\n", recordingId.c_str(), recSize);
                sprintf(stringDetails, "RecordingSize: %lld", recSize);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingDuration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();

                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s not found \n", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId:%s\n", recordingId.c_str());
                        // Pre-condition: Create test recording
                        RecordingSpec spec;
			int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "RecordingId not found. Failed to create test recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
                                return TEST_FAILURE;
                        }

                        pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for GetRecordingDuration";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
                                return TEST_FAILURE;
                        }

			long long recDuration = dvm->getRecordingDuration( recordingId );
                	DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingDuration: %lld\n", recordingId.c_str(), recDuration);
                	sprintf(stringDetails, "RecordingDuration: %lld", recDuration);

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetRecordingDuration";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                long long recDuration = dvm->getRecordingDuration( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingDuration: %lld\n", recordingId.c_str(), recDuration);
                sprintf(stringDetails, "RecordingDuration: %lld", recDuration);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
        return TEST_FAILURE;
}




/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingStartTime.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();

                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s not found \n", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId:%s\n", recordingId.c_str());
                        // Pre-condition: Create test recording
                        RecordingSpec spec;
			int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "RecordingId not found. Failed to create test recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                                return TEST_FAILURE;
                        }

                        pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for GetRecordingStartTime";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                                return TEST_FAILURE;
                        }

                	long long recStartTime = dvm->getRecordingStartTime( recordingId );
                	DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingStartTime: %lld\n", recordingId.c_str(), recStartTime);
                	sprintf(stringDetails, "RecordingStartTime: %lld", recStartTime);

                        // Post-condition: Delete test recording
                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for GetRecordingStartTime";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                long long recStartTime = dvm->getRecordingStartTime( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingStartTime: %lld\n", recordingId.c_str(), recStartTime);
                sprintf(stringDetails, "RecordingStartTime: %lld", recStartTime);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
        return TEST_FAILURE;
}



/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the default TSB Max duration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                int defTSBMaxDuration = dvm->getDefaultTSBMaxDuration( );

                DEBUG_PRINT(DEBUG_LOG, "DefaultTSBMaxDuration is %d\n", defTSBMaxDuration);
                sprintf(stringDetails, "DefaultTSBMaxDuration: %d", defTSBMaxDuration);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DefaultTSBMaxDuration";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB

Arguments     : Input argument is 'duration'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to create TSB with given duration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string tsbId;
                long long duration = 0;
                duration = req["duration"].asDouble();

                int dvrres= dvm->createTSB( duration, tsbId );

                DEBUG_PRINT(DEBUG_TRACE, "Result of createTSB: %d\n", dvrres);

                if ( dvrres == DVRResult_ok )
                {
                        response["result"] = "SUCCESS";
                        sprintf(stringDetails, "TSBId: %s", tsbId.c_str());
                        response["details"] = stringDetails;

			//Post-Condition: Reset tsb
			tsbId.clear();
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Get on DVR manager instance success but failed to create TSB";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording

Arguments     : Input arguments are 'tsbId' and 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to convert TSB to Recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                int dvrres = DVRResult_ok;
                string tsbId = req["tsbId"].asString();
                string recordingId = req["recordingId"].asString();

		// Check whether tsbId is present
   		RecordingInfo *pTSBRecInfo = dvm->getRecordingInfoById( tsbId );
   		if ( !pTSBRecInfo )
   		{
			// Create TSB with default duration
			dvrres= dvm->createTSB( -1LL, tsbId );
			DEBUG_PRINT(DEBUG_ERROR, "Result of createTSB: %d\n", dvrres);
			if ( DVRResult_ok != dvrres )
			{
                        	response["result"] = "FAILURE";
                        	response["details"] = "Failed to create TSB";
                        	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        	return TEST_FAILURE;
                	}
			DEBUG_PRINT(DEBUG_ERROR, "Created TSBId: %s for ConvertTSBToRecording \n", tsbId.c_str());

			pTSBRecInfo = dvm->getRecordingInfoById( tsbId );
                        if ( !pTSBRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get recording info by tsbId for ConvertTSBToRecording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                                return TEST_FAILURE;
                        }
   		}

                if ( pTSBRecInfo->isShadowedById( recordingId ) )
                {
                	response["result"] = "SUCCESS";
                        response["details"] = "TSB conversion of tsbId to recordingId has already happened: Ignoring request";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_SUCCESS;
                }

		// Check whether recordingId is present
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( !pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId: %s\n", recordingId.c_str());
                        // Pre-condition: Create test recording
                        RecordingSpec spec;
                        string playUrl = req["playUrl"].asString();
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "RecordingId not found. Failed to create test recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                                return TEST_FAILURE;
                        }

                        pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for ConvertTSBToRecording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                                return TEST_FAILURE;
                        }

                        if ( (pTSBRecInfo->isShadowedById(recordingId)) && (pRecInfo->shadowingId.size() != 0) )
			{
				response["result"] = "SUCCESS";
				response["details"] = "TSB conversion of tsbId to recordingId has already happened: Ignoring request";

                        	int res_DVR = dvm->deleteRecording ( recordingId );
                        	DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);

				DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
				return TEST_SUCCESS;
			}

			dvrres= dvm->convertTSBToRecording( tsbId, recordingId );
			DEBUG_PRINT(DEBUG_TRACE, "Result of convertTSBToRecording: %d\n", dvrres);
                	if ( (dvrres != DVRResult_ok) && (dvrres != DVRResult_cciExclusions) )
                	{
                        	response["result"] = "FAILURE";
                        	response["details"] = "Failed to convert TSB to Recording";
                        	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        	return TEST_FAILURE;
                	}

                        // Post-condition: Delete test recording and clear tsb
			tsbId.clear();
                        pRecInfo->shadowingId.clear();

                        int res_DVR = dvm->deleteRecording ( recordingId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to delete recording for ConvertTSBToRecording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording --> Exit\n");
                                return TEST_FAILURE;
                        }
                        else
                        {
                                response["result"] = "SUCCESS";
                                response["details"] = "Converted TSB to Recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                                return TEST_SUCCESS;
                        }
                }

                if ( (pTSBRecInfo->isShadowedById(recordingId)) && (pRecInfo->shadowingId.size() != 0) )
                {
                	response["result"] = "SUCCESS";
                        response["details"] = "TSB conversion of tsbId to recordingId has already happened: Ignoring request";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_SUCCESS;
                }

                dvrres= dvm->convertTSBToRecording( tsbId, recordingId );
                DEBUG_PRINT(DEBUG_TRACE, "Result of convertTSBToRecording: %d\n", dvrres);
                if ( (dvrres != DVRResult_ok) && (dvrres != DVRResult_cciExclusions) )
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to convert TSB to Recording";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_FAILURE;
                }
                else
                {
                        response["result"] = "SUCCESS";
			response["details"] = "Converted TSB to Recording";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording

Arguments     : Input arguments are 'recordingId', 'recordingTitle', 'recordDuration' and 'qamLocator'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to create a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char work[256] = {'\0'};
                int dvrres;
                RecordingSpec spec;
                long long recordDuration = 0;
                string recordingTitle, recordingId, qamLocator;
		char stringDetails[256] = {'\0'};

                recordingTitle = req["recordingTitle"].asString();
                recordingId = req["recordingId"].asString();
                recordDuration= req["recordDuration"].asDouble();
                qamLocator=req["qamLocator"].asString();

                recordDuration *= 1000;
                sprintf( work, "{\"title\":\"%s %s\"}", recordingId.c_str(), recordingTitle.c_str());
                DEBUG_PRINT(DEBUG_TRACE, "Recording title to be set : %s\n", work);

                // Create recording
                createTestRecordingSpec (recordingId, qamLocator, spec);
                spec.setDuration(recordDuration);
                spec.setProperties( work );

                dvrres= dvm->createRecording( spec );
                DEBUG_PRINT(DEBUG_TRACE, "Result of createRecording: %d\n", dvrres);

                if ( DVRResult_ok == dvrres )
                {
			sprintf(stringDetails, "Created recording id: %s", recordingId.c_str());
                        response["result"] = "SUCCESS";
			response["details"] = stringDetails;

                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
                }
		else if (DVRResult_alreadyExists == dvrres)
		{
			DEBUG_PRINT(DEBUG_TRACE, "Recording Id %s already exists.\n", recordingId.c_str());

			char sRecId[25] = {'\0'};
			int iRecId = rand() % 10000 + 2000;

			sprintf(sRecId, "%d", iRecId);
			recordingId = std::string(sRecId);
			spec.setRecordingId(recordingId);

			DEBUG_PRINT(DEBUG_TRACE, "Creating new Recording Id %s \n", recordingId.c_str());
			dvrres= dvm->createRecording( spec );
			DEBUG_PRINT(DEBUG_TRACE, "Result of createRecording: %d\n", dvrres);
			
			if ( DVRResult_ok != dvrres )
                	{
                        	response["result"] = "FAILURE";
                        	response["details"] = "Retry to create recording failed";
                        	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
                        	return TEST_FAILURE;
                	}

                        sprintf(stringDetails, "Created recording id: %s", recordingId.c_str());
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;

			DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
		}
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Get on DVR manager instance success but failed to create record";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
                        return TEST_FAILURE;
                }

                // Post-condition: Delete test recording
                int res_DVR = dvm->deleteRecording ( recordingId );
                DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording %s\n", res_DVR, recordingId.c_str());
                if ( DVRResult_ok != res_DVR )
                {
                       response["result"] = "FAILURE";
                       response["details"] = "Failed to delete recording after create recording";
                       DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording --> Exit\n");
                       return TEST_FAILURE;
                }
                else
                {
                       DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                       return TEST_SUCCESS;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording

Arguments     : Input argument is 'recordingId'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to update the title of a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char work[256] = {'\0'};
                char stringDetails[256] = {'\0'};
                int dvrres;
		RecordingSpec spec;
		bool newRec = false;

                string recordingId = req["recordingId"].asString();
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );

   		if ( !pRecInfo )
   		{
			DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s not found \n", recordingId.c_str());

			newRec = true;

			// Pre-condition: Create test recording
			string playUrl = req["playUrl"].asString();
        		createTestRecordingSpec (recordingId, playUrl, spec);

			DEBUG_PRINT(DEBUG_TRACE, "Creating RecordingId:%s\n", recordingId.c_str());
			dvrres= dvm->createRecording( spec );

			if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                	{
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to create recording for update recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                                return TEST_FAILURE;
                	}

                        pRecInfo= dvm->getRecordingInfoById( recordingId );
                        if ( !pRecInfo )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById for update recording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                                return TEST_FAILURE;
                        }
   		}

                DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, RecordingTitle:%s", pRecInfo->recordingId.c_str(), pRecInfo->title);

                // Create recording spec from existing record info
                spec.setRecordingId(pRecInfo->recordingId);
                spec.setStartTime(pRecInfo->requestedStartTime);
                spec.setDuration(pRecInfo->requestedDuration);
                spec.setEntitlementId(pRecInfo->entitlementId);
                spec.setIsPPV(pRecInfo->isPPV);
                spec.setBitRate(pRecInfo->bitRate);

                // Update the recording title
                sprintf( work, "{\"title\":\"%s Updated test record\"}", recordingId.c_str());
                DEBUG_PRINT(DEBUG_TRACE, "Updated title to be set : %s\n", work);

                spec.setProperties( work );

                dvrres= dvm->updateRecording( spec );
                DEBUG_PRINT(DEBUG_TRACE, "Result of updateRecording: %d\n", dvrres);
                if ( dvrres == DVRResult_ok )
                {
                	DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, RecordingTitle:%s", pRecInfo->recordingId.c_str(), pRecInfo->title);
                        sprintf(stringDetails, "UpdatedTitle: %s", pRecInfo->title);

                        // Post-condition: Delete test recording
			if (true == newRec)
			{
	                	int res_DVR = dvm->deleteRecording ( recordingId );
                        	DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        	if ( DVRResult_ok != res_DVR )
                        	{
                                	response["result"] = "FAILURE";
                                	response["details"] = "Failed to delete recording for UpdateRecording";
                                	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording --> Exit\n");
                                	return TEST_FAILURE;
                        	}
			}

                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
			sprintf(stringDetails, "Failed to update record. Error code: %d", dvrres);
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording

Arguments     : Input argument is 'recordingId'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to delete a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                string recordingId = req["recordingId"].asString();
                int result= dvm->deleteRecording ( recordingId );
                DEBUG_PRINT(DEBUG_ERROR, "Result of deleteRecording is %d\n", result);

                if ( DVRResult_ok == result )
                {
                        response["result"] = "SUCCESS";
			response["details"] = "Recording deleted";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
		else if (DVRResult_notFound == result)
		{
                        DEBUG_PRINT(DEBUG_ERROR, "RecordingId %s not found. Creating now \n", recordingId.c_str());
                        RecordingSpec spec;
                        string playUrl = req["playUrl"].asString();

			// Pre-condition: Create test recording
                        createTestRecordingSpec (recordingId, playUrl, spec);
                        result = dvm->createRecording( spec );

                        if ( DVRResult_ok != result )
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to create recording for DeleteRecording";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
                                return TEST_FAILURE;
                        }
			else
			{
				DEBUG_PRINT(DEBUG_TRACE, "Retrying to delete recording \n");
				result= dvm->deleteRecording ( recordingId );

				if ( DVRResult_ok == result )
				{
					response["result"] = "SUCCESS";
					response["details"] = "Recording deleted";
					DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
					return TEST_SUCCESS;
				}
				else
				{
					DEBUG_PRINT(DEBUG_ERROR, "Retry: Error deleting recording : %d\n", result);
					response["result"] = "FAILURE";
					response["details"] = "Failed to delete recording";
					DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
					return TEST_FAILURE;
				}
			}
		}
                else
                {
			DEBUG_PRINT(DEBUG_ERROR, "Error deleting recording : %d\n", result);
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to delete recording";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount

Arguments     : Input argument is NONE.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the segments count.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[25] = {'\0'};
                int count = dvm->getSegmentsCount();

                DEBUG_PRINT(DEBUG_LOG, "Number of Segments = %d\n", count);
                sprintf(stringDetails, "SegmentCount:%d", count);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex

Arguments     : Input argument is 'index'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the segment info by index.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex --->Entry\n");
        unsigned int index = req["index"].asInt();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[50] = {'\0'};
                unsigned int count = 0;

                RecordingSegmentInfo *pSegInfo= dvm->getRecordingSegmentInfoByIndex( index );
                if ( pSegInfo )
                {
                        long long segmentName = pSegInfo->segmentName;
                        DEBUG_PRINT(DEBUG_TRACE, "Segment Name: %lld\n", segmentName);
                        sprintf(stringDetails, "Index: %d SegmentName:%lld", index, segmentName);
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        count = dvm->getRecordingCount();
                        if (0 == count)
                        {
                            DEBUG_PRINT(DEBUG_ERROR, "Found no recordings on device\n");
                        }
                        else if (index >= count )
                        {
                            DEBUG_PRINT(DEBUG_ERROR, "No recording found with index: %d\n", index);

                            sprintf(stringDetails, "Check index value. No recording found with index: %d\n", index);
                            response["result"] = "FAILURE";
                            response["details"] = stringDetails;
                            DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                            return TEST_FAILURE;
                        }
                        else
                        {
                            DEBUG_PRINT(DEBUG_ERROR, "Invalid recording segment for index: %d\n", index);
                            RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex(index);
                            if (pRecInfo)
                            {
                                sprintf(stringDetails, "Index:%d Id:%s Duration:%lld segmentCount:%d",
                                index, pRecInfo->recordingId.c_str(), dvm->getRecordingDuration(pRecInfo->recordingId), pRecInfo->segmentCount);
                            }
                            else
                            {
                                sprintf(stringDetails, "DVR mgr failed to get recording info by index");
                            }

                            response["result"] = "FAILURE";
                            response["details"] = stringDetails;
                            DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                            return TEST_FAILURE;
                        }

                        // Pre-condition: Create test recording
                        RecordingSpec spec;
                        int dvrres = DVRResult_ok;
                        string playUrl = req["playUrl"].asString();
                        index = 0;

                        char sRecId[25] = {'\0'};
                        int iRecId = rand() % 10000 + 2000;

                        sprintf(sRecId, "%d", iRecId);
                        std::string randRecId(sRecId);
                        spec.setRecordingId(randRecId);

                        createTestRecordingSpec (randRecId, playUrl, spec);
                        DEBUG_PRINT(DEBUG_TRACE, "Creating new recording:%s\n", randRecId.c_str());
                        dvrres = dvm->createRecording( spec );

                        if (( DVRResult_ok != dvrres ) && ( DVRResult_alreadyExists != dvrres ))
                        {
                            response["result"] = "FAILURE";
                            response["details"] = "Failed to create recording for GetRecordingSegmentInfoByIndex";
                            DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                            return TEST_FAILURE;
                        }

                        RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex(index);
                        if (pRecInfo)
                        {
                            sprintf(stringDetails, "Index:%d Id:%s Duration:%lld segmentCount:%d",
                            index, pRecInfo->recordingId.c_str(), dvm->getRecordingDuration(pRecInfo->recordingId), pRecInfo->segmentCount);
                        }
                        else
                        {
                            sprintf(stringDetails, "DVR Mgr failed to get recording info by index");
                        }

                        pSegInfo = dvm->getRecordingSegmentInfoByIndex( index );
                        if ( !pSegInfo )
                        {
                            DEBUG_PRINT(DEBUG_TRACE, "Failed to get RecordingSegmentInfoByIndex\n");
                            response["result"] = "FAILURE";
                            response["details"] = stringDetails;
                            DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                            return TEST_FAILURE;
                        }

                        long long segmentName = pSegInfo->segmentName;
                        DEBUG_PRINT(DEBUG_TRACE, "Segment Name: %lld\n", segmentName);
                        sprintf(stringDetails, "Index: %d SegmentName:%lld", index, segmentName);
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;

                        // Post-condition: Delete test recording
                        DEBUG_PRINT(DEBUG_TRACE, "Deleting recording:%s\n", randRecId.c_str());
                        int res_DVR = dvm->deleteRecording ( randRecId );
                        DEBUG_PRINT(DEBUG_ERROR, "Error (%d) deleting recording\n", res_DVR);
                        if ( DVRResult_ok != res_DVR )
                        {
                            response["result"] = "FAILURE";
                            response["details"] = "Failed to delete recording for GetRecordingSegmentInfoByIndex";
                            DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex --> Exit\n");
                            return TEST_FAILURE;
                        }

                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                        return TEST_SUCCESS;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
        return TEST_FAILURE;
}
/**************************************************************************
Function name : MediaframeworkAgent::testmodulepost_requisites

Arguments     : None

Description   : Re-Setting the Pre-requisites which was set after execution

***************************************************************************/
bool MediaframeworkAgent::testmodulepost_requisites()
{
	#ifdef USE_SOC_INIT
        // Uninitialize SOC
        soc_uninit();
	#endif
        DEBUG_PRINT(DEBUG_TRACE, "testmodulepost_requisites --> Entry\n");
        ifstream logfile;
        string MF_testmodule_POST_cmd, MF_testmodule_POST_log,line;
        MF_testmodule_POST_cmd= g_tdkPath + "/" + POST_REQUISITE_FILE;
        MF_testmodule_POST_log= g_tdkPath + "/" + POST_REQUISITE_LOG_PATH;
        string post_req_chk= "source "+MF_testmodule_POST_cmd;

	/*TODO:Commented due to the bug RDKTT:106  */
#if 0
        int offset;
        try
        {
		
                system((char *)post_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of post-requisite script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
        logfile.open(MF_testmodule_POST_log.c_str());
        if(logfile.is_open())
        {
                if(getline(logfile,line)>0);
                {
                        if ((offset = line.find("SUCCESS", 0)) != std::string::npos) {
                        logfile.close();
                        DEBUG_PRINT(DEBUG_LOG,"\nPost-Requisites set %s\n",line.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "testmodulepost_requisites --> Exit\n");
                        return TEST_SUCCESS;
                        }
                        DEBUG_PRINT(DEBUG_ERROR,"\nPost-Requisites Reset Failed - %s\n", line.c_str());
                        return TEST_FAILURE;
                }
                logfile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\nPost-Requisites not set\n");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
                return TEST_FAILURE;
        }
#endif
	return TEST_SUCCESS;
}


/**************************************************************************
  Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "MediaframeworkAgent".
 **************************************************************************/

extern "C" MediaframeworkAgent* CreateObject()
{
	return new MediaframeworkAgent();
}

/**************************************************************************
  Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/

bool MediaframeworkAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_ERROR, "cleaningup\n");

	if(NULL == ptrAgentObj)
	{
		return TEST_FAILURE;
	}

	ptrAgentObj->UnregisterMethod("TestMgr_MPSink_SetGetMute");
	ptrAgentObj->UnregisterMethod("TestMgr_MPSink_SetGetVolume");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrc_GetBufferedRanges");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_State");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_MuteUnmute");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_Volume");

	/*DVR Recording List*/
	ptrAgentObj->UnregisterMethod("TestMgr_DVR_Rec_List");
	ptrAgentObj->UnregisterMethod("TestMgr_DVR_CreateNewRecording");

	/*DVR sink*/
	ptrAgentObj->UnregisterMethod("TestMgr_DVRSink_init_term");

	/*DVR Manager*/
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetSpace");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingCount");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingInfoByIndex");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingInfoById");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetIsRecordingInProgress");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingSize");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingDuration");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingStartTime");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetDefaultTSBMaxDuration");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_CreateTSB");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_ConvertTSBToRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_CreateRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_UpdateRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_DeleteRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetSegmentsCount");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingSegmentInfoByIndex");

/*Optimised Code*/
#if 1
	ptrAgentObj->UnregisterMethod("TestMgr_CheckAudioVideoStatus");
	ptrAgentObj->UnregisterMethod("TestMgr_CheckRmfStreamerCrash");
	ptrAgentObj->UnregisterMethod("TestMgr_ClearLogFile");

	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementCreateInstance");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementRemoveInstance");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementInit");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementTerm");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementOpen");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementClose");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementPlay");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementPause");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementSetSpeed");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetSpeed");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementSetMediaTime");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetMediaTime");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetMediaInfo");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetState");

	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_Sink_SetSource");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_MpSink_SetVideoRectangle");

	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_RmfPlatform_Init");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_InitPlatform");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_UninitPlatform");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_UseFactoryMethods");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_GetLTSID");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_GetLowLevelElement");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_FreeLowLevelElement");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_QAMSrc_ChangeURI");

	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_HNSink_InitPlatform");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_HNSink_UninitPlatform");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_HNSink_SetProperties");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_HNSink_SetSourceType");

#endif

	return TEST_SUCCESS;
}

/**************************************************************************
  Function Name : DestroyObject

Arguments     : Input argument is MediaframeworkAgent Object

Description   : This function will be used to destory the MediaframeAgent object.
 **************************************************************************/
extern "C" void DestroyObject(MediaframeworkAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying Mediaframework Agent object\n");
	delete stubobj;
}
