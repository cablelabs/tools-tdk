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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HN_Persist_SetandGet_DeviceName</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_HN_GetDeviceName</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check whether Device name set using home networking service persist even after unregistering the service</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_64</test_case_id>
    <test_objective>To check whether Device name set using home networking service persist even after unregistering the service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring Ã¢ÂÂ serviceName                                
CallMethod : const QString - "set_device_name"/"get_device_name" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "homeNetworkingService" with ServiceManager component.
3. On Success of registerService , set the api version as 7
4.Service_Manager_Agent will invoke the api set_device_name to set the device name.
5.Unregister the "homeNetworkingService" service and register again
6.Service_Manager_Agent will invoke the api get_device_name to get the device name.
7.TM will check if the values are same and return SUCCESS/FAILURE status.
8. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.Check the return values of APIs for success status.
Checkpoint 2. Check the value retrieved using get_device_name API is same as the value set using set_device_name API.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_HN_Persist_SetandGet_DeviceName</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_HN_Persist_SetandGet_DeviceName');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "homeNetworkingService";
        register = servicemanager.registerService(smObj,serviceName)
        if "SUCCESS" in register:
                tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                expectedresult = "SUCCESS"
                apiVersion = 7;
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Set the API version %s succesfully" % apiVersion
               
                    #Set and Get the device name
                    tdkTestObj = smObj.createTestStep('SM_HN_SetDeviceName');
                    deviceName = "Test_STB_3"
                    tdkTestObj.addParameter("device_name",deviceName);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    deviceNameDetails = tdkTestObj.getResultDetails();
                    print "[TEST EXECUTION DETAILS 1] : ",deviceNameDetails; 
                    if expectedresult in actualresult:
                        #Check the device name set or not
                        if deviceName in deviceNameDetails:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully set the device name as" ,deviceName;
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Device name is not set as ",deviceName;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Unable to set the device name";

                    #Unregister home networking service 
                    print "Unregistering the homeNetworkingService to check device name persists after registering the service again"
                    unregister = servicemanager.unRegisterService(smObj,serviceName);
                 
                    #Register the home networking service
                    print "Registering the homeNetworkingService and check whether device name persists or not"
                    register = servicemanager.registerService(smObj,serviceName)
                    if "SUCCESS" in register:
                        #Get the device name
                        tdkTestObj = smObj.createTestStep('SM_HN_GetDeviceName');
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        getDeviceNameDetails = tdkTestObj.getResultDetails();
                        print "[TEST EXECUTION DETAILS 2] : ",deviceNameDetails; 
                    if expectedresult in actualresult:
                        #Check the device name set or not
                        if deviceName in getDeviceNameDetails:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully get the device name as" ,deviceName;
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Device name is not get as ",deviceName;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Unable to get the device name";
                    
                    #Unregister home networking service 
                    unregister = servicemanager.unRegisterService(smObj,serviceName);
             
                else:
                    tdkTestObj.setResultStatus("FAILURE"); 
                    print "Unable to set the API Version " , apiVersion
        #Unloading service manager module
        smObj.unloadModule("servicemanager");
else:
    print "Failed to load service manager module\n"; 
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");

