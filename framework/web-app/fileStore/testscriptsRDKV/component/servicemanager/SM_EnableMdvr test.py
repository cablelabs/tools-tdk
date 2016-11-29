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
  <id>984</id>
  <version>1</version>
  <name>SM_EnableMdvr test</name>
  <primitive_test_id>137</primitive_test_id>
  <primitive_test_name>SM_HN_EnableMDVR</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script enables or disables MDVR using Home Networking service
Test Case ID: CT_SM_13</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <remarks>This scripting has not developed as this functionality has not been implemented by Service Manager module.</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_13</test_case_id>
    <test_objective>Service Manager – Checking for MDVR support(Enabled/Disabled).</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName)
virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp; )</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring – serviceName
CallMethod : const QString -  METHOD_HN_IS_MDVR_ENABLED,const ServiceParams&amp; - Null
CallMethod : const QString- METHOD_HN_SET_MDVR_ENABLED, const ServiceParams - bool 
unregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register a given homenetworking service with ServiceManager component. 
3.On Success of registerService , Service_Manager_Agent will enable MDVR for homenetworking service.
4. Service_Manager_Agent will check MDVR enable for homenetworking service.
5.Service_Manager_Agent will deregister a given service from ServiceManager component.
6. Service_Manager_Agent will check MDVR enable status and return SUCCESS/FAILURE status.

</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.

Checkpoint 2. Compare the MDVR status before and after enabling.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libservicemanagerstub.so
1.TestMgr_SM_RegisterService
2.TestMgr_SM_HN_EnableMDVR
3.TestMgr_SM_UnRegisterService
</test_stub_interface>
    <test_script>SM_EnableMdvr test</test_script>
    <skipped>Yes</skipped>
    <release_version>M21</release_version>
    <remarks>This scripting has not developed as this functionality has not been implemented by Service Manager module.</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_SM_13');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling ServiceManger - registerService API
        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult="SUCCESS"
        serviceName="homeNetworkingService";
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully registered a service with serviceManger";
                print "Registered Service:%s" %serviceName;
                tdkTestObj = obj.createTestStep('SM_HN_EnableMDVR');
                expectedresult="SUCCESS"
                enable=1;
                tdkTestObj.addParameter("enable",enable);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult= tdkTestObj.getResult();
                mdvrdetails= tdkTestObj.getResultDetails();
                enable="%s" %enable;
                #Check for SUCCESS/FAILURE return value of SM_HN_EnableMDVR
                if expectedresult in actualresult:
                        print "SUCCESS: Application succesfully executes SM_HN_EnableMDVR API";
                        print mdvrdetails;
                        if enable in mdvrdetails:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: MDVR enabled successfully";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Failed to enable MDVR";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Application Failed to execute SM_HN_EnableMDVR API";
                # calling SM_UnRegisterService to unregister service
                tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully unRegisteres a service";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Failed to unRegister the service" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Application failed to register a service";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
