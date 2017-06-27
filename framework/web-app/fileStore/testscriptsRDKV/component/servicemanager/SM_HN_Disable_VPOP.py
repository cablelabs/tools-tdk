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
  <name>SM_HN_Disable_VPOP</name>
  <primitive_test_id>136</primitive_test_id>
  <primitive_test_name>SM_HN_EnableVPOP</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Disable the VPOP using home networking service</synopsis>
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
    <test_case_id>CT_Service Manager_66</test_case_id>
    <test_objective>Disable the VPOP using home networking service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring Ã&#131;Â¢Ã&#130;Â&#128;Ã&#130;Â&#147; serviceName                                
CallMethod : const QString - "set_vpop_enabled"/"is_vpop_enabled" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "homeNetworkingService" with ServiceManager component.
3. On Success of registerService , set the api version as 3.
4.Service_Manager_Agent will invoke the api set_vpop_enabled to disable the vpop.
5.Service_Manager_Agent will invoke the api is_vpop_enabled to get the status of the vpop.
6.TM will check if the values are same and return SUCCESS/FAILURE status.
7. Service_Manager_Agent will deregister the given service from ServiceManager component</automation_approch>
    <except_output>Checkpoint 1.Check the return values of APIs for success status.
Checkpoint 2. Check the value retrieved using is_vpop_enabled API is same as the value set using set_vpop_enabled API.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_HN_Disable_VPOP</test_script>
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
smObj.configureTestCase(ip,port,'SM_HN_Disable_VPOP');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %smLoadStatus;
smObj.setLoadModuleStatus(smLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "homeNetworkingService";
        register = servicemanager.registerService(smObj,serviceName)
        if "SUCCESS" in register:
                #Set the spi version as 3
                tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                expectedresult = "SUCCESS"
                apiVersion = 3;
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name",serviceName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Set the API version %s succesfully" % apiVersion
               
                    #Disable the VPOP
                    tdkTestObj = smObj.createTestStep('SM_HN_EnableVPOP');
                    print "Disable the VPOP"
                    enableValue = 0;
                    tdkTestObj.addParameter("enable",enableValue);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    enableVPOPDetails = tdkTestObj.getResultDetails();
                    print "[TEST EXECUTION DETAILS] : ",enableVPOPDetails;
                    if expectedresult in actualresult:
                        #Check whether VPOP is disabled or not
                        if str(enableValue) in enableVPOPDetails:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully disabled VPOP";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Disable VPOP failed";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Unable to disable the VPOP";
                else:
                    tdkTestObj.setResultStatus("FAILURE"); 
                    print "Unable to set the API Version " , apiVersion

        #Unregister home networking service 
        unregister = servicemanager.unRegisterService(smObj,serviceName);
        #Unloading service manager module
        smObj.unloadModule("servicemanager");
else:
    print "Failed to load service manager module\n"; 
    #Set the module loading status
    smObj.setLoadModuleStatus("FAILURE");
