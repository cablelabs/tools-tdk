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

#include <stdio.h>
#include "iarmUtil.h"
#include "libIARM.h"
#include "libIBus.h"
#include "dummytestmgr.h"
#include "string.h"
#include <time.h>
#include <sys/time.h>
#include <pthread.h>

static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static bool stopped = false;

#define DEBUG_PRINT(pui8Debugmsg...)\
      do{\
                char buffer[30];\
                struct timeval tv;\
                time_t curtime;\
                gettimeofday(&tv, NULL); \
                curtime=tv.tv_sec;\
                strftime(buffer,30,"%m-%d-%Y %T.",localtime(&curtime));\
                fprintf(stdout,"\n%s%ld [%s %s():%d] ", buffer, tv.tv_usec, IARM_BUS_DUMMYMGR_NAME, __FUNCTION__, __LINE__);\
                fprintf(stdout,pui8Debugmsg);\
                fflush(stdout);\
      }while(0)

/**
 * These functions are invoked from other applications(test agent)
 */
static IARM_Result_t _dummyAPI0(void *arg)
{
    DEBUG_PRINT("Enter dummyAPI0");
    IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *)arg;
    param->iRet0=(param->iData0)+0x10000000;
    DEBUG_PRINT("Input iData0=%d Output iRet0=%x",param->iData0,param->iRet0);
    DEBUG_PRINT("Exit dummyAPI0");
    return IARM_RESULT_SUCCESS;

}

static IARM_Result_t _dummyAPI1(void *arg)
{
    DEBUG_PRINT("Enter dummyAPI1");
    IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *)arg;
    param->iRet1=(param->iData1)+0x10000000;
    DEBUG_PRINT("Input iData1=%d Output iRet1=%x",param->iData1,param->iRet1);
    DEBUG_PRINT("Exit dummyAPI1");
    return IARM_RESULT_SUCCESS;
}


static IARM_Result_t _handlerReady(void *arg)
{
    DEBUG_PRINT("Enter handlerReady");
    IARM_Bus_DUMMYMGR_HandlerReady_Param_t *param = (IARM_Bus_DUMMYMGR_HandlerReady_Param_t *)arg;
    stopped = param->stopped;
    DEBUG_PRINT("stopped = %d", stopped);
    /* Unlocking on receiving handler */
    pthread_mutex_lock(&lock);
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
    DEBUG_PRINT("Exit handlerReady");
    return IARM_RESULT_SUCCESS;
}

int main(int argc, char **argv)
{
        DEBUG_PRINT("Starting Dummy Manager\n");

	IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
	IARM_Bus_Connect();

	/* Register the RPC Calls */
        DEBUG_PRINT("Registering Event IARM_BUS_DUMMYMGR_EVENT_MAX\n");
	IARM_Bus_RegisterEvent(IARM_BUS_DUMMYMGR_EVENT_MAX);
        DEBUG_PRINT("Registering RPC Call dummyAPI0\n");
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI0,  	_dummyAPI0);
	DEBUG_PRINT("Registering RPC Call dummyAPI1\n");
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI1,  	_dummyAPI1);
	DEBUG_PRINT("Registering RPC Call handlerReady\n");
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_HANDLER_READY,	_handlerReady);

        DEBUG_PRINT("Lock to get app synced\n");
	/* Lock to get app synced */
	pthread_mutex_lock(&lock);
	pthread_cond_wait(&cond,&lock);
	pthread_mutex_unlock(&lock);

	/* Populate Event Data Here */
        IARM_Bus_DUMMYMGR_EventData_t eventXData , eventYData , eventZData;

        memset(eventXData.data.dummy0.dummyData,'\0',DATA_LEN);
        memset(eventXData.data.dummy0.dummyData,'x',DATA_LEN-1);
        strncpy(eventXData.data.dummy0.dummyData,argv[1],strlen(argv[1]));
	DEBUG_PRINT("Dummy Event X: %s (size:%d)\n", eventXData.data.dummy0.dummyData, sizeof(eventXData.data.dummy0.dummyData));

        memset(eventYData.data.dummy0.dummyData,'\0',DATA_LEN);
        memset(eventYData.data.dummy0.dummyData,'y',DATA_LEN-1);
        strncpy(eventYData.data.dummy0.dummyData,argv[1],strlen(argv[1]));
	DEBUG_PRINT("Dummy Event Y: %s (size:%d)\n", eventYData.data.dummy0.dummyData, sizeof(eventYData.data.dummy0.dummyData));

        memset(eventZData.data.dummy0.dummyData,'\0',DATA_LEN);
        memset(eventZData.data.dummy0.dummyData,'z',DATA_LEN-1);
	strncpy(eventZData.data.dummy0.dummyData,argv[1],strlen(argv[1]));
	DEBUG_PRINT("Dummy Event Z: %s (size:%d)\n", eventZData.data.dummy0.dummyData, sizeof(eventZData.data.dummy0.dummyData));

        DEBUG_PRINT("Broadcasting Dummy Event X from Dummy Manager\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYX, &eventXData, sizeof(eventXData));

        DEBUG_PRINT("Broadcasting Dummy Event Y from Dummy Manager\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYY, &eventYData, sizeof(eventYData));

        DEBUG_PRINT("Broadcasting Dummy Event Z from Dummy Manager\n");
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYZ, &eventZData, sizeof(eventZData));

	DEBUG_PRINT("Lock to get app synced\n");
	/* Lock to get app synced */
	pthread_mutex_lock(&lock);
	pthread_cond_wait(&cond,&lock);
	pthread_mutex_unlock(&lock);

	IARM_Bus_Disconnect();
	IARM_Bus_Term();

	DEBUG_PRINT("Exiting Dummy Manager\n");
}
