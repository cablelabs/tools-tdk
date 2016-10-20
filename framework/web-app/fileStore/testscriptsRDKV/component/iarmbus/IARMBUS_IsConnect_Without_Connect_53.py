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
  <id>802</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_IsConnect_Without_Connect_53</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>4</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script tests Checking process registration status without registering it with IARMDaemon Manager
TEST CASE ID:CT_IARMBUS_53</synopsis>
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
obj.configureTestCase(ip,port,'CT_IARMBUS_53');
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
        details = tdkTestObj.getResultDetails();
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Application is initialized with IARM Bus library";
                #calling IARMBUS API "IARM_Bus_IsConnected"
                tdkTestObj = obj.createTestStep('IARMBUS_IsConnected');
                expectedresult="FAILURE";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of IARMBUS_IsConnected
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "FAILURE: IARM_Bus_Isconnected failed. %s " %details;

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "SUCCESS: API-Is_Connected Fails";                        
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
        #Unload the iarmbus module
        obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
