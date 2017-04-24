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

#ifndef __NETSRVMGR_STUB_H__
#define __NETSRVMGR_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#include "wifiSrvMgrIarmIf.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

/*
 *Maximum value for Wifi Manager 
 *Parameter and Parameter List
 */
#define WIFI_MGR_PARAM_LIST_BUFFER_SIZE  10000
#define WIFI_MGR_PARAM_BUFFER_SIZE 100
#define MAX_WIFI_STATUS_CODE     7
#define MAX_WIFI_LNF_STATUS_CODE 7
#define WIFI_SSID_SIZE		33

using namespace std;
#if 0
enum {
    NETSRVMGR_GET_CURRENT_STATE = 1,
    NETSRVMGR_GET_LAF_STATE = 2,
    NETSRVMGR_SET_ENABLED = 3,
    NETSRVMGR_GET_PAIRED_SSID = 4,
    NETSRVMGR_CONNECT = 5,
    NETSRVMGR_INITIATE_WPS_PAIRING = 6,
    NETSRVMGR_SAVE_SSID = 7,
    NETSRVMGR_CLEAR_SSID = 8,
    NETSRVMGR_IS_PAIRED = 9,
    NETSRVMGR_GET_CONNECTED_SSID = 10,
    NETSRVMGR__GET_AVAILABLE_SSIDS = 11,
    NETSRVMGR_GET_RADIO_PROPS = 12,
    NETSRVMGR_GET_RADIO_STATS_PROPS = 13,
    NETSRVMGR_GET_SSID_PROPS = 14,
    NETSRVMGR_GET_END_POINT_PROPS =15
};
#endif


class RDKTestAgent;
class NetSrvMgrAgent : public RDKTestStubInterface
{
private:
    string aWifiStatus[MAX_WIFI_LNF_STATUS_CODE] = {"Wifi Uninstalled",
			   "Wifi disabled",
			   "Wifi disconnected",
			   "Wifi pairing",
			   "Wifi connecting",
			   "Wifi connected",
			   "Wifi failed"};
    string aWifiLAFStatus[MAX_WIFI_LNF_STATUS_CODE] = {"LNF Uninitialised",
			    "LNF in progress",
			    "LNF connected",
			    "LNF connected to private network",
			    "Disconnected no LNF gateway detected",
			    "Disconnected get LFAT failed",
			    "Disconnected cant connect to private network"};
    		
public:
    /*
     *Constructor
     */
    NetSrvMgrAgent ();

    /*
     *Inherited functions
     */
    bool initialize (IN const char* szVersion, IN RDKTestAgent *);

    bool cleanup (const char*, RDKTestAgent*);
    std::string testmodulepre_requisites ();
    bool testmodulepost_requisites ();

    /*
     *NetSrvMgrAgent Wrapper functions
     */
    bool NetSrvMgrAgent_WifiMgr_GetAvailableSSIDs (IN const Json::Value& req, OUT Json::Value& response);
    bool NetSrvMgrAgent_WifiMgr_GetCurrentState (IN const Json::Value& req, OUT Json::Value& response);
    bool NetSrvMgrAgent_WifiMgr_GetLAFState (IN const Json::Value& req, OUT Json::Value& response);
    bool NetSrvMgrAgent_WifiMgr_GetPairedSSID (IN const Json::Value& req, OUT Json::Value& response);
    bool NetSrvMgrAgent_WifiMgr_SetEnabled (IN const Json::Value& req, OUT Json::Value& response);
};

extern "C" NetSrvMgrAgent* CreateObject();

#endif //__NETSRVMGR_STUB_H__
