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
#include "rdktestagentintf.h"
#include "IARMBUSAgent.h"
#include "gen_irevent.h"

/********************************************************
* Function Name	: _ReleaseOwnership
* Description  	: This the call back function used to rgister with 
*		  registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
	DEBUG_PRINT(DEBUG_TRACE,"############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n");

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
	if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) {
		switch (eventId) {
		case IARM_BUS_IRMGR_EVENT_IRKEY:
		{
			IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
			int keyCode = irEventData->data.irkey.keyCode;
			int keyType = irEventData->data.irkey.keyType;
			DEBUG_PRINT(DEBUG_TRACE," EventHdlr Test Bus Client Get IR Key (%d, %d) From IR Manager\r\n", keyCode, keyType);
		}
			break;
		default:
			break;
		}

	}
}
void print_usage() {
	DEBUG_PRINT(DEBUG_TRACE,"Usage: -o owner -i eventId -t type -c keycode\n");
}

int main(int argc,char **argv)
{
	int i = 0;
	int type = 0;
	int code = 0;
	char *owner;
	int eventId = 0;
        for (i = 1; i < argc; i++)  /* Skip argv[0] (program name). */
        {
            /*
             * Use the 'strcmp' function to compare the argv values
             * to a string of your choice (here, it's the optional
             * argument "-q").  When strcmp returns 0, it means that the
             * two strings are identical.
             */

            if (strcmp(argv[i], "-o") == 0)  /* Process optional arguments. */
            { 
                i++;
                owner = argv[i];

                DEBUG_PRINT(DEBUG_TRACE,"Owner is %s\n",owner);
            }

            if (strcmp(argv[i], "-i") == 0)
            {
                i++;
                eventId = atoi(argv[i]);
                DEBUG_PRINT(DEBUG_TRACE,"EventId is %d\n",eventId);
            }
            if (strcmp(argv[i], "-t") == 0)  /* Process optional arguments. */
            { 
                i++;
                type = atoi(argv[i]);

                DEBUG_PRINT(DEBUG_TRACE,"Type is %d\n",type);
            }

            if (strcmp(argv[i], "-c") == 0)
            {
                i++;
                code = atoi(argv[i]);
                DEBUG_PRINT(DEBUG_TRACE,"Code is %d\n",code);
            }
        }

	/* Check parameters */
	if (type == 0 || code == 0)
	{
		/* not valid */
		DEBUG_PRINT(DEBUG_ERROR,"FAILURE: Type and Code must be non-zero\n");
		return -1;
	}

	DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Entry-------------->%d %d\n",type,code);

	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE,"Client Entering %d\r\n", getpid());
	IARM_Bus_Init("Bus Client");
	IARM_Bus_Connect();
	IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
	DEBUG_PRINT(DEBUG_TRACE,"\nRequesting Resource\n");
	retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

	/*Event Data for BUS,IR,PWR events*/
	IRMgr_EventData_tp eventData_ir;

	/*Braodcasting IR IRKey event*/
    	eventData_ir.data.irkey.keyType = type;
    	eventData_ir.data.irkey.keyCode = code;

	if( clock_gettime( CLOCK_REALTIME, &eventData_ir.data.irkey.clock_when_event_sent) == -1) 
	{
		perror("clock gettime main");
	}

        DEBUG_PRINT(DEBUG_TRACE,"2nd APP sending %d %lx %lx \n",code,eventData_ir.data.irkey.clock_when_event_sent.tv_sec,eventData_ir.data.irkey.clock_when_event_sent.tv_nsec);        
	DEBUG_PRINT(DEBUG_TRACE,"\nBroadcasting IR event %d %d\n",type,code);
	IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));
	
	DEBUG_PRINT(DEBUG_TRACE,"\nApplication sleep for 5 seconds\n");
	sleep(5);
	DEBUG_PRINT(DEBUG_TRACE,"\nReleasing Resource\n");
	retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);
	IARM_Bus_Disconnect();
	IARM_Bus_Term();
	DEBUG_PRINT(DEBUG_TRACE,"Bus Client Exiting\r\n");
    	DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Exit-------------->\n");
	return(retCode);
}
