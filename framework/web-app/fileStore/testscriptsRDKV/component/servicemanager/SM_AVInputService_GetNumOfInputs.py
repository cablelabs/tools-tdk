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
  <id/>
  <version>1</version>
  <name>SM_AVInputService_GetNumOfInputs</name>
  <primitive_test_id/>
  <primitive_test_name>SM_AVInputService_GetNumberOfInputs</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis/>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_70</test_case_id>
    <test_objective>Checks if the service manager API to get the number of available AV inputs returns success</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â&#128;&#147; serviceName                                
CallMethod : const QString - "numberOfInputs" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "AVInput" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "numberOfInputs" API to get the number of available AV inputs.
4. TM will check if the API returns success and return SUCCESS/FAILURE status.
5. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of APIs for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_AVInputService_GetNumOfInputs</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import servicemanager;
import devicesettings;


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'SM_AVInputService_GetNumOfInputs');

#Get the result of connection with test component and STB
result=dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %result;
dsObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                print "DS Manager initialization success\n";
        else:
                print "DS Manager initialization failed\n";
                dsObj.unloadModule("devicesettings");
                exit();
else:
        exit();

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
obj.configureTestCase(ip,port,'SM_AVInputService_GetNumOfInputs');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %result;
if "SUCCESS" in result.upper():
        service_name = "AVInput";
        #Register Service
        register = servicemanager.registerService(obj,service_name);
        if "SUCCESS" in register:
                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('SM_AVInputService_GetNumberOfInputs');
                expectedresult = "SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        details = tdkTestObj.getResultDetails();
                        print "No: of AV inputs: %s" %details;
                else:
                        print "Failed to get AV input details";
                        tdkTestObj.setResultStatus("FAILURE");
                unregister = servicemanager.unRegisterService(obj,service_name);
        obj.unloadModule("servicemanager");

devicesettings.dsManagerDeInitialize(dsObj);
dsObj.unloadModule("devicesettings");

