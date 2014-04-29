/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
 * ============================================================================
 */

#include <fstream>
#include <iostream>
#include <json/json.h>
#include <rdktestagentintf.h>
#include "E2ELinearTV.h"
#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
using namespace std;

/*************************************************************************
Function name : E2ELinearTVStub constructor

Arguments     : NULL

**************************************************************************/
E2ELinearTVStub::E2ELinearTVStub()
{
	E2ELinearTVhandle=NULL;
}

/**************************************************************************
Function name : E2ELinearTVStub::initialize

Arguments     : IN const char*,IN RDKTestAgent

Description   : Register the callback function of LinearTVStub

***************************************************************************/

bool E2ELinearTVStub::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"E2ELinearTV Initialized");
	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&E2ELinearTVStub::E2ELinearTVstubGetURL,"TestMgr_E2ELinearTV_GetURL");
	ptrAgentObj->RegisterMethod(*this,&E2ELinearTVStub::E2ELinearTVstubPlayURL,"TestMgr_E2ELinearTV_PlayURL");
	ptrAgentObj->RegisterMethod(*this,&E2ELinearTVStub::E2ELinearTVstubT2pTuning,"TestMgr_E2ELinearTV_T2pTuning");
	ptrAgentObj->RegisterMethod(*this,&E2ELinearTVStub::E2ELinearTVstubT2pTrickplay,"TestMgr_E2ELinearTV_T2pTrickMode");
	return true;
}

/**************************************************************************
  Function name : E2ELinearTVStub::E2ELinearTVstubT2pTuning

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the T2pmsg for tuning to the Videoproxy and get the response in the T2ptuningresponse.txt
 ***************************************************************************/

bool E2ELinearTVStub::E2ELinearTVstubT2pTuning(IN const Json::Value& request, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_LOG,"\nE2ELinearTVStub::E2ELinearTVstubT2pTuning--Entry\n");
	// FILE *filepointer;
	string ocapid=""; 
	int errorResponse=0;
	ifstream fileInput;
	int sysRetValScript;
	string line;
	string searchPattern("OK");
	int respline =0;

	ocapid=(char*)request["ValidocapId"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nValid ocapid  from TestFramework : %s\n",request["ValidocapId"].asCString());

	std::string urlstringptr = "sh T2pTuning.sh " + ocapid +" > t2ptuneresponse.txt";
	sysRetValScript = system((char *)urlstringptr.c_str());

	if(sysRetValScript!=0 && sysRetValScript <=0)
	{

		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing T2pTuning.sh  \n");
		response["result"]="FAILURE";
		return false;
	}
	char cwd[1024];
	string syscwd;

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
		response["result"]="SUCCESS";
		//response["log-path"]=syscwd+"t2ptuneresponse.txt";
		response["log-path"]="t2ptuneresponse.txt";
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGeneric error not OK\n");

		response["result"]="FAILURE";
		//response["log-path"]=syscwd+"t2ptuneresponse.txt";
		response["log-path"]="t2ptuneresponse.txt";
		return false;

	}

	return true;
}

/**************************************************************************
Function name : E2ELinearTVStub::E2ELinearTVstubGetURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the URL to the Mediastreamer get the valid URL in the Json Response.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/

bool E2ELinearTVStub::E2ELinearTVstubGetURL(IN const Json::Value& request, OUT Json::Value& response)
{
	
     DEBUG_PRINT(DEBUG_LOG,"\nE2ELinearTVStub::E2ELinearTVstubcb--Entry\n");
	CURL *curl;
	CURLcode curlResponse;
	int errorResponse;
	FILE *filepointer;
	string url=""; 
	Json::Value root;
	url=(char*)request["Validurl"].asCString();
        
	
     DEBUG_PRINT(DEBUG_LOG,"\nValidurl form TestFramework : %s\n",request["Validurl"].asCString());
    
	curl = curl_easy_init();
    if(curl)
    {
                curl_easy_setopt(curl, CURLOPT_URL,(char *)url.c_str());
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
		return false;
	}

	curl_easy_cleanup(curl);

    std::ifstream file("jsonfile.json");
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

	}

	return true;

}

/**************************************************************************
Function name : E2ELinearTVStub::E2ELinearTVstubPlayURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Play the URL with the Mediaplayer.captured log is 
                return back to the TestFramework 
***************************************************************************/

bool E2ELinearTVStub::E2ELinearTVstubPlayURL(IN const Json::Value& request, OUT Json::Value& response)
{
      FILE *ErrorCheck;
      int status;
      int errorResponse=0;
      ifstream fileInput;
      int sysRetValScript;
      int offset;
      string line;
      char* searchPattern = (char *)"+";
      int curline =0;

      string validurl=request["videoStreamURL"].asString();
      DEBUG_PRINT(DEBUG_ERROR,"\nPLAY_URL   : %s \n",validurl.c_str());

	 std::string urlstringptr = "sh runmplayer_xi3.sh mplayer \""+ validurl +"\" l >mplayerlog.txt";
 
     
      DEBUG_PRINT(DEBUG_ERROR,"\nmplayerscript about to execute ..... URL : %s \n",urlstringptr.c_str());

      sysRetValScript = system((char *)urlstringptr.c_str());
      if(sysRetValScript!=0)
      {
             
             DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing mplayerscript \n");
             response["result"]="FAILURE";
             return false;
      }

      char cwd[1024];
      string syscwd;
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
		response["log-path"]="t2ptuneresponse.txt";

        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nURL is Not Played n");

                response["result"]="FAILURE";
                response["log-path"]="t2ptuneresponse.txt";
                return false;

        }
       

        return true;


}

/**************************************************************************
  Function name : E2ELinearTVStub::E2ELinearTVstubT2pTrickplay

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Changes the trick play rate and captures the log in /t2ptrickmoderesponse.txt and sends to the TestFramework. 
 ***************************************************************************/

bool E2ELinearTVStub::E2ELinearTVstubT2pTrickplay(IN const Json::Value& request, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nE2ELinearTVStub::E2ELinearTVstubT2pTrickplay--Entry\n");
	int errorResponse=0;
	ifstream fileInput;
	int sysRetValScript;
	string rate;
	string line;
	string searchPattern("OK");
	int respline =0;

	rate = request["trickPlayRate"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nValid trickPlayRate  from TestFramework : %f\n",request["trickPlayRate"].asCString());

	std::string urlstringptr = "sh T2pTrickMode.sh " + rate +" > t2ptrickmoderesponse.txt";
	sysRetValScript = system((char *)urlstringptr.c_str());

	if(sysRetValScript!=0 && sysRetValScript <=0)
	{

		DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing T2pTrickMode.sh \n");
		response["result"]="FAILURE";
		return false;
	}

	char cwd[1024];
	string syscwd;

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
				errorResponse=1;
			}

		}
		fileInput.close();
	}


	if(errorResponse)
	{
		response["result"]="SUCCESS";
		//response["log-path"]=syscwd+"t2ptrickmoderesponse.txt";
		response["log-path"]="t2ptrickmoderesponse.txt";
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nGeneric error not OK\n");

		response["result"]="FAILURE";
		//response["log-path"]=syscwd+"t2ptrickmoderesponse.txt";
		response["log-path"]="t2ptrickmoderesponse.txt";
		return false;
	}

	return true;
}

/**************************************************************************
  Function name : E2ELinearTVStub::CreateObject()

Arguments     : NULL

Description   : create the object of E2ELinearTVStub  
***************************************************************************/
extern "C" E2ELinearTVStub* CreateObject()
{
	return new E2ELinearTVStub();
}

/**************************************************************************
Function name : E2ELinearTVStub::cleanup()

Arguments     : NULL

Description   :close things cleanly  
***************************************************************************/
bool E2ELinearTVStub::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	/* All done, close things cleanly */
	DEBUG_PRINT(DEBUG_LOG,"\n E2ELinearTVStub shutting down ");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_GetURL");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_PlayURL");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_T2pTuning");
	ptrAgentObj->UnregisterMethod("TestMgr_E2ELinearTV_T2pTrickMode");

	return true;
}
