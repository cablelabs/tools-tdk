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

#ifndef __CC_STUB_H__
#define __CC_STUB_H__

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "vlCCConstants.h"
#include "vlGfxScreen.h"

#define IN
#define OUT

#define TEST_SUCCESS true
#define TEST_FAILURE false 

#define NUM_SERVICES 			71
#define NUM_ANALOGCHANNEL_RANGE 	8
#define NUM_DIGITALCHANNEL_RANGE 	63
#define ERRORVALUE                  	100


#define TEST_INVALID 1000
#define TEST_DEFAULT 1001

class RDKTestAgent;
class CCAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		CCAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		/*ClosedCaption Wrapper functions*/
		bool CCInit(IN const Json::Value& req, OUT Json::Value& response);
                bool CCSetGetState(IN const Json::Value& req, OUT Json::Value& response);
                bool CCSetGetAttribute(IN const Json::Value& req, OUT Json::Value& response);
                bool CCSetGetDigitalChannel(IN const Json::Value& req, OUT Json::Value& response);
                bool CCSetGetAnalogChannel(IN const Json::Value& req, OUT Json::Value& response);
                bool CCGetSupportedServiceNumberCount(IN const Json::Value& req, OUT Json::Value& response);
                bool CCGetSupportedServiceNumber(IN const Json::Value& req, OUT Json::Value& response);
                bool CCHide(IN const Json::Value& req, OUT Json::Value& response);
                bool CCShow(IN const Json::Value& req, OUT Json::Value& response);
                bool CCOnEasStart(IN const Json::Value& req, OUT Json::Value& response);
                bool CCOnEasStop(IN const Json::Value& req, OUT Json::Value& response);
                bool CCSetTrickPlayStatus(IN const Json::Value& req, OUT Json::Value& response);
                bool CCResetTrickPlayStatus(IN const Json::Value& req, OUT Json::Value& response);
		
};
#endif //__CC_STUB_H__
