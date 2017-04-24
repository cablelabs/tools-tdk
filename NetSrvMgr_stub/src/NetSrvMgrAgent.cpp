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

#include "NetSrvMgrAgent.h"
#include <string.h>

#ifdef __cplusplus
extern "C" {
#include "libIBus.h"
#include "libIARMCore.h"
}
#endif

/*************************************************************************
Function name : NetSrvMgrAgent::NetSrvMgrAgent

Arguments     : NULL

Description   : Constructor for NetSrvMgrAgent class
***************************************************************************/

NetSrvMgrAgent::NetSrvMgrAgent () {

    DEBUG_PRINT (DEBUG_LOG, "NetSrvMgrAgent Initialized\n");
}

/**************************************************************************
Function name : NetSrvMgrAgent::initialize

Arguments     : Input arguments are Version string and NetSrvMgrAgent obj ptr

Description   : Registering all the wrapper functions with the agent for using these functions in the script
***************************************************************************/

bool NetSrvMgrAgent::initialize (IN const char* szVersion,IN RDKTestAgent *ptrAgentObj) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent Initialization Entry\n");

    ptrAgentObj->RegisterMethod (*this,&NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs, "TestMgr_NetSrvMgr_WifiMgrGetAvailableSSIDs");
    ptrAgentObj->RegisterMethod (*this,&NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetCurrentState, "TestMgr_NetSrvMgr_WifiMgrGetCurrentState");
    ptrAgentObj->RegisterMethod (*this,&NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetLAFState, "TestMgr_NetSrvMgr_WifiMgrGetLAFState");
    ptrAgentObj->RegisterMethod (*this,&NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetPairedSSID, "TestMgr_NetSrvMgr_WifiMgrGetPairedSSID");
    ptrAgentObj->RegisterMethod (*this,&NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetEnabled, "TestMgr_NetSrvMgr_WifiMgrSetEnabled");

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent Initialization Exit\n");

    return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                1.
 *****************************************************************************/

std::string NetSrvMgrAgent::testmodulepre_requisites() {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule pre_requisites --> Entry\n");
    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule pre_requisites --> Exit\n");
    return "SUCCESS";
}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Description   : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/

bool NetSrvMgrAgent::testmodulepost_requisites() {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Entry\n");

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgr testmodule post_requisites --> Exit\n");

    return TEST_SUCCESS;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the list of 
		available SSIDs.

Description   : Retrieve the available SSIDs from Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

bool NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs --->Entry\n");

    try {
	    
	char ssidList[WIFI_MGR_PARAM_LIST_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_SsidList_Param_t param;

 	memset (&param, 0, sizeof(param));
	iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
	    		        IARM_BUS_WIFI_MGR_API_getAvailableSSIDs,
	    		        (void *)&param,
	    		        sizeof(IARM_Bus_WiFiSrvMgr_SsidList_Param_t));
	    

	if (iarmResult != IARM_RESULT_SUCCESS || !(param.status)) {

	    DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetAvailableSSIDs for wifi manager failed\n");
	    response["result"] = "FAILURE";
	    response["details"] = "IARM_Bus_Call to GetAvailableSSIDs for wifi manager failed";
 	}
	else {

	    DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetAvailableSSIDs for wifi manager successful\n");

	    response["result"] = "SUCCESS";
	    if (0 >= param.curSsids.jdataLen) {
	        response["details"] = "No SSIDs are available";
	    }
	    else {     
	        memcpy (ssidList, param.curSsids.jdata, param.curSsids.jdataLen);
	        DEBUG_PRINT (DEBUG_TRACE, "Available SSIDs for Wifi Service Manager : %s\n", param.curSsids.jdata); 
	        response["details"] = ssidList;
	    }
	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetCurrentState

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the current 
		state of Wifi Service Manager.

Description   : Retrieve the current state of Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

bool NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetCurrentState(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetCurrentState --->Entry\n");

    try {
	    
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting wifi manager current state\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting wifi manager current state";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
	  			        IARM_BUS_WIFI_MGR_API_getCurrentState,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetCurrentState of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetCurrentState of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetCurrentState of wifi manager successful\n");
		if (param->data.wifiStatus < 0 || param->data.wifiStatus > MAX_WIFI_STATUS_CODE) {
		    
		    DEBUG_PRINT (DEBUG_TRACE, "Invalid Wifi manager status\n");
		    response["result"] = "FAILURE";
                    response["details"] = "Invalid Wifi manager status";
		}
		else {

		    DEBUG_PRINT (DEBUG_TRACE, "Current State of Wifi Service Manager : %s\n", aWifiStatus[param->data.wifiStatus].c_str()); 
			
		    response["result"] = "SUCCESS";
		    response["details"] = aWifiStatus[param->data.wifiStatus];
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetCurrentState\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetCurrentState";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetCurrentState -->Exit\n");
    return TEST_SUCCESS;
}
/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetLAFState

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the LAF 
		state of Wifi Service Manager.

Description   : Retrieve the LAF state of Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

bool NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetLAFState(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetLAFState --->Entry\n");

    try {
	    
	char lafState[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting wifi manager LAF state\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting wifi manager LAF state";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
					IARM_BUS_WIFI_MGR_API_getLNFState,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetLAFState of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetLAFState of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetLAFState of wifi manager successful\n");
		/*
		 *Check if Status code retured is a valid one
		 */
	        if (param->data.wifiLNFStatus < 0 || param->data.wifiLNFStatus > MAX_WIFI_LNF_STATUS_CODE) {

                    DEBUG_PRINT (DEBUG_TRACE, "Invalid Wifi LAF status\n");
                    response["result"] = "FAILURE";
                    response["details"] = "Invalid Wifi LAF status";
                }
                else {

	            DEBUG_PRINT (DEBUG_TRACE, "LAF State of Wifi Service Manager : %s\n", aWifiLAFStatus[param->data.wifiLNFStatus].c_str()); 
		
	            response["result"] = "SUCCESS";
	            response["details"] = aWifiLAFStatus[param->data.wifiLNFStatus];
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetLAFState\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetLAFState";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetLAFState -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_GetPairedSSID

Arguments     : Input argument None.
                Output argument is "SUCCESS" or "FAILURE" and the paired
		SSID for Wifi Service Manager.

Description   : Retrieve the paired SSID for Wifi Service Manager and
                pass it to Test Manager.
**************************************************************************/

bool NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_GetPairedSSID(IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetPairedSSID --->Entry\n");

    try {
	    
	//char currentState[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	char aSsid[WIFI_SSID_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t  *param = NULL;

	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	    		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for getting paired SSID for wifi manager\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for getting paired SSID for wifi manager";
	}
	else {

	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME, 
					IARM_BUS_WIFI_MGR_API_getPairedSSID,
				        (void *)param,
				        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
		

	    if (iarmResult != IARM_RESULT_SUCCESS || !(param->status)) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to GetPairedSSID of wifi manager failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to GetPairedSSID of wifi manager failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to GetPairedSSID of wifi manager successful\n");

		strcpy (aSsid, param->data.getPairedSSID.ssid);
		response["result"] = "SUCCESS";
		/*
		 *Check if a valid SSID
		 */
		if ('\0' != aSsid[0]) {

	            DEBUG_PRINT (DEBUG_TRACE, "Paired SSID for Wifi Service Manager : %s\n", aSsid); 
	            response["details"] = aSsid;
		}
		else {
	 	    DEBUG_PRINT (DEBUG_TRACE, "No ssid assigned\n");
                    response["details"] = "No ssid assigned";
		}
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_GetPairedSSID\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_GetPairedSSID";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_GetPairedSSID -->Exit\n");
    return TEST_SUCCESS;
}

/**************************************************************************
Function name : NetSrvMgrAgent_WifiMgr_SetEnabled

Arguments     : Input argument - Enable : True/False to enable/disable
		Wifi adapter.
                Output argument is "SUCCESS" or "FAILURE"

Description   : Enable/Disable the Wifi adapter
**************************************************************************/

bool NetSrvMgrAgent::NetSrvMgrAgent_WifiMgr_SetEnabled (IN const Json::Value& req, OUT Json::Value& response) {

    DEBUG_PRINT (DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetEnabled --->Entry\n");

    try {
	    
	char details[WIFI_MGR_PARAM_BUFFER_SIZE] = {'\0'};
	IARM_Result_t iarmResult = IARM_RESULT_SUCCESS;
	IARM_Bus_WiFiSrvMgr_Param_t *param = NULL;
	
	//Allocate enough to store the structure, the message
	iarmResult = IARM_Malloc (IARM_MEMTYPE_PROCESSLOCAL,
	  		          sizeof(IARM_Bus_WiFiSrvMgr_Param_t),
	    		          (void**)&param);

	if(iarmResult != IARM_RESULT_SUCCESS) {

	    DEBUG_PRINT (DEBUG_ERROR, "Error allocating memory for enabling/disabling wifi adapter\n");
	    response["result"] = "FAILURE";
	    response["details"] = "Error allocating memory for enabling/disabling wifi adapter";
	}
	else {
	    
	    memset (param, 0, sizeof(IARM_Bus_WiFiSrvMgr_Param_t));
	    param->data.setwifiadapter.enable = req["enable"].asBool();
            iarmResult = IARM_Bus_Call (IARM_BUS_NM_SRV_MGR_NAME,
                                        IARM_BUS_WIFI_MGR_API_setEnabled,
                                        (void *)param,
                                        sizeof(IARM_Bus_WiFiSrvMgr_Param_t));

	    /*
	     *No need to check param->status since its not set
	     *in this case
	     */
	    if (iarmResult != IARM_RESULT_SUCCESS) {

		DEBUG_PRINT (DEBUG_ERROR, "IARM_Bus_Call to SetEnabled for Wifi adapter failed\n");
		response["result"] = "FAILURE";
		response["details"] = "IARM_Bus_Call to SetEnabled for Wifi adapter failed";
 	    }
	    else {

	        DEBUG_PRINT (DEBUG_TRACE, "IARM_Bus_Call to SetEnabled successful\n");

		DEBUG_PRINT (DEBUG_TRACE, "Wifi adapter SetEnable status: %d\n", param->data.setwifiadapter.enable);
		sprintf(details,"Wifi adapter SetEnable status:%d", param->data.setwifiadapter.enable);
		response["result"] = "SUCCESS";
	        response["details"] = details;
	    }
	    /*
	     * Free Allocated memory
	     */
    	    IARM_Free(IARM_MEMTYPE_PROCESSLOCAL, param);
   	}
    }
    catch(...) {

       	DEBUG_PRINT (DEBUG_ERROR, "Exception Caught in NetSrvMgrAgent_WifiMgr_SetEnabled\n");

        response["details"]= "Exception Caught in NetSrvMgrAgent_WifiMgr_SetEnabled";
        response["result"]= "FAILURE";
    }

    DEBUG_PRINT(DEBUG_TRACE, "NetSrvMgrAgent_WifiMgr_SetEnabled -->Exit\n");
    return TEST_SUCCESS;
}

/****ee********************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "NetSrvMgrAgent".
**************************************************************************/

extern "C" NetSrvMgrAgent* CreateObject () {

    return new NetSrvMgrAgent ();
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
**************************************************************************/

bool NetSrvMgrAgent::cleanup (IN const char* szVersion, IN RDKTestAgent *ptrAgentObj) {

    DEBUG_PRINT (DEBUG_TRACE, "Cleaningup\n");
    if (NULL == ptrAgentObj) {
        return TEST_FAILURE;
    }

    ptrAgentObj->UnregisterMethod ("TestMgr_NetSrvMgr_WifiMgrGetAvailableSSIDs");
    ptrAgentObj->UnregisterMethod ("TestMgr_NetSrvMgr_WifiMgrGetCurrentState");
    ptrAgentObj->UnregisterMethod ("TestMgr_NetSrvMgr_WifiMgrGetLAFState");
    ptrAgentObj->UnregisterMethod ("TestMgr_NetSrvMgr_WifiMgrGetPairedSSID");
    ptrAgentObj->UnregisterMethod ("TestMgr_NetSrvMgr_WifiMgrSetEnabled");

    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is NetSrvMgrAgent Object

Description   : This function will be used to destory the NetSrvMgrAgent object.
**************************************************************************/
extern "C" void DestroyObject (NetSrvMgrAgent *stubobj) {

    DEBUG_PRINT (DEBUG_LOG, "Destroying NetSrvMgrAgent object\n");
    delete stubobj;
}
