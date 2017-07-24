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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_StorageManagerService_SetTSBEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>7</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if the service manager API setTSBEnabled sets TSB enable status successfully</synopsis>
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
    <test_case_id>CT_Service Manager_95</test_case_id>
    <test_objective>Checks if the service manager API setTSBEnabled sets TSB enable status successfully</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â serviceName                                
CallMethod : const QString - "isTSBEnabled/setTSBEnabled" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register the service "org.openrdk.StoragemanagerService" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "isTSBEnabled" API to check if TSB is enabled/disabled.
4. Service_Manager_Agent will check if TSB is enabled or disabled and will invoke "setTSBEnabled" API to set TSB status to disable or enable respectively 
5. Service_Manager_Agent will invoke "isTSBEnabled" API to check if TSB status is same as the value set in step 4.
6. Repeat step 4 once again to change the TSB status.
7. Service_Manager_Agent will invoke "isTSBEnabled" API to check if TSB status is same as the value set in step 6 and return SUCCESS/FAILURE status.
8. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the return value of the get API is same as the one set using set API.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_StorageManagerService_SetTSBEnabled</test_script>
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
import iarmbus;
import json;


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_StorageManagerService_SetTSBEnabled');
iarmObj.configureTestCase(ip,port,'SM_StorageManagerService_SetTSBEnabled');


def changeTSBStatus(valueToEnable, serviceName):
	print "Setting TSB status to %s" %valueToEnable;
	success = False;
        expectedresult="SUCCESS"
        tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
        tdkTestObj.addParameter("service_name", serviceName);
        tdkTestObj.addParameter("method_name", "setTSBEnabled");
        tdkTestObj.addParameter("params", valueToEnable);
        tdkTestObj.addParameter("inputCount", 1);
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
        	tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name", serviceName);
                tdkTestObj.addParameter("method_name", "isTSBEnabled");
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                	tdkTestObj.setResultStatus("SUCCESS");
                        resultDetails = tdkTestObj.getResultDetails();
                        enableStatus = json.loads(resultDetails);
                        print "TSB enable status: ", enableStatus;
                        if enableStatus == valueToEnable:
                        	tdkTestObj.setResultStatus("SUCCESS");
                                print "TSB status changed successfully";
				success = True;
                        else:
                        	tdkTestObj.setResultStatus("FAILURE");
                                print "TSB status not changed";
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get TSB enable status \n";
	else:
        	tdkTestObj.setResultStatus("FAILURE");
                print "Failed to set TSB enable status \n";
	return success;


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
                		tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
		                expectedresult="SUCCESS"
                		tdkTestObj.addParameter("service_name", serviceName);
		                tdkTestObj.addParameter("method_name", "isTSBEnabled");
                		tdkTestObj.executeTestCase(expectedresult);
		                #Get the result of execution
                		actualresult = tdkTestObj.getResult();
		                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
		                        resultDetails = tdkTestObj.getResultDetails();
                		        enableStatus = json.loads(resultDetails);
		                        print "TSB enable status: ", enableStatus;
					enable = not enableStatus;
					result = changeTSBStatus(enable,serviceName);
					if result:
						result = changeTSBStatus(enableStatus,serviceName);		
				else:
					tdkTestObj.setResultStatus("FAILURE");
                        		print "Failed to get TSB enable status \n";
	
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
