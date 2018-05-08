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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_DisplaySettings_GetConnectedVideoDisplays</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if the service manager API to get connected video displays retrieves the value based on connection status</synopsis>
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
    <test_case_id>CT_Service Manager_125</test_case_id>
    <test_objective>Checks if the service manager API to get connected video displays retrieves the value based on connection status</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring - serviceName                                
CallMethod : const QString - "getConnectedVideoDisplays" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent and Device_Settings_Agent via the test agent.
2. Service_Manager_Agent will register the service "org.openrdk.DisplaySettings" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "getConnectedVideoDisplays" API to get the list of connected displays.
4. Device_Settings_Agent will invoke dsIsDisplayConnected API to check if display is connected.
5. TM will check if the data retrieved in step 3 supports the connection status and return SUCCESS/FAILURE status.
6. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the return value of the API is in accordance with the connection status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_DisplaySettings_GetConnectedVideoDisplays</test_script>
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
import json;


#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_DisplaySettings_GetConnectedVideoDisplays');
dsObj.configureTestCase(ip,port,'SM_DisplaySettings_GetConnectedVideoDisplays');

smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus ;
dsLoadStatus = dsObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %dsLoadStatus;

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in dsLoadStatus.upper():
        #Set the module loading status
        smObj.setLoadModuleStatus("SUCCESS");
        dsObj.setLoadModuleStatus("SUCCESS");
	result = devicesettings.dsManagerInitialize(dsObj);
        if "SUCCESS" in result:
        	serviceName="org.openrdk.DisplaySettings";
	        #Register Service
        	register = servicemanager.registerService(smObj,serviceName);
	
        	if "SUCCESS" in register:
                	print "SUCCESS: Registered %s with serviceManager"%serviceName;

			#Set API version
                        tdkTestObj = smObj.createTestStep('SM_SetAPIVersion');
                        expectedresult="SUCCESS"
                        apiVersion=6;
                        tdkTestObj.addParameter("apiVersion",apiVersion);
                        tdkTestObj.addParameter("service_name", serviceName);
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        apiversiondetail =tdkTestObj.getResultDetails();
                        print "[EXECUTION DETAILS] APi Version : %s"%apiversiondetail;
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "setApiVersionNumber successfully";
                        else:
                                print "setApiVersionNumber failed";
                                tdkTestObj.setResultStatus("FAILURE");

		        #Check for display connection status
                	isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj);
			print "Connection status: ", isDisplayConnected;
			if isDisplayConnected =="TRUE":
                		tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
		        	expectedresult="SUCCESS"
	                	tdkTestObj.addParameter("service_name", serviceName);
				tdkTestObj.addParameter("method_name", "getConnectedVideoDisplays");
                		tdkTestObj.executeTestCase(expectedresult);
		        	#Get the result of execution
	                	actualresult = tdkTestObj.getResult();
				if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
				        resultDetails = tdkTestObj.getResultDetails();
                			connectedDisplays = json.loads(resultDetails);
			        	print "Connected video displays: ", connectedDisplays;
					if connectedDisplays != []:
						status = False;
						for item in connectedDisplays:
							if "HDMI" in item:
								status = True;
								break
						if status: 
							tdkTestObj.setResultStatus("SUCCESS");
			                        	print "Display connected and listed in result";
						else:
							tdkTestObj.setResultStatus("FAILURE");
	                                	        print "Incorrect value retrieved for Connected Video Displays\n";
					else:
						tdkTestObj.setResultStatus("FAILURE");
			                	print "Empty list retrieved for connected video displays \n";
				else:	
					tdkTestObj.setResultStatus("FAILURE");
                			print "Failed to get connected video displays \n";
			else:
				tdkTestObj.setResultStatus("FAILURE");
	               		print "Please test with TV connected \n";
	
			unregister = servicemanager.unRegisterService(smObj,serviceName);
		result = devicesettings.dsManagerDeInitialize(dsObj);	
	else:
		print "Failed to initialize DS Manager";	
	smObj.unloadModule("servicemanager");
	dsObj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        smObj.setLoadModuleStatus("FAILURE");
        dsObj.setLoadModuleStatus("FAILURE");
