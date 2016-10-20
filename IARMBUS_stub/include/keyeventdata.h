/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
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
