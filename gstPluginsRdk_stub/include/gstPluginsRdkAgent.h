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

#ifndef __GSTPLUGINSRDKAGENT_STUB_H__
#define __GSTPLUGINSRDKAGENT_STUB_H__
#include <json/json.h>
#include <unistd.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <string.h>
#include <glib.h>
#include <sstream>

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"

#define SEARCH_PATTERN " | grep \"%:\\\|:F:\\\|:E:\" > gstCheckLog"; 

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false

using namespace std;

class RDKTestAgent;
class gstPluginsRdkAgent : public RDKTestStubInterface
{
        public:
                //Constructor
                gstPluginsRdkAgent();

                //Inherited functions
                bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);
                bool cleanup(const char*, RDKTestAgent*);
		std::string testmodulepre_requisites();
		bool testmodulepost_requisites();	
		
		/*Optimised Code */
                bool gstPluginsRdkAgent_Aesdecrypt_SetProp_DecryptionEnable(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Aesdecrypt_GetProp_DecryptionEnable(const Json::Value&, Json::Value&);
                
		bool gstPluginsRdkAgent_Aesencrypt_SetProp_EncryptionEnable(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Aesencrypt_GetProp_EncryptionEnable(const Json::Value&, Json::Value&);
                
		bool gstPluginsRdkAgent_Dvrsrc_SetProp_RecordId(const Json::Value&, Json::Value&);
		bool gstPluginsRdkAgent_Dvrsrc_GetProp_RecordId(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_SetProp_Segmentname(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_Segmentname(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_Ccivalue(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_SetProp_Rate(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_Rate(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_StartTime(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_Duration(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_SetProp_PlayStartPosition(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsrc_GetProp_PlayStartPosition(const Json::Value&, Json::Value&);

                bool gstPluginsRdkAgent_Dvrsink_SetProp_RecordId(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsink_GetProp_RecordId(const Json::Value&, Json::Value&);
                bool gstPluginsRdkAgent_Dvrsink_GetProp_Ccivalue(const Json::Value&, Json::Value&);
};
        extern "C" gstPluginsRdkAgent* CreateObject();

#endif //__GSTPLUGINSRDKAGENT_STUB_H__
