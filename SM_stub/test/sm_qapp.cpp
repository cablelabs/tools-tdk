/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include "sm_qapp.h"

using namespace std;
bool bBenchmarkEnabled;
QApplication *app;
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
		return registerStatus;
        registerStatus = ServiceManager::getInstance()->registerService(serviceName, serviceStruct);

	return registerStatus;
}

bool sm_event_register(QString serviceName, QString eventName)
{
        bool registerStatus = false;
        Service* ptr_service=NULL;

	ptr_service = ServiceManager::getInstance()->getGlobalService(serviceName);
        QList<QString> event_list;
        ServiceListener *listener=NULL;

	DEBUG_PRINT(DEBUG_TRACE,"Registering event %s for the service %s \n", eventName.toUtf8().constData(), serviceName.toUtf8().constData());

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
	registerStatus = sm_create(serviceName);

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
