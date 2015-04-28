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

void print_usage() {
	DEBUG_PRINT(DEBUG_TRACE,"Usage: -o ownername -e eventID -t type -c keycode -n newstate -r resrctype\n");
}

int main(int argc,char **argv)
{
	int option = 0, i;
	int type = 0x0000, code = 0x000;
	int eventId=0;
	char *ownerName = NULL;
	int newState = 0,resrcType = 0;

	if(argc < 2)
		print_usage();

        for (i = 1; i < argc; i++)  /* Skip argv[0] (program name). */
        {
		DEBUG_PRINT(DEBUG_LOG,"\nIteration loop : %d, Value : %s\n", i, argv[i]);
            /*
             * Use the 'strcmp' function to compare the argv values
             * to a string of your choice (here, it's the optional
             * argument "-q").  When strcmp returns 0, it means that the
             * two strings are identical.
             */

            if (strcmp(argv[i], "-o") == 0)  /* Process optional arguments. */
            { 
                ownerName = argv[i+1];
                DEBUG_PRINT(DEBUG_TRACE,"ownerName is %s\n",ownerName);
            }

            if (strcmp(argv[i], "-e") == 0)
            {
		if (argv[i+1] != NULL)
		{
	                eventId = atoi(argv[i+1]);
        	        DEBUG_PRINT(DEBUG_TRACE,"eventId is %d\n",eventId);
		}
            }
            if (strcmp(argv[i], "-t") == 0)  /* Process optional arguments. */
            { 
		if (argv[i+1] != NULL)
		{
		        type = atoi(argv[i+1]);
		        DEBUG_PRINT(DEBUG_TRACE,"Type is %d\n",type);
		}
            }

            if (strcmp(argv[i], "-c") == 0)
            {
		if (argv[i+1] != NULL)
		{
		        code = atoi(argv[i+1]);
		        DEBUG_PRINT(DEBUG_TRACE,"Code is %d\n",code);
		}
            }
            if (strcmp(argv[i], "-n") == 0)  /* Process optional arguments. */
            { 
		if (argv[i+1] != NULL)
		{
	                newState = atoi(argv[i+1]);
	                DEBUG_PRINT(DEBUG_TRACE,"newState is %d\n",newState);
		}
            }

            if (strcmp(argv[i], "-r") == 0)
            {
		if (argv[i+1] != NULL)
		{
		        resrcType = atoi(argv[i+1]);
		        DEBUG_PRINT(DEBUG_TRACE,"resrcType is %d\n",resrcType);
		}
            }
        }

	DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Entry-------------->%d %d\n",type,code);

	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	DEBUG_PRINT(DEBUG_TRACE,"Client Entering %d\r\n", getpid());
	IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
	IARM_Bus_Connect();
	/*
	IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
	DEBUG_PRINT(DEBUG_TRACE,"\nRequesting Resource\n");
	retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);
	IARM_Bus_RegisterEvent(IARM_BUS_DUMMYMGR_EVENT_MAX);*/


	_IARM_Bus_PWRMgr_EventData_tp eventData_pwr;
	/*Braodcasting PWR event*/
	eventData_pwr.data.state.newState = (IARM_Bus_PWRMgr_PowerState_t) newState;
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting PWR event\n");
	if( clock_gettime( CLOCK_MONOTONIC, &eventData_pwr.data.state.clock_when_event_sent) == -1) 
	{
		perror("clock gettime main");
	}

	IARM_Bus_BroadcastEvent(IARM_BUS_PWRMGR_NAME,IARM_BUS_PWRMGR_EVENT_MODECHANGED,(void*)&eventData_pwr, sizeof(eventData_pwr));

	/*Event Data for BUS,IR,PWR events*/
	IRMgr_EventData_tp eventData_ir;

	/*Braodcasting IR IRKey event*/
    	eventData_ir.data.irkey.keyType = type;
    	eventData_ir.data.irkey.keyCode = code;
	DEBUG_PRINT(DEBUG_TRACE,"\nBroadcasting IR event %d %d\n",type,code);
	if( clock_gettime( CLOCK_MONOTONIC, &eventData_ir.data.irkey.clock_when_event_sent) == -1) 
	{
		perror("clock gettime main");
	}

	IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));


	/*Braodcasting Bus event-ResolutionChange*/
	DEBUG_PRINT(DEBUG_LOG,"\nBroadcasting ResolutionChange event\n");
	IARM_Bus_ResolutionChange_EventData_tp eventData_bus1;
	eventData_bus1.width=1;
	eventData_bus1.height=2;	
	if( clock_gettime( CLOCK_MONOTONIC, &eventData_bus1.clock_when_event_sent) == -1) 
	{
		perror("clock gettime main");
	}
	IARM_Bus_BroadcastEvent(IARM_BUS_DAEMON_NAME,IARM_BUS_EVENT_RESOLUTIONCHANGE, (void*) &eventData_bus1, sizeof(eventData_bus1));
	
	DEBUG_PRINT(DEBUG_TRACE,"\nApplication sleep for 5 seconds\n");
	sleep(5);
	/*
	DEBUG_PRINT(DEBUG_TRACE,"\nReleasing Resource\n");
	retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);*/
	IARM_Bus_Disconnect();
	IARM_Bus_Term();
	DEBUG_PRINT(DEBUG_TRACE,"Bus Client Exiting\r\n");
    	DEBUG_PRINT(DEBUG_TRACE,"\n<-----------SECOND APPLICATION---Exit-------------->\n");
}

