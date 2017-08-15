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

#ifndef __TDKIntegration_STUB_H__
#define __TDKIntegration_STUB_H__

#include <json/json.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fstream>
#include <iostream>
#include "rdkteststubintf.h"
#include <rdktestagentintf.h>
#include <string.h>
#include <sstream>
#include <malloc.h>
#include <fstream>
#include <stdlib.h>
#include <curl/curl.h>

#include <ifaddrs.h>
#include <arpa/inet.h>

#ifdef RMFAGENT
#include "mediaplayersink.h"
#include "rmfbase.h"
#include "hnsource.h"
#include "rmfqamsrc.h"
#include "rmf_platform.h"
#include "benchmark.h"
#endif

#define SKIP_FORWARD 0
#define SKIP_BACKWARD 1
#define BUFFER_LENGTH 64
#define NOT_PRESENT -1

#define CMD_LENGTH 180
#define CMD "cat /proc/video_status | grep started: | cut -d ' ' -f 14 | sed 2d"

#define X_VALUE 0
#define Y_VALUE 0
#define WIDTH 1280
#define HEIGHT 720


#define IN
#define OUT
#define CMAF_MAX_NAME_LEN 64

#define TEST_SUCCESS true
#define TEST_FAILURE false 
#define JSON_PARSER_LOG_PATH "output_json_parser_details.log"
#define JSON_PARSER_SCRIPT "output_json_parser.sh"
using namespace std;
#define NUMBER_OCAPID 10

class RDKTestAgent;
class TDKIntegrationStub : public RDKTestStubInterface
{
	public:

		/*Ctor*/
		TDKIntegrationStub();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*LiveTrickplay Wrapper functions*/
#ifdef HYBRID
#ifdef RDK_BR_1DOT3
		bool TDKIntegrationT2pTuning(IN const Json::Value& request, OUT Json::Value& response);
		bool TDKIntegrationT2pTrickplay(IN const Json::Value& request, OUT Json::Value& response);
#endif
#endif
		/*1DOT3 DVR Testing Wrapper functions*/
#ifdef IPCLIENT
		bool E2EStubPlayURL(IN const Json::Value& request, OUT Json::Value& response);
		bool E2EStubGetRecURLS(IN const Json::Value& request, OUT Json::Value& response);
		bool E2ELinearTVstubGetURL(IN const Json::Value& req, OUT Json::Value& response);
		bool E2ELinearTVstubPlayURL(IN const Json::Value& req, OUT Json::Value& response);
#endif	
#ifdef RMFAGENT
		/*E2ERMFAgent Wrapper functions*/
		/* E2E DVR TrickPlay */
		bool E2ERMFAgent_LinearTv_Dvr_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_LinearTv_AudioChannel_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_TrickPlay_FF_FR(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause_Play_Repeat(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Forward_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Forward_From_Middle(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Forward_From_End(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Backward_From_End(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Backward_From_Middle(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Skip_Backward_From_Starting(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Rewind_Forward(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Forward_Rewind(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_FF_FR_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause_FF_FR(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause_Play_SF_SB(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_FF_FR_SF_SB(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Pause_Pause(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_Play_Play(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFAgent_GETURL(IN const Json::Value& , OUT Json::Value& );
		bool E2ERMFTSB_Play(IN const Json::Value& , OUT Json::Value& );
		/* E2E RF Video */
		bool E2ERMFAgent_ChannelChange(IN const Json::Value& , OUT Json::Value&);
		bool E2ERMFAgent_MDVR_GetResult(IN const Json::Value& , OUT Json::Value&);

#endif	

};

#endif //__TDKIntegrationStub
