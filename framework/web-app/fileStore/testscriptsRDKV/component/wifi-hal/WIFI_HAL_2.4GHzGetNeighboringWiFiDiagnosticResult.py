##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2018 RDK Management
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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>WIFI_HAL_2.4GHzGetNeighboringWiFiDiagnosticResult</name>
  <primitive_test_id/>
  <primitive_test_name>WIFI_HAL_GetNeighboringWiFiDiagnosticResult</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To get neighbor wifi diagnostic for 2.4GHz</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-Wifi</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_WIFI_HAL_21</test_case_id>
    <test_objective>To get neighboring wifi diagnostic result for 2.4GHz</test_objective>
    <test_type>Positive</test_type>
    <test_setup>IPClient-Wifi</test_setup>
    <pre_requisite>1.Ccsp Components  should be in a running state else invoke cosa_start.sh manually that includes all the ccsp components and TDK Component
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>wifi_connectEndpoint()
wifi_getNeighboringWiFiDiagnosticResult()</api_or_interface_used>
    <input_parameters>methodName : getNeighboringWiFiDiagnosticResult
radioIndex : 0</input_parameters>
    <automation_approch>1.Load the module.
2.Check if the DUT is connected to the required SSID, if not do the connection using wifi_connectEndpoint().
3.Invoke wifi_getNeighboringWiFiDiagnosticResult() api to get the neighboring WiFi Diagostic result.
4.If the api return SUCCESS,print the values,else FAILURE.
5.Unload the module.</automation_approch>
    <except_output>Get the neighboring wifi diagnostic result for 2.4GHz.</except_output>
    <priority>High</priority>
    <test_stub_interface>WIFI_HAL</test_stub_interface>
    <test_script>WIFI_HAL_2.4GHzGetNeighboringWiFiDiagnosticResult</test_script>
    <skipped>No</skipped>
    <release_version>M61</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkvWifiUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("wifihal","1");
sysObj = tdklib.TDKScriptingLibrary("sysutil","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetNeighboringWiFiDiagnosticResult');
sysObj.configureTestCase(ip,port,'WIFI_HAL_2.4GHzGetNeighboringWiFiDiagnosticResult');

#Get the result of connection with test component and DUT
loadmodulestatus1 =obj.getLoadModuleResult();
loadmodulestatus2 =sysObj.getLoadModuleResult();

if "SUCCESS" in loadmodulestatus1.upper() and loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");
    radioIndex = 0
    connectresult = isConnectedtoSSID(obj,sysObj,radioIndex);
    if "TRUE" in connectresult:
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('WIFI_HAL_GetNeighboringWiFiDiagnosticResult');
        #Radio index is 0 for 2.4GHz and 1 for 5GHz
        tdkTestObj.addParameter("radioIndex",0);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "TEST STEP 1: Get the neighbor wifi diagnostic"
            print "EXPECTED RESULT 1: Should get the neighbor wifi diagnostic"
            print "ACTUAL RESULT 1: Gets the neighbor wifi diagnostic successfully"
            print "Details : %s"%details;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : SUCCESS";
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print "TEST STEP 1: Get the neighbor wifi diagnostic"
            print "EXPECTED RESULT 1: Should get the neighbor wifi diagnostic"
            print "ACTUAL RESULT 1: Failed to get the neighbor wifi diagnostic"
            print "Details : %s"%details;
            #Get the result of execution
            print "[TEST EXECUTION RESULT] : FAILURE";
    else:
        print "Connecting to SSID operation failed"
	print "[TEST EXECUTION RESULT] : FAILURE";

    obj.unloadModule("wifihal");
    sysObj.unloadModule("sysutil");
else:
    print "Failed to load the module";
    sysObj.setLoadModuleStatus("FAILURE");
    obj.setLoadModuleStatus("FAILURE");
    print "Module loading failed";

