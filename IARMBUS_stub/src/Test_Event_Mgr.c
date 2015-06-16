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
#include <unistd.h>
#include "iarmUtil.h"
#include "libIARM.h"
#include "libIBus.h"
#include "dummytestmgr.h"

static pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static bool stopped = false;

/**
 * These functions are invoked from other applications(test agent)
 */
static IARM_Result_t _dummyAPI0(void *arg)
{
    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
        printf("Inside fun1");
    IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI0_Param_t *)arg;
    printf("i=%d",param->i);
    param->iret=(param->i)+0x10000000;
        printf("Exit fun1");
    return retCode;

}

static IARM_Result_t _dummyAPI1(void *arg)
{
    IARM_Result_t retCode = IARM_RESULT_SUCCESS;
    printf("Inside fun2");
    IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *param = (IARM_Bus_DUMMYMGR_DummyAPI1_Param_t *)arg;
    param->jret=(param->j)+0x10000000;
    printf("j=%d",param->j);
    printf("Exit fun2");
    return retCode;
}


static IARM_Result_t _handlerReady(void *arg)
{
    IARM_Bus_DUMMYMGR_HandlerReady_Param_t *param = (IARM_Bus_DUMMYMGR_HandlerReady_Param_t *)arg;
    stopped = param->stopped;
    /* Unlocking on receiving handler */
    pthread_mutex_lock(&lock);
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
    return IARM_RESULT_SUCCESS;
}

int main(int argc, char **argv)
{
	printf("\nStarting Dummy Manager\n");

	IARM_Bus_DUMMYMGR_EventData_t eventData;
	IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
	IARM_Bus_Connect();
	IARM_Bus_RegisterEvent(IARM_BUS_DUMMYMGR_EVENT_MAX);
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI0,  	_dummyAPI0);
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI1,  	_dummyAPI1);
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_HANDLER_READY,	_handlerReady);

	/* Lock to get app synced */
	pthread_mutex_lock(&lock);
	pthread_cond_wait(&cond,&lock);
	pthread_mutex_unlock(&lock);

	/* Populate Event Data Here */
	eventData.data.dummy0.dummyData = 1;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYX, &eventData, sizeof(eventData));
	eventData.data.dummy1.dummyData = 2;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYY, &eventData, sizeof(eventData));
	eventData.data.dummy2.dummyData = 3;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYZ, &eventData, sizeof(eventData));

	/* Lock to get app synced */
	pthread_mutex_lock(&lock);
	pthread_cond_wait(&cond,&lock);
	pthread_mutex_unlock(&lock);

	IARM_Bus_Disconnect();
	IARM_Bus_Term();

	printf("\nExiting Dummy Manager\n");
}
