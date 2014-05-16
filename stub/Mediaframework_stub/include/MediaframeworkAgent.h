/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
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
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <signal.h>
#include <wait.h>

#include <fstream>
#include <string.h>

using namespace std;

#include <glib.h>
#include <iostream>
#include <termios.h>

#include "mediaplayersink.h"
#include "hnsource.h"
#include "DVRSource.h" 
#include "DVRSink.h" 
#include "dvrmanager.h"
#include "rmf_osal_init.h"

#include "rmfqamsrc.h"
#include "rmf_platform.h"

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
using namespace std;


class RDKTestAgent;
class MediaframeworkAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                MediaframeworkAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
		
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

		/*QAM Source*/
		bool MediaframeworkAgent_QAMSource_InitTerm(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_OpenClose(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_Play(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_Pause(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_GetTsId(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_GetLtsId(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_Init_Uninit_Platform(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_GetUseFactoryMethods(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_GetQAMSourceInstance(IN const Json::Value& req, OUT Json::Value& response);
		bool MediaframeworkAgent_QAMSource_ChangeURI(IN const Json::Value& req, OUT Json::Value& response);
		
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

