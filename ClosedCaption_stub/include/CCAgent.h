/*
* ============================================================================
* RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
* ============================================================================
* This file (and its contents) are the intellectual property of RDK Management, LLC.
* It may not be used, copied, distributed or otherwise  disclosed in whole or in
* part without the express written permission of RDK Management, LLC.
* ============================================================================
* Copyright (c) 2016 RDK Management, LLC. All rights reserved.
* ============================================================================
*/

#ifndef __CC_STUB_H__
#define __CC_STUB_H__

#include "rdkteststubintf.h"
#include "rdktestagentintf.h"
#include "vlCCConstants.h"
#include "vlGfxScreen.h"
#include <jsonrpccpp/server/connectors/tcpsocketserver.h>

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
class CCAgent : public RDKTestStubInterface , public AbstractServer<CCAgent>
{
	public:
		CCAgent(TcpSocketServer &ptrRpcServer) : AbstractServer <CCAgent>(ptrRpcServer)
                {
                  this->bindAndAddMethod(Procedure("TestMgr_CC_Init", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCInit);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_GetSupportedServiceNumber", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCGetSupportedServiceNumber);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_GetSupportedServiceNumberCount", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCGetSupportedServiceNumberCount);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_ResetTrickPlayStatus", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCResetTrickPlayStatus);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_OnEasStart", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCOnEasStart);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_OnEasStop", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCOnEasStop);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_SetTrickPlayStatus", PARAMS_BY_NAME, JSON_STRING,"trickPlayStatus",JSON_INTEGER,NULL), &CCAgent::CCSetTrickPlayStatus);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_Show", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCShow);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_Hide", PARAMS_BY_NAME, JSON_STRING,NULL), &CCAgent::CCHide);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_SetGetState", PARAMS_BY_NAME, JSON_STRING,"status",JSON_INTEGER,NULL), &CCAgent::CCSetGetState);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_SetGetDigitalChannel", PARAMS_BY_NAME, JSON_STRING,"channel_num",JSON_INTEGER,NULL), &CCAgent::CCSetGetDigitalChannel);  
                  this->bindAndAddMethod(Procedure("TestMgr_CC_SetGetAnalogChannel", PARAMS_BY_NAME, JSON_STRING,"analog_channel_num",JSON_INTEGER,NULL), &CCAgent::CCSetGetAnalogChannel);
                  this->bindAndAddMethod(Procedure("TestMgr_CC_SetGetAttribute", PARAMS_BY_NAME, JSON_STRING,"Categories",JSON_STRING,"ccAttribute",JSON_INTEGER,"ccType",JSON_INTEGER,"stylevalue",JSON_STRING,"value",JSON_INTEGER,NULL), &CCAgent::CCSetGetAttribute);
          
                }

		/*Ctor*/
//		CCAgent(){
                  //RDKTestAgent::bindAndAddMethod(Procedure("CCInit", PARAMS_BY_NAME, JSON_STRING,NULL),&CCAgent::CCInit);
  //               }

		/*inherited functions*/
		bool initialize(IN const char* szVersion);

	        //bool cleanup(IN const char* szVersion,IN RDKTestAgent *ptrAgentObj);
		bool cleanup(IN const char* szVersion);
                std::string testmodulepre_requisites();
                bool testmodulepost_requisites();
		/*ClosedCaption Wrapper functions*/

		void CCInit(IN const Json::Value& req, OUT Json::Value& response);
#if 1
                void CCSetGetState(IN const Json::Value& req, OUT Json::Value& response);
                void CCSetGetAttribute(IN const Json::Value& req, OUT Json::Value& response);
                void CCSetGetDigitalChannel(IN const Json::Value& req, OUT Json::Value& response);
                void CCSetGetAnalogChannel(IN const Json::Value& req, OUT Json::Value& response);
                void CCGetSupportedServiceNumberCount(IN const Json::Value& req, OUT Json::Value& response);
                void CCGetSupportedServiceNumber(IN const Json::Value& req, OUT Json::Value& response);
                void CCHide(IN const Json::Value& req, OUT Json::Value& response);
                void CCShow(IN const Json::Value& req, OUT Json::Value& response);
                void CCOnEasStart(IN const Json::Value& req, OUT Json::Value& response);
                void CCOnEasStop(IN const Json::Value& req, OUT Json::Value& response);
                void CCSetTrickPlayStatus(IN const Json::Value& req, OUT Json::Value& response);
                void CCResetTrickPlayStatus(IN const Json::Value& req, OUT Json::Value& response);
#endif		
};
#endif //__CC_STUB_H__
