/*

* ============================================================================

* COMCAST CONFIDENTIAL AND PROPRIETARY

* ============================================================================

* This file and its contents are the intellectual property of Comcast.  It may

* not be used, copied, distributed or otherwise  disclosed in whole or in part

* without the express written permission of Comcast.

* ============================================================================

* Copyright (c) 2013 Comcast. All rights reserved.

* ============================================================================*/

#ifndef __E2E_RMF_STUB_H__
#define __E2E_RMF_STUB_H__
#include <json/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include <string.h>
#include <string>
#include <unistd.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <iostream>
#include <cstring>
#include "mediaplayersink.h"
#include "hnsource.h"
#include "benchmark.h"
#include <curl/curl.h>
#include <malloc.h>
#include <fstream>

#include <ifaddrs.h>
#include <arpa/inet.h>

using namespace std;

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

#define TEST_SUCCESS true
#define TEST_FAILURE false

class RDKTestAgent;
class E2ERMFAgent : public RDKTestStubInterface
{
	public:
		/*Constructor*/
		E2ERMFAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

		/*E2ERMFAgent Wrapper functions*/
		/* E2E DVR TrickPlay */
		bool E2ERMFAgent_LinearTv_Dvr_Play(IN const Json::Value& , OUT Json::Value& );
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
	
		/* E2E RF Video */	
		bool E2ERMFAgent_ChannelChange(IN const Json::Value& , OUT Json::Value&);
};

extern "C" E2ERMFAgent* CreateObject();

#endif //__E2E_RMF_Stub_H__

