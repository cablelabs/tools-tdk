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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_GenerationId_Preserve_Across_reboot_17</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder- To preserve generation Id across reboot in normal case</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <!--  -->
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
import recorderlib
from random import randint
from time import sleep
#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Preserve_Across_reboot_17');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper())
#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
        sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        requestID = str(randint(10,500));
	genIdInput = "test3a";

        #Frame json message
        jsonMsg = "{\"noUpdate\":{\"generationId\":\""+genIdInput+"\"}}";
        expResponse = "noUpdate";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "noUpdate message post success";
                tdkTestObj.executeTestCase(expectedResult);

        	#Primitive test case which associated to this script
	        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        	expectedResult="SUCCESS";

		#reboot the stb and check for persistency.
        	recObj.initiateReboot();

		print "Sleeping to wait for the recoder to be up"
        	sleep(300);

	        #Primitive test case which associated to this script
	        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        	expectedResult="SUCCESS";

        	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\"}}";

	        expResponse = "updateSchedule";
	        tdkTestObj.executeTestCase(expectedResult);
	        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        	if expResponse in actResponse:
                	tdkTestObj.setResultStatus("SUCCESS");
	               	print "updateSchedule message post success";
                	tdkTestObj.executeTestCase(expectedResult);
			genOut = recorderlib.readGenerationId(ip)
		    	if genOut == genIdInput:
                            tdkTestObj.setResultStatus("SUCCESS");
	                    print "GenerationId matches with the expected one";
		        else:
        	            tdkTestObj.setResultStatus("FAILURE");
                	    print "GenerationId does not match with the expected one";
		else:
                	tdkTestObj.setResultStatus("FAILURE");
	               	print "updateSchedule message post failure";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "noUpdate message post failure";

        recObj.unloadModule("Recorder");
