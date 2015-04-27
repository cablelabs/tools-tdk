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
#include "RecorderStub.h"

string g_tdkPath = getenv("TDK_PATH");

/***************************************************************************
*Function name: RecorderAgent::RecorderAgent
*
*Arguments    : NULL
*
*Description  : Constructor function for RecorderAgent class
***************************************************************************/
RecorderAgent::RecorderAgent()
{
	DEBUG_PRINT(DEBUG_TRACE, "Initializing RecorderAgent\n");
}

/**************************************************************************
Function name : RecorderAgent::initialize

Arguments     : Input arguments are Version string and RecorderAgent obj ptr 

Description   : Registering all the wrapper functions with the agent for using these functions in the script

***************************************************************************/
bool RecorderAgent::initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Registering wrapper functions with the agent\n");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_ScheduleRecording,"TestMgr_Recorder_ScheduleRecording");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_checkRecording_status,"TestMgr_Recorder_checkRecording_status");
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : RecorderAgent::testmodulepre_requisites

Arguments     : None

Description   : Setting Pre-requisites needed to execute Recorder tests

***************************************************************************/
std::string RecorderAgent::testmodulepre_requisites()
{
	DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Entry\n");
	ifstream logfile;
	string Rec_testmodule_PR_cmd, Rec_testmodule_PR_log,line;
	Rec_testmodule_PR_cmd= g_tdkPath + "/" + PRE_REQUISITE_FILE;
	Rec_testmodule_PR_log= g_tdkPath + "/" + PRE_REQUISITE_LOG_PATH;
	string pre_req_chk= "source "+Rec_testmodule_PR_cmd; 
	try
        {
                system((char *)pre_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of pre-requisite script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE<DETAILS>Exception occured execution of pre-requisite script";
        }
	logfile.open(Rec_testmodule_PR_log.c_str());
        if(logfile.is_open())
	{
		if(getline(logfile,line)>0);
		{
			logfile.close();
			DEBUG_PRINT(DEBUG_LOG,"\nPre-Requisites set\n");
			DEBUG_PRINT(DEBUG_TRACE, "testmodulepre_requisites --> Exit\n");
			return line;
		}
		logfile.close();
		DEBUG_PRINT(DEBUG_ERROR,"\nPre-Requisites not set\n");
                return "FAILURE<DETAILS>Proper result is not found in the log file";
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
                return "FAILURE<DETAILS>Unable to open the log file";
        }
}
/**************************************************************************
Function name : RecorderAgent::testmodulepost_requisites

Arguments     : None

Description   : Re-Setting the Pre-requisites which was set after execution

***************************************************************************/

bool RecorderAgent::testmodulepost_requisites()
{
#if 0
	DEBUG_PRINT(DEBUG_TRACE, "testmodulepost_requisites --> Entry\n");
        ifstream logfile;
        string Rec_testmodule_POST_cmd, Rec_testmodule_POST_log,line;
        Rec_testmodule_POST_cmd= g_tdkPath + "/" + POST_REQUISITE_FILE;
        Rec_testmodule_POST_log= g_tdkPath + "/" + POST_REQUISITE_LOG_PATH;
        string post_req_chk= "source "+Rec_testmodule_POST_cmd;
	int offset;
        try
        {
                system((char *)post_req_chk.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of post-requisite script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }
        logfile.open(Rec_testmodule_POST_log.c_str());
        if(logfile.is_open())
        {
                if(getline(logfile,line)>0);
                {
			if ((offset = line.find("SUCCESS", 0)) != std::string::npos) {
                        logfile.close();
                        DEBUG_PRINT(DEBUG_LOG,"\nPost-Requisites set %s\n",line.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "testmodulepost_requisites --> Exit\n");
                        return TEST_SUCCESS;
			}
			DEBUG_PRINT(DEBUG_ERROR,"\nPost-Requisites Reset Failed - %s\n", line.c_str());
	                return TEST_FAILURE;
                }
		logfile.close();
                DEBUG_PRINT(DEBUG_ERROR,"\nPost-Requisites not set\n");
                return TEST_FAILURE;
        }
        else
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the log file.\n");
	        return TEST_FAILURE;
        }
#endif
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : RecorderAgent::Recorder_ScheduleRecording()

Arguments     : Input arguments are Source_id,Recording_Id,Duration. Output argument is details,result.

Description   : Returns Generated Json Message in details.
***************************************************************************/
bool RecorderAgent::Recorder_ScheduleRecording(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder ScheduleRecording ---> Entry\n");
        string recording_id, src_id, duration_msec, current_rec, datetime;
        
        string log_removing, set_time;
        datetime = request["UTCTime"].asString();
        recording_id = request["Recording_Id"].asString();
        duration_msec = request["Duration"].asString();
        src_id = request["Source_id"].asString();
        current_rec = request["Start_time"].asString();
	set_time = "date " + datetime;
	try
        {
                //system((char *)set_time.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured in setting UTC time\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                response["result"] = "FAILURE";
        }


        string json_url = "{\"updateSchedule\" : {\"requestId\" : \"7\", \"schedule\" : [\
        {\"recordingId\" : \""+recording_id+"\",\"locator\" : [ \"ocap://"+src_id+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+current_rec+" ,\"duration\" : "+duration_msec+" ,\"properties\":{\"title\":\"Recording_"+recording_id+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" }]}}";

        DEBUG_PRINT(DEBUG_LOG,"Framed_RecordingURL is %s\n", json_url.c_str());
        response["details"] = json_url;

        DEBUG_PRINT(DEBUG_LOG,"Checking URL is %s\n", response["details"].asString().c_str());

        log_removing = ">"OCAPRI_LOG_PATH;
        DEBUG_PRINT(DEBUG_LOG,"Log_deletion is %s\n", log_removing.c_str());

        //* To handle exception for system call
        try
        {
                //system((char *)log_removing.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                response["result"] = "FAILURE";
        }

        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "Recorder_ScheduleRecording ---> Exit\n");
        return TEST_SUCCESS;
}
/**************************************************************************
  Function name : RecorderAgent::Recorder_checkRecording_status()

Arguments     : Input argument is Recording_Id. Output argument is details,result.

Description   : Returns Generated Json Message in details.
 ***************************************************************************/
bool RecorderAgent::Recorder_checkRecording_status(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "checkRecording_status ---> Entry\n");

        string recording_id, RecorderLogFilePath, line_Recorder_Log, entry_pos, rec;
        recording_id = request["Recording_Id"].asString();

        std::string strCmd;
        strCmd = getenv ("TDK_PATH");
        strCmd.append("/");
        strCmd.append(RECORDER_LOG_PATH);
        
//        string log_copying = "cp -r " OCAPRI_LOG_PATH " " RECORDER_LOG_PATH;
//        string permission = "chmod 777 " RECORDER_LOG_PATH;

        string log_copying = "cp -r " OCAPRI_LOG_PATH " ";
        log_copying.append(strCmd);
        string permission = "chmod 777 ";
        permission.append(strCmd);

        DEBUG_PRINT(DEBUG_LOG,"copying is %s\n", log_copying.c_str());
        DEBUG_PRINT(DEBUG_LOG,"chmod is %s\n", permission.c_str());
//        RecorderLogFilePath = RECORDER_LOG_PATH;
        RecorderLogFilePath = strCmd;

        //* To handle exception for system call
        try
        {
                system((char *)log_copying.c_str());
                system((char*)permission.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
                return TEST_FAILURE;
        }

        /* Checking for the success pattern from ocapRI log*/
        ifstream RecorderLogFile;
        RecorderLogFile.open(RecorderLogFilePath.c_str());
        if(RecorderLogFile.is_open())
        {
                while (!RecorderLogFile.eof())
                {
                        if(getline(RecorderLogFile,line_Recorder_Log)>0)
                        {
                                if(line_Recorder_Log.find(RECORDER_PATTERN) != string::npos)
                                {
                                        if(line_Recorder_Log.find(recording_id) != string::npos)
                                        {
                                                response["result"] = "SUCCESS";
                                                response["details"] = line_Recorder_Log.c_str();
//                                                response["log-path"]= RECORDER_LOG_PATH;
                                                response["log-path"]= strCmd.c_str();
                                                break;
                                        }
                                }
                        }
                        else
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "No Pattern found in Log file";
//                                response["log-path"]= RECORDER_LOG_PATH;
                                response["log-path"]= strCmd.c_str();
                        }

                }
                RecorderLogFile.close();
                response["result"] = "SUCCESS";
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Unable to open %s\n", RecorderLogFilePath.c_str());
                DEBUG_PRINT(DEBUG_TRACE,"CheckRecording_status ---> Exit\n");
                response["result"] = "FAILURE";
                response["details"] = "Unable to open the log file";
        }
        DEBUG_PRINT(DEBUG_TRACE,"CheckRecording_status ---> Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : RecorderAgent::CreateObject()

Arguments     : NULL

Description   : create the object of RecorderAgent  
***************************************************************************/
extern "C" RecorderAgent* CreateObject()
{
	DEBUG_PRINT(DEBUG_TRACE, "Creating Recorder Agent Object\n");
	return new RecorderAgent();
}

/**************************************************************************
Function name : RecorderAgent::cleanup()

Arguments     : NULL

Description   :close things cleanly  
***************************************************************************/
bool RecorderAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
        if(NULL == ptrAgentObj)
        {
                return TEST_FAILURE;
	}
	ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_ScheduleRecording");
	ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_checkRecording_status");
	/* All done, close things cleanly */
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaStreamerAgent::DestroyObject()

Arguments     : Input argument is MediaStreamerAgent Stub Object

Description   : Delete MediaStreamer stub object
***************************************************************************/
extern "C" void DestroyObject(RecorderAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying Object\n");
	delete stubobj;
}

