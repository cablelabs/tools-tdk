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

#ifndef __RECORDER_STUB_H__
#define __RECORDER_STUB_H__
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <string>
#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false 

#define RECORDER_PATTERN "dvr_update_recording"
#define RECORDER_LOG_PATH "/recorderlog.txt"
#define OCAPRI_LOG_PATH "/opt/logs/ocapri_log.txt"
#define PRE_REQUISITE_LOG_PATH "logs/Recorder_testmodule_prereq_details.log"
#define PRE_REQUISITE_FILE "scripts/Recorder_testmodule_pre-script.sh"
#define POST_REQUISITE_LOG_PATH "logs/Recorder_testmodule_postreq_details.log"
#define POST_REQUISITE_FILE "scripts/Recorder_testmodule_post-script.sh"
#define RECORDING_METADATA_PATH "/tmp/mnt/diska3/persistent/dvr/recdbser"
#define RMFCONFIG_INI_FILE "/opt/rmfconfig.ini"
using namespace std;
#define NUMBER_OCAPID 10

class RDKTestAgent;
class RecorderAgent : public RDKTestStubInterface
{
	public:
		void* RecorderAgenthandle;

		/*Constuctor*/
		RecorderAgent();
		bool Recorder_ScheduleRecording(IN const Json::Value& request, OUT Json::Value& response);
		bool Recorder_checkRecording_status(IN const Json::Value& request, OUT Json::Value& response);
		bool Recorder_SendRequest(IN const Json::Value& request, OUT Json::Value& response);
		bool Recorder_SendRequestToDeleteFile(IN const Json::Value& request, OUT Json::Value& response);
		bool Recorder_DeleteRecordingMetaData(IN const Json::Value& request, OUT Json::Value& response);
                bool Recorder_PresenceOfRecordingMetaData(IN const Json::Value& request, OUT Json::Value& response);
		bool Recorder_SetValuesInRmfconfig(IN const Json::Value& request, OUT Json::Value& response);
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);		
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();
		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
};

	extern "C" RecorderAgent* CreateObject();

#endif //__RECORDER_Stub
