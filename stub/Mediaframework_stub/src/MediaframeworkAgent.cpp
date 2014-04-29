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

#include "MediaframeworkAgent.h"


/*helper functions for DVR sink*/

static long long getCurrentTime()
{
	struct timeval tv;
	long long currentTime;

	gettimeofday( &tv, 0 );

	currentTime= (((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000);

	return currentTime;
}

IRMFMediaSource* createHNSrc(const std::string& url)
{
	RMFResult result= RMF_RESULT_SUCCESS;
	RMFMediaSourceBase *pSrc= 0;

	pSrc= new HNSource();
	if ( pSrc == 0 )
	{
		DEBUG_PRINT(DEBUG_ERROR, "createHNSrc: Error: unable to create HNSrc\n");
	}
	else
	{
		result= pSrc->init();
		if ( result != RMF_RESULT_SUCCESS )
		{
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc init failed with rc=0x%X", (unsigned int)result);
		}
		else
		{
			result= pSrc->open( url.c_str(), 0 );
			if ( result != RMF_RESULT_SUCCESS )
			{
				DEBUG_PRINT(DEBUG_ERROR, "HNSrc open(%s) failed with rc=0x%X", url.c_str(), (unsigned int) result );
			}
		}
	}

        if ( result != RMF_RESULT_SUCCESS )
        {
                if ( pSrc )
                {
                        delete pSrc;
                        pSrc= 0;
                }
        }

	return pSrc;
}

/*Helper function for QAMSource*/
static bool gThreadFlag = false;
static void getGthreadInstance()
{
	if(false == gThreadFlag)
	{
		g_thread_init(NULL);
		gThreadFlag = true;
		DEBUG_PRINT(DEBUG_TRACE, "g_thread_init called and gThreadFlag is set to true\n");
	}

	DEBUG_PRINT(DEBUG_TRACE, "g_thread_init is up already\n");
}

/*************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent

Arguments     : NULL

Description   : Constructor for MediaframeworkAgent class
 ***************************************************************************/

MediaframeworkAgent::MediaframeworkAgent()
{
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent Initialized\n");
}

typedef std::list<std::pair<float, float> > range_list_t;

/**************************************************************************
  Function name : MediaframeworkAgent::initialize

Arguments     : Input arguments are Version string and MediaframeworkAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
 ***************************************************************************/

bool MediaframeworkAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Mediaframework Initialize----->Entry\n");

	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute, "TestMgr_MPSink_SetGetMute");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume, "TestMgr_MPSink_SetGetVolume");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges, "TestMgr_HNSrc_GetBufferedRanges");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State, "TestMgr_HNSrcMPSink_Video_State");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute, "TestMgr_HNSrcMPSink_Video_MuteUnmute");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume, "TestMgr_HNSrcMPSink_Video_Volume");

	/*DVR Recording List*/
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List, "TestMgr_DVR_Rec_List");

	/*QAM Source */

	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_InitTerm, "TestMgr_QAMSource_InitTerm");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_OpenClose, "TestMgr_QAMSource_OpenClose");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_Play, "TestMgr_QAMSource_Play");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_Pause, "TestMgr_QAMSource_Pause");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetTsId, "TestMgr_QAMSource_GetTsId");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetLtsId, "TestMgr_QAMSource_GetLtsId");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_Init_Uninit_Platform, "TestMgr_QAMSource_Init_Uninit_Platform");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetUseFactoryMethods, "TestMgr_QAMSource_GetUseFactoryMethods");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement, "TestMgr_QAMSource_Get_Free_LowLevelElement");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetQAMSourceInstance, "TestMgr_QAMSource_GetQAMSourceInstance");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_QAMSource_ChangeURI, "TestMgr_QAMSource_ChangeURI");
	
	/*DVR sink*/
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm, "TestMgr_DVRSink_init_term");

	/*DVR Manager*/

        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace, "TestMgr_DVRManager_GetSpace");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount, "TestMgr_DVRManager_GetRecordingCount");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex, "TestMgr_DVRManager_GetRecordingInfoByIndex");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById, "TestMgr_DVRManager_GetRecordingInfoById");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress, "TestMgr_DVRManager_GetIsRecordingInProgress");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize, "TestMgr_DVRManager_GetRecordingSize");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration, "TestMgr_DVRManager_GetRecordingDuration");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime, "TestMgr_DVRManager_GetRecordingStartTime");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration, "TestMgr_DVRManager_GetDefaultTSBMaxDuration");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB, "TestMgr_DVRManager_CreateTSB");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording, "TestMgr_DVRManager_ConvertTSBToRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording, "TestMgr_DVRManager_CreateRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording, "TestMgr_DVRManager_UpdateRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording, "TestMgr_DVRManager_DeleteRecording");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount, "TestMgr_DVRManager_GetSegmentsCount");
        ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex, "TestMgr_DVRManager_GetRecordingSegmentInfoByIndex");

#if 1
/*Optimised Code*/	
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementCreateInstance,"TestMgr_RmfElementCreateInstance");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementRemoveInstance,"TestMgr_RmfElementRemoveInstance");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementInit,"TestMgr_RmfElementInit");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementTerm,"TestMgr_RmfElementTerm");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementOpen,"TestMgr_RmfElementOpen");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementClose,"TestMgr_RmfElementClose");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementPlay,"TestMgr_RmfElementPlay");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementPause,"TestMgr_RmfElementPause");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementSetSpeed,"TestMgr_RmfElementSetSpeed");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetSpeed,"TestMgr_RmfElementGetSpeed");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementSetMediaTime,"TestMgr_RmfElementSetMediaTime");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaTime,"TestMgr_RmfElementGetMediaTime");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaInfo,"TestMgr_RmfElementGetMediaInfo");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElementGetState,"TestMgr_RmfElementGetState");


	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_SinkSetSource,"TestMgr_RmfElement_Sink_SetSource");
	ptrAgentObj->RegisterMethod(*this,&MediaframeworkAgent::MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle,"TestMgr_RmfElement_MpSink_SetVideoRectangle");
#endif	
	
	return TEST_SUCCESS;
}


#if 1

static DVRSource* dvrSource=NULL;
static HNSource* hnSource=NULL;
static MediaPlayerSink* mpSink=NULL;

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementCreateInstance(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementCreateInstance -->Entry\n");

	string rmfInstance = req["rmfElement"].asCString();	
	
        DEBUG_PRINT(DEBUG_TRACE, "RMF Insatnce: %s\n",rmfInstance.c_str());

	if(rmfInstance == "DVRSrc")
	{
		dvrSource = new DVRSource();
		if ( NULL == dvrSource )
	        {
        	        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create DVRSrc\n");
        	        response["result"] = "FAILURE";
               		response["details"] = "Error: unable to create DVRSrc";

	                return TEST_FAILURE;
        	}
        	DEBUG_PRINT(DEBUG_TRACE, "DVRSrc is created \n");
		response["details"] = "DVR instance creation successful";
	}
	if(rmfInstance == "HNSrc")
	{
		hnSource = new HNSource();
                if ( NULL == hnSource )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create HNSrc\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Error: unable to create HNSrc";

                        return TEST_FAILURE;
                }
        	DEBUG_PRINT(DEBUG_TRACE, "HNSrc is created \n");
                response["details"] = "HNSrc instance creation successful";
	}
	if(rmfInstance == "MPSink")
	{
		mpSink = new MediaPlayerSink();
                if ( NULL == mpSink )
                {
                        DEBUG_PRINT(DEBUG_ERROR, "Error: unable to create MediaPlayerSink\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Error: unable to create MediaPlayerSink";

                        return TEST_FAILURE;
                }
        	DEBUG_PRINT(DEBUG_TRACE, "MediaPlayerSink is created \n");
                response["details"] = "MediaPlayerSink instance creation successful";
	}
	if(rmfInstance == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be created\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be created";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementCreateInstance -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementRemoveInstance(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementRemoveInstance -->Entry\n");

	string rmfInstance = req["rmfElement"].asCString();	
	
        DEBUG_PRINT(DEBUG_TRACE, "RMF Insatnce: %s\n",rmfInstance.c_str());
	if(rmfInstance == "DVRSrc")
	{
		delete dvrSource;
        	
		DEBUG_PRINT(DEBUG_TRACE, "DVRSrc is deleted \n");
		response["details"] = "DVR instance deleted successful";
	}
	if(rmfInstance == "HNSrc")
	{
		delete hnSource;
        	
		DEBUG_PRINT(DEBUG_TRACE, "HNSrc is deleted \n");
                response["details"] = "HNSrc instance deleted successful";
	}
	if(rmfInstance == "MPSink")
	{
		delete mpSink;
        	
		DEBUG_PRINT(DEBUG_TRACE, "MediaPlayerSink is deleted \n");
                response["details"] = "MediaPlayerSink instance deleted successful";
	}
	if(rmfInstance == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be deleted\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be deleted";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementRemoveInstance -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementInit(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementInit -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc init() FAILURE";
			
			delete dvrSource;
			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc init successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc init() FAILURE";

			delete hnSource;
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc init() successful";
	}
	if(rmfComponent == "MPSink")
	{
		retResult = mpSink->init();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MediaPlayerSink init() FAILURE";

			delete mpSink;
			DEBUG_PRINT(DEBUG_ERROR, "MediaPlayerSink init() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MediaPlayerSink init() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate init()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate init()";
                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementInit -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementTerm(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementTerm -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc term() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc term() successful";
	}
	if(rmfComponent == "MPSink")
	{
		retResult = mpSink->term();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MediaPlayerSink term() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "MediaPlayerSink term() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MediaPlayerSink term() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate term()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate term()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementTerm -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementOpen(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementOpen -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->open(req["url"].asCString(),0);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE"; 
	                response["details"] = "DVRSrc open() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc open() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc open() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->open(req["url"].asCString(),0);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc open() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc open() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc open() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate open()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate open()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementOpen -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementClose(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementClose -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());

	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->close();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc close() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc close() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc close() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->close();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc close() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc close() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc close() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate close()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate close()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementClose -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementPause(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPause -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();		

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
	{
		retResult = dvrSource->pause();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc pause() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc pause() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc pause() successful";
	}

	if(rmfComponent == "HNSrc")
	{
		retResult = hnSource->pause();	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc pause() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc pause() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc pause() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to initiate pause()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to initiate pause()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPause -->Exit\n");
	return TEST_SUCCESS;
}


bool MediaframeworkAgent::MediaframeworkAgent_RmfElementPlay(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPlay -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfComponent = req["rmfElement"].asCString();	
	
	/* 0 - default, play without passing speed and mediaTime arguments.
           1 - play with passing speed and mediaTime arguments */
        int playArgs = req["defaultPlay"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
	{
		if(0 == playArgs)
		{
			retResult = dvrSource->play();	
		}
		else
		{
			float speed = req["playSpeed"].asFloat();
		        double time = req["playTime"].asDouble();
			retResult = dvrSource->play(speed,time);	
			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc play() with speed and time\n");
			
		}
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "DVRSrc play() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "DVRSrc play() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "DVRSrc play() successful";
	}
	if(rmfComponent == "HNSrc")
	{
		if(0 == playArgs)
                {
                        retResult = hnSource->play();
                }
                else
                {
                        float speed = req["playSpeed"].asFloat();
                        double time = req["playTime"].asDouble();
                        retResult = hnSource->play(speed,time);
			DEBUG_PRINT(DEBUG_ERROR, "HNSrc play() with speed and time\n");
                }
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "HNSrc play() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "HNSrc play() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "HNSrc play() successful";
	}
	if(rmfComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to initiate play()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to initiate play()";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementPlay -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementSetSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetSpeed -->Entry\n");

        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
        float playSpeed = req["playSpeed"].asFloat();

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s \n",rmfComponent.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "SeSpeed: %f \n",playSpeed);
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->setSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc setSpeed() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc setSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "DVRSrc setSpeed() successful";
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->setSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
		 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc setSpeed() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc setSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "HNSrc setSpeed() successful";
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to setSpeed()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to setSpeed()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetSpeed -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetSpeed(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetSpeed -->Entry\n");

        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream details;

        float playSpeed;

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc getSpeed() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc getSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
		details << "DVRSrc getSpeed() successful, Speed:" << playSpeed;
                response["details"] = details.str();
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getSpeed(playSpeed);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc getSpeed() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc getSpeed() FAILURE\n");
                        return TEST_FAILURE;
                }
		details << "HNSrc getSpeed() successful, Speed:" << playSpeed;
                response["details"] = details.str();
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to getSpeed()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to getSpeed()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetSpeed -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_SinkSetSource(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SinkSetSource -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	string rmfSrcComponent = req["rmfSourceElement"].asCString();	
	string rmfSinkComponent = req["rmfSinkElement"].asCString();	

        DEBUG_PRINT(DEBUG_TRACE, "RMF Src Component: %s\n",rmfSrcComponent.c_str());
        DEBUG_PRINT(DEBUG_TRACE, "RMF Sink Component: %s\n",rmfSinkComponent.c_str());
	
	if(rmfSrcComponent == "DVRSrc" && rmfSinkComponent == "MPSink")
	{
		if(dvrSource == NULL || mpSink == NULL)
		{
			response["result"] = "FAILURE";
	                response["details"] = "Create DVRSrc/MPSink  instances first";

			DEBUG_PRINT(DEBUG_ERROR, "Create DVRSrc/MPSink Instance \n");
			return TEST_FAILURE;

		}
		retResult = mpSink->setSource(dvrSource);	
		if(RMF_RESULT_SUCCESS != retResult)
	        {
			response["result"] = "FAILURE";
	                response["details"] = "MPSink setSource() FAILURE";

			DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource() FAILURE\n");
			return TEST_FAILURE;
		}
                response["details"] = "MPSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "MPSink setSource() successful\n");
	}

	if(rmfSrcComponent == "HNSrc" && rmfSinkComponent == "MPSink")
	{
		if(hnSource == NULL || mpSink == NULL)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Create HNSrc/MPSink  instances first";

                        DEBUG_PRINT(DEBUG_ERROR, "Create HNSrc/MPSink Instance \n");
                        return TEST_FAILURE;

                }
                retResult = mpSink->setSource(hnSource);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "MPSink setSource() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "MPSink setSource() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "MPSink setSource() successful";
		DEBUG_PRINT(DEBUG_TRACE, "MPSink setSource() successful\n");
	}

	if(rmfSrcComponent == "" && rmfSinkComponent == "")
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to be used\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to be used";

                return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SinkSetSource -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_MpSinkSetVideoRectangle -->Entry\n");

	RMFResult retResult = RMF_RESULT_SUCCESS;	
	bool applyNow = req["apply"].asInt();
	unsigned x = req["X_Value"].asInt();
	unsigned y = req["Y_Value"].asInt();
	unsigned height = req["height"].asInt();
	unsigned width = req["width"].asInt();

        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value x: %u\n",x);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value y: %u\n",y);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value height: %u\n",height);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value width: %u\n",width);
        DEBUG_PRINT(DEBUG_TRACE, "setVideoRectangle value apply: %d\n",applyNow);
		
	if(mpSink == NULL)	
	{
		DEBUG_PRINT(DEBUG_ERROR, "Error: Create the Mediaframework Instance\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Create the Mediaframework Instance";

                return TEST_FAILURE;
	}
	
	retResult = mpSink->setVideoRectangle(x, y, width, height,applyNow);	
	if(RMF_RESULT_SUCCESS != retResult)
	{
		response["result"] = "FAILURE";
	        response["details"] = "MPSink setVideoRectangle() FAILURE";

		DEBUG_PRINT(DEBUG_ERROR, "MPSink setVideoRectangle() FAILURE\n");
		return TEST_FAILURE;
	}
	response["details"] = "MPSink setVideoRectangle() SUCCESS";
	response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElement_SetVideoRectangle -->Exit\n");
	return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementSetMediaTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetMediaTime -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
        double mediaTime = req["mediaTime"].asDouble();

        DEBUG_PRINT(DEBUG_TRACE, "Media Time: %f\n",mediaTime);

        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->setMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                {
  	                response["result"] = "FAILURE";
                        response["details"] = "DVRSrc SetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc SetMediaTime() FAILURE\n");
                        return TEST_SUCCESS;
                }
                response["details"] = "DVRSrc SetMediaTime() successful";
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->setMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc SetMediaTime() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc SetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
                response["details"] = "HNSrc SetMediaTime() successful";
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to SetMediaTime()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to SetMediaTime()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementSetMediaTime -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaTime -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream detail_string;
        double mediaTime;


        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());

        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"DVRSrc GetMediaTime() successful, MediaTime:"<< mediaTime;
                response["details"] = detail_string.str();
        }
        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getMediaTime(mediaTime);
                if(RMF_RESULT_SUCCESS != retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc GetMediaTime() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"HNSrc GetMediaTime() successful, MediaTime:"<<mediaTime;
                response["details"] = detail_string.str();
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src/Sink element to GetMediaTime()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src/Sink element to GetMediaTime()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaTime -->Exit\n");
        return TEST_SUCCESS;
}

bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetMediaInfo(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaInfo -->Entry\n");
        RMFResult retResult = RMF_RESULT_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	stringstream detail_string;
	RMFMediaInfo mediaInfo;        

        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
        if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getMediaInfo(mediaInfo);
                if(RMF_RESULT_SUCCESS != retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetMediaTime() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetMediaTime() FAILURE\n");
                        return TEST_FAILURE;
                }
		detail_string<<"DVRSrc GetMediaInfo() successful, MediaStartTime:"<< mediaInfo.m_startTime <<" MediaDuration:"<<mediaInfo.m_duration;
                response["details"] = detail_string.str();
        }
        
	if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to GetMediaInfo()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to GetMediaInfo()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetMediaInfo -->Exit\n");
        return TEST_SUCCESS;
}



bool MediaframeworkAgent::MediaframeworkAgent_RmfElementGetState(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetState -->Entry\n");
        RMFStateChangeReturn retResult = RMF_STATE_CHANGE_SUCCESS;
        string rmfComponent = req["rmfElement"].asCString();
	RMFState currentState;
        
        DEBUG_PRINT(DEBUG_TRACE, "RMF Component: %s\n",rmfComponent.c_str());
	if(rmfComponent == "DVRSrc")
        {
                retResult = dvrSource->getState(&currentState,NULL);
                if(RMF_STATE_CHANGE_FAILURE == retResult)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "DVRSrc GetState() FAILURE";
                        DEBUG_PRINT(DEBUG_ERROR, "DVRSrc GetState() FAILURE\n");
                        return TEST_FAILURE;
                }
		switch(currentState)
		{
			case RMF_STATE_VOID_PENDING: 
 	        	    	 response["details"] = "DVRSrc GetState() successful, Current State is: VOID";
	 			 break;
			case RMF_STATE_NULL:
				 response["details"] = "DVRSrc GetState() successful, Current State is: NULL";
				 break;
			case RMF_STATE_READY:
				 response["details"] = "DVRSrc GetState() successful, Current State is: READY";
				 break;
			case RMF_STATE_PAUSED: 
				 response["details"] = "DVRSrc GetState() successful, Current State is: PAUSED";
				 break;
			case RMF_STATE_PLAYING:
				 response["details"] = "DVRSrc GetState() successful, Current State is: PLAYING";
				 break;
			default: 
				 response["details"] = "DVRSrc GetState() successful, Current State is: INVALID";
				 break;
		}
        }

        if(rmfComponent == "HNSrc")
        {
                retResult = hnSource->getState(&currentState,NULL);
                if(RMF_STATE_CHANGE_FAILURE == retResult)
                 {
                        response["result"] = "FAILURE";
                        response["details"] = "HNSrc GetState() FAILURE";

                        DEBUG_PRINT(DEBUG_ERROR, "HNSrc GetState() FAILURE\n");
                        return TEST_FAILURE;
                }
		switch(currentState)
		{
			case RMF_STATE_VOID_PENDING: 
				 response["details"] = "HNSrc GetState() successful, Current State is: VOID";
				 break;
			case RMF_STATE_NULL:
				 response["details"] = "HNSrc GetState() successful, Current State is: NULL";
				 break;
			case RMF_STATE_READY:
				 response["details"] = "HNSrc GetState() successful, Current State is: READY";
				 break;
			case RMF_STATE_PAUSED: 
				 response["details"] = "HNSrc GetState() successful, Current State is: PAUSED";
				 break;
			case RMF_STATE_PLAYING:
				 response["details"] = "HNSrc GetState() successful, Current State is: PLAYING";
				 break;
			default: 
				 response["details"] = "HNSrc GetState() successful, Current State is: INVALID";
				 break;
		}
        }
        if(rmfComponent == "")
        {
                DEBUG_PRINT(DEBUG_ERROR, "Error: Enter the Src element to GetState()\n");
                response["result"] = "FAILURE";
                response["details"] = "Error: Enter the Src element to GetState()";

                return TEST_FAILURE;
        }

        response["result"] = "SUCCESS";
        
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_RmfElementGetState -->Exit\n");
        return TEST_SUCCESS;
}

#endif

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List

Arguments     : Input argument is None. Output argument is "SUCCESS" or "FAILURE". 

Description   : Receives the request from Test Manager to get total number of recording avaliable.
Gets the response from dvr manager and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_DVR_Rec_List(IN const Json::Value& req, OUT Json::Value& response)
{
	DVRManager *dvm= DVRManager::getInstance();
	long long recDuration = 0;
	ofstream recordDetails;
	int count = 0;		
	long long segmentName;
	
	/* Get Total recording List */
	count = dvm->getRecordingCount();
	
	/*Open a file*/
	recordDetails.open(RECORD_DETAILS_TXT, ios::out | ios::trunc);
	if (recordDetails.is_open())
	{
        	DEBUG_PRINT(DEBUG_TRACE, "Number of recordings: %d\n",count);
		recordDetails << "Total Recording: " << count << endl;

		for( int ii= 0; ii < count; ++ii )
		{
		      RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex( ii );

	              DEBUG_PRINT(DEBUG_TRACE, "Record: %d id: %s \n",ii,pRecInfo->recordingId.c_str());
		      recordDetails << "Record: " << ii << " id: " << pRecInfo->recordingId.c_str();
		
		      if (NULL == pRecInfo->title)
		      {
        	      		DEBUG_PRINT(DEBUG_TRACE, "title: (NULL)\n");
				recordDetails << " title: (NULL)";
		      }
		      else
		      {
              			DEBUG_PRINT(DEBUG_TRACE, "title: %s\n", pRecInfo->title);
				recordDetails << " title: " << pRecInfo->title;
	      	      }
	
		      recDuration = dvm->getRecordingDuration(pRecInfo->recordingId.c_str());
	              DEBUG_PRINT(DEBUG_TRACE, " Duration: %lld\n", recDuration);
		      recordDetails << " Duration: " << recDuration;

                      for (int i = 0;i < pRecInfo->segmentCount && i != 1; i++)
		      {
	                        RecordingSegmentInfo *pSegInfo= pRecInfo->segments[i];
				segmentName = pSegInfo->segmentName;
	                        DEBUG_PRINT(DEBUG_TRACE, "SegmentName: %lld\n", segmentName);
				recordDetails << " SegmentName: " << segmentName << endl;
		      }

	              DEBUG_PRINT(DEBUG_TRACE, " Seg Count: %d\n", pRecInfo->segmentCount);
		      if (0 == pRecInfo->segmentCount)
		      {
				recordDetails << " SegmentName: 0" << endl;
		      }
		}
		recordDetails.close();
        	DEBUG_PRINT(DEBUG_TRACE, "Writing into a file succeess\n");
	}
	else
	{
		response["log-path"]= "NULL";	
		response["result"] = "FAILURE";
		response["details"] = "File Creation Failed";
		DEBUG_PRINT(DEBUG_TRACE, "File Creation Failed");
		return TEST_FAILURE;
	}

  	char cwd[1024];
	string syscwd;
	if(getcwd(cwd, sizeof(cwd))==NULL)
	{
	       response["result"]="FAILURE";
  	}
	else if(strcmp(cwd,"/")==0)
	{
	       syscwd = std::string(cwd);
	}
	else
	{
	       syscwd = std::string(cwd)+"/";
	}

	response["log-path"]= syscwd + RECORD_DETAILS_TXT;	
	response["result"] = "SUCCESS";
	response["details"] = "Recording List File Created Successfully";
	DEBUG_PRINT(DEBUG_TRACE, "Success");

        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVR_Rec_List -->Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute.

Arguments     : Input argument is none. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Set and Get Mute state. 
Gets the response from MPSink element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetMute(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetMute --->Entry\n");
#ifdef ENABLE_DVRSRC_MPSINK

	int res_MPSinkterm, res_MPSinkinit;
	bool res_GetMute, res_afterSetMute;

	MediaPlayerSink* pSink = new MediaPlayerSink();

	res_MPSinkinit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Initialize is %d\n",res_MPSinkinit);

	if(0 == res_MPSinkinit)
	{
		res_GetMute = pSink->getMuted();
		if(0 == res_GetMute)
		{
			res_GetMute = 1;
		}
		else
		{
			res_GetMute = 0;
		}
		pSink->setMuted(res_GetMute);
		res_afterSetMute = pSink->getMuted();
		res_MPSinkterm = pSink->term();
		DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n",res_MPSinkterm);

		if(res_afterSetMute == res_GetMute)
		{
			if(0 == res_MPSinkterm)
			{
				DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink_SetGetMute is Success\n" );	
				response["result"] = "SUCCESS";
				return TEST_SUCCESS;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "SetgetMute is success but failed to terminate MPSink";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
				return TEST_FAILURE;
			}
		}
		else
		{
			response["details"] = "SetgetMute is failed";
			response["result"] = "FAILURE";
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
			return TEST_FAILURE;
		}	
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Initialization of MPSink is failed";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetMute --->Exit\n");
		return TEST_FAILURE;
	}
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif
}
/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume

Arguments     : Input argument is Volume.  Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Set and Get Volume.
Gets the response from MPSink element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_MPSink_SetGetVolume(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetVolume --->Entry\n");
#ifdef ENABLE_DVRSRC_MPSINK

	int res_MPSinkterm, res_MPSinkinit;
	float res_GetVolume;
	float volume = req["Volume"].asFloat();

	MediaPlayerSink* pSink = new MediaPlayerSink();

	res_MPSinkinit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Initialize is %d\n", res_MPSinkinit);

	if(0 == res_MPSinkinit)
	{
		res_GetVolume = pSink->getVolume();
		if(volume == res_GetVolume)
		{
			res_MPSinkterm = pSink->term();
			DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n", res_MPSinkterm);
			if(0 == res_MPSinkterm)
			{
				response["result"] = "FAILURE";
				response["details"] = "Get value and entered values are same, Please enter a different value";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "Get value and entered values are same and failed to do terminate MPSink";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}
		}
		else
		{
			pSink->setVolume(volume);
			res_GetVolume = pSink->getVolume();
			DEBUG_PRINT(DEBUG_LOG, "Result of GetVolume after setting is %f\n", res_GetVolume);

			res_MPSinkterm = pSink->term();
			DEBUG_PRINT(DEBUG_LOG, "Result of MPSink Termination is %d\n", res_MPSinkterm);

			if(res_GetVolume == volume)
			{
				if(0 == res_MPSinkterm)
				{
					response["result"] = "SUCCESS";
					DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
					return TEST_SUCCESS;
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "SetgetVoulme is Success but failed to terminate MPSink";
					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
					return TEST_FAILURE;
				}
			}
			else
			{
				response["details"] = "SetgetVoulme is Failed";
				response["result"] = "FAILURE";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
				return TEST_FAILURE;
			}	
		}
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_MPSink_SetGetVolume --->Exit\n");
		return TEST_FAILURE;
	}
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Get Buffer range supported by HNSource.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrc_GetBufferedRanges(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrc_Getbufferrange --->Entry\n");

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcGetbuffrange;

	HNSource* pSource = new HNSource();
	range_list_t ranges;

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n",res_HNSrcInit);

	if(0 == res_HNSrcInit)
	{
		res_HNSrcGetbuffrange = pSource->getBufferedRanges(ranges);
		DEBUG_PRINT(DEBUG_LOG, "Result of Get buffered ranges is %d\n", res_HNSrcGetbuffrange);

		res_HNSrcTerm = pSource->term();
		DEBUG_PRINT(DEBUG_LOG, "Result of Hnsource termination is %d\n", res_HNSrcTerm);

		if(0 == res_HNSrcGetbuffrange)
		{
			if(0 == res_HNSrcTerm)
			{
				response["result"] = "SUCCESS";
				DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrc_Getbufferrange --->Exit\n");
				return TEST_SUCCESS;
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "Getting buffer range is success, but failed to terminate Hnsource";
				DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrc_Getbufferrange --->Exit\n");
				return TEST_FAILURE;
			}	
		}
		else
		{
			response["details"] = "Getting buffer range is failure";
			response["result"] = "FAILURE";               
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrc_Getbufferrange --->Exit\n");
			return TEST_FAILURE;
		}	
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize Hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrc_Getbufferrange --->Exit\n");
		return TEST_FAILURE;
	}
}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the state of video.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_State(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_State --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay;
	int res_HNSrcGetState, res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;

	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;

	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcOpen = pSource->open(req["playuri"].asCString(), 0);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
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
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}	

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{	
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(20);

	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of GstState is %d\n", res_HNSrcGetState);

	if(1 != res_HNSrcGetState)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Get Video State";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		DEBUG_PRINT(DEBUG_ERROR, "Get State API is returning Success, but current state is not RMF_STATE_PLAYING");
		response["result"] = "FAILURE";
		response["details"] = "Get State API is returning Success, but current state is not RMF_STATE_PLAYING";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Get Video state is success. Video is playing and showing state as RMF_STATE_PLAYING\n");

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Get Video state is success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_State--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to verify Mute and Unmute functionality.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay, res_HNSrcGetState; 
	int res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;
	bool res_MPSinkGetMute, res_afterSetMute;

	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;

	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}	

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcOpen = pSource->open(req["playuri"].asCString(), 0);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
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
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(10);
	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Play API call is Success, but Video is not playing";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}						

	DEBUG_PRINT(DEBUG_LOG, "Video is playing\n");

	res_MPSinkGetMute = pSink->getMuted();
	if(0 == res_MPSinkGetMute)
	{
		res_MPSinkGetMute = 1;
	}
	else
	{
		res_MPSinkGetMute = 0;
	}

	pSink->setMuted(res_MPSinkGetMute);
	res_afterSetMute = pSink->getMuted();

	if(res_afterSetMute != res_MPSinkGetMute)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to do Mute and Unmute";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Mute Unmute is success\n");

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Mute Unmute is success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_MuteUnmute--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif
}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume

Arguments     : Input argument is URL. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to Get the volume of Video.
Gets the response from HNSource element and send it to the Test Manager.
 **************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_HNSrcMPSink_Video_Volume(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_Volume --->Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	int res_HNSrcTerm, res_HNSrcInit, res_HNSrcOpen, res_HNSrcClose, res_HNSrcPlay, res_HNSrcGetState; 
	int res_MPSinksetrect, res_MPSinksetsrc, res_MPSinkInit, res_MPSinkTerm;
	float volume, res_GetVolume;
	unsigned x, y, height, width;
	bool applyNow;
	int applynow;

	MediaPlayerSink* pSink = new MediaPlayerSink();
	HNSource* pSource = new HNSource();
	RMFState cur_state;

	volume = req["Volume"].asFloat();
	x = req["X"].asInt();
	y = req["Y"].asInt();
	height = req["H"].asInt();
	width = req["W"].asInt();
	applynow = req["apply"].asInt();

	if(0 == applynow)
	{
		applyNow = false;
	}
	else if(1 == applynow)
	{
		applyNow = true;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "Invald boolean Value\n");
	}

	res_HNSrcInit = pSource->init();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Initialize is %d\n", res_HNSrcInit);

	if(0 != res_HNSrcInit)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcOpen = pSource->open(req["playuri"].asCString(), 0);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of HNSrc open is %d\n", res_HNSrcOpen);

	if(0 != res_HNSrcOpen)
	{
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to open hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinkInit = pSink->init();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Initialize is %d\n", res_MPSinkInit);

	if(0 != res_MPSinkInit)
	{
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to Initialize MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_MPSinksetrect = pSink->setVideoRectangle(x, y, height, width, applyNow);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of setting Video resolution is %d\n", res_MPSinksetrect);

	if(0 != res_MPSinksetrect)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to set video resolution";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
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
		response["details"] = "Failed to set source";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	res_HNSrcPlay = pSource->play();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of Play is %d\n", res_HNSrcPlay);

	if(0 != res_HNSrcPlay)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Failed to play hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	sleep(10);

	res_HNSrcGetState = pSource->getState(&cur_state, NULL);
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of getState is %d\n", res_HNSrcGetState);

	if (cur_state != RMF_STATE_PLAYING)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		DEBUG_PRINT(DEBUG_ERROR, "Play API call is Success, but Video is not playing");
		response["result"] = "FAILURE";
		response["details"] = "Play API call is Success, but Video is not playing";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}							

	DEBUG_PRINT(DEBUG_LOG, "Video is playing\n");

	res_GetVolume = pSink->getVolume();
	if(res_GetVolume == volume)
	{
		pSink->term();
		pSource->close();
		pSource->term();
		response["result"] = "FAILURE";
		response["details"] = "Volime entered is same as the existing Volume, Please enter a different value";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;

	}

	pSink->setVolume(volume);
	res_GetVolume = pSink->getVolume();
	DEBUG_PRINT(DEBUG_LOG, "Result of GetVolume after setting is %f\n", res_GetVolume);

	if(res_GetVolume != volume)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to do set get volume";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_LOG, "Set Get Volume is Success\n");

	res_MPSinkTerm = pSink->term();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of MPSink Termination is %d\n", res_MPSinkTerm);

	res_HNSrcClose = pSource->close();
	DEBUG_PRINT(DEBUG_LOG, "RMF Result of hnsrc close is %d\n", res_HNSrcClose);

	res_HNSrcTerm = pSource->term();
	DEBUG_PRINT(DEBUG_LOG, "Result of HNSrc Termination is %d\n", res_HNSrcTerm);

	if(0 != res_MPSinkTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to Terminate MPSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}	

	if(0 != res_HNSrcClose)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to close hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;						
	}

	if(0 != res_HNSrcTerm)
	{
		response["result"] = "FAILURE";
		response["details"] = "Set Get Volume is Success, but failed to Terminate hnsource";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
		return TEST_FAILURE;
	}

	response["result"] = "SUCCESS";
	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_HNSrcMPSink_Video_Volume--->Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_InitTerm

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Initialize and Termination of the QAMSource Element.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_InitTerm(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_InitTerm ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
		
	getGthreadInstance();	
	
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);
	
	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	RMFQAMSrc::disableCaching();
	
	qamsrc = new RMFQAMSrc();
        if(!qamsrc)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc instance create failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc instance create failed \n");

                retResultQAMSource =  RMFQAMSrc::uninit_platform();
                DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
                platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }

        retResultQAMSource = qamsrc->init();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init failed and result is %ld\n",retResultQAMSource);

                delete qamsrc;
                retResultQAMSource = RMFQAMSrc::uninit_platform();
                DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
                platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	retResultQAMSource = qamsrc->term();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init success but term failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init success but term failed and result is %ld\n",retResultQAMSource);
		
		delete qamsrc;
	        retResultQAMSource = RMFQAMSrc::uninit_platform();
                DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
	        platformRes = mPlatform->uninit();
	        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	delete qamsrc;
        retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
        platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
	response["result"] = "SUCCESS";
        response["details"] = "QAMSrc init and term success";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_InitTerm ---> Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_OpenClose

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Open and Close the QAMSource Component
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_OpenClose(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_OpenClose ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
	const char *ocaplocator = req["ocaplocator"].asCString();
		
	getGthreadInstance();	
		
	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);
	
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);
	
	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	RMFQAMSrc::disableCaching();
	
	qamsrc = new RMFQAMSrc();

        if(!qamsrc)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc instance create failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc instance create failed \n");

                retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }

        retResultQAMSource = qamsrc->init();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init failed and result is %ld\n",retResultQAMSource);

                delete qamsrc;
                retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
                platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	retResultQAMSource = qamsrc->open(ocaplocator,  NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc open is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc intialized but open failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc initialized but open failed and result is %ld\n",retResultQAMSource);

        	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);
		delete qamsrc;
	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	float speed = 1.0;
        double time = 0.0;
	
	retResultQAMSource = qamsrc->play(speed,time);	
	DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc play is %ld\n",retResultQAMSource);

        retResultQAMSource = qamsrc->close();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
		
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc open success but close failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc open success but close failed and result is %ld\n",retResultQAMSource);
			
        	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
		
		return TEST_FAILURE;
	}	

	retResultQAMSource = qamsrc->term();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init success but term failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init success but term failed and result is %ld\n",retResultQAMSource);
	
		delete qamsrc;
	        retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
	        platformRes = mPlatform->uninit();
	        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	delete qamsrc;
        retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
        platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
	response["result"] = "SUCCESS";
        response["details"] = "QAMSrc open and close success";	
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_OpenClose ---> Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Play

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Play the Live content
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_Play(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Play ---> Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;

	RMFMediaSinkBase* playSink;
	MediaPlayerSink* pSink= 0;
	const char *ocaplocator = req["ocaplocator"].asCString();
	float speed = 1.0;
        double time = 0.0;	
		
	getGthreadInstance();	

	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);

	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
		
	retResultQAMSource = RMFQAMSrc::init_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init_platform failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

		platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	

        RMFQAMSrc::disableCaching();
	qamsrc = new RMFQAMSrc();

        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc instance create failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc instance create failed \n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
                DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		return TEST_FAILURE;
        }	
	
	retResultQAMSource = qamsrc->init();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init failed and result is %ld\n",retResultQAMSource);
		
		delete qamsrc;	
		RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();	
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}

	retResultQAMSource = qamsrc->open(ocaplocator,  NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc open is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc open failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc initialized but open failed and result is %ld\n",retResultQAMSource);

        	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);
		delete qamsrc;	
	 	retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	pSink = new MediaPlayerSink();			

        if(!pSink)
        {
		response["result"] = "FAILURE";
		response["details"] = "MPSink instance create failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance create failed \n");

		return TEST_FAILURE;
        }	
	
	retResultQAMSource = pSink->init();
	DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink init failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink init failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}

	pSink->setVideoRectangle(X_VALUE, Y_VALUE, WIDTH, HEIGHT);
	playSink = pSink;
	playSink->setSource(qamsrc);
	
	retResultQAMSource = qamsrc->play(speed,time);	
	DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc play is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc play failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc play failed and result is %ld\n",retResultQAMSource);
  		
		retResultQAMSource = qamsrc->close();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
         	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);
		
		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	
	
	sleep(30);

	playSink->setSource ( NULL );

        retResultQAMSource = qamsrc->close();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
		
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc close failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc close failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}	

        retResultQAMSource = qamsrc->term();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc term failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc term failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}

	delete qamsrc;	
	retResultQAMSource = RMFQAMSrc::uninit_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
	pSink->term ();
	delete pSink;

	platformRes = mPlatform->uninit();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform uninit failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "QAMSrc Play Successful";

	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Play ---> Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Pause

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Pause the Live content
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_Pause(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Pause ---> Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;

	RMFMediaSinkBase* playSink;
	MediaPlayerSink* pSink= 0;
	const char *ocaplocator = req["ocaplocator"].asCString();
	float speed = 1.0;
        double time = 0.0;	
		
	getGthreadInstance();	

	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);

	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
		
	retResultQAMSource = RMFQAMSrc::init_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init_platform failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	

        RMFQAMSrc::disableCaching();
	qamsrc = new RMFQAMSrc();

        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc instance create failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc instance create failed \n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		return TEST_FAILURE;
        }	
	
	retResultQAMSource = qamsrc->init();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init failed and result is %ld\n",retResultQAMSource);
		
		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();	
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}

	retResultQAMSource = qamsrc->open(ocaplocator,  NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc open is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc open failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc initialized but open failed and result is %ld\n",retResultQAMSource);

        	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);
		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	pSink = new MediaPlayerSink();			

        if(!pSink)
        {
		response["result"] = "FAILURE";
		response["details"] = "MPSink instance create failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance create failed \n");

		return TEST_FAILURE;
        }	
	
	retResultQAMSource = pSink->init();
	DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink init failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink init failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}

	pSink->setVideoRectangle(X_VALUE, Y_VALUE, WIDTH, HEIGHT);
	playSink = pSink;
	playSink->setSource(qamsrc);
	
	retResultQAMSource = qamsrc->play(speed,time);	
	DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc play is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc play failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc play failed and result is %ld\n",retResultQAMSource);
  		
		retResultQAMSource = qamsrc->close();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
         	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);
		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	
	
	sleep(30);
	
	retResultQAMSource = qamsrc->pause();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc pause failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc pause failed and result is %ld\n",retResultQAMSource);
  		
		retResultQAMSource = qamsrc->close();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
         	retResultQAMSource = qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

		delete qamsrc;	
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	playSink->setSource ( NULL );
        retResultQAMSource = qamsrc->close();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
		
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc close failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc close failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}	

        retResultQAMSource = qamsrc->term();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc term failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc term failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}
	delete qamsrc;	
	retResultQAMSource = RMFQAMSrc::uninit_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
	pSink->term ();
	delete pSink;

	platformRes = mPlatform->uninit();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform uninit failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "QAMSrc Pause Successful";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_Pause ---> Exit\n");

	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetTsId

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get transferstream id from PAT the QAMSource Component
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetTsId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_GetTsId ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
	const char *ocaplocator = req["ocaplocator"].asCString();
		
	getGthreadInstance();	
		
	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);
	
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);
	
	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	RMFQAMSrc::disableCaching();
        
	qamsrc = RMFQAMSrc::getQAMSourceInstance(ocaplocator );
        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "getQAMSrc instance failed";
		DEBUG_PRINT(DEBUG_ERROR, "getQAMSrc instance failed \n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
        }

	unsigned int tsID;
        retResultQAMSource = qamsrc->getTSID(tsID);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc getTSID is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc getTSID failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getTSID failed and result is %ld\n",retResultQAMSource);
        	
		RMFQAMSrc::freeQAMSourceInstance(qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInsatnce call Done\n");
		
		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
		
		return TEST_FAILURE;
        }

	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getTSID value is %u\n",tsID);
	
	RMFQAMSrc::freeQAMSourceInstance(qamsrc);
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInsatnce call Done\n");

        retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
	response["result"] = "SUCCESS";
        response["details"] = "QAMSrc GetTSID success";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_GetTsId ---> Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetLtsId

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get LTSID corresponding to the QAMSource Instance
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetLtsId(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_GetLtsId ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
	const char *ocaplocator = req["ocaplocator"].asCString();
		
	getGthreadInstance();	
		
	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);
	
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);
	
	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	RMFQAMSrc::disableCaching();
	
	qamsrc = RMFQAMSrc::getQAMSourceInstance(ocaplocator);
        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "getQAMSrc instance failed";
		DEBUG_PRINT(DEBUG_ERROR, "getQAMSrc instance failed \n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
        }

	unsigned int ltsID;
        retResultQAMSource = qamsrc->getLTSID(ltsID);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc getLTSID is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc getLTSID failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getLTSID failed and result is %ld\n",retResultQAMSource);
	
		RMFQAMSrc::freeQAMSourceInstance(qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInsatnce call Done\n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
        	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
		
		return TEST_FAILURE;
        }

	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getLTSID value is %u\n",ltsID);
	
	RMFQAMSrc::freeQAMSourceInstance(qamsrc);
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInsatnce call Done\n");

        retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
	response["result"] = "SUCCESS";
        response["details"] = "QAMSrc GetLTSID success";
	
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_GetLtsId ---> Exit\n");
	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Init_Uninit_Platform

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Initialize and Uninitialize platform dependent functionalities.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_Init_Uninit_Platform(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Init_Uninit_Platform ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
		
	getGthreadInstance();	
	
	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);
	
	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
        retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);
        
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc uninit_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc uninit_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }
	
	platformRes = mPlatform->uninit();
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
	response["result"] = "SUCCESS";
        response["details"] = "QAMSrc init and unint platform success";
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_QAMSource_Init_Uninit_Platform ---> Exit\n");

	return TEST_SUCCESS;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetUseFactoryMethods

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Check if factory methods are to be used by the client. By Calling Init_Platform to read rmfconfig.ini and set the useFactory class varible.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetUseFactoryMethods(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_GetUseFactoryMethods ---> Entry\n");
	bool useFactory;
        RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
        int platformRes = RMF_SUCCESS;
        rmfPlatform *mPlatform = NULL;

        getGthreadInstance();

        mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

        if(RMF_SUCCESS != platformRes)
        {
                response["result"] = "FAILURE";
                response["details"] = "Platform init failed";
                DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);

                return TEST_FAILURE;
        }

        retResultQAMSource = RMFQAMSrc::init_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc init_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }	
	
	/* Assumption: In rmfconfig.ini, "QAMSRC.FACTORY.ENABLED" is set to TRUE.
		So, useFactory value should be TRUE.
	*/
	useFactory = RMFQAMSrc::useFactoryMethods();
	
	if(false == useFactory)
	{
		retResultQAMSource = RMFQAMSrc::uninit_platform();
	        DEBUG_PRINT(DEBUG_TRACE, "Result of uninit_platform is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
	        DEBUG_PRINT(DEBUG_TRACE, "Result of rmf platform uninit is %d\n",platformRes);

                response["result"] = "FAILURE";
                response["details"] = "QAMSrc useFactoryMethods failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc useFactoryMethods failed\n");
	
                return TEST_FAILURE;
	}	

	retResultQAMSource = RMFQAMSrc::uninit_platform();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

        if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                response["result"] = "FAILURE";
                response["details"] = "QAMSrc uninit_platform failed";
                DEBUG_PRINT(DEBUG_ERROR, "QAMSrc uninit_platform failed and result is %ld\n",retResultQAMSource);

                platformRes = mPlatform->uninit();
	        DEBUG_PRINT(DEBUG_ERROR, "Result of platform uninit is %d\n",platformRes);

                return TEST_FAILURE;
        }

        platformRes = mPlatform->uninit();
        DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

        response["result"] = "SUCCESS";
        response["details"] = "QAMSrc GetUseFactoryMethods success";

	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_GetUseFactoryMethods ---> Exit\n");
        return TEST_SUCCESS;
}
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement

Arguments     : Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to get unused low level element of qamsrc.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;
	void* lowSrcElement = NULL;	

	const char *ocaplocator = req["ocaplocator"].asCString();
		
	getGthreadInstance();	

	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);

	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init_platform failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	

        RMFQAMSrc::disableCaching();
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getQAMSourceInstance called \n");
        qamsrc = RMFQAMSrc::getQAMSourceInstance(ocaplocator);
        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "getQAMSourceInstance instance failed returns NULL";
		DEBUG_PRINT(DEBUG_ERROR, "getQAMSourceInstance instance failed returns NULL\n");
			
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
        }

	lowSrcElement = RMFQAMSrc::getLowLevelElement();
	
	if (NULL == lowSrcElement)
	{
        	response["result"] = "FAILURE";
	        response["details"] = "QAMSrc getLowlevelelement failure";	
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc getLowlevelelement failure\n");

        	RMFQAMSrc::freeQAMSourceInstance(qamsrc);
		
		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	RMFQAMSrc::freeLowLevelElement(lowSrcElement);
        DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeLowLevelElement invoked\n");


        RMFQAMSrc::freeQAMSourceInstance(qamsrc);
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInstance successful \n");
	
	retResultQAMSource = RMFQAMSrc::uninit_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
	platformRes = mPlatform->uninit();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform uninit failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "QAMSrc getLowlevelelement and freeLowLevelElement Successful";

	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_Get_Free_LowLevelElement ---> Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetQAMSourceInstance

Arguments     : Input argument is OCAPLOCATOR,i.e SourceId. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to gets a RMFQAMSrc instance from QAMSrc factory corresponding to ocaplocator
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_GetQAMSourceInstance(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_GetQAMSourceInstance ---> Entry\n");
	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;

	const char *ocaplocator = req["ocaplocator"].asCString();
		
	getGthreadInstance();	

	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);

	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init_platform failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

		platformRes = mPlatform->uninit();

		return TEST_FAILURE;
	}	

        RMFQAMSrc::disableCaching();
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getQAMSourceInstance called \n");
        qamsrc = RMFQAMSrc::getQAMSourceInstance(ocaplocator);
        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "getQAMSourceInstance failed returns NULL";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSourceInstance failed returns NULL\n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
        }
        RMFQAMSrc::freeQAMSourceInstance(qamsrc);
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInstance call Done \n");
	retResultQAMSource = RMFQAMSrc::uninit_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
	platformRes = mPlatform->uninit();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform uninit failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "QAMSrc getQAMSourceInstance Successful";

	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_QAMSource_GetQAMSourceInstance ---> Exit\n");
	return TEST_SUCCESS;
}
/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_QAMSource_ChangeURI

Arguments     : Input argument is OCAPLOCATOR and new OCAPLOCATOR to change. Output arguments is "SUCCESS" or "FAILURE"

Description   : Receives the request from Test Manager to Update URI of existing qam instance with new one if possible.If not possible, gets a new instance and returns it.
Gets the response from QAMSrc element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_QAMSource_ChangeURI(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG, "MediaframeworkAgent_QAMSource_ChangeURI ---> Entry\n");

#ifdef ENABLE_DVRSRC_MPSINK

	RMFResult retResultQAMSource = RMF_RESULT_SUCCESS;
	RMFQAMSrc *qamsrc = NULL;	
	int platformRes = RMF_SUCCESS;
	rmfPlatform *mPlatform = NULL;

	RMFMediaSinkBase* playSink;
	MediaPlayerSink* pSink= 0;
	float speed = 1.0;
        double time = 0.0;
	
	const char *ocaplocator = req["ocaplocator"].asCString();
	const char *new_ocaplocator = req["newocaplocator"].asCString();
		
	getGthreadInstance();	

	DEBUG_PRINT(DEBUG_TRACE, "QAMSource ocapLocator is %s\n",ocaplocator);
	DEBUG_PRINT(DEBUG_TRACE, "QAMSource new_ocapLocator is %s\n",new_ocaplocator);

	mPlatform = rmfPlatform::getInstance();
        platformRes = mPlatform->init( 0, NULL);
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform init is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform init failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform init failed and result is %d\n",platformRes);
	
		return TEST_FAILURE;
	}
	
	retResultQAMSource = RMFQAMSrc::init_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc init_platform is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc init_platform failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc init_platform failed and result is %ld\n",retResultQAMSource);

		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
	}	

        RMFQAMSrc::disableCaching();
	DEBUG_PRINT(DEBUG_TRACE, "QAMSrc getQAMSourceInstance called \n");
        qamsrc = RMFQAMSrc::getQAMSourceInstance(ocaplocator);
        if(!qamsrc)
        {
		response["result"] = "FAILURE";
		response["details"] = "getQAMSourceInstance failed returns NULL";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSourceInstance failed returns NULL\n");

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		return TEST_FAILURE;
        }

	pSink = new MediaPlayerSink();			
        if(!pSink)
        {
		response["result"] = "FAILURE";
		response["details"] = "MPSink instance create failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink instance create failed \n");

		return TEST_FAILURE;
        }	
	
	retResultQAMSource = pSink->init();
	DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "MPSink init failed";
		DEBUG_PRINT(DEBUG_ERROR, "MPSink init failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
	}

	pSink->setVideoRectangle(X_VALUE, Y_VALUE, WIDTH, HEIGHT);
	playSink = pSink;
	playSink->setSource(qamsrc);
	
	retResultQAMSource = qamsrc->play(speed,time);	
	DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc open is %ld\n",retResultQAMSource);
	
	if(RMF_RESULT_SUCCESS != retResultQAMSource)
	{
		response["result"] = "FAILURE";
		response["details"] = "QAMSrc open failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc initialized but open failed and result is %ld\n",retResultQAMSource);

        	RMFQAMSrc::freeQAMSourceInstance(qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInstance call Done \n");
		delete qamsrc;	

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
		platformRes = mPlatform->uninit();
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);
	
		retResultQAMSource = playSink->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);
		delete playSink;		

		return TEST_FAILURE;
	}
	
	sleep(30);
	
	retResultQAMSource = qamsrc->pause();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);

        bool newInstance;
        RMFQAMSrc *new_qamsrc = new RMFQAMSrc();

        retResultQAMSource = RMFQAMSrc::changeURI(new_ocaplocator,qamsrc,&new_qamsrc,newInstance);
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc changeURI is %ld\n",retResultQAMSource);

	if(RMF_RESULT_SUCCESS != retResultQAMSource)
        {
                delete new_qamsrc;

		retResultQAMSource = RMFQAMSrc::uninit_platform();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
		platformRes = mPlatform->uninit();	
		DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

		if(RMF_SUCCESS != platformRes)
		{
			response["result"] = "FAILURE";
			response["details"] = "Platform uninit failed";
			DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

			return TEST_FAILURE;
		}

                retResultQAMSource = playSink->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);
                delete playSink;

		response["result"] = "FAILURE";
		response["details"] = "QAMSrc changeURI failed";
		DEBUG_PRINT(DEBUG_ERROR, "QAMSrc changeURI failed and result is %ld\n",retResultQAMSource);

		return TEST_FAILURE;
        }

	if(newInstance == true)
        {
                retResultQAMSource = playSink->setSource(NULL);
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink setSource is %ld\n",retResultQAMSource);

                retResultQAMSource = playSink->setSource(new_qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink setSource is %ld\n",retResultQAMSource);

                retResultQAMSource = new_qamsrc->play(speed,time);
		DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc play is %ld\n",retResultQAMSource);
                
		if(RMF_RESULT_SUCCESS != retResultQAMSource)
                {
			response["result"] = "FAILURE";
			response["details"] = "QAMSrc play failed";
			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc play failed and result is %ld\n",retResultQAMSource);

                	retResultQAMSource = playSink->term();
			DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink init is %ld\n",retResultQAMSource);
	                delete playSink;
				
                	retResultQAMSource = new_qamsrc->pause();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);

        	        retResultQAMSource = new_qamsrc->close();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
	                retResultQAMSource = new_qamsrc->term();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

        	        delete new_qamsrc;
			
			retResultQAMSource = RMFQAMSrc::uninit_platform();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
			platformRes = mPlatform->uninit();	
			DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

			if(RMF_SUCCESS != platformRes)
			{
				response["result"] = "FAILURE";
				response["details"] = "Platform uninit failed";
				DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

				return TEST_FAILURE;
			}
			return TEST_FAILURE;
                }
                sleep(10);

                retResultQAMSource = new_qamsrc->pause();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);

                retResultQAMSource = new_qamsrc->close();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc close is %ld\n",retResultQAMSource);
                retResultQAMSource = new_qamsrc->term();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc term is %ld\n",retResultQAMSource);

                delete new_qamsrc;
	}
	else
	{
                retResultQAMSource = playSink->setSource(NULL);
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink setSource is %ld\n",retResultQAMSource);

                retResultQAMSource = playSink->setSource(qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "Result of MPSink setSource is %ld\n",retResultQAMSource);

                retResultQAMSource = qamsrc->play(speed,time);
		DEBUG_PRINT(DEBUG_LOG, "Result of QAMSrc play is %ld\n",retResultQAMSource);
                
		if(RMF_RESULT_SUCCESS != retResultQAMSource)
                {
			response["result"] = "FAILURE";
			response["details"] = "QAMSrc play failed";
			DEBUG_PRINT(DEBUG_ERROR, "QAMSrc play failed and result is %ld\n",retResultQAMSource);

                	retResultQAMSource = qamsrc->pause();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);
						
        		RMFQAMSrc::freeQAMSourceInstance(qamsrc);
			DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInstance call Done \n");
		
			retResultQAMSource = RMFQAMSrc::uninit_platform();
			DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
			platformRes = mPlatform->uninit();	
			DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

			if(RMF_SUCCESS != platformRes)
			{
				response["result"] = "FAILURE";
				response["details"] = "Platform uninit failed";
				DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

				return TEST_FAILURE;
			}

			return TEST_FAILURE;
                }

                sleep(10);
                retResultQAMSource = qamsrc->pause();
		DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc pause is %ld\n",retResultQAMSource);
	        RMFQAMSrc::freeQAMSourceInstance(qamsrc);
		DEBUG_PRINT(DEBUG_TRACE, "QAMSrc freeQAMSourceInstance call Done \n");
	}

	retResultQAMSource = RMFQAMSrc::uninit_platform();
	DEBUG_PRINT(DEBUG_TRACE, "Result of QAMSrc uninit_platform is %ld\n",retResultQAMSource);
        
	platformRes = mPlatform->uninit();	
	DEBUG_PRINT(DEBUG_TRACE, "Result of platform uninit is %d\n",platformRes);

	if(RMF_SUCCESS != platformRes)
	{
		response["result"] = "FAILURE";
		response["details"] = "Platform uninit failed";
		DEBUG_PRINT(DEBUG_ERROR, "Platform uninit failed and result is %d\n",platformRes);

		return TEST_FAILURE;
	}
	
	response["result"] = "SUCCESS";
	response["details"] = "QAMSrc ChangeURI Successful";

	DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_QAMSource_ChangeURI ---> Exit\n");
	return TEST_SUCCESS;
#else
        response["result"] = "FAILURE";
        response["details"] = "DVR SOURCE & MP SINK are not linked during compilation";
        DEBUG_PRINT(DEBUG_ERROR, "DVR SOURCE & MP SINK are not linked during compilation \n");
        return TEST_FAILURE;
#endif

}

/**************************************************************************
  Function name : MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm

Arguments     : Input argument is RecordingId and playUrl. Output argument is "SUCCESS" or "FAILURE". 

Description   : Receives the request from Test Manager to Initialize, get recording Id and Termination of the DVRSink Element.
Gets the response from DVRSink element and send it to the Test Manager.
 **************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRSink_InitTerm(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->Entry\n");

	RMFResult res_DVRSinkterm = RMF_RESULT_FAILURE;
	RMFResult res_DVRSinkinit = RMF_RESULT_FAILURE;
	RMFResult res_DVR = RMF_RESULT_FAILURE;

	string recordingId = req["recordingId"].asString();
	DEBUG_PRINT(DEBUG_LOG, "RecordingId input: %s\n", recordingId.c_str());
	string playUrl = req["playUrl"].asString();
	DEBUG_PRINT(DEBUG_LOG, "Play URL input: %s\n", playUrl.c_str());

	IRMFMediaSource *src = 0;
	DVRSink *dvrSink = 0;
	char work[TITLE_LEN] = {'\0'};

	if ( playUrl.compare( 0, 7, "http://" ) == 0 )
	{
		src = createHNSrc(playUrl);
		if ( !src )
		{
			response["result"] = "FAILURE";
			response["details"] = "Failed to create HNSrc for recording";
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Failed to create HNSrc. Exit\n");
			return TEST_FAILURE;
		}		
	}
	else
	{
		response["result"] = "FAILURE";
		response["details"] = "Unsupported src locator type";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->Source creation success\n");

	// Create recording
	RecordingSpec spec;
	spec.setRecordingId(recordingId);
	spec.setStartTime( getCurrentTime());
	spec.setDuration(REC_DURATION);
	spec.setDeletePriority(PRIORITY);
	spec.setBitRate( RecordingBitRate_high );
	sprintf( work, "{\"title\":\"DVRSink test recording\"}");
	spec.setProperties( work );
	spec.addLocator( playUrl );
	res_DVR = DVRManager::getInstance()->createRecording( spec );
	if ( res_DVR != DVRResult_ok )
	{
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->createRecording failed\n");
		response["result"] = "FAILURE";
		response["details"] = "Failed to create recording";

		if ( src )
		{
			src->term();
			delete src;
			src = 0;
			DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
		}

		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
		return TEST_FAILURE;
	}

	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->createRecording success\n");

	// Create DVRSink instance
	dvrSink = new DVRSink(recordingId);

	if (0 == dvrSink)
	{
		response["result"] = "FAILURE";
		response["details"] = "Failed to create DVRSink";
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> Exit\n");
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->DVRSink creation success\n");

		res_DVRSinkinit = dvrSink->init();
		DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink Initialization: %d\n", (int)res_DVRSinkinit);

		if(RMF_RESULT_SUCCESS == res_DVRSinkinit)
		{
			char stringDetails[75] = {'\0'};
			dvrSink->setSource(src);

			string rec_id = dvrSink->getRecordingId();
			DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink GetRecordingId: %s\n", rec_id.c_str());

			res_DVRSinkterm = dvrSink->term();
			DEBUG_PRINT(DEBUG_ERROR, "Result of DVRSink Termination: %d\n", (int)res_DVRSinkterm);

			if(RMF_RESULT_SUCCESS == res_DVRSinkterm)
			{
				if(rec_id == recordingId)
				{
					sprintf(stringDetails,"RecordingId:%s", rec_id.c_str());
					response["details"] = stringDetails;
					response["result"] = "SUCCESS";

					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> GetRecordingId success\n");

					if ( src )
					{
						src->term();
						delete src;
						src = 0;
						DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
					}

					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_Init&term --->Exit\n");
					return TEST_SUCCESS;	
				}
				else
				{
					response["result"] = "FAILURE";
					response["details"] = "DVRSink term is success but failed to get recording Id";
					DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm ---> GetRecordingId failed\n");
				}
			}
			else
			{
				response["result"] = "FAILURE";
				response["details"] = "DVRSink Initialization is success but failed to do terminate";
			}
		}
		else
		{
			response["result"] = "FAILURE";
			response["details"] = "Initialization of DVRSink is failed";
		}
	}

	if ( src )
	{
		src->term();
		delete src;
		src = 0;
		DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_InitTerm --->source termination success\n");
	}

	DEBUG_PRINT(DEBUG_ERROR, "MediaframeworkAgent_DVRSink_Init&term --->Exit\n");
	return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get TotalSpace and FreeSpace.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/
bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSpace(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                long long totalSpace= dvm->getTotalSpace();
                long long freeSpace= dvm->getFreeSpace();
                char stringDetails[75] = {'\0'};

                DEBUG_PRINT(DEBUG_LOG, "Total Space: %lld bytes\n", totalSpace);
                DEBUG_PRINT(DEBUG_LOG, "Free Space: %lld bytes\n", freeSpace );

                if((0 == totalSpace) || (totalSpace < freeSpace))
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get total/free space";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Exit\n");
                        return TEST_FAILURE;
                }

                sprintf(stringDetails,"TotalSpace:%lld bytes,FreeSpace:%lld bytes", totalSpace, freeSpace);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;

                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get total/free space";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSpace --->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingCount.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingCount(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[25] = {'\0'};
                int count= dvm->getRecordingCount();

                DEBUG_PRINT(DEBUG_LOG, "Number of recordings = %d\n", count);
                sprintf(stringDetails, "RecordingCount:%d", count);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get recording count";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingCount -->Exit\n");
        return TEST_FAILURE;

}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex

Arguments     : Input argument is 'index'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoByIndex.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex --->Entry\n");

        char stringDetails[75] = {'\0'};
        int index = req["index"].asInt();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                int count = dvm->getRecordingCount();
                DEBUG_PRINT(DEBUG_TRACE, "RecordingCount: %d\n", count);

                for( int i= 0; i < count; ++i )
                {
                        RecordingInfo *pRecInfoTmp = dvm->getRecordingInfoByIndex( i );
                        DEBUG_PRINT( DEBUG_TRACE, "recording %d id %s title \"%s\"\n", i, pRecInfoTmp->recordingId.c_str(), pRecInfoTmp->title );
                }

                if (index >= count)
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfo. Index not found";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                        return TEST_FAILURE;
                }

                RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex( index );
                if ( pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Index:%d, RecordingId:%s, Title:%s\n", index, pRecInfo->recordingId.c_str(), pRecInfo->title);
                        sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfo by Index";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get RecordingInfo by Index";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoByIndex -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get RecordingInfoById.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingInfoById(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById --->Entry\n");

        char stringDetails[75] = {'\0'};
        string recordingId = req["recordingId"].asString();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );
                if ( pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, Title:%s\n", pRecInfo->recordingId.c_str(), pRecInfo->title );
                        if (recordingId == pRecInfo->recordingId)
                        {
                                sprintf(stringDetails, "RecordingId:%s,Title:%s", pRecInfo->recordingId.c_str(), pRecInfo->title );
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                                return TEST_SUCCESS;
                        }
                        else
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Failed to get RecordingInfoById";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                                return TEST_FAILURE;
                        }
                }
                else
                {
                        DEBUG_PRINT(DEBUG_ERROR, "No record found with requested Id\n");
                        response["result"] = "FAILURE";
                        response["details"] = "No record found with requested Id";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
        return TEST_FAILURE;
}



/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the status RecordingInProgress.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetIsRecordingInProgress(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[30] = {'\0'};
                string recordingId = req["recordingId"].asString();
                bool recStatus = dvm->isRecordingInProgress( recordingId );
                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, IsRecordingInProgress: %d\n", recordingId.c_str(), recStatus);

                if (true == recStatus)
                {
                        sprintf(stringDetails, "%s", "Recording IS InProgress");
                }
                else
                {
                        sprintf(stringDetails, "%s", "Recording IS NOT InProgress");
                }

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetIsRecordingInProgress -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingSize.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSize(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();
                long long recSize = dvm->getRecordingSize( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingSize: %lld\n", recordingId.c_str(), recSize);
                sprintf(stringDetails, "RecordingSize: %lld", recSize);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSize -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingDuration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingDuration(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();
                long long recDuration = dvm->getRecordingDuration( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingDuration: %lld\n", recordingId.c_str(), recDuration);
                sprintf(stringDetails, "RecordingDuration: %lld", recDuration);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingDuration -->Exit\n");
        return TEST_FAILURE;
}




/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime

Arguments     : Input argument is 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the RecordingStartTime.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingStartTime(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string recordingId = req["recordingId"].asString();
                long long recStartTime = dvm->getRecordingStartTime( recordingId );

                DEBUG_PRINT(DEBUG_LOG, "RecordingId:%s, RecordingStartTime: %lld\n", recordingId.c_str(), recStartTime);
                sprintf(stringDetails, "RecordingStartTime: %lld", recStartTime);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingStartTime -->Exit\n");
        return TEST_FAILURE;
}



/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration

Arguments     : Input argument is NONE. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the default TSB Max duration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                int defTSBMaxDuration = dvm->getDefaultTSBMaxDuration( );

                DEBUG_PRINT(DEBUG_LOG, "DefaultTSBMaxDuration is %d\n", defTSBMaxDuration);
                sprintf(stringDetails, "DefaultTSBMaxDuration: %d", defTSBMaxDuration);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DefaultTSBMaxDuration";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetDefaultTSBMaxDuration -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB

Arguments     : Input argument is 'duration'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to create TSB with given duration.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateTSB(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[35] = {'\0'};
                string tsbId;
                long long duration = 0;
                duration = req["duration"].asDouble();

                int dvrres= dvm->createTSB( duration, tsbId );

                DEBUG_PRINT(DEBUG_TRACE, "Result of createTSB: %d\n", dvrres);

                if ( dvrres == DVRResult_ok )
                {
                        response["result"] = "SUCCESS";
                        sprintf(stringDetails, "TSBId: %s", tsbId.c_str());
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Get on DVR manager instance success but failed to create TSB";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateTSB -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording

Arguments     : Input arguments are 'tsbId' and 'recordingId'. Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to convert TSB to Recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_ConvertTSBToRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                int dvrres = DVRResult_ok;
                string tsbId = req["tsbId"].asString();
                string recordingId = req["recordingId"].asString();

                dvrres= dvm->convertTSBToRecording( tsbId, recordingId );
                DEBUG_PRINT(DEBUG_TRACE, "Result of convertTSBToRecording: %d\n", dvrres);
                if ( (dvrres != DVRResult_ok) && (dvrres != DVRResult_cciExclusions) )
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to convert TSB to Recording";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_FAILURE;
                }
                else
                {
                        response["result"] = "SUCCESS";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_ConvertTSBToRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording

Arguments     : Input arguments are 'recordingId', 'recordingTitle', 'recordDuration' and 'qamLocator'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to create a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_CreateRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char work[256] = {'\0'};
                int dvrres;
                RecordingSpec spec;
                long long recordDuration = 0;
                string recordingTitle, recordingId, qamLocator;

                recordingTitle = req["recordingTitle"].asString();
                recordingId = req["recordingId"].asString();
                recordDuration= req["recordDuration"].asDouble();
                qamLocator=req["qamLocator"].asString();

                long long now= getCurrentTime();
                recordDuration *= 1000;
                sprintf( work, "{\"title\":\"%s %s\"}", recordingId.c_str(), recordingTitle.c_str());
                DEBUG_PRINT(DEBUG_TRACE, "Recording title to be set : %s\n", work);

                // Create recording
                spec.setRecordingId(recordingId);
                spec.setStartTime( now );
                spec.setDuration(recordDuration);
                spec.setDeletePriority(PRIORITY);
                spec.setBitRate( RecordingBitRate_high );
                spec.setProperties( work );
                spec.addLocator( qamLocator );

                dvrres= dvm->createRecording( spec );
                DEBUG_PRINT(DEBUG_TRACE, "Result of createRecording: %d\n", dvrres);
                if ( dvrres == DVRResult_ok )
                {
                        response["result"] = "SUCCESS";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Get on DVR manager instance success but failed to create record";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_CreateRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording

Arguments     : Input argument is 'recordingId'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to update the title of a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_UpdateRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char work[256] = {'\0'};
                char stringDetails[256] = {'\0'};
                int dvrres;

                string recordingId = req["recordingId"].asString();
                RecordingInfo *pRecInfo= dvm->getRecordingInfoById( recordingId );

                if ( pRecInfo )
                {
                        DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, RecordingTitle:%s", pRecInfo->recordingId.c_str(), pRecInfo->title);

                        // Create recording spec from record info
                        RecordingSpec spec;
                        spec.setRecordingId(pRecInfo->recordingId);
                        spec.setStartTime(pRecInfo->requestedStartTime);
                        spec.setDuration(pRecInfo->requestedDuration);
                        spec.setEntitlementId(pRecInfo->entitlementId);
                        spec.setIsPPV(pRecInfo->isPPV);
                        spec.setBitRate(pRecInfo->bitRate);

                        // Update the recording title
                        sprintf( work, "{\"title\":\"%s Updated test record\"}", recordingId.c_str());
                        DEBUG_PRINT(DEBUG_TRACE, "Updated title to be set : %s\n", work);

                        spec.setProperties( work );

                        dvrres= dvm->updateRecording( spec );
                        DEBUG_PRINT(DEBUG_TRACE, "Result of updateRecording: %d\n", dvrres);
                        if ( dvrres == DVRResult_ok )
                        {
                                DEBUG_PRINT(DEBUG_TRACE, "RecordingId:%s, RecordingTitle:%s", pRecInfo->recordingId.c_str(), pRecInfo->title);
                                sprintf(stringDetails, "UpdatedTitle: %s", pRecInfo->title);
                                response["result"] = "SUCCESS";
                                response["details"] = stringDetails;
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                                return TEST_SUCCESS;
                        }
                        else
                        {
                                response["result"] = "FAILURE";
                                response["details"] = "Get on record info success but failed to update record";
                                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
                                return TEST_FAILURE;
                        }
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingInfoById";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingInfoById -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_UpdateRecording -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording

Arguments     : Input argument is 'recordingId'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to delete a recording.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_DeleteRecording(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                string recordingId = req["recordingId"].asString();
                int result= dvm->deleteRecording ( recordingId );
                DEBUG_PRINT(DEBUG_ERROR, "Result of deleteRecording is %d\n", result);

                if ( DVRResult_ok == result )
                {
                        response["result"] = "SUCCESS";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to delete recording. RecordingId not found";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_DeleteRecording -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount

Arguments     : Input argument is NONE.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the segments count.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetSegmentsCount(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount --->Entry\n");

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[25] = {'\0'};
                int count = dvm->getSegmentsCount();

                DEBUG_PRINT(DEBUG_LOG, "Number of Segments = %d\n", count);
                sprintf(stringDetails, "SegmentCount:%d", count);

                response["result"] = "SUCCESS";
                response["details"] = stringDetails;
                DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount -->Exit\n");
                return TEST_SUCCESS;
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetSegmentsCount -->Exit\n");
        return TEST_FAILURE;
}


/**************************************************************************
Function name : MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex

Arguments     : Input argument is 'index'.
                Output argument is "SUCCESS" or "FAILURE".

Description   : Receives the request from Test Manager to get the segment info by index.
                Gets the response from DVRManager element and send it to the Test Manager.
**************************************************************************/

bool MediaframeworkAgent::MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex(IN const Json::Value& req, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex --->Entry\n");
        int index = req["index"].asInt();

        DVRManager *dvm= DVRManager::getInstance();
        if (dvm)
        {
                char stringDetails[50] = {'\0'};
                RecordingSegmentInfo *pSegInfo= dvm->getRecordingSegmentInfoByIndex( index );
                if ( pSegInfo )
                {
                        long long segmentName = pSegInfo->segmentName;
                        DEBUG_PRINT(DEBUG_TRACE, "Segment Name: %lld\n", segmentName);
                        sprintf(stringDetails, "Index: %d SegmentName:%lld", index, segmentName);
                        response["result"] = "SUCCESS";
                        response["details"] = stringDetails;
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                        return TEST_SUCCESS;
                }
                else
                {
                        DEBUG_PRINT(DEBUG_TRACE, "Failed to get RecordingSegmentInfoByIndex. Index more than number of Segments\n");
                        response["result"] = "FAILURE";
                        response["details"] = "Failed to get RecordingSegmentInfoByIndex";
                        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
                        return TEST_FAILURE;
                }
        }

        response["result"] = "FAILURE";
        response["details"] = "Failed to get DVR Manager instance";
        DEBUG_PRINT(DEBUG_TRACE, "MediaframeworkAgent_DVRManager_GetRecordingSegmentInfoByIndex -->Exit\n");
        return TEST_FAILURE;
}

/**************************************************************************
  Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "MediaframeworkAgent".
 **************************************************************************/

extern "C" MediaframeworkAgent* CreateObject()
{
	return new MediaframeworkAgent();
}

/**************************************************************************
  Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/

bool MediaframeworkAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_ERROR, "cleaningup\n");

	if(NULL == ptrAgentObj)
	{
		return TEST_FAILURE;
	}

	ptrAgentObj->UnregisterMethod("TestMgr_MPSink_SetGetMute");
	ptrAgentObj->UnregisterMethod("TestMgr_MPSink_SetGetVolume");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrc_GetBufferedRanges");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_State");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_MuteUnmute");
	ptrAgentObj->UnregisterMethod("TestMgr_HNSrcMPSink_Video_Volume");

	/*DVR Recording List*/
	ptrAgentObj->UnregisterMethod("TestMgr_DVR_Rec_List");

	/*QAM Source*/
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_InitTerm");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_OpenClose");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_Play");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_Pause");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_GetTsId");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_GetLtsId");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_Init_Uninit_Platform");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_GetUseFactoryMethods");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_Get_Free_LowLevelElement");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_GetQAMSourceInstance");
	ptrAgentObj->UnregisterMethod("TestMgr_QAMSource_ChangeURI");

	/*DVR sink*/
	ptrAgentObj->UnregisterMethod("TestMgr_DVRSink_init_term");

	/*DVR Manager*/
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetSpace");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingCount");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingInfoByIndex");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingInfoById");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetIsRecordingInProgress");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingSize");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingDuration");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingStartTime");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetDefaultTSBMaxDuration");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_CreateTSB");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_ConvertTSBToRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_CreateRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_UpdateRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_DeleteRecording");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetSegmentsCount");
        ptrAgentObj->UnregisterMethod("TestMgr_DVRManager_GetRecordingSegmentInfoByIndex");

/*Optimised Code*/
#if 1
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementCreateInstance");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementRemoveInstance");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementInit");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementTerm");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementOpen");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementClose");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementPlay");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementPause");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementSetSpeed");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetSpeed");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementSetMediaTime");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetMediaTime");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetMediaInfo");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElementGetState");

	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_Sink_SetSource");
	ptrAgentObj->UnregisterMethod("TestMgr_RmfElement_MpSink_SetVideoRectangle");
#endif

	return TEST_SUCCESS;
}

/**************************************************************************
  Function Name : DestroyObject

Arguments     : Input argument is MediaframeworkAgent Object

Description   : This function will be used to destory the MediaframeAgent object.
 **************************************************************************/
extern "C" void DestroyObject(MediaframeworkAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_TRACE, "Destroying Mediainterface Agent object\n");
	delete stubobj;
}

