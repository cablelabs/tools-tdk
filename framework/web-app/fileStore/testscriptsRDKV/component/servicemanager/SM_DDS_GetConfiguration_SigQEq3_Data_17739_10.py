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
  <name>SM_DDS_GetConfiguration_SigQEq3_Data_17739_10</name>
  <primitive_test_id/>
  <primitive_test_name>SM_DDS_GetConfiguration</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Checks if the service manager wrapper for TR-181 returns non empty value for Pre-equalization data for the CM after convolution with data indicated</synopsis>
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
    <test_case_id>CT_17739_10</test_case_id>
    <test_objective>Checks if the service manager wrapper for TR-181 returns non empty value for Pre-equalization data for the CM after convolution with data indicated</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite>HostIF should be enabled</pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â&#128;&#147; serviceName                                
CallMethod : const QString - "getConfiguration" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register "org.rdk.DeviceDiagnostics_1" with ServiceManager component.
3.On Success of registerService , Service_Manager_Agent will invoke "getConfiguration" API to get the value of the object "Device.X_RDKCENTRAL-COM_DocsIf.docsIfSigQEqualizationData_3".
4. TM will check if the value is non empty and return SUCCESS/FAILURE status.
5.Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
Checkpoint 2. Check the value retrieved using API is non empty.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_DDS_GetConfiguration_SigQEq3_Data_17739_10</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
smObj.configureTestCase(ip,port,'SM_DDS_GetConfiguration_SigQEq3_Data_17739_10');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus);

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "org.rdk.DeviceDiagnostics_1";
        #Register Service
        register = servicemanager.registerService(smObj,serviceName);
        if "SUCCESS" in register:
                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_DDS_GetConfiguration');
                names = "Device.X_RDKCENTRAL-COM_DocsIf.docsIfSigQEqualizationData_3";
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("names",names);
		print "Getting configuration data for %s" %names;

                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        resultDetails = tdkTestObj.getResultDetails();
			if resultDetails:
	                        resultDetails = resultDetails.replace(" name: ","").lstrip('[');
        	                resultDetails = resultDetails.replace(" value: ","").rstrip(']');
                	        resultDetails = resultDetails.rstrip('; ');
				print "Received response";
                        	print resultDetails;
                                tdkTestObj.setResultStatus("SUCCESS");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Response is empty";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get TR-181 value\n";

                unregister = servicemanager.unRegisterService(smObj,serviceName);

        smObj.unloadModule("servicemanager");
else:
         print "Module loading failed";

