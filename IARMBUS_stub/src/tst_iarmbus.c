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
#include <time.h>
#include <sys/time.h>

#define DEBUG_PRINT(pui8Debugmsg...)\
      do{\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y %T.",localtime(&curtime));\
                fprintf(stdout,"\n%s%ld [%s %s():%d pid=%d] ", buffer, tv.tv_usec, "tst_iarmbus", __FUNCTION__, __LINE__, getpid());\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
      }while(0)


/********************************************************
* Function Name	: _ReleaseOwnership
* Description  	: This the call back function used to rgister with 
*		  registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
    DEBUG_PRINT("############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n");
    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    return retCode;
}

int main(int argc, char *argv[] )
{
        DEBUG_PRINT("\n<-----------SECOND APPLICATION---Entry-------------->\n");

	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	DEBUG_PRINT("Client Entering %d\r\n", getpid());

	IARM_Bus_Init("Bus_Client");
	IARM_Bus_Connect();

	IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
	DEBUG_PRINT("Requesting Resource\n");
	retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

	/*Broadcasting Bus event-ResourceAvailable*/
	DEBUG_PRINT("Broadcasting Daemon ResourceAvailable Event (id: %d)\n", IARM_BUS_EVENT_RESOURCEAVAILABLE);
	IARM_Bus_EventData_t raEventData;
        raEventData.resrcType = (IARM_Bus_ResrcType_t)0;
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOURCEAVAILABLE, (void*) &raEventData, sizeof(raEventData));

	/*Broadcasting Bus event-ResolutionChange*/
	DEBUG_PRINT("Broadcasting Daemon ResolutionChange Event (id: %d)\n", IARM_BUS_EVENT_RESOLUTIONCHANGE);
        IARM_Bus_ResolutionChange_EventData_t rcEventData;
        rcEventData.width=1;
	rcEventData.height=2;	
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME, IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &rcEventData, sizeof(rcEventData));
	
	/*Broadcasting IR IRKey event*/
        IARM_Bus_IRMgr_EventData_t eventData_ir0;
        eventData_ir0.data.irkey.keyType = 0x00008000;
        eventData_ir0.data.irkey.keyCode = 0x00000033;
	DEBUG_PRINT("Broadcasting Digit3 Key Press IR Event (id: %d)\n", IARM_BUS_IRMGR_EVENT_IRKEY);
	IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir0, sizeof(eventData_ir0));

        IARM_Bus_IRMgr_EventData_t eventData_ir1;
        eventData_ir1.data.irkey.keyType = 0x00008100;
        eventData_ir1.data.irkey.keyCode = 0x00000033;
        DEBUG_PRINT("Broadcasting Digit3 Key Release IR Event (id: %d)\n", IARM_BUS_IRMGR_EVENT_IRKEY);
        IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir1, sizeof(eventData_ir1));
	
	/*Broadcasting PWR event*/
	IARM_Bus_PWRMgr_EventData_t eventData_pwr;
	eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t)IARM_BUS_PWRMGR_POWERSTATE_ON;
	DEBUG_PRINT("Broadcasting PWRMgr Mode Changed Event (id: %d)\n", IARM_BUS_PWRMGR_EVENT_MODECHANGED);
	IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME, IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));

	/*Broadcasting DISKMGR event*/
	IARM_BUS_DISKMgr_EventData_t eventData_disk;
	char *eventType = NULL; 
	DEBUG_PRINT("Broadcasting DISKMgr HWDISK Event (id: %d)\n", IARM_BUS_DISKMGR_EVENT_HWDISK);
	IARM_Bus_BroadcastEvent(IARM_BUS_DISKMGR_NAME, IARM_BUS_DISKMGR_EVENT_HWDISK,(void*)&eventData_disk,sizeof(eventData_disk));

	if (argc < 2)
	{
		eventType = (char *)"ON";
	}
	else
	{
		eventType = argv[1];
	}

	if(strcmp(eventType,"ON")==0)
		eventData_disk.eventType = DISKMGR_EVENT_EXTHDD_ON;
	else if(strcmp(eventType,"OFF")==0)
		eventData_disk.eventType =DISKMGR_EVENT_EXTHDD_OFF;
	else if(strcmp(eventType,"PAIR")==0)
		eventData_disk.eventType =DISKMGR_EVENT_EXTHDD_PAIR;
	DEBUG_PRINT("Broadcasting DISKMgr %s EXTHDD Event (id: %d)\n", eventType, IARM_BUS_DISKMGR_EVENT_EXTHDD);
	IARM_Bus_BroadcastEvent(IARM_BUS_DISKMGR_NAME, IARM_BUS_DISKMGR_EVENT_EXTHDD,(void*)&eventData_disk,sizeof(eventData_disk));

	/*Broadcasting SYSMGR event*/
	IARM_Bus_SYSMgr_EventData_t eventData_sys;
	eventData_sys.data.xupnpData.deviceInfoLength = 0;
	DEBUG_PRINT("Broadcasting SYSMgr Xupnp Data Request Event (id: %d)\n", IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST);
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_REQUEST,(void*)&eventData_sys,sizeof(eventData_sys));
	DEBUG_PRINT("Broadcasting SYSMgr Xupnp Data Update Event (id: %d)\n", IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE);
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_XUPNP_DATA_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
	DEBUG_PRINT("Broadcasting SYSMgr CARD FW download Event (id: %d)\n", IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD);
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_CARD_FWDNLD,(void*)&eventData_sys,sizeof(eventData_sys));
	DEBUG_PRINT("Broadcasting SYSMgr HDCP Profile Update Event (id: %d)\n", IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE);
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_HDCP_PROFILE_UPDATE,(void*)&eventData_sys,sizeof(eventData_sys));
	DEBUG_PRINT("Broadcasting SYSMgr System State Event (id: %d)\n", IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE);
	IARM_Bus_BroadcastEvent(IARM_BUS_SYSMGR_NAME,IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE,(void*)&eventData_sys,sizeof(eventData_sys));

	sleep(1);

	DEBUG_PRINT("Releasing Resource\n");
	retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);

	IARM_Bus_Disconnect();
	IARM_Bus_Term();

	DEBUG_PRINT("Bus Client Exiting\r\n");
        DEBUG_PRINT("\n<-----------SECOND APPLICATION---Exit-------------->\n");
}
