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

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "libIBus.h"
#include "libIBusDaemon.h"
#include "pwrMgr.h"
#include "irMgr.h"
#include "diskMgr.h"
#include "sysMgr.h"

/********************************************************
* Function Name	: _ReleaseOwnership
* Description  	: This the call back function used to rgister with 
*		  registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
	printf("############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n");

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
			printf("Event IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",
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
			printf("Test Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
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
                	printf("\nResourceAvailable event received\n");
		}
                        break;
		case IARM_BUS_EVENT_RESOLUTIONCHANGE:
		{
			printf("\nResolution Change event received\n");
		}
                default:
                        break;
                }

        }

}

int main(int argc, char *argv[] )
{

        printf("\n<-----------SECOND APPLICATION---Entry-------------->\n");
	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	printf("Client Entering %d\r\n", getpid());
	IARM_Bus_Init("Bus_Client");
	IARM_Bus_Connect();
	IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
	printf("\nRequesting Resource\n");
	retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);
	/*Event Data for BUS,IR,PWR events*/
	IARM_Bus_EventData_t eventData_bus;
	IARM_Bus_IRMgr_EventData_t eventData_ir;
	IARM_Bus_PWRMgr_EventData_t eventData_pwr;
	IARM_BUS_DISKMgr_EventData_t eventData_disk;
	IARM_Bus_SYSMgr_EventData_t eventData_sys;
        /*Hard coded values*/
	printf("\nBroadcasting ResourceAvailable event\n");
	/*Braodcasting Bus event-ResourceAvailable*/
        eventData_bus.resrcType = (IARM_Bus_ResrcType_t)0;
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOURCEAVAILABLE, (void*) &eventData_bus, sizeof(eventData_bus));
	/*Braodcasting Bus event-ResolutionChange*/
	printf("\nBroadcasting ResolutionChange event\n");
        IARM_Bus_ResolutionChange_EventData_t eventData_bus1;
        eventData_bus1.width=1;
	eventData_bus1.height=2;	
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME,IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &eventData_bus1, sizeof(eventData_bus1));
	
	/*Braodcasting IR IRKey event*/
        eventData_ir.data.irkey.keyType = 0x80;
        eventData_ir.data.irkey.keyCode = 0x8100;
	printf("\nBroadcasting IR event\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));
	
	/*Braodcasting PWR event*/
	eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)0;
	printf("\nBroadcasting PWR event\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME,IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));

	/*Braodcasting DISKMGR event*/
	printf("\n Broadcasting DISk Mgr HWDISK Event \n");
	IARM_Bus_BroadcastEvent(IARM_BUS_DISKMGR_NAME,IARM_BUS_DISKMGR_EVENT_HWDISK,(void*)&eventData_disk,sizeof(eventData_disk));

	if(strcmp(argv[1],"ON")==0)
		eventData_disk.eventType = DISKMGR_EVENT_EXTHDD_ON;
	else if(strcmp(argv[1],"OFF")==0)
		eventData_disk.eventType =DISKMGR_EVENT_EXTHDD_OFF;
	else if(strcmp(argv[1],"PAIR")==0)
		eventData_disk.eventType =DISKMGR_EVENT_EXTHDD_PAIR;
	printf("\n Broadcasting DISk Mgr HDDDISK Event \n");
	IARM_Bus_BroadcastEvent(IARM_BUS_DISKMGR_NAME,IARM_BUS_DISKMGR_EVENT_EXTHDD,(void*)&eventData_disk,sizeof(eventData_disk));

	/*Braodcasting SYSMGR event*/
	printf("\n Broadcasting SYS Mgr Event \n");
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST,(void*)&eventData_sys,sizeof(eventData_sys));
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD,(void*)&eventData_sys,sizeof(eventData_sys));
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE,(void*)&eventData_sys,sizeof(eventData_sys));

	printf("\nApplication sleep for 5 seconds\n");
	sleep(5);
	printf("\nReleasing Resource\n");
	retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);
	IARM_Bus_Disconnect();
	IARM_Bus_Term();
	printf("Bus Client Exiting\r\n");
        printf("\n<-----------SECOND APPLICATION---Exit-------------->\n");
}
