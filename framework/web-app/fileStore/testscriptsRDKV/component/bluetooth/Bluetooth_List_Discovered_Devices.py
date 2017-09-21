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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Bluetooth_List_Discovered_Devices</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Bluetooth_GetDiscoveredDevices</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check whether discoverable  devices are avail bale in the discovered devices list</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <except_output></except_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import bluetoothlib;
from time import sleep

#Test component to be tested
bluetoothObj = tdklib.TDKScriptingLibrary("bluetooth","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
bluetoothObj.configureTestCase(ip,port,'Bluetooth_List_Discovered_Devices');

def getDiscoverableStatus():
    tdkTestObj = bluetoothObj.createTestStep('Bluetooth_IsAdapterDiscoverable');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    discoverableStatus = tdkTestObj.getResultDetails();
    if actualresult == expectedresult:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Bluetooth_IsAdapterDiscoverable Call is Successfull"
        return discoverableStatus
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Bluetooth_IsAdapterDiscoverable Call is NOT Successfull"


#Get the result of connection with test component and STB
bluetoothLoadStatus =bluetoothObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %bluetoothLoadStatus;
bluetoothObj.setLoadModuleStatus(bluetoothLoadStatus.upper());

if "SUCCESS" in bluetoothLoadStatus.upper():

   #Prmitive test case which associated to this Script
   expectedresult="SUCCESS"
   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterPowerStatus');
   #Execute the test case in STB
   tdkTestObj.executeTestCase(expectedresult);
   actualresult = tdkTestObj.getResult();
   powerStatusBefore = tdkTestObj.getResultDetails();
   if actualresult == expectedresult:
       tdkTestObj.setResultStatus("SUCCESS");
       print "Bluetooth_GetAdapterPowerStatus call is SUCCESS"
       print "DETAILS : Bluetooth_GetAdapterPowerStatus : " , powerStatusBefore
       if powerStatusBefore !="1":
           print "Bluetooth Adapter is OFF"
           print  "Turn ON the Bluetooth Adapter"
           tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterPowerStatus');
           tdkTestObj.addParameter("powerstatus",1);
           #Execute the test case in STB
           tdkTestObj.executeTestCase(expectedresult);
           actualresult = tdkTestObj.getResult();
           if actualresult == expectedresult:
               tdkTestObj.setResultStatus("SUCCESS");
               print "Bluetooth_SetAdapterPowerStatus call is SUCCESS"
               tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetAdapterPowerStatus');
               #Execute the test case in STB
               tdkTestObj.executeTestCase(expectedresult);
               actualresult = tdkTestObj.getResult();
               powerStatusAfter = tdkTestObj.getResultDetails();
               if powerStatusAfter == "1":
                   tdkTestObj.setResultStatus("SUCCESS");
                   print "Bluetooth Adapter Turned ON successfully"
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "Unable to Turn ON the Bluetooth Adapter"
           else:
               tdkTestObj.setResultStatus("FAILURE");
               print "Bluetooth_SetAdapterPowerStatus call is FAILURE"
       else:
           print "Bluetooth adapter is already ON"
   else:
       tdkTestObj.setResultStatus("FAILURE");
       print "Bluetooth_GetAdapterPowerStatus call is FAILURE"  
                 
   print "Get the Bluetooth discoverable status"
   discoverableStatusBefore = getDiscoverableStatus()
   if discoverableStatusBefore != "1":
       print "Bluetooth discoverable status is OFF"
       print  "Turn ON the Bluetooth discoverable status"
       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_SetAdapterDiscoverable');
       tdkTestObj.addParameter("discoverablestatus",1);
       tdkTestObj.addParameter("timeout",1000);
       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);
       actualresult = tdkTestObj.getResult();
       if actualresult == expectedresult:
           tdkTestObj.setResultStatus("SUCCESS");
           print "Bluetooth_SetAdapterDiscoverable call is SUCCESS"
           discoverableStatusAfter = getDiscoverableStatus()
           if  discoverableStatusAfter == "1":
               tdkTestObj.setResultStatus("SUCCESS");
               print "Bluetooth Discoverable status changed to ON successfully"
           else:
               tdkTestObj.setResultStatus("FAILURE");
               print "Unable to set the Bluetooth Discoverable status as ON"
       else:
           tdkTestObj.setResultStatus("FAILURE");
           print "Bluetooth_SetAdapterDiscoverable call is FAILURE"
   else:
       print "Bluetooth discoverable status is already ON"

   print "Set the client device as discoverable before starting the discovery in DUT"
   commandList = ['bluetoothctl','discoverable on','quit'] 
   output = bluetoothlib.executeBluetoothCtl(bluetoothObj,commandList)
   if "FAILURE" in output:
        tdkTestObj.setResultStatus("FAILURE");
        print "Connecting to client device got failed"
   else:
       print "Discoverable enabeld Client Device Name" , bluetoothlib.deviceName
       print "Starting the device discovery in DUT"
       tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StartDeviceDiscovery');
       #Execute the test case in STB
       tdkTestObj.executeTestCase(expectedresult);
       actualresult = tdkTestObj.getResult();
       if actualresult == expectedresult:
           tdkTestObj.setResultStatus("SUCCESS");
           print "Bluetooth_StartDeviceDiscovery call is SUCCESS"
           sleep(30);
           print "Check the discovered device list"
           tdkTestObj = bluetoothObj.createTestStep('Bluetooth_GetDiscoveredDevices');
           #Execute the test case in STB
           tdkTestObj.executeTestCase(expectedresult);
           actualresult = tdkTestObj.getResult();
           discoveredDeviceList = tdkTestObj.getResultDetails();
           print "discoveredDeviceList" , discoveredDeviceList.split()
           if actualresult == expectedresult:
               tdkTestObj.setResultStatus("SUCCESS");
               print "Bluetooth_GetDiscoveredDevices call is SUCCESS"
               if str(bluetoothlib.deviceName) in discoveredDeviceList.split():
                   tdkTestObj.setResultStatus("SUCCESS");
                   print "Client device is successfully discovered in DUT" 
                   print "Stop the device discovery"
                   tdkTestObj = bluetoothObj.createTestStep('Bluetooth_StopDeviceDiscovery');
                   #Execute the test case in STB
                   tdkTestObj.executeTestCase(expectedresult);
                   actualresult = tdkTestObj.getResult();
                   if actualresult == expectedresult:
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "Bluetooth_StopDeviceDiscovery call is SUCCESS"
                   else: 
                       tdkTestObj.setResultStatus("FAILURE");
                       print "Bluetooth_StopDeviceDiscovery call is FAILURE"
               else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print "Client device is NOT discovered in DUT" 
           else:
               tdkTestObj.setResultStatus("FAILURE");
               print "Bluetooth_GetDiscoveredDevices call is FAILURE"
       else:
           tdkTestObj.setResultStatus("FAILURE");
           print "Bluetooth_StartDeviceDiscovery call is FAILURE"


   bluetoothObj.unloadModule("bluetooth");

else:
    print "Failed to load bluetooth module\n";
    #Set the module loading status
    bluetoothObj.setLoadModuleStatus("FAILURE");
