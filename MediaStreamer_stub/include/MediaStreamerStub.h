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

#define TEST_SUCCESS true
#define TEST_FAILURE false 

using namespace std;
#define NUMBER_OCAPID 10

class RDKTestAgent;
class MediaStreamerAgent : public RDKTestStubInterface
{
	public:
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
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);		
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

		/*MediaStreamerAgent Wrapper functions*/
	        bool MediaStreamerAgent_LiveTune_Request(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_Recording_Request(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_Recorded_Urls(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_Recorded_Metadata(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_Live_Playback(IN const Json::Value& request, OUT Json::Value& response);	
		bool MediaStreamerAgent_Recording_Playback(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_Live_Trickplay(IN const Json::Value& request, OUT Json::Value& response);
		bool MediaStreamerAgent_DVR_Trickplay(IN const Json::Value& request, OUT Json::Value& response);
#ifdef RDK_BR_2DOT0
		bool RMFStreamerAgent_InterfaceTesting(IN const Json::Value& request, OUT Json::Value& response);
		bool RMFStreamerAgent_Player(IN const Json::Value& request, OUT Json::Value& response);
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

	extern "C" MediaStreamerAgent* CreateObject();

#endif //__MEDIASTREAMER_Stub
