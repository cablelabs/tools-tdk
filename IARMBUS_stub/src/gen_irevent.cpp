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
#include "libIBus.h"
#include "libIBusDaemon.h"
#include "irMgr.h"
#include "rdktestagentintf.h"
#include "gen_irevent.h"

/********************************************************
* Function Name	: _ReleaseOwnership
* Description  	: This the call back function used to rgister with
*		  registercall method
*
********************************************************/

static IARM_Result_t _ReleaseOwnership(void *arg)
{
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] ############### Bus Client _ReleaseOwnership, CLIENT releasing stuff\r\n",getpid());

    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    return retCode;
}

int main(int argc,char **argv)
{
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] <-----------SECOND APPLICATION---Entry-------------->\n",getpid());

    int i = 0;
    int type = 0;
    int code = 0;
    char *owner;
    int eventId = 0;

    if(argc < 3)
    {
        DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Usage: -o owner -i eventId -t type -c keycode\n", getpid());
        DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] <-----------SECOND APPLICATION---Exit-------------->\n", getpid());
        exit(0);
    }

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
            if (argv[i] != NULL)
            {
                owner = argv[i];
                DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Owner is %s\n",getpid(),owner);
            }
        }
        else if (strcmp(argv[i], "-i") == 0)
        {
            i++;
            if (argv[i] != NULL)
            {
                eventId = atoi(argv[i]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] EventId is %d\n",getpid(),eventId);
            }
        }
        else if (strcmp(argv[i], "-t") == 0)  /* Process optional arguments. */
        {
            i++;
            if (argv[i] != NULL)
            {
                type = atoi(argv[i]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Type is %d\n",getpid(),type);
            }
        }
        else if (strcmp(argv[i], "-c") == 0)
        {
            i++;
            if (argv[i] != NULL)
            {
                code = atoi(argv[i]);
                DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Code is %d\n",getpid(),code);
            }
        }
    }

    /* Check parameters */
    if (type == 0 || code == 0)
    {
        /* not valid */
        DEBUG_PRINT(DEBUG_ERROR,"[gen_irevent pid=%d] FAILURE: Type and Code must be non-zero\n",getpid());
        DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] <-----------SECOND APPLICATION---Exit-------------->\n",getpid());
        return -1;
    }

    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Client Entering\n", getpid());
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Connect second application\n", getpid());
    IARM_Bus_Init("Bus_Client");
    IARM_Bus_Connect();
    IARM_Bus_RegisterCall(IARM_BUS_COMMON_API_ReleaseOwnership, _ReleaseOwnership);
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Requesting Resource\n",getpid());
    retCode=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

    /*Event Data for BUS,IR,PWR events*/
    IRMgr_EventData_tp eventData_ir;

    /*Braodcasting IR IRKey event*/
    eventData_ir.data.irkey.keyType = type;
    eventData_ir.data.irkey.keyCode = code;

    if( clock_gettime( CLOCK_REALTIME, &eventData_ir.data.irkey.clock_when_event_sent) == -1)
    {
        DEBUG_PRINT(DEBUG_ERROR, "[gen_irevent pid=%d] clock gettime error",getpid());
    }

    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Sending %d %lx %lx \n",getpid(),code,eventData_ir.data.irkey.clock_when_event_sent.tv_sec,eventData_ir.data.irkey.clock_when_event_sent.tv_nsec);
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Broadcasting IR event %d %d\n",getpid(),type,code);
    IARM_Bus_BroadcastEvent(IARM_BUS_IRMGR_NAME, IARM_BUS_IRMGR_EVENT_IRKEY, (void*)&eventData_ir, sizeof(eventData_ir));

    sleep(1);
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Releasing Resource\n",getpid());
    retCode = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Disconnect second application",getpid());
    IARM_Bus_Disconnect();
    IARM_Bus_Term();
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] Bus Client Exiting\r\n",getpid());
    DEBUG_PRINT(DEBUG_TRACE,"[gen_irevent pid=%d] <-----------SECOND APPLICATION---Exit-------------->\n",getpid());
    return(retCode);
}
