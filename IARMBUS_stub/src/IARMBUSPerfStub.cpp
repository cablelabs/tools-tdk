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

#include "IARMBUSAgent.h"


int LastKeyType_Perf;
int LastKeyCode_Perf;
double LastKeyTime;
static char LastEvent[40];
static char gLastEvent[40];
static char gEventSummary[1024];
int gEventSummaryCount = 0;
int ExpectedKeyCode = 0;
int ExpectedKeyType = 0;
int gRegisteredEventCount = 0;

/*These global variables are to check the test app with event handler and BusCall APIS*/
// std::string g_tdkPath = getenv("TDKOUTPUT_PATH");

#if 0
/**************************************************************************
 *
 * Function Name        : prereqcheck
 * Descrption   : This function will get the existense of pre- requisite app
 *                 nd return SUCESS or FAILURE status to the
 *                caller.
 *
 * @param retval [in] ownerName - owner(manager) to be checked.
 *		 [out]- bool - SUCCESS / FAILURE
 ***************************************************************************/

bool prereqcheck(char *ownerName )
{
	std::string pre_req_chk;
	std::string pre_req_chk_file;
	pre_req_chk_file= g_tdkPath + "/" + PRE_REQ_CHECK;
	pre_req_chk ="ps -ef | grep Main >" + pre_req_chk_file;
	int offset;
	std::string line;
	std::ifstream IrMyfile;
	char *appName = (char*)malloc(sizeof(char*)*20);
	memset(appName , '\0', (sizeof(char)*20));
	if ((strcmp(ownerName, "Daemon")  == 0)||(strcmp(ownerName,IARM_BUS_DUMMYMGR_NAME) ==0))
        {
		strcpy(appName,DAEMON_EXE);	
	}
	else if (strcmp(ownerName, "IRMgr")  == 0)
        {
		strcpy(appName,IRMGR_EXE);
	}
	else if (strcmp(ownerName, "PWRMgr")  == 0)
        {
		strcpy(appName,PWRMGR_EXE);
	}
	else if (strcmp(ownerName, "MFRLib")  == 0)
        {
		strcpy(appName,MFRMGR_EXE);
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"Invalid Owner Name\n");
		return TEST_FAILURE;
	}
	
	 //* To handle exception for system call
	try
	{
		system((char *)pre_req_chk.c_str());
	}
	catch(...)
	{
		DEBUG_PRINT(DEBUG_ERROR,"Exception occured during pidstat\n");
		DEBUG_PRINT(DEBUG_LOG, " ---> Exit\n");
		return TEST_FAILURE;
	}
	IrMyfile.open (pre_req_chk_file.c_str());

	if(IrMyfile.is_open())
	{
		while(!IrMyfile.eof())
		{
			getline(IrMyfile,line);
			if ((offset = line.find(appName, 0)) != std::string::npos) {
				IrMyfile.close();
				DEBUG_PRINT(DEBUG_LOG,"\nPre-Requisites present\n");
				return TEST_SUCCESS;
			}
		}
		DEBUG_PRINT(DEBUG_ERROR,"\nPre-Requisites not present\n");
		return TEST_FAILURE;
	}
	else
	{
		DEBUG_PRINT(DEBUG_ERROR,"\nUnable to open this file.\n");
		return TEST_FAILURE;
	}
}
#endif

/**************************************************************************
 *
 * Function Name	: getResult_Perf
 * Descrption	: This function will get the retvalue as input and it returns 
 *		  corresponding SUCCESS or FAILUER status to the 
 *		  wrapper function.
 *
 * @param retval [in] - return value of BUS APIs
 ***************************************************************************/

char* getResult_Perf(int retval,char *resultDetails)
{
	if(retval==0)
	{
		strcpy(resultDetails,"NULL");
		return (char*)"SUCCESS";
	}
	else
	{       

		switch(retval)
		{
			case 1: strcpy(resultDetails,"INVALID_PARAM");
				break;
			case 2: strcpy(resultDetails,"INVALID_STATE");
				break;
			case 3: strcpy(resultDetails,"IPCORE_FAIL");
				break;
			case 4: strcpy(resultDetails,"OUT_OF_MEMORY");
				break;
			default :
				strcpy(resultDetails,"Unidentified Error");
				break; 
		}
		return (char*)"FAILURE";
	}

}
/**************************************************************************
 * Function Name	: fill_LastReceivedKey_Perf
 * Description	: fill_LastReceivedKey_Perf function is to fill the last recived IR 
 *		  key details in the global variable.
 *
 * @param[in]- keyCode,keyType IR key code and type.
 ***************************************************************************/

void fill_LastReceivedKey_Perf(const char *EvtHandlerName, char *gLastEvent ,double keyTime, int keyCode = 0 ,int keyType = 0)
{

	DEBUG_PRINT(DEBUG_LOG,"\n fill_LastReceivedKey_Perf --->Entry \n");
	LastKeyCode_Perf=keyCode;
	LastKeyType_Perf=keyType;
	LastKeyTime=keyTime;
	gLastEvent = LastEvent;
	DEBUG_PRINT(DEBUG_LOG, "LastEvent: %s LastKeyCode: 0x%x LastKeyType : 0x%x LastKeyTime: %lf seconds\r\n",gLastEvent, keyCode, keyType, keyTime);

	if(gRegisteredEventCount > 1) {
		DEBUG_PRINT(DEBUG_LOG, " \n Registered for more than one event : %d \n ", gRegisteredEventCount);
		char TempEventSummary[200] ;

		if(strcmp(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY") == 0)
			sprintf(TempEventSummary, "%s, %s, %x, %x, %lf::", EvtHandlerName, LastEvent, LastKeyType_Perf, LastKeyCode_Perf, LastKeyTime);
		else
			sprintf(TempEventSummary, "%s, %s, %lf::", EvtHandlerName, LastEvent, LastKeyTime);

		strcat( gEventSummary, TempEventSummary);
		gEventSummaryCount++;
		DEBUG_PRINT(DEBUG_LOG, "gEventSummary: %s\n\n", gEventSummary);
	}else {
		DEBUG_PRINT(DEBUG_LOG, " \n Registered for only one event : %d \n ", gRegisteredEventCount);
	}

	DEBUG_PRINT(DEBUG_LOG,"\n fill_LastReceivedKey_Perf --->Exit \n");
}

/***************************************************************************
 * Function Name : _PWRMGRevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of PWR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _PWRMGRevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	struct timespec clock_at_recv_PWRMgr;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_PWRMgr) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\ncan't get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n got Event received time\n");
	}

	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_tp *param = (IARM_Bus_PWRMgr_EventData_tp *)data;
					DEBUG_PRINT(DEBUG_LOG,"\nEvent IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					double keyTime = 0.0;

					keyTime = ((double)(clock_at_recv_PWRMgr.tv_sec - param->data.state.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_PWRMgr.tv_nsec - param->data.state.clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of PWRMgr was %lf seconds\r\n", keyTime);

					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
					fill_LastReceivedKey_Perf(__func__, LastEvent, keyTime);
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}
	}
	
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}
/***************************************************************************

 * Function Name : _IRevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of IR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */


void _IRevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\ncan't get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n got current time\n");
	}

	if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					
					double keyTime = 0.0;

					/*Convert Received and Expected data to Hexa format for comparision*/
					char TempRecvKeyCode[10], TempRecvKeyType[10], TempExpectedKeyCode[10],TempExpectedKeyType[10];
					sprintf(TempRecvKeyCode, "%x",irEventData->data.irkey.keyCode);
					sprintf(TempRecvKeyType, "%x",irEventData->data.irkey.keyType);
					sprintf(TempExpectedKeyCode, "%x", ExpectedKeyCode);
					sprintf(TempExpectedKeyType, "%x", ExpectedKeyType);
					DEBUG_PRINT(DEBUG_LOG,"\nReceived : %s, %s \n\n", TempRecvKeyCode, TempRecvKeyType);
					DEBUG_PRINT(DEBUG_LOG,"\nExpected Data: %s, %s \n\n", TempExpectedKeyCode, TempExpectedKeyType);
					
					/* Verify the reeived event */
					if ( (strcmp(TempRecvKeyCode, TempExpectedKeyCode) == 0) && (strcmp(TempRecvKeyType,TempExpectedKeyType) == 0))
					{

						keyTime = ((double)(clock_at_recv_event.tv_sec - irEventData->data.irkey.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - irEventData->data.irkey.clock_when_event_sent.tv_nsec)) / (double)BILLION;
						DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of IR key 0x%x type 0x%x was %lf seconds\r\n",keyCode, keyType, keyTime);

						DEBUG_PRINT(DEBUG_LOG,"\nTest Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
						strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
						fill_LastReceivedKey_Perf(__func__, LastEvent,keyTime,keyCode,keyType);
					} else {
						DEBUG_PRINT(DEBUG_LOG,"\nRecevived Unexpected IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					}
					
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}

	}
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}

/***************************************************************************
 * Function Name : _IBUSevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of IARMBUS events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _IBUSevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	struct timespec clock_at_recv_RC;
	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_RC) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\ncan't get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n got Event received time\n");
	}
	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	double keyTime = 0;
	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					DEBUG_PRINT(DEBUG_LOG,"\nResolution Change event received\n");
					IARM_Bus_ResolutionChange_EventData_tp *eventData_bus1 = (IARM_Bus_ResolutionChange_EventData_tp*)data ;
					
					DEBUG_PRINT(DEBUG_LOG,"\nReceived Width & Height : %d, %d \n\n", eventData_bus1->width, eventData_bus1->height);

					keyTime = ((double)(clock_at_recv_RC.tv_sec - eventData_bus1->clock_when_event_sent.tv_sec) + (double)(clock_at_recv_RC.tv_nsec - eventData_bus1->clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for Receviving ResourceAvailable event : %lf seconds\r\n", keyTime);
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
					fill_LastReceivedKey_Perf(__func__, LastEvent, keyTime);
				}
				break;
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"\nResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
					fill_LastReceivedKey_Perf(__func__,LastEvent, keyTime);
				}
			default:
				break;
		}

	}
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}

/***************************************************************************
 * Function Name : _DUMMYTestMgrevtHandler
 * Description 	: This function is the event handler call back function for handling the 
 different type of DUMMY events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _DUMMYTestMgrevtHandler(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	struct timespec clock_at_recv_event;
	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		perror("can't get current time");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n got Event received time\n");
	}
	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	double EvtTime = 0.0;
	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\nInside DummyMgr event handler\n");
		/* Handle events here */
		IARM_Bus_DUMMYMGR_EventData_tp *eventData = (IARM_Bus_DUMMYMGR_EventData_tp *)data;
		
		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:
			DEBUG_PRINT(DEBUG_LOG,"\nReceived i:%d",eventData->data.dummy0.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - X : IARM_BUS_DUMMYMGR_EVENT_DUMMYX \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy0.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy0.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYX");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYX %d was %lf seconds\r\n",eventData->data.dummy0.dummyData, EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:
			DEBUG_PRINT(DEBUG_LOG,"\nReceived j:%d",eventData->data.dummy1.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - Y : IARM_BUS_DUMMYMGR_EVENT_DUMMYY \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy1.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy1.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYY");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYY %d was %lf seconds\r\n",eventData->data.dummy1.dummyData, EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:
			DEBUG_PRINT(DEBUG_LOG,"\nReceived k:%d",eventData->data.dummy2.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - Z : IARM_BUS_DUMMYMGR_EVENT_DUMMYZ \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy2.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy2.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYZ");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYZ %d was %lf seconds\r\n",eventData->data.dummy2.dummyData, EvtTime);
			break;
		}
	}

	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}

/***************************************************************************
 * Function Name : _evtHandler_Perf
 * Description 	: This function is the event handler call back function for handling the 
 different type of events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

/*Hard-coded event handler*/

void _evtHandler_Perf(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{
	struct timespec clock_at_recv_event;

	if(clock_gettime( CLOCK_MONOTONIC, &clock_at_recv_event) == -1)
	{
		DEBUG_PRINT(DEBUG_ERROR,"\ncan't get current time\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n got Event received time\n");
	}

	DEBUG_PRINT(DEBUG_LOG, "Entering _evtHandler_Perf\n");
	double EvtTime = 0.0;

	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler_Perf --> \n owner : %s, eventId : %d ", owner, eventId);

	if (strcmp(owner, IARM_BUS_PWRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_PWRMGR_EVENT_MODECHANGED:
				{
					IARM_Bus_PWRMgr_EventData_tp *param = (IARM_Bus_PWRMgr_EventData_tp *)data;
					DEBUG_PRINT(DEBUG_LOG,"\nEvent IARM_BUS_PWRMGR_EVENT_MODECHANGED: State Changed %d -- > %d\r\n",param->data.state.curState, param->data.state.newState);
					double keyTime = 0.0;
					keyTime = ((double)(clock_at_recv_event.tv_sec - param->data.state.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - param->data.state.clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of PWRMgr was %lf seconds\r\n", keyTime);

					strcpy(LastEvent , "IARM_BUS_PWRMGR_EVENT_MODECHANGED");
					fill_LastReceivedKey_Perf(__func__,LastEvent, keyTime);
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}
	}
	else if (strcmp(owner, IARM_BUS_IRMGR_NAME)  == 0) 
	{
		switch (eventId) 
		{
			case IARM_BUS_IRMGR_EVENT_IRKEY:
				{
					IRMgr_EventData_tp *irEventData = (IRMgr_EventData_tp*)data;
					int keyCode = irEventData->data.irkey.keyCode;
					int keyType = irEventData->data.irkey.keyType;
					double keyTime = 0.0;

					printf("irEventData : %p", data);

					if ( ExpectedKeyCode == irEventData->data.irkey.keyCode && ExpectedKeyType == irEventData->data.irkey.keyType)
					{

						keyTime = ((double)(clock_at_recv_event.tv_sec - irEventData->data.irkey.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - irEventData->data.irkey.clock_when_event_sent.tv_nsec)) / (double)BILLION;
						DEBUG_PRINT(DEBUG_LOG, "Time taken for sending of IR key 0x%x type 0x%x was %lf seconds\r\n",keyCode, keyType, keyTime);
						DEBUG_PRINT(DEBUG_LOG,"\nTest Bus Client Get IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
						strcpy(LastEvent , "IARM_BUS_IRMGR_EVENT_IRKEY");
						fill_LastReceivedKey_Perf(__func__,LastEvent,keyTime,keyCode,keyType);
					} else {
						DEBUG_PRINT(DEBUG_LOG,"\nRecevived Unexpected IR Key (%x, %x) From IR Manager\r\n", keyCode, keyType);
					}
					
				}
				break;
			default:
				{
					DEBUG_PRINT(DEBUG_ERROR,"\nUnindentified event\n");
				}
				break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DAEMON_NAME) == 0) {
		switch (eventId) {
			case IARM_BUS_EVENT_RESOURCEAVAILABLE:
				{
					DEBUG_PRINT(DEBUG_LOG,"\nResourceAvailable event received\n");
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOURCEAVAILABLE");
				}
				break;
			case IARM_BUS_EVENT_RESOLUTIONCHANGE:
				{
					double keyTime = 0.0;
					DEBUG_PRINT(DEBUG_LOG,"\nResolution Change event received\n");
					IARM_Bus_ResolutionChange_EventData_tp *eventData_bus1 = (IARM_Bus_ResolutionChange_EventData_tp*)data ;
					DEBUG_PRINT(DEBUG_LOG,"\nReceived Width & Height : %d, %d \n\n", eventData_bus1->width, eventData_bus1->height);
					keyTime = ((double)(clock_at_recv_event.tv_sec - eventData_bus1->clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData_bus1->clock_when_event_sent.tv_nsec)) / (double)BILLION;
					DEBUG_PRINT(DEBUG_LOG, "Time taken for Receviving ResourceAvailable event : %lf seconds\r\n", keyTime);
					strcpy(LastEvent , "IARM_BUS_EVENT_RESOLUTIONCHANGE");
					fill_LastReceivedKey_Perf(__func__,LastEvent, keyTime);
				}
			default:
				break;
		}

	}
	else if (strcmp(owner, IARM_BUS_DUMMYMGR_NAME) == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\nInside DummyMgr event handler\n");

		/* Handle events here */
		IARM_Bus_DUMMYMGR_EventData_tp *eventData = (IARM_Bus_DUMMYMGR_EventData_tp *)data;
		switch(eventId) {
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYX:

			DEBUG_PRINT(DEBUG_LOG,"\nReceived i:%d",eventData->data.dummy0.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - X : IARM_BUS_DUMMYMGR_EVENT_DUMMYX \r\n");
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy0.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy0.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYX");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYX %d was %lf seconds\r\n",eventData->data.dummy0.dummyData, EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYY:

			DEBUG_PRINT(DEBUG_LOG,"\nReceived j:%d",eventData->data.dummy1.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - Y : IARM_BUS_DUMMYMGR_EVENT_DUMMYY \r\n");
					
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy1.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy1.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYY");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYY %d was %lf seconds\r\n",eventData->data.dummy1.dummyData, EvtTime);
			break;
		case IARM_BUS_DUMMYMGR_EVENT_DUMMYZ:

			DEBUG_PRINT(DEBUG_LOG,"\nReceived k:%d",eventData->data.dummy2.dummyData);
			DEBUG_PRINT(DEBUG_LOG,"\nReceived Event - Z : IARM_BUS_DUMMYMGR_EVENT_DUMMYZ \r\n");
						
			EvtTime = ((double)(clock_at_recv_event.tv_sec - eventData->data.dummy2.clock_when_event_sent.tv_sec) + (double)(clock_at_recv_event.tv_nsec - eventData->data.dummy2.clock_when_event_sent.tv_nsec)) / (double)BILLION;
			strcpy(LastEvent , "IARM_BUS_DUMMYMGR_EVENT_DUMMYZ");
			fill_LastReceivedKey_Perf(__func__,LastEvent, EvtTime);
			DEBUG_PRINT(DEBUG_LOG, "Time taken for receving IARM_BUS_DUMMYMGR_EVENT_DUMMYZ %d was %lf seconds\r\n",eventData->data.dummy2.dummyData, EvtTime);
			break;
		}
	}

}
#if 0
/*************************************************************************************************
 *Function name	: IARMBUSPerfAgent 
 *Descrption	: This is a constructor function for IARMBUSPerfAgent class. 
 ************************************************************************************************/ 
IARMBUSPerfAgent::IARMBUSPerfAgent()
{
	DEBUG_PRINT(DEBUG_LOG,"IARMBUSPerfAgent Initialized");
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Descrption    : testmodulepre_requisites will  be used for setting the
 *                pre-requisites that are necessary for this component
 *
 *****************************************************************************/
std::string IARMBUSPerfAgent::testmodulepre_requisites()
{
	char retval[512];
	memset(retval, '\0', sizeof(512));
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);
	if ((prereqcheck((char*)"Daemon"))== TEST_SUCCESS)
		sprintf(retval, "SUCCESS");
	else
		sprintf(retval, "FAILURE<DETAILS> Pre-requisite check failed for Daemon Mgr");
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
	return retval;
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool IARMBUSPerfAgent::testmodulepost_requisites()
{
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);
        return TEST_SUCCESS;
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
}

/***************************************************************************************************
 *Function name	: initialize
 *Descrption	: Initialize Function will be used for registering the wrapper method 
 * 	 	  with the agent so that wrapper functions will be used in the 
 *  		  script
 ***************************************************************************************************/ 

bool IARMBUSPerfAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);

	/*Register stub function for callback*/
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::BUSAgent_Init, "TestMgr_IARMBUSPERF_Init");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::BUSAgent_Term, "TestMgr_IARMBUSPERF_Term");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::BUSAgent_BusConnect, "TestMgr_IARMBUSPERF_Connect");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::BUSAgent_BusDisconnect, "TestMgr_IARMBUSPERF_Disconnect");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::RegisterEventHandler, "TestMgr_IARMBUSPERF_RegisterEventHandler");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::UnRegisterEventHandler, "TestMgr_IARMBUSPERF_UnRegisterEventHandler");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::InvokeEventTransmitterApp, "TestMgr_IARMBUSPERF_InvokeEventTransmitterApp");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::GetLastReceivedEventDetails, "TestMgr_IARMBUSPERF_GetLastReceivedEventDetails");
	ptrAgentObj->RegisterMethod(*this,&IARMBUSPerfAgent::RegisterMultipleEventHandlers, "TestMgr_IARMBUSPERF_RegisterMultipleEventHandlers");
	
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
	return true;
}

#endif

/**************************************************************************
 *
 * Function Name	: IARMBUSPerfAgent_Init
 * Descrption	: IARMBUSPerfAgent_Init wrapper function will be used to call BUS 
 API "IARM_Bus_Init".
 *
 * @param [in] req- has "Process_name" which is input to IARM_Bus_Init
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of BUS API.
 ***************************************************************************/

bool IARMBUSAgent::BUSAgent_Init(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_TRACE,"\n %s --->Entry\n", __func__);
	IARM_Result_t retval;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	if(&req["Process_name"]==NULL)
	{
		return TEST_FAILURE;
	}
	DEBUG_PRINT(DEBUG_TRACE,"\ncalling IARM_Bus_Init directly from IARMBUSPerfAgent_Init\n");
	/*Calling BUS API IARM_Bus_Init with json req as parameter*/
	retval=IARM_Bus_Init((char *)req["Process_name"].asCString());
	/*retval=IARM_Bus_Init("Bus Client");*/
	response["result"]=getResult_Perf(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n%s --->Exit\n", __func__);
	return TEST_SUCCESS;
}

/**************************************************************************
 * Function Name	: IARMBUSPerfAgent_Term
 * Descrption	: IARMBUSPerfAgent_Term wrapper function will be used to call BUS API "IARM_Bus_Term".
 *
 * @param [in] req- None
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of BUS API.
 ***************************************************************************/
bool IARMBUSAgent::BUSAgent_Term(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n %s --->Entry\n", __func__);
	IARM_Result_t retval;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_TRACE,"\ncalling IARM_Bus_Term()\n");
	/*Calling BUS API IARM_Bus_Term  */
	retval=IARM_Bus_Term();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult_Perf(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n%s --->Exit\n", __func__);
	return TEST_SUCCESS;

}

/**************************************************************************
 * Functio Name	: IARMBUSPerfAgent_BusConnect
 * Descrption	: IARMBUSPerfAgent_BusConnect wrapper function will be used to call BUS API "IARM_Bus_Connect".
 * 
 * @param [in] req- None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of BUS API.
 ***************************************************************************/	

bool IARMBUSAgent::BUSAgent_BusConnect(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n %s --->Entry\n", __func__);
	IARM_Result_t retval;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_TRACE,"\ncalling IARM_Bus_Connect\n");
	/*Calling BUS API IARM_Bus_Connect  */
	retval=IARM_Bus_Connect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult_Perf(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n%s --->Exit\n", __func__);
	return TEST_SUCCESS;

}

/**************************************************************************
 * Function Name	: IARMBUSPerfAgent_BusDisconnect
 * Descrption	: IARMBUSPerfAgent_BusDisconnect wrapper function will be used to call 
 BUS API "IARM_Bus_Disconnect".
 *
 * @param [in] req-None 
 * @param [out] response- filled with SUCCESS or FAILURE based on the return value of BUS API.
 ***************************************************************************/
bool IARMBUSAgent::BUSAgent_BusDisconnect(IN const Json::Value& req, OUT Json::Value& response)
{

	DEBUG_PRINT(DEBUG_TRACE,"\n %s --->Entry\n", __func__);
	IARM_Result_t retval;
	char *resultDetails;
	resultDetails=(char *)malloc(sizeof(char)*16);
	memset(resultDetails , '\0', (sizeof(char)*16));
	DEBUG_PRINT(DEBUG_TRACE,"\ncalling IARM_Bus_Disconnect\n");
	/*Calling BUS API IARM_Bus_Disconnect  */
	retval=IARM_Bus_Disconnect();
	/*Checking the return value of API*/
	/*Filling json response with SUCCESS status*/	
	response["result"]=getResult_Perf(retval,resultDetails);
	response["details"]=resultDetails;
	free(resultDetails);
	DEBUG_PRINT(DEBUG_TRACE,"\n%s --->Exit\n", __func__);
	return TEST_SUCCESS;

}


/***************************************************************************

 * Function Name : _evtHandlerRept1
 * Description 	: This function is the event handler call back function for handling the 
 different type of IR events.
 * @param[in]-owner - owner(manager) for that event.
 *	    - eventId - id of the event whose call back is called
 *	    - data - event data
 *	    - len - size of data.
 ***************************************************************************** */

void _evtHandlerRept1(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"DummyTestMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}
void _evtHandlerRept2(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"DummyTestMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}
void _evtHandlerRept3(const char *owner, IARM_EventId_t eventId, void *data, size_t len)
{

	DEBUG_PRINT(DEBUG_LOG, "Entering _%s\n", __func__);
	/* Get the request details*/
	char *ownerName=(char*) owner;

	DEBUG_PRINT(DEBUG_LOG,"*_evtHandler --> \n owner : %s, eventId : %d ", owner, eventId);

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for for IR Key Events ... \n");
		_IRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_PWRMGRevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_IBUSevtHandler(owner, eventId, data, len);
	}
	else if(strcmp(ownerName,"DummyTestMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registred for DUMMY TEST MANAGER Events ... \n");
		_DUMMYTestMgrevtHandler(owner, eventId, data, len);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		_evtHandler_Perf(owner, eventId, data, len);
	}

	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);

}

/*******************************************************************************************************
 *Function name	: RegisterMultipleEventHandlers
 *Descrption	: RegisterMultipleEventHandlers wrapper function will be used to Register multiple event handler for single event
 *******************************************************************************************************/ 
bool IARMBUSAgent::RegisterMultipleEventHandlers(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);

	int retval = 0;
	char details[512];
	memset(details, '\0', sizeof(512));
	//IARM_Result_t retCode = IARM_RESULT_SUCCESS;

	if( &req["event_id"]==NULL ||&req["owner_name"]==NULL)
	{
		return TEST_FAILURE;
	}

	/* Get the request details*/
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nRequesting Resource...\n");
	retval=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler from RegisterEventHandler ... \n");
	DEBUG_PRINT(DEBUG_LOG,"\n ownerName : %s,  eventId : %d \n", ownerName,(IARM_EventId_t)eventId );

	DEBUG_PRINT(DEBUG_LOG,"\n Registering for IR Key Events ... \n");
	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept1);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return "FAILURE";
	}

	gRegisteredEventCount++;

	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept2);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return "FAILURE";
	}


	gRegisteredEventCount++;

	/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
	retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandlerRept3);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return "FAILURE";
	}

	DEBUG_PRINT(DEBUG_LOG,"\nReleasing Resource...\n");
	retval = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);

	gRegisteredEventCount ++;
		
	/*Filling json response with SUCCESS status*/
	sprintf(details, "%s Successfully Executed", __func__);
	response["result"]="SUCCESS";
	response["details"]=details;
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
        return true;
}
/*******************************************************************************************************
 *Function name	: IARMBUSPerfAgent_Execute
 *Descrption	: IARMBUSPerfAgent_Execute wrapper function will be used to execute Single Event Performance Test
 *******************************************************************************************************/ 
bool IARMBUSAgent::RegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)

{
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);

	int retval = 0;
	char details[512];
	memset(details, '\0', sizeof(512));
	//IARM_Result_t retCode = IARM_RESULT_SUCCESS;

	if( &req["event_id"]==NULL ||&req["owner_name"]==NULL)
	{
		return TEST_FAILURE;
	}

	/* Get the request details*/
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();

	DEBUG_PRINT(DEBUG_LOG,"\nRequesting Resource...\n");
	retval=IARM_BusDaemon_RequestOwnership(IARM_BUS_RESOURCE_FOCUS);

	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler from RegisterEventHandler ... \n");
	DEBUG_PRINT(DEBUG_LOG,"\n ownerName : %s,  eventId : %d \n", ownerName,(IARM_EventId_t)eventId );

	/* Register Corresponding Event Hander for the Event*/
	if(strcmp(ownerName,"IRMgr")==0)
	{	
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for IR Key Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _IRevtHandler);
	}
	else if(strcmp(ownerName,"PWRMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for PWRMGR Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _PWRMGRevtHandler);
	}
	else if(strcmp(ownerName,"Daemon")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for IARMBUS DAEMON Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _IBUSevtHandler);
	}
	else if(strcmp(ownerName,"DummyTestMgr")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for DUMMY TEST MANAGER Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		DEBUG_PRINT(DEBUG_LOG,"\n ownerName : %s,  eventId : %d DUMMYTestMgrevtHandler :%p \n", ownerName,(IARM_EventId_t)eventId, &_DUMMYTestMgrevtHandler );
		retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _DUMMYTestMgrevtHandler);
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"\n Registering for All Events ... \n");
		/*Calling IARMBUS API IARM_Bus_RegisterEventHandler */
		retval=IARM_Bus_RegisterEventHandler(ownerName,(IARM_EventId_t)eventId, _evtHandler_Perf);
	}
	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_RegisterEventHandler ... -FAILURE \n");
		/*Filling json response with SUCCESS status*/
		strcpy(details, "IARM_Bus_RegisterEventHandler() FAILED");
		response["result"]="FAILURE";
		response["details"]=details;
		return "FAILURE";
	}

	DEBUG_PRINT(DEBUG_LOG,"\nReleasing Resource...\n");
	retval = IARM_BusDaemon_ReleaseOwnership(IARM_BUS_RESOURCE_FOCUS);

	//Increment the counter for collecting events
	gRegisteredEventCount++;
		
	/*Filling json response with SUCCESS status*/
	sprintf(details, "%s Successfully Executed", __func__);
	response["result"]="SUCCESS";
	response["details"]=details;
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
        return true;
}


/*******************************************************************************************************
 *Function name	: IARMBUSPerfAgent_UnReigsterIARMBUSEvent
 *Descrption	: IARMBUSPerfAgent_Execute wrapper function will be used to execute Single Event Performance Test
 *******************************************************************************************************/ 

bool IARMBUSAgent::UnRegisterEventHandler(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);

	/* Get the request details*/
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	int retval = 0;
	char details[512];
	memset(details, '\0', sizeof(512));

	DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_UnRegisterEventHandler ... \n");
	DEBUG_PRINT(DEBUG_LOG,"\n ownerName : %s,  eventId : %d \n", ownerName,(IARM_EventId_t)eventId );

	/*Calling IARMBUS API IARM_Bus_UnRegisterEventHandler */
	retval=IARM_Bus_UnRegisterEventHandler(ownerName,(IARM_EventId_t)eventId);

	if(retval == 0) {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_UnRegisterEventHandler ... - SUCCESS\n");
	} else {
		DEBUG_PRINT(DEBUG_LOG,"\n calling IARM_Bus_UnRegisterEventHandler ... -FAILURE \n");
		sprintf(details, "calling IARM_Bus_UnRegisterEventHandler ... -FAILURE");
		response["result"]="FAILURE";
		response["details"]=details;
		return TEST_FAILURE;
	}
	
	//counter decremented 
	gRegisteredEventCount--;

	/*Filling json response with SUCCESS status*/
	DEBUG_PRINT(DEBUG_LOG,"lastcode %d lasttype %d lasttime %lf lastev %s\n",LastKeyCode_Perf,LastKeyType_Perf,LastKeyTime,LastEvent);
	sprintf(details, "lastcode %d lasttype %d lasttime %lf lastev %s\n",LastKeyCode_Perf,LastKeyType_Perf,LastKeyTime,LastEvent);
	response["result"]="SUCCESS";
	response["details"]=details;
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
        return true;

}

bool IARMBUSAgent::InvokeEventTransmitterApp(IN const Json::Value& req, OUT Json::Value& response)
{
	char details[512];
	memset(details, '\0', sizeof(512));
	DEBUG_PRINT(DEBUG_LOG,"\nEntering %s function", __func__);

	if(&req["event_id"]==NULL ||&req["owner_name"]==NULL ||&req["evttxappname"]==NULL)
	{
		/*Filling json response with SUCCESS status*/
		strcpy(details, "Invalid Parameters-check owner_name, event_id, evttxappname");
		response["result"]="FAILURE";
		response["details"]=details;
		return TEST_FAILURE;
	}

	pid_t idChild = vfork();

	char * appname=(char*)req["evttxappname"].asCString();
	int eventId=req["event_id"].asInt();
	char *ownerName=(char*)req["owner_name"].asCString();
	std::string testenvPath = getenv("OPENSOURCETEST_PATH");
	testenvPath.append("../");

	std::string path;
	strcpy((char*)path.c_str(),getenv("TDK_PATH"));	
	strcat((char*)path.c_str(),"/");
	strcat((char*)path.c_str(),appname);
	DEBUG_PRINT(DEBUG_ERROR,"\nAppPath:%s, appname:%s\n",path.c_str(), appname);

	if(idChild == 0)
	{
		if(strcmp(ownerName,"IRMgr")==0)
		{	
			int keyType = (unsigned int) req["keyType"].asInt();
			int keyCode = (unsigned int)req["keyCode"].asInt();
			ExpectedKeyCode = keyCode;
			ExpectedKeyType = keyType;
         		std::string skeyCode;          // string which will contain the result
         		std::string skeyType;          // string which will contain the result
         		std::string seventId;          // string which will contain the result
 
         		std::ostringstream convert;   // stream used for the conversion
         		std::ostringstream convert2;   // stream used for the conversion
         		std::ostringstream convert3;   // stream used for the conversion
 
         		convert << keyCode;      // insert the textual representation of 'Number' in the characters in the stream
         		convert2 << keyType;      // insert the textual representation of 'Number' in the characters in the stream
         		convert3 << eventId;      // insert the textual representation of 'Number' in the characters in the stream
 
         		skeyCode = convert.str(); // set 'Result' to the contents of the stream
         		skeyType = convert2.str(); // set 'Result' to the contents of the stream
         		seventId = convert3.str(); // set 'Result' to the contents of the stream
 
			DEBUG_PRINT(DEBUG_LOG,"\n ExpectedKeyCode : %d, ExpectedKeyType: %d \n", keyCode, keyType);

 			// Parameters to execl must be strings
 			execl(path.c_str(), appname, "-o", ownerName, "-i", seventId.c_str(),"-t", skeyType.c_str(), "-c", skeyCode.c_str(), (char *)NULL);
		}
		else if(strcmp(ownerName,"PWRMgr")==0)
		{
			int newState = (unsigned int) req["newState"].asInt();
        		std::string snewState;          // string which will contain the result
         		std::ostringstream convert;   // stream used for the conversion
         		convert << newState;      // insert the textual representation of 'Number' in the characters in the stream
         		snewState = convert.str(); // set 'Result' to the contents of the stream

			DEBUG_PRINT(DEBUG_LOG,"\n newState : %d \n", newState);
			execl(path.c_str(),appname, "-n", snewState.c_str(), (char*)NULL);
		}
		else if(strcmp(ownerName,"Daemon")==0)
		{
			int resrcType = (unsigned int) req["resource_type"].asInt();
        		std::string sresrcType;          // string which will contain the result
         		std::ostringstream convert;   // stream used for the conversion
         		convert << resrcType;      // insert the textual representation of 'Number' in the characters in the stream
         		sresrcType = convert.str(); // set 'Result' to the contents of the stream

			DEBUG_PRINT(DEBUG_LOG,"\n resource_type : %d \n", resrcType);
			execl(path.c_str(),appname, "-o", ownerName, "-r", sresrcType.c_str(), (char*)NULL);
		}
		else if(strcmp(ownerName,"DummyTestMgr")==0)
		{
			DEBUG_PRINT(DEBUG_LOG,"\n DummyTestMgr Triggering events.. \n");
         		std::string seventId;          // string which will contain the result
         		std::ostringstream convert3;   // stream used for the conversion
         		convert3 << eventId;      // insert the textual representation of 'Number' in the characters in the stream
         		seventId = convert3.str(); // set 'Result' to the contents of the stream

			execl(path.c_str(), appname, "-o", ownerName, "-i", seventId.c_str(), (char*)NULL);
		}

	}
	else if(idChild <0)
	{
		DEBUG_PRINT(DEBUG_LOG,"failed fork\n");
		response["result"]="FAILURE";
		response["details"]="second application Execution failed";
		return false;
	}

	sprintf(details, "%s Successfully Executed", __func__);
	response["details"]=details;
	response["result"]="SUCCESS";
	DEBUG_PRINT(DEBUG_LOG,"\nExiting %s function", __func__);
	return true;	

}


/**************************************************************************
 * Function Name	: get_LastReceivedEventDetails
 * Description	: This function is to get the last received Event details 	
 *
 ***************************************************************************/


bool IARMBUSAgent::GetLastReceivedEventDetails(IN const Json::Value& req, OUT Json::Value& response)
{
	DEBUG_PRINT(DEBUG_LOG,"\n %s --->Entry \n", __func__);
	char details[400]="Event Details:";
	const char *KeyCodedetails=" :: KeyCode : " ;
	const char *KeyTypedetails=" :: KeyType : ";
	const char *KeyTimedetails=" :: Time : ";
	char *KeyCodedetails1 =(char*)malloc(sizeof(char)*150); 
	memset(KeyCodedetails1 , '\0', (sizeof(char)*150));
	char *KeyTypedetails1 =(char*)malloc(sizeof(char)*100);
	memset(KeyTypedetails1 , '\0', (sizeof(char)*100));
	char *KeyTimedetails1 =(char*)malloc(sizeof(char)*120);
	memset(KeyTimedetails1 , '\0', (sizeof(char)*120));

        DEBUG_PRINT(DEBUG_LOG,"**lasttime %lf lastev %s\n",LastKeyTime,LastEvent);
        
	if(strcmp(LastEvent,"IARM_BUS_IRMGR_EVENT_IRKEY")==0)
	{
		DEBUG_PRINT(DEBUG_LOG,"lastcode %d lasttype %d lasttime %lf lastev %s\n",LastKeyCode_Perf,LastKeyType_Perf,LastKeyTime,LastEvent);
		strcat(details,LastEvent);
		sprintf(KeyCodedetails1,"%d" , LastKeyCode_Perf);
                sprintf(KeyTypedetails1,"%d" , LastKeyType_Perf);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);

		strcat(details,KeyCodedetails);
                strcat(details,KeyCodedetails1);
                strcat(details,KeyTypedetails);
		strcat(details,KeyTypedetails1);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		strcpy(KeyCodedetails1,details);
		response["details"]=KeyCodedetails1;
		response["result"]="SUCCESS";
	
	}
	else if((strcmp(LastEvent,"IARM_BUS_PWRMGR_EVENT_MODECHANGED")==0)||
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOURCEAVAILABLE")==0)|| 
			(strcmp(LastEvent,"IARM_BUS_EVENT_RESOLUTIONCHANGE")==0))
	{
		strcat(details,LastEvent);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		response["details"]=details;
		response["result"]="SUCCESS";
	}
	else if((strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYX")==0)||
			(strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYY")==0)|| 
			(strcmp(LastEvent,"IARM_BUS_DUMMYMGR_EVENT_DUMMYZ")==0))
	{
		strcat(details,LastEvent);
                sprintf(KeyTimedetails1,"%lf" , LastKeyTime);
		strcat(details,KeyTimedetails);
		strcat(details,KeyTimedetails1);
		response["details"]=details;
		response["result"]="SUCCESS";
	}
	else
	{
		DEBUG_PRINT(DEBUG_LOG,"NO EVENTS RECEIVED BY HANDLER : %s", LastEvent);
		response["details"]="NO EVENTS RECEIVED BY HANDLER";
		response["result"]="FAILURE";
	}

	//ajan 
	char *lastKeyTimeStr =(char*)malloc(sizeof(char)*150);
	memset(lastKeyTimeStr , '\0', (sizeof(char)*150));
	sprintf(lastKeyTimeStr,"%lf" , LastKeyTime);

	char *pefDataInfo =(char*)malloc(sizeof(char)*150);
	memset(pefDataInfo , '\0', (sizeof(char)*150));
	sprintf(pefDataInfo,"%d:%d" , LastKeyCode_Perf,LastKeyType_Perf);

	response["performanceDataReading"]=lastKeyTimeStr;
	response["performanceDataName"]="TimeToGetIRKeyEvent";
	response["performanceDataUnit"]="ms";
	response["performanceDataInfo"]=pefDataInfo;


	/* TODO : Currently response is overwritten but need to change appropriately*/
	/* Check if more than one event recieved */
	if (gEventSummaryCount > 1)
	{
		response["details"]=gEventSummary;
		response["result"]="SUCCESS";
	}


	memset(&(gEventSummary) , '\0', (sizeof(char)*1024));
	gEventSummaryCount = 0;
	gRegisteredEventCount = 0;

	memset(&(LastEvent) , '\0', (sizeof(char)*20));
	memset(&(gLastEvent) , '\0', (sizeof(char)*20));
	LastKeyCode_Perf = 0;
	LastKeyType_Perf = 0;
	LastKeyTime = 0;
	free(KeyCodedetails1);
	free(KeyTypedetails1);
	free(KeyTimedetails1);

	DEBUG_PRINT(DEBUG_LOG,"\n %s --->Exit \n", __func__);
	return true;
}
#if 0
/**************************************************************************
 * Function Name : CreateObject
 * Description   : this function will be used to create a new object
 *      for the class IARMBUSPerfAgent
 **************************************************************************/

extern "C" IARMBUSPerfAgent* CreateObject()
{
	DEBUG_PRINT(DEBUG_LOG,"\n Creating the IarmBusPerf stub object \n");
	return new IARMBUSPerfAgent();
}

/**************************************************************************
 * Function Name : cleanup
 * Description   : This function will do the clean up.
 *
 **************************************************************************/

bool IARMBUSPerfAgent::cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{
	DEBUG_PRINT(DEBUG_LOG,"\n IARMBUSPerfAgent shutting down ");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_Init");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_Term");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_Connect");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_Disconnect");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_RegisterEventHandler");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_UnRegisterEventHandler");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_InvokeEventTransmitterApp");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_GetLastReceivedEventDetails");
	ptrAgentObj->UnregisterMethod("TestMgr_IARMBUSPERF_RegisterMultipleEventHandlers");

	return true;
}

/**************************************************************************
 * Function Name : DestroyObject
 * Description   : This function will be used to destory the object. 
 *
 **************************************************************************/

extern "C" void DestroyObject(IARMBUSPerfAgent *stubobj)
{
	DEBUG_PRINT(DEBUG_LOG,"\n Destroying IarmBusPerf stub object");
	delete stubobj;
}
#endif
