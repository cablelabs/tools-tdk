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

#include "MediaUtilsAgent.h"

typedef struct appDataStruct{
    RMF_AudioCaptureHandle hAudCap;
    FILE * file;
    unsigned long bytesWritten;
    unsigned samplerate;
    unsigned channels;
    unsigned bitsPerSample;
    unsigned int prevCbTime;
    unsigned int firstCbTime;
} appDataStruct;
appDataStruct appData;

/****Helpers****/
/**Function to open a wave format file in to which the captured audio need to be saved**/
int fileOpen(appDataStruct *appData)
{
    const char *filename = NULL;
    char wav_file[200] = {'\0'};
    std::string g_tdkPath = getenv("TDK_PATH");
    sprintf (wav_file, "%s/tmp/audioCapture.wav",g_tdkPath.c_str());

    appData->file = 0;
    appData->file = fopen(wav_file, "w+");
    if (!appData->file)
    {
        fprintf(stderr, "### unable to open the file /opt/TDK/tmp/audioCapture.wav");
        return 0;
    }
    else
    {
        printf("Capturing Audio to /opt/TDK/tmp/audioCapture.wav\n");
        return 1;
    }
}


/*static int writeDefaultWavHdr(appDataStruct *appData){
    struct wave_header wave_header;

    get_default_wave_header(&wave_header);
    wave_header.riffCSize = 0xfffffff0;
    wave_header.dataLen = 0xffffffcc;
    wave_header.bps = appData->bitsPerSample;
    wave_header.channels = appData->channels;
    wave_header.samplesSec = appData->samplerate;
    wave_header.bytesSec = wave_header.samplesSec * wave_header.channels * wave_header.bps / 8;
    wave_header.chbits = wave_header.channels * wave_header.bps / 8;
    write_wave_header(appData->file, &wave_header);
    printf("%s:%d wave_header.bps=%d ,wave_header.channels=%d wave_header.samplesSec=%ld\n", __FUNCTION__, __LINE__, wave_header.bps, wave_header.channels, wave_header.samplesSec);
    return 0;
}*/


/******************************************************/
rmf_Error cbBufferReady (void *context, void *buf, unsigned int size)
{
    struct timeval tv;
    unsigned long int currTime = 0;

    appDataStruct *data = (appDataStruct*) context;

    gettimeofday(&tv,NULL);
    currTime = (1000 * tv.tv_sec) + tv.tv_usec/1000;

    fwrite(buf, sizeof(char), size, data->file);
    data->bytesWritten += size;

    printf("audioCaptureCb sz=%04d total=%08lu ", size, data->bytesWritten);

    if (data->prevCbTime) {
//        unsigned long int endTime;
//        gettimeofday(&tv,NULL);
//        endTime = (1000 * tv.tv_sec) + tv.tv_usec/1000;
        printf(" %03ums ", (unsigned int)(currTime - data->prevCbTime));
//        printf("execute=%02ums ", (unsigned int)(endTime - currTime));
        if (currTime>data->firstCbTime){
            printf("avg=%03ukhz", (unsigned int)((data->bytesWritten/4)/(currTime - data->firstCbTime)));
        }
    }
    else{
        data->firstCbTime = currTime;
    }

    data->prevCbTime = currTime;
    printf("\n");
    fflush(stdout);
    return RMF_SUCCESS;
}


/*************************************************************************
Function name : MediaUtilsAgent::MediaUtilsAgent

Arguments     : NULL

Description   : Constructor for MediaUtilsAgent class
***************************************************************************/

MediaUtilsAgent::MediaUtilsAgent()
{
        DEBUG_PRINT(DEBUG_LOG, "MediaUtilsAgent Initialized\n");
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                1.
 *****************************************************************************/

std::string MediaUtilsAgent::testmodulepre_requisites()
{
	char cmdstring[200] = {'\0'};
	system("systemctl stop audiocapturemgr.service");
        std::string g_tdkPath = getenv("TDK_PATH"); 
        sprintf (cmdstring, "mkdir %s/tmp",g_tdkPath.c_str());
	system(cmdstring);
        sprintf (cmdstring, "touch %s/tmp/audioCapture.wav",g_tdkPath.c_str());
	system(cmdstring);

	memset(&appData, 0, sizeof(appData));
        appData.bitsPerSample = 16;
        appData.samplerate = 48000;
        appData.channels = 10;
//	return "SUCCESS";
        if(!fileOpen(&appData))
            {
            printf("Could not open the .wav file\n");
            return "FAILURE";
            }
        else
            {
            printf(".wave file opened\n");
	    return "SUCCESS";
	    }

   /*         if(!writeDefaultWavHdr(&appData))
                {
                printf("Wave header written\n");
                return "SUCCESS";
                }
            else
                {
                printf("Wave header not written\n");
                return "FAILURE";
                }
            }*/
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool MediaUtilsAgent::testmodulepost_requisites()
{
	return "SUCCESS";
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "MediaUtilsAgent".
**************************************************************************/

extern "C" MediaUtilsAgent* CreateObject()
{
        return new MediaUtilsAgent();
}

/***************************************************************************
 *Function name : initialize
 *Descrption    : Initialize Function will be used for registering the wrapper method
 *                with the agent so that wrapper functions will be used in the
 *                script
 *****************************************************************************/

bool MediaUtilsAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT (DEBUG_TRACE, "MediaUtils Initialization Entry\n");
    
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_AudioCapture_Open, "TestMgr_MediaUtils_AudioCapture_Open");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_Get_DefaultSettings, "TestMgr_MediaUtils_Get_DefaultSettings");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_Get_Current_Settings, "TestMgr_MediaUtils_Get_Current_Settings");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_Get_Status, "TestMgr_MediaUtils_Get_Status");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_AudioCaptureStart, "TestMgr_MediaUtils_AudioCaptureStart");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_AudioCaptureStop, "TestMgr_MediaUtils_AudioCaptureStop");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_AudioCapture_Close, "TestMgr_MediaUtils_AudioCapture_Close");
    ptrAgentObj->RegisterMethod(*this,&MediaUtilsAgent::MediaUtils_ExecuteCmd,"TestMgr_MediaUtils_ExecuteCmd");
    DEBUG_PRINT (DEBUG_TRACE, "MediaUtils Initialization Exit\n");

    return TEST_SUCCESS;
}


/***************************************************************************
 *Function name : MediaUtils_AudioCapture_Open
 *Descrption    : This function is to get the default settings of audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_AudioCapture_Open(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Open --->Entry\n");

    audiocapture_Open=RMF_AudioCapture_Open(&appData.hAudCap);
    if (!audiocapture_Open)
    {
	response["result"] = "SUCCESS";
	response["details"] = "RMF_AudioCapture_Open success\n";
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_AudioCapture_Open success\n");
	DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Open -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
	response["result"] = "FAILURE";
	response["details"] = "RMF_AudioCapture_Open failed\n";
        DEBUG_PRINT(DEBUG_ERROR, "RMF_AudioCapture_Open failed\n");
	DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Open -->Exit\n");
        return TEST_FAILURE;
    }

}


/***************************************************************************
 *Function name : MediaUtils_Get_DefaultSettings
 *Descrption    : This function is to get the default settings of audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_Get_DefaultSettings(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_Get_DefaultSettings --->Entry\n");
    int returnStatus;
    returnStatus = RMF_AudioCapture_GetDefaultSettings(&settings);

    std::string outputDetails;
    outputDetails += "   fifoSize = " + std::to_string(settings.fifoSize);
    outputDetails += "   threshold =" + std::to_string(settings.threshold);
    outputDetails += "   format =" + std::to_string(settings.format);
    outputDetails += "   samplingFreq = " + std::to_string(settings.samplingFreq);
    outputDetails += "   delayCompensation_ms = "+ std::to_string(settings.delayCompensation_ms);
    cout << "\noutputDetails:" << outputDetails << endl;

    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_GetDefaultSettings call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetDefaultSettings -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MediaUtils_GetDefaultSettings call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetDefaultSettings -->Exit\n");
        return TEST_FAILURE;
    }

}

/***************************************************************************
 *Function name : MediaUtils_GetCurrentSettings
 *Descrption    : This function is to get the current settings of audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_Get_Current_Settings(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetCurrentSettings --->Entry\n");
    int returnStatus;
    paramHandle = req["paramHandle"].asCString();
    if(paramHandle == "NULL")
	{
        handle = 0;
        returnStatus = RMF_AudioCapture_GetCurrentSettings(handle,&settings);
	}
    else if(paramHandle == "VALID")
	{
        returnStatus = RMF_AudioCapture_GetCurrentSettings(appData.hAudCap,&settings);
	}
    else
	{
	return TEST_FAILURE;
	}

    std::string outputDetails;
    outputDetails += "   fifoSize = " + std::to_string(settings.fifoSize);
    outputDetails += "   threshold =" + std::to_string(settings.threshold);
    outputDetails += "   format =" + std::to_string(settings.format);
    outputDetails += "   samplingFreq = " + std::to_string(settings.samplingFreq);
    outputDetails += "   delayCompensation_ms = "+ std::to_string(settings.delayCompensation_ms);
    cout << "\noutputDetails:" << outputDetails << endl;

    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        response["details"] = outputDetails;
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_GetCurrentSettings call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetCurrentSettings -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MediaUtils_GetCurrentSettings call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetCurrentSettings -->Exit\n");
        return TEST_FAILURE;
    }

}



/***************************************************************************
 *Function name : MediaUtils_GetStatus
 *Descrption    : This function is to get the status of audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_Get_Status(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetStatus --->Entry\n");
    int returnStatus;
    returnStatus = RMF_AudioCapture_GetStatus(appData.hAudCap,&status);
    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_GetStatus call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetStatus -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MediaUtils_GetStatus call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_GetStatus -->Exit\n");
        return TEST_FAILURE;
    }

}


/***************************************************************************
 *Function name : MediaUtils_AudioCaptureStart
 *Descrption    : This function is to start the audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_AudioCaptureStart(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStart --->Entry\n");

    
    /*For cbBufferReady*/
    appData.prevCbTime = 0;
    settings.cbBufferReadyParm  = &appData;
    settings.samplingFreq = racFreq_e48000;
    
    int returnStatus;

    string paramHandle, paramBufferReady,paramFifosize;
    paramBufferReady = req["paramBufferReady"].asCString();
    paramHandle = req["paramHandle"].asCString();
    paramFifosize = req["paramFifosize"].asCString();
    if(paramBufferReady == "NOTREADY")
        {
	settings.cbBufferReady =0;
	}
    else if(paramBufferReady == "READY")
	{
	settings.cbBufferReady = cbBufferReady;
	}
    else
	{
	return TEST_FAILURE;
	}

    if(paramFifosize == "NULL")
        {
        settings.fifoSize = 0;
	settings.threshold = 0;
        }
    else if(paramFifosize == "VALID")
        {
        /* 8KB PCM data buffer */
        settings.threshold          =  8 * 1024;
        settings.fifoSize           =  64 * 1024;
        }
    else
        {
        return TEST_FAILURE;
        }
    if(paramHandle == "NULL")
	{
	handle = 0;
	returnStatus = RMF_AudioCapture_Start(handle,&settings);
	}
    else if(paramHandle == "VALID")
	{
	returnStatus = RMF_AudioCapture_Start(appData.hAudCap,&settings);
	}
    else
	{
	return TEST_FAILURE;
	}


    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_AudioCaptureStart call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStart -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MediaUtils_AudioCaptureStart call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStart -->Exit\n");
        return TEST_FAILURE;
    }

}

/***************************************************************************
 *Function name : MediaUtils_AudioCaptureStop
 *Descrption    : This function is to stop the audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_AudioCaptureStop(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStop --->Entry\n");
    int returnStatus;
    paramHandle = req["paramHandle"].asCString();
    if(paramHandle == "NULL")
	{
        handle =0;
        returnStatus = RMF_AudioCapture_Stop(handle);
	}
    else if(paramHandle == "VALID")
	{
	
        returnStatus = RMF_AudioCapture_Stop(appData.hAudCap);
	}

    if(!returnStatus)
    {
        response["result"] = "SUCCESS";
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_AudioCaptureStop call is SUCCESS");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStop -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        DEBUG_PRINT(DEBUG_ERROR, "MediaUtils_AudioCaptureStop call is FAILURE");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCaptureStop -->Exit\n");
        return TEST_FAILURE;
    }

}

/***************************************************************************
 *Function name : MediaUtils_AudioCapture_Close
 *Descrption    : This function is to get the default settings of audio capture
 *****************************************************************************/
bool MediaUtilsAgent::MediaUtils_AudioCapture_Close(IN const Json::Value& req, OUT Json::Value& response)
{
    DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Close --->Entry\n");
    paramHandle = req["paramHandle"].asCString();
    if(paramHandle == "NULL")
	{
	handle = 0;
        audiocapture_Close=RMF_AudioCapture_Close(handle);
	}
    else if(paramHandle == "VALID")
	{
        audiocapture_Close=RMF_AudioCapture_Close(appData.hAudCap);
	}
    printf("audiocapture_Close: %d \n",audiocapture_Close);
    if (!audiocapture_Close)
    {
        response["result"] = "SUCCESS";
        response["details"] = "RMF_AudioCapture_Close success\n";
        DEBUG_PRINT(DEBUG_LOG, "MediaUtils_AudioCapture_Close success\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Close -->Exit\n");
        return TEST_SUCCESS;
    }
    else
    {
        response["result"] = "FAILURE";
        response["details"] = "RMF_AudioCapture_Close failed\n";
        DEBUG_PRINT(DEBUG_ERROR, "RMF_AudioCapture_Close failed\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_AudioCapture_Close -->Exit\n");
        return TEST_FAILURE;
    }

}
/***************************************************************************
 * Function name : MediaUtilsAgent::MediaUtils_ExecuteCmd()
 *
 * Arguments     : Input arguments are command to execute in box
 *
 * Description   : This will execute linux commands in box
 * ***************************************************************************/
bool MediaUtilsAgent::MediaUtils_ExecuteCmd(IN const Json::Value& request, OUT Json::Value& response)
{
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_ExecuteCmd ---> Entry\n");
        string fileinfo = request["command"].asCString();
        FILE *fp = NULL;
        char readRespBuff[BUFF_LENGTH];

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
                DEBUG_PRINT(DEBUG_ERROR, "popen() failure\n");

                return TEST_FAILURE;
        }

        /*copy the response to a buffer */
        while(fgets(readRespBuff,sizeof(readRespBuff),fp) != NULL)
        {
		DEBUG_PRINT(DEBUG_TRACE, "Command Response:\n");
		cout<<"readRespBuff:"<<readRespBuff<<endl;
        }

        pclose(fp);

	string respResult(readRespBuff);
        DEBUG_PRINT(DEBUG_TRACE, "\n\nResponse: %s\n",respResult.c_str());
        response["result"] = "SUCCESS";
        response["details"] = respResult;
        DEBUG_PRINT(DEBUG_LOG, "Execution success\n");
        DEBUG_PRINT(DEBUG_TRACE, "MediaUtils_ExecuteCmd -->Exit\n");
        return TEST_SUCCESS;
}
/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool MediaUtilsAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");

    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }

    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_AudioCapture_Open");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_Get_DefaultSettings");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_Get_Current_Settings");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_Get_Status");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_AudioCaptureStart");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_AudioCaptureStop");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_AudioCapture_Close");
    ptrAgentObj->UnregisterMethod("TestMgr_MediaUtils_ExecuteCmd");
    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is MediaUtilsAgent Object

Description   : This function will be used to destory the MediaUtilsAgent object.
**************************************************************************/
extern "C" void DestroyObject(MediaUtilsAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying MediaUtils Agent object\n");
        delete stubobj;
}

