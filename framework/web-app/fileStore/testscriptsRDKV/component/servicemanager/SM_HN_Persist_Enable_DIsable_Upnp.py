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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HN_Persist_Enable_DIsable_Upnp</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_HN_SetUpnpEnabled</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if Upnp enable/disable status persists across different instances of service.</synopsis>
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
    <box_type>Emulator-Client</box_type>
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
    <test_case_id>CT_Service Manager_61</test_case_id>
    <test_objective>Checks if Upnp enable/disable status persists across different instances of service.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â serviceName                                
CallMethod : const QString - "setUpnpEnabled"/"isUpnpEnabled" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register "homeNetworkingService" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "setUpnpEnabled" API to set the value of Upnp status to "true".
4. Service_Manager_Agent will invoke "isUpnpEnabled" API to get the value of Upnp status.
5. TM will check if the values are same and return SUCCESS/FAILURE status.
6. Service_Manager_Agent will deregister the given service from ServiceManager component.
7. Service_Manager_Agent will register "homeNetworkingService" with ServiceManager component again.
8. Service_Manager_Agent will invoke "isUpnpEnabled" API to get the value of Upnp status.
9. TM will check if the value is "true" and return SUCCESS/FAILURE status.
10. Service_Manager_Agent will invoke "setUpnpEnabled" API to set the value of Upnp status to "false".
11. Service_Manager_Agent will invoke "isUpnpEnabled" API to get the value of Upnp status.
12. TM will check if the values are same and return SUCCESS/FAILURE status.
13. Service_Manager_Agent will deregister the given service from ServiceManager component.
14. Service_Manager_Agent will register "homeNetworkingService" with ServiceManager component again.
15. Service_Manager_Agent will invoke "isUpnpEnabled" API to get the value of Upnp status.
16. TM will check if the value is "false" and return SUCCESS/FAILURE status.
17. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of APIs for success status.
Checkpoint 2. Check the enable/disable values persist across different instances of service</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_HN_Persist_Enable_DIsable_Upnp</test_script>
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

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_HN_Persist_Enable_DIsable_Upnp');

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

                #Enable Upnp status.
                tdkTestObj = smObj.createTestStep('SM_HN_SetUpnpEnabled');
                expectedresult = "SUCCESS";
                enable = 1;
                print "Setting Upnp status to ",enable;
                tdkTestObj.addParameter("enable",enable);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                setEnabledDetails = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #Get Upnp enable status
                tdkTestObj = smObj.createTestStep('SM_HN_IsUpnpEnabled');
                expectedresult = "SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                getEnabledDetails = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
                if expectedresult in actualresult:
                        #Compare the set value with get value
                        if enable == int(getEnabledDetails):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Upnp status enabled";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Upnp status not enabled"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
		
		#Unregistering and re registering service to check persistence of Upnp status
                unregister = servicemanager.unRegisterService(smObj,serviceName);
                register = servicemanager.registerService(smObj,serviceName)
                if "SUCCESS" in register:
			#Get Upnp enable status
	                tdkTestObj = smObj.createTestStep('SM_HN_IsUpnpEnabled');
        	        expectedresult = "SUCCESS";
                	tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
        	        getEnabledDetails = tdkTestObj.getResultDetails();
                	print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
	                if expectedresult in actualresult:
        	                #Compare the set value with get value
                	        if enable == int(getEnabledDetails):
                        	        tdkTestObj.setResultStatus("SUCCESS");
                                	print "Upnp enable status Persists";
	                        else:
        	                        tdkTestObj.setResultStatus("FAILURE");
                	                print "Upnp enable status does not persist"
	                else:
        	                tdkTestObj.setResultStatus("FAILURE");


	                #Disable Upnp status.
        	        tdkTestObj = smObj.createTestStep('SM_HN_SetUpnpEnabled');
                	expectedresult = "SUCCESS";
	                enable = 0;
        	        print "Setting Upnp status to ",enable;
                	tdkTestObj.addParameter("enable",enable);
	                tdkTestObj.executeTestCase(expectedresult);
        	        actualresult = tdkTestObj.getResult();
                	setEnabledDetails = tdkTestObj.getResultDetails();
	                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
        	        if expectedresult in actualresult:
                	        tdkTestObj.setResultStatus("SUCCESS");
	                else:
        	                tdkTestObj.setResultStatus("FAILURE");

                	#Get Upnp enable status
	                tdkTestObj = smObj.createTestStep('SM_HN_IsUpnpEnabled');
        	        expectedresult = "SUCCESS";
                	tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
        	        getEnabledDetails = tdkTestObj.getResultDetails();
                	print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
	                if expectedresult in actualresult:
        	                #Compare the set value with get value
                	        if enable == int(getEnabledDetails):
                        	        tdkTestObj.setResultStatus("SUCCESS");
                                	print "Upnp status disabled";
	                        else:
        	                        tdkTestObj.setResultStatus("FAILURE");
                	                print "Upnp status not disabled";

			#Unregistering and re registering service to check persistence of Upnp status
                        unregister = servicemanager.unRegisterService(smObj,serviceName);
                        register = servicemanager.registerService(smObj,serviceName)
                        if "SUCCESS" in register:
				#Get Upnp enable status
	                        tdkTestObj = smObj.createTestStep('SM_HN_IsUpnpEnabled');
        	                expectedresult = "SUCCESS";
                	        tdkTestObj.executeTestCase(expectedresult);
                        	actualresult = tdkTestObj.getResult();
	                        getEnabledDetails = tdkTestObj.getResultDetails();
        	                print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
                	        if expectedresult in actualresult:
                        	        #Compare the set value with get value
                                	if enable == int(getEnabledDetails):
                                        	tdkTestObj.setResultStatus("SUCCESS");
	                                        print "Upnp disable status persists";
        	                        else:
                	                        tdkTestObj.setResultStatus("FAILURE");
                        	                print "Upnp disable status does not persist";


		                unregister = servicemanager.unRegisterService(smObj,serviceName);
        smObj.unloadModule("servicemanager");
else:
        print "Failed to load service manager module\n";

