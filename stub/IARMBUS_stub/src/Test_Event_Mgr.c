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
#include <unistd.h>
#include "iarmUtil.h"
#include "libIARM.h"
#include "libIBus.h"
#include "dummytestmgr.h"

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

int main()
{

	printf("\ninside main\n");
	int sleepus = 200 * 1000; 
	IARM_Result_t retCode = IARM_RESULT_SUCCESS;
	IARM_Bus_DUMMYMGR_EventData_t eventData;
	IARM_Bus_Init(IARM_BUS_DUMMYMGR_NAME);
	IARM_Bus_Connect();
	IARM_Bus_RegisterEvent(IARM_BUS_DUMMYMGR_EVENT_MAX);
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI0,  	_dummyAPI0);
	IARM_Bus_RegisterCall(IARM_BUS_DUMMYMGR_API_DummyAPI1,  	_dummyAPI1);
	int i = 0,j=0;
	usleep(4*sleepus);

	/* Populate Event Data Here */
	eventData.data.dummy0.dummyData = 1;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYX, &eventData, sizeof(eventData));
	eventData.data.dummy1.dummyData = 2;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYY, &eventData, sizeof(eventData));
	eventData.data.dummy2.dummyData = 3;
	IARM_Bus_BroadcastEvent(IARM_BUS_DUMMYMGR_NAME,IARM_BUS_DUMMYMGR_EVENT_DUMMYZ, &eventData, sizeof(eventData));

	IARM_Bus_Disconnect();
	IARM_Bus_Term();
	printf("\nExit main\n");
}
