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
  <name>SM_StorageManagerService_GetDeviceInfoById</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>7</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if the service manager API getDeviceInfo returns the device information of all available devices.</synopsis>
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
    <test_case_id>CT_Service Manager_106</test_case_id>
    <test_objective>Checks if the service manager API getDeviceInfo returns the device information of all available devices.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp;)</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â serviceName                                
CallMethod : const QString - "getDeviceInfo/getDeviceId" ,const ServiceParams - bool
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2. Service_Manager_Agent will register the service "org.openrdk.StoragemanagerService" with ServiceManager component.
3. On Success of registerService , Service_Manager_Agent will invoke "getDeviceInfo" API to get the device information for all the available devices.
4. Service_Manager_Agent will invoke "getDeviceIds" API to get the list of available device ids.
5. Service_Manager_Agent will invoke "getDeviceInfo" API with with device id as parameter for each device id obtained from step 4.
6. Service_Manager_Agent will check if the device info obtained in step 5 is a subset of output from step 3 and return SUCCESS/FAILURE status.
7. Service_Manager_Agent will deregister the given service from ServiceManager component.</automation_approch>
    <except_output>Checkpoint 1.Check the invocation of the API is success.
Checkpoint 2.Check the return value of getDeviceInfo API with device id as parameter is a subset of return value of getDeviceInfo API without any parameter.</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so</test_stub_interface>
    <test_script>SM_StorageManagerService_GetDeviceInfoById</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
smObj.configureTestCase(ip,port,'SM_StorageManagerService_GetDeviceInfoById');
iarmObj.configureTestCase(ip,port,'SM_StorageManagerService_GetDeviceInfoById');

loadmodulestatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;


def getCompleteDeviceInfo(serviceName):
	tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
        expectedresult="SUCCESS"
	devInfoList = [];
        tdkTestObj.addParameter("service_name", serviceName);
        tdkTestObj.addParameter("method_name", "getDeviceInfo");
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
		tdkTestObj.setResultStatus("SUCCESS");
                resultDetails = tdkTestObj.getResultDetails();
                devInfoList = json.loads(resultDetails);
                print "Device Info List : ", devInfoList;
	else:
		tdkTestObj.setResultStatus("FAILURE");
		print "Failed to get Device Info List";

	return devInfoList;


if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in iarmLoadStatus.upper():
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
				deviceInfo = getCompleteDeviceInfo(serviceName);
		                #Call GetDeviceIds API
                		tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
		                expectedresult="SUCCESS"
				tdkTestObj.addParameter("service_name", serviceName);
		                tdkTestObj.addParameter("method_name", "getDeviceIds");
                		tdkTestObj.executeTestCase(expectedresult);
		                #Get the result of execution
                		actualresult = tdkTestObj.getResult();
		                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
		                        resultDetails = tdkTestObj.getResultDetails();
                		        deviceIdList = json.loads(resultDetails);
		                        print "Device Id List : ", deviceIdList;
					for devId in deviceIdList:
						print "Device Id is %s" %devId;
						tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
		                                expectedresult="SUCCESS"
                		                tdkTestObj.addParameter("service_name", serviceName);
                                		tdkTestObj.addParameter("method_name", "getDeviceInfo");
						tdkTestObj.addParameter("params", devId);
						tdkTestObj.addParameter("inputCount", 1);
		                                tdkTestObj.executeTestCase(expectedresult);
                		                #Get the result of execution
                                		actualresult = tdkTestObj.getResult();
		                                if expectedresult in actualresult:
                                		        resultDetails = tdkTestObj.getResultDetails();
		                                        deviceInfoList = json.loads(resultDetails);
							print deviceInfoList;
							print deviceInfo[devId];
							if devId in deviceInfo.keys():
								if deviceInfo[devId] == deviceInfoList[devId]:
                		                        		tdkTestObj.setResultStatus("SUCCESS");
									print "Device information for the device id %s is present in the complete device info details" %devId;
								else:
									tdkTestObj.setResultStatus("FAILURE");
									print "Device information for the device id %s is not present in the complete device info details" %devId;
							else:
								tdkTestObj.setResultStatus("FAILURE");
								print "Device id %s is not a key in the complete device info details" %devId;
						else:
							tdkTestObj.setResultStatus("FAILURE");
							print "Failed to get DeviceInfo";

				else:
					tdkTestObj.setResultStatus("FAILURE");
                        		print "Failed to get device ids \n";
	
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
