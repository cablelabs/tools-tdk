##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>417</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_DummyCall_Persistent_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>9</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script tests the successful Dummy RPC calls for 'x' times
Test Case ID : CT_IARMBUS_41</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Dummy');
loadmodulestatus =obj.getLoadModuleResult();
print "Iarmbus module loading status :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling IARM_Bus_Init API
        tdkTestObj = obj.createTestStep('IARMBUS_Init');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details=tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application successfully initialized with IARMBUS library";
                #calling IARM_Bus_Connect API
                tdkTestObj = obj.createTestStep('IARMBUS_Connect');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details=tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_Connect IARMBUS_Connect
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application successfully connected with IARMBUS ";
                        i=0
                        for i in range(0,100):
                                print "**************** Iteration ", (i+1), " ****************";
                                tdkTestObj = obj.createTestStep('IARMBUS_InvokeSecondApplication');
                                tdkTestObj.addParameter("appname","Test_Event_Mgr");
                                tdkTestObj.addParameter("argv1","");
                                tdkTestObj.addParameter("apptype","background");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #details=tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Second application Invoked successfully";

                                        time.sleep(2)
                                        #Syncing Second Application
                                        tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                        tdkTestObj.addParameter("lockenabled","false");
                                        expectedresult="SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        #Check for SUCCESS/FAILURE for syncing second application
                                        if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Second application synced successfully";

                                                #calling two dummy RPC using IARM_Bus_Call API
                                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                tdkTestObj.addParameter("method_name","DummyAPI0");
                                                api_0_Data=1;
                                                tdkTestObj.addParameter("testapp_API0_data",api_0_Data);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                print details;
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                                if expectedresult in actualresult:
                                                        print "SUCCESS: Application invokes RPC-DummyAPI0 successfully";
                                                        dataCompare="%s" %(api_0_Data+10000000);
                                                        if dataCompare in details:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Both data are same";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE: Both data are not same";
                                                                break;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_Call failed. %s" %details;

                                                tdkTestObj = obj.createTestStep('IARMBUS_BusCall');
                                                tdkTestObj.addParameter("owner_name","Test_Event_Mgr");
                                                tdkTestObj.addParameter("method_name","DummyAPI1");
                                                api_1_Data=3;
                                                tdkTestObj.addParameter("testapp_API1_data",api_1_Data);
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details=tdkTestObj.getResultDetails();
                                                print details;
                                                #Check for SUCCESS/FAILURE return value of IARMBUS_BusCall
                                                if expectedresult in actualresult:
                                                        print "SUCCESS: Application invokes an RPC-DummyAPI1 successfully";
                                                        dataCompare="%s" %(api_1_Data+10000000);
                                                        if dataCompare in details:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "SUCCESS: Both data are same";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE: Both data are not same";
                                                                break;
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: IARM_Bus_Call failed. %s" %details;

                                                time.sleep(2)

                                                #Syncing Second Application
                                                tdkTestObj = obj.createTestStep('IARMBUS_SyncSecondApplication');
                                                tdkTestObj.addParameter("lockenabled","false");
                                                expectedresult="SUCCESS"
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                #Check for SUCCESS/FAILURE for syncing second application
                                                if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "SUCCESS: Second application synced successfully";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "FAILURE: Failed to sync second application";

                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Failed to sync second application";

                                        time.sleep(1);
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Second application failed to execute";

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
