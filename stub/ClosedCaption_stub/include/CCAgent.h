/*

* ============================================================================

* COMCAST CONFIDENTIAL AND PROPRIETARY

* ============================================================================

* This file and its contents are the intellectual property of Comcast.  It may

* not be used, copied, distributed or otherwise  disclosed in whole or in part

* without the express written permission of Comcast.

* ============================================================================

* Copyright (c) 2013 Comcast. All rights reserved.

* ============================================================================*/

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

class RDKTestAgent;
class CCAgent : public RDKTestStubInterface
{
	public:
		/*Ctor*/
		CCAgent();

		/*inherited functions*/
		bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj);

		bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);

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
