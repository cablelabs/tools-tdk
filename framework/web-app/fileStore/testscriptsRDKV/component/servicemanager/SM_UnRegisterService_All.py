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
  <id>1524</id>
  <version>2</version>
  <name>SM_UnRegisterService_All</name>
  <primitive_test_id>108</primitive_test_id>
  <primitive_test_name>SM_UnRegisterService</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script verifies the error scenario when un-registering of all supported services is done without being registered
Test Case ID: CT_Service Manager_16</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_16</test_case_id>
    <test_objective>Script to unregister all available services ("deviceSettingService", "screenCaptureService", "WebSocketService")</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ServiceManager::unregisterService</api_or_interface_used>
    <input_parameters>string service_name ("deviceSettingService", "screenCaptureService", "WebSocketService")</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will deregister a given service from ServiceManager component without registering
3. Service_Manager_Agent will return SUCCESS/FAILURE status based on the return value of “unregisterService” API.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.</except_output>
    <priority>High </priority>
    <test_stub_interface>libservicemanagerstub.so
1.TestMgr_SM_UnRegisterService</test_stub_interface>
    <test_script>SM_UnRegisterService_All</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Service Manager_16');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        services = ["deviceSettingService","screenCaptureService","WebSocketService"]
        for service_name in services:
            #calling ServiceManger - unregisterService API
            tdkTestObj = obj.createTestStep('SM_UnRegisterService');
            expectedresult="FAILURE"
            tdkTestObj.addParameter("service_name",service_name);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            serviceDetail = tdkTestObj.getResultDetails();
            print "[UNREGISTRATION DETAILS] : %s"%serviceDetail;
            #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Service not registered to unregister it";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Application unRegistered %s"%service_name;
                print "Failed to Unregister :%s"%service_name;
                break;
        print "[TEST EXECUTION RESULT] : %s"%actualresult;
        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
