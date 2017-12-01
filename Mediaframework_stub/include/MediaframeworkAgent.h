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
#include "hnsink.h"
#ifndef SINGLE_TUNER_IP_CLIENT
#include "DVRSource.h" 
#include "DVRSink.h" 
#include "dvrmanager.h"
#endif
#include "rmf_osal_init.h"
#include "rmfqamsrc.h"
#include "rmf_platform.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

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
#define REC_DURATION    60
#define PRIORITY        "P3"
#define TITLE_LEN	40

#define RECORD_DETAILS_TXT "recordDetails.txt"
#define PRE_REQUISITE_LOG_PATH "logs/Mediaframework_testmodule_prereq_details.log"
#define PRE_REQUISITE_FILE "scripts/mediaframework_test_module_pre-script.sh"
#define POST_REQUISITE_LOG_PATH "logs/Mediaframework_testmodule_postreq_details.log"
#define POST_REQUISITE_FILE "scripts/mediaframework_test_module_post-script.sh"
#define QAM_PRE_REQUISITE_FILE "scripts/mediaframework_qamsrc_test_module_pre-script.sh"
#define QAM_PRE_REQUISITE_LOG_PATH "logs/Mediaframework_qamsrc_testmodule_postreq_details.log"
/*
 Fetching Streaming Interface Name
 */
#define STREAMING_INTERFACE "Streaming Interface"
#define FETCH_STREAMING_INT_FILE "streaming_interface_file"

using namespace std;

string g_tdkPath = getenv("TDK_PATH");

class RDKTestAgent;
class MediaframeworkAgent : public RDKTestStubInterface , public AbstractServer<MediaframeworkAgent>
{
        public:
        MediaframeworkAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <MediaframeworkAgent>(ptrRpcServer)
        {
           this->bindAndAddMethod(Procedure("TestMgr_MPSink_SetGetMute", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute);
           this->bindAndAddMethod(Procedure("TestMgr_MPSink_SetGetVolume", PARAMS_BY_NAME, JSON_STRING,"Volume",JSON_REAL,NULL), &MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume);
           this->bindAndAddMethod(Procedure("TestMgr_HNSrc_GetBufferedRanges", PARAMS_BY_NAME, JSON_STRING,"X",JSON_INTEGER,"Y",JSON_INTEGER,"H",JSON_INTEGER,"W",JSON_INTEGER,"apply",JSON_INTEGER,"playuri",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges);
           this->bindAndAddMethod(Procedure("TestMgr_HNSrcMPSink_Video_State", PARAMS_BY_NAME, JSON_STRING,"X",JSON_INTEGER,"Y",JSON_INTEGER,"H",JSON_INTEGER,"W",JSON_INTEGER,"apply",JSON_INTEGER,"playuri",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State);
           this->bindAndAddMethod(Procedure("TestMgr_HNSrcMPSink_Video_MuteUnmute", PARAMS_BY_NAME, JSON_STRING,"X",JSON_INTEGER,"Y",JSON_INTEGER,"H",JSON_INTEGER,"W",JSON_INTEGER,"apply",JSON_INTEGER,"playuri",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute);
           this->bindAndAddMethod(Procedure("TestMgr_HNSrcMPSink_Video_Volume", PARAMS_BY_NAME, JSON_STRING,"Volume",JSON_REAL,"X",JSON_INTEGER,"Y",JSON_INTEGER,"H",JSON_INTEGER,"W",JSON_INTEGER,"apply",JSON_INTEGER,"playuri",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume);
	
	#ifndef SINGLE_TUNER_IP_CLIENT
        /*DVR Recording List*/

           this->bindAndAddMethod(Procedure("TestMgr_DVR_Rec_List", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List);
           this->bindAndAddMethod(Procedure("TestMgr_DVR_CreateNewRecording", PARAMS_BY_NAME, JSON_STRING,"recordId",JSON_STRING,"recordDuration",JSON_STRING,"recordTitle",JSON_STRING,"ocapId",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVR_CreateNewRecording);

	/*DVR sink*/
           this->bindAndAddMethod(Procedure("TestMgr_DVRSink_init_term", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm);
	/*DVR Manager*/
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetSpace", PARAMS_BY_NAME ,JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace);

           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingCount", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingInfoByIndex", PARAMS_BY_NAME, JSON_STRING,"index",JSON_INTEGER,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_CheckRecordingInfoByIndex", PARAMS_BY_NAME, JSON_STRING,"index",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingInfoById", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_CheckRecordingInfoById", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_CheckRecordingInfoById);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetIsRecordingInProgress", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingSize", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingDuration", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingStartTime", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetDefaultTSBMaxDuration", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_CreateTSB", PARAMS_BY_NAME, JSON_STRING,"duration",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_ConvertTSBToRecording", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,"tsbId",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_CreateRecording", PARAMS_BY_NAME, JSON_STRING,"recordingTitle",JSON_STRING,"recordingId",JSON_STRING,"recordDuration",JSON_INTEGER,"qamLocator",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_UpdateRecording", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_DeleteRecording", PARAMS_BY_NAME, JSON_STRING,"recordingId",JSON_STRING,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetSegmentsCount", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount);
           this->bindAndAddMethod(Procedure("TestMgr_DVRManager_GetRecordingSegmentInfoByIndex", PARAMS_BY_NAME, JSON_STRING,"index",JSON_INTEGER,"playUrl",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex);
#endif

/*Optimised Code*/


           this->bindAndAddMethod(Procedure("TestMgr_CheckAudioVideoStatus", PARAMS_BY_NAME, JSON_STRING,"audioVideoStatus",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_CheckAudioVideoStatus);
           this->bindAndAddMethod(Procedure("TestMgr_CheckRmfStreamerCrash", PARAMS_BY_NAME, JSON_STRING,"patternToSearch",JSON_STRING,"logFile",JSON_STRING,"FileNameToCpTdkPath",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent::MediaframeworkAgent_CheckRmfStreamerCrash);
           this->bindAndAddMethod(Procedure("TestMgr_ClearLogFile", PARAMS_BY_NAME, JSON_STRING,"logFileToClear",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_ClearLogFile);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementCreateInstance", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"factoryEnable",JSON_STRING,"qamSrcUrl",JSON_STRING,"newQamSrc",JSON_STRING,"newQamSrcUrl",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementCreateInstance);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementRemoveInstance", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"factoryEnable",JSON_STRING,"newQamSrc",JSON_STRING,"newQamSrc",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementRemoveInstance);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementInit", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementInit);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementTerm", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementTerm);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementOpen", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"url",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementOpen);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementClose", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementClose);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementPlay", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"newQamSrc",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,"defaultPlay",JSON_INTEGER,"playSpeed",JSON_REAL,"playTime",JSON_REAL,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementPlay);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementPause", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"newQamSrc",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementPause);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementSetSpeed", PARAMS_BY_NAME, JSON_STRING,"playSpeed",JSON_REAL,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementSetSpeed);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementGetSpeed", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementGetSpeed);

           this->bindAndAddMethod(Procedure("TestMgr_RmfElementSetMediaTime", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,"mediaTime",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementSetMediaTime);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementGetMediaTime", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaTime);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementGetMediaInfo", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaInfo);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElementGetState", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElementGetState);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_Sink_SetSource", PARAMS_BY_NAME, JSON_STRING,"rmfSourceElement",JSON_STRING,"rmfSinkElement",JSON_STRING,"newQamSrc",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_SinkSetSource);

           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_MpSink_SetVideoRectangle", PARAMS_BY_NAME, JSON_STRING,"apply",JSON_INTEGER,"X",JSON_INTEGER,"Y",JSON_INTEGER,"height",JSON_INTEGER,"width",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_CheckForSPTSRead_QAMSrc_Error", PARAMS_BY_NAME, JSON_STRING,"logPath",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error);

           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_RmfPlatform_Init", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_RmfPlatform_Uninit", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_InitPlatform", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_UninitPlatform", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_UseFactoryMethods", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_GetTSID", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetTSID);
           this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_GetLTSID", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_GetLowLevelElement", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_FreeLowLevelElement", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_QAMSrc_ChangeURI", PARAMS_BY_NAME, JSON_STRING,"url",JSON_STRING,"numOfTimeChannelChange",JSON_INTEGER,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI);

            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_HNSink_InitPlatform", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_InitPlatform);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_HNSink_UninitPlatform", PARAMS_BY_NAME, JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_UninitPlatform);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_HNSink_SetProperties", PARAMS_BY_NAME, JSON_STRING,"url",JSON_STRING,"socketId",JSON_INTEGER,"dctpEnable",JSON_STRING,"streamIp",JSON_STRING,"typeFlag",JSON_INTEGER,"useChunkTransfer",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetProperties);
            this->bindAndAddMethod(Procedure("TestMgr_RmfElement_HNSink_SetSourceType", PARAMS_BY_NAME, JSON_STRING,"rmfElement",JSON_STRING,NULL), &MediaframeworkAgent::MediaframeworkAgent_RmfElement_HNSink_SetSourceType);
        }

                //Inherited functions
                bool initialize(IN const char* szVersion);
                bool cleanup(const char* szVersion);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();	
		
		/*Optimised Code */
#if 1
		void MediaframeworkAgent_CheckAudioVideoStatus(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_CheckRmfStreamerCrash(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_ClearLogFile(IN const Json::Value& req, OUT Json::Value& response);
		
		void MediaframeworkAgent_RmfElementCreateInstance(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementRemoveInstance(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementInit(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementTerm(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementOpen(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementClose(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementPlay(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementPause(IN const Json::Value& req, OUT Json::Value& response);

		void MediaframeworkAgent_RmfElement_SinkSetSource(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle(IN const Json::Value& req, OUT Json::Value& response);

		void MediaframeworkAgent_RmfElementSetSpeed(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementGetSpeed(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementSetMediaTime(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElementGetMediaTime(IN const Json::Value& req, OUT Json::Value& response);	
		void MediaframeworkAgent_RmfElementGetMediaInfo(IN const Json::Value& req, OUT Json::Value& response);	
		void MediaframeworkAgent_RmfElementGetState(IN const Json::Value& req, OUT Json::Value& response);

		void MediaframeworkAgent_RmfElement_CheckForSPTSRead_QAMSrc_Error(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Init(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_RmfPlatform_Uninit(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_InitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_UseFactoryMethods(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_GetTSID(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_GetLTSID(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_GetLowLevelElement(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_FreeLowLevelElement(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_QAMSrc_ChangeURI(IN const Json::Value& req, OUT Json::Value& response);
		
		void MediaframeworkAgent_RmfElement_HNSink_InitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_HNSink_UninitPlatform(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_HNSink_SetProperties(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_RmfElement_HNSink_SetSourceType(IN const Json::Value& req, OUT Json::Value& response);
		
#endif

                //Mediaframework Wrapper functions
                void MediaframeworkAgent_MPSink_SetGetMute(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_MPSink_SetGetVolume(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_HNSrc_GetBufferedRanges(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_HNSrcMPSink_Video_State(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_HNSrcMPSink_Video_Volume(IN const Json::Value& req, OUT Json::Value& response);
	
		/*DVR Recording List*/
		void MediaframeworkAgent_DVR_Rec_List(IN const Json::Value& req, OUT Json::Value& response);
		void MediaframeworkAgent_DVR_CreateNewRecording(IN const Json::Value& req, OUT Json::Value& response);
		
		/*DVR sink*/
        	void MediaframeworkAgent_DVRSink_InitTerm(IN const Json::Value& req, OUT Json::Value& response);

                /*DVR Manager*/
                void MediaframeworkAgent_DVRManager_GetSpace(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_DVRManager_GetRecordingCount(IN const Json::Value& req, OUT Json::Value& response);
                void MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex(const Json::Value&, Json::Value&);
		void MediaframeworkAgent_DVRManager_CheckRecordingInfoByIndex(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetRecordingInfoById(const Json::Value&, Json::Value&);
		void MediaframeworkAgent_DVRManager_CheckRecordingInfoById(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetIsRecordingInProgress(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetRecordingSize(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetRecordingDuration(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetRecordingStartTime(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_CreateTSB(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_ConvertTSBToRecording(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_CreateRecording(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_UpdateRecording(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_DeleteRecording(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetSegmentsCount(const Json::Value&, Json::Value&);
                void MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex(const Json::Value&, Json::Value&);

};
        extern "C" MediaframeworkAgent* CreateObject(TcpSocketServer &ptrtcpServer);

#endif //__MEDIAFRAMEWORK_STUB_H__

