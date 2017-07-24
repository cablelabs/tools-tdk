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
  <version>3</version>
  <name>SM_StorageManagerService_IsDVREnabled</name>
  <primitive_test_id/>
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <primitive_test_version>7</primitive_test_version>
  <status>FREE</status>
  <synopsis>Checks if the service manager API to check if DVR is enabled returns the value true/false</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Service Manager_93</test_case_id>
    <test_objective>Checks if the service manager API to check if DVR is enabled returns the value true/false</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3	</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â&#128;&#147; serviceName                                
CallMethod : const QString - "isDVREnabled" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register the service "org.openrdk.StoragemanagerService" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "isDVREnabled" API to check if DVR is enabled.
4. TM will check if the API returns the value true/false and return SUCCESS/FAILURE status.
5. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the return value of the API is true/false.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_StorageManagerService_IsDVREnabled</test_script>
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
import iarmbus;
import json;


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_StorageManagerService_IsDVREnabled');
iarmObj.configureTestCase(ip,port,'SM_StorageManagerService_IsDVREnabled');

smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus ;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():
        #Set the module loading status
        smObj.setLoadModuleStatus("SUCCESS");

        serviceName="org.openrdk.StoragemanagerService";
        #Register Service
        register = servicemanager.registerService(smObj,serviceName);

        if "SUCCESS" in register:
                print "SUCCESS: Registered %s with serviceManager"%serviceName;
		#Calling IARM Bus Init
                init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
                if "SUCCESS" in init:
                        connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
                        if "SUCCESS" in connect:
		                #Call GetDeviceIds API
                		tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
		                expectedresult="SUCCESS"
                		tdkTestObj.addParameter("service_name", serviceName);
		                tdkTestObj.addParameter("method_name", "isDVREnabled");
                		tdkTestObj.executeTestCase(expectedresult);
		                #Get the result of execution
                		actualresult = tdkTestObj.getResult();
		                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
		                        resultDetails = tdkTestObj.getResultDetails();
                		        enableStatus = json.loads(resultDetails);
		                        print "DVR enable status: ", enableStatus;
					if enableStatus == True or enableStatus == False:
						 tdkTestObj.setResultStatus("SUCCESS");
	                                         print "DVR enable status retrieved successfully \n";
					else:
						 tdkTestObj.setResultStatus("FAILURE");
                                                 print "Incorrect value retrieved for DVR enable status\n";
				else:
					tdkTestObj.setResultStatus("FAILURE");
                        		print "Failed to get DVR enable status \n";
	
				#Calling IARM_Bus_DisConnect API
                                disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                        term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

		unregister = servicemanager.unRegisterService(smObj,serviceName);
	smObj.unloadModule("servicemanager");
	iarmObj.unloadModule("iarmbus");

else:
        print"Load module failed";
        #Set the module loading status
        smObj.setLoadModuleStatus("FAILURE");
        iarmObj.setLoadModuleStatus("FAILURE");
