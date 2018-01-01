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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_AVInputService_GetCurrentVideoMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if the service manager API call to get current video mode is success</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_143</test_case_id>
    <test_objective>Checks if the service manager API call to get current video mode is success</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>"bool registerService(const QString&amp; , ServiceStruct )
Generic_CallMethod(const QString&amp; servicename,const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)"</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring - serviceName                                
CallMethod : const QString - "currentVideoMode" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register the service "AVInput" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke"currentVideoMode" API to get the current video mode.
4. Service_Manager_Agent will check if the call is success and return SUCCESS/FAILURE status.
5. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_AVInputService_GetCurrentVideoMode</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;
import devicesettings;
import iarmbus;
import json;


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_AVInputService_GetCurrentVideoMode');
dsObj.configureTestCase(ip,port,'SM_AVInputService_GetCurrentVideoMode');

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

loadmodulestatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
smObj.setLoadModuleStatus(loadmodulestatus.upper());

if "SUCCESS" in loadmodulestatus.upper():
        serviceName="AVInput";

	tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
	expectedresult="SUCCESS"
	tdkTestObj.addParameter("service_name", serviceName);
	tdkTestObj.addParameter("method_name", "currentVideoMode");
	tdkTestObj.executeTestCase(expectedresult);
	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	if expectedresult in actualresult:
		tdkTestObj.setResultStatus("SUCCESS");
		resultDetails = tdkTestObj.getResultDetails();
		print "Current Video Mode : ", resultDetails;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Failed to get Current Video Mode \n";

	smObj.unloadModule("servicemanager");

devicesettings.dsManagerDeInitialize(dsObj);
dsObj.unloadModule("devicesettings");
