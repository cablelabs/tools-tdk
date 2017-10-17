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

#ifndef __BLUETOOTH_STUB_H__
#define __BLUETOOTH_STUB_H__


#include <json/json.h>
#include <string.h>
#include <stdlib.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#include "btmgr.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define DEVICE_NAME_BUFFER 10
#define DISCOVERED_DEVICE_BUFFER 30
#define PAIRED_DEVICE_BUFFER 10
#define CONNECTED_DEVICE_BUFFER 10
#define DEVICE_HANDLE_BUFFER 20
#define DEVICE_PROPERTIES_BUFFER 100

using namespace std;

BTRMGR_Result_t rc = BTRMGR_RESULT_SUCCESS;

class RDKTestAgent;
class BluetoothAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                BluetoothAgent ();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

                bool cleanup(const char*, RDKTestAgent*);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();

                //Stub functions
                bool Bluetooth_GetNumberOfAdapters(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetAdapterName(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_SetAdapterName(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_SetAdapterPowerStatus(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_IsAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_SetAdapterDiscoverable(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_StartDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_StopDeviceDiscovery(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetDiscoveredDevices(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_ConnectToDevice(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_DisconnectFromDevice(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetConnectedDevices(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_PairDevice(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_UnpairDevice(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetPairedDevices(IN const Json::Value& req, OUT Json::Value& response);
                bool Bluetooth_GetDeviceProperties(IN const Json::Value& req, OUT Json::Value& response);            
               
};
        extern "C" BluetoothAgent* CreateObject();
#endif //__BLUETOOTH_STUB_H__
