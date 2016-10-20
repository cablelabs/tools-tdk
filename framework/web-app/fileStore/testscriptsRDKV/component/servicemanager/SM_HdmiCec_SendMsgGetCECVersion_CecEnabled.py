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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HdmiCec_SendMsgGetCECVersion_CecEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>106</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_RegisterService</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: Service Manager – Send message to the STB device with enabling CEC.
Test Case Id: CT_Service Manager_40.
Test Type: Positive.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
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

smObj.configureTestCase(ip,port,'SM_HdmiCec_SendMsgGetCECVersion_CecEnabled');
iarmObj.configureTestCase(ip,port,'SM_HdmiCec_SendMsgGetCECVersion_CecEnabled');

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
			#Create HdmiCecService instance 1 
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
					
					#Set the device Name.
	                                tdkTestObj = smObj.createTestStep('SM_HdmiCec_SendMessage');
	                                expectedresult = "SUCCESS"
					message = "30 9F 53 65 74 74 " + str(b2a_hex(urandom(1))).upper()
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
						else:
							tdkTestObj.setResultStatus("FAILURE");
							logpath=tdkTestObj.getLogPath();
							print "Log path : %s" %logpath;
							#tdkTestObj.transferLogs(logpath,"false");	
					else:
						tdkTestObj.setResultStatus("FAILURE");
				else:
					tdkTestObj.setResultStatus("FAILURE");

                                #Delete HdmiCecService instance 1
                                unregister = servicemanager.unRegisterService(smObj,service_name)

                        #Calling IARM_Bus_DisConnect API
                        disconnect=iarmbus.IARMBUS_DisConnect(iarmObj,'SUCCESS')
                term=iarmbus.IARMBUS_Term(iarmObj,'SUCCESS')

        #Unload the modules
        smObj.unloadModule("servicemanager");
        iarmObj.unloadModule("iarmbus");
