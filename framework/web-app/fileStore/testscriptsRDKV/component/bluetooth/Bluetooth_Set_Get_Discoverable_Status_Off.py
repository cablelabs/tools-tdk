##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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
  <name>Bluetooth_Set_Get_Discoverable_Status_Off</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_IsAdapterDiscoverable</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Set and get the bluetooth discoverable status as Off</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
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
    <test_case_id>CT_BLUETOOTH_06</test_case_id>
    <test_objective>To set and get the bluetooth discoverable power status as Off.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1. Initialize the bluetooth manager
BTRMGR_Init();
2. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_IsAdapterDiscoverable
bool Bluetooth_SetAdapterDiscoverable</api_or_interface_used>
    <input_parameters>BTRMGR_IsAdapterDiscoverable(0,&amp;discoverableStatus);
BTRMGR_SetAdapterDiscoverable(0,discoverableStatus,Timeout);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Bluetooth agent will invoke the api   BTRMGR_SetAdapterDiscoverable with discoverable status as OFF
3.Check whether the discoverable status is set as OFF using BTRMGR_IsAdapterDiscoverable API</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The adapter discoverable status should set to OFF</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Set_Get_Discoverable_Status_Off</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Set_Get_Discoverable_Status_Off');

def setDiscoverableStatus(discoverableStatus,timeout):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterDiscoverable');
    tdkTestObj.addParameter("discoverablestatus",int(discoverableStatus))
    tdkTestObj.addParameter("timeout",int(timeout))
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"

def isAdapterDiscoverable(currentValue):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_IsAdapterDiscoverable')
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    discoverable = tdkTestObj.getResultDetails();
    print "RESULT : Bluetooth_IsAdapterDiscoverable : " , actualresult
    print "DETAILS : Bluetooth_IsAdapterDiscoverable : " , discoverable
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_IsAdapterDiscoverable API Call is Success"
        if discoverable == currentValue:
            tdkTestObj.setResultStatus("SUCCESS");
            return "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE"
    else:
        print "Bluetooth_IsAdapterDiscoverable API Call is Failure"
        tdkTestObj.setResultStatus("FAILURE");
        return "FAILURE"

#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():
 
    expectedresult="SUCCESS"
    print "Set the Bluetooth Discoverable status to ON (1)"
    discoverableOn = "1"
    timeout = "30"
    returnValue = setDiscoverableStatus(discoverableOn,timeout)
    if returnValue in expectedresult:
        print "Bluetooth_SetAdapterDiscoverable API Call is Successfull with status value as " , discoverableOn ,"and timeout is " ,timeout
        print "Check whether the Discoverable status is set to ON (1)" 
        returnValue = isAdapterDiscoverable(discoverableOn)
        if returnValue in expectedresult:
            print "Discoverable status changed to " , discoverableOn , "successfully"
            print "Change the Discoverable status to OFF (0)"
            discoverableOff = "0"
            returnValue = setDiscoverableStatus(discoverableOff,timeout)
            if returnValue in expectedresult:
                print "Bluetooth_SetAdapterDiscoverable API Call is Successfull with status value as " , discoverableOff ,"and timeout is " ,timeout
                print "Check whether the Discoverable status is set to OFF (0)"
                returnValue = isAdapterDiscoverable(discoverableOff)
                if returnValue in expectedresult:
                    print "Discoverable status changed to " , discoverableOff , "successfully"
                else:
                    print "Discoverable status NOT changed to " , discoverableOff
            else:
                print "Bluetooth_SetAdapterDiscoverable API Call is NOT Successfull with status value as " , discoverableOff ,"and timeout is " ,timeout
        else:
            print "Discoverable status NOT changed to " , discoverableOn
    else:
        print "Bluetooth_SetAdapterDiscoverable API Call is NOT Successfull with status value as " , discoverableOn ,"and timeout is " ,timeout

    bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");

