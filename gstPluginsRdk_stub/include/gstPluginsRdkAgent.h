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
