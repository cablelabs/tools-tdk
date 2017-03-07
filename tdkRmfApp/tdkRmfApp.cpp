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
#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <fstream>
#include <string.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/types.h>

#include "mediaplayersink.h"
#include "hnsource.h"
#ifndef SINGLE_TUNER_IP_CLIENT
#include "DVRSink.h"
#include "dvrmanager.h"
#endif

using namespace std;

#define SUCCESS 0
#define FAILURE 1
#define DEBUG_PRINT(pui8Debugmsg...)\
      do{\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y %T.",localtime(&curtime));\
                fprintf(stdout,"\n%s%ld [%s %s():%d] [pid=%d] ", buffer, tv.tv_usec, "tdkRmfApp", __FUNCTION__, __LINE__, getpid());\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
      }while(0)

/*
 Fetching Streaming Interface Name
 */
#define BUFFER_LENGTH            64
#define STREAMING_INTERFACE      "Streaming Interface"
#define FETCH_STREAMING_INT_FILE "streaming_interface_file"

#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int , char *, int );
#endif

//******************************************//
// Helper function: GetHostIP
// Function: Gets IP of a given interface
//******************************************//

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
                DEBUG_PRINT("Interface %s has IP %s",szInterface, szAddressBuffer);
                break;
            }
        }
    }

    if (pIfAddrStruct != NULL)
    {
        freeifaddrs (pIfAddrStruct);
    }

    return szAddressBuffer;
}

//******************************************//
// Helper function: getCurrentTime
// Function: Gets Current Time in millisecs
//******************************************//

static long long getCurrentTime()
{
    struct timeval tv;
    long long currentTime;

    gettimeofday( &tv, 0 );

    currentTime= (((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000);

    return currentTime;
}

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
        char *g_tdkPath = getenv("TDK_PATH");

        DEBUG_PRINT("Fetch Streaming Interface function --> Entry\n");
        if (NULL == g_tdkPath)
        {
        DEBUG_PRINT("Error! TDK_PATH not exported \n");
        return "FAILURE<DETAILS>TDK_PATH not exported";
        }

	streamingInterfaceFile = string(g_tdkPath) + "/" + FETCH_STREAMING_INT_FILE;
        fetchInterfaceCmd = "cat " + streamingInterfaceFile + "| grep \"" + STREAMING_INTERFACE + "\" | cut -d \"=\" -f 2 |tr -d '\\r\\n'";

        /*Reading the streaming_interface_file to read the interface name */
	interfaceFile = popen(fetchInterfaceCmd.c_str(), "r");
        if(interfaceFile == NULL)
        {
                DEBUG_PRINT("\nUnable to open the streaming interface file.\n");
                return "FAILURE<DETAILS>Unable to open the streaming interface file";
        }
	if(fgets(streamingInterfaceName, BUFFER_LENGTH, interfaceFile) != NULL)
        {
                pclose(interfaceFile);
                DEBUG_PRINT("Streaming interface = %s \n",streamingInterfaceName);
                DEBUG_PRINT("Fetch Streaming Interface function--> Exit\n");
                return streamingInterfaceName;
        }
        else
        {
                pclose(interfaceFile);
                DEBUG_PRINT("\nStreaming interface not fetched\n");
                return "FAILURE<DETAILS>Proper interface name not found in streaming interface file";
        }
}

static HNSource* hnSource=NULL;
static MediaPlayerSink* mpSink=NULL;
#ifndef SINGLE_TUNER_IP_CLIENT
static DVRSink* dvrSink=NULL;
#endif

//***********************//
// RMF Function: rmfHnSourceInitialize
// HN Source Init
//***********************//

int rmfHnSourceInitialize(string ocapIdOrRecordId,string liveOrDvr = "-l")
{
    RMFResult retResult = RMF_RESULT_SUCCESS;

    DEBUG_PRINT("Id: %s option: %s\n", ocapIdOrRecordId.c_str(), liveOrDvr.c_str());
    string streamingIntf = fetchStreamingInterface();
    if (streamingIntf.find("FAILURE") != std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        size_t pos = 0;
        while ((pos = streamingIntf.find(delimiter)) != std::string::npos) {
            token = streamingIntf.substr(0, pos);
            streamingIntf.erase(0, pos + delimiter.length());
        }

        DEBUG_PRINT("Error: %s", token.c_str());
        return FAILURE;
    }

    /*Get the Streaming Ip Address */
    string streamingIp = GetHostIP(streamingIntf.c_str());
    /*Constructing url of the form: http://<streamingIp>:8080/vldms/tuner?ocap_locator=ocap://0x125d */
    string url = "http://";
    url.append(streamingIp);
    if(liveOrDvr == "-l")
    {
        //url.append(":8080/vldms/tuner?ocap_locator=");
        url.append(":8080/hnStreamStart?live=");
        url.append(ocapIdOrRecordId);
        //Commented the following line to fix the RDKTT-369 issue
        //url.append("&tsb=26");
    }
    else if(liveOrDvr == "-d")
    {
        url.append(":8080/hnStreamStart?recordingId=");
        url.append(ocapIdOrRecordId);
        url.append("&segmentId=0");
    }

    DEBUG_PRINT("Create HNSource instance");
    hnSource = new HNSource();
    if ( NULL == hnSource )
    {
        DEBUG_PRINT("Error: unable to create HNSrc");
        return FAILURE;
    }
    DEBUG_PRINT("HNSource instance creation SUCCESS");

    DEBUG_PRINT("Initialize HNSource instance");
    retResult = hnSource->init();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("HNSource init() FAILURE");
        delete hnSource;
        return FAILURE;
    }
    DEBUG_PRINT("HNSource instance initialization SUCCESS");

    DEBUG_PRINT("HNSource open URL: %s", url.c_str());
    retResult = hnSource->open(url.c_str(),0);
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: HNSource open() FAILURE");
        hnSource->term();
        delete hnSource;
        return FAILURE;
    }
    DEBUG_PRINT("HNSource open URL SUCCESS");

    DEBUG_PRINT("RMF HnSource Initialization Successful");

    return SUCCESS;
}

//***********************//
// RMF Function: rmfHnSourceUnintialize
// HN Source UnInit
//***********************//

int rmfHnSourceUnintialize()
{
    RMFResult retResult = RMF_RESULT_SUCCESS;
    bool retStatus = SUCCESS;

    DEBUG_PRINT("Pause HnSource instance");
    //retResult = hnSource->pause();
    double mediaTime=0.0;
    float trickplayspeed = 0.0f;
    retResult = hnSource->play(trickplayspeed,mediaTime);
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: HNSource pause() FAILURE");
        retStatus = FAILURE;
    }
    else
    {
        DEBUG_PRINT("Pause HnSource instance successful");
    }

    DEBUG_PRINT("Close HnSource instance");
    retResult = hnSource->close();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: HNSource close() FAILURE");
        retStatus = FAILURE;
    }
    else
    {
        DEBUG_PRINT("Close HnSource instance successful");
    }

    DEBUG_PRINT("Term HnSource instance\n");
    retResult = hnSource->term();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("HNSource term() FAILURE");
        retStatus = FAILURE;
    }
    else
    {
        DEBUG_PRINT("Term HnSource instance successful");
    }

    delete hnSource;

    return retStatus;
}

//***********************//
// RMF Function: rmfMpSinkInitialize
// MP Sink Init
//***********************//

int rmfMpSinkInitialize()
{
    RMFResult retResult = RMF_RESULT_SUCCESS;
    bool applyNow = true;
    unsigned x = 0;
    unsigned y = 0;
    unsigned height = 720;
    unsigned width = 1280;

    DEBUG_PRINT("RMF MpSink Initialization");

    DEBUG_PRINT("Create MpSink instance");
    mpSink = new MediaPlayerSink();
    if ( NULL == mpSink )
    {
        DEBUG_PRINT("Error: unable to create MediaPlayerSink");
        return FAILURE;
    }
    DEBUG_PRINT("MpSink instance creation SUCCESS");

    DEBUG_PRINT("Initialize MpSink instance\n");
    retResult = mpSink->init();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("MediaPlayerSink init() FAILURE");
        delete mpSink;
        return FAILURE;
    }
    DEBUG_PRINT("Initialization of MpSink instance SUCCESS");

    DEBUG_PRINT("RMF MpSink SetVideoRectangle [X=%d Y=%d HEIGHT=%d WIDTH=%d ApplyNow=%d]",x,y,height,width,applyNow);
    retResult = mpSink->setVideoRectangle(x, y, width, height,applyNow);
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: MediaPlayerSink setVideoRectangle() FAILURE");
        mpSink->term();
        delete mpSink;
        return FAILURE;
    }
    DEBUG_PRINT("MpSink instance setVideoRectangle SUCCESS");

    DEBUG_PRINT("MpSink instance setSource");
    retResult = mpSink->setSource(hnSource);
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: MediaPlayerSink setSource() FAILURE");
        mpSink->term();
        delete mpSink;
        return FAILURE;
    }
    DEBUG_PRINT("MpSink instance setSource SUCCESS");

    DEBUG_PRINT("RMF MpSink Initialization Successful");
    return SUCCESS;
}

//***********************//
// RMF Function: rmfMpSinkUninitialize
// MP Sink UnInit
//***********************//

int rmfMpSinkUninitialize()
{
    RMFResult retResult = RMF_RESULT_SUCCESS;

    DEBUG_PRINT("Term MpSink instance");
    retResult = mpSink->term();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("MediaPlayerSink term() FAILURE");
        delete mpSink;
        return FAILURE;
    }
    DEBUG_PRINT("Term MpSink instance SUCCESS");

    delete mpSink;

    return SUCCESS;
}

#ifndef SINGLE_TUNER_IP_CLIENT
//*******************************************//
// RMF Function: rmfDvrSinkInitialize
// DVR Sink Init
// Not applicable on Single Tuner IP Client
//******************************************//

int rmfDvrSinkInitialize(string dvrRecordId,int duration,string title,string ocapId)
{
    RMFResult retResult = RMF_RESULT_SUCCESS;

    string streamingIntf = fetchStreamingInterface();
    if (streamingIntf.find("FAILURE") != std::string::npos)
    {
        std::string delimiter = "<FAILURE>";
        std::string token;
        size_t pos = 0;
        while ((pos = streamingIntf.find(delimiter)) != std::string::npos) {
            token = streamingIntf.substr(0, pos);
            streamingIntf.erase(0, pos + delimiter.length());
        }

        DEBUG_PRINT("Error: %s", token.c_str());
        return FAILURE;
    }

    /*Get the Streaming Ip Address */
    string streamingIp = GetHostIP(streamingIntf.c_str());
    /*Constructing url of the form: http://<streamingIp>:8080/vldms/tuner?ocap_locator=ocap://0x125d */
    string url = "http://";
    url.append(streamingIp);
    //url.append(":8080/vldms/tuner?ocap_locator=");
    url.append(":8080/hnStreamStart?live=");
    url.append(ocapId);

    DEBUG_PRINT("Play Url: %s", url.c_str());

    /* Make an entry of recording in the DVR Manager.*/
    long long recDuration = duration;
    char properties[256];
    sprintf( properties, "{\"title\":\"%s\"}", title.c_str());

    RecordingSpec spec;
    spec.setRecordingId(dvrRecordId);
    spec.addLocator(url);
    spec.setProperties(properties);
    spec.setStartTime(getCurrentTime());
    spec.setDuration(recDuration);
    spec.setDeletePriority("P3");
    spec.setBitRate(RecordingBitRate_low);

    DEBUG_PRINT("Create Recording using RecordingSpec\n");
    int result= DVRManager::getInstance()->createRecording( spec );
    if ( result != DVRResult_ok )
    {
        DEBUG_PRINT("Error: Unable to create recording for id: %s", dvrRecordId.c_str());
        return FAILURE;
    }
    DEBUG_PRINT("Creating recording id: %s success", dvrRecordId.c_str());

    /*Initialzing the dvrSink instance */
    DEBUG_PRINT("Create DVRSink instance");
    dvrSink = new DVRSink(dvrRecordId);
    if ( NULL == dvrSink )
    {
        DEBUG_PRINT("Error: unable to create DVRSink");
        return FAILURE;
    }
    DEBUG_PRINT("DVRSink instance creation SUCCESS");

    DEBUG_PRINT("Init DVRSink instance");
    retResult = dvrSink->init();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("DVRSink init() FAILURE");
        delete dvrSink;
        return FAILURE;
    }
    DEBUG_PRINT("DVRSink instance Init SUCCESS");

    DEBUG_PRINT("SetSource Hnsrc instance");
    retResult = dvrSink->setSource(hnSource);
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: DVRSink setSource() FAILURE");
        dvrSink->term();
        delete dvrSink;
        return FAILURE;
    }
    DEBUG_PRINT("DVRSink instance setSource SUCCESS");

    DEBUG_PRINT("RMF DVRSink Initialization Successful");

    return SUCCESS;
}

//*******************************************//
// RMF Function: rmfDvrSinkUninitialize
// DVR Sink UnInit
// Not applicable on Single Tuner IP Client
//******************************************//

int rmfDvrSinkUninitialize()
{
    RMFResult retResult = RMF_RESULT_SUCCESS;

    DEBUG_PRINT("Term RMF DVRSink");
    retResult = dvrSink->term();
    if(RMF_RESULT_SUCCESS != retResult)
    {
        DEBUG_PRINT("Error: DVRSink setSource() FAILURE");
        delete dvrSink;
        return FAILURE;
    }
    DEBUG_PRINT("RMF DVRSink Instance Term SUCCESS");

    delete dvrSink;

    DEBUG_PRINT("RMF DVRSink Un-Initialization Successful");
    return SUCCESS;
}
#endif

void usage()
{
    cout<<endl<<"Usage:"<<endl;
    cout<<"============="<<endl;
    cout<<"tdkRmfApp <operations> <options>"<<endl;
#ifdef SINGLE_TUNER_IP_CLIENT
    cout<<endl<<"Operations: play rew ff"<<endl;
#else
    cout<<endl<<"Operations: play rew ff record ls"<<endl;
#endif
    cout<<"=============="<<endl;

    cout<<"<play/rew/ff> [speed] <-l/-d> <locator/recordId>"<<endl;
    cout<<"play : Live or DVR play back for 60 seconds"<<endl;
    cout<<"rew  : Live Rewind or DVR Rewind for 30 seconds"<<endl;
    cout<<"ff   : Live Fast-Forward or DVR Fast-Forward for 30 seconds"<<endl;
    cout<<"speed: Rewind (-n) or fastfwd (n) speed"<<endl;
    cout<<"[-l] : Live play back [-d] : DVR play back"<<endl;
#ifndef SINGLE_TUNER_IP_CLIENT
    cout<<endl<<"record <id> <duration> <title> <locator>"<<endl;
    cout<<"<id>      : Unique id to identify the recording."<<endl;
    cout<<"<duration>: Recording duration in mins."<<endl;
    cout<<"<title>   : Title name to your recording."<<endl;
    cout<<"<locator> : OcapId of the Service locator to be recorded."<<endl;
    cout<<endl<<"ls : List the available recordings with details"<<endl;
#endif

    cout<<endl<<"Examples:"<<endl;
    cout<<"Live playback        : tdkRmfApp play   -l ocap://0x236A"<<endl;
    cout<<"Live Rewind          : tdkRmfApp rew -4 -l ocap://0x236A"<<endl;
    cout<<"Live Fast-Forward    : tdkRmfApp ff   4 -l ocap://0x236A"<<endl;
    cout<<"DVR playback         : tdkRmfApp play   -d 467467695758585"<<endl;
    cout<<"DVR Rewind           : tdkRmfApp rew -4 -d 467467695758585"<<endl;
    cout<<"DVR Fast-Forward     : tdkRmfApp ff   4 -d 467467695758585"<<endl;
#ifndef SINGLE_TUNER_IP_CLIENT
    cout<<"Create new recording : tdkRmfApp record TestID1111 5 test_record ocap://0x236A"<<endl<<endl;
    cout<<"List recordings      : tdkRmfApp ls"<<endl<<endl<<endl;
#endif
}

//*******************************************//
// Function: Main tdkRmfApp
// Gets the input parameters from command line Input
// and forms pipeline for Live or DVR
//******************************************//

int main(int argc, char *argv[])
{
    int result = SUCCESS;
    RMFResult retResult = RMF_RESULT_SUCCESS;

#ifdef USE_SOC_INIT
    DEBUG_PRINT("Initialize SOC\n");
    soc_init(1, (char*)"tdkRmfApp", 1);
#endif

    DEBUG_PRINT("Number of input arguments = %d\n",argc);
    switch(argc)
    {
    case 2:
    {
#ifndef SINGLE_TUNER_IP_CLIENT
        string list(argv[1]);
        if(list == "ls")
        {
            DVRManager *dvm= DVRManager::getInstance();
            int count = dvm->getRecordingCount();
            int recDuration;
            long long segmentName;

            for( int ii= 0; ii < count; ++ii )
            {
                RecordingInfo *pRecInfo= dvm->getRecordingInfoByIndex( ii );

                cout << "Record: " << ii << " id: " << pRecInfo->recordingId.c_str();

                if (NULL == pRecInfo->title)
                {
                    cout << " title: (NULL)";
                }
                else
                {
                    cout << " title: " << pRecInfo->title;
                }

                recDuration = dvm->getRecordingDuration(pRecInfo->recordingId.c_str());
                cout << " Duration: " << recDuration << "(in secs)";

                for (int i = 0; i < pRecInfo->segmentCount && i != 1; i++)
                {
                    RecordingSegmentInfo *pSegInfo= pRecInfo->segments[i];
                    segmentName = pSegInfo->segmentName;
                    cout << " SegmentName: " << segmentName << endl;
                }

                if (0 == pRecInfo->segmentCount)
                {
                    cout << " SegmentName: 0" << endl;
                }
            }
        }
        else
#endif
        {
            usage();
        }
        break;
    }
    case 4:
    {
        string play(argv[1]);
        string liveOrDvr(argv[2]);
        string ocapIdOrRecordId(argv[3]);

        if((liveOrDvr != "-l") && (liveOrDvr != "-d"))
        {
            DEBUG_PRINT("Invalid option %s", liveOrDvr.c_str());
            usage();
            break;
        }

        if(play == "play")
        {
            DEBUG_PRINT("Entered play option");
            DEBUG_PRINT("Init HnSource");
            result = rmfHnSourceInitialize(ocapIdOrRecordId,liveOrDvr);
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Initialize failed");
                return FAILURE;
            }

            DEBUG_PRINT("Init MpSink");
            result = rmfMpSinkInitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Initialize failed");
                return FAILURE;
            }

            /*Start playing*/
            DEBUG_PRINT("Start HNSrc play\n");
            retResult = hnSource->play();
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("Plays for 60 secs\n");

            sleep(60);

            DEBUG_PRINT("Un-Init HnSource");
            result = rmfHnSourceUnintialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF HnSource Un-Initialization Successful");

            DEBUG_PRINT("Un-Init MpSink");
            result = rmfMpSinkUninitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF MpSink Un-Initialization Successful");
        }
        else
        {
            usage();
        }
        break;
    }
    case 5:
    {
        string trickplay(argv[1]);
        string trickplay_value(argv[2]);
        string source(argv[3]);
        string ocapId(argv[4]);

        if((source != "-l") && (source != "-d"))
        {
            usage();
            break;
        }

        if(trickplay == "rew")
        {
            DEBUG_PRINT("entered rewind option");

            DEBUG_PRINT("Init HnSource");
            result = rmfHnSourceInitialize(ocapId,source);
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Initialize failed");
                return FAILURE;
            }

            DEBUG_PRINT("Init MpSink");
            result = rmfMpSinkInitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Initialize failed");
                return FAILURE;
            }

            /*Start playing*/
            DEBUG_PRINT("Start HNSrc play\n");
            retResult = hnSource->play();
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("Plays for 60 secs\n");

            sleep(60);

            DEBUG_PRINT("Get HNSrc MediaTime");
            double mediaTime;
            retResult = hnSource->getMediaTime(mediaTime);
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource getMediaTime() FAILURE");
            }
            DEBUG_PRINT("Media time Value %lf", mediaTime);

            DEBUG_PRINT("Start HNSrc Rewind\n");
            float trickplayspeed = strtof(trickplay_value.c_str(),NULL);
            retResult = hnSource->play(trickplayspeed,mediaTime);
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("Rewind for 30 secs\n");
            sleep(30);

            DEBUG_PRINT("Un-Init HnSource");
            result = rmfHnSourceUnintialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF HnSource Un-Initialization Successful");

            DEBUG_PRINT("Un-Init MpSink");
            result = rmfMpSinkUninitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF MpSink Un-Initialization Successful");
        }
        else if(trickplay == "ff")
        {
            DEBUG_PRINT("Entered fast forward option");

            DEBUG_PRINT("Init HnSource");
            result = rmfHnSourceInitialize(ocapId,source);
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Initialize failed");
                return FAILURE;
            }

            DEBUG_PRINT("Init MpSink");
            result = rmfMpSinkInitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Initialize failed");
                return FAILURE;
            }

            /*Start playing*/
            DEBUG_PRINT("Start HNSrc play\n");
            retResult = hnSource->play();
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("Plays for 60 secs\n");

            sleep(60);

            double mediaTime=0;
            DEBUG_PRINT("Get HNSrc MediaTime");
            retResult = hnSource->getMediaTime(mediaTime);
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource getMediaTime() FAILURE");
            }
            DEBUG_PRINT("Media time Value: %lf", mediaTime);

            DEBUG_PRINT("Set HNSrc VideoLength");
            retResult = hnSource->setVideoLength(mediaTime);
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource setVideoLength() FAILURE");
            }

            mediaTime=0;
            DEBUG_PRINT("Start HNSrc FastFwd\n");
            float trickplayspeed = strtof(trickplay_value.c_str(),NULL);
            retResult = hnSource->play(trickplayspeed,mediaTime);
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("FastFwd for 30 secs\n");
            sleep(30);

            DEBUG_PRINT("Un-Init HnSource");
            result = rmfHnSourceUnintialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF HnSource Un-Initialization Successful");

            DEBUG_PRINT("Un-Init MpSink");
            result = rmfMpSinkUninitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: MpSink Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF MpSink Un-Initialization Successful");
        }
        else
        {
            usage();
        }
        break;
    }
    case 6:
    {
#ifndef SINGLE_TUNER_IP_CLIENT
        string record(argv[1]);
        string recordId(argv[2]);
        string duration(argv[3]);
        string title(argv[4]);
        string ocapId(argv[5]);

        int recDuration = 0;
        recDuration = atoi(duration.c_str());

        if(record == "record")
        {
            DEBUG_PRINT("entered record option");

            DEBUG_PRINT("Init HnSource");
            result = rmfHnSourceInitialize(ocapId);
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Initialize failed");
                return FAILURE;
            }

            DEBUG_PRINT("Init DVRSink");
            result = rmfDvrSinkInitialize(recordId,recDuration,title,ocapId);
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: DVRSink Initialize failed");
                return FAILURE;
            }

            /*Start playing*/
            DEBUG_PRINT("Start HnSource Play");
            retResult = hnSource->play();
            if(RMF_RESULT_SUCCESS != retResult)
            {
                DEBUG_PRINT("Error: HnSource play() FAILURE");
                return FAILURE;
            }
            DEBUG_PRINT("HNSrc play() success");
            DEBUG_PRINT("Sleeping for recording duration of %d mins",recDuration);
            sleep(recDuration * 60);

            DEBUG_PRINT("Un-Init HnSource");
            result = rmfHnSourceUnintialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: HnSource Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF HnSource Un-Initialization Successful");

            DEBUG_PRINT("Un-Init DVRSink");
            result = rmfDvrSinkUninitialize();
            if(result != SUCCESS)
            {
                DEBUG_PRINT("Error: DvrSink Uninitialize failed");
                return FAILURE;
            }
            DEBUG_PRINT("RMF DVRSink Un-Initialization Successful");
        }
        else
#endif
        {
            usage();
        }
        break;
    }
    default:
        usage();
        break;
    }

#ifdef USE_SOC_INIT
    DEBUG_PRINT("Un-Initialize SOC\n");
    soc_uninit();
#endif

    return 0;
}
