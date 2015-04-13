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
#include <iostream>
#include <unistd.h>
#include <sstream>
#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <fstream>
#include <string.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <glib.h>
#include <termios.h>
#include <sys/time.h>

#include "mediaplayersink.h"
#include "hnsource.h"
#include "DVRSource.h"
#include "DVRSink.h"
#include "dvrmanager.h"
#include "rmf_osal_init.h"
#include "rmfqamsrc.h"
#include "rmf_platform.h"
#define FETCH_STREAMING_INT_NAME "streaming_interface_file"

using namespace std;

#define SUCCESS 0
#define FAILURE 1

#ifdef USE_SOC_INIT
void soc_uninit();
void soc_init(int , char *, int );
#endif

string g_tdkPath = getenv("TDK_PATH");

int usage()
{
        cout<<"Usage:"<<endl;
        cout<<"============="<<endl;
        cout<<"tdkRmfApp <options> <url>"<<endl;
        cout<<endl<<"Options:"<<endl;
        cout<<"=============="<<endl;
        cout<<"play <option>:"<<endl;
        cout<<"play -l for the entered url (plays for 60 seconds) live play back and play -d for Dvr play back (plays for 60 seconds)."<<endl;
        cout<<endl<<"Examples:"<<endl;
        cout<<"For Live playback with -l:"<<endl;
	cout<<"tdkRmfApp play -l ocap://0x236A"<<endl;
	cout<<"For Dvr playback with -d:"<<endl;
	cout<<"tdkRmfApp play -d 467467695758585"<<endl;
	cout<<"For live Rewind :"<<endl;
	cout<<"tdkRmfApp rew -4 -l ocap://0x236A"<<endl;
	cout<<"For live Fast-Forward :"<<endl;
	cout<<"tdkRmfApp ff 4 -l ocap://0x236A"<<endl;
	cout<<"For DVR Rewind :"<<endl;
	cout<<"tdkRmfApp rew -4 -d 467467695758585"<<endl;
	cout<<"For live Fast-Forward :"<<endl;
	cout<<"tdkRmfApp ff 4 -d 467467695758585"<<endl;
	#ifndef SINGLE_TUNER_IP_CLIENT
        cout<<endl<<"record:"<<endl;
        cout<<"record option used to record given url. Each record option should be passed with a unique Id to indetify the recording."<<endl;
        cout<<endl<<"usage:"<<endl;
        cout<<"record <id> <duration> <title> <url>"<<endl;
        cout<<"<id>: unique id to identify the recording."<<endl;
        cout<<"<duration>: recording duration in mins."<<endl;
        cout<<"<title>: Title name to your recording."<<endl;
        cout<<endl<<"Examples:"<<endl;
        cout<<"tdkRmfApp record 111111 5 test_record ocap://0x236A"<<endl<<endl;
	cout<<"ls:"<<endl;
	cout<<"List the avaliable recording with the details"<<endl;
	cout<<endl<<"Example:"<<endl;
	cout<<"tdkRmfApp ls"<<endl<<endl<<endl;
#endif
        return 0;
}

static HNSource* hnSource=NULL;
static MediaPlayerSink* mpSink=NULL;
#ifndef SINGLE_TUNER_IP_CLIENT		
static DVRSink* dvrSink=NULL;
#endif

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

}

static long long getCurrentTime()
{
        struct timeval tv;
        long long currentTime;

        gettimeofday( &tv, 0 );

        currentTime= (((unsigned long long)tv.tv_sec) * 1000 + ((unsigned long long)tv.tv_usec) / 1000);

        return currentTime;
}

std::string fetchStreamingInterface()
{
        ifstream interfacefile;
        string Fetch_Streaming_interface_cmd, Streaming_Interface_name,line;
        Streaming_Interface_name = g_tdkPath + "/" + FETCH_STREAMING_INT_NAME;
/*      //Fetch_Streaming_interface_cmd = g_tdkPath + "/" + FETCH_STREAMING_INT_SCRIPT;
        //string fetch_streaming_int_chk= "source "+Fetch_Streaming_interface_cmd;
        //try
        {
                system((char*)fetch_streaming_int_chk());
        }
        catch(...)
        {
                DEBUG_PRINT(DEBUG_ERROR,"Exception occured execution of streaming ip fetch script\n");
                DEBUG_PRINT(DEBUG_TRACE, " ---> Exit\n");
                return "FAILURE<DETAILS>Exception occured execution of streaming ip fetch script";

        }
*/

        interfacefile.open(Streaming_Interface_name.c_str());
        if(interfacefile.is_open())
        {
                if(getline(interfacefile,line)>0);
                {
                        interfacefile.close();
                        return line;
                }
                interfacefile.close();
                return "FAILURE<DETAILS>Proper result is not found in the streaming interface name file";
        }
        else
        {
                return "FAILURE<DETAILS>Unable to open the streaming interface  file";
        }


}

int rmfHnSourceInitialize(string ocapIdOrRecordId,string liveOrDvr = "-l")
{
	RMFResult retResult = RMF_RESULT_SUCCESS;

	/*Get the Streaming Ip Address */
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
                       	std::cout << token << std::endl;
	              	streaming_interface.erase(0, pos + delimiter.length());
                 }
		 cout<<token<<endl;
                 return FAILURE;
	}
	const char * streaming_interface_name = streaming_interface.c_str();
        string streamingIp = GetHostIP(streaming_interface_name);
        string url;
	
	if((liveOrDvr != "-l") || (liveOrDvr != "-d"))
	{
		usage();
	}
	
	hnSource = new HNSource();
	if ( NULL == hnSource )
        {
  	      cout<<"Error: unable to create HNSrc"<<endl;
              return FAILURE;
        }
        cout<<"HNSource instance created SUCCESS"<<endl;


        retResult = hnSource->init();
        if(RMF_RESULT_SUCCESS != retResult)
        {
       		cout<<"HNSource init() FAILURE";
		delete hnSource;

                return FAILURE;
        }
        cout<<"HNSource init() SUCCESS"<<endl;


        /*Constructing url of the form: http://<streamingIp>:8080/vldms/tuner?ocap_locator=ocap://0x125d */
        url = "http://";
        url.append(streamingIp);
	/*url.append(":8080/vldms/tuner?ocap_locator=");*/
	if(liveOrDvr == "-l")
	{
		url.append(":8080/hnStreamStart?live=");
        	url.append(ocapIdOrRecordId);
		url.append("&tsb=26");
	}
	else if(liveOrDvr == "-d")
	{
		url.append(":8080/hnStreamStart?recordingId=");
        	url.append(ocapIdOrRecordId);
		url.append("&segmentId=0");
	}

        cout<<"Complete URL:"<<url<<endl;

        retResult = hnSource->open(url.c_str(),0);
        if(RMF_RESULT_SUCCESS != retResult)
        {
        	cout<<"Error: HNSource open() FAILURE"<<endl;

		hnSource->term();
		delete hnSource;		

                return FAILURE;
        }
        cout<<"HNSource open() SUCCESS"<<endl;
		
	
	return SUCCESS;
}

int rmfHnSourceUnintialize()
{
	RMFResult retResult = RMF_RESULT_SUCCESS;
	
	retResult = hnSource->pause();
        if(RMF_RESULT_SUCCESS != retResult)
        {
                cout<<"Error: HNSource pause() FAILURE"<<endl;

		hnSource->close();
		hnSource->term();
		delete hnSource;

                return FAILURE;
        }
        cout<<"HNSrc pause() successful"<<endl;
	

        retResult = hnSource->close();
        if(RMF_RESULT_SUCCESS != retResult)
        {
	        cout<<"Error: HNSource close() FAILURE"<<endl;

		hnSource->term();
 		delete hnSource;		

                return FAILURE;
        }
        cout<<"HNSource close() SUCCESS"<<endl;

	retResult = hnSource->term();
        if(RMF_RESULT_SUCCESS != retResult)
        {
               cout<<"HNSource term() FAILURE"<<endl;

		delete hnSource;
               return FAILURE;
        }
        cout<<"HNSsource term() SUCCESS"<<endl;

	delete hnSource;

	return SUCCESS;
}

int rmfMpSinkInitialize()
{
	RMFResult retResult = RMF_RESULT_SUCCESS;
        bool applyNow = true;
        unsigned x = 0;
        unsigned y = 0;
        unsigned height = 720;
        unsigned width = 1280;

	mpSink = new MediaPlayerSink();
        if ( NULL == mpSink )
        {
        	cout<<"Error: unable to create MediaPlayerSink"<<endl;
                return FAILURE;
        }
        cout<<"MediaPlayerSink instance created SUCCESS"<<endl;
	
        retResult = mpSink->init();
        if(RMF_RESULT_SUCCESS != retResult)
        {
        	cout<<"MediaPlayerSink init() FAILURE";

		delete mpSink;
                return FAILURE;
        }
        cout<<"MediaPlayerSink init() SUCCESS"<<endl;


        cout<<"setVideoRectangle value x: "<<x<<endl;
	cout<<"setVideoRectangle value y: "<<y<<endl;
        cout<<"setVideoRectangle value height: "<<height<<endl;
        cout<<"setVideoRectangle value width: "<<width<<endl;
        cout<<"setVideoRectangle value apply: "<<applyNow<<endl;

	retResult = mpSink->setVideoRectangle(x, y, width, height,applyNow);
        if(RMF_RESULT_SUCCESS != retResult)
        {
                cout<<"Error: MediaPlayerSink setVideoRectangle() FAILURE"<<endl;
		
		mpSink->term();
		delete mpSink;

                return FAILURE;
        }

	retResult = mpSink->setSource(hnSource);
        if(RMF_RESULT_SUCCESS != retResult)
        {
                cout<<"Error: MediaPlayerSink setSource() FAILURE"<<endl;

		mpSink->term();
		delete mpSink;

                return FAILURE;
        }

	return SUCCESS;
}

int rmfMpSinkUninitialize()
{
	RMFResult retResult = RMF_RESULT_SUCCESS;

        retResult = mpSink->term();
        if(RMF_RESULT_SUCCESS != retResult)
        {
               cout<<"MediaPlayerSink term() FAILURE"<<endl;
		
	       delete mpSink;
               return FAILURE;
        }
        cout<<"MediaPlayerSink term() SUCCESS"<<endl;

	delete mpSink;

	return SUCCESS;
}

#ifndef SINGLE_TUNER_IP_CLIENT
int rmfDvrSinkInitialize(string dvrRecordId,int duration,string title,string ocapId)
{
	RMFResult retResult = RMF_RESULT_SUCCESS;
	/*Get the Streaming Ip Address */

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
                       	std::cout << token << std::endl;
	              	streaming_interface.erase(0, pos + delimiter.length());
                 }
		 cout<<token<<endl;
                 return FAILURE;
	}
	const char * streaming_interface_name = streaming_interface.c_str();
        string streamingIp = GetHostIP(streaming_interface_name);
	/* Make an entry of recording in the DVR Manager.*/
        string recordId = dvrRecordId;
	
	/*Constructing url of the form: http://<streamingIp>:8080/vldms/tuner?ocap_locator=ocap://0x125d */
        string url = "http://";
        url.append(streamingIp);
        /*url.append(":8080/vldms/tuner?ocap_locator=");*/
	url.append(":8080/hnStreamStart?live=");
        url.append(ocapId);

        cout<<"Complete URL:"<<url<<endl;

        string playUrl = url;
        long long recDuration = duration;

        char properties[256];
        sprintf( properties, "{\"title\":\"%s\"}", title.c_str());

        RecordingSpec spec;

        spec.setRecordingId(recordId);
        spec.addLocator(playUrl);
        spec.setProperties(properties);
        spec.setStartTime(getCurrentTime());
        spec.setDuration(recDuration);
        spec.setDeletePriority("P3");
        spec.setBitRate(RecordingBitRate_low);

        int result= DVRManager::getInstance()->createRecording( spec );
        if ( result != DVRResult_ok )
        {
                cout<<"Error: Unable to create recording for id: "<<recordId<<endl;

                return FAILURE;
        }

        cout<<"Creating recording for id: "<<recordId<<" success"<<endl;


	/*Initialzing the dvrSink instance */
        dvrSink = new DVRSink(dvrRecordId);
        if ( NULL == dvrSink )
        {
	        cout<<"Error: unable to create DVRSink"<<endl;
                return FAILURE;
        }
        cout<<"DVRSink instance created SUCCESS"<<endl;

        retResult = dvrSink->init();
        if(RMF_RESULT_SUCCESS != retResult)
        {
               cout<<"DVRSink init() FAILURE"<<endl;
	
               delete dvrSink;
               return FAILURE;
        }
        cout<<"DVRSink init() SUCCESS"<<endl;

	retResult = dvrSink->setSource(hnSource);
        if(RMF_RESULT_SUCCESS != retResult)
        {
                cout<<"Error: DVRSink setSource() FAILURE"<<endl;

                dvrSink->term();
                delete dvrSink;

                return FAILURE;
        }

	return SUCCESS;
}

int rmfDvrSinkUninitialize()
{
	RMFResult retResult = RMF_RESULT_SUCCESS;

	retResult = dvrSink->term();
	if(RMF_RESULT_SUCCESS != retResult)
        {
                cout<<"Error: DVRSink setSource() FAILURE"<<endl;
		
		delete dvrSink;
		return FAILURE;
	}
        cout<<"DVRSink term() SUCCESS"<<endl;

	delete dvrSink;

	return SUCCESS;
}
#endif

int main(int argc, char *argv[])
{
	int result = SUCCESS;	
	RMFResult retResult = RMF_RESULT_SUCCESS;	
#ifdef USE_SOC_INIT	
	//Initialize SOC
	soc_init(1, "tdkRmfApp", 1);
#endif
        switch(argc)
        {
	case 2:
	      {
                cout<<"Num of arg="<<argc<<"  "<<endl;
                string list(argv[1]);
#ifndef SINGLE_TUNER_IP_CLIENT		
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
                	                cout<< " title: (NULL)";
                      	      }
	                      else
        	              {
                	                cout << " title: " << pRecInfo->title;
	                      }

        	              recDuration = dvm->getRecordingDuration(pRecInfo->recordingId.c_str());
                	      cout << " Duration: " << recDuration << "(in secs)";

	                      for (int i = 0;i < pRecInfo->segmentCount && i != 1; i++)
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
                cout<<"Num of arg="<<argc<<"  "<<endl;
                string play(argv[1]);
		string liveOrDvr(argv[2]);
		string ocapIdOrRecordId(argv[3]);

                if(play == "play")
                {
                        cout<<"entered play option"<<endl;
			
			result = rmfHnSourceInitialize(ocapIdOrRecordId,liveOrDvr);			
			if(result != SUCCESS)
			{
				cout<<"Error: HnSource Initialize failed"<<endl;	
				return FAILURE;
			}
			cout<<"HnSource Initialize success"<<endl;
			
			result = rmfMpSinkInitialize();	
			if(result != SUCCESS)
                        {
                                cout<<"Error: MpSink Initialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"MpSink Initialize success"<<endl;
		
			/*Start playing*/	
			retResult = hnSource->play();	
                        if(RMF_RESULT_SUCCESS != retResult)
                        {
        	                cout<<"Error: HnSource play() FAILURE"<<endl;
                	        return FAILURE;
                	}
	                cout<<"HNSrc play() success"<<endl;
			cout<<"Plays for 60 secs"<<endl;			
	
			sleep(60);
			
			result = rmfHnSourceUnintialize();	
                	if(result != SUCCESS)
                        {
                                cout<<"Error: HnSource Uninitialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"HnSource Uninitialize success"<<endl;
		
			result = rmfMpSinkUninitialize();
                        if(result != SUCCESS)
                        {
                                cout<<"Error: MpSink Uninitialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"MpSink Uninitialize success"<<endl;
                }
                else
                {
                        usage();
                }
                break;
                }
	case 5:
		{
			cout<<"Num of arg="<<argc<<" "<<endl;
			string trickplay(argv[1]);
	                string trickplay_value(argv[2]);
        	        string source(argv[3]);
                	string ocapId(argv[4]);

 			if(trickplay == "rew")
	                {
				cout<<"entered rewind option"<<endl;
				result = rmfHnSourceInitialize(ocapId,source);
                        	if(result != SUCCESS)
                        	{
                                	cout<<"Error: HnSource Initialize failed"<<endl;
                                	return FAILURE;
                        	}
                        	cout<<"HnSource Initialize success"<<endl;

                        	result = rmfMpSinkInitialize();
                        	if(result != SUCCESS)
                        	{
                                	cout<<"Error: MpSink Initialize failed"<<endl;
                                	return FAILURE;
                        	}
                        	cout<<"MpSink Initialize success"<<endl;

                        	/*Start playing*/
                        	retResult = hnSource->play();
                        	if(RMF_RESULT_SUCCESS != retResult)
                        	{
                                	cout<<"Error: HnSource play() FAILURE"<<endl;
                                	return FAILURE;
                        	}
                        	cout<<"HNSrc play() success"<<endl;
                        	cout<<"Plays for 60 secs"<<endl;

                        	sleep(60);
				double mediaTime;
				retResult = hnSource->getMediaTime(mediaTime);
			        cout<<"Return of get Media time "<<retResult<<endl;
			        cout<<" Media time Value "<<mediaTime<<endl;
				float trickplayspeed = strtof(trickplay_value.c_str(),NULL);
				retResult = hnSource->play(trickplayspeed,mediaTime);
				if(RMF_RESULT_SUCCESS != retResult)
                                {
                                        cout<<"Error: HnSource play() FAILURE"<<endl;
                                        return FAILURE;
                                }
                                cout<<"HNSrc play() success"<<endl;
                                cout<<"Rewind for 30 secs"<<endl;
				sleep(30);
                        	result = rmfHnSourceUnintialize();
                        	if(result != SUCCESS)
                        	{
                                	cout<<"Error: HnSource Uninitialize failed"<<endl;
                                	return FAILURE;
                        	}
                        	cout<<"HnSource Uninitialize success"<<endl;

                        	result = rmfMpSinkUninitialize();
                        	if(result != SUCCESS)
                        	{
                                	cout<<"Error: MpSink Uninitialize failed"<<endl;
                                	return FAILURE;
                        	}
                        	cout<<"MpSink Uninitialize success"<<endl;


			}
  			else if(trickplay == "ff")
                        {
                                cout<<"Entered fast forward option"<<endl;
                                result = rmfHnSourceInitialize(ocapId,source);
                                if(result != SUCCESS)
                                {
                                        cout<<"Error: HnSource Initialize failed"<<endl;
                                        return FAILURE;
                                }
                                cout<<"HnSource Initialize success"<<endl;

                                result = rmfMpSinkInitialize();
                                if(result != SUCCESS)
                                {
                                        cout<<"Error: MpSink Initialize failed"<<endl;
                                        return FAILURE;
                                }
                                cout<<"MpSink Initialize success"<<endl;

                                /*Start playing*/
                                retResult = hnSource->play();
                                if(RMF_RESULT_SUCCESS != retResult)
                                {
                                        cout<<"Error: HnSource play() FAILURE"<<endl;
                                        return FAILURE;
                                }
                                cout<<"HNSrc play() success"<<endl;
                                cout<<"Plays for 60 secs"<<endl;

                                sleep(60);
				/*retResult = hnSource->pause();
			        if(RMF_RESULT_SUCCESS != retResult)
       	 			{
                			cout<<"Error: HNSource pause() FAILURE"<<endl;
                			return FAILURE;
        			}
				sleep(5);*/
                                double mediaTime=0;
                                retResult = hnSource->getMediaTime(mediaTime);
                                cout<<"Return of get Media time "<<retResult<<endl;
                                cout<<" Media time Value "<<mediaTime<<endl;

				retResult = hnSource->setVideoLength(mediaTime);
				cout<<"Return of get set Video Length "<<retResult<<endl;

				mediaTime=0;
	
                                float trickplayspeed = strtof(trickplay_value.c_str(),NULL);
                                retResult = hnSource->play(trickplayspeed,mediaTime);
                                if(RMF_RESULT_SUCCESS != retResult)
                                {
                                        cout<<"Error: HnSource play() FAILURE"<<endl;
                                        return FAILURE;
                                }
                                cout<<"HNSrc play() success"<<endl;
                                cout<<"Rewind for 30 secs"<<endl;
                                sleep(30);
                         	result = rmfHnSourceUnintialize();
                                if(result != SUCCESS)
                                {
                                        cout<<"Error: HnSource Uninitialize failed"<<endl;
                                        return FAILURE;
                                }
                                cout<<"HnSource Uninitialize success"<<endl;

                                result = rmfMpSinkUninitialize();
                                if(result != SUCCESS)
                                {
                                        cout<<"Error: MpSink Uninitialize failed"<<endl;
                                        return FAILURE;
                                }
                                cout<<"MpSink Uninitialize success"<<endl;

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
                cout<<"Num of arg="<<argc<<" "<<endl;
                string record(argv[1]);
		string recordId(argv[2]);
		string duration(argv[3]);
		string title(argv[4]);
		string ocapId(argv[5]);
		
		int recDuration = 0;
		recDuration = atoi(duration.c_str());
		
                if(record == "record")
                {
                        cout<<"entered record option"<<endl;
			
			result = rmfHnSourceInitialize(ocapId);
                        if(result != SUCCESS)
                        {
                                cout<<"Error: HnSource Initialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"HnSource Initialize success"<<endl;

			result = rmfDvrSinkInitialize(recordId,recDuration,title,ocapId);
                        if(result != SUCCESS)
                        {
                                cout<<"Error: MpSink Initialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"MpSink Initialize success"<<endl;

                        /*Start playing*/
                        retResult = hnSource->play();
                        if(RMF_RESULT_SUCCESS != retResult)
                        {
                                cout<<"Error: HnSource play() FAILURE"<<endl;
                                return FAILURE;
                        }
                        cout<<"HNSrc play() success"<<endl;
		
			cout<<"Duration of recording: "<<recDuration<<endl;
			cout<<"Sleeping for "<<recDuration<<" mins"<<endl;	
			sleep(recDuration * 60);

			result = rmfHnSourceUnintialize();
                        if(result != SUCCESS)
                        {
                                cout<<"Error: HnSource Uninitialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"HnSource Uninitialize SUCCESS"<<endl;
	
			result = rmfDvrSinkUninitialize();
                        if(result != SUCCESS)
                        {
                                cout<<"Error: DvrSink Uninitialize failed"<<endl;
                                return FAILURE;
                        }
                        cout<<"DvrSink Uninitialize SUCCESS"<<endl;
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
	// Uninitialize SOC
	soc_uninit();
#endif

        return 0;
}
