/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2017 RDK Management
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

#include "BluetoothAgent.h"
/*************************************************************************
Function name : BluetoothAgent::BluetoothAgent

Arguments     : NULL

Description   : Constructor for BluetoothAgent class
***************************************************************************/

BluetoothAgent::BluetoothAgent()
{
        DEBUG_PRINT(DEBUG_LOG, "BluetoothAgent Initialized\n");
}

/***************************************************************************
 *Function name : testmodulepre_requisites
 *Description   : testmodulepre_requisites will be used for setting the
 *                pre-requisites that are necessary for this component
 *                
 *****************************************************************************/

std::string BluetoothAgent::testmodulepre_requisites()
{
    DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Entry\n");
    rc = BTRMGR_Init();
    if (BTRMGR_RESULT_SUCCESS != rc)
    {
        DEBUG_PRINT(DEBUG_TRACE, "Failed to init Bluetooth Manager... Quiting..\n");
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
        return "FAILURE";
    }
    else
    {
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
        return "SUCCESS";
    }

}

/***************************************************************************
 *Function name : testmodulepost_requisites
 *Descrption    : testmodulepost_requisites will be used for resetting the
 *                pre-requisites that are set
 *
 *****************************************************************************/
bool BluetoothAgent::testmodulepost_requisites()
{
        DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule post_requisites --> Entry\n");
        rc = BTRMGR_DeInit();
        if (BTRMGR_RESULT_SUCCESS != rc)
        {
            DEBUG_PRINT(DEBUG_TRACE, "Failed to Deinit Bluetooth Manager... Quiting..\n");
            DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
            return false;
        }
        else
        {
            DEBUG_PRINT(DEBUG_TRACE, "Bluetooth testmodule pre_requisites --> Exit\n");
            return true;
        }
}

/**************************************************************************
Function Name   : CreateObject

Arguments       : NULL

Description     : This function is used to create a new object of the class "BluetoothAgent".
**************************************************************************/

extern "C" BluetoothAgent* CreateObject()
{
        return new BluetoothAgent();
}

bool BluetoothAgent::initialize(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj)
{    
        DEBUG_PRINT (DEBUG_TRACE, "Bluetooth Initialization Entry\n");

        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_GetNumberOfAdapters, "TestMgr_Bluetooth_GetNumberOfAdapters");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_GetAdapterName, "TestMgr_Bluetooth_GetAdapterName");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_SetAdapterName, "TestMgr_Bluetooth_SetAdapterName");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_GetAdapterPowerStatus, "TestMgr_Bluetooth_GetAdapterPowerStatus");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_SetAdapterPowerStatus, "TestMgr_Bluetooth_SetAdapterPowerStatus");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_IsAdapterDiscoverable, "TestMgr_Bluetooth_IsAdapterDiscoverable");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_SetAdapterDiscoverable, "TestMgr_Bluetooth_SetAdapterDiscoverable");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_StartDeviceDiscovery, "TestMgr_Bluetooth_StartDeviceDiscovery");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_StopDeviceDiscovery, "TestMgr_Bluetooth_StopDeviceDiscovery");
        ptrAgentObj->RegisterMethod(*this,&BluetoothAgent::Bluetooth_GetDiscoveredDevices, "TestMgr_Bluetooth_GetDiscoveredDevices");

        DEBUG_PRINT (DEBUG_TRACE, "Bluetooth Initialization Exit\n");
        return TEST_SUCCESS;
}

/***************************************************************************
 *Function name : Bluetooth_GetNumberOfAdapters
 *Descrption    : This function is to get the number of bluetooth adapters
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_GetNumberOfAdapters(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters --->Entry\n");
     
   unsigned char numOfAdapters = 0;
   rc = BTRMGR_GetNumberOfAdapters(&numOfAdapters);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = numOfAdapters;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetNumberOfAdapters call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetNumberOfAdapters call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetNumberOfAdapters -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetAdapterName
 *Descrption    : This function is to get the bluetooth adapter name
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_GetAdapterName(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName --->Entry\n");
   char adapterName[DEVICE_NAME_BUFFER]= {'\0'};
   rc = BTRMGR_GetAdapterName(0, adapterName);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = adapterName;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterName call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterName call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterName -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterName
 *Descrption    : This function is to set the bluetooth adapter name
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_SetAdapterName(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName --->Entry\n");
   char nameAdapter[DEVICE_NAME_BUFFER]= {'\0'};
   strcpy(nameAdapter, req["name"].asCString());
   rc = BTRMGR_SetAdapterName(0, nameAdapter);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = nameAdapter;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterName call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterName call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterName -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetAdapterPowerStatus
 *Descrption    : This function is to get the bluetooth adapter power status
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_GetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus --->Entry\n");
   unsigned char powerStatus;
   rc = BTRMGR_GetAdapterPowerStatus(0, &powerStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = powerStatus;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterPowerStatus call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetAdapterPowerStatus call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetAdapterPowerStatus -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterPowerStatus
 *Descrption    : This function is to set the bluetooth adapter power status
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_SetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus --->Entry\n");
   unsigned char powerStatus;
   powerStatus = req["powerstatus"].asInt();
   rc = BTRMGR_SetAdapterPowerStatus(0,powerStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterPowerStatus call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterPowerStatus call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterPowerStatus -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_IsAdapterDiscoverable
 *Descrption    : This function is to get the bluetooth discoverable status
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_IsAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable --->Entry\n");
   unsigned char discoverableStatus;
   rc = BTRMGR_IsAdapterDiscoverable(0,&discoverableStatus);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       response["details"] = discoverableStatus;
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAdapterDiscoverable call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_IsAdapterDiscoverable call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_IsAdapterDiscoverable -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_SetAdapterDiscoverable
 *Descrption    : This function is to set the bluetooth discoverable status
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_SetAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable --->Entry\n");
   unsigned char discoverableStatus;
   unsigned char Timeout;
   discoverableStatus = req["discoverablestatus"].asInt();
   Timeout = req["timeout"].asInt();
   rc = BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterDiscoverable call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_SetAdapterDiscoverable call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_SetAdapterDiscoverable -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_StartDeviceDiscovery
 *Descrption    : This function is to start the device discovery
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_StartDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery --->Entry\n");
   rc = BTRMGR_StartDeviceDiscovery(0);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartDeviceDiscovery call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StartDeviceDiscovery call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StartDeviceDiscovery -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_StopDeviceDiscovery
 *Descrption    : This function is to stop the device discovery
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_StopDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery --->Entry\n");
   rc = BTRMGR_StopDeviceDiscovery(0);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopDeviceDiscovery call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_StopDeviceDiscovery call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_StopDeviceDiscovery -->Exit\n");
       return TEST_FAILURE;
   }
}

/***************************************************************************
 *Function name : Bluetooth_GetDiscoveredDevices
 *Descrption    : This function is to get the discovered devices
 *****************************************************************************/
bool BluetoothAgent::Bluetooth_GetDiscoveredDevices(IN const Json::Value& req, OUT Json::Value& response)
{
   DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices --->Entry\n");
   BTRMGR_DiscoveredDevicesList_t discoveredDevices;
   rc = BTRMGR_GetDiscoveredDevices(0, &discoveredDevices);
   if (BTRMGR_RESULT_SUCCESS == rc)
   {
       response["result"] = "SUCCESS";
       int j = 0;
       DEBUG_PRINT(DEBUG_TRACE, "Number of Discovered Devices is (%d)  \n", discoveredDevices.m_numOfDevices);
       int deviceNameArraySize = discoveredDevices.m_numOfDevices*DEVICE_NAME_BUFFER;
       if (deviceNameArraySize)
       {
           char deviceName[deviceNameArraySize]= {'\0'};
           char *deviceNameAddr = deviceName;
           for (; j< discoveredDevices.m_numOfDevices; j++)
           {
               deviceNameAddr += sprintf(deviceNameAddr,"%s;",discoveredDevices.m_deviceProperty[j].m_name);
           }
           response["details"] = deviceName;
       }
       else
       {
          response["details"] = "NO_DEVICES_AVAILABLE";
       }
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDiscoveredDevices call is SUCCESS");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices --->Exit\n");
       return TEST_SUCCESS;
   }
   else
   {
       response["result"] = "FAILURE";
       DEBUG_PRINT(DEBUG_ERROR, "Bluetooth_GetDiscoveredDevices call is FAILURE");
       DEBUG_PRINT(DEBUG_TRACE, "Bluetooth_GetDiscoveredDevices -->Exit\n");
       return TEST_FAILURE;
   }
}

/**************************************************************************
Function Name   : cleanup

Arguments       : NULL

Description     : This function will be used to the close things cleanly.
 **************************************************************************/
bool BluetoothAgent::cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj)
{
    DEBUG_PRINT(DEBUG_TRACE, "cleaning up\n");

    if(NULL == ptrAgentObj)
    {
        return TEST_FAILURE;
    }

    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_GetNumberOfAdapters"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_GetAdapterName"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_SetAdapterName"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_GetAdapterPowerStatus"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_SetAdapterPowerStatus"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_IsAdapterDiscoverable"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_SetAdapterDiscoverable"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_StartDeviceDiscovery"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_StopDeviceDiscovery"); 
    ptrAgentObj->UnregisterMethod("TestMgr_Bluetooth_GetDiscoveredDevices"); 

    return TEST_SUCCESS;
}

/**************************************************************************
Function Name : DestroyObject

Arguments     : Input argument is BluetoothAgent Object

Description   : This function will be used to destory the BluetoothAgent object.
**************************************************************************/
extern "C" void DestroyObject(BluetoothAgent *stubobj)
{
        DEBUG_PRINT(DEBUG_LOG, "Destroying Bluetooth Agent object\n");
        delete stubobj;
}
