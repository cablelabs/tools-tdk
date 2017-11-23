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

#include "sm_qapp.h"

using namespace std;
bool bBenchmarkEnabled;
QApplication *app;

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
static VideoApplicationEventsService * pVideoApplicationEventsService = NULL;
static VideoApplicationSignalListener *plistener = NULL;
#endif 

void dsHdmiEventHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len);

#ifdef HAS_API_AVINPUT
void AVIListener::onServiceEvent(const QString& event, ServiceParams params)
{
	DEBUG_PRINT(DEBUG_TRACE,"onServiceEvent receieved for %s \n", event.toUtf8().constData());
	QString input = params["inputDeviceActive"].toString();
	DEBUG_PRINT(DEBUG_TRACE,"Input port receievd as %s \n", input.toUtf8().constData());
	if (input.toInt() == (int)PORT)
                app->exit();
	else
		app->exit(FAIL);
}
#endif


#ifdef USE_DISPLAY_SETTINGS
void DisListener::onServiceEvent(const QString& event, ServiceParams params)
{
        QVariantList connectedVideoDisplays = params["connectedVideoDisplays"].toList();
        DEBUG_PRINT(DEBUG_TRACE,"onServiceEvent receieved for DS \n");

        if( connectedVideoDisplays.isEmpty())
        {
                DEBUG_PRINT(DEBUG_TRACE,"Received event CONNECTED_DISPLAYS_UPDATED with disconnected \n");
                app->exit();
        }
        else if(connectedVideoDisplays[0].toString() == "HDMI0")
        {
                DEBUG_PRINT(DEBUG_TRACE,"Received event CONNECTED_DISPLAYS_UPDATED with connected %s",connectedVideoDisplays[0].toString().toUtf8().constData());
                app->exit();
        }
        else
                app->exit(FAIL);
}
#endif

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
void VideoApplicationSignalListener::onServiceEvent(const QString& event, ServiceParams params)
{
	if (event == VideoApplicationEventsService::EVT_ON_START)
	{
        	DEBUG_PRINT(DEBUG_TRACE,"EVT_ON_START event receieved");
    	}
    	if (event == VideoApplicationEventsService::EVT_ON_COMPLETTE)
    	{
        	DEBUG_PRINT(DEBUG_TRACE,"EVT_ON_COMPLETTE event receieved");
    	}
    	if (event == VideoApplicationEventsService::EVT_ON_WATCHED)
    	{
        	DEBUG_PRINT(DEBUG_TRACE,"EVT_ON_WATCHED event receieved");
    	}
	app->exit();
}

bool startVideoApplicationEventsService(void)
{
        bool bReturn = false;
        printf("Create new instance of VideoApplicationEventsService\n");
        if (ServiceManager::getInstance()->doesServiceExist(VideoApplicationEventsService::SERVICE_NAME))
        {
                pVideoApplicationEventsService = dynamic_cast<VideoApplicationEventsService*>(ServiceManager::getInstance()->createService(VideoApplicationEventsService::SERVICE_NAME));
                if (pVideoApplicationEventsService != NULL)
                {
                        printf("pVideoApplicationEventsService = %p\n", pVideoApplicationEventsService);
                        bReturn = true;
                }
                else
                {
                        printf("Failed to create instance of VideoApplicationEventsService\n");
                }
        }
        else
        {
                printf("Video application Service does not exist");
        }

        return bReturn;
}

void stopVideoApplicationEventsService(void)
{
        printf("Delete instance of VideoApplicationEventsService\n");
        if (pVideoApplicationEventsService != NULL)
        {
                printf("Delete %p\n", pVideoApplicationEventsService);
                delete pVideoApplicationEventsService;
                pVideoApplicationEventsService = NULL;
                printf("\nDeleted service successfully\n");
        }
        else
        {
                printf("ETV Service does not exist");
        }
}
#endif


bool sm_create(QString serviceName)
{
	ServiceStruct serviceStruct;
	bool registerStatus = false;

	DEBUG_PRINT(DEBUG_TRACE,"Creating service instance of %s", serviceName.toUtf8().constData());
#ifdef HAS_API_AVINPUT
	if (serviceName == AVInputService::SERVICE_NAME)
	{
		serviceStruct.createFunction = &createAVInputService;
		serviceStruct.serviceName = AVInputService::SERVICE_NAME;
	}
	else
#endif
#ifdef USE_DISPLAY_SETTINGS
        if (serviceName == DISPLAY_SETTINGS_SERVICE_NAME)
        {
                serviceStruct.createFunction = &createDisplaySettingsService;
                serviceStruct.serviceName = serviceName;
        }
        else
#endif
#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        if (serviceName == VideoApplicationEventsService::SERVICE_NAME)
        {
                serviceStruct.createFunction = &createVideoApplicationEventsService;
		serviceStruct.serviceName = serviceName;
        }
	else
#endif
		return registerStatus;
        registerStatus = ServiceManager::getInstance()->registerService(serviceName, serviceStruct);

#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        if (serviceName == VideoApplicationEventsService::SERVICE_NAME)
        {
		registerStatus = startVideoApplicationEventsService(); 
		return registerStatus;
        }
#endif
	return registerStatus;
}

bool sm_event_register(QString serviceName, QString eventName)
{
        bool registerStatus = false;
        Service* ptr_service=NULL;

        QList<QString> event_list;
        ServiceListener *listener=NULL;

	DEBUG_PRINT(DEBUG_TRACE,"Registering event %s for the service %s \n", eventName.toUtf8().constData(), serviceName.toUtf8().constData());
#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        if(serviceName == VideoApplicationEventsService::SERVICE_NAME)
        {
		ptr_service = pVideoApplicationEventsService;
                plistener = new VideoApplicationSignalListener();
		listener = plistener;
                if(!listener)
                        return registerStatus;
        }
	else
#endif
		ptr_service = ServiceManager::getInstance()->getGlobalService(serviceName);

#ifdef HAS_API_AVINPUT
	if(eventName == AVInputService::EVENT_NAME_ON_AVINPUT_ACTIVE)
	{
	        event_list.append(AVInputService::EVENT_NAME_ON_AVINPUT_ACTIVE);
		listener = new AVIListener();
	}
	else if(eventName == AVInputService::EVENT_NAME_ON_AVINPUT_INACTIVE)
        {
                event_list.append(AVInputService::EVENT_NAME_ON_AVINPUT_INACTIVE);
                listener = new AVIListener();
        }
	else
#endif
#ifdef USE_DISPLAY_SETTINGS
        if(eventName == EVT_DISPLAY_SETTINGS_CONNECTED_DISPLAYS_UPDATED)
        {
                //event_list.append(EVT_DISPLAY_SETTINGS_CONNECTED_DISPLAYS_UPDATED);
                event_list.append("connectedVideoDisplaysUpdated");
                listener = new DisListener();
                if(!listener)
                        return registerStatus;
        }
	else
#endif
#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        if(eventName == VideoApplicationEventsService::EVT_ON_START)
        {
                event_list.append(VideoApplicationEventsService::EVT_ON_START);
        }
	else if(eventName == VideoApplicationEventsService::EVT_ON_COMPLETTE)
        {
                event_list.append(VideoApplicationEventsService::EVT_ON_COMPLETTE);
        }
	else if(eventName == VideoApplicationEventsService::EVT_ON_WATCHED)
        {
                event_list.append(VideoApplicationEventsService::EVT_ON_WATCHED);
        }
	else
#endif
		return registerStatus;
	if(listener)
		registerStatus = ptr_service->registerForEvents(event_list,listener);
	return registerStatus;
}

void iarm_register()
{
	IARM_Bus_Init("IARM_BUS_TDK_QAPP");
	IARM_Bus_Connect();
	IARM_Bus_RegisterEventHandler(IARM_BUS_DSMGR_NAME,IARM_BUS_DSMGR_EVENT_HDMI_IN_HOTPLUG, dsHdmiEventHandler);
	IARM_Bus_RegisterEventHandler(IARM_BUS_DSMGR_NAME,IARM_BUS_DSMGR_EVENT_HDMI_HOTPLUG, dsHdmiEventHandler);

	DEBUG_PRINT(DEBUG_TRACE, "IARM event registered \n");
}

void dsHdmiEventHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	switch (eventId) 
	{
        	case IARM_BUS_DSMGR_EVENT_HDMI_IN_HOTPLUG : 
		{
                	IARM_Bus_DSMgr_EventData_t *eventData = (IARM_Bus_DSMgr_EventData_t *)data;
	                int hdmiin_hotplug_port = eventData->data.hdmi_in_connect.port;
	                int hdmiin_hotplug_conn = eventData->data.hdmi_in_connect.isPortConnected;
            		printf("Received IARM_BUS_DSMGR_EVENT_HDMI_IN_HOTPLUG  event data:%d, %d \r\n", hdmiin_hotplug_port);
	                ServiceManagerNotifier::getInstance()->notifyHdmiInputHotPlugEvent(hdmiin_hotplug_port, hdmiin_hotplug_conn);
	        	break;
        	}
                case IARM_BUS_DSMGR_EVENT_HDMI_HOTPLUG :
                {
                        IARM_Bus_DSMgr_EventData_t *eventData = (IARM_Bus_DSMgr_EventData_t *)data;
                        int hdmi_hotplug_event = eventData->data.hdmi_hpd.event;
                        printf("Received IARM_BUS_DSMGR_EVENT_HDMI_HOTPLUG  event data:%d \r\n", hdmi_hotplug_event);
                        ServiceManagerNotifier::getInstance()->notifyHdmiHotPlugEvent(hdmi_hotplug_event);
                        break;
                }
		default:
			break;
	}
}

void trigger_event(unsigned char app_signal)
{
	QByteArray application_id(6, 0);
	unsigned int locator_id = 0;
	application_id[0] = 0x00;
        application_id[1] = 0x00;
        application_id[2] = 0x14;
        application_id[3] = 0xd5;
        application_id[4] = 0x00;
        application_id[5] = 0x00;
        sleep(10);
        pVideoApplicationEventsService->setEnabled(true);
        if( true == pVideoApplicationEventsService->isEnabled())
        {
                printf("Enabled event\n");
        }
        QVariantList AppArray;
        QVariantList getAppArray;
        QHash<QString,QVariant> AppDetails;
        AppDetails["applicationName"] = "advertisement";
        AppDetails["maxRandomDelay"] = 15;
        AppDetails["filters"] = NULL;
        AppArray << AppDetails;
        pVideoApplicationEventsService->setApplications(AppArray);

	ServiceManagerNotifier::getInstance()->notifyEISSAppSignal(application_id, app_signal, locator_id);	
}

IARM_Result_t iarm_broadcast(QString eventName, QString eventParam)
{
        IARM_Bus_DSMgr_EventData_t _eventData;
//	bool retStatus = true;
	IARM_Result_t retStatus = IARM_RESULT_INVALID_STATE;

#ifdef HAS_API_AVINPUT
	if(eventName == AVInputService::EVENT_NAME_ON_AVINPUT_ACTIVE)
	{
	        _eventData.data.hdmi_in_connect.port = (dsHdmiInPort_t)PORT;
        	_eventData.data.hdmi_in_connect.isPortConnected = eventParam.toInt();

	        retStatus = IARM_Bus_BroadcastEvent(IARM_BUS_DSMGR_NAME,
                                (IARM_EventId_t)IARM_BUS_DSMGR_EVENT_HDMI_IN_HOTPLUG,
                                (void *)&_eventData,
                                sizeof(_eventData));
	}
        else if(eventName == AVInputService::EVENT_NAME_ON_AVINPUT_INACTIVE)
        {
                _eventData.data.hdmi_in_connect.port = (dsHdmiInPort_t)PORT;
                _eventData.data.hdmi_in_connect.isPortConnected = eventParam.toInt();

                retStatus = IARM_Bus_BroadcastEvent(IARM_BUS_DSMGR_NAME,
                                (IARM_EventId_t)IARM_BUS_DSMGR_EVENT_HDMI_IN_HOTPLUG,
                                (void *)&_eventData,
                                sizeof(_eventData));
        }
#endif
#ifdef USE_DISPLAY_SETTINGS
        if(eventName == EVT_DISPLAY_SETTINGS_CONNECTED_DISPLAYS_UPDATED)
        {
                _eventData.data.hdmi_hpd.event = (dsDisplayEvent_t)eventParam.toInt();
                retStatus = IARM_Bus_BroadcastEvent(IARM_BUS_DSMGR_NAME,
                                (IARM_EventId_t)IARM_BUS_DSMGR_EVENT_HDMI_HOTPLUG,
                                (void *)&_eventData,
                                sizeof(_eventData));
        }
#endif

	return retStatus;
}


int main(int argc, char* argv[])
{
	bool registerStatus = false;
	QString eventName, serviceName, eventParam;	

	app = new QApplication(argc, argv);

	if (argc > 2)
	{
		DEBUG_PRINT(DEBUG_TRACE,"Arguments received as: %s %s %s \n",argv[1], argv[2], argv[3]);
		serviceName = QString::fromUtf8(argv[1]);
		eventName = QString::fromUtf8(argv[2]);
		eventParam = QString::fromUtf8(argv[3]);
	}
	else
	{
		DEBUG_PRINT(DEBUG_TRACE,"not enough arguments \n");
		return FAIL;
	}
	//registerStatus = sm_create(serviceName);
	//Commenting the registration part as not required  (RDKTT-661)
        registerStatus = true;
#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
        if (serviceName == VideoApplicationEventsService::SERVICE_NAME)
        {
                registerStatus = startVideoApplicationEventsService();
        }
#endif
	if(registerStatus)
	{
		DEBUG_PRINT(DEBUG_TRACE,"SM create success\n");
		registerStatus = sm_event_register(serviceName, eventName);
		if(registerStatus)
			iarm_register();
		else
		{
			DEBUG_PRINT(DEBUG_TRACE,"Event registration failed \n");
			return FAIL;
		}
	}
	else
	{
		DEBUG_PRINT(DEBUG_TRACE,"SM creation failed\n");
		return FAIL;
	}
	sleep(5);
#ifdef HAS_API_VIDEO_APPLICATION_EVENTS
	if (eventName ==  VideoApplicationEventsService::EVT_ON_START)
		trigger_event(EISS_STATUS_ON_START);
	else if (eventName == VideoApplicationEventsService::EVT_ON_COMPLETTE)
		trigger_event(EISS_STATUS_ON_COMPLETE);
	else if (eventName == VideoApplicationEventsService::EVT_ON_WATCHED)
		trigger_event(EISS_STATUS_ON_WATCHED);
	else	
#endif
	if( iarm_broadcast(eventName, eventParam) )
		return FAIL;

	DEBUG_PRINT(DEBUG_TRACE,"Starting main loop\n");
	int ret = app->exec();
	DEBUG_PRINT(DEBUG_TRACE,"Main loop exited with ret %d \n", ret);
	if( !ret )
		return 0;
	else
		return FAIL;
}
