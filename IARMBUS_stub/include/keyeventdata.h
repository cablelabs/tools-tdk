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

#ifndef __KEYEVENT_H__
#define __KEYEVENT_H__
#include <time.h>

#ifdef __cplusplus
extern "C"
{
#endif

#define BILLION 1000000000L
#if 0
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
#endif
/*! Key Event Data */
typedef struct _IRMgr_EventData_tp 
{
	union 
	{
		struct _IRKEY_DATA{
		   /* Declare Event Data structure for IRMGR_EVENT_DUMMY0 */
			int keyType;              /*!< Key type (UP/DOWN/REPEAT) */
			int keyCode;              /*!< Key code */
			struct timespec clock_when_event_sent;   /*!< clock val at send */
        } irkey, fpkey;
	} data;
}IRMgr_EventData_tp; 

typedef struct _IARM_Bus_EventData_tp 
{
	int resrcType;              /*!< resrcType type */
	int width;              /*!< width */
	int height;              /*!height */
	struct timespec clock_when_event_sent;   /*!< clock val at send */
}IARM_Bus_EventData_tp,IARM_Bus_ResolutionChange_EventData_tp; 

typedef struct _IARM_Bus_PWRMgr_EventData_tp 
{
	union 
	{
		struct _PWRMGR_DATA{
			int curState;
			int newState;
			struct timespec clock_when_event_sent;   /*!< clock val at send */
		} state;
	} data;
}IARM_Bus_PWRMgr_EventData_tp; 

typedef struct _DUMMYMGR_EventData_tp {
    union {
        struct _EventData_DUMMY_0{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY0 */
                int dummyData;
		struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy0;
        struct _EventData_DUMMY_1{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY1 */
                int dummyData;
		struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy1;
        struct _EventData_DUMMY_2{
                /* Declare Event Data structure for DUMMYMGR_EVENT_DUMMY2 */
                int dummyData;
		struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy2;
    } data;
} IARM_Bus_DUMMYMGR_EventData_tp;
#ifdef __cplusplus
}
#endif
#endif //__KEYEVENT_H__
