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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1533</id>
  <version>2</version>
  <name>SM_WebSocket_GetUrl</name>
  <primitive_test_id>648</primitive_test_id>
  <primitive_test_name>SM_WebSocket_GetUrl</primitive_test_name>
  <primitive_test_version>0</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify get url on WebSocketService.
Test Case ID: CT_Service Manager_27</synopsis>
  <groupsid/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <remarks>XONE-15631: requestUrl() will return an empty string until WebSocket is connected.</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_27</test_case_id>
    <test_objective>To verify get url on WebSocketService</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ServiceManager::getGlobalService
WebSocketService::requestUrl</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register DeviceSettingService with ServiceManager component.
3.On Success of registerService , Service_Manager_Agent will get Url address info from WebSocketService requestUrl method.
5.Service_Manager_Agent will deregister a given service from ServiceManager component.
6. Service_Manager_Agent will check requestUrl status and return SUCCESS/FAILURE status.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.</except_output>
    <priority>High </priority>
    <test_stub_interface>libservicemanagerstub.so
1.TestMgr_SM_RegisterService
2.TestMgr_SM_WebSocket_GetUrl
3.TestMgr_SM_UnRegisterService</test_stub_interface>
    <test_script>SM_WebSocket_GetUrl</test_script>
    <skipped>Yes</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'CT_Service Manager_27');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #Call ServiceManger - registerService API
        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult="SUCCESS"
        service_name="WebSocketService";
        tdkTestObj.addParameter("service_name",service_name);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        serviceDetail = tdkTestObj.getResultDetails();
        print "[REGISTRATION DETAILS] : %s"%serviceDetail;
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Registered %s with serviceManager"%service_name

                #Call GetUrl API
                tdkTestObj = obj.createTestStep('SM_WebSocket_GetUrl');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceDetail = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] : %s"%serviceDetail;
                #Check for SUCCESS/FAILURE return value of SM_WebSocket_GetUrl
                if expectedresult in actualresult:
                        print "SUCCESS: GetUrl successful";
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        print "FAILURE: GetUrl failure";
                        tdkTestObj.setResultStatus("FAILURE");

                #Call ServiceManger - UnregisterService API
                tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceDetail = tdkTestObj.getResultDetails();
                print "[UNREGISTRATION DETAILS] : %s"%serviceDetail;
                #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: UnRegistered %s with serviceManager"%service_name
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Failed to unRegister service %s"%service_name
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Failed to register service %s"%service_name;

        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
