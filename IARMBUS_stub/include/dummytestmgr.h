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


#define IARM_BUS_DUMMYMGR_NAME			  "DummyTestMgr"

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
                int dummyData;
        } dummy0;
        struct _EventData_DUMMY_1{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY1 */
                int dummyData;
        } dummy1;
        struct _EventData_DUMMY_2{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY2 */
                int dummyData;
        } dummy2;
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


