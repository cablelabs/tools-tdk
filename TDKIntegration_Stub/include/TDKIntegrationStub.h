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
#include <stdlib.h>
#include <sys/time.h>
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

#include <ifaddrs.h>
#include <arpa/inet.h>

#ifdef RMFAGENT
#include "mediaplayersink.h"
#include "rmfbase.h"
#include "hnsource.h"
#include "rmfqamsrc.h"
#include "rmf_platform.h"
//#include "benchmark.h"
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
//class TDKIntegrationStub : public RDKTestStubInterface
class TDKIntegrationStub : public RDKTestStubInterface , public AbstractServer<TDKIntegrationStub>
{
	public:
		TDKIntegrationStub(TcpSocketServer &ptrRpcServer) : AbstractServer <TDKIntegrationStub>(ptrRpcServer)
                {
#ifdef HYBRID
#ifdef RDK_BR_1DOT3
        	  /*Register stub function for callback*/
                  this->bindAndAddMethod(Procedure("TestMgr_HybridE2E_T2pTuning", PARAMS_BY_NAME,JSON_STRING, "ValidocapId",JSON_STRING, NULL), &TDKIntegrationStub::TDKIntegrationT2pTuning);
                  this->bindAndAddMethod(Procedure("TestMgr_HybridE2E_T2pTrickMode", PARAMS_BY_NAME,JSON_STRING, "trickPlayRate",JSON_STRING, NULL), &TDKIntegrationStub::TDKIntegrationT2pTrickplay);
#endif
#endif
#ifdef IPCLIENT
	          /*Dvr stub wrapper functions*/
                  this->bindAndAddMethod(Procedure("TestMgr_E2EStub_PlayURL", PARAMS_BY_NAME,JSON_STRING, "videoStreamURL",JSON_STRING, NULL), &TDKIntegrationStub::E2EStubPlayURL);
                  this->bindAndAddMethod(Procedure("TestMgr_E2EStub_GetRecURLS", PARAMS_BY_NAME,JSON_STRING, "RecordURL",JSON_STRING, NULL), &TDKIntegrationStub::E2EStubGetRecURLS);
	          /*LinearTV wrapper functions*/
                  this->bindAndAddMethod(Procedure("TestMgr_E2ELinearTV_GetURL", PARAMS_BY_NAME,JSON_STRING, "Validurl",JSON_STRING, NULL), &TDKIntegrationStub::E2ELinearTVstubGetURL);
                  this->bindAndAddMethod(Procedure("TestMgr_E2ELinearTV_PlayURL", PARAMS_BY_NAME,JSON_STRING, "videoStreamURL",JSON_STRING, NULL), &TDKIntegrationStub::E2ELinearTVstubPlayURL);
#endif
		  /* E2E DVR TrickPlay */
                  this->bindAndAddMethod(Procedure("TestMgr_LinearTv_Dvr_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_LinearTv_Dvr_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_LinearTv_AudioChannel_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_LinearTv_AudioChannel_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Pause_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Pause_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_TrickPlay_FF_FR", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_FF_FR);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause_Play_Repeat", PARAMS_BY_NAME,JSON_STRING, "rCount",JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_Repeat);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "rewindSpeed",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Forward_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "seconds", JSON_REAL, "rCount",JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Forward_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Forward_From_Middle", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "seconds", JSON_REAL, "rCount",JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_Middle);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Forward_From_End", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "seconds",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Forward_From_End);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Backward_From_End", PARAMS_BY_NAME,JSON_STRING, "playUrl", JSON_STRING, "seconds", JSON_REAL, "rCount", JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_End);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Backward_From_Middle", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "seconds",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Middle);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Skip_Backward_From_Starting", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "seconds", JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Skip_Backward_From_Starting);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Rewind_Forward", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "rewindSpeed", JSON_REAL, "forwardSpeed",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Rewind_Forward);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Forward_Rewind", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "rewindSpeed", JSON_REAL, "forwardSpeed",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Forward_Rewind);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_FF_FR_Pause_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "trickPlayRate", JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_Pause_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause_FF_FR", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "trickPlayRate",JSON_REAL, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause_FF_FR);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause_Play_SF_SB", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "sfSeconds", JSON_REAL, "sbSeconds",JSON_REAL, "rCount",JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause_Play_SF_SB);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_FF_FR_SF_SB", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, "rewindSpeed", JSON_REAL, "forwardSpeed",JSON_REAL, "sfSeconds",JSON_REAL, "sbSeconds",JSON_REAL, "rCount",JSON_INTEGER, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_FF_FR_SF_SB);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Pause_Pause", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Pause_Pause);
                  this->bindAndAddMethod(Procedure("TestMgr_Dvr_Play_Play", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_Play_Play);
                  this->bindAndAddMethod(Procedure("TestMgr_LiveTune_GETURL", PARAMS_BY_NAME,JSON_STRING, "Validurl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_GETURL);
		  /*E2E_RMF_TSB*/
		  this->bindAndAddMethod(Procedure("TestMgr_TSB_Play", PARAMS_BY_NAME,JSON_STRING, "SpeedRate",JSON_REAL, "VideostreamURL",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFTSB_Play); 
	          /* E2E RF Video */
                  this->bindAndAddMethod(Procedure("TestMgr_RF_Video_ChannelChange", PARAMS_BY_NAME,JSON_STRING, "playUrl",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_ChannelChange);
                  this->bindAndAddMethod(Procedure("TestMgr_MDVR_GetResult", PARAMS_BY_NAME,JSON_STRING, "resultList",JSON_STRING, NULL), &TDKIntegrationStub::E2ERMFAgent_MDVR_GetResult);
                }

		/*Ctor*/
		//TDKIntegrationStub();

		/*inherited functions*/
		bool initialize(IN const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		bool cleanup(IN const char* szVersion);

		/*LiveTrickplay Wrapper functions*/
#ifdef HYBRID
#ifdef RDK_BR_1DOT3
		void TDKIntegrationT2pTuning(IN const Json::Value& request, OUT Json::Value& response);
		void TDKIntegrationT2pTrickplay(IN const Json::Value& request, OUT Json::Value& response);
#endif
#endif
		/*1DOT3 DVR Testing Wrapper functions*/
#ifdef IPCLIENT
		void E2EStubPlayURL(IN const Json::Value& request, OUT Json::Value& response);
		void E2EStubGetRecURLS(IN const Json::Value& request, OUT Json::Value& response);
		void E2ELinearTVstubGetURL(IN const Json::Value& req, OUT Json::Value& response);
		void E2ELinearTVstubPlayURL(IN const Json::Value& req, OUT Json::Value& response);
#endif	
#ifdef RMFAGENT
		/*E2ERMFAgent Wrapper functions*/
		/* E2E DVR TrickPlay */
		void E2ERMFAgent_LinearTv_Dvr_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_LinearTv_AudioChannel_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_TrickPlay_FF_FR(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause_Play_Repeat(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Forward_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Forward_From_Middle(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Forward_From_End(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Backward_From_End(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Backward_From_Middle(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Skip_Backward_From_Starting(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Rewind_Forward(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Forward_Rewind(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_FF_FR_Pause_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause_FF_FR(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause_Play_SF_SB(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_FF_FR_SF_SB(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Pause_Pause(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_Play_Play(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFAgent_GETURL(IN const Json::Value& , OUT Json::Value& );
		void E2ERMFTSB_Play(IN const Json::Value& , OUT Json::Value& );
		/* E2E RF Video */
		void E2ERMFAgent_ChannelChange(IN const Json::Value& , OUT Json::Value&);
		void E2ERMFAgent_MDVR_GetResult(IN const Json::Value& , OUT Json::Value&);

#endif	

};
//to resolve Time issue ###Need to revisit
class Time
{
        public:
          int getTime(struct timeval *);
          float ExecutionTime(int rb, struct timeval *, int ra, struct timeval * );
};
#endif //__TDKIntegrationStub
