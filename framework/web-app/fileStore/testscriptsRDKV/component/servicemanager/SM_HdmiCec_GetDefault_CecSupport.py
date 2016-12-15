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
  <version>5</version>
  <name>SM_HdmiCec_GetDefault_CecSupport</name>
  <primitive_test_id>106</primitive_test_id>
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: Service Manager - Checking for CEC support default value (Enabled / Disabled). Default value: false(Disabled).
Test Case Id: CT_Service Manager_31
Test Type: Positive.</synopsis>
  <groups_id/>
  <execution_time>4</execution_time>
  <long_duration>false</long_duration>
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
    <test_case_id>CT_Service Manager_31</test_case_id>
    <test_objective>Service Manager – Checking for CEC support default value (Enabled / Disabled). Default value: false(Disabled)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName)
bool getEnabled()
bool unregisterService(const QString&amp; )</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring – serviceName
getEnabled : None
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register a given hdmicec service with ServiceManager component.
3.On Success of registerService, Service_Manager_Agent will check for hdmicec service support fetch default value.
4.Service_Manager_Agent will deregister a given service from ServiceManager component.
5. Service_Manager_Agent will compare the default status with current status returned.

</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.

Checkpoint 2.Compare the default status with current status returned.

</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so
</test_stub_interface>
    <test_script>SM_HdmiCec_GetDefault_CecSupport</test_script>
    <skipped>No</skipped>
    <release_version>M25</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;
import iarmbus;
import servicemanager;
from time import sleep;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#To Check whether HDMI device is connected or not.
#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'DS_isDisplayConnected');
#Get the result of connection with test component and STB
result = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %result;
dsObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
	isDisplayConnected = "FALSE"
	#Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
	#Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj)
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");

        if "FALSE" == isDisplayConnected:
		print "\nPlease test with HDMI device connected. Exiting....!!!"
		exit()
else:
	exit()


#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");

smObj.configureTestCase(ip,port,'SM_HdmiCec_GetDefault_CecSupport');
iarmObj.configureTestCase(ip,port,'SM_HdmiCec_GetDefault_CecSupport');

#Get the result of connection with test component and STB
smLoadStatus = smObj.getLoadModuleResult();
print "[servicemanager LIB LOAD STATUS]  :  %s" %smLoadStatus;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
#Set the module loading status
smObj.setLoadModuleStatus(smLoadStatus.upper());
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():

	#Calling IARM Bus Init
	init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')	
        if "SUCCESS" in init:
		connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
		if "SUCCESS" in connect:

        		#Remove cecData file
        		print "Flush CEC persistent data"
        		tdkTestObj = smObj.createTestStep('SM_HdmiCec_FlushCecData');
        		expectedresult = "SUCCESS"
        		tdkTestObj.executeTestCase(expectedresult);
        		actualresult = tdkTestObj.getResult();
        		details = tdkTestObj.getResultDetails();
        		print "[TEST EXECUTION DETAILS] : ",details;
        		if expectedresult in actualresult:
                		tdkTestObj.setResultStatus("SUCCESS");
        		else:
                		tdkTestObj.setResultStatus("FAILURE");

			#Create HdmiCecService
			service_name = "com.comcast.hdmiCec_1"
			register = servicemanager.registerService(smObj,service_name)
			if "SUCCESS" in register:	
				print "Get default cec support value"
				defaultCec = 0
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_GetEnabled');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                getEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",getEnabledDetails;
                                if expectedresult in actualresult:
                                        #Compare the set value with get value
                                        if defaultCec == int(getEnabledDetails):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Get Default CecSupport returned false as expected"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Get Default CecSupport did not return false as expected"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");


                                #Verify the presence of the cecData file
                                print "Verify the presence of CEC data"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckCecData');
                                expectedresult = "SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",details;
                                if expectedresult in actualresult:
                                        #Compare the set value with get value
                                        if 'false' in details:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "CecSupport value set to false"
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "CecSupport value not set to false"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                #Delete HdmiCecService
                                unregister = servicemanager.unRegisterService(smObj,service_name)

                        #Calling IARM_Bus_DisConnect API
                        disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
