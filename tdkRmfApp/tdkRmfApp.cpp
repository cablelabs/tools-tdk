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
using namespace std;

#define SUCCESS 0
#define FAILURE 1


int usage()
{
        cout<<"Usage:"<<endl;
        cout<<"============="<<endl;
        cout<<"tdkRmfApp <option> <url>"<<endl;
        cout<<endl<<"Options:"<<endl;
        cout<<"=============="<<endl;
        cout<<"play:"<<endl;
        cout<<"play option is used to play the entered url(plays for 60 seconds)."<<endl;
        cout<<endl<<"Examples:"<<endl;
        cout<<"tdkRmfApp play ocap://0x236A"<<endl;
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

        return 0;
}

static HNSource* hnSource=NULL;
static MediaPlayerSink* mpSink=NULL;
static DVRSink* dvrSink=NULL;

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

int rmfHnSourceInitialize(string ocapId)
{
	RMFResult retResult = RMF_RESULT_SUCCESS;

	/*Get the Streaming Ip Address */
        string streamingIp = GetHostIP("eth1");
        string url;
	
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
	url.append(":8080/vldms/tuner?ocap_locator=");
        url.append(ocapId);

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


int rmfDvrSinkInitialize(string dvrRecordId,int duration,string title,string ocapId)
{
	RMFResult retResult = RMF_RESULT_SUCCESS;
	/*Get the Streaming Ip Address */
        string streamingIp = GetHostIP("eth1");
	/* Make an entry of recording in the DVR Manager.*/
        string recordId = dvrRecordId;
	
	/*Constructing url of the form: http://<streamingIp>:8080/vldms/tuner?ocap_locator=ocap://0x125d */
        string url = "http://";
        url.append(streamingIp);
        url.append(":8080/vldms/tuner?ocap_locator=");
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

int main(int argc, char *argv[])
{
	int result = SUCCESS;	
	RMFResult retResult = RMF_RESULT_SUCCESS;	

        switch(argc)
        {
	case 2:
	      {
                cout<<"Num of arg="<<argc<<"  "<<endl;
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
		{

			usage();
		}
		break;
	      }
        case 3:
              {
                cout<<"Num of arg="<<argc<<"  "<<endl;
                string play(argv[1]);
		string ocapId(argv[2]);

                if(play == "play")
                {
                        cout<<"entered play option"<<endl;
			
			result = rmfHnSourceInitialize(ocapId);			
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
        case 6:
                {
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
                {
                        usage();
                }
                break;
                }
        default:
                usage();
                break;
        }

        return 0;
}