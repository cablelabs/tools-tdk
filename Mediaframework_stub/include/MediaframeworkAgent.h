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

#ifndef __MEDIAFRAMEWORK_STUB_H__
#define __MEDIAFRAMEWORK_STUB_H__
#include <json/json.h>
#include <iostream>
#include <unistd.h>
#include <sstream>
#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <signal.h>
#include <wait.h>
#include <ifaddrs.h>
#include <arpa/inet.h>

#include <fstream>
#include <string.h>

#include <glib.h>
#include <iostream>
#include <termios.h>

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#include "mediaplayersink.h"
#include "hnsource.h"
#include "DVRSource.h" 
#include "DVRSink.h" 
#include "hnsink.h"
#include "dvrmanager.h"
#include "rmf_osal_init.h"

#include "rmfqamsrc.h"
#include "rmf_platform.h"

#define BUFFER_LENGTH 64
#define CMD "cat /etc/rmfconfig.ini | grep \"QAMSRC.FACTORY.ENABLED\" | cut -d \"=\" -f 2"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

/*DVR source*/
#define BEGIN_TIME 0.0
#define X_VALUE 0 
#define Y_VALUE 0
#define WIDTH 1280
#define HEIGHT 720

/*DVR sink*/
#define REC_DURATION    30*60*1000
#define PRIORITY        "P3"
#define TITLE_LEN	40

#define RECORD_DETAILS_TXT "recordDetails.txt"
#define PRE_REQUISITE_LOG_PATH "logs/Mediaframework_testmodule_prereq_details.log"
#define PRE_REQUISITE_FILE "scripts/mediaframework_test_module_pre-script.sh"
#define POST_REQUISITE_LOG_PATH "logs/Mediaframework_testmodule_postreq_details.log"
#define POST_REQUISITE_FILE "scripts/mediaframework_test_module_post-script.sh"
#define QAM_PRE_REQUISITE_FILE "scripts/mediaframework_qamsrc_test_module_pre-script.sh"
#define QAM_PRE_REQUISITE_LOG_PATH "logs/Mediaframework_qamsrc_testmodule_postreq_details.log"

using namespace std;

string g_tdkPath = getenv("TDK_PATH");

class RDKTestAgent;
class MediaframeworkAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                MediaframeworkAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();	
		
		/*Optimised Code */
#if 1
		bool MediaframeworkAgent_RmfElementCreateInstance(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementRemoveInstance(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementInit(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementTerm(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementOpen(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementClose(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementPlay(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementPause(IN const Json::Value& req, OUT Json::Value& response);

		bool MediaframeworkAgent_RmfElement_SinkSetSource(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle(IN const Json::Value& req, OUT Json::Value& response);

		bool MediaframeworkAgent_RmfElementSetSpeed(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementGetSpeed(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementSetMediaTime(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElementGetMediaTime(IN const Json::Value& req, OUT Json::Value& response);	
		bool MediaframeworkAgent_RmfElementGetMediaInfo(IN const Json::Value& req, OUT Json::Value& response);	
		bool MediaframeworkAgent_RmfElementGetState(IN const Json::Value& req, OUT Json::Value& response);

		bool MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_GetTSID(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI(IN const Json::Value& req, OUT Json::Value& response);
		
		bool MediaframeworkAgent_RmfElement_HNSink_InitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_HNSink_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_HNSink_SetProperties(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_RmfElement_HNSink_SetSourceType(IN const Json::Value& req, OUT Json::Value& response);
		
#endif

                //Mediaframework Wrapper functions
                bool MediaframeworkAgent_MPSink_SetGetMute(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_MPSink_SetGetVolume(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_HNSrc_GetBufferedRanges(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_HNSrcMPSink_Video_State(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_HNSrcMPSink_Video_Volume(IN const Json::Value& req, OUT Json::Value& response);
	
		/*DVR Recording List*/
		bool MediaframeworkAgent_DVR_Rec_List(IN const Json::Value& req, OUT Json::Value& response);
		
		/*DVR sink*/
        	bool MediaframeworkAgent_DVRSink_InitTerm(IN const Json::Value& req, OUT Json::Value& response);

                /*DVR Manager*/
                bool MediaframeworkAgent_DVRManager_GetSpace(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_DVRManager_GetRecordingCount(IN const Json::Value& req, OUT Json::Value& response);
                bool MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex(const Json::Value&, Json::Value&);
		bool MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetRecordingInfoById(const Json::Value&, Json::Value&);
		bool MediaframeworkAgent_DVRManager_CheckRecordingInfoById(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetIsRecordingInProgress(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetRecordingSize(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetRecordingDuration(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetRecordingStartTime(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_CreateTSB(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_ConvertTSBToRecording(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_CreateRecording(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_UpdateRecording(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_DeleteRecording(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetSegmentsCount(const Json::Value&, Json::Value&);
                bool MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex(const Json::Value&, Json::Value&);

};
        extern "C" MediaframeworkAgent* CreateObject();

#endif //__MEDIAFRAMEWORK_STUB_H__

