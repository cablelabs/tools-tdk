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
  <name>SM_HdmiCec_SendMsgGetPowerStatus_CecEnabled</name>
  <primitive_test_id>106</primitive_test_id>
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: Service Manager – Send a message HEX command (30 8F) to check the device power status and receive message from the cec device ( 03 90 00(off) or 03 90 01(on)) after enabling the cec.
Test Case Id: CT_Service Manager_48.
Test Type: Positive.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_Service Manager_48</test_case_id>
    <test_objective>Service Manager – Send a message HEX command (30 8F) to check the device power status and receive message from the cec device ( 03 90 00(off) or 03 90 01(on)) after enabling the cec.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite>Atleast one HDMI device must be connected and power state should be ON.</pre_requisite>
    <api_or_interface_used>bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName)
void setEnabled(bool true)
void sendMessage(Qstring message)
void onMessage( QString message )
bool unregisterService(const QString&amp; )</api_or_interface_used>
    <input_parameters>registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring – serviceName
setEnabled: bool false
sendMessage: Qstring message
onMessage: Qstring message
UnregisterService : Qstring-serviceName</input_parameters>
    <automation_approch>1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register a given hdmicec service with ServiceManager component.
3.On Success of registerService, Service_Manager_Agent will disable cec service.
4. On Success of enabling cec, Service_Manager_Agent will send message (30 8F) for a CEC device.
5. On Success of sending the message to the device, Service_Manager_Agent should recieve the message (03 90 00 or 03 90 01 ) as response from the device and when onMessage event will be called.
6 On Success of onMessage, Service_Manager_Agent will deregister a given service from ServiceManager component.


</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.

Checkpoint 2.Check for the message pattern for message sent in cec.txt.

Checkpoint 3.Compare the power status with the values (039000 -&gt; on, 039001 -&gt; off)  
</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so
</test_stub_interface>
    <test_script>SM_HdmiCec_SendMsgGetPowerStatus_CecEnabled</test_script>
    <skipped>No</skipped>
    <release_version>M25</release_version>
    <remarks>SM_HdmiCec_EnableCec_SendReceivePowerState changed to SM_HdmiCec_SendMsgGetPowerStatus_CecDisabled during M-29 release.</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import devicesettings;
import iarmbus;
import servicemanager;
from time import sleep;
from os import urandom
from binascii import b2a_hex

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

smObj.configureTestCase(ip,port,'"SM_HdmiCec_SendMsgGetPowerStatus_CecEnabled');
iarmObj.configureTestCase(ip,port,'"SM_HdmiCec_SendMsgGetPowerStatus_CecEnabled');

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
                        #Register HdmiCecService
			service_name = "com.comcast.hdmiCec_1"
			register = servicemanager.registerService(smObj,service_name)
			if "SUCCESS" in register:
                                #Enable the cec support setting it true.
				print "Set CEC Enabled"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SetEnabled');
                                expectedresult = "SUCCESS"
				valueToSetEnabled = 1
				print "setEnabled to ",valueToSetEnabled
				tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
                                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");

                                        #Sending the message to the connected device
	                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SendMessage');
	                                expectedresult = "SUCCESS"
                                        message = "30 8F 53 65 74 74 " + str(b2a_hex(urandom(1))).upper()
					print "Message to be sent to HDMI device: ",message
	                                tdkTestObj.addParameter("messageToSend",message);
	                                tdkTestObj.executeTestCase(expectedresult);
	                                actualresult = tdkTestObj.getResult();
	                                sendMsgDetails = tdkTestObj.getResultDetails();
        	                        print "[TEST EXECUTION DETAILS] : ",sendMsgDetails;
					if expectedresult in actualresult:
						tdkTestObj.setResultStatus("SUCCESS");

                                                #Wait for data to be printed to cec log
                                                sleep(70)

						#Check for the message sent for confirmation.
						tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckStatus');
						expectedresult = "SUCCESS"
						tdkTestObj.addParameter("pattern",message);
						tdkTestObj.executeTestCase(expectedresult);
	                                        actualresult = tdkTestObj.getResult();
        	                                patternDetails= tdkTestObj.getResultDetails();
                	                        print "[TEST EXECUTION DETAILS] : ",patternDetails;
						if expectedresult in actualresult:
							tdkTestObj.setResultStatus("SUCCESS");
							logpath=tdkTestObj.getLogPath();
							print "Log path : %s" %logpath;
							#tdkTestObj.transferLogs(logpath,"false");
							
							#Check for the reply from the Cec device.
							tdkTestObj = smObj.createTestStep('SM_RegisterForEvents');	
		                                        expectedresult = "SUCCESS"
                                                        expectedresult="SUCCESS"
                                                        event_name="onMessage";
                                                        tdkTestObj.addParameter("service_name",service_name);
                                                        tdkTestObj.addParameter("event_name",event_name);
                                                        tdkTestObj.executeTestCase(expectedresult);
                                                        actualresult= tdkTestObj.getResult();
                                                        if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                eventregisterdetail =tdkTestObj.getResultDetails(); 
                                                                print eventregisterdetail;
                                                                print "SUCCESS: Application succesfully executes SM_RegisterForEvents API";
                                                                sleep(70)
                                                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckStatus');
                		                                expectedresult = "SUCCESS"
                                                                #Assuming TV is on and should receive power state 039000
                                		                pattern = "03 90 00"
		                                                tdkTestObj.addParameter("pattern",pattern);
		                                                tdkTestObj.executeTestCase(expectedresult);
                		                                actualresult = tdkTestObj.getResult();
		                                                patternDetails= tdkTestObj.getResultDetails();
		                                                print "[TEST EXECUTION DETAILS] : ",patternDetails;
								if expectedresult in actualresult:
	                        	                                tdkTestObj.setResultStatus("SUCCESS");
        	                        	                        logpath=tdkTestObj.getLogPath();
                	                        	                print "Log path : %s" %logpath;
                        	                        	        #tdkTestObj.transferLogs(logpath,"false");
								else:
									tdkTestObj.setResultStatus("FAILURE");
									logpath=tdkTestObj.getLogPath();
									print "Log path : %s" %logpath;
									#tdkTestObj.transferLogs(logpath,"false");
                                                                tdkTestObj = smObj.createTestStep('SM_UnRegisterForEvents');
                                                                tdkTestObj.addParameter("service_name",service_name);
                                                                tdkTestObj.addParameter("event_name",event_name);
                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                actualresult= tdkTestObj.getResult();
                                                                #eventregisterdetail =tdkTestObj.getResultDetails();
                                                                #Check for SUCCESS/FAILURE return value of SM_RegisterForEvents
                                                                if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        eventregisterdetail =tdkTestObj.getResultDetails(); 
                                                                        print eventregisterdetail;
                                                                        print "SUCCESS: Application succesfully executes SM_UnRegisterForEvents API";
                                                                else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print "FAILURE: Application Failed to execute SM_UnRegisterForEvents API";

                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "FAILURE: Application Failed to execute SM_RegisterForEvents API";
                                                else:
							tdkTestObj.setResultStatus("FAILURE");
							logpath=tdkTestObj.getLogPath();
							print "Log path : %s" %logpath;
							#tdkTestObj.transferLogs(logpath,"false");	
					else:
						tdkTestObj.setResultStatus("FAILURE");
				else:
					tdkTestObj.setResultStatus("FAILURE");

				#Unregister hdmicec service
				unregister = servicemanager.unRegisterService(smObj,service_name)

                        #Calling IARM_Bus_DisConnect API
                        disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
