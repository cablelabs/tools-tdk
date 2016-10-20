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
  <id>646</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetBlink_STRESS_test_102</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>75</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetBlink</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully change blink value of the front panel indicator continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_102</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_102');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                i = 0;
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling Device Settings - setBlink and getBlink APIs
                        tdkTestObj = obj.createTestStep('DS_SetBlink');
                        #setting scroll class parameters values
                        blink_interval = 1;
                        print "Blink interval value set to:%d" %blink_interval;
                        blink_iteration = 2;
                        print "Blink iteration value set to:%d" %blink_iteration;
                        tdkTestObj.addParameter("blink_interval",blink_interval);
                        tdkTestObj.addParameter("blink_iteration",blink_iteration);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        blinkdetails = tdkTestObj.getResultDetails();
                        blinkinterval="%s" %blink_interval;
                        blinkiteration="%s" %blink_iteration;
                        #Check for SUCCESS/FAILURE return value of DS_SetBlink
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the blink rate";
                                print "getblink %s" %blinkdetails;
                                #comparing the blink paramaters before and after setting
                                if ((blinkinterval in blinkdetails)and(blinkiteration in blinkdetails)):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the blink rates are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the blink rates are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set blink rate for LED";
                        time.sleep(100/1000);
                        #calling Device Settings - setBlink and getBlink APIs
                        tdkTestObj = obj.createTestStep('DS_SetBlink');
                        #setting scroll class parameters values
                        blink_interval = 5;
                        print "Blink interval value set to:%d" %blink_interval;
                        blink_iteration = 6;
                        print "Blink iteration value set to:%d" %blink_iteration;
                        tdkTestObj.addParameter("blink_interval",blink_interval);
                        tdkTestObj.addParameter("blink_iteration",blink_iteration);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        blinkdetails = tdkTestObj.getResultDetails();
                        blinkinterval="%s" %blink_interval;
                        blinkiteration="%s" %blink_iteration;
                        #Check for SUCCESS/FAILURE return value of DS_SetBlink
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the blink rate";
                                print "getblink %s" %blinkdetails;
                                #comparing the blink paramaters before and after setting
                                if ((blinkinterval in blinkdetails)and(blinkiteration in blinkdetails)):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the blink rates are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the blink rates are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set blink rate for LED";

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
