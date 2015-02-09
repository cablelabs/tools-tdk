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
//#define XDISC_OUTPUT_FILE      "/opt/output.json"
#define BASICDEVXML_FILE       "/opt/xupnp/BasicDevice.xml"
#define XCALDEVCONFIG          "/etc/xupnp/xdevice.conf"
#define XCALDEVHYBCONFIG       "/etc/xupnp/xdevice_hybrid.conf"
#define XDISCONFIG             "/etc/xupnp/xdiscovery.conf"
#define STARTUPCMD             "/etc/init.d/start-upnp-service restart"
#define TDK_XDEVICE_CONF_FILE  "tdk_xdevice.conf"

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
    bool XUPNPAgent_ModifyBasicDeviceXml(IN const Json::Value& req, OUT Json::Value& response);
    bool XUPNPAgent_CheckXMLRestoration(IN const Json::Value& req, OUT Json::Value& response);
    //Only for Gateway boxes
    bool XUPNPAgent_ReadXcalDeviceLogFile(IN const Json::Value& req, OUT Json::Value& response);
    bool XUPNPAgent_BroadcastEvent(IN const Json::Value& req, OUT Json::Value& response);
};

extern "C" XUPNPAgent* CreateObject();

#endif //__XUPNP_STUB_H__
