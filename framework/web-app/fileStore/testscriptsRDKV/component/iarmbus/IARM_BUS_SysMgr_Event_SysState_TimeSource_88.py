#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1391</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARM_BUS_SysMgr_Event_SysState_TimeSource_88</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>18</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BroadcastEvent</primitive_test_name>
  <!--  -->
  <primitive_test_version>6</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>IARMBUS – Broadcasting and Receiving “IARM_BUS_SYSMGR_EVENT_SYSTEMSTATE” event and setting data for IARM_BUS_SYSMGR_SYSSTATE_TIME_SOURCE and getting back using IARM_BUS_SYSMGR_API_GetSystemStates RPC call.
Test case Id - CT_IARMBUS_88</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
from tdklib import TDKScriptingLibrary;
import time;
#Test component to be tested
obj = TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_88');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling IARMBUS API "IARM_Bus_Init"
        tdkTestObj = obj.createTestStep('IARMBUS_Init');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with IARMBUS library";
                #calling IARMBUS API "IARM_Bus_Connect"
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully connected with IARMBUS ";                       
                        #calling IARMBUS API "IARM_Bus_RegisterEventHandler"
                        tdkTestObj = obj.createTestStep('IARMBUS_RegisterEventHandler');
                        #passing parameter for receiving SYSMgr event sys state Time source
                        tdkTestObj.addParameter("owner_name","SYSMgr");
                        tdkTestObj.addParameter("event_id",0);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_RegisterEventHandler
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Event Handler registered successfully";
                                #invoking application to broadcast event
                                tdkTestObj = obj.createTestStep('IARMBUS_BroadcastEvent');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("event_id",0);
                                tdkTestObj.addParameter("newState",13);
                                setstate=11;
                                seterror=22;
                                setpayload="TimeSource";
                                tdkTestObj.addParameter("state",setstate);
                                tdkTestObj.addParameter("error",seterror);
                                tdkTestObj.addParameter("payload",setpayload);

                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
				print "set state:%d "%setstate, "error:%d "%seterror, "payload:%s "%setpayload;
                                actualresult = tdkTestObj.getResult();
                                #checking for Broadcast event invokation status
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:Broadcast event success";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE:Broadcast event fails";

				#Wait for SystemStates values to change
                                time.sleep(10);

                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                tdkTestObj.addParameter("method_name","GetSystemStates");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
				print details;
                                #checking for event received status
                                if expectedresult in actualresult:
                                        if str(setstate) in details and  str(seterror) in details:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: RPC method invoked and Time Source value for state and error properly set";
                                        else :
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: RPC method invoked and Time Source value for state and error has not been set";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARMBUS call failed";
                                #calling IARM_Bus_UnRegisterEventHandler API
                                tdkTestObj = obj.createTestStep('IARMBUS_UnRegisterEventHandler');
                                tdkTestObj.addParameter("owner_name","SYSMgr");
                                #Register for Broadcast event
                                tdkTestObj.addParameter("event_id",0);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of IARMBUS_UnRegisterEventHandler
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS:UnRegister Event Handler registered successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: IARM_Bus_UnRegisterEventHandler failed %s" %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_RegisterEventHandler %s" %details;
                        # Calling IARM_Bus_DisConnect API
                        tdkTestObj = obj.createTestStep('IARMBUS_DisConnect');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of IARMBUS_DisConnect
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application successfully disconnected from IARMBus";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: IARM_Bus_Disconnect failed. %s " %details;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus_Connect failed. %s" %details;
                #calling IARMBUS API "IARM_Bus_Term"
                tdkTestObj = obj.createTestStep('IARMBUS_Term');
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Term
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: IARM_Bus term success";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: IARM_Bus Term failed";                        
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: IARM_Bus_Init failed. %s " %details;
        
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
