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

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "libIBus.h"
#include "libIBusDaemon.h"
#include "pwrMgr.h"
#include "irMgr.h"
#include "rdktestagentintf.h"

/********************************************************
* Function Name	: _ReleaseOwnership
* Description  	: This the call back function used to rgister with 
*		  registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
	DEBUG_PRINT(DEBUG_LOG,"############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n");

    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    return retCode;
}

/********************************************************
* Function Name	: _eventHandler_
* Description  	: This the call back function used to handle different tyes of 
*		  with events.\
*
********************************************************/
static void _eventHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) {
		switch (eventId) {
		case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
		{
			IARM_Bus_PWRMgr_EventData_t *param = (IARM_Bus_PWRMgr_EventData_t *)data;
			DEBUG_PRINT(DEBUG_LOG,"Event IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",
					param->data.state.curState, param->data.state.newState);
		}
			break;
		default:
			break;
		}
	}
	else if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) {
		switch (eventId) {
		case IARM_BUS_IRMGR_EVENT_IRKEY:
		{
			IARM_Bus_IRMgr_EventData_t *irEventData = (IARM_Bus_IRMgr_EventData_t*)data;
			int keyCode = irEventData->data.irkey.keyCode;
			int keyType = irEventData->data.irkey.keyType;
			DEBUG_PRINT(DEBUG_LOG,"Test Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
		}
			break;
		default:
			break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
	switch (eventId) {
                case IARM_BUS_EVENT_RESOURCEAVAILABLE:
                {
                	DEBUG_PRINT(DEBUG_LOG,"\nResourceAvailable event received\n");
		}
                        break;
		case IARM_BUS_EVENT_RESOLUTIONCHANGE:
		{
			DEBUG_PRINT(DEBUG_LOG,"\nResolution Change event received\n");
		}
                default:
                        break;
                }

        }

}

int main()
{


        DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Entry-------------->\n");
	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_LOG,"Client Entering %d\r\n", getpid());
	IARM_Bus_Init("Bus_Client");
	IARM_Bus_Connect();
	IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
	DEBUG_PRINT(DEBUG_LOG,"\nRequesting Resource\n");
	retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);
	/*Event Data for BUS,IR,PWR events*/
	IARM_Bus_EventData_t eventData_bus;
	IARM_Bus_IRMgr_EventData_t eventData_ir;
	IARM_Bus_PWRMgr_EventData_t eventData_pwr;
        /*Hard coded values*/
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting ResourceAvailable event\n");
	/*Braodcasting Bus event-ResourceAvailable*/
        eventData_bus.resrcType = (IARM_Bus_ResrcType_t)0;
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOURCEAVAILABLE, (void*) &eventData_bus, sizeof(eventData_bus));
	/*Braodcasting Bus event-ResolutionChange*/
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting ResolutionChange event\n");
        IARM_Bus_ResolutionChange_EventData_t eventData_bus1;
        eventData_bus1.width=1;
	eventData_bus1.height=2;	
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME,IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &eventData_bus1, sizeof(eventData_bus1));
	
	/*Braodcasting IR IRKey event*/
        eventData_ir.data.irkey.keyType = 0x80;
        eventData_ir.data.irkey.keyCode = 0x8100;
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting IR event\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));
	
	/*Braodcasting PWR event*/
	eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)0;
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting PWR event\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME,IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));

	DEBUG_PRINT(DEBUG_LOG,"\nApplication sleep for 5 seconds\n");
	sleep(5);
	DEBUG_PRINT(DEBUG_LOG,"\nReleasing Resource\n");
	retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);
	IARM_Bus_Disconnect();
	IARM_Bus_Term();
	DEBUG_PRINT(DEBUG_LOG,"Bus Client Exiting\r\n");
        DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Exit-------------->\n");
}
