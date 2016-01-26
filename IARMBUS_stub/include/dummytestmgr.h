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
#include <stdbool.h>
#include <pthread.h>
#include <string.h>
#include <time.h>

#define IARM_BUS_DUMMYMGR_NAME			  "Test_Event_Mgr"

#define IARM_BUS_DUMMYMGR_API_HANDLER_READY "HandlerReady"

#define DUMMYDATA_X "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#define DUMMYDATA_Y "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

#define DUMMYDATA_Z "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
typedef struct {
    bool stopped;
}IARM_Bus_DUMMYMGR_HandlerReady_Param_t;

/*
 * Declare Published Events
 */
typedef enum _DUMMYMGR_EventId_t {
    IARM_BUS_DUMMYMGR_EVENT_DUMMYX,
    IARM_BUS_DUMMYMGR_EVENT_DUMMYY,
    IARM_BUS_DUMMYMGR_EVENT_DUMMYZ,
    IARM_BUS_DUMMYMGR_EVENT_MAX,
} IARM_Bus_DUMMYMGR_EventId_t;

/*
 * Declare Event Data
 */
typedef struct _DUMMYMGR_EventData_t {
    union {
        struct _EventData_DUMMY_0{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY0 */
                char dummyData[128];
                struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy0;
#if 0

#endif
    } data;
} IARM_Bus_DUMMYMGR_EventData_t;
/*
 * Declare RPC API names and their arguments
 */
#define IARM_BUS_DUMMYMGR_API_DummyAPI0           "DummyAPI0"
typedef struct _IARM_Bus_DUMMYMGR_DummyAPI0_Param_t {
int i;
int iret;
} IARM_Bus_DUMMYMGR_DummyAPI0_Param_t;

#define IARM_BUS_DUMMYMGR_API_DummyAPI1           "DummyAPI1"
typedef struct _IARM_Bus_DUMMYMGR_DummyAPI1_Param_t {
int j;
int jret;
} IARM_Bus_DUMMYMGR_DummyAPI1_Param_t;


