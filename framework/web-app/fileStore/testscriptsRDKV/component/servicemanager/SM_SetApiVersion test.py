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
  <id>300</id>
  <version>1</version>
  <name>SM_SetApiVersion test</name>
  <primitive_test_id>134</primitive_test_id>
  <primitive_test_name>SM_SetAPIVersion</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script gets and sets the API version of the requested service
Test Case ID: CT_SM_8</synopsis>
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
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_8</test_case_id>
    <test_objective>Service Manager – Get and Set service's API version number</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName)
unsigned int getApiVersionNumber()
Void setApiVersionNumber(unsigned int )
bool unregisterService(const QString&amp; )</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring - serviceName
ApiVersionNumber:  unsigned int – serviceName
unregisterService : Qstring-serviceName

</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register a given service with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will get the API version number for a given service and it will compare the default value with acquired value.
4.From step-3, if both the values are not same then  step- 5 will be continued otherwise the agent will expect another value which is not equal to default value.
5. Service_Manager_Agent will set the API version number for a given service.
6. Service_Manager_Agent will get the API version number for a given service.
7.Service_Manager_Agent will deregister a given service from ServiceManager component.
8. Service_Manager_Agent will compare both API  version number and return SUCCESS/FAILURE status.
</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.

Checkpoint 2. Compare the API version number with the new API version number.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libservicemanagerstub.so
1.TestMgr_SM_RegisterService
2.TestMgr_SM_SetAPIVersion
3.TestMgr_SM_UnRegisterService
</test_stub_interface>
    <test_script>SM_SetApiVersion test</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import random;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_SM_8');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling ServiceManger - registerService API
        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult="SUCCESS"
        serviceName="deviceSettingService";
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully registered a service with serviceManger";
                print "Registered Service:%s" %serviceName;
                tdkTestObj = obj.createTestStep('SM_SetAPIVersion');
                expectedresult="SUCCESS"
                apiVersion=random.randint(1,10000);
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult= tdkTestObj.getResult();
                
                apiVersion ="%s"%apiVersion;
                #Check for SUCCESS/FAILURE return value of SM_SetAPIVersion
                if expectedresult in actualresult:
                        print "SUCCESS: Application succesfully executes SM_SetAPIVersion API";
                        apiversiondetail =tdkTestObj.getResultDetails();
                        print apiversiondetail;
                        if "SAME_DATA_ALREADY_ENTERED" in apiversiondetail:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Existing API version value is same as the entered value";
                        elif apiVersion in apiversiondetail:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both API versions are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: API versions are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Application Failed to execute SM_SetAPIVersion API";
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
