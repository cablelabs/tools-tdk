/*
* ============================================================================
* RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file (and its contents) are the intellectual property of RDK Management, LLC.
* It may not be used, copied, distributed or otherwise  disclosed in whole or in
* part without the express written permission of RDK Management, LLC.
* ============================================================================
* Copyright (c) 2016 RDK Management, LLC. All rights reserved.
* ============================================================================
*/

#ifndef __MEDIASTREAMER_STUB_H__
#define __MEDIASTREAMER_STUB_H__
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <curl/curl.h>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#ifdef RDK_BR_2DOT0
#include "mediaplayersink.h"
#include "hnsource.h"
#include "rmfqamsrc.h"
#include "rmf_platform.h"
#endif

#include <exception>

#define IN
#define OUT
#define CMAF_MAX_NAME_LEN 64
#define PRE_REQUISITE_LOG_PATH "logs/Mediastreamer_testmodule_prereq_details.log"
#define PRE_REQUISITE_FILE "scripts/mediastreamer_test_module_pre-script.sh"

#define TEST_SUCCESS true
#define TEST_FAILURE false 

using namespace std;
#define NUMBER_OCAPID 10

class RDKTestAgent;
class MediaStreamerAgent : public RDKTestStubInterface , public AbstractServer<MediaStreamerAgent>
{
	public:

	        MediaStreamerAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <MediaStreamerAgent>(ptrRpcServer)
	        {
		   #ifdef RDK_BR_1DOT3
        	   this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_LiveTune_Request", PARAMS_BY_NAME, JSON_STRING,"ocapId",JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_LiveTune_Request);
	           this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_Recording_Request", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_Recording_Request);
	           this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_Recorded_Urls", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_Recorded_Urls);
        	   this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_Recorded_Metadata", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_Recorded_Metadata);

        	   this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_Live_Playback", PARAMS_BY_NAME, JSON_STRING,"ocapId",JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_Live_Playback);
	           this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_Recording_Playback", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_Recording_Playback);
	           this->bindAndAddMethod(Procedure("TestMgr_MediaStreamer_DVR_Trickplay", PARAMS_BY_NAME, JSON_STRING,"PlaySpeed",JSON_STRING,"timePosition",JSON_STRING,NULL), &MediaStreamerAgent::MediaStreamerAgent_DVR_Trickplay);
		   #endif

		   #ifdef RDK_BR_2DOT0
        	  
		   this->bindAndAddMethod(Procedure("TestMgr_RMFStreamer_InterfaceTesting", PARAMS_BY_NAME, JSON_STRING,"URL",JSON_STRING,NULL), &MediaStreamerAgent::RMFStreamerAgent_InterfaceTesting); 
        	   this->bindAndAddMethod(Procedure("TestMgr_RMFStreamer_Player", PARAMS_BY_NAME, JSON_STRING,"play_time", JSON_INTEGER,"VideostreamURL",JSON_STRING,NULL), &MediaStreamerAgent::RMFStreamerAgent_Player);
		   #endif
        	}

		void* MediaStreamerAgenthandle;

		/*Constuctor*/
		MediaStreamerAgent();

		// Declaring enum type Mode for framing requested URL
		enum Mode
		{             
			LIVE_TUNE_REQUEST = 0,    //for Live tune request
			RECORDING_REQUEST,        //for Recording request
			RECORDING_URL_LIST,       //for recording url list
			RECORDING_URL_METADATA    //for recording metadata			   
		};
		/*inherited functions*/
		bool initialize(IN const char* szVersion);		
		bool cleanup(IN const char* szVersion);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

		/*MediaStreamerAgent Wrapper functions*/
		#ifdef RDK_BR_1DOT3
	        void MediaStreamerAgent_LiveTune_Request(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_Recording_Request(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_Recorded_Urls(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_Recorded_Metadata(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_Live_Playback(IN const Json::Value& request, OUT Json::Value& response);	
		void MediaStreamerAgent_Recording_Playback(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_Live_Trickplay(IN const Json::Value& request, OUT Json::Value& response);
		void MediaStreamerAgent_DVR_Trickplay(IN const Json::Value& request, OUT Json::Value& response);
		#endif

		#ifdef RDK_BR_2DOT0
		void RMFStreamerAgent_InterfaceTesting(IN const Json::Value& request, OUT Json::Value& response);
		void RMFStreamerAgent_Player(IN const Json::Value& request, OUT Json::Value& response);
		#endif
		
		
	private:
	
		string curlRequest(Mode mode, string id);
		string curlRequest(Mode mode);
		string getRandomRecId();		
		string playRequest(string playurl, bool trickplay);
		string getRecorderId();
		string frameURL(enum Mode, string Id);
		string frameURL(enum Mode);		
		string frameURL(string playurl, string play_speed, string time_position);
};

//	extern "C" MediaStreamerAgent* CreateObject();

#endif //__MEDIASTREAMER_Stub
