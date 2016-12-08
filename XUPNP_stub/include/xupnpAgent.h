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

#ifndef __XUPNP_STUB_H__
#define __XUPNP_STUB_H__

#include <json/json.h>
#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

#define STR_LEN                128
#define LINE_LEN               1024
#define MAX_DATA_LEN           8192
#define XCALDEVICE             "xcal-device"
#define XDISCOVERY             "xdiscovery"
#define XDISC_LOG_FILE         "/opt/logs/xdiscovery.log"
#define XCALDEV_LOG_FILE       "/opt/logs/xdevice.log"
#define XDISCONFIG             "/etc/xupnp/xdiscovery.conf"
#define XDISCONFIG_EMULTR      "/etc/xdiscovery.conf"

using namespace std;

class RDKTestAgent;
class XUPNPAgent : public RDKTestStubInterface
{
public:
    //Constructor
    XUPNPAgent();

    //Inherited functions
    bool initialize(IN const char* szVersion, IN RDKTestAgent *);

    bool cleanup(const char*, RDKTestAgent*);
    std::string testmodulepre_requisites();
    bool testmodulepost_requisites();

    //XUPNPAgent Wrapper functions
    //Generic (common to Gateway + IPClient boxes)
    bool XUPNPAgent_GetUpnpResult(IN const Json::Value& req, OUT Json::Value& response);
    bool XUPNPAgent_ReadXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response);
    bool XUPNPAgent_CheckXDiscOutputFile(IN const Json::Value& req, OUT Json::Value& response);
    //Only for Gateway boxes
    bool XUPNPAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
};

extern "C" XUPNPAgent* CreateObject();

#endif //__XUPNP_STUB_H__
