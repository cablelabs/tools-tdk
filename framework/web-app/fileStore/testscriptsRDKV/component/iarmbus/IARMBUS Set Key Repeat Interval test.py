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
  <id>89</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS Set Key Repeat Interval test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>8</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets the Key Repeat Interval of the STB to the desired value
Test Case ID : CT_IARMBUS_25</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_IARMBUS_25');
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
                        #calling IARMBUS API "IARM_Bus_Call"
                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                        #passing prameter for querying key repeat interval time
                        tdkTestObj.addParameter("method_name","GetRepeatInterval");
                        tdkTestObj.addParameter("owner_name","IRMgr");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details=tdkTestObj.getResultDetails();
                        print "Query- Key Repeat Interval: %s" %details;
                        #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Query- RPC method invoked for querying key repeat interval ";
                                #calling IARMBUS API "IARM_Bus_Call"
                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                #passing prameter for setting key repeat interval time
                                tdkTestObj.addParameter("method_name","SetRepeatInterval");
                                tdkTestObj.addParameter("owner_name","IRMgr");
                                #setting Repeat interval to 100
                                tdkTestObj.addParameter("set_timeout",100);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details=tdkTestObj.getResultDetails();
                                print "Set- Key Repeat Interval: %s" %details;
                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                set_interval=details;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Set- RPC method invoked for setting key repeat interval ";
                                        #calling IARMBUS API "IARM_Bus_Call"
                                        tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                        #passing prameter for querying key repeat interval time
                                        tdkTestObj.addParameter("method_name","GetRepeatInterval");
                                        tdkTestObj.addParameter("owner_name","IRMgr");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        details=tdkTestObj.getResultDetails();
                                        print "Query- Key Repeat Interval: %s" %details;
                                        actualresult = tdkTestObj.getResult();
                                        get_interval=tdkTestObj.getResultDetails();
                                        #Check for both Repeat Interval before and after setting it
                                        if get_interval == set_interval:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Key Repeat Intervals are same";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Both the Key Repeat Interval are not same";
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Query- RPC method invoked for setting key repeat interval ";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: GetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: SetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: GetRepeatInterval ---> IARM_Bus_Call failed. %s " %details;
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
                print "FAILURE: IARM_Bus_Init failed. %s" %details;

        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
