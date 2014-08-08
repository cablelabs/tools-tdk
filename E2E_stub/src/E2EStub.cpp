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

#include <fstream>
#include <iostream>
#include <json/json.h>
#include <rdktestagentintf.h>
#include "E2EStub.h"
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
Function name: E2EStub constructor

Arguments    : NULL

 **************************************************************************/
E2EStub::E2EStub()
{
	E2EStubhandle=NULL;
}

/**************************************************************************
Function name : E2EStub::initialize

Arguments     : IN const char*,IN RDKTestAgent

Description   : Register the callback function of E2EStub

***************************************************************************/

bool E2EStub::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	
     DEBUG_PRINT(DEBUG_LOG,"E2EStub Initialized");

	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&E2EStub::E2EStubGetURL,"TestMgr_E2EStub_GetURL");
	ptrAgentObj->RegisterMethod(*this,&E2EStub::E2EStubPlayURL,"TestMgr_E2EStub_PlayURL");
     ptrAgentObj->RegisterMethod(*this,&E2EStub::E2EStubGetRecURLS,"TestMgr_E2EStub_GetRecURLS");

	return true;
}

/**************************************************************************
Function name : E2EStub::E2EStubGetRecURLS

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Receving the Requesturl from Test Manager and sends the URL to the Mediastreamer to get the 
                Recorded Url List. 
                Returns the FilePath of Recorded Urls List captured 
***************************************************************************/


bool E2EStub::E2EStubGetRecURLS(IN const Json::Value& request, OUT Json::Value& response)
{
        FILE *ErrorCheck;
        int sysRetValCurl,sysRetValScript;
        std::string recordedurl=request["RecordURL"].asString();
        std::string ptr = "curl " + recordedurl +" >recordedlist.txt";
        
        DEBUG_PRINT(DEBUG_ERROR,"\nRecorded URL Received from Test framework : %s \n",ptr.c_str());


        sysRetValCurl=system((char *)ptr.c_str());
        

        if(sysRetValCurl!=0)
        {
             
             DEBUG_PRINT(DEBUG_ERROR,"\n system command is failed on executing Curl  \n");
             response["result"]="FAILURE";
             return false;
	}
        sysRetValScript=system("source recordedurlscript.sh >Recordedlistmod.txt");
        if(sysRetValScript!=0) 
        {
             
             DEBUG_PRINT(DEBUG_ERROR,"\n system command is failed on executing script \n");
             response["result"]="FAILURE";
             return false;
        }
        char cwd[1024];
        string syscwd;
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
             return false;
	}

        return true;
}


/**************************************************************************
Function name : E2EStub::E2EStubGetURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Receving the Validurl from Test Manager and sends the URL to the Mediastreamer to get the 
		Json Response. 
                Return the Error code,Error Description and VideoStreamingURL to the Test Manager
***************************************************************************/

bool E2EStub::E2EStubGetURL(IN const Json::Value& request, OUT Json::Value& response)
{
	CURL *curl;
	CURLcode curlResponse;
	int errorResponse;
	FILE *fp;
	string url=""; 
	Json::Value root;
	url=(char*)request["Validurl"].asCString();

	
      DEBUG_PRINT(DEBUG_ERROR,"\n URL from TestFrameWork : %s\n",url.c_str());
	curl = curl_easy_init();
	if(curl)
	{
		curl_easy_setopt(curl, CURLOPT_URL,(char *)url.c_str());
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

		//write in to a file 
		fp=fopen("jfile.json","wb");
		curl_easy_setopt( curl, CURLOPT_WRITEDATA, fp ) ;
		curlResponse= curl_easy_perform(curl);
		printf("The curlResponse value %d\n",curlResponse);
		fclose(fp);
	}

	if(curlResponse != CURLE_OK)
	{
		fprintf(stderr, "curl_easy_perform() failed: %s \n",curl_easy_strerror(curlResponse));
		response["result"]="FAILURE";
        curl_easy_cleanup(curl);
	
		return false;
	}

	curl_easy_cleanup(curl);

	std::ifstream file("jfile.json");
	file>>root;
	errorResponse=root["errorCode"].asInt();

	response["details"]=root["videoStreamingURL"].asString();

     DEBUG_PRINT(DEBUG_ERROR,"\nJSON Response from MediaStreamer :-\n");
     DEBUG_PRINT(DEBUG_ERROR,"\nErrorCode         : %d\n",root["errorCode"].asInt());
     DEBUG_PRINT(DEBUG_ERROR,"\nErrorDescription  : %s \n",root["errorDescription"].asCString());
     DEBUG_PRINT(DEBUG_ERROR,"\nVideoStreamingURL : %s\n",root["videoStreamingURL"].asCString());
    

	
	if(!errorResponse)
	{
		response["result"]="SUCCESS";
	}
	else
	{

		response["result"]="FAILURE";

	}

	return true;

}
/**************************************************************************
Function name : E2EStub::E2EStubPlayURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Play the URL with the Mediaplayer.captured log is 
		return back to the TestFramework 
****************************************************************************/

bool E2EStub::E2EStubPlayURL(IN const Json::Value& request, OUT Json::Value& response)
{
	
	int status;
	int errorResponse=0;
    int sysRetValScript;
	string validurl=request["videoStreamURL"].asString();
	
    DEBUG_PRINT(DEBUG_ERROR,"\nPLAY_URL   : %s \n",validurl.c_str());

    std::string urlstringptr = "source mplayerscript.sh \"" + validurl +"\" l ";
	           
   
    DEBUG_PRINT(DEBUG_ERROR,"\nmplayerscript about to execute ..... URL : %s \n",urlstringptr.c_str());


    sysRetValScript = system((char *)urlstringptr.c_str());
    if(sysRetValScript!=0)
    {
         
         DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on executing mplayerscript \n");

         response["result"]="FAILURE";
         return false;
    }
    
    sysRetValScript = system("cat e2emplayerlog.txt >> e2emplayerappend.txt");
    if(sysRetValScript!=0)
    {
         
         DEBUG_PRINT(DEBUG_ERROR,"\nsystem command is failed on appending mplayer log \n");

         response["result"]="FAILURE";
         return false;
    }

	ifstream fileInput;
	int offset;
	string line;
	char* playPattern =(char *)"+"; 
	int curline =0;

	// open file to playPattern
	fileInput.open("e2emplayerlog.txt");
	if(fileInput.is_open()) 
	{
		while(getline(fileInput, line)) 
		{ 
			curline++;
			if (line.find(playPattern, 0) != string::npos) 
			{
				
                     DEBUG_PRINT(DEBUG_ERROR,"\nURL is Playing found:+++\n");

				errorResponse=1;
			}
     
		}
        fileInput.close();
	}
    else
    {
         DEBUG_PRINT(DEBUG_ERROR,"\ne2emplayerlog.txt is not found\n");

         response["result"]="FAILURE";
               
    }
    char cwd[1024];
      string syscwd;
     if(getcwd(cwd, sizeof(cwd))==NULL)
     {
         
         DEBUG_PRINT(DEBUG_ERROR,"\nGetcwd returns NULL\n");

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

	
	if(errorResponse)
	{
		response["result"]="SUCCESS";
		
	}
	else
	{
		response["result"]="FAILURE";

	}
    response["log-path"]=syscwd+"e2emplayerappend.txt";
	return true;


}

/**************************************************************************
Function name : E2EStub::CreateObject()

Arguments     : NULL

Description   : create the object of E2EStub  
 ***************************************************************************/
extern "C" E2EStub* CreateObject()
{
	return new E2EStub();
}

/**************************************************************************
Function name : E2EStub::cleanup()

Arguments     : NULL

Description   :close things cleanly  
 ***************************************************************************/
bool E2EStub::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	
       /* All done, close things cleanly */
        DEBUG_PRINT(DEBUG_LOG,"\n E2EStub-DVR TrickPlay shutting down ");
       ptrAgentObj->UnregisterMethod("TestMgr_E2EStub_GetURL");
       ptrAgentObj->UnregisterMethod("TestMgr_E2EStub_PlayURL");
       ptrAgentObj->UnregisterMethod("TestMgr_E2EStub_GetRecURLS");

	return true;
}
