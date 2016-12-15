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
  <name>SM_HdmiCec_SendAbortMsg_CecDisabled</name>
  <primitive_test_id>106</primitive_test_id>
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: Service Manager – Send a random message and receive message to and from the cec device after disabling the cec.
Test Case Id: CT_Service Manager_47.
Test Type: Negative.</synopsis>
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
    <test_case_id>CT_Service Manager_47</test_case_id>
    <test_objective>Service Manager – Send a random message and receive message to and from the cec device after disabling the cec.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite>Atleast one HDMI device must be connected.</pre_requisite>
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
4. On Success of disabling cec, Service_Manager_Agent will send message for a CEC device.
5. On Success of sending the message to the device, Service_Manager_Agent should recieve the message as response from the device and when onMessage event will be called.
6 On Success of onMessage, Service_Manager_Agent will deregister a given service from ServiceManager component.


</automation_approch>
    <except_output>Checkpoint 1.Check the return value of APIs for success status.

Checkpoint 2.Check for the message pattern for message sent in cec.txt.
</except_output>
    <priority>High</priority>
    <test_stub_interface>libservicemanagerstub.so
</test_stub_interface>
    <test_script>SM_HdmiCec_SendAbortMsg_CecDisabled</test_script>
    <skipped>No</skipped>
    <release_version>M25</release_version>
    <remarks>SM_HdmiCec_DisableCec_SendReceiveMsg changed to SM_HdmiCec_SendAbortMsg_CecDisabled during M-29 release</remarks>
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
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

smObj.configureTestCase(ip,port,'SM_HdmiCec_SendAbortMsg_CecDisabled');
iarmObj.configureTestCase(ip,port,'SM_HdmiCec_SendAbortMsg_CecDisabled');

#Get the result of connection with test component and STB
smLoadStatus = smObj.getLoadModuleResult();
print "[servicemanager LIB LOAD STATUS]  :  %s" %smLoadStatus;
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[iarmbus LIB LOAD STATUS]  :  %s" %iarmLoadStatus;
#Set the module loading status
smObj.setLoadModuleStatus(smLoadStatus.upper());
iarmObj.setLoadModuleStatus(iarmLoadStatus.upper());

if "SUCCESS" in smLoadStatus.upper() and "SUCCESS" in iarmLoadStatus.upper():

	service_name = "com.comcast.hdmiCec_1"

	register = servicemanager.registerService(smObj,service_name)
        if "SUCCESS" in register:

                #Calling IARM Bus Init
		init=iarmbus.IARMBUS_Init(iarmObj,'SUCCESS')
		if "SUCCESS" in init:
			connect=iarmbus.IARMBUS_Connect(iarmObj,'SUCCESS')
			if "SUCCESS" in connect:

                                #Enable the cec support setting it false
				print "Set CEC Disabled"
                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SetEnabled');
                                expectedresult = "SUCCESS"
				valueToSetEnabled = 0
				tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                setEnabledDetails = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : ",setEnabledDetails;
                                if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
					
					#Set the abort opcode
	                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SendMessage');
	                                expectedresult = "SUCCESS"
					#Send the random message.
                                        message = "30 FF 00 FF FF FF " + str(b2a_hex(urandom(1))).upper()
                                        print "Message to be sent to HDMI device: ",message
	                                tdkTestObj.addParameter("messageToSend",message);
	                                tdkTestObj.executeTestCase(expectedresult);
	                                actualresult = tdkTestObj.getResult();
	                                sendMsgDetails = tdkTestObj.getResultDetails();
        	                        print "[TEST EXECUTION DETAILS] : ",sendMsgDetails;
					if expectedresult in actualresult:
						tdkTestObj.setResultStatus("SUCCESS");
	
						sleep(70)

						#Check for the message sent for confirmation.
						tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckStatus');
						expectedresult = "FAILURE"
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
							#tdkTestObj = smObj.createTestStep('SM_HdmiCec_OnMessage');	
		                                        #expectedresult = "SUCCESS"
		                                        #TODO: Need confirmation from Devlopement team.  Assuming to receive INVALID.
                		                        #onMessage = "INVALID"
	                                	        #tdkTestObj.addParameter("onMessage",onMessage);
        	                                	#tdkTestObj.executeTestCase(expectedresult);
	                	                        #actualresult = tdkTestObj.getResult();
        	                	                #onMsgDetails = tdkTestObj.getResultDetails();
                	                	        #print "[TEST EXECUTION DETAILS] : ",onMsgDetails;
							#if expectedresult in actualresult:
							#	tdkTestObj.setResultStatus("SUCCESS");
							#	sleep(5)
							#
							#	#Check for the message sent for confirmation.
		                                        #        tdkTestObj = smObj.createTestStep('SM_HdmiCec_CheckStatus');
                		                        #        expectedresult = "FAILURE"
                                		        #        pattern = "INVALID"
		                                        #        tdkTestObj.addParameter("pattern",pattern);
		                                        #        tdkTestObj.executeTestCase(expectedresult);
                		                        #        actualresult = tdkTestObj.getResult();
		                                        #        patternDetails= tdkTestObj.getResultDetails();
		                                        #        print "[TEST EXECUTION DETAILS] : ",patternDetails;
							#	if expectedresult in actualresult:
	                        	                #                tdkTestObj.setResultStatus("SUCCESS");
        	                        	        #                logpath=tdkTestObj.getLogPath();
                	                        	#                print "Log path : %s" %logpath;
                        	                        #	        #tdkTestObj.transferLogs(logpath,"false");
							#	else:
							#		tdkTestObj.setResultStatus("FAILURE");
							#		logpath=tdkTestObj.getLogPath();
							#		print "Log path : %s" %logpath;
							#		#tdkTestObj.transferLogs(logpath,"false");
							#else:
							#	tdkTestObj.setResultStatus("FAILURE");
						else:
							tdkTestObj.setResultStatus("FAILURE");
							logpath=tdkTestObj.getLogPath();
							print "Log path : %s" %logpath;
							#tdkTestObj.transferLogs(logpath,"false");	
					else:
						tdkTestObj.setResultStatus("FAILURE");
				else:
					tdkTestObj.setResultStatus("FAILURE");

                                #Calling IARM_Bus_DisConnect API
                                disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                        term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

                #Unregister hdmicec service
		unregister = servicemanager.unRegisterService(smObj,service_name)

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
