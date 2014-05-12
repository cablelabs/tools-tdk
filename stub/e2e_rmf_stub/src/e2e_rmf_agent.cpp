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

#include "e2e_rmf_agent.h"

/* Single Instance of HNsource and MediaplayerSink  */
static MediaPlayerSink *pSink = NULL;
static HNSource *pSource = NULL;




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

    std::cout << "Found IP: " << szAddressBuffer << std::endl;

    if (pIfAddrStruct != NULL)
    {
        freeifaddrs (pIfAddrStruct);
    }

    return szAddressBuffer;

} /* End of GetHostIP */



/* Time taken to tune the channel.
	totalTuningTime = (time difference of HNSrc->open() API call and return) + (time difference of HNSrc->play() API call and return)
 */
static float totalTuningTime;
/**************************************************************************
Function name : init_open_HNsrc_MPsink

Arguments     : Input argument is Playback URL, mime, Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper function to initialize, open HnSrc and MpSink component. 
****************************************************************************/
int init_open_HNsrc_MPsink(const char *url,char *mime,OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	RMFResult retMPSinkValue = RMF_RESULT_SUCCESS;

	pSource = new HNSource();
	pSink =  new MediaPlayerSink();	
	
	if(pSource == NULL)
	{
		response["result"] = "FAILURE";
                response["details"] = "HNSource instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource instance creation failed\n");

                return TEST_FAILURE;
	}

	if(pSink == NULL)
	{
		response["result"] = "FAILURE";
                response["details"] = "MPSink instance creation failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance creation failed\n");

                return TEST_FAILURE;
	}

        retHNSrcValue = pSource->init();
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource initialization failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource initialization failed %ld\n",retHNSrcValue);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc init\n");
	
	Time tuneTime;
	struct timeval startTime, endTime;
	int sTime = 0, eTime = 0;
	RMFResult retResult = RMF_RESULT_SUCCESS;

#if ENABLE_XG1_CODECOMPILE
	/*Fetching the streming interface IP: eth1 */
        string streamingip;
		
	streamingip=GetHostIP("eth1");
	string urlIn = url;
	string http = "http://";

        http.append(streamingip);

	cout<<"Incoming url: "<<url<<endl;
	cout<<"After appending streaming IP to http: "<<http<<endl;

        cout<<"IP:"<<streamingip<<endl;
	size_t pos = 0;
	pos = urlIn.find(":8080");
	urlIn = urlIn.replace(0,pos,http);
		
	cout<<"Final URL passed to Open(): "<<urlIn<<endl;
        retHNSrcValue = pSource->open(urlIn.c_str(),mime);

	DEBUG_PRINT(DEBUG_TRACE, "XG1:Passed Open() with streamingIP URL\n");
#else
	sTime = tuneTime.getTime(&startTime);
        retHNSrcValue = pSource->open(url,mime);
	eTime = tuneTime.getTime(&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "XI3:Passed Open() without streamingIP URL\n");
#endif

        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource open failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource open failed %ld\n",retHNSrcValue);
	
		pSource->term();		

                return TEST_FAILURE;
        }
	
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc open\n");
	
	/* TuningTime */	
	totalTuningTime = tuneTime.ExecutionTime(sTime,&startTime,eTime,&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "open() tune time: %f in ms (milli seconds)\n",totalTuningTime);

        retMPSinkValue = pSink->init();
        if(RMF_RESULT_SUCCESS != retMPSinkValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "MPSink initialization failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink initialization failed %ld\n",retMPSinkValue);

		//Source close and terminate before exiting.		
		pSource->close();
		pSource->term();	
	
                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink init\n");

        retMPSinkValue = pSink->setVideoRectangle(X_VALUE, Y_VALUE, WIDTH, HEIGHT, 0);
        if(RMF_RESULT_SUCCESS != retMPSinkValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "MPSink setVideoRectangle failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink setVideoRectangle failed %ld\n",retMPSinkValue);

		//Source close and terminate before exiting.		
		pSource->close();
		pSource->term();

		//Sink terminate
		 pSink->term();
	
                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink set video rectangle\n");

        retMPSinkValue = pSink->setSource(pSource);
        if(RMF_RESULT_SUCCESS != retMPSinkValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "MPSink setSource failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource failed %ld\n",retMPSinkValue);

		//Source close and terminate before exiting.		
		pSource->close();
		pSource->term();

		//Sink terminate
		pSink->term();

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed MP Sink setSource\n");
	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

        return TEST_SUCCESS;
}


/**************************************************************************
Function name : close_Term_HNSrc_MPSink

Arguments     : Input argument is Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper function to close, terminate HnSrc and MpSink component. 
****************************************************************************/
int close_Term_HNSrc_MPSink(OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	RMFResult retMPSinkValue = RMF_RESULT_SUCCESS;
    
	retHNSrcValue = pSource->close();
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource close failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource close failed %ld\n",retHNSrcValue);

        	retMPSinkValue = pSink->term();
        	retHNSrcValue = pSource->term();

		delete pSink;
		delete pSource;

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed Hnsrc close\n");

        retMPSinkValue = pSink->term();
        if(RMF_RESULT_SUCCESS != retMPSinkValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "MPSink termination failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink termination failed %ld\n",retMPSinkValue);
		
		pSource->term();
		delete pSource;

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed MPSink term\n");

        retHNSrcValue = pSource->term();
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource termination failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource termination failed %ld\n",retHNSrcValue);

        	retMPSinkValue = pSink->term();
		delete pSink;

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed Hnsrc term\n");

	delete pSource;
	delete pSink;

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

        return TEST_SUCCESS;
}

/**************************************************************************
Function name : changePlaySpeed

Arguments     : Input argument is Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper function to perform the trickplay (forward/rewind). 
****************************************************************************/
bool changePlaySpeed(float newSpeed,OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	retHNSrcValue = pSource->setSpeed(newSpeed);
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);

                return TEST_FAILURE;
        }

	sleep(10);	
	
	float curSpeed = 0.0;	
	pSource->getSpeed(curSpeed);
	
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay current rate: %f\n",curSpeed);

        if(newSpeed != curSpeed)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource failed to change speed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to change speed\n");

                return TEST_FAILURE;
        }
	
	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : parseProcVideoStatus

Arguments     : Input argument is Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper Function to parse the /proc/video_status to check whther is video is playing
               video_status: will be "yes" if playing, "no" if not playing. 
****************************************************************************/
bool parseProcVideoStatus(OUT Json::Value& response) 
{
	FILE *fp = NULL;
	char resultBuffer[BUFFER_LENGTH] = {'\0'};		
	char cmd[CMD_LENGTH] = CMD;

	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	/* Reading the /proc/video_status to no whether video is playing or not */
	fp = popen(cmd,"r");
	
	if(fp == NULL) 
	{
		response["result"] = "FAILURE";
	        response["details"] = "Popen error, popen failed to open";
		DEBUG_PRINT(DEBUG_ERROR, "Popen error, popen failed to open\n");

                return TEST_FAILURE;
        }

        if(fgets(resultBuffer,BUFFER_LENGTH,fp)!= NULL) 
	{
		DEBUG_PRINT(DEBUG_TRACE, "Result of /proc/video_status: %s\n",resultBuffer);
	}
	else
	{	
		response["result"] = "FAILURE";
	        response["details"] = "Cannot read /proc/videos_status";
		DEBUG_PRINT(DEBUG_ERROR, "Cannot read /proc/videos_status\n");

                return TEST_FAILURE;
        }
	
	if(0 == strncmp(resultBuffer,"no",2))
	{
		response["result"] = "FAILURE";
	        response["details"] = "Video not playing.";
		DEBUG_PRINT(DEBUG_ERROR, "Video not playing\n");

                return TEST_FAILURE;
	}

	if(0 == strncmp(resultBuffer,"yes",3))	
	{
		DEBUG_PRINT(DEBUG_TRACE, "Video playing.\n");
	}

        pclose(fp);

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : skipNumberOfSeconds

Arguments     : Input argument is number of seconds to skip, to skip forward or backward and Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper function, To skip forward and backward for a given number of seconds form the current point. 
****************************************************************************/
bool skipNumberOfSeconds(int numberOfSec, int direction, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);
	
	double time = 0.0;	
	retHNSrcValue = pSource->getMediaTime(time);
	if(direction == SKIP_FORWARD)		
	{
                retHNSrcValue = pSource->setMediaTime(time + numberOfSec);
                if(RMF_RESULT_SUCCESS != retHNSrcValue)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSource setMediaTime failed.\n";
                        DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.");

                        return TEST_FAILURE;
                }
		DEBUG_PRINT(DEBUG_TRACE, " Skip Forward: %d Done.\n",numberOfSec);
	}
	else
	{
		retHNSrcValue = pSource->setMediaTime(time - numberOfSec);
                if(RMF_RESULT_SUCCESS != retHNSrcValue)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSource setMediaTime failed.\n";
                        DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.");

                        return TEST_FAILURE;
                }
		DEBUG_PRINT(DEBUG_TRACE, " Skip Backward: %d Done.\n",numberOfSec);
	}

	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : playPause

Arguments     : Input argument Json object. Output argument is "SUCCESS" or "FAILURE". 

Description   : Helper function to perform play and pause on video playback. 
****************************************************************************/
bool playPause(OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;	
	DEBUG_PRINT(DEBUG_TRACE, " Entered into %s\n",__FUNCTION__);

	retHNSrcValue = pSource->play();
	 sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play \n");
	
        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(25);

	retHNSrcValue = pSource->pause();
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource pause failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue)
        {
		response["result"] = "FAILURE";
                response["details"] = "HNSource getState failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource getState failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	if (RMF_STATE_PAUSED == curState)
        {
		response["result"] = "SUCCESS";
	        response["details"] = "DVR Play pause Successful ";
		DEBUG_PRINT(DEBUG_ERROR, "DVR Play pause Successful \n");
	}
	
	sleep(10);
	
	DEBUG_PRINT(DEBUG_TRACE, "Passed %s\n",__FUNCTION__);

	return TEST_SUCCESS;
}

/*************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent

Arguments     : NULL

Description   : Constructor for E2ERMFAgent class
***************************************************************************/

E2ERMFAgent::E2ERMFAgent()
{
	DEBUG_PRINT(DEBUG_ERROR, "E2ERMFAgent Initialized\n");
}

typedef std::list<std::pair<float, float> > range_list_t;

/**************************************************************************
Function name : E2ERMFAgent::initialize

Arguments     : Input arguments are Version string and E2ERMFAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
*****************************************************************************/
bool E2ERMFAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "E2ERMF Initialize----->Entry\n");
	
	/* E2E DVR TrickPlay */
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_LinearTv_Dvr_Play, "TestMgr_LinearTv_Dvr_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause, "TestMgr_Dvr_Play_Pause");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Pause_Play, "TestMgr_Dvr_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_FF_FR, "TestMgr_Dvr_Play_TrickPlay_FF_FR");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause_Play, "TestMgr_Dvr_Play_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_Repeat, "TestMgr_Dvr_Play_Pause_Play_Repeat");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point, "TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Forward_Play, "TestMgr_Dvr_Skip_Forward_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_Middle, "TestMgr_Dvr_Skip_Forward_From_Middle");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_End, "TestMgr_Dvr_Skip_Forward_From_End");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_End, "TestMgr_Dvr_Skip_Backward_From_End");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Middle, "TestMgr_Dvr_Skip_Backward_From_Middle");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Starting, "TestMgr_Dvr_Skip_Backward_From_Starting");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Rewind_Forward, "TestMgr_Dvr_Play_Rewind_Forward");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Forward_Rewind, "TestMgr_Dvr_Play_Forward_Rewind");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_FF_FR_Pause_Play, "TestMgr_Dvr_Play_FF_FR_Pause_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause_FF_FR, "TestMgr_Dvr_Play_Pause_FF_FR");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_SF_SB, "TestMgr_Dvr_Play_Pause_Play_SF_SB");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_FF_FR_SF_SB, "TestMgr_Dvr_Play_FF_FR_SF_SB");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Pause_Pause, "TestMgr_Dvr_Play_Pause_Pause");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_Play_Play, "TestMgr_Dvr_Play_Play");
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_GETURL, "TestMgr_LiveTune_GETURL");

	/* E2E RF Video */
	ptrAgentObj->RegisterMethod(*this,&E2ERMFAgent::E2ERMFAgent_ChannelChange, "TestMgr_RF_Video_ChannelChange");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   :Sends the URL to XG1 to playback the video. URL can be Linear TV or DVR URL. 
 **************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_LinearTv_Dvr_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	
	/*Check for the play_speed, from the input URL */	
	int playSpeedStrPosition = url.find("play_speed");
	float urlSpeed = 0.0;
	

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
		stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play\n");
	
	/*Only for DVR Trick Play, Extract the trickPlay rate from the url.*/	
	if(NOT_PRESENT != playSpeedStrPosition)
	{
		string playSpeed = url.substr(playSpeedStrPosition);
		int ePos = playSpeed.find("=");
		int aPos = playSpeed.find("&");
		string rate = playSpeed.substr(ePos + 1,(aPos - ePos) - 1);

		urlSpeed = strtof(rate.c_str(),NULL);			
		DEBUG_PRINT(DEBUG_TRACE, "URL appended Rate: %f\n",urlSpeed);
	}

	/*Query the current speed */	
	float curSpeed = 0.0;
        pSource->getSpeed(curSpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	sleep(60);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	if(NOT_PRESENT != playSpeedStrPosition)
	{	
		/*Compare the queried speed with requested speed */
		if(curSpeed != urlSpeed)
		{
			response["result"] = "FAILURE";
        		response["details"] = "Playback failed to play in the specified speed";
		        DEBUG_PRINT(DEBUG_ERROR, "Playback failed to play in the specified speed\n");
			
			return TEST_FAILURE;	
		}
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Playback Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Playback Successful \n");
	
	return TEST_SUCCESS;
}
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Play and Pause on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause(IN const Json::Value& req, OUT Json::Value& response)
{
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	if(TEST_FAILURE == playPause(response))
	{
		return TEST_FAILURE;
	}
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Pause and Play on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();
	
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
#if 1	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
        cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
#endif
	
	sleep(1);

	/*Query the current speed */	
	float curSpeed = 0.0;
        pSource->getSpeed(curSpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource failed to pause.";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to pause.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	sleep(5);
	
	float changeSpeed = 1.0;	
	
	retHNSrcValue = pSource->setSpeed(changeSpeed);
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		close_Term_HNSrc_MPSink(response);

		response["result"] = "FAILURE";
                response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);

                return TEST_FAILURE;
        }
	
	sleep(1);

        retHNSrcValue = pSource->getState(&curState, &pendingState);
	if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state is not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state is not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	sleep(40);

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
        response["details"] = "Pause Play is Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Pause Play Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_FF_FR

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Play and can perform trickplay(forward/rewind in different rate) on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_FF_FR(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
        DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play\n");

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(40);

	float changeSpeed = req["speed"].asFloat();	

	if(TEST_FAILURE == changePlaySpeed(changeSpeed,response))	
	{
		close_Term_HNSrc_MPSink(response);
		
		return TEST_FAILURE;	
	}
        DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed success.\n");
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
        response["details"] = "DVR Trickplay Fast Forward/Rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "DVR Trickplay Fast Forward/Rewind Successful \n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Play still the end of recording and can perform trickplay(rewind in different rate) on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_TrickPlay_Rewind_From_End_Point(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float changeSpeed = req["rewindSpeed"].asFloat();
	
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay RewindSpeed: %f\n",changeSpeed);
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

	/*Query the current speed */	
	float curSpeed = 0.0;
        pSource->getSpeed(curSpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Current Speed: %f\n",curSpeed);

/*      FIXME: Need to figure out the way to get the Total video duration.

	//MediaInfo: startTime and Duration.
	RMFMediaInfo mediaInfo;
        pSource->getMediaInfo(mediaInfo);
	cout << "Duration of Video: " << mediaInfo.m_duration << endl; 
	cout << "StartTime of Video: " << mediaInfo.m_startTime << endl; 
*/
        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	sleep(20);

	/*Aussuming the total duration for 2mins. i.e,120 seconds*/
	double seekToEndPoint = 120;
	retHNSrcValue = pSource->setMediaTime(seekToEndPoint);
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource setMediaTime failed.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	retHNSrcValue = pSource->setSpeed(changeSpeed);
        if(RMF_RESULT_SUCCESS != retHNSrcValue)
        {
		close_Term_HNSrc_MPSink(response);

		response["result"] = "FAILURE";
                response["details"] = "HNSource setSpeed failed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource  setSpeed failed %ld\n",retHNSrcValue);

                return TEST_FAILURE;
        }
	
	sleep(5);	
	
	curSpeed = 0.0;	
	pSource->getSpeed(curSpeed);
	DEBUG_PRINT(DEBUG_TRACE, "TrickPlay current speed: %f\n",curSpeed);
        if(changeSpeed != curSpeed)
        {
		close_Term_HNSrc_MPSink(response);
		
		response["result"] = "FAILURE";
                response["details"] = "HNSource failed to change speed";
		DEBUG_PRINT(DEBUG_ERROR, "HNSource failed to change speed\n");

                return TEST_FAILURE;
        }

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Rewind from end point Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Rewind from end point Successful \n");
	
	return TEST_SUCCESS;
}

#if 1 
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Play, pause and play on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	if(TEST_FAILURE == playPause(response))
	{
		return TEST_FAILURE;
	}

	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);

		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	sleep(20);	
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}

	return TEST_SUCCESS;
}
#endif
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_Repeat

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And does Play, pause and play repeat the sequence multiple times on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_Repeat(IN const Json::Value& req, OUT Json::Value& response)
{
	int repeatCount = req["rCount"].asInt();
	
	DEBUG_PRINT(DEBUG_TRACE, " Repeat time: %d\n",repeatCount);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	for(int repeat = 0;repeat < repeatCount; repeat++)
	{	
		if(TEST_FAILURE == playPause(response))
		{	
			DEBUG_PRINT(DEBUG_TRACE, " Failure: %d repeatation\n",repeat + 1);
			stringstream ss;
			string details;
			
			ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
			details = ss.str();
			response["details"] = details;		
			
			return TEST_FAILURE;
		}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
	}

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "DVR Play Pause Play Repeat Successful";
	DEBUG_PRINT(DEBUG_TRACE, "DVR Play Pause Play Repeat Successful\n");
	
	return TEST_SUCCESS;
}



/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Forward_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips forward number of seconds on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Forward_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	
        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_TRACE, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )	
	{
		if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(5);
	}
	
	sleep(40);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip forward from starting of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from starting of video Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_Middle

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips forward number of seconds on the video being played when time position is half the total duration.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_Middle(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	

	/*FIXME: Don't no the Duration of the video. So, assuming middle of the video as 25 seconds.*/
	sleep(25);
	
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )
        {
                if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
                {
                        stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                        DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

                        close_Term_HNSrc_MPSink(response);

                        return TEST_FAILURE;
                }
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
                sleep(5);
        }
	
	sleep(30);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip forward from middle of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from middle of video Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_End

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips forward number of seconds on the video being played when time position is equal to the total duration.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Forward_From_End(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	/*FIXME: Don't no the Duration of the video. So, assuming end of the video as 40 seconds.*/
	sleep(40);
	
	if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_FORWARD,response))
	{
	        close_Term_HNSrc_MPSink(response);
                return TEST_FAILURE;
        }
	
	sleep(20);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip forward from end of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip forward from end of video Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_End

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips Backward number of seconds on the video being played when time position is equal to the total duration.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_End(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);
	DEBUG_PRINT(DEBUG_TRACE, "Number of repeatation: %d\n",numberOfRepeatation);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	/*FIXME: Don't no the Duration of the video. So, assuming end of the video as 40 seconds.*/
	sleep(40);
	
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )	
	{
		if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(5);
	}
	
	sleep(20);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip backward from end of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip backward from end of video Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Middle

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips Backward number of seconds on the video being played when time position is half to the total duration.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Middle(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	

	/*FIXME: Don't no the Duration of the video. So, assuming middle of the video as 25 seconds.*/
	sleep(25);
	
        if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
        {
                close_Term_HNSrc_MPSink(response);

	        return TEST_FAILURE;
        }
	sleep(30);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip Backward from middle of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip Backward from middle of video Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Starting

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Skips Backward number of seconds on the video that is being started playing.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Skip_Backward_From_Starting(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double mediaTime = req["seconds"].asDouble();

	DEBUG_PRINT(DEBUG_TRACE, "Number of seconds to skip: %f\n",mediaTime);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	
	sleep(3);

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	if (TEST_FAILURE == skipNumberOfSeconds(mediaTime,SKIP_BACKWARD,response))
	{
	      	close_Term_HNSrc_MPSink(response);

       		return TEST_FAILURE;
       	}
	
	sleep(40);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Skip backward from starting of video Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Skip backward from starting of video Successful \n");
	
	return TEST_SUCCESS;
}
 
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Rewind_Forward

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do rewind and forward for the given trickplay speed on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Rewind_Forward(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();

	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	
        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                cout << "Error: " << retHNSrcValue << " returned, HNsource playback failed current state not playing.\n";
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(20);
	
	/*Rewind it for some time.*/
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Rewind success passed \n");

	/*Forward it for some time*/
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, " Forward success passed \n");
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play rewind forward Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play rewind forward Successful");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Forward_Rewind

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do forward and rewind for the given trickplay speed on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Forward_Rewind(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();

	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	
	sleep(1);

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(20);
	
	/*Forward it for some time*/
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Forward success Passed \n");
	
	/*Rewind it for some time.*/
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Rewind success Passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play forward rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play forward rewind Successful");
	
	return TEST_SUCCESS;
}


/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_FF_FR_Pause_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do forward or rewind followed by pause and play on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_FF_FR_Pause_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float trickPlaySpeed = req["trickPlayRate"].asFloat();
	
	DEBUG_PRINT(DEBUG_TRACE, "Trick Play Speed: %f \n",trickPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(20);
	
	/*Forward/Rewind it for some time*/
	if(TEST_FAILURE == changePlaySpeed(trickPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "Forward/Rewind success passed\n");
	
	/*pause it for sometime */	
	retHNSrcValue = pSource->pause();
        DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);
	
	sleep(10);
		
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource pause failed current state not paused.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	/*Play it in normal speed 1.0*/
	float normalSpeed = 1.0;
	if(TEST_FAILURE == changePlaySpeed(normalSpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
        DEBUG_PRINT(DEBUG_TRACE, "Setting to normal speed success passed \n");
	
	sleep(10);

        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play forward/Rewind pause play Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play forward/Rewind pause play Successful");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause_FF_FR

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do pause and do forward/rewind on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause_FF_FR(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float trickPlaySpeed = req["trickPlayRate"].asFloat();
	
	DEBUG_PRINT(DEBUG_TRACE, " Trick Play Speed: %f\n",trickPlaySpeed);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
        cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");
	
        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(20);
	
	/*pause it for sometime */	
	retHNSrcValue = pSource->pause();
        DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);
	
	sleep(10);
		
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource pause failed current state not paused.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	/*Forward/Rewind it for some time*/
	if(TEST_FAILURE == changePlaySpeed(trickPlaySpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
        DEBUG_PRINT(DEBUG_TRACE, "Forward/Rewind success Passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play pause forward/Rewind Successful ";
	DEBUG_PRINT(DEBUG_TRACE, "Play pause forward/Rewind Successful");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_SF_SB

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do pause, play and skip forward/backward for the given number of seconds on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause_Play_SF_SB(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	double skipForwardSec = req["sfSeconds"].asDouble();
	double skipBackwardSec = req["sbSeconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();

	DEBUG_PRINT(DEBUG_TRACE, "Number Of repeatation: %d \n",numberOfRepeatation);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds forward: %f\n",skipForwardSec);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds backward: %f\n",skipBackwardSec);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, " Passed HNSrc play\n");

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(20);
	
	/*pause it for sometime */	
	retHNSrcValue = pSource->pause();
        DEBUG_PRINT(DEBUG_TRACE, "HNSource pause return value: %ld \n",retHNSrcValue);
	
	sleep(10);
		
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource pause failed current state not paused.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed current state not paused.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	
	/* FIXME: setSpeed not working in this sequence of API call. So, using play() */	
#if 0
	/*Play it in normal speed 1.0*/
	float normalSpeed = 1.0;
	if(TEST_FAILURE == changePlaySpeed(normalSpeed,response))
	{
		close_Term_HNSrc_MPSink(response);
	
		return TEST_FAILURE;
	}
	cout << "Log:" << "Setting to normal speed success: " <<  __FUNCTION__ << " Passed" << endl;
	sleep(10);

        retHNSrcValue = pSource->getState(&curState, &pendingState);
	cout << "Log: " << __LINE__ << ": getState() return: "<< retHNSrcValue << " Current State:"<< curState << endl;
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                cout << "Error: " << retHNSrcValue << " returned, HNsource playback failed current state not playing.\n";
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
#endif

	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE, "playing in normal speed success passed \n");
	
	sleep(10);
	
	/*Skip Forward/Backward for entered number of times*/
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )	
	{
		/*Skip Forward for skipForwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipForwardSec,SKIP_FORWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		sleep(15);

		/*Skip Backward for skipBackwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipBackwardSec,SKIP_BACKWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(15);
	}
	DEBUG_PRINT(DEBUG_TRACE, "Skip Forward/ Skip Backward success passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play pause play Skip Forward/Backward Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play pause play Skip Forward/Backward Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_FF_FR_SF_SB

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do forward/rewind for the given trickplay speed and skip forward/backward number of seconds given on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_FF_FR_SF_SB(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	string url = req["playUrl"].asCString();
	float rewindPlaySpeed = req["rewindSpeed"].asFloat();
	float forwardPlaySpeed = req["forwardSpeed"].asFloat();
	double skipForwardSec = req["sfSeconds"].asDouble();
	double skipBackwardSec = req["sbSeconds"].asDouble();
	int numberOfRepeatation = req["rCount"].asInt();
	
	DEBUG_PRINT(DEBUG_TRACE, "Number Of repeatation: %d\n",numberOfRepeatation);

	DEBUG_PRINT(DEBUG_TRACE, "Rewind Play Speed: %f\n",rewindPlaySpeed);
	DEBUG_PRINT(DEBUG_TRACE, "Forward Play Speed: %f\n",forwardPlaySpeed);

	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds forward: %f\n",skipForwardSec);
	DEBUG_PRINT(DEBUG_TRACE, "Skip Number of seconds backward: %f\n",skipBackwardSec);

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
                stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	sleep(15);
	
	/*Forward video in the speed given*/	
	if(TEST_FAILURE == changePlaySpeed(forwardPlaySpeed,response))	
	{
		close_Term_HNSrc_MPSink(response);
		
		return TEST_FAILURE;	
	}
	DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed forward success passed \n");
	
	sleep(5);	
	
	/*Backward video in the speed given*/	
	if(TEST_FAILURE == changePlaySpeed(rewindPlaySpeed,response))	
	{
		close_Term_HNSrc_MPSink(response);
		
		return TEST_FAILURE;	
	}
	DEBUG_PRINT(DEBUG_TRACE, "changePlaySpeed backward success passed \n");
	
	sleep(5);
	
	/*Skip Forward/Backward for entered number of times*/
	for (int repeat = 0; repeat < numberOfRepeatation; repeat++ )	
	{
		/*Skip Forward for skipForwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipForwardSec,SKIP_FORWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		sleep(15);

		/*Skip Backward for skipBackwardSec */
		if (TEST_FAILURE == skipNumberOfSeconds(skipBackwardSec,SKIP_BACKWARD,response))
		{
			stringstream ss;
                        string details;

                        ss << response["details"] << "and failed in " << repeat + 1 << "Repeatation";
                        details = ss.str();
                        response["details"] = details;
                	DEBUG_PRINT(DEBUG_ERROR, "HNSource setMediaTime failed and in repeatation %d.\n",repeat + 1);

	                close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		DEBUG_PRINT(DEBUG_TRACE, " Success: %d repeatation\n",repeat + 1);
		sleep(15);
	}
	DEBUG_PRINT(DEBUG_TRACE, "Skip Forward/ Skip Backward passed \n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play, Forward/Rewind and Skip Forward/Backward Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play, Forward/Rewind and Skip Forward/Backward Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Pause_Pause

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do Pause and Pause on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Pause_Pause(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();
	
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	retHNSrcValue = pSource->play();
	sleep(1);
        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
		stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");

	sleep(30);
	
	for (int repeat = 0; repeat < 2; repeat++)
	{	
		retHNSrcValue = pSource->pause();
        	if(RMF_RESULT_SUCCESS != retHNSrcValue)
	        {
        	        cout << "Error: " << retHNSrcValue << " returned, HNsource pause failed \n";
			response["result"] = "FAILURE";
        	        response["details"] = "HNSource pause failed";
			DEBUG_PRINT(DEBUG_ERROR, "HNSource pause failed %ld\n",retHNSrcValue);
		
			close_Term_HNSrc_MPSink(response);

        	        return TEST_FAILURE;
        	}
		sleep(10);	
		DEBUG_PRINT(DEBUG_TRACE, "HNSource pause called %d time.\n",repeat + 1);
	}

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PAUSED != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource pause failed current state not paused.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource paused failed current state not paused.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play, Pause and Pause on video playback Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play, Pause and Pause on video playback Successful \n");
	
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_Play_Play

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is DVR URL. 
		And Play for sometime, do Play  on the video being played.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_Play_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;
	string url = req["playUrl"].asCString();
	
	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}
	
	for (int repeat = 0; repeat < 2; repeat++)
	{	
		retHNSrcValue = pSource->play();
		sleep(1);
	        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        	{
			stringstream ss;
	                string details;

        	        ss << response["details"] << " HNSource play failed";
	                details = ss.str();
        	        response["details"] = details;

			DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
			close_Term_HNSrc_MPSink(response);

                	return TEST_FAILURE;
        	}
	        cout << "LOG Line:" << __LINE__ << " : Passed HNSrc play \n";
		DEBUG_PRINT(DEBUG_TRACE, "HNSource play called %d time.\n",repeat + 1);
		sleep(20);
	}

        RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);

        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                cout << "Error: " << retHNSrcValue << " returned, HNsource play failed current state not playing.\n";
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
        DEBUG_PRINT(DEBUG_TRACE, "HNSource getState() passed.\n");

	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
        response["details"] = "Play and Play on video playback Successful";
	DEBUG_PRINT(DEBUG_TRACE, "Play and Play on video playback Successful \n");
	
	return TEST_SUCCESS;
}

#if 1
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_ChannelChange

Arguments     : Input argument is Playback URL. Output argument is "SUCCESS" or "FAILURE". 

Description   : Sends the URL to XG1 to playback the video. URL is . 
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_ChannelChange(IN const Json::Value& req, OUT Json::Value& response)
{
	RMFResult retHNSrcValue = RMF_RESULT_SUCCESS;

	if(TEST_FAILURE == init_open_HNsrc_MPsink(req["playUrl"].asCString(),NULL,response))
	{
		return TEST_FAILURE;
	}

	Time tuneTime;
	struct timeval startTime, endTime;
	int sTime = 0, eTime = 0;
	
	sTime = tuneTime.getTime(&startTime);
	retHNSrcValue = pSource->play();
	eTime = tuneTime.getTime(&endTime);

	sleep(1);
	
	totalTuningTime += tuneTime.ExecutionTime(sTime,&startTime,eTime,&endTime);
	DEBUG_PRINT(DEBUG_TRACE, "Total time for tuning: %f in ms (milli seconds)\n",totalTuningTime);

        if(RMF_RESULT_SUCCESS != retHNSrcValue )
        {
		stringstream ss;
                string details;

                ss << response["details"] << " HNSource play failed";
                details = ss.str();
                response["details"] = details;

		DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed %ld\n",retHNSrcValue);
		
		close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	DEBUG_PRINT(DEBUG_TRACE, "Passed HNSrc play \n");
        
	RMFState curState, pendingState;
        retHNSrcValue = pSource->getState(&curState, &pendingState);
	
        if(RMF_STATE_CHANGE_SUCCESS != retHNSrcValue || RMF_STATE_PLAYING != curState)
        {
                response["result"] = "FAILURE";
                response["details"] = "HNSource play failed current state not playing.\n";
                DEBUG_PRINT(DEBUG_ERROR, "HNSource play failed current state not playing.\n");

                close_Term_HNSrc_MPSink(response);

                return TEST_FAILURE;
        }
	
	sleep(5);
	
	if(TEST_FAILURE == close_Term_HNSrc_MPSink(response))
	{
		return TEST_FAILURE;
	}
	
	stringstream sst1,sst2;
	string strTuningTime;
	
	sst1 << totalTuningTime;	
	strTuningTime = sst1.str();
	
	sst2 << "{'summary':'Channel Tuning Successful','tuningtime':'" << strTuningTime << "'}";

	response["result"] = "SUCCESS";
        response["details"] = sst2.str();
	DEBUG_PRINT(DEBUG_TRACE, "Channel Tuning Successful \n");

	return TEST_SUCCESS;
}
#endif
/**************************************************************************
Function name : E2ERMFAgent::E2ERMFAgent_GetURL

Arguments     : IN const Json::Value,OUT Json::Value

Description   : Send the URL to the Mediastreamer get the valid URL in the Json Response.
                Return the Error code and Error Description to the testFramework.
***************************************************************************/
bool E2ERMFAgent::E2ERMFAgent_GETURL(IN const Json::Value& request, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_LOG,"\nE2ERMF::E2ERMF_GETURL---Entry\n");
	CURL *curl;
	CURLcode curlResponse;
	int errorResponse;
	FILE *filepointer;
	string url="";
	Json::Value root;
	url=(char*)request["Validurl"].asCString();


	DEBUG_PRINT(DEBUG_LOG,"\nValidurl form TestFramework : %s\n",request["Validurl"].asCString());

	curl = curl_easy_init();
	if(curl)
	{
		curl_easy_setopt(curl, CURLOPT_URL,(char *)url.c_str());
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

		//write in to a file
		filepointer=fopen("jsonfile.json","wb");
		curl_easy_setopt( curl, CURLOPT_WRITEDATA, filepointer ) ;
		curlResponse= curl_easy_perform(curl);
		DEBUG_PRINT(DEBUG_ERROR,"The curlResponse value %d\n",curlResponse);
		fclose(filepointer);
	}

	if(curlResponse != CURLE_OK)
	{
		fprintf(stderr, "curl_easy_perform() failed: %s \n",curl_easy_strerror(curlResponse));
		response["result"]="FAILURE";
		return TEST_FAILURE;
	}

	curl_easy_cleanup(curl);

	ifstream file("jsonfile.json");
	file>>root;
	errorResponse=root["errorCode"].asInt();

	response["details"]=root["videoStreamingURL"].asString();

	DEBUG_PRINT(DEBUG_LOG,"\nJSON Response from MediaStreamer :-\n");
	DEBUG_PRINT(DEBUG_LOG,"\nErrorCode         : %d\n",root["errorCode"].asInt());
	DEBUG_PRINT(DEBUG_LOG,"\nErrorDescription  : %s \n",root["errorDescription"].asCString());
	DEBUG_PRINT(DEBUG_LOG,"\nVideoStreamingURL : %s\n",root["videoStreamingURL"].asCString());

	if(!errorResponse)
	{
		response["result"]="SUCCESS";
	}
	else
	{
		//Filling json response with FAILURE status and error message
		response["result"]="FAILURE";

	}

	DEBUG_PRINT(DEBUG_LOG,"\nE2ERMF::E2ERMF_GETURL---Exit\n");
	return TEST_SUCCESS;

}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "E2ERMFAgent".
 **************************************************************************/
extern "C" E2ERMFAgent* CreateObject()
{
	return new E2ERMFAgent();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
***************************************************************************/
bool E2ERMFAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "cleaningup and Exiting E2ERMFAgent\n");

	if(NULL == ptrAgentObj)
	{
		return TEST_FAILURE;
	}

	/* E2E DVR TrickPlay */
	ptrAgentObj->UnregisterMethod("TestMgr_LinearTv_Dvr_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_TrickPlay_FF_FR");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play_Repeat");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_TrickPlay_RewindFromEndPoint");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_From_Middle");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Forward_From_End");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_End");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_Middle");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Skip_Backward_From_Starting");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Rewind_Forward");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Forward_Rewind");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_FF_FR_Pause_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_FF_FR");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Play_SF_SB");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_FF_FR_SF_SB");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Pause_Pause");
	ptrAgentObj->UnregisterMethod("TestMgr_Dvr_Play_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_LiveTune_GETURL");

	/* E2E RF Video */
	ptrAgentObj->UnregisterMethod("TestMgr_RF_Video_ChannelChange");

	return TEST_SUCCESS;
}

/**************************************************************************
  Function Name : DestroyObject

Arguments     : Input argument is E2ERMFAgent Object

Description   : This function will be used to destory the E2ERMFAgent object.
 **************************************************************************/
extern "C" void DestroyObject(E2ERMFAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying E2ERMF Agent object\n");
	delete stubobj;
}

