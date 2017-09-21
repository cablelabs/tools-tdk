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
  <name>Bluetooth_Persist_Set_Get_Adapter_Power_Status_Off</name>
  <primitive_test_id/>
  <primitive_test_name>Bluetooth_SetAdapterPowerStatus</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check whether bluetooth adapter power status OFF persists or not</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_BLUETOOTH_11</test_case_id>
    <test_objective>To check whether bluetooth adapter power status OFF persists or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI5</test_setup>
    <pre_requisite>1. Initialize the bluetooth manager
BTRMGR_Init();
2. Deinit the bluetooth manager after test
BTRMGR_DeInit();</pre_requisite>
    <api_or_interface_used>bool Bluetooth_GetAdapterPowerStatus
bool Bluetooth_SetAdapterPowerStatus</api_or_interface_used>
    <input_parameters>BTRMGR_GetAdapterPowerStatus(0, &amp;powerStatus);
BTRMGR_SetAdapterPowerStatus(0,powerStatus);</input_parameters>
    <automation_approch>1. TM loads the Bluetooth agent via the test agent.
2  Bluetooth agent will invoke the api   BTRMGR_SetAdapterPowerStatus with power status as OFF
3.Check whether the power status is persists as OFF using BTRMGR_GetAdapterPowerStatus API</automation_approch>
    <except_output>Checkpoint 1.Verify the API call return value
Checkpoint 2.The adapter power status should persists as OFF</except_output>
    <priority>High</priority>
    <test_stub_interface>libbluetoothstub.so.0</test_stub_interface>
    <test_script>Bluetooth_Persist_Set_Get_Adapter_Power_Status_Off</test_script>
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
bluetoothObj.configureTestCase(ip,port,'Bluetooth_Persist_Set_Get_Adapter_Power_Status_Off');

def setAdapterPowerStatus(adapterPowerStatus):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterPowerStatus');
    tdkTestObj.addParameter("powerstatus",int(adapterPowerStatus))
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_SetAdapterPowerStatus API Call is Successfull with value as " , adapterPowerStatus
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Bluetooth_SetAdapterPowerStatus API Call is NOT Successfull with value as " ,adapterPowerStatus
def getAdapterPowerStatus(currentValue):
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterPowerStatus');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    adapterPower = tdkTestObj.getResultDetails();
    print "RESULT : Bluetooth_GetAdapterPowerStatus : " , actualresult
    print "DETAILS : Bluetooth_GetAdapterPowerStatus : " , adapterPower
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_GetAdapterPowerStatus API Call is Success"
        if adapterPower == currentValue:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Bluetooth Adapter Power Status set to " , adapterPower , "successfully"
            return "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Bluetooth Adapter Power Status NOT set to " , adapterPower
            return "FAILURE"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Bluetooth_GetAdapterPowerStatus API Call is Failure"
        return "FAILURE"

#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():
   
   expectedresult="SUCCESS"
   print "Set Bluetooth Adapter Power Status as OFF (0)"
   powerStatus = "0";
   setAdapterPowerStatus(powerStatus);
   print "Check whether the power status is set to OFF (0)"
   output = getAdapterPowerStatus(powerStatus);
   if "SUCCESS" in output:
       #Reboot the STB
       bluetoothObj.initiateReboot();
          
       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterPowerStatus');
       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);
       actualresult = tdkTestObj.getResult();
       adapterPower = tdkTestObj.getResultDetails();
       print "RESULT : Bluetooth_GetAdapterPowerStatus After Reboot : " , actualresult
       print "DETAILS : Bluetooth_GetAdapterPowerStatus After Reboot : " , adapterPower
       if actualresult == expectedresult:
           tdkTestObj.setResultStatus("SUCCESS");
           print "Bluetooth_GetAdapterPowerStatus API Call After Reboot is Success"
           if adapterPower == powerStatus:
               tdkTestObj.setResultStatus("SUCCESS");
               print "Bluetooth Adapter Power Status " , adapterPower , "Persisted successfully"
           else:
               tdkTestObj.setResultStatus("FAILURE");
               print "Bluetooth Adapter Power Status " , adapterPower , "NOT Persisted"
       else:
           tdkTestObj.setResultStatus("FAILURE");
           print "Bluetooth_GetAdapterPowerStatus API Call After Reboot is Failure"

       powerStatus = "1";
       print "Revert the power status to ON (1)"
       setAdapterPowerStatus(powerStatus)
       print "Check whether the power status is set to ON (1)"
       getAdapterPowerStatus(powerStatus);


   bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");

