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
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_checkOcapri_log,"TestMgr_Recorder_checkOcapri_log");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_SendRequest,"TestMgr_Recorder_SendRequest");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_SendRequestToDeleteFile,"TestMgr_Recorder_SendRequestToDeleteFile");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_DeleteRecordingMetaData,"TestMgr_Recorder_DeleteRecordingMetaData");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_SetValuesInRmfconfig,"TestMgr_Recorder_SetValuesInRmfconfig");
        ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_PresenceOfRecordingMetaData,"TestMgr_Recorder_PresenceOfRecordingMetaData");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_clearOcapri_log,"TestMgr_Recorder_clearOcapri_log");
	ptrAgentObj->RegisterMethod(*this,&RecorderAgent::Recorder_ExecuteCmd,"TestMgr_Recorder_ExecuteCmd");
	
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
Function name : RecorderAgent::Recorder_clearOcapri_log()

Arguments     : None

Description   : This will clear the ocapri log
 ***************************************************************************/
bool RecorderAgent::Recorder_clearOcapri_log(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "clearOcapri_log ---> Entry\n");
        string clearLogCmd = "cat /dev/null > " OCAPRI_LOG_PATH;      
        DEBUG_PRINT(DEBUG_TRACE, "clearLogCmd: %s\n",clearLogCmd.c_str());
        try
        {
                system((char *)clearLogCmd.c_str());
                DEBUG_PRINT(DEBUG_TRACE,"Clear Ocapri Log Success\n");
                response["result"]="SUCCESS";
                response["details"]="Cleared Ocapri Log";
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured while clearing Ocapri Log\n");
                response["result"]="FAILURE";
                response["details"]="Failed to clear Ocapri Log";
        }
        DEBUG_PRINT(DEBUG_TRACE,"clearOcapri_log ---> Exit\n");
        return TEST_SUCCESS;
} 


/**************************************************************************
Function name : RecorderAgent::Recorder_checkOcapri_log()

Arguments     : Input argument is a pattern. Output argument is details,result.

Description   : To check whether  pattern is there in ocapri log. Returns Generated Json Message in details.
 ***************************************************************************/
bool RecorderAgent::Recorder_checkOcapri_log(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "checkOcapri_log ---> Entry\n");

        string pattern = request["pattern"].asCString();

        string recording_id, RecorderLogFilePath, line_Recorder_Log, entry_pos, rec;

        std::string strCmd;
        strCmd = getenv ("TDK_PATH");
        strCmd.append("/");
        strCmd.append(RECORDER_LOG_PATH);
        

        string log_copying = "cp -r " OCAPRI_LOG_PATH " ";
        log_copying.append(strCmd);
        string permission = "chmod 777 ";
        permission.append(strCmd);

        DEBUG_PRINT(DEBUG_LOG,"copying is %s\n", log_copying.c_str());
        DEBUG_PRINT(DEBUG_LOG,"chmod is %s\n", permission.c_str());
        RecorderLogFilePath = strCmd;

        //* To handle exception for system call
        try
        {
                system((char *)log_copying.c_str());
                system((char*)permission.c_str());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured while copying ocapri log file\n");
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
                                if(line_Recorder_Log.find(pattern) != string::npos)
                                {
                                        response["result"] = "SUCCESS";
                                        response["details"] = line_Recorder_Log.c_str();
                                        response["log-path"]= strCmd.c_str();
                                        break;
                                       
                                }
                        }
                        else
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "No Pattern found in Log file";
                                response["log-path"]= strCmd.c_str();
                        }

                }
                RecorderLogFile.close();
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE,"Unable to open %s\n", RecorderLogFilePath.c_str());
                DEBUG_PRINT(DEBUG_TRACE,"checkOcapri_log ---> Exit\n");
                response["result"] = "FAILURE";
                response["details"] = "Unable to open the log file";
        }
        DEBUG_PRINT(DEBUG_TRACE,"checkOcapri_log ---> Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
Function name : RecorderAgent::Recorder_SendRequest()

Arguments     : None

Description   : Returns success
***************************************************************************/
bool RecorderAgent::Recorder_SendRequest(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder SendRequest ---> Entry\n");
	response["result"] = "SUCCESS";
	response["details"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_TRACE,"Recorder SendRequest ---> Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : RecorderAgent::Recorder_SendRequestToDeleteFile()

Arguments     : Filename on STB to be deleted

Description   : Returns success
***************************************************************************/
bool RecorderAgent::Recorder_SendRequestToDeleteFile(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder SendRequestToDeleteFile ---> Entry\n");

        string filename = request["filename"].asString();

        if (!filename.empty())
	{
        	// Remove the file
        	if( remove( filename.c_str() ) != 0 )
        	{
                	DEBUG_PRINT(DEBUG_ERROR,"Error deleting file %s\n", filename.c_str());
			response["result"] = "FAILURE";
			response["details"] = "Error deleting file";
        	}
        	else
        	{
                	DEBUG_PRINT(DEBUG_TRACE, "Successfully deleted file %s\n", filename.c_str());
			response["result"] = "SUCCESS";
			response["details"] = "File successfully deleted";
        	}
        }
        else
        {
                DEBUG_PRINT(DEBUG_TRACE, "Error: Filename is NULL\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Filename is null";
        }

        DEBUG_PRINT(DEBUG_TRACE,"Recorder SendRequestToDeleteFile ---> Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
 * Function name : RecorderAgent::Recorder_DeleteRecordingMetaData()
 *
 * Arguments     : Input argument is Recording ID
 *
 * Description   : Find recording meta data files which contains its recording ID and delete them
 * ***************************************************************************/
bool RecorderAgent::Recorder_DeleteRecordingMetaData(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder DeleteRecordingMetaData ---> Entry\n");
        string recording_id = request["Recording_Id"].asString();
        string search_recid_delete_cmd,search_recid_cmd;
        string str1 = "grep -rls";
        string str2(recording_id);
	string find = "find";
	int count = 0;

        search_recid_cmd= str1 + " " + str2 + " " + RECORDING_METADATA_PATH;
	DEBUG_PRINT(DEBUG_TRACE,"Command for searching metadata files contains rec-id: \"%s\" \n",search_recid_cmd.c_str() );

	/* Before going for deletion, check whether there are any metadata file contains the rec id*/
	FILE *file = popen(search_recid_cmd.c_str(), "r");
        if ( file != NULL)
        {
        	char line[128];
            	while (fgets(line, sizeof line, file) != NULL)
		{
                	++count;
            	}
            	fclose (file);
		DEBUG_PRINT(DEBUG_TRACE, "Number of lines: %d\n", count);
        }
	if (count == 0)
	{
                response["result"] = "FAILURE";
                response["details"] = "No Files Found!";
                DEBUG_PRINT(DEBUG_ERROR," There are no metadata files present with rec-id:%s \n",recording_id.c_str() );
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
	}

	/* Now we can go for deletion as there are files present contains rec-id*/
	search_recid_delete_cmd = find + " " + RECORDING_METADATA_PATH + " " + "-type f -exec grep -q" + " " + str2 + " " + "{}" + " " + "\\;" + " " + "-delete";
	DEBUG_PRINT(DEBUG_TRACE,"Command for searching metadata files contains rec-id and delete them: \"%s\" \n",search_recid_delete_cmd.c_str() );

        try
        {
                system ((char *)search_recid_delete_cmd.c_str());
        }
        catch(...)
        {
                response["result"] = "FAILURE";
                response["details"] = "Error deleting files";
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of deleting metadata files \n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }

        DEBUG_PRINT(DEBUG_TRACE, "Successfully deleted files \n");
        response["result"] = "SUCCESS";
        response["details"] = "Files successfully deleted";

        DEBUG_PRINT(DEBUG_TRACE,"Recorder DeleteRecordingMetaData ---> Exit\n");
        return TEST_SUCCESS;
}

/**************************************************************************
 * Function name : RecorderAgent::Recorder_PresenceOfRecordingMetaData()
 *
 * Arguments     : Input argument is Recording ID
 *
 * Description   : Checking the presence of recording meta data files which contains its recording ID and priority
 * ***************************************************************************/
bool RecorderAgent::Recorder_PresenceOfRecordingMetaData(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder_PresenceOfRecordingMetaData ---> Entry\n");
        string recording_id = request["Recording_Id"].asString();
        string search_recid_priority_cmd;
        string str1 = "grep -rls";
        string str2(recording_id);
        string find = "find";
        int count = 0;

        search_recid_priority_cmd= find + " " + RECORDING_METADATA_PATH + " " + " -type f | xargs " + str1 + " " + str2 + " " + " | xargs " + str1 + " " + "P0";
        DEBUG_PRINT(DEBUG_TRACE,"Command for searching metadata files contains rec-id: \"%s\" \n",search_recid_priority_cmd.c_str() );

        /* check whether there are any metadata file contains the rec id*/

        FILE *file = popen(search_recid_priority_cmd.c_str(), "r");
        if ( file != NULL)
        {
                char line[128];
                while (fgets(line, sizeof line, file) != NULL)
                {
                        ++count;
                }
                fclose (file);
                DEBUG_PRINT(DEBUG_TRACE, "Number of lines: %d\n", count);
        }
        if (count == 0)
        {
                response["result"] = "FAILURE";
                response["details"] = "No Files Found!";
                DEBUG_PRINT(DEBUG_ERROR," There are no metadata files present with rec-id:%s \n",recording_id.c_str() );
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return TEST_FAILURE;
        }

        DEBUG_PRINT(DEBUG_TRACE, "Successfully found metadata files \n");
        response["result"] = "SUCCESS";
        response["details"] = "Files found successfully";

        DEBUG_PRINT(DEBUG_TRACE,"Recorder_PresenceOfRecordingMetaData ---> Exit\n");
        return TEST_SUCCESS;
}
/**************************************************************************
 * Function name : RecorderAgent::Recorder_ExecuteCmd()
 *
 * Arguments     : Input arguments are command to execute in box
 *
 * Description   : This will execute linux commands in box
 * ***************************************************************************/
bool RecorderAgent::Recorder_ExecuteCmd(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder_ExecuteCmd ---> Entry\n");
        string fileinfo = request["command"].asCString();
        FILE *fp = NULL;
        char readRespBuff[BUFF_LENGTH];
        string popenBuff;

        /*Frame the command  */
        string path = "";
        path.append(fileinfo);

        DEBUG_PRINT(DEBUG_TRACE, "Command Request Framed: %s\n",path.c_str());

        fp = popen(path.c_str(),"r");

        /*Check for popen failure*/
        if(fp == NULL)
        {
                response["result"] = "FAILURE";
                response["details"] = "popen() failure";
                DEBUG_PRINT(DEBUG_ERROR, "popen() failure for %s\n", path.c_str());

                return TEST_FAILURE;
        }

        /*copy the response to a buffer */
        while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
                popenBuff += readRespBuff;
        }

        pclose(fp);

        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",popenBuff.c_str());
        response["result"] = "SUCCESS";
        response["details"] = popenBuff;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "Recorder_ExecuteCmd -->Exit\n");
        return TEST_SUCCESS;

}


/**************************************************************************
 * Function name : RecorderAgent::Recorder_SetValuesInRmfconfig()
 *
 * Arguments     : Input arguments are keyword, value, set or reset flag
 *
 * Description   : Set the values in the rmfconfig.ini for the corresponding keyword. Response details will send previous value after setting the new value.
 * Caller needs to store the previous value from response[details] in order to reset the value (if required)
 * ***************************************************************************/
bool RecorderAgent::Recorder_SetValuesInRmfconfig(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "Recorder_SetValuesInRmfconfig ---> Entry\n");
        string keyword = request["Keyword"].asString();
	string value = request["Value"].asString();
	string write_cmd,read_cmd;
	string sed = "sed -i -e";
        string sedarg1="\"s#";
        string sedarg2= "#g\"";
        string key(keyword);
	string awk = "awk -F";
	char line[128];

	DEBUG_PRINT(DEBUG_TRACE,"Value received for overriding: \"%s\" \n",value.c_str() );

        /* Before writing the new value, get the existing value */
        read_cmd=awk + " " + "\"=\"" + " " + "'/" + key + "/" + " "+ "{print $2}\'" + " " + RMFCONFIG_INI_FILE;
        DEBUG_PRINT(DEBUG_TRACE,"Command for reading existing data: \"%s\" \n",read_cmd.c_str() );
        FILE *file = popen(read_cmd.c_str(), "r");
        if ( file != NULL)
        {
		/* WARNING: Assumption : All keywords have single line of data. Multiple lines of data not handled */
                int count = 0, i = 0;
                memset(line, '\0', strlen(line));
                while (fgets(line, sizeof(line), file) != NULL)
                {
                        ++count;
                }
                fclose (file);
                DEBUG_PRINT(DEBUG_TRACE,"Number of lines: %d, value: %s\n:",count,line);

		/* Ignore the new line character */
		while( (line[i++] != '\n') && (i < strlen(line)) );
                if (line[--i]== '\n')
                        line[i]='\0';

        }
       	/* send the previous value thru response details*/
	response["details"]=line;

	/* As we now stored the existing value into response details, go for writing the new value */
	write_cmd= sed + " " + sedarg1 + key + "=.*#" + key + "=" + value + sedarg2 + " " + RMFCONFIG_INI_FILE;
	DEBUG_PRINT(DEBUG_TRACE,"Command for searching metadata files contains rec-id: \"%s\" \n",write_cmd.c_str() );
	try
	{
		system ((char *)write_cmd.c_str());
	}
	catch(...)
	{
		response["result"] = "FAILURE";
		response["details"] = "Error in updating file";
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of updating rmfconfig.ini \n");
		DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
		return TEST_FAILURE;
	}
	response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "Successfully updated! \n");
        DEBUG_PRINT(DEBUG_TRACE,"Recorder_SetValuesInRmfconfig ---> Exit\n");
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
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_ScheduleRecording");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_checkOcapri_log");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_SendRequest");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_SendRequestToDeleteFile");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_DeleteRecordingMetaData");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_SetValuesInRmfconfig");
        ptrAgentObj->UnregisterMethod("TestMgr_Recorder_PresenceOfRecordingMetaData");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_clearOcapri_log");
	ptrAgentObj->UnregisterMethod("TestMgr_Recorder_ExecuteCmd");
	
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
