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

#include "iarmUtil.h"
#include "libIARM.h"
#include "libIBus.h"
#include <stdbool.h>
#include <time.h>

#define IARM_BUS_DUMMYMGR_NAME		     "Test_Event_Mgr"
#define IARM_BUS_DUMMYMGR_API_HANDLER_READY  "HandlerReady"
#define IARM_BUS_DUMMYMGR_API_DummyAPI0      "DummyAPI0"
#define IARM_BUS_DUMMYMGR_API_DummyAPI1      "DummyAPI1"
#define DATA_LEN                             128

char dummydata_x[DATA_LEN];
char dummydata_y[DATA_LEN];
char dummydata_z[DATA_LEN];

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
                char dummyData[DATA_LEN];
                struct timespec clock_when_event_sent;   /*!< clock val at send */
        } dummy0;
    } data;
} IARM_Bus_DUMMYMGR_EventData_t;

/*
 * Declare RPC API names and their arguments
 */
typedef struct _IARM_Bus_DUMMYMGR_HandlerReady_Param_t {
    	bool stopped;
}IARM_Bus_DUMMYMGR_HandlerReady_Param_t;

typedef struct _IARM_Bus_DUMMYMGR_DummyAPI0_Param_t {
	int iData0;
	int iRet0;
} IARM_Bus_DUMMYMGR_DummyAPI0_Param_t;

typedef struct _IARM_Bus_DUMMYMGR_DummyAPI1_Param_t {
	int iData1;
	int iRet1;
} IARM_Bus_DUMMYMGR_DummyAPI1_Param_t;
