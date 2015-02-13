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

#include "TDKIntegrationStub.h"

string g_tdkPath = getenv("TDK_PATH");
#define FETCH_STREAMING_INT_NAME "streaming_interface_file"
using namespace std;
#ifdef RMFAGENT
static float totalTuningTime;
static MediaPlayerSink *pSink = NULL;
static HNSource *pSource = NULL;
#endif
#define VIDEO_STATUS "/CheckVideoStatus.sh"
#define AUDIO_STATUS "/CheckAudioStatus.sh"
 
#ifdef XI4
#define CLIENT_MOCA_INTERFACE "eth0"
#else
#define CLIENT_MOCA_INTERFACE "eth1"
#endif

#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int , char *, int );
#endif

/********************************************************************************************************************
Purpose:               To get the current status of the AV running

Parameters:
scriptname [IN]       - The input scriptname

Return:               - bool SUCCESS/FAILURE

 *********************************************************************************************************************/

bool getstreamingstatus(string scriptname)
{
        char buffer[128];
        std::string script = g_tdkPath;
        std::string result = "";
        script.append(scriptname);

        FILE* pipe = popen(script.c_str(), "r");
        if (!pipe)
        {
                DEBUG_PRINT(DEBUG_TRACE, "Error in opening pipe \n");
                return TEST_FAILURE;
        }
        while(!feof(pipe)) {
                if(fgets(buffer, 128, pipe) != NULL)
                        result += buffer;
        }
        pclose(pipe);
        DEBUG_PRINT(DEBUG_TRACE, "Script Output: %s %s\n", script.c_str(), result.c_str());
        if (result.find("SUCCESS") != string::npos)
                return TEST_SUCCESS;
        else
                return TEST_FAILURE;

}

std::string fetchStreamingInterface()
{
        DEBUG_PRINT(DEBUG_TRACE, "Fetch Streaming Interface function --> Entry\n");
        ifstream interfacefile;
        string Fetch_Streaming_interface_cmd, Streaming_Interface_name,line;
        Streaming_Interface_name = g_tdkPath + "/" + FETCH_STREAMING_INT_NAME;
/*      //Fetch_Streaming_interface_cmd = g_tdkPath + "/" + FETCH_STREAMING_INT_SCRIPT;
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

/*************************************************************************
  Function name : E2ELinearTVStub constructor

Arguments     : NULL
 **************************************************************************/
TDKIntegrationStub::TDKIntegrationStub()
{
	DEBUG_PRINT(DEBUG_LOG,"TDKIntegrationTest Initialized");
}
/**************************************************************************
  Function name : TDKIntegrationStub::initialize

Arguments     : IN const char*,IN RDKTestAgent

Description   : Register the callback function of TDKIntegrationStub
 ***************************************************************************/

bool TDKIntegrationStub::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"TDKIntegrationTest Initialized");
#ifdef HYBRID
#ifdef RDK_BR_1DOT3
	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::TDKIntegrationT2pTuning,"TestMgr_HybridE2E_T2pTuning");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::TDKIntegrationT2pTrickplay,"TestMgr_HybridE2E_T2pTrickMode");
#endif
#endif
#ifdef IPCLIENT
	/*Dvr stub wrapper functions*/
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2EStubPlayURL,"TestMgr_E2EStub_PlayURL");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2EStubGetRecURLS,"TestMgr_E2EStub_GetRecURLS");
	/*LinearTV wrapper functions*/
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ELinearTVstubGetURL,"TestMgr_E2ELinearTV_GetURL");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ELinearTVstubPlayURL,"TestMgr_E2ELinearTV_PlayURL");
#endif
#ifdef RMFAGENT
	/* E2E DVR TrickPlay */
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_LinearTv_Dvr_Play, "TestMgr_LinearTv_Dvr_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause, "TestMgr_Dvr_Play_Pause");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Pause_Play, "TestMgr_Dvr_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_FF_FR, "TestMgr_Dvr_Play_TrickPlay_FF_FR");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play, "TestMgr_Dvr_Play_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_Repeat, "TestMgr_Dvr_Play_Pause_Play_Repeat");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point, "TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Forward_Play, "TestMgr_Dvr_Skip_Forward_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_Middle, "TestMgr_Dvr_Skip_Forward_From_Middle");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_End, "TestMgr_Dvr_Skip_Forward_From_End");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_End, "TestMgr_Dvr_Skip_Backward_From_End");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Middle, "TestMgr_Dvr_Skip_Backward_From_Middle");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Starting, "TestMgr_Dvr_Skip_Backward_From_Starting");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Rewind_Forward, "TestMgr_Dvr_Play_Rewind_Forward");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Forward_Rewind, "TestMgr_Dvr_Play_Forward_Rewind");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_Pause_Play, "TestMgr_Dvr_Play_FF_FR_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause_FF_FR, "TestMgr_Dvr_Play_Pause_FF_FR");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_SF_SB, "TestMgr_Dvr_Play_Pause_Play_SF_SB");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_SF_SB, "TestMgr_Dvr_Play_FF_FR_SF_SB");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Pause_Pause, "TestMgr_Dvr_Play_Pause_Pause");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_Play_Play, "TestMgr_Dvr_Play_Play");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_GETURL, "TestMgr_LiveTune_GETURL");
        /*E2E_RMF_TSB*/
        ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFTSB_Play, "TestMgr_TSB_Play");
	/* E2E RF Video */
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_ChannelChange, "TestMgr_RF_Video_ChannelChange");
	ptrAgentObj->RegisterMethod(*this,&TDKIntegrationStub::E2ERMFAgent_MDVR_GetResult, "TestMgr_MDVR_GetResult");
#endif
	return TEST_SUCCESS;
}
/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/

std::string TDKIntegrationStub::testmodulepre_requisites()
{
 	#ifdef USE_SOC_INIT
        //Initialize SOC
        soc_init(1, "agent", 1);
        #endif

        return "SUCCESS";
}
/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool TDKIntegrationStub::testmodulepost_requisites()
{
	#ifdef USE_SOC_INIT
        // Uninitialize SOC
        soc_uninit();
        #endif

        return TEST_SUCCESS;
}
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

        DEBUG_PRINT(DEBUG_TRACE, "Found IP: %s\n",szAddressBuffer);

        if (pIfAddrStruct != NULL)
        {
                freeifaddrs (pIfAddrStruct);
        }

        return szAddressBuffer;

} /* End of GetHostIP */

#ifdef HYBRID
#ifdef RDK_BR_1DOT3
/**************************************************************************
  Function name : TDKIntegrationStub::TDKIntegrationT2pTuning

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the T2pmsg for tuning to the Videoproxy and get the response in the T2ptuningresponse.txt
 ***************************************************************************/
bool TDKIntegrationStub::TDKIntegrationT2pTuning(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::TDKIntegrationT2pTuning--Entry\n");
	string ocapid, line;
	ifstream fileInput;
	int sysRetValScript, errorResponse = 0, respline =0;
	string searchPattern("OK");
	ocapid=(char*)request["ValidocapId"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nValid ocapid  from TestFramework : %s\n",request["ValidocapId"].asCString());

	string urlstringptr = "sh T2pTuning.sh " + ocapid +" > t2ptuneresponse.txt";
	sysRetValScript = system((char *)urlstringptr.c_str());

	if(sysRetValScript!=0 && sysRetValScript <=0)
	{

		DEBUG_PRINT(DEBUG_ERROR,"\nSystem command is failed on executing T2pTuning.sh  \n");
		response["result"]="FAILURE";
		response["details"]="FAILURE:System command is failed on executing T2pTuning.sh";
		return TEST_FAILURE;
	}
	char cwd[1024];
	string syscwd;

	if(getcwd(cwd, sizeof(cwd))==NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGetcwd returns NULL \n");
		response["result"]="FAILURE";
		response["details"]="FAILURE";
	}
	else if(strcmp(cwd,"/")==0)
	{
		syscwd = std::string(cwd);
	}
	else
	{
		syscwd = std::string(cwd)+"/"; 
	}
	// open t2ptuneresponse.txt log file to search pattern for SUCCESS  or FAILURE
	fileInput.open("t2ptuneresponse.txt");
	if(fileInput.is_open())
	{
		while(getline(fileInput, line))
		{
			respline++;

			if (line.find(searchPattern) != string::npos)
			{

				DEBUG_PRINT(DEBUG_ERROR,"\n Status found in t2ptuneresponse.txt\n");
				errorResponse=1;
			}

		}
		fileInput.close();
	}
	if(errorResponse)
	{
		response["result"] = "SUCCESS";
		response["details"]="SUccess:Successfully got the error response";
		response["log-path"] = g_tdkPath+ "t2ptuneresponse.txt";
		return TEST_SUCCESS;	
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGeneric error not OK\n");
		response["result"] = "FAILURE";
		response["details"]="FAILURE:Generic error Not OK";
		//response["log-path"]=syscwd+"t2ptuneresponse.txt";
		response["log-path"] = g_tdkPath+"t2ptuneresponse.txt";
		return TEST_FAILURE;	
	}
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::TDKIntegrationT2pTuning--Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::TDKIntegrationT2pTrickplay

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Changes the trick play rate and captures the log in /t2ptrickmoderesponse.txt and sends to the TestFramework. 
 ***************************************************************************/
bool TDKIntegrationStub::TDKIntegrationT2pTrickplay(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegration::TDKIntegrationT2pTrickplay--Entry\n");
	int errorResponse = 0;
	ifstream fileInput;
	int sysRetValScript;
	string rate;
	string line;
	string searchPattern("OK");
	int respline = 0;
	rate = request["trickPlayRate"].asCString();
	char cwd[1024];
	string syscwd;

	DEBUG_PRINT(DEBUG_LOG,"\nValid trickPlayRate  from TestFramework : %s\n",request["trickPlayRate"].asCString());
	string urlstringptr = "sh T2pTrickMode.sh " + rate +" > t2ptrickmoderesponse.txt";
	sysRetValScript = system((char *)urlstringptr.c_str());
	if(sysRetValScript!=0 && sysRetValScript <=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing T2pTrickMode.sh \n");
		response["result"] = "FAILURE";
		response["details"] = "FAILURE:System command is failed on executing T2pTrickMode.sh";
		return TEST_FAILURE;
	}
	if(getcwd(cwd, sizeof(cwd)) == NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGetcwd returns NULL \n");
		response["details"] = "FAILURE:Getcwd returns NULL";
		response["result"] = "FAILURE";
	}
	else if(strcmp(cwd,"/")==0)
	{
		syscwd = std::string(cwd);
	}
	else
	{
		syscwd = std::string(cwd)+"/";
	}
	// open t2ptrickmoderesponse.txt log file to search pattern for SUCCESS  or FAILURE
	fileInput.open("t2ptrickmoderesponse.txt");
	if(fileInput.is_open())
	{
		while(getline(fileInput, line))
		{
			respline++;

			if (line.find(searchPattern) != string::npos)
			{
				DEBUG_PRINT(DEBUG_ERROR,"\n Status found in t2ptrickmoderesponse.txt\n");
				errorResponse = 1;
			}
		}
		fileInput.close();
	}
	if(errorResponse)
	{
		response["result"] = "SUCCESS";
		response["details"] = "SUCCESS:Status found in t2ptrickmoderesponse.txt";
		response["log-path"] = g_tdkPath+"t2ptrickmoderesponse.txt";
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGeneric error not OK\n");
		response["result"] = "FAILURE";
		response["details"] = "FAILURE:Generic error not OK";
		//response["log-path"]=syscwd+"t2ptrickmoderesponse.txt";
		response["log-path"] = g_tdkPath+"t2ptrickmoderesponse.txt";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegration::TDKIntegrationT2pTrickplay--Exit\n");
	return TEST_SUCCESS;
}
#endif
#endif
#ifdef IPCLIENT
/**************************************************************************
  Function name : TDKIntegrationStub::E2EStubGetRecURLS

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Receving the Requesturl from Test Manager and sends the URL to the Mediastreamer to get the
Recorded Url List.
Returns the FilePath of Recorded Urls List captured
 ***************************************************************************/
bool TDKIntegrationStub::E2EStubGetRecURLS(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2EStubGetRecURLS--Entry\n");
	FILE *ErrorCheck;
	int sysRetValCurl, sysRetValScript;
	string recordedurl = request["RecordURL"].asString();
	//char cmd[128] = "arp -n -i CLIENT_MOCA_INTERFACE|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'"; 
	string cmd = "arp -n -i "+string(CLIENT_MOCA_INTERFACE)+"|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'"; 
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe)
        {
                response["result"] = "FAILURE";
                response["details"] = "Error on popen()";
                DEBUG_PRINT(DEBUG_ERROR, "Error on popen()\n");

                return TEST_FAILURE;
        }
        char buffer[128] = {'\0'};

        std::string resultip = "";
        char ip[128] = {'\0'};

        if(fgets(buffer, sizeof(buffer), pipe) != NULL)
        {
                sscanf(buffer,"%s",ip);
        }
        pclose(pipe);

        if(strcmp(ip,"") == 0)
        {
                response["result"] = "FAILURE";
                response["details"] = "Failed to fetch streaming ip";
                DEBUG_PRINT(DEBUG_ERROR, "Failed to fetch streaming ip\n");

                return TEST_FAILURE;
        }

        resultip = ip;
        DEBUG_PRINT(DEBUG_TRACE, "IP :%send\n",resultip.c_str());
        string urlIn = recordedurl;
        string http = "http://";

        http.append(resultip);

        size_t pos = 0;
        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);
	DEBUG_PRINT(DEBUG_TRACE, "IPCLIENT:Final URL passed to CURL: %s\n",urlIn.c_str());	

	string ptr = "curl " + urlIn +" >recordedlist.txt";
	char cwd[1024];
	string syscwd;
	
	DEBUG_PRINT(DEBUG_ERROR,"\nRecorded URL Received from Test framework : %s \n",ptr.c_str());
	sysRetValCurl=system((char *)ptr.c_str());
	if(sysRetValCurl!=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n system command is failed on executing Curl  \n");
		response["result"]="FAILURE";
		return TEST_FAILURE;
	}
	sysRetValScript=system("source recordedurlscript.sh >Recordedlistmod.txt");
	if(sysRetValScript!=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n system command is failed on executing script \n");
		response["result"]="FAILURE";
		return TEST_FAILURE;
	}
	if(getcwd(cwd, sizeof(cwd))==NULL)
	{

		response["result"]="FAILURE";
	}
	else if(strcmp(cwd,"/")==0)
	{
		syscwd = std::string(cwd);
	}
	else
	{
		syscwd = std::string(cwd)+"/";
	}
	ErrorCheck = fopen("Recordedlistmod.txt","r");
	if(ErrorCheck)
	{
		response["log-path"]=syscwd+"Recordedlistmod.txt";
		fclose(ErrorCheck);
		response["result"]="SUCCESS";
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\n Recordedlistmod.txt is not created \n");
		response["result"]="FAILURE";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2EStubGetRecURLS--Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2EStubPlayURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Play the URL with the Mediaplayer.captured log is
return back to the TestFramework
 ****************************************************************************/
bool TDKIntegrationStub::E2EStubPlayURL(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2EStubPlayURL--Entry\n");
	int sysRetValScript, errorResponse = 0;
	char* playPattern =(char *)"+";
	char cwd[1024];
	string syscwd, line;
	string validurl=request["videoStreamURL"].asString();
	DEBUG_PRINT(DEBUG_ERROR,"\nPLAY_URL   : %s \n",validurl.c_str());

	string urlstringptr = "source mplayerscript.sh \"" + validurl +"\" l ";
	DEBUG_PRINT(DEBUG_ERROR,"\nmplayerscript about to execute ..... URL : %s \n",urlstringptr.c_str());

	sysRetValScript = system((char *)urlstringptr.c_str());
	if(sysRetValScript!=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing mplayerscript \n");
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	sysRetValScript = system("cat e2emplayerlog.txt >> e2emplayerappend.txt");
	if(sysRetValScript!=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on appending mplayer log \n");
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	ifstream fileInput;
	// open file to playPattern
	fileInput.open("e2emplayerlog.txt");
	if(fileInput.is_open())
	{
		while(getline(fileInput, line))
		{
			if (line.find(playPattern, 0) != string::npos)
			{
				DEBUG_PRINT(DEBUG_ERROR,"\nURL is Playing found:+++\n");
				errorResponse = 1;
			}
		}
		fileInput.close();
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\ne2emplayerlog.txt is not found\n");
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	if(getcwd(cwd, sizeof(cwd))== NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGetcwd returns NULL\n");
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	else if(strcmp(cwd,"/")==0)
	{
		syscwd = std::string(cwd);
	}
	else
	{
		syscwd = std::string(cwd)+"/";
	}
	if(errorResponse)
	{
		response["result"] = "SUCCESS";
	}
	else
	{
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	response["log-path"] = syscwd+"e2emplayerappend.txt";
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2EStubPlayURL--Entry\n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ELinearTVstubGetURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the URL to the Mediastreamer get the valid URL in the Json Response.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ELinearTVstubGetURL(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2ELinearTVstubcb--Entry\n");
	CURL *curl;
	CURLcode curlResponse;
	int errorResponse;
	FILE *filepointer;
	string url="";
	Json::Value root;
	url=(char*)request["Validurl"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nValidurl form TestFramework : %s\n",request["Validurl"].asCString());

        //char cmd[128] = "arp -n -i CLIENT_MOCA_INTERFACE|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'";
        string cmd = "arp -n -i"+string(CLIENT_MOCA_INTERFACE)+"|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'";
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe)
        {
                response["result"] = "FAILURE";
                response["details"] = "Error on popen()";
                DEBUG_PRINT(DEBUG_ERROR, "Error on popen()\n");

                return TEST_FAILURE;
        }
        char buffer[128] = {'\0'};

        std::string resultip = "";
        char ip[128] = {'\0'};

        if(fgets(buffer, sizeof(buffer), pipe) != NULL)
        {
                sscanf(buffer,"%s",ip);
        }
        pclose(pipe);

        if(strcmp(ip,"") == 0)
        {
                response["result"] = "FAILURE";
                response["details"] = "Failed to fetch streaming ip";
                DEBUG_PRINT(DEBUG_ERROR, "Failed to fetch streaming ip\n");

                return TEST_FAILURE;
        }

        resultip = ip;
        DEBUG_PRINT(DEBUG_TRACE, "IP :%send\n",resultip.c_str());
        string urlIn = url;
        string http = "http://";

        http.append(resultip);

        size_t pos = 0;
        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);

        DEBUG_PRINT(DEBUG_TRACE, "IPCLIENT:Final URL passed to CURL: %s\n",urlIn.c_str());

	curl = curl_easy_init();
	if(curl)
	{
		curl_easy_setopt(curl, CURLOPT_URL,(char *)urlIn.c_str());
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		//write in to a file
		filepointer=fopen("jsonfile.json","wb");
		curl_easy_setopt( curl, CURLOPT_WRITEDATA, filepointer ) ;
		curlResponse= curl_easy_perform(curl);
		DEBUG_PRINT(DEBUG_ERROR,"the curlResponse value %d\n",curlResponse);
		fclose(filepointer);
	}
	if(curlResponse != CURLE_OK)
	{
		fprintf(stderr, "curl_easy_perform() failed: %s \n",curl_easy_strerror(curlResponse));
		response["result"]="FAILURE";
		response["details"]="Curl API failed";
		return false;
	}
	curl_easy_cleanup(curl);
	ifstream file("jsonfile.json");
	file>>root;
	errorResponse=root["errorCode"].asInt();
	response["details"]=root["videoStreamingURL"].asString();
	DEBUG_PRINT(DEBUG_LOG,"\nJSON Response from MediaStreamer :-\n");
	DEBUG_PRINT(DEBUG_LOG,"\nErrorCode         : %d\n",root["errorCode"].asInt());
	DEBUG_PRINT(DEBUG_LOG,"\nErrorDescription  : %s \n",root["errorDescription"].asCString());
	DEBUG_PRINT(DEBUG_LOG,"\nVideoStreamingURL : %s\n",root["videoStreamingURL"].asCString());
	if(!errorResponse)
	{
		response["result"]="SUCCESS";
	}
	else
	{
		//Filling json response with FAILURE status and error message
		response["result"]="FAILURE";
		response["details"]="Response of Json is failed";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2EStubPlayURL--Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ELinearTVstubPlayURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Play the URL with the Mediaplayer.captured log is
return back to the TestFramework
 ***************************************************************************/
bool TDKIntegrationStub::E2ELinearTVstubPlayURL(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2ELinearTVStubPlayURL--Entry\n");
	int errorResponse=0;
	ifstream fileInput;
	int sysRetValScript;
	string line;
	char* searchPattern = (char *)"+";
	int curline =0;
	char cwd[1024];
	string syscwd;

	string validurl=request["videoStreamURL"].asString();
	DEBUG_PRINT(DEBUG_ERROR,"\nPLAY_URL   : %s \n",validurl.c_str());

	string urlstringptr = "sh runmplayer.sh mplayer \""+ validurl +"\" l >mplayerlog.txt";

	DEBUG_PRINT(DEBUG_ERROR,"\nmplayerscript about to execute ..... URL : %s \n",urlstringptr.c_str());

	sysRetValScript = system((char *)urlstringptr.c_str());
	if(sysRetValScript!=0)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing mplayerscript \n");
		response["result"]="FAILURE";
		return TEST_FAILURE;
	}

	if(getcwd(cwd, sizeof(cwd))==NULL)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGetcwd returns NULL \n");
		response["result"]="FAILURE";
	}
	else if(strcmp(cwd,"/")==0)
	{
		syscwd = std::string(cwd);
	}
	else
	{
		syscwd = std::string(cwd)+"/";
	}
	// open mplayer log file to search pattern for SUCCESS  or FAILURE
	fileInput.open("mplayerlog.txt");
	if(fileInput.is_open())
	{
		while(getline(fileInput, line))
		{
			curline++;
			if (line.find(searchPattern, 0) != string::npos)
			{
				DEBUG_PRINT(DEBUG_ERROR,"\nURL is Playing found:+++\n");
				errorResponse=1;
			}

		}
		fileInput.close();
	}
	if(errorResponse)
	{
		response["result"]="SUCCESS";
		response["log-path"] = g_tdkPath+"t2ptuneresponse.txt";
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nURL is Not Played n");
		response["result"] = "FAILURE";
		response["log-path"] = g_tdkPath+"t2ptuneresponse.txt";
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2ELinearTVStubPlayURL--Exit\n");
	return TEST_SUCCESS;
}
#endif
#ifdef RMFAGENT

/* Time taken to tune the channel.
   totalTuningTime = (time difference of HNSrc->open() API call and return) + (time difference of HNSrc->play() API call and return)
 */
/**************************************************************************
  Function name : init_open_HNsrc_MPsink

Arguments     : Input argument is Playback URL, mime, Json object. Output argument is "SUCCESS" or "FAILURE".

Description   : Helper function to initialize, open HnSrc and MpSink component.
 ****************************************************************************/
int init_open_HNsrc_MPsink(const char *url,char *mime,OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	RMFResult retMPSinkValue = RMF_RESULT_SUCCESS;

	pSource = new HNSource();
	pSink =  new MediaPlayerSink();

	if(pSource == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource instance creation failed\n");

		return TEST_FAILURE;
	}

	if(pSink == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance creation failed\n");

		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->init();
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource initialization failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource initialization failed %ld\n",retHNSrcValue);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc init\n");

	Time tuneTime;
	struct timeval startTime, endTime;
	int sTime = 0, eTime = 0;

#ifdef ENABLE_HYBRID_CODECOMPILE
	/*Fetching the streming interface IP: eth1 */
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
	string urlIn = url;
	string http = "http://";

	http.append(streamingip);

	DEBUG_PRINT(DEBUG_TRACE, "Incoming URL: %s\n",url);
	DEBUG_PRINT(DEBUG_TRACE, "After appending streaming IP to http: %s\n",http.c_str());
	DEBUG_PRINT(DEBUG_TRACE, "IP : %s\n",streamingip.c_str());


	pos = urlIn.find(":8080");
	urlIn = urlIn.replace(0,pos,http);

	DEBUG_PRINT(DEBUG_TRACE, "HYBRID:Final URL passed to Open(): %s\n",urlIn.c_str());

	sTime = tuneTime.getTime(&startTime);
	retHNSrcValue = pSource->open(urlIn.c_str(),mime);
	eTime = tuneTime.getTime(&endTime);

	DEBUG_PRINT(DEBUG_TRACE, "HYBRID:Passed Open() with streamingIP URL\n");

#else

    #ifndef STAND_ALONE_CLIENT

	//char cmd[128] = "arp -n -i CLIENT_MOCA_INTERFACE|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'";
	string  cmd= "arp -n -i "+string(CLIENT_MOCA_INTERFACE)+"|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'";
	FILE* pipe = popen(cmd.c_str(), "r");
	if (!pipe)
	{
		response["result"] = "FAILURE";
		response["details"] = "Error on popen()";
		DEBUG_PRINT(DEBUG_ERROR, "Error on popen()\n");

		return TEST_FAILURE;
	}
	char buffer[128] = {'\0'};

	std::string resultip = "";
	char ip[128] = {'\0'};

	if(fgets(buffer, sizeof(buffer), pipe) != NULL)
	{
		sscanf(buffer,"%s",ip);
	}
	pclose(pipe);

	if(strcmp(ip,"") == 0)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to fetch streaming ip";
		DEBUG_PRINT(DEBUG_ERROR, "Failed to fetch streaming ip\n");

		return TEST_FAILURE;
	}

	resultip = ip;
	DEBUG_PRINT(DEBUG_TRACE, "IP :%send\n",resultip.c_str());
	string urlIn = url;
	string http = "http://";

	http.append(resultip);

	size_t pos = 0;
	pos = urlIn.find(":8080");
	urlIn = urlIn.replace(0,pos,http);

	DEBUG_PRINT(DEBUG_TRACE, "Final URL passed to Open(): %s\n",urlIn.c_str());

	sTime = tuneTime.getTime(&startTime);
	retHNSrcValue = pSource->open(urlIn.c_str(),mime);
	eTime = tuneTime.getTime(&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "XI3:Passed Open() with streamingIP URL\n");

    #else
        string urlIn = url;
        DEBUG_PRINT(DEBUG_TRACE, "IPCLIENT:Final URL passed to CURL: %s\n",urlIn.c_str());
    #endif

#endif
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource open failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource open failed %ld\n",retHNSrcValue);

		pSource->term();
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc open\n");
	/* TuningTime */
	totalTuningTime = tuneTime.ExecutionTime(sTime,&startTime,eTime,&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "open() tune time: %f in ms (milli seconds)\n",totalTuningTime);
	retMPSinkValue = pSink->init();
	if(RMF_RESULT_SUCCESS != retMPSinkValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink initialization failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink initialization failed %ld\n",retMPSinkValue);
		//Source close and terminate before exiting.
		pSource->close();
		pSource->term();
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink init\n");
	retMPSinkValue = pSink->setVideoRectangle(X_VALUE, Y_VALUE, WIDTH, HEIGHT, 0);
	if(RMF_RESULT_SUCCESS != retMPSinkValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink setVideoRectangle failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink setVideoRectangle failed %ld\n",retMPSinkValue);
		//Source close and terminate before exiting.
		pSource->close();
		pSource->term();
		//Sink terminate
		pSink->term();
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink set video rectangle\n");
	retMPSinkValue = pSink->setSource(pSource);
	if(RMF_RESULT_SUCCESS != retMPSinkValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink setSource failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource failed %ld\n",retMPSinkValue);
		//Source close and terminate before exiting.
		pSource->close();
		pSource->term();
		//Sink terminate
		pSink->term();
		return TEST_FAILURE;
	}
	
	/*FIX for RDKTT-124 ticket*/
	/*Video length not known.*/
        retHNSrcValue = pSource->setVideoLength(0);
        cout << "\nSource_setVideoLength return value :" << retHNSrcValue <<endl;

	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink setSource\n");
	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : close_Term_HNSrc_MPSink

Arguments     : Input argument is Json object. Output argument is "SUCCESS" or "FAILURE".

Description   : Helper function to close, terminate HnSrc and MpSink component.
 ****************************************************************************/
int close_Term_HNSrc_MPSink(OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	RMFResult retMPSinkValue = RMF_RESULT_SUCCESS;
	
	/*FIX for RDKTT-126 ticket*/
        double mediaTime;
        retHNSrcValue = pSource->setMediaTime(0);
        cout<<"Return of Set Media time "<<retHNSrcValue<<endl;
        sleep(5);
        retHNSrcValue = pSource->getMediaTime(mediaTime);
        cout<<"Return of get Media time "<<retHNSrcValue<<endl;
        cout<<" Media time Value "<<mediaTime<<endl;

	retHNSrcValue = pSource->close();
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource close failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource close failed %ld\n",retHNSrcValue);

		retMPSinkValue = pSink->term();
		retHNSrcValue = pSource->term();

		delete pSink;
		delete pSource;
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed Hnsrc close\n");

	retMPSinkValue = pSink->term();
	if(RMF_RESULT_SUCCESS != retMPSinkValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink termination failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink termination failed %ld\n",retMPSinkValue);

		pSource->term();
		delete pSource;

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed MPSink term\n");

	retHNSrcValue = pSource->term();
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource termination failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource termination failed %ld\n",retHNSrcValue);

		retMPSinkValue = pSink->term();
		delete pSink;

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed Hnsrc term\n");

	delete pSource;
	delete pSink;

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : changePlaySpeed

Arguments     : Input argument is Json object. Output argument is "SUCCESS" or "FAILURE".

Description   : Helper function to perform the trickplay (forward/rewind).
 ****************************************************************************/
bool changePlaySpeed(float newSpeed,OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	retHNSrcValue = pSource->setSpeed(newSpeed);
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);

		return TEST_FAILURE;
	}

	sleep(10);

	float curSpeed = 0.0;
	pSource->getSpeed(curSpeed);
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay current rate: %f\n",curSpeed);

	if(newSpeed != curSpeed)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource failed to change speed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to change speed\n");

		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : skipNumberOfSeconds

Arguments     : Input argument is number of seconds to skip, to skip forward or backward and Json object. Output argument is "SUCCESS" or "FAILURE".

Description   : Helper function, To skip forward and backward for a given number of seconds form the current point.
 ****************************************************************************/
bool skipNumberOfSeconds(int numberOfSec, int direction, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	double time = 0.0;
	retHNSrcValue = pSource->getMediaTime(time);
	if(direction == SKIP_FORWARD)
	{
		retHNSrcValue = pSource->setMediaTime(time + numberOfSec);
		if(RMF_RESULT_SUCCESS != retHNSrcValue)
		{
			response["result"] = "FAILURE";
			response["details"] = "HNSource setMediaTime failed.\n";
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.");

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Skip Forward: %d Done.\n",numberOfSec);
	}
	else
	{
		retHNSrcValue = pSource->setMediaTime(time - numberOfSec);
		if(RMF_RESULT_SUCCESS != retHNSrcValue)
		{
			response["result"] = "FAILURE";
			response["details"] = "HNSource setMediaTime failed.\n";
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.");

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Skip Backward: %d Done.\n",numberOfSec);
	}

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : playPause

Arguments     : Input argument Json object. Output argument is "SUCCESS" or "FAILURE".

Description   : Helper function to perform play and pause on video playback.
 ****************************************************************************/
bool playPause(OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);
	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play \n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(25);
	retHNSrcValue = pSource->pause();
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource pause failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource getState failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource getState failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	if (RMF_STATE_PAUSED == curState)
	{
		response["result"] = "SUCCESS";
		response["details"] = "DVR Play pause Successful ";
		DEBUG_PRINT(DEBUG_ERROR, "DVR Play pause Successful \n");
	}

	sleep(10);
	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   :Sends the URL to HYBRID to playback the video. URL can be Linear TV or DVR URL.
 **************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_LinearTv_Dvr_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	string modurl;

	/*The URL speed comparision part of code is commented, Based on the comment made against the ticket RDKTT-49 */
#if 0
	/*Check for the play_speed, from the input URL */
	int playSpeedStrPosition = url.find("play_speed");
	float urlSpeed = 0.0;
#endif
	if( url.find("dvr")!= -1)
        {
	int modurllen = url.find("&0");
        modurl = url.substr(0,modurllen+2);
        DEBUG_PRINT(DEBUG_LOG,"\nmodurl=%s\n",modurl.c_str());
	}
	else
	{
		modurl=url;
	}

	//if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	if(TEST_FAILURE == init_open_HNsrc_MPsink(modurl.c_str(),NULL,response))
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_ERROR, "After init_open_HNsrc_MPsink------------------\n");
	
        int playSpeedStrPosition = url.find("play_speed");

        if( url.find("dvr")!= -1)
        {
                DEBUG_PRINT(DEBUG_LOG,"\nDVR url\n");
        int TimePosStrPosition = url.find("time_pos");
        float URLPlaySpeed = 0.0;
        double URLTimepos = 0.0;
        if(-1 != playSpeedStrPosition)
        {
                std::string playSpeed = url.substr(playSpeedStrPosition);
                int ePos = playSpeed.find("=");
                int aPos = playSpeed.find("&");
                std::string rate = playSpeed.substr(ePos + 1,(aPos - ePos) - 1);
                std::string Timepos = url.substr(TimePosStrPosition);
                ePos = Timepos.find("=");
                std::string time = Timepos.substr(ePos +1,string::npos );

                URLPlaySpeed = strtof(rate.c_str(),NULL);
                URLTimepos = strtod(time.c_str(),NULL);
                DEBUG_PRINT(DEBUG_LOG,"URL appended Rate: %f\n",URLPlaySpeed);
                DEBUG_PRINT(DEBUG_LOG,"URL appended time: %lf\n",URLTimepos);
		retHNSrcValue = pSource->play(URLPlaySpeed,URLTimepos);
        }
        }
        else if( url.find("live")!= -1)
        {
                DEBUG_PRINT(DEBUG_LOG,"\nLive url\n");
		retHNSrcValue = pSource->play();
        }
        else
        {
                DEBUG_PRINT(DEBUG_LOG,"\nInvalid url\n");
		retHNSrcValue = -1;
        }

	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play\n");
#if 0
	/*Only for DVR Trick Play, Extract the trickPlay rate from the url.*/
	if(NOT_PRESENT != playSpeedStrPosition)
	{
		string playSpeed = url.substr(playSpeedStrPosition);
		int ePos = playSpeed.find("=");
		int aPos = playSpeed.find("&");
		string rate = playSpeed.substr(ePos + 1,(aPos - ePos) - 1);

		urlSpeed = strtof(rate.c_str(),NULL);
		DEBUG_PRINT(DEBUG_TRACE, "URL appended Rate: %f\n",urlSpeed);
	}
#endif
	/*Query the current speed */
	float curSpeed = 0.0;
	pSource->getSpeed(curSpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(5);

	/* additional check with scripts */
	if(TEST_FAILURE == getstreamingstatus(VIDEO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Video playback have encountered an error.";
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	if(TEST_FAILURE ==  getstreamingstatus(AUDIO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Audio playback have encountered an error.";
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}

	sleep(60);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

#if 0
	if(NOT_PRESENT != playSpeedStrPosition)
	{
		/*Compare the queried speed with requested speed */
		if(curSpeed != urlSpeed)
		{
			response["result"] = "FAILURE";
			response["details"] = "Playback failed to play in the specified speed";
			DEBUG_PRINT(DEBUG_ERROR, "Playback failed to play in the specified speed\n");

			return TEST_FAILURE;
		}
	}
#endif

	response["result"] = "SUCCESS";
	response["details"] = "Playback Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Playback Successful \n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Play and Pause on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause(IN const Json::Value& req, OUT Json::Value& response)
{
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	if(TEST_FAILURE == playPause(response))
	{
		return TEST_FAILURE;
	}

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Pause and Play on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
	sleep(1);
	/*Query the current speed */
	float curSpeed = 0.0;
	pSource->getSpeed(curSpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	

	/*Commented this part code as per comment made by the core team against the ticket RDKTT-49 */
/*	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)*/
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource failed to play.";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to play.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	sleep(5);

	float changeSpeed = 1.0;

	retHNSrcValue = pSource->setSpeed(changeSpeed);
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		close_Term_HNSrc_MPSink(response);
		response["result"] = "FAILURE";
		response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);

		return TEST_FAILURE;
	}

	sleep(1);

	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state is not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state is not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(40);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Pause Play is Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Pause Play Successful \n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_FF_FR

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Play and can perform trickplay(forward/rewind in different rate) on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_FF_FR(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play\n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	sleep(40);
	float changeSpeed = req["speed"].asFloat();
	if(TEST_FAILURE == changePlaySpeed(changeSpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed success.\n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	response["result"] = "SUCCESS";
	response["details"] = "DVR Trickplay Fast Forward/Rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "DVR Trickplay Fast Forward/Rewind Successful \n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Play still the end of recording and can perform trickplay(rewind in different rate) on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();
	float changeSpeed = req["rewindSpeed"].asFloat();

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay RewindSpeed: %f\n",changeSpeed);

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	/*Query the current speed */
	float curSpeed = 0.0;
	pSource->getSpeed(curSpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

	/*      FIXME: Need to figure out the way to get the Total video duration.

	//MediaInfo: startTime and Duration.
	RMFMediaInfo mediaInfo;
	pSource->getMediaInfo(mediaInfo);
	cout << "Duration of Video: " << mediaInfo.m_duration << endl;
	cout << "StartTime of Video: " << mediaInfo.m_startTime << endl;
	 */
	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(20);

	/*Aussuming the total duration for 2mins. i.e,120 seconds*/
	double seekToEndPoint = 120;
	retHNSrcValue = pSource->setMediaTime(seekToEndPoint);
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource setMediaTime failed.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	retHNSrcValue = pSource->setSpeed(changeSpeed);
	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	{
		close_Term_HNSrc_MPSink(response);

		response["result"] = "FAILURE";
		response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);
		return TEST_FAILURE;
	}
	sleep(5);

	curSpeed = 0.0;
	pSource->getSpeed(curSpeed);
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay current speed: %f\n",curSpeed);
	if(changeSpeed != curSpeed)
	{
		close_Term_HNSrc_MPSink(response);

		response["result"] = "FAILURE";
		response["details"] = "HNSource failed to change speed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to change speed\n");

		return TEST_FAILURE;
	}

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Rewind from end point Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Rewind from end point Successful \n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Play, pause and play on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	if(TEST_FAILURE == playPause(response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(20);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_Repeat

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And does Play, pause and play repeat the sequence multiple times on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_Repeat(IN const Json::Value& req, OUT Json::Value& response)
{
	int repeatCount = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, " Repeat time: %d\n",repeatCount);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	for(int repeat = 0;repeat < repeatCount; repeat++)
	{
		if(TEST_FAILURE == playPause(response))
		{
			DEBUG_PRINT(DEBUG_TRACE, " Failure: %d repeatation\n",repeat + 1);
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
	}
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "DVR Play Pause Play Repeat Successful";
	DEBUG_PRINT(DEBUG_TRACE, "DVR Play Pause Play Repeat Successful\n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Forward_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips forward number of seconds on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Forward_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_TRACE, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}

	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
	{
		if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(5);
	}

	sleep(40);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Skip forward from starting of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from starting of video Successful \n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_Middle

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips forward number of seconds on the video being played when time position is half the total duration.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_Middle(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");


	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	/*FIXME: Don't no the Duration of the video. So, assuming middle of the video as 25 seconds.*/
	sleep(25);
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
	{
		if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
		{
			stringstream ss;
			string details;
			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);
			close_Term_HNSrc_MPSink(response);
			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(5);
	}
	sleep(30);
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	response["result"] = "SUCCESS";
	response["details"] = "Skip forward from middle of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from middle of video Successful \n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_End

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips forward number of seconds on the video being played when time position is equal to the total duration.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_End(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");


	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	/*FIXME: Don't no the Duration of the video. So, assuming end of the video as 40 seconds.*/
	sleep(40);

	if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}

	sleep(20);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Skip forward from end of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from end of video Successful \n");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_End

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips Backward number of seconds on the video being played when time position is equal to the total duration.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_End(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");


	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	/*FIXME: Don't no the Duration of the video. So, assuming end of the video as 40 seconds.*/
	sleep(40);

	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
	{
		if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(5);
	}

	sleep(20);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Skip backward from end of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip backward from end of video Successful \n");
	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Middle

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips Backward number of seconds on the video being played when time position is half to the total duration.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Middle(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;
		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");


	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}


	/*FIXME: Don't no the Duration of the video. So, assuming middle of the video as 25 seconds.*/
	sleep(25);

	if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(30);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Skip Backward from middle of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip Backward from middle of video Successful \n");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Starting

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Skips Backward number of seconds on the video that is being started playing.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Starting(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	sleep(3);

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(40);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Skip backward from starting of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip backward from starting of video Successful \n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Rewind_Forward

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do rewind and forward for the given trickplay speed on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Rewind_Forward(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();

	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		cout << "Error: " << retHNSrcValue << " returned, HNsource playback failed current state not playing.\n";
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(20);

	/*Rewind it for some time.*/
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Rewind success passed \n");

	/*Forward it for some time*/
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Forward success passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play rewind forward Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play rewind forward Successful");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Forward_Rewind

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do forward and rewind for the given trickplay speed on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Forward_Rewind(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();
	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	sleep(1);

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(20);

	/*Forward it for some time*/
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Forward success Passed \n");

	/*Rewind it for some time.*/
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Rewind success Passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	response["result"] = "SUCCESS";
	response["details"] = "Play forward rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play forward rewind Successful");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do forward or rewind followed by pause and play on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float trickPlaySpeed = req["trickPlayRate"].asFloat();

	DEBUG_PRINT(DEBUG_TRACE, "Trick Play Speed: %f \n",trickPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(20);

	/*Forward/Rewind it for some time*/
	if(TEST_FAILURE == changePlaySpeed(trickPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Forward/Rewind success passed\n");
	/*pause it for sometime */
	retHNSrcValue = pSource->pause();
	DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);
	sleep(10);
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource pause failed current state not paused.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	/*Play it in normal speed 1.0*/
	float normalSpeed = 1.0;
	if(TEST_FAILURE == changePlaySpeed(normalSpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Setting to normal speed success passed \n");
	sleep(10);
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play forward/Rewind pause play Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play forward/Rewind pause play Successful");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause_FF_FR

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do pause and do forward/rewind on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause_FF_FR(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float trickPlaySpeed = req["trickPlayRate"].asFloat();

	DEBUG_PRINT(DEBUG_TRACE, " Trick Play Speed: %f\n",trickPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(20);

	/*pause it for sometime */
	retHNSrcValue = pSource->pause();
	DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);

	sleep(10);

	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource pause failed current state not paused.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	/*Forward/Rewind it for some time*/
	if(TEST_FAILURE == changePlaySpeed(trickPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Forward/Rewind success Passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play pause forward/Rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play pause forward/Rewind Successful");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_SF_SB

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do pause, play and skip forward/backward for the given number of seconds on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_SF_SB(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();
	double skipForwardSec = req["sfSeconds"].asDouble();
	double skipBackwardSec = req["sbSeconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number Of repeatation: %d \n",numberOfRepeatation);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds forward: %f\n",skipForwardSec);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds backward: %f\n",skipBackwardSec);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	sleep(20);

	/*pause it for sometime */
	retHNSrcValue = pSource->pause();
	DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);

	sleep(10);

	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource pause failed current state not paused.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "playing in normal speed success passed \n");

	sleep(10);

	/*Skip Forward/Backward for entered number of times*/
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
	{
		/*Skip Forward for skipForwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipForwardSec,SKIP_FORWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);
			close_Term_HNSrc_MPSink(response);
			return TEST_FAILURE;
		}
		sleep(15);

		/*Skip Backward for skipBackwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipBackwardSec,SKIP_BACKWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(15);
	}
	DEBUG_PRINT(DEBUG_TRACE, "Skip Forward/ Skip Backward success passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play pause play Skip Forward/Backward Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play pause play Skip Forward/Backward Successful \n");
	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_SF_SB

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do forward/rewind for the given trickplay speed and skip forward/backward number of seconds given on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_SF_SB(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();
	double skipForwardSec = req["sfSeconds"].asDouble();
	double skipBackwardSec = req["sbSeconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number Of repeatation: %d\n",numberOfRepeatation);

	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds forward: %f\n",skipForwardSec);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds backward: %f\n",skipBackwardSec);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	sleep(15);

	/*Forward video in the speed given*/
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed forward success passed \n");

	sleep(5);

	/*Backward video in the speed given*/
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed backward success passed \n");

	sleep(5);

	/*Skip Forward/Backward for entered number of times*/
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
	{
		/*Skip Forward for skipForwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipForwardSec,SKIP_FORWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		sleep(15);

		/*Skip Backward for skipBackwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipBackwardSec,SKIP_BACKWARD,response))
		{
			stringstream ss;
			string details;

			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;
			DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(15);
	}
	DEBUG_PRINT(DEBUG_TRACE, "Skip Forward/ Skip Backward passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	response["result"] = "SUCCESS";
	response["details"] = "Play, Forward/Rewind and Skip Forward/Backward Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play, Forward/Rewind and Skip Forward/Backward Successful \n");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Pause_Pause

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do Pause and Pause on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Pause_Pause(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;
		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

	sleep(30);

	for (int repeat = 0; repeat < 2; repeat++)
	{
		retHNSrcValue = pSource->pause();
		if(RMF_RESULT_SUCCESS != retHNSrcValue)
		{
			cout << "Error: " << retHNSrcValue << " returned, HNsource pause failed \n";
			response["result"] = "FAILURE";
			response["details"] = "HNSource pause failed";
			DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed %ld\n",retHNSrcValue);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		sleep(10);
		DEBUG_PRINT(DEBUG_TRACE, "HNSource pause called %d time.\n",repeat + 1);
	}

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource pause failed current state not paused.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource paused failed current state not paused.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play, Pause and Pause on video playback Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play, Pause and Pause on video playback Successful \n");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_Play_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is DVR URL.
And Play for sometime, do Play  on the video being played.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_Play_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	for (int repeat = 0; repeat < 2; repeat++)
	{
		retHNSrcValue = pSource->play();
		sleep(1);
		if(RMF_RESULT_SUCCESS != retHNSrcValue )
		{
			stringstream ss;
			string details;

			ss << response["details"] << " HNSource play failed";
			details = ss.str();
			response["details"] = details;

			DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

			close_Term_HNSrc_MPSink(response);

			return TEST_FAILURE;
		}
		cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
		DEBUG_PRINT(DEBUG_TRACE, "HNSource play called %d time.\n",repeat + 1);
		sleep(20);
	}

	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);

	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		cout << "Error: " << retHNSrcValue << " returned, HNsource play failed current state not playing.\n";
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

		close_Term_HNSrc_MPSink(response);

		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "HNSource getState() passed.\n");
	/* Additional checkpoint for video and audio status */
	if(TEST_FAILURE == getstreamingstatus(VIDEO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Video playback have encountered an error.";
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	if(TEST_FAILURE ==  getstreamingstatus(AUDIO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Audio playback have encountered an error.";
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(5);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	response["details"] = "Play and Play on video playback Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play and Play on video playback Successful \n");

	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_ChannelChange

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Sends the URL to HYBRID to playback the video. URL is .
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_ChannelChange(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	Time tuneTime;
	struct timeval startTime, endTime;
	int sTime = 0, eTime = 0;

	sTime = tuneTime.getTime(&startTime);
	retHNSrcValue = pSource->play();
	eTime = tuneTime.getTime(&endTime);

	sleep(1);

	totalTuningTime += tuneTime.ExecutionTime(sTime,&startTime,eTime,&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "Total time for tuning: %f in ms (milli seconds)\n",totalTuningTime);

	if(RMF_RESULT_SUCCESS != retHNSrcValue )
	{
		stringstream ss;
		string details;

		ss << response["details"] << " HNSource play failed";
		details = ss.str();
		response["details"] = details;
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");
	RMFState curState, pendingState;
	retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource play failed current state not playing.\n";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");
		close_Term_HNSrc_MPSink(response);
		return TEST_FAILURE;
	}
	sleep(5);
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	stringstream sst1,sst2;
	string strTuningTime;

	sst1 << totalTuningTime;
	strTuningTime = sst1.str();
	sst2 << "{'summary':'Channel Tuning Successful','tuningtime':'" << strTuningTime << "'}";

	response["result"] = "SUCCESS";
	response["details"] = sst2.str();
	DEBUG_PRINT(DEBUG_TRACE, "Channel Tuning Successful \n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_GetURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the URL to the Mediastreamer get the valid URL in the Json Response.
Return the Error code and Error Description to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFAgent_GETURL(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2ERMF_GETURL---Entry\n");
	CURL *curl;
	CURLcode curlResponse;
	int errorResponse;
	FILE *filepointer;
	string url;
	Json::Value root;
	url=(char*)request["Validurl"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nValidurl from TestFramework : %s\n",request["Validurl"].asCString());
	string streaming_interface;
	string streamingip;
#ifdef ENABLE_HYBRID_CODECOMPILE
        /*Fetching the streming interface IP: eth1 */
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
        string urlIn = url;
#if 0
        string http = "http://";

        http.append(streamingip);

        DEBUG_PRINT(DEBUG_TRACE, "Incoming URL: %s\n",url.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "After appending streaming IP to http: %s\n",http.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "IP : %s\n",streamingip.c_str());


        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);
#endif

        DEBUG_PRINT(DEBUG_TRACE, "HYBRID:Final URL passed to CURL(): %s\n",urlIn.c_str());
#else

   #ifndef STAND_ALONE_CLIENT

        string cmd = "arp -n -i "+string(CLIENT_MOCA_INTERFACE)+"|grep : | cut -d ' ' -f 2 | cut -b 2- |sed 's/.$//'";
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe)
        {
                response["result"] = "FAILURE";
                response["details"] = "Error on popen()";
                DEBUG_PRINT(DEBUG_ERROR, "Error on popen()\n");

                return TEST_FAILURE;
        }
        char buffer[128] = {'\0'};

        std::string resultip = "";
        char ip[128] = {'\0'};

        if(fgets(buffer, sizeof(buffer), pipe) != NULL)
        {
                sscanf(buffer,"%s",ip);
        }
        pclose(pipe);

        if(strcmp(ip,"") == 0)
        {
                response["result"] = "FAILURE";
                response["details"] = "Failed to fetch streaming ip";
                DEBUG_PRINT(DEBUG_ERROR, "Failed to fetch streaming ip\n");

                return TEST_FAILURE;
        }

        resultip = ip;
	streamingip = ip;
        DEBUG_PRINT(DEBUG_TRACE, "IP :%send\n",resultip.c_str());
        string urlIn = url;
        string http = "http://";

        http.append(resultip);

        size_t pos = 0;
        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);

        DEBUG_PRINT(DEBUG_TRACE, "IPCLIENT:Final URL passed to CURL: %s\n",urlIn.c_str());

    #else
        string urlIn = url;
        DEBUG_PRINT(DEBUG_TRACE, "IPCLIENT:Final URL passed to CURL: %s\n",urlIn.c_str());
    #endif

#endif
#if 0
	curl = curl_easy_init();
	if(curl)
	{
		curl_easy_setopt(curl, CURLOPT_URL,(char *)urlIn.c_str());
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		//write in to a file
		filepointer=fopen("jsonfile.json","wb");
		curl_easy_setopt( curl, CURLOPT_WRITEDATA, filepointer ) ;
		curlResponse= curl_easy_perform(curl);
		DEBUG_PRINT(DEBUG_ERROR,"The curlResponse value %d\n",curlResponse);
		fclose(filepointer);
	}
	if(curlResponse != CURLE_OK)
	{
		fprintf(stderr, "curl_easy_perform() failed: %s \n",curl_easy_strerror(curlResponse));
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
	curl_easy_cleanup(curl);
	ifstream file("/tmp/output.json");
	file>>root;
	//errorResponse = root["errorCode"].asInt();
	response["details"] = root["xmediagateways"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nJSON Response from MediaStreamer :-\n");
	//DEBUG_PRINT(DEBUG_LOG,"\nErrorCode         : %d\n",root["errorCode"].asInt());
	//DEBUG_PRINT(DEBUG_LOG,"\nErrorDescription  : %s \n",root["errorDescription"].asCString());
	DEBUG_PRINT(DEBUG_LOG,"\nVideoStreamingURL : %s\n",root["xmediagateways"].asCString());

	//if(!errorResponse)
	{
		response["result"] = "SUCCESS";
		return TEST_FAILURE;
	}
	//else
	{
		//Filling json response with FAILURE status and error message
		response["result"] = "FAILURE";
		return TEST_FAILURE;
	}
#endif

// Added the code to parse the base URL from output.json
	ifstream logfile;
	string json_parser_cmd, json_parser_log,line;
	json_parser_cmd=g_tdkPath + "/" + JSON_PARSER_SCRIPT;
	json_parser_log=g_tdkPath + "/" + JSON_PARSER_LOG_PATH;
	string parser_chk= "source "+json_parser_cmd + " "+ streamingip + " "+"\""+ urlIn.c_str()+"\"";
	try
        {
                system((char *)parser_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of parser script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
		response["result"] = "FAILURE";
		response["details"] = "Exception occured execution of parser script";
		return TEST_FAILURE;
        }
	logfile.open(json_parser_log.c_str());
        if(logfile.is_open())
        {
                if(getline(logfile,line)>0);
                {
                        logfile.close();
			pos = line.find(":8080");
			if (pos!=std::string::npos)
        		{
                        	DEBUG_PRINT(DEBUG_LOG,"\noutput.json parsed \n");
				response["result"] = "SUCCESS";
				response["details"]= line;
				logfile.close();
                        	return TEST_SUCCESS;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"]= line;
				logfile.close();
				return TEST_FAILURE;
			}	
                }
                logfile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\nJson file  not parsed \n");
		response["result"] = "FAILURE";
		response["details"] = "Proper result is not found in the log file";
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
		response["result"] = "FAILURE";
		response["details"] = "Unable to open the log file";
                return TEST_FAILURE;
        }
	
	DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegrationStub::E2ERMF_GETURL---Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFTSB_Play

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Get the Streaming URL from the TM and play with Hnsrc->MPsink Pipeline.
Return the SUCCESS or FAILURE  to the testFramework.
 ***************************************************************************/
bool TDKIntegrationStub::E2ERMFTSB_Play(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_LOG,"\nTDKIntegration::TDKIntegration_TSB --Entry\n");
        int res_HNSrcGetState;
        float SpeedRate = request["SpeedRate"].asFloat();
        int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcPlay, res_MPSinksetrect, res_HNSrcSetSpeed, res_HNSrcPause;
        int res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm, res_HNSrcClose, res_HNSrcGetSpeed;
        char* playuri = (char*)request["VideostreamURL"].asCString();
        stringstream details;
        RMFState curstate;
        pSource = new HNSource();
        pSink =  new MediaPlayerSink();

	if(pSource == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "HNSource instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource instance creation failed\n");

		return TEST_FAILURE;
	}

	if(pSink == NULL)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance creation failed\n");

		return TEST_FAILURE;
	}

        res_HNSrcInit = pSource->init();
        DEBUG_PRINT(DEBUG_LOG, "----->>>>>> Result of HNSrc Initialize is %d\n", res_HNSrcInit);
        if(0 != res_HNSrcInit)
        {
		delete pSource;		

                response["result"] = "FAILURE";
                response["details"] = "Failed to Initialize hnsource";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }
        DEBUG_PRINT(DEBUG_LOG, "URL From TM is %s\n", playuri);
        res_HNSrcOpen = pSource->open(playuri, 0);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);
        if(0 != res_HNSrcOpen)
        {
                pSource->term();
		delete pSource;

                response["result"] = "FAILURE";
                response["details"] = "Failed to Open hnsource";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

        res_MPSinkInit = pSink->init();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

        if(0 != res_MPSinkInit)
        {
                pSource->close();
                pSource->term();
		delete pSource;

                response["result"] = "FAILURE";
                response["details"] = "Failed to Initialze Mpsink";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

        res_MPSinksetrect = pSink->setVideoRectangle(0, 0, 1280, 720, true);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

        if(0 != res_MPSinksetrect)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Failed to set Video resolution";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

        res_MPSinksetsrc = pSink->setSource(pSource);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);
        if(0 != res_MPSinksetsrc)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Failed to do set source";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

        res_HNSrcPlay = pSource->play();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);
	sleep(5);
	/* Additional checkpoint for video and audio status */
	if(TEST_FAILURE == getstreamingstatus(VIDEO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Video playback have encountered an error.";
		pSink->term();
		pSource->close();
		pSource->term();
		delete pSource;
		delete pSink;

		return TEST_FAILURE;
	}
	if(TEST_FAILURE ==  getstreamingstatus(AUDIO_STATUS))
	{
		response["result"] = "FAILURE";
		response["details"] = "Audio playback have encountered an error.";
		pSink->term();
		pSource->close();
		pSource->term();
		delete pSource;
		delete pSink;

		return TEST_FAILURE;
	}
        sleep(30);
        DEBUG_PRINT(DEBUG_LOG, "Playing the Video for 30 seconds\n");
        if(0 != res_HNSrcPlay)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Failed to play video using Hnsource and Mpsink pipeline";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

        res_HNSrcGetState = pSource->getState(&curstate, NULL);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);
        if (curstate != RMF_STATE_PLAYING)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                DEBUG_PRINT(DEBUG_ERROR, "Play API call is Success, but Video is not playing");
                response["result"] = "FAILURE";
                response["details"] = "Play API call is Success, but Video is not playing";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }
        //SpeedRate = 0.5;
        DEBUG_PRINT(DEBUG_LOG, "Video is playing");
        DEBUG_PRINT(DEBUG_LOG, "Value from TM:%f",SpeedRate);
        if (SpeedRate >0)
        {
                DEBUG_PRINT(DEBUG_ERROR, "\nPause the video for Forward speed\n");
                res_HNSrcPause = pSource->pause();
                DEBUG_PRINT(DEBUG_LOG, "RMF Result of Pause is %d\n", res_HNSrcPause);
                sleep(100);
                DEBUG_PRINT(DEBUG_LOG, "Pausing the Video for 100 seconds \n");
                if(0 != res_HNSrcPause)
                {
			if(curstate != RMF_STATE_PAUSED)
			{
	                        pSink->term();
        	                pSource->close();
                	        pSource->term();
				delete pSource;
				delete pSink;

	                        DEBUG_PRINT(DEBUG_ERROR, "Video not paused");
        	                response["result"] = "FAILURE";
                	        response["details"] = "Video not paused";
	                        DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
        	                return TEST_FAILURE;
			}
                }
        }

        res_HNSrcSetSpeed = pSource->setSpeed(SpeedRate);
        if(0 != res_HNSrcSetSpeed)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "HNSrc setSpeed() FAILURE";
                DEBUG_PRINT(DEBUG_ERROR, "HNSrc setSpeed() FAILURE\n");
                return TEST_FAILURE;
        }
        response["details"] = "HNSrc setSpeed() successful";
        res_HNSrcGetSpeed = pSource->getSpeed(SpeedRate);
        if(0 != res_HNSrcGetSpeed)
        {
                pSink->term();
                pSource->close();
                pSource->term();
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "FAILURE:Video is not playing for Requested Trickrate in Live ";
                DEBUG_PRINT(DEBUG_ERROR, "HNSrc setSpeed() FAILURE\n");
                return TEST_FAILURE;
        }
        details << "HNSrc getSpeed() successful, Speed:" << SpeedRate;
        response["details"] = details.str();

        res_MPSinkTerm = pSink->term();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPsink termination is %d\n", res_MPSinkTerm);
        res_HNSrcClose = pSource->close();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Hnsource close is %d\n", res_HNSrcClose);
        res_HNSrcTerm = pSource->term();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Hnsource termination is %d\n", res_HNSrcTerm);

        if(0 != res_MPSinkTerm)
        {
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Video played successfully, but failed to terminate MPSink";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }
        if(0 != res_HNSrcClose)
        {
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Video played successfully, but failed to close Hnsource";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }
        if(0 != res_HNSrcTerm)
        {
		delete pSource;
		delete pSink;

                response["result"] = "FAILURE";
                response["details"] = "Video played successfully, but failed to terminate Hnsource";
                DEBUG_PRINT(DEBUG_ERROR, "TDKIntegration_Player--->Exit\n");
                return TEST_FAILURE;
        }

	delete pSource;
	delete pSink;

        response["result"] = "SUCCESS";
        response["details"] = "Video played with TSB successfully";
        DEBUG_PRINT(DEBUG_TRACE, "TDKIntegration_Player--->Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
  Function name : TDKIntegrationStub::E2ERMFAgent_MDVR_GetResult

  Arguments     : Input argument is Overall result list from all clients.
                  Output argument is "SUCCESS" or "FAILURE".

  Description   : Finds if the final result list contains any failure.
***************************************************************************/

bool TDKIntegrationStub::E2ERMFAgent_MDVR_GetResult(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_LOG, "E2ERMFAgent_MDVR_GetResult ----> Entry\n");

        string result = req["resultList"].asCString();

        DEBUG_PRINT(DEBUG_LOG, "Overall execution result  = %s\n", result.c_str());

        if(result.find("FAILURE") != std::string::npos)
        {
                DEBUG_PRINT(DEBUG_ERROR, "One or more clients failed to execute successfully\n");
                response["result"] = "FAILURE";
                response["details"] = "One or more clients failed to execute successfully";
                DEBUG_PRINT(DEBUG_LOG, "E2ERMFAgent_MDVR_GetResult ----> Exit\n");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_LOG, "All Clients executed successfully\n");
                response["result"] = "SUCCESS";
                response["details"] = "All Clients executed successfully";
        }

        DEBUG_PRINT(DEBUG_LOG, "E2ERMFAgent_MDVR_GetResult ----> Exit\n");

        return TEST_SUCCESS;
}
#endif
/**************************************************************************
  Function name : TDKIntegrationStub::CreateObject()

Arguments     : NULL

Description   : create the object of HybridE2EStub  
 ***************************************************************************/
extern "C" TDKIntegrationStub* CreateObject()
{
	return new TDKIntegrationStub();
}

/**************************************************************************
  Function name : HybridE2EStub::cleanup()

Arguments     : NULL

Description   :close things cleanly  
 ***************************************************************************/
bool TDKIntegrationStub::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
#ifdef HYBRID
	/* UnRegister Wrapper functions */
	ptrAgentObj->UnregisterMethod("TestMgr_HybridE2E_T2pTuning");
	ptrAgentObj->UnregisterMethod("TestMgr_HybridE2E_T2pTrickMode");
#endif
#ifdef IPCLIENT
	ptrAgentObj->UnregisterMethod("TestMgr_E2EStub_PlayURL");
	ptrAgentObj->UnregisterMethod("TestMgr_E2EStub_GetRecURLS");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_GetURL");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_PlayURL");	
#endif
#ifdef RMFAGENT
	/* E2E DVR TrickPlay */
	ptrAgentObj->UnregisterMethod("TestMgr_LinearTv_Dvr_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_TrickPlay_FF_FR");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play_Repeat");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_From_Middle");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_From_End");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_End");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_Middle");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_Starting");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Rewind_Forward");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Forward_Rewind");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_FF_FR_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_FF_FR");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play_SF_SB");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_FF_FR_SF_SB");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Pause");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_LiveTune_GETURL");
        ptrAgentObj->UnregisterMethod("TestMgr_TSB_Play");
	/* E2E RF Video */
	ptrAgentObj->UnregisterMethod("TestMgr_RF_Video_ChannelChange");
	ptrAgentObj->UnregisterMethod("TestMgr_MDVR_GetResult");
#endif
	return TEST_SUCCESS;
}
/**************************************************************************
  Function Name : DestroyObject

Arguments     : Input argument is TDKIntegrationStub Object

Description   : This function will be used to destory the TDKIntegrationStub object.
 **************************************************************************/
extern "C" void DestroyObject(TDKIntegrationStub *agentobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying TDKIntegrationStub object\n");
	delete agentobj;
}

