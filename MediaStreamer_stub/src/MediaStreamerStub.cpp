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
#include "MediaStreamerStub.h"


#define REC_ID_START_POS_OFFSET 7
#define TRASPORT_CMD_OFFSET 49
#define FRAME_SEARCH_OFFSET 23
#define FRAME_DIV_FACTOR 3.0
#define TRANS_CMD_SLOW_REWIND 4
#define TRANS_CMD_SLOW_FORWARD 6
#define CURRENT_POSITION_OFFSET 17
#define TRASPORT_CMD_LENGTH 1

#define JSON_FILE_PATH "jfile.json"
#define RECORDER_ID_FILE_PATH "/opt/www/whitebox/wbdevice.dat"
#define PLAYER_SCRIPT_PATH "runPlayer.sh"
#define PLAYER_LOG_PATH "playerlog.txt"
#define OCAPRI_LOG_PATH "/opt/logs/ocapri_log.txt"
#define MEDIA_STREAMER_LOG_PATH "mediaStreamerLog.txt"
#define RECORDED_LIST_PATH "recordedlist.txt"
#define RECORDED_LIST_MOD_PATH "recordedListMod.txt"
#define RECORDED_LIST_SCRIPT_PATH "alignRecList.sh"
#define SUCCESS_PATTERN "Current Position="
#define FRAME_SEARCH_PATTERN "next_predicted_frame = "
#define TRASPORT_CMD_PATTERN "IpStreamOut::transport_command"
/*
 Fetching Streaming Interface Name
 */
#define BUFFER_LENGTH 64
#define STREAMING_INTERFACE "Streaming Interface"
#define FETCH_STREAMING_INT_FILE "streaming_interface_file"

#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int , char *, int );
#endif


using namespace std;

string g_tdkPath = getenv("TDK_PATH");

/*************************************************************************
Function name: MediaStreamerAgent::MediaStreamerAgent

Arguments    : NULL

Description  : Constructor function for MediaStreamerAgent class
***************************************************************************/
MediaStreamerAgent::MediaStreamerAgent()
{
    DEBUG_PRINT(DEBUG_TRACE, "Initializing MediastreamerAgent\n");
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string MediaStreamerAgent::testmodulepre_requisites()
{
    /*	#ifdef USE_SOC_INIT
            //Initialize SOC
            soc_init(1, "tdk_agent", 1);
            #endif
    */
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool MediaStreamerAgent::testmodulepost_requisites()
{
    /*	#ifdef USE_SOC_INIT
            // Uninitialize SOC
            soc_uninit();
            #endif
    */
    return true;
}
/********************************************************************************************************************
 Purpose:               To get the Host's IP Address by querrying the network Interface.

 Parameters:
                             szInterface [IN]    - Interface used to communicate.

 Return:                 string    - IP address of corresponding interface.

*********************************************************************************************************************/
std::string GetHostIP (const char* szInterface)
{
    struct ifaddrs* pIfAddrStruct = NULL;
    struct ifaddrs* pIfAddrIterator = NULL;
    void* pvTmpAddrPtr = NULL;
    char szAddressBuffer [INET_ADDRSTRLEN];
    getifaddrs (&pIfAddrStruct);

    for (pIfAddrIterator = pIfAddrStruct; pIfAddrIterator != NULL; pIfAddrIterator = pIfAddrIterator->ifa_next)
    {
        if (pIfAddrIterator->ifa_addr->sa_family == AF_INET)
        {
            // check it is a valid IP4 Address
            pvTmpAddrPtr = & ( (struct sockaddr_in *)pIfAddrIterator->ifa_addr )-> sin_addr;
            inet_ntop (AF_INET, pvTmpAddrPtr, szAddressBuffer, INET_ADDRSTRLEN);

            if ( (strcmp (pIfAddrIterator -> ifa_name, szInterface) ) == 0)
            {
                break;
            }
        }
    }

    DEBUG_PRINT(DEBUG_TRACE, "Found IP: %s\n", szAddressBuffer);

    if (pIfAddrStruct != NULL)
    {
        freeifaddrs (pIfAddrStruct);
    }

    return szAddressBuffer;

} /* End of GetHostIP */

/*********************************************************************************************
Function name : fetchStreamingInterface

Arguments     : NULL

Description   : Fetching the streaming interface name from streaming_interface_name file
 ********************************************************************************************/
std::string fetchStreamingInterface()
{
        FILE *interfaceFile = NULL;
        char streamingInterfaceName[BUFFER_LENGTH] = {'\0'};
        string streamingInterfaceFile, fetchInterfaceCmd;

        DEBUG_PRINT(DEBUG_TRACE, "Fetch Streaming Interface function --> Entry\n");

        streamingInterfaceFile = g_tdkPath + "/" + FETCH_STREAMING_INT_FILE;
        fetchInterfaceCmd = "cat " + streamingInterfaceFile + "| grep \"" + STREAMING_INTERFACE + "\" | cut -d \"=\" -f 2 |tr -d '\\r\\n'";

        /*Reading the streaming_interface_file to read the interface name */
        interfaceFile = popen(fetchInterfaceCmd.c_str(), "r");
        if(interfaceFile == NULL)
        {
                DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open the streaming interface file.\n");
                return "FAILURE<DETAILS>Unable to open the streaming interface file";
        }
        if(fgets(streamingInterfaceName, BUFFER_LENGTH, interfaceFile) != NULL)
        {
                pclose(interfaceFile);
                DEBUG_PRINT(DEBUG_TRACE, "Streaming interface = %s \n",streamingInterfaceName);
                DEBUG_PRINT(DEBUG_TRACE, "Fetch Streaming Interface function--> Exit\n");
                return streamingInterfaceName;
        }
	else
        {
                pclose(interfaceFile);
                DEBUG_PRINT(DEBUG_ERROR,"\nStreaming interface not fetched\n");
                return "FAILURE<DETAILS>Proper interface name not found in streaming interface file";
        }


}


/**************************************************************************
Function name : MediaStreamerAgent::initialize

Arguments     : Input arguments are Version string and MediaStreamerAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script

***************************************************************************/
bool MediaStreamerAgent::initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "Registering wrapper functions with the agent\n");
#ifdef RDK_BR_1DOT3
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_LiveTune_Request,"TestMgr_MediaStreamer_LiveTune_Request");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_Recording_Request,"TestMgr_MediaStreamer_Recording_Request");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_Recorded_Urls,"TestMgr_MediaStreamer_Recorded_Urls");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_Recorded_Metadata,"TestMgr_MediaStreamer_Recorded_Metadata");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_Live_Playback,"TestMgr_MediaStreamer_Live_Playback");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_Recording_Playback,"TestMgr_MediaStreamer_Recording_Playback");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::MediaStreamerAgent_DVR_Trickplay,"TestMgr_MediaStreamer_DVR_Trickplay");
#endif
#ifdef RDK_BR_2DOT0
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::RMFStreamerAgent_InterfaceTesting,"TestMgr_RMFStreamer_InterfaceTesting");
    ptrAgentObj->RegisterMethod(*this,&MediaStreamerAgent::RMFStreamerAgent_Player,"TestMgr_RMFStreamer_Player");
#endif
    return TEST_SUCCESS;
}
#ifdef RDK_BR_1DOT3
/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_LiveTune_Request

Arguments     : Input argument is OcapId. Output argument is videoStreamingURL for success scenario or errorCode extracted from json Response

Description   : Receives the ocapid from Test Manager and makes curl request to Media Streamer via Web Interface
				for Live Tune. Gets the error code of Json Response and send it to the Test Manager.
***************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_LiveTune_Request(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_LiveTune_Request ---> Entry\n");
    string ocapid, errorStatus_LiveTune;
    ocapid = request["ocapId"].asString();

    // Web Interface request for live tune
    errorStatus_LiveTune = curlRequest(LIVE_TUNE_REQUEST, ocapid);
    DEBUG_PRINT(DEBUG_LOG, "Curl Response for Live Tune Request is %s\n", errorStatus_LiveTune.c_str());

    if("FAILURE" == errorStatus_LiveTune)
    {
        response["result"] = "FAILURE";
        response["details"] = "Failed to get curl response";
        DEBUG_PRINT(DEBUG_ERROR, "Failed to get curl response\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_LiveTune_Request ---> Exit\n");
        return TEST_FAILURE;
    }

    // Returning errorStatus as "0" for success case
    if(errorStatus_LiveTune.find("http://") != string::npos)
    {
        errorStatus_LiveTune = "0";
    }
    response["result"] = errorStatus_LiveTune;
    response["details"] = "SUCCESS";
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_LiveTune_Request ---> Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_Recording_Request

Arguments     : Input argument is recordingId. Output argument is videoStreamingURL for success scenario or
				errorCode extracted from json Response

Description   : Gets the recordingid of a random url and makes curl request to Media Streamer via Web Inteface
				for Recording asset. Gets the error code of Json Response and send it to the Test Manager.
***************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_Recording_Request(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Entry\n");
    string rec_id, recordingid, errorStatus_Recording;

    recordingid = request["recordingId"].asString();
    if("validId" == recordingid)
    {
        // To get random recording id from url list
        rec_id = getRandomRecId();
        DEBUG_PRINT(DEBUG_LOG, "Random recording id is %s\n", rec_id.c_str());
        if("FAILURE" == rec_id)
        {
            response["result"] = "FAILURE";
            response["details"] = "Failed to get Random Recording";
            DEBUG_PRINT(DEBUG_ERROR, "Failed to get Random Recording\n");
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Exit\n");
            return TEST_FAILURE;
        }

        // If there is no recording asset present in box
        else if("NO_RECORD_ASSET" == rec_id)
        {
            response["result"] = "FAILURE";
            response["details"] = "There is no recording content present";
            DEBUG_PRINT(DEBUG_ERROR, "There is no recording content present\n");
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Exit\n");
            return TEST_FAILURE;
        }
    }
    else
    {
        // To handle negative senarios like resource not found, general error
        rec_id = recordingid;
    }

    // Web Interface request for recording content
    errorStatus_Recording = curlRequest(RECORDING_REQUEST, rec_id);
    DEBUG_PRINT(DEBUG_LOG, "Curl Response for Recording request is %s\n", errorStatus_Recording.c_str());

    if("FAILURE" == errorStatus_Recording)
    {
        response["result"] = "FAILURE";
        response["details"] = "Failed to get curl response";
        DEBUG_PRINT(DEBUG_ERROR, "Failed to get curl response\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Exit\n");
        return TEST_FAILURE;
    }

    // Returning errorStatus as zero for success scenario
    if(errorStatus_Recording.find("http://") != string::npos)
    {
        errorStatus_Recording = "0";
    }
    response["result"] = errorStatus_Recording;
    response["details"] = "SUCCESS";
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_Recorded_Urls

Arguments     : Input argument is None. Output argument is URL List log file path for success scenario or details for failure scenario

Description   : Recieves webinterface request to get list of recorded urls, makes curl request to Media Sreamer
				via Web Inteface to get log file path and send it to Test Manager.
***************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_Recorded_Urls(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Entry\n");
    string curlReqStatus_Urls, logFilePath_Urls, line_Urls;

    // Web Interface request for recording url list
    curlReqStatus_Urls = curlRequest(RECORDING_URL_LIST);

    if("FAILURE" == curlReqStatus_Urls)
    {
        response["result"] = "FAILURE";
        response["details"] = "Get Recorded_Urls failed while getting the curl responce";
        DEBUG_PRINT(DEBUG_ERROR, "Get Recorded_Urls failed while getting the curl responce\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Exit\n");
        return TEST_FAILURE;
    }

    // CurlRequest returns log path of recording url list for success scenario
    logFilePath_Urls=curlReqStatus_Urls;
    DEBUG_PRINT(DEBUG_LOG, "logFilePath for url list is %s\n", logFilePath_Urls.c_str());

    ifstream recordedListmodFile;
    recordedListmodFile.open(logFilePath_Urls.c_str());
    if(recordedListmodFile.is_open())
    {
        getline(recordedListmodFile, line_Urls);

        // To check whether recorded assets present or not
        if((line_Urls.find("Recording #") == string::npos))
        {
            DEBUG_PRINT(DEBUG_ERROR, "There is no recorded assets present in the box\n");
            response["result"] = "SUCCESS";
            response["log-path"] = logFilePath_Urls;
            recordedListmodFile.close();
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Exit\n");
            return TEST_SUCCESS;
        }

        // Format checking for the recorded assets present
        do
        {
            if(line_Urls != "</body></html>") // Skipping Last line which is not having url list data
            {
                if(((line_Urls.find("Recording #") != string::npos) && (line_Urls.find("Duration : ") != string::npos) && (line_Urls.find("http://") != string::npos) && (line_Urls.find("/vldms/dvr?rec_id=") != string::npos)) != true)
                {
                    DEBUG_PRINT(DEBUG_ERROR, "line that is not in format is %s\n", line_Urls.c_str());
                    response["result"] = "FAILURE";
                    response["details"] = logFilePath_Urls + " file is not in correct format";
                    recordedListmodFile.close();
                    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Exit\n");
                    return TEST_FAILURE;
                }
            }
            getline(recordedListmodFile, line_Urls);
        } while(!recordedListmodFile.eof());
        response["result"] = "SUCCESS";
        response["details"] = "SUCCESS";
        response["log-path"] = logFilePath_Urls;
        recordedListmodFile.close();
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR, "Not able to open the file %s \n", logFilePath_Urls.c_str());
        response["result"] = "FAILURE";
        response["details"] = "Unable to open " + logFilePath_Urls + " file";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Urls ---> Exit\n");
        return TEST_FAILURE;
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_Recorded_Metadata

Arguments     : Input arguments None. Output argument is URL Metadata log file path for success scenario or details for failure scenario

Description   : Recieves webinterface request to get metadata of recorded urls, makes curl request to Media Sreamer
				via Web Inteface to get log file path and send it to Test Manager.
***************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_Recorded_Metadata(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Entry\n");
    string curlReqResult_Metadata, logFilePath_Metadata, line_Metadata;

    // Web Interface request for recording metadata
    curlReqResult_Metadata = curlRequest(RECORDING_URL_METADATA);

    if("FAILURE" == curlReqResult_Metadata)
    {
        response["result"] = "FAILURE";
        response["details"] = "Get Recorded_Data failed while getting the curl responce";
        DEBUG_PRINT(DEBUG_ERROR, "Get Recorded_Metadat failed while getting the curl responce\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Exit\n");
        return TEST_FAILURE;
    }

    // curlRequest returns recording metadata log path for success
    logFilePath_Metadata=curlReqResult_Metadata;
    DEBUG_PRINT(DEBUG_LOG, "logFilePath for url metadata is %s\n", logFilePath_Metadata.c_str());

    ifstream recMetadatamodFile;
    recMetadatamodFile.open(logFilePath_Metadata.c_str());
    if(recMetadatamodFile.is_open())
    {
        getline(recMetadatamodFile, line_Metadata); //Skip first line as it is not having recodrding metadata
        getline(recMetadatamodFile, line_Metadata);

        // To check whether recorded assets present or not
        if((line_Metadata.find("Recording #") == string::npos))
        {
            DEBUG_PRINT(DEBUG_ERROR, "There is no recorded assets present in the box\n");
            response["result"] = "SUCCESS";
            response["log-path"] = logFilePath_Metadata;
            recMetadatamodFile.close();
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Exit\n");
            return TEST_SUCCESS;
        }
        // Format checking for the recorded assets present
        while(!recMetadatamodFile.eof())
        {
            if(((line_Metadata.find("Recording #") != string::npos) && (line_Metadata.find("leaf_id") != string::npos) &&
                    (line_Metadata.find("seg_leaf_id=") != string::npos) && (line_Metadata.find("source_id=") != string::npos) &&
                    (line_Metadata.find("frequency=") != string::npos) && (line_Metadata.find("tuner_handle=") != string::npos) &&
                    (line_Metadata.find("record_handle=") != string::npos) && (line_Metadata.find("path=")!= string::npos) &&
                    (line_Metadata.find("start_time=") != string::npos) && (line_Metadata.find("start_time=") != string::npos) &&
                    (line_Metadata.find("requested_duration=") != string::npos) && (line_Metadata.find("min_length=") != string::npos) &&
                    (line_Metadata.find("audio PIDs") != string::npos) && (line_Metadata.find("video PIDs=") != string::npos) &&
                    (line_Metadata.find("data PIDs=") != string::npos) && (line_Metadata.find("status=") != string::npos )&&
                    (line_Metadata.find("ocap_status=")!= string::npos) && (line_Metadata.find("recorded_duration=") != string::npos) &&
                    (line_Metadata.find("recorded_size=") != string::npos)) != true)
            {
                DEBUG_PRINT(DEBUG_ERROR, "line that is not in format is %s\n", line_Metadata.c_str());
                response["result"] = "FAILURE";
                response["details"] = logFilePath_Metadata + " file is not in correct format";
                recMetadatamodFile.close();
                DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Exit\n");
                return TEST_FAILURE;
            }
            getline(recMetadatamodFile, line_Metadata);
        }
        response["result"] = "SUCCESS";
        response["details"] = "SUCCESS";
        response["log-path"] = logFilePath_Metadata;
        recMetadatamodFile.close();
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR, "Not able to open the file %s \n", logFilePath_Metadata.c_str());
        response["result"] = "FAILURE";
        response["details"] = "Unable to open " + logFilePath_Metadata + " file";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recorded_Metadata ---> Exit\n");
        return TEST_FAILURE;
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_Live_Playback

Arguments     : Input argument is OcapId. Output argument is "SUCCESS" or "FAILURE" and details

Description   : Receives the ocapid from Test Manager and makes curl request to Media Streamer via Web Interface
				for Live Tune and gets videoStreamingURL. Play the url using gstreamer plugin. Capture mediastreamer
				log from ocapri_log file. Search for the success pattern in the log and send the result to the Test Manager.
****************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_Live_Playback(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Live_Playback ---> Entry\n");
    string ocapid, webInterfaceStatus_Live, playurl_Live, errorStatus_Live;
    ocapid = request["ocapId"].asString();

    // Web Interface request for live tune
    webInterfaceStatus_Live=curlRequest(LIVE_TUNE_REQUEST, ocapid);
    DEBUG_PRINT(DEBUG_LOG, "webInterface response for Live tune is %s\n", webInterfaceStatus_Live.c_str());

    // Handling Web interface General Error
    if ("1" == webInterfaceStatus_Live)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface General Error\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is General Error";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    // Handling Web interface Resource Not Found
    else if ("2" == webInterfaceStatus_Live)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface Resource Not Found\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is Resource Not Found";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    if(webInterfaceStatus_Live.find("http://") == string::npos) // Checking curlRequest returns videoStreamingURL
    {
        response["result"] = "FAILURE";
        response["details"] = "Failed to get the video streaming url from webinterface";
        DEBUG_PRINT(DEBUG_ERROR, "Failed to get the video streaming url from webinterface\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Live_Playback ---> Exit\n");
        return TEST_FAILURE;
    }
    // CurlRequest returns videoStreamingURL for success scenario
    playurl_Live = webInterfaceStatus_Live;
    DEBUG_PRINT(DEBUG_LOG, "video streaming url is %s\n", playurl_Live.c_str());

    // To play the url and check the success pattern in log
    errorStatus_Live = playRequest(playurl_Live, false);
    DEBUG_PRINT(DEBUG_LOG, "Play request response is %s\n", errorStatus_Live.c_str());
    if("SUCCESS" == errorStatus_Live)
    {
        response["result"] = "SUCCESS";
        response["details"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Live_Playback ---> Exit\n");
        return TEST_SUCCESS;
    }
    response["result"] = "FAILURE";
    response["details"] = "Failed to play the url";
    DEBUG_PRINT(DEBUG_ERROR, "Failed to play the url\n");
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Live_Playback ---> Exit\n");
    return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_Recording_Playback

Arguments     : Input argument is OcapId. Output argument is "SUCCESS" or "FAILURE" and details

Description   : Gets the recordingid of a random url and makes curl request to Media Streamer via Web Inteface
				to get videoStreamingURL. Play the url using gstreamer plugin. Capture mediastreamer log from
				ocapri_log file. Search for the success pattern in the log and send the result to the Test Manager.
****************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_Recording_Playback(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Entry\n");
    string rec_id, webInterfaceStatus_Rec, playurl_Rec, errorStatus_Rec;

    // To get random recording id from url list
    rec_id = getRandomRecId();
    if("FAILURE" == rec_id)
    {
        DEBUG_PRINT(DEBUG_ERROR, "Recording_Playback failed while getting rec_id\n");
        response["result"] = "FAILURE";
        response["details"] = "get rec_id Failed";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    // If there is no recording asset present in box
    else if("NO_RECORD_ASSET" == rec_id)
    {
        response["result"] = "FAILURE";
        response["details"] = "There is no recording content present";
        DEBUG_PRINT(DEBUG_ERROR, "There is no recording content present\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Request ---> Exit\n");
        return TEST_FAILURE;
    }

    // Web interface request to get videoStreamingURL for the requested recording id
    DEBUG_PRINT(DEBUG_LOG,"webInterfaceStatus_Rec is %s\n",  webInterfaceStatus_Rec.c_str());
    webInterfaceStatus_Rec = curlRequest(RECORDING_REQUEST, rec_id);

    // Handling Web interface General Error
    if ("1" == webInterfaceStatus_Rec)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface General Error\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is General Error";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    // Handling Web interface Resource Not Found
    else if ("2" == webInterfaceStatus_Rec)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface Resource Not Found\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is Resource Not Found";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    else if(webInterfaceStatus_Rec.find("http://") == string::npos)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Recording_Playback failed while getting response from Web Interface\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface Failure";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    //curlRequest returns videoStreamingURL for success scenario
    playurl_Rec = webInterfaceStatus_Rec;

    // To play the url and check the success pattern in log
    errorStatus_Rec = playRequest(playurl_Rec, false);
    if("SUCCESS" == errorStatus_Rec)
    {
        response["result"] = "SUCCESS";
        response["details"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_SUCCESS;
    }
    response["result"] = "FAILURE";
    response["details"] = "Failed to play the url";
    DEBUG_PRINT(DEBUG_ERROR,"Failed to play the url\n");
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
    return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaStreamerAgent::MediaStreamerAgent_DVR_Trickplay

Arguments     : Input argument is playSpeed and timePosition. Output argument is "SUCCESS" or "FAILURE" and details

Description   : Gets the recordingid of a random url and makes curl request to Media Streamer via Web Inteface
				to get videoStreamingURL. Frames the playurl by appending play_speed and time_pos. Play it using
				gstreamer plugin. Capture mediastreamer log from ocapri_log file. Search for the success pattern
				in the log and send the result to the Test Manager.
****************************************************************************/
bool MediaStreamerAgent::MediaStreamerAgent_DVR_Trickplay(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Entry\n");
    string rec_id_Dvr, webInterfaceStatus_Dvr, play_speed_Dvr, time_pos_Dvr, playurl_Dvr, errorStatus_Dvr, successPattern_Dvr;

    // To get the random recording id from url list
    rec_id_Dvr = getRandomRecId();
    if("FAILURE" == rec_id_Dvr)
    {
        DEBUG_PRINT(DEBUG_ERROR,"DVR_Trickplay failed while getting rec_id\n");
        response["result"] = "FAILURE";
        response["details"] = "get rec_id Failed";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Exit\n");
        return TEST_FAILURE;
    }

    // If there is no recording asset present in box
    else if("NO_RECORD_ASSET" == rec_id_Dvr)
    {
        response["result"] = "FAILURE";
        response["details"] = "There is no recording content present";
        DEBUG_PRINT(DEBUG_ERROR, "There is no recording content present\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_RDVR_Trickplay ---> Exit\n");
        return TEST_FAILURE;
    }

    // Web interface request to get videoStreamingURL for the requested recording id
    webInterfaceStatus_Dvr = curlRequest(RECORDING_REQUEST, rec_id_Dvr);

    // Handling Web interface General Error
    if ("1" == webInterfaceStatus_Dvr)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface General Error\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is General Error";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    // Handling Web interface Resource Not Found
    else if ("2" == webInterfaceStatus_Dvr)
    {
        DEBUG_PRINT(DEBUG_ERROR,"WebInterface Resource Not Found\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface response is Resource Not Found";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_Recording_Playback ---> Exit\n");
        return TEST_FAILURE;
    }

    else if(webInterfaceStatus_Dvr.find("http://") == string::npos)
    {
        DEBUG_PRINT(DEBUG_ERROR,"DVR_Trickplay failed while getting response from Web Interface\n");
        response["result"] = "FAILURE";
        response["details"] = "WebInterface Failure";
        DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Exit\n");
        return TEST_FAILURE;
    }

    DEBUG_PRINT(DEBUG_LOG,"webInterfaceStatus_Dvr is %s\n",  webInterfaceStatus_Dvr.c_str());

    // Framing the url with videoStreamingURL, play_speed and time_pos for DVR trick play
    play_speed_Dvr = request["PlaySpeed"].asString();
    time_pos_Dvr = request["timePosition"].asString();

    DEBUG_PRINT(DEBUG_LOG,"webInterfaceStatus_Dvr is %s\n",  webInterfaceStatus_Dvr.c_str());
    DEBUG_PRINT(DEBUG_LOG,"play_speed_Dvr is %s\n",  play_speed_Dvr.c_str());
    DEBUG_PRINT(DEBUG_LOG,"time_pos_Dvr is %s\n",  time_pos_Dvr.c_str());

    playurl_Dvr = frameURL(webInterfaceStatus_Dvr, play_speed_Dvr, time_pos_Dvr);

    // To play the url and check the trick rate. PlayRequest function returns trick_rate for success scenario
    errorStatus_Dvr = playRequest(playurl_Dvr, true);
    DEBUG_PRINT(DEBUG_LOG,"errorStatus_Dvr is %s\n",  errorStatus_Dvr.c_str());

    DEBUG_PRINT(DEBUG_LOG,"play_speed_Dvr requested is %s\n", play_speed_Dvr.c_str());
    if(errorStatus_Dvr != "FAILURE")
    {
        if(errorStatus_Dvr == play_speed_Dvr)
        {
            response["result"] = "SUCCESS";
            response["details"] = "SUCCESS";
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Exit\n");
            return TEST_SUCCESS;
        }
        else
        {
            response["result"] = "FAILURE";
            response["details"] = "Url is playing with speed " + errorStatus_Dvr;
            DEBUG_PRINT(DEBUG_ERROR,"Url is playing with speed %s\n", errorStatus_Dvr.c_str());
            DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Exit\n");
            return TEST_FAILURE;
        }
    }
    response["result"] = "FAILURE";
    response["details"] = "Failed to play the url";
    DEBUG_PRINT(DEBUG_ERROR,"Failed to play the url\n");
    DEBUG_PRINT(DEBUG_TRACE, "MediaStreamerAgent_DVR_Trickplay ---> Exit\n");
    return TEST_FAILURE;
}
#endif
#ifdef RDK_BR_2DOT0

/**************************************************************************
Function name : MediaStreamerAgent::RMFStreamerAgent_InterfaceTesting

Arguments     : Input argument is RequestURL. Output argument is Error code from json Response and VideoStreamURL

Description   : Receives the RequestURL  from Test Manager and makes curl request to RMF Streamer via Web/Stream Interface
                                for Live Tune or Live playback. Gets the error code of Json Response sends it to the Test Manager.
***************************************************************************/
bool MediaStreamerAgent::RMFStreamerAgent_InterfaceTesting(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "RMFStreamerAgent_InterfaceTesting ---> Entry\n");

    string url = (char*)request["URL"].asCString();
    DEBUG_PRINT(DEBUG_LOG,"Incoming URL: %s\n",url.c_str());

    CURLcode curlResponse;
    CURL *curl;
    int errorResponse;
    FILE *filepointer;
    Json::Value root;

    /*Fetching the streaming interface IP: eth1 */
    size_t pos = 0;

    string streaming_interface = fetchStreamingInterface();
    size_t found = streaming_interface.find("FAILURE");
    if (found!=std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
            token = streaming_interface.substr(0, pos);
            DEBUG_PRINT(DEBUG_TRACE, "Token = %s\n", token.c_str());
            streaming_interface.erase(0, pos + delimiter.length());
        }
        response["result"]="FAILURE";
        response["details"]=token;
        return false;
    }
    else
    {
        string streamingip = GetHostIP(streaming_interface.c_str());
        string urlIn = url;
        string http = "http://";

        http.append(streamingip);

        DEBUG_PRINT(DEBUG_TRACE, "After appending streaming IP to http: %s\n",http.c_str());

        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);

        DEBUG_PRINT(DEBUG_TRACE, "HYBRID:Final URL passed to CURL(): %s\n",urlIn.c_str());

        try {
            DEBUG_PRINT(DEBUG_TRACE, "Curl init");
            curl = curl_easy_init();
            if(curl)
            {
                curl_easy_setopt(curl, CURLOPT_URL,(char *)urlIn.c_str());
                curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

                //write in to a file
                filepointer = fopen("rmf.json","wb");
                curl_easy_setopt( curl, CURLOPT_WRITEDATA, filepointer );
                DEBUG_PRINT(DEBUG_TRACE, "Curl perform");
                curlResponse = curl_easy_perform(curl);
                DEBUG_PRINT(DEBUG_ERROR,"The curlResponse value %d\n",curlResponse);
                fclose(filepointer);
                DEBUG_PRINT(DEBUG_TRACE, "Curl cleanup");
                curl_easy_cleanup(curl);
            }
        }
        catch(...)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Exception caught while doing curl operations\n");
            response["result"]="FAILURE";
            response["details"]="CURL operation failed";
            return false;
        }

        if(curlResponse != CURLE_OK)
        {
            fprintf(stderr, "curl_easy_perform() failed: %s \n",curl_easy_strerror(curlResponse));
            response["result"]="FAILURE";
            response["details"]="CURL API Failed";
            return false;
        }

        std::ifstream file;
        file.open("rmf.json");
        std::string temp;
        while(!file.eof())
        {
            getline(file,temp);
            DEBUG_PRINT(DEBUG_TRACE, "Read line: %s", temp.c_str());
            if(temp.find("NOT FOUND",0)!= string::npos)
            {
                response["result"] = "FAILURE";
                response["details"] = temp;
                break;
            }
            else if(temp.find("General Error",0)!= string::npos)
            {
                file.close();
                stringstream strStream;
                file.open("rmf.json");
                strStream << file.rdbuf();
                temp = strStream.str();
                response["result"] = "FAILURE";
                response["details"] = temp;
                break;
            }
            else if(temp.find("videoStreamingURL",0)!= string::npos)
            {
                file.close();
                file.open("rmf.json");
                file>>root;
                errorResponse=root["errorCode"].asInt();

                response["details"] = root["videoStreamingURL"].asString();

                DEBUG_PRINT(DEBUG_LOG,"\nJSON Response from MediaStreamer :-\n");
                DEBUG_PRINT(DEBUG_LOG,"\nErrorCode         : %d\n",root["errorCode"].asInt());
                DEBUG_PRINT(DEBUG_LOG,"\nErrorDescription  : %s \n",root["errorDescription"].asCString());
                DEBUG_PRINT(DEBUG_LOG,"\nVideoStreamingURL : %s\n",root["videoStreamingURL"].asCString());

                if(!errorResponse)
                {
                    response["result"] = "SUCCESS";
                    response["details"] = root["videoStreamingURL"].asCString();
                }
                else
                {
                    //Filling json response with FAILURE status and error message
                    response["result"] = "FAILURE";
                    response["details"] = "Failed to do Curl Request";
                }
                break;
            }
            else
            {
                continue;
            }
        }
        file.close();
        return true;
        DEBUG_PRINT(DEBUG_TRACE, "RMFStreamerAgent_InterfaceTesting ---> Exit\n");
        return TEST_SUCCESS;
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::RMFStreamerAgent__Player

Arguments     : Input argument is VideStreamURL and playtime. Output argument is player log

Description   : Receives the RequestURL  from Test Manager and makes to play RMF elemnts via HNSrc and MPSink
                Gets the return value from HNSrc->MPSink elements and send it to the Test Manager.
***************************************************************************/
bool MediaStreamerAgent::RMFStreamerAgent_Player(IN const Json::Value& request, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "RMFStreamerAgent_Player ---> Entry\n");

#ifdef USE_SOC_INIT
    //Initialize SOC
    soc_init(1, "tdk_agent", 1);
#endif

    int res_HNSrcGetState;
    int sleep_time = request["play_time"].asInt();
    int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcPlay, res_MPSinksetrect;
    int res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm, res_HNSrcClose;
    char* playuri = (char*)request["VideostreamURL"].asCString();

    string streamingip;
    string streaming_interface;
    size_t pos = 0;
    size_t found;
    streaming_interface=fetchStreamingInterface();
    found=streaming_interface.find("FAILURE");
    if (found!=std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
            token = streaming_interface.substr(0, pos);
            DEBUG_PRINT(DEBUG_TRACE, "Token = %s\n", token.c_str());
            streaming_interface.erase(0, pos + delimiter.length());
        }
        response["result"]="FAILURE";
        response["details"]=token;
        return false;
    }
    else
    {
        streamingip=GetHostIP(streaming_interface.c_str());
        string urlIn = playuri;

        MediaPlayerSink* pSink = new MediaPlayerSink();
        HNSource* pSource = new HNSource();
        RMFState curstate;

        res_HNSrcInit = pSource->init();
        DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

        if(0 != res_HNSrcInit)
        {
            response["result"] = "FAILURE";
            response["details"] = "Failed to Initialize hnsource";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }
        string http = "http://";

        http.append(streamingip);

        DEBUG_PRINT(DEBUG_TRACE, "Incoming URL: %s\n",playuri);
        DEBUG_PRINT(DEBUG_TRACE, "After appending streaming IP to http: %s\n",http.c_str());

        pos = urlIn.find(":8080");
        urlIn = urlIn.replace(0,pos,http);

        DEBUG_PRINT(DEBUG_TRACE, "HYBRID:Final URL passed to Open(): %s\n",urlIn.c_str());

        res_HNSrcOpen = pSource->open(urlIn.c_str(), 0);

        DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);
        if(0 != res_HNSrcOpen)
        {
            pSource->term();
            response["result"] = "FAILURE";
            response["details"] = "Failed to Open hnsource";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_MPSinkInit = pSink->init();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

        if(0 != res_MPSinkInit)
        {
            pSource->close();
            pSource->term();
            response["result"] = "FAILURE";
            response["details"] = "Failed to Initialze Mpsink";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_MPSinksetrect = pSink->setVideoRectangle(0, 0, 1280, 720, true);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

        if(0 != res_MPSinksetrect)
        {
            pSink->term();
            pSource->close();
            pSource->term();
            response["result"] = "FAILURE";
            response["details"] = "Failed to set Video resolution";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_MPSinksetsrc = pSink->setSource(pSource);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting source is %d\n", res_MPSinksetsrc);

        if(0 != res_MPSinksetsrc)
        {
            pSink->term();
            pSource->close();
            pSource->term();
            response["result"] = "FAILURE";
            response["details"] = "Failed to do set source";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_HNSrcPlay = pSource->play();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);
        sleep(sleep_time);

        if(0 != res_HNSrcPlay)
        {
            pSink->term();
            pSource->close();
            pSource->term();
            response["result"] = "FAILURE";
            response["details"] = "Failed to play video using Hnsource and Mpsink pipeline";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_HNSrcGetState = pSource->getState(&curstate, NULL);
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);

        if (curstate != RMF_STATE_PLAYING)
        {
            DEBUG_PRINT(DEBUG_ERROR, "HNSource Current State is not in RMF_STATE_PLAYING");
            response["result"] = "FAILURE";
            response["details"] = "HNSource Current State is not in RMF_STATE_PLAYING";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        res_MPSinkTerm = pSink->term();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPsink termination is %d\n", res_MPSinkTerm);

        res_HNSrcClose = pSource->close();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Hnsource close is %d\n", res_HNSrcClose);
        res_HNSrcTerm = pSource->term();
        DEBUG_PRINT(DEBUG_LOG, "RMF Result of Hnsource termination is %d\n", res_HNSrcTerm);
#ifdef USE_SOC_INIT
        // Uninitialize SOC
        soc_uninit();
#endif
        if(0 != res_MPSinkTerm)
        {
            response["result"] = "FAILURE";
            response["details"] = "Video played successfully, but failed to terminate MPSink";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        if(0 != res_HNSrcClose)
        {
            response["result"] = "FAILURE";
            response["details"] = "Video played successfully, but failed to close Hnsource";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        if(0 != res_HNSrcTerm)
        {
            response["result"] = "FAILURE";
            response["details"] = "Video played successfully, but failed to terminate Hnsource";
            DEBUG_PRINT(DEBUG_ERROR, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
            return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        response["details"] = "Video played successfully";
        DEBUG_PRINT(DEBUG_LOG, "Video played successfully\n");
        DEBUG_PRINT(DEBUG_TRACE, "RMFStreamer_HNSrcMPSink_Video_Play--->Exit\n");
        return TEST_SUCCESS;
    }
}
#endif
#ifdef RDK_BR_1DOT3
/**************************************************************************
Function name : MediaStreamerAgent::curlRequest()

Arguments     : Input arguments are mode(Live or Recording) and Id(OcapId or Recording Id). Output argument is errorstatus

Description   : Returns videoStreamingURL
***************************************************************************/
string MediaStreamerAgent::curlRequest(Mode mode, string id)
{
    DEBUG_PRINT(DEBUG_TRACE, "curlRequest with Id ---> Entry\n");
    int curl_Res, errorCode;
    Json::Value root;
    string queryurl_id, curlrequest_id, errorStatus, jsonFilePath;
    jsonFilePath = g_tdkPath + "/" + JSON_FILE_PATH;

    // Framing the url with the requested mode (live or recording) and id
    queryurl_id = frameURL(mode, id);
    DEBUG_PRINT(DEBUG_LOG,"queryurl is :%s\n",  queryurl_id.c_str());

    // Making curl request to media streamer and capturing json response to json file
    curlrequest_id = "curl " + queryurl_id + ">" + jsonFilePath;
    DEBUG_PRINT(DEBUG_LOG,"curlrequest_id is %s\n",  curlrequest_id.c_str());

    // To handle exception for system call
    try
    {
        curl_Res = system((char *)curlrequest_id.c_str());
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest with Id ---> Exit\n");
        return "FAILURE";
    }

    DEBUG_PRINT(DEBUG_LOG,"curl Response value is %d\n", curl_Res);
    if(curl_Res != 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"system command is failed on executing Curl\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest with Id ---> Exit\n");
        return "FAILURE";
    }

    // Extracting the error code from json file
    ifstream jsonFile;
    jsonFile.open(jsonFilePath.c_str());
    if(jsonFile.is_open())
    {
        jsonFile>>root;
        DEBUG_PRINT(DEBUG_LOG,"JSON Response from MediaStreamer \n");
        DEBUG_PRINT(DEBUG_LOG,"ErrorCode : %d\n", root["errorCode"].asInt());

        errorCode = root["errorCode"].asInt();

        // Converting errorCode int to string and assigning to errorStatus
        if(errorCode != 0)
        {
            ostringstream errorCodeString;
            errorCodeString << errorCode;
            errorStatus = errorCodeString.str();
        }
        else
        {
            //Returning videoStreamingURL for success case
            errorStatus = root["videoStreamingURL"].asString();
            DEBUG_PRINT(DEBUG_LOG,"videoStreamingURL is %s\n",errorStatus.c_str());
        }
        jsonFile.close();
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest with Id ---> Exit\n");
        return errorStatus;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Not able to open jfile.json file\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest with Id ---> Exit\n");
        return "FAILURE";
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::curlRequest()

Arguments     : Input argument is Mode mode. Output argument is log file path

Description   : Returns log file path
***************************************************************************/
string MediaStreamerAgent::curlRequest(Mode mode)
{
    DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Entry\n");
    int curl_Res_Info, script_Res;
    string queryurl_Info, curlReq_Info, logPath_Info, recListScriptPath, recListFilePath, recListModFilePath, recReq;
    recListScriptPath = g_tdkPath + "/" + RECORDED_LIST_SCRIPT_PATH;
    recListFilePath = g_tdkPath + "/" + RECORDED_LIST_PATH;
    recListModFilePath = g_tdkPath + "/" + RECORDED_LIST_MOD_PATH;

    // Framing the url with the requested mode (Url list or metadata)
    queryurl_Info = frameURL(mode);
    DEBUG_PRINT(DEBUG_LOG,"queryurl is :%s\n",  queryurl_Info.c_str());
    DEBUG_PRINT(DEBUG_LOG,"g_tdkPath is :%s\n",  g_tdkPath.c_str());

    // Making curl request to media streamer and capturing the response
    curlReq_Info = "curl " + queryurl_Info + ">" + recListFilePath;
    DEBUG_PRINT(DEBUG_LOG,"curlReq_Info is :%s\n",  curlReq_Info.c_str());

    // To handle exception for system call
    try
    {
        curl_Res_Info = system((char *)curlReq_Info.c_str());
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");
        return "FAILURE";
    }
    DEBUG_PRINT(DEBUG_LOG,"Curl Response value is %d\n", curl_Res_Info);

    if(curl_Res_Info != 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"system command is failed on executing Curl\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");
        return "FAILURE";
    }

    // Aligning the recording content(one entry per line)
    recReq = "source " + recListScriptPath + " " +recListFilePath + ">" + recListModFilePath;
    DEBUG_PRINT(DEBUG_LOG,"recReq is %s\n",  recReq.c_str());
    DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");

    // To handle exception for system call
    try
    {
        script_Res = system(recReq.c_str());
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");
        return "FAILURE";
    }

    if(script_Res != 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"system command is failed on executing %s\n",  recListScriptPath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");
        return "FAILURE";
    }
    logPath_Info = recListModFilePath;
    DEBUG_PRINT(DEBUG_LOG,"logPath_Info is %s\n",  logPath_Info.c_str());
    DEBUG_PRINT(DEBUG_TRACE, "curlRequest for Info ---> Exit\n");
    return logPath_Info;
}

/**************************************************************************
Function name : MediaStreamerAgent::getRandomRecId()

Arguments     : Input arguments None. Output argument is RecordingId

Description   : Returns RecordingId of a RandomUrl from recorded url list.
***************************************************************************/
string MediaStreamerAgent::getRandomRecId()
{
    DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Entry\n");
    string recordingid, curlReqResult, logFilePath, line, randurl;
    int start_pos_rec_id, end_pos_rec_id;
    vector<string> urlList; // To handle url list
    int randNum, urlListSize;

    // Web interface request to get url list
    curlReqResult = curlRequest(RECORDING_URL_LIST);
    if( "FAILURE" == curlReqResult)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Recording request failed while getting recording list from Web Interface\n");
        DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Exit\n");
        return "FAILURE";
    }

    // CurlRequest returns log path of recording url list for success scenario
    logFilePath = curlReqResult;

    ifstream recUrlListmodFile;
    recUrlListmodFile.open(logFilePath.c_str());
    DEBUG_PRINT(DEBUG_LOG,"logFilePath is %s\n",  logFilePath.c_str());

    // To check whether recorded assets present or not
    if(recUrlListmodFile.is_open())
    {
        getline(recUrlListmodFile, line);
        if((line.find("Recording #") == string::npos))
        {
            DEBUG_PRINT(DEBUG_ERROR,", There is no recorded assets present in the box\n");
            recUrlListmodFile.close();
            DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Exit\n");
            return "NO_RECORD_ASSET";
        }

        // Pushing the urls from file to urlList
        urlList.push_back(line);
        DEBUG_PRINT(DEBUG_LOG,"urlList.push_back() is %s\n", line.c_str());
        while(!recUrlListmodFile.eof())
        {
            getline(recUrlListmodFile, line);
            if(line != "</body></html>") // Skipping Last line which is not having url list data
            {
                urlList.push_back(line);
            }
        }

        // Removing empty element added at the end
        urlList.pop_back();
        recUrlListmodFile.close();
        urlListSize = urlList.size();

        // Generating random number between zero and size of urlList
        randNum = rand() %urlListSize;
        DEBUG_PRINT(DEBUG_LOG,"urlList.size() is %d\n", urlList.size());
        DEBUG_PRINT(DEBUG_LOG,"randNum is %d\n", randNum);

        // Fetching random url
        randurl = urlList[randNum];
        DEBUG_PRINT(DEBUG_LOG,"randurl is %s\n", randurl.c_str());

        // Checking for the presence of rec_id in the fetched random url and extracting recording id if present
        if((randurl.find("rec_id=") != string::npos) && (randurl.find("</code><br />DTCP/IP URL") != string::npos))
        {
            start_pos_rec_id = randurl.find("rec_id=") + REC_ID_START_POS_OFFSET;
            end_pos_rec_id = randurl.find("</code><br />DTCP/IP URL", start_pos_rec_id);
            recordingid=randurl.substr(start_pos_rec_id, end_pos_rec_id-start_pos_rec_id);
            DEBUG_PRINT(DEBUG_LOG,"recordingid is %s\n",  recordingid.c_str());
            DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Exit\n");
            return recordingid;
        }
        else
        {
            DEBUG_PRINT(DEBUG_ERROR, " file is not in correct format%s\n", logFilePath.c_str());
            DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Exit\n");
            return "FAILURE";
        }
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Not able to open %s\n", logFilePath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "getRandomRecId ---> Exit\n");
        return "FAILURE";
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::playRequest()

Arguments     : Input arguments are playurl and trickplay (true/false). Output argument is errorstatus

Description   : Returns error code
***************************************************************************/
string MediaStreamerAgent::playRequest(string playurl, bool trickplay)
{
    DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Entry\n");
    int playScript_Res, current_pos_start, first_frame_start_pos, next_frame_start_pos, transport_cmd_start_pos, trans_cmd, first_frame_number, next_frame_number;
    string playReq, playerScriptPath, ocapriLogPath, playerLogFilePath, mediaStreamerLogFilePath, line_MediaStreamer_Log, line_Player_Log, current_pos;
    string first_frame, next_frame, transport_cmd, trick_play_speed;
    bool first_frame_found = false;
    float play_speed;

    playerLogFilePath = g_tdkPath + "/" + PLAYER_LOG_PATH;
    mediaStreamerLogFilePath = g_tdkPath + "/" + MEDIA_STREAMER_LOG_PATH;
    playerScriptPath = g_tdkPath + "/" + PLAYER_SCRIPT_PATH;
    ocapriLogPath = OCAPRI_LOG_PATH;

    // Playing the url and capturing the log
    playurl = "\"" + playurl + "\"";
    playReq = "source " + playerScriptPath +  " " + playurl + " l " + mediaStreamerLogFilePath + " " +ocapriLogPath + "> " + playerLogFilePath;

    DEBUG_PRINT(DEBUG_LOG,"playReq is %s\n", playReq.c_str());
    try
    {
        playScript_Res = system(playReq.c_str());
    }
    catch(...)
    {
        DEBUG_PRINT(DEBUG_ERROR,"Exception occured\n");
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }
    DEBUG_PRINT(DEBUG_LOG,"playScript_Response is %d\n", playScript_Res);
    if(playScript_Res != 0)
    {
        DEBUG_PRINT(DEBUG_ERROR,"system command is failed on executing %s\n", playerScriptPath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }

    // Checking for the success pattern from mplayer log
    ifstream playerLogFile;
    playerLogFile.open(playerLogFilePath.c_str());
    if(playerLogFile.is_open())
    {
        while (!playerLogFile.eof())
        {
            getline(playerLogFile,line_Player_Log);
            if(line_Player_Log.find(SUCCESS_PATTERN) != string::npos)
            {
                current_pos_start =  line_Player_Log.find(SUCCESS_PATTERN) + CURRENT_POSITION_OFFSET;
                current_pos=line_Player_Log.substr(current_pos_start);
                DEBUG_PRINT(DEBUG_LOG,"current_pos is %s\n", current_pos.c_str());

                if(current_pos != "0")
                {
                    DEBUG_PRINT(DEBUG_LOG, "Current Position is %s Url is playing\n", current_pos.c_str());
                    if (trickplay == false)
                    {
                        playerLogFile.close();
                        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
                        return "SUCCESS";
                    }
                }
                else
                {
                    playerLogFile.close();
                    DEBUG_PRINT(DEBUG_ERROR,"Current Position is Zero. Url is not playing\n");
                    DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
                    return "FAILURE";
                }
            }
        }
        playerLogFile.close();
        DEBUG_PRINT(DEBUG_ERROR,"Search pattern not found.\n");
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Unable to open %s\n", playerLogFilePath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }

    // Checking trick rate for from ocapri log
    ifstream mediaStreamerLogFile;
    mediaStreamerLogFile.open(mediaStreamerLogFilePath.c_str());
    if(mediaStreamerLogFile.is_open())
    {
        while (!mediaStreamerLogFile.eof())
        {
            getline(mediaStreamerLogFile,line_MediaStreamer_Log);
            if(line_MediaStreamer_Log.find(FRAME_SEARCH_PATTERN) != string::npos)
            {
                if(first_frame_found == false)
                {
                    first_frame_start_pos =  line_MediaStreamer_Log.find(FRAME_SEARCH_PATTERN) + FRAME_SEARCH_OFFSET;
                    first_frame = line_MediaStreamer_Log.substr(first_frame_start_pos);
                    first_frame_found = true;
                }
                else
                {
                    next_frame_start_pos =  line_MediaStreamer_Log.find(FRAME_SEARCH_PATTERN) + FRAME_SEARCH_OFFSET;
                    next_frame = line_MediaStreamer_Log.substr(next_frame_start_pos);
                    stringstream(first_frame) >> first_frame_number;
                    stringstream(next_frame) >> next_frame_number;
                    play_speed = ((next_frame_number - first_frame_number) / FRAME_DIV_FACTOR);

                    // Converting play speed from float to string
                    ostringstream play_speedString;
                    play_speedString << play_speed;
                    trick_play_speed = play_speedString.str();

                    DEBUG_PRINT(DEBUG_LOG,"trick_play_speed is %s\n", trick_play_speed.c_str());
                    first_frame_found = false;
                    mediaStreamerLogFile.close();
                    DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
                    return trick_play_speed;
                }
            }
        }

        // Checking for slow rewind/slow forward trick rates from ocapri log
        mediaStreamerLogFile.clear();
        mediaStreamerLogFile.seekg(0, std::ios::beg);
        while (!mediaStreamerLogFile.eof())
        {
            getline(mediaStreamerLogFile,line_MediaStreamer_Log);
            if(line_MediaStreamer_Log.find(TRASPORT_CMD_PATTERN) != string::npos)
            {
                transport_cmd_start_pos = line_MediaStreamer_Log.find(TRASPORT_CMD_PATTERN) + TRASPORT_CMD_OFFSET;
                transport_cmd = line_MediaStreamer_Log.substr(transport_cmd_start_pos, TRASPORT_CMD_LENGTH);
                mediaStreamerLogFile.close();
                DEBUG_PRINT(DEBUG_LOG,"transport_cmd is %s\n",  transport_cmd.c_str());
                stringstream(transport_cmd) >> trans_cmd;
                switch(trans_cmd)
                {
                case TRANS_CMD_SLOW_REWIND :
                    trick_play_speed = "-0.500000";
                    DEBUG_PRINT(DEBUG_LOG,"trick_play_speed is %s\n",  trick_play_speed.c_str());
                    break;
                case TRANS_CMD_SLOW_FORWARD :
                    trick_play_speed = "0.500000";
                    DEBUG_PRINT(DEBUG_LOG,"trick_play_speed is %s\n",  trick_play_speed.c_str());
                    break;
                default :
                    trick_play_speed = "Unsupported";
                    DEBUG_PRINT(DEBUG_LOG,"trick_play_speed is %s\n",  trick_play_speed.c_str());
                    break;
                }
                mediaStreamerLogFile.close();
                DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
                return trick_play_speed;
            }
        }

        DEBUG_PRINT(DEBUG_ERROR,"Search pattern not found. Unable to find trick_play_speed %s\n", mediaStreamerLogFilePath.c_str());
        mediaStreamerLogFile.close();
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Unable to open %s\n",  mediaStreamerLogFilePath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "playRequest ---> Exit\n");
        return "FAILURE";
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::getRecorderId()

Arguments     : Input arguments None. Output argument is Recorder ID of gateway box

Description   : Returns RecorderId of gateway box
***************************************************************************/
string MediaStreamerAgent::getRecorderId()
{
    DEBUG_PRINT(DEBUG_TRACE, "getRecorderId ---> Entry\n");
    string recorderId, recorderIdFilePath;

    // Extract the recorder id from the wbdevice.dat file. Path is provided as RECORDER_ID_FILE_PATH
    ifstream recorderIdFile;
    recorderIdFilePath = RECORDER_ID_FILE_PATH;
    recorderIdFile.open(recorderIdFilePath.c_str());
    if(recorderIdFile.is_open())
    {
        getline(recorderIdFile,recorderId);
        DEBUG_PRINT(DEBUG_LOG,"recorderId is: %s\n",  recorderId.c_str());
        recorderIdFile.close();
        DEBUG_PRINT(DEBUG_TRACE, "getRecorderId ---> Exit\n");
        return recorderId;
    }
    else
    {
        DEBUG_PRINT(DEBUG_ERROR,"Unable to open file %s\n", recorderIdFilePath.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "getRecorderId ---> Exit\n");
        return NULL;
    }
}

/**************************************************************************
Function name : MediaStreamerAgent::frameURL()

Arguments     : Input arguments are mode(Live or Recording) and Id(OcapId or Recording Id). Output argument is validurl

Description   : Frames the valid URL depends on the required case. Returns the framed URL.
***************************************************************************/
string MediaStreamerAgent::frameURL(Mode mode, string Id)
{
    DEBUG_PRINT(DEBUG_TRACE, "frameURL with mode and id ---> Entry\n");
    string validurl;
    string streamingip;
    string streaming_interface;
    size_t pos = 0;
    size_t found;
    streaming_interface=fetchStreamingInterface();
    found=streaming_interface.find("FAILURE");
    if (found!=std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
            token = streaming_interface.substr(0, pos);
            DEBUG_PRINT(DEBUG_TRACE, "Token = %s\n", token.c_str());
            streaming_interface.erase(0, pos + delimiter.length());
        }
        validurl=token;
    }
    else
    {

        streamingip=GetHostIP(streaming_interface);
        switch(mode)
        {
        case LIVE_TUNE_REQUEST:
            validurl = "http://"+streamingip+":8080/videoStreamInit?recorderId="+getRecorderId()+"live="+Id;
            break;
        case RECORDING_REQUEST:
            validurl = "http://"+streamingip+":8080/videoStreamInit?recorderId="+getRecorderId()+"recordingId="+Id;
            break;
        default :
            break;
        }
        DEBUG_PRINT(DEBUG_LOG,"framedURL is: %s\n",  validurl.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "frameURL with mode and id ---> Exit\n");
    }
    return validurl;
}

/**************************************************************************
Function name : MediaStreamerAgent::frameURL()

Arguments     : Input arguments are playurl, play_speed and time_pos. Output argument is validurl

Description   : Frames the valid URL depends on the required case. Returns the framed URL.
***************************************************************************/
string MediaStreamerAgent::frameURL(string playurl, string play_speed, string time_pos)
{
    DEBUG_PRINT(DEBUG_TRACE, "frameURL with playurl, play_speed and time_pos ---> Entry\n");
    string validUrl_TrickPlay;

    //for Live or Recording Playback at normal speed
    if("1.000000" == play_speed)
    {
        validUrl_TrickPlay = playurl;
    }

    //for TrickPlay on Recorded assets
    else
    {
        validUrl_TrickPlay = playurl+"&play_speed="+play_speed+"&time_pos="+time_pos;
    }
    DEBUG_PRINT(DEBUG_LOG,"framedURL is:%s\n", validUrl_TrickPlay.c_str());
    DEBUG_PRINT(DEBUG_TRACE, "frameURL with playurl, play_speed and time_pos ---> Exit\n");
    return validUrl_TrickPlay;
}

/**************************************************************************
Function name : MediaStreamerAgent::frameURL()

Arguments     : Input argument Enum Mode. Output argument is validurl

Description   : Frames the valid URL depends on the required case. Returns the framed URL.
***************************************************************************/
string MediaStreamerAgent::frameURL(Mode mode)
{
    DEBUG_PRINT(DEBUG_TRACE, "frameURL with mode ---> Entry\n");
    string validUrl_Info;
    string streamingip;
    string streaming_interface;
    size_t pos = 0;
    size_t found;
    streaming_interface=fetchStreamingInterface();
    found=streaming_interface.find("FAILURE");
    if (found!=std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        while ((pos = streaming_interface.find(delimiter)) != std::string::npos) {
            token = streaming_interface.substr(0, pos);
            DEBUG_PRINT(DEBUG_TRACE, "Token = %s\n", token.c_str());
            streaming_interface.erase(0, pos + delimiter.length());
        }
        validUrl_Info=token;
    }
    else
    {
        streamingip = GetHostIP(streaming_interface);
        switch(mode)
        {
        case RECORDING_URL_LIST:

            validUrl_Info = "http://"+streamingip+":8080/vldms/info/recordingurls";
            break;
        case RECORDING_URL_METADATA:
            validUrl_Info = "http://"+streamingip+":8080/vldms/info/recordings";
            break;
        default :
            break;

        }
    }

    DEBUG_PRINT(DEBUG_LOG,"framedURL is: %s\n", validUrl_Info.c_str());
    DEBUG_PRINT(DEBUG_TRACE, "frameURL with mode ---> Exit\n");
    return validUrl_Info;
}
#endif
/**************************************************************************
Function name : MediaStreamerAgent::CreateObject()

Arguments     : NULL

Description   : create the object of MediaStreamerAgent
***************************************************************************/
extern "C" MediaStreamerAgent* CreateObject()
{
    DEBUG_PRINT(DEBUG_TRACE, "Creating MediaStreamer Agent Object\n");
    return new MediaStreamerAgent();
}

/**************************************************************************
Function name : MediaStreamerAgent::cleanup()

Arguments     : NULL

Description   :close things cleanly
***************************************************************************/
bool MediaStreamerAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaningup\n");
    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }
#ifdef RDK_BR_1DOT3
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_LiveTune_Request");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_Recording_Request");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_Recorded_Urls");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_Recorded_Metadata");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_Live_Playback");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_Recording_Playback");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaStreamer_DVR_Trickplay");
#endif
#ifdef RDK_BR_2DOT0
    ptrAgentObj->UnregisterMethod("TestMgr_RMFStreamer_InterfaceTesting");
    ptrAgentObj->UnregisterMethod("TestMgr_RMFStreamer_Player");
#endif
    /* All done, close things cleanly */
    return TEST_SUCCESS;

}

/**************************************************************************
Function name : MediaStreamerAgent::DestroyObject()

Arguments     : Input argument is MediaStreamerAgent Stub Object

Description   : Delete MediaStreamer stub object
***************************************************************************/
extern "C" void DestroyObject(MediaStreamerAgent *stubobj)
{
    DEBUG_PRINT(DEBUG_TRACE, "Destroying Object\n");
    delete stubobj;
}
