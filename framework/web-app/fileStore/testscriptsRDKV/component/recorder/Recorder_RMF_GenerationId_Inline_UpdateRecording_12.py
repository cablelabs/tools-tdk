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
  <name>Recorder_RMF_GenerationId_Inline_UpdateRecording_12</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder accepts Generation ID via inline updateRecordings</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Inline_UpdateRecording_12');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
	       print "Waiting for the recoder to be up"
	       sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
	expectedResult="SUCCESS";
	tdkTestObj.executeTestCase(expectedResult);

	#STEP1: SCHEDULE FOR A RECORDING
        requestID = str(randint(10, 5500));
        recordingID = str(randint(10000, 550000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
        genIdInput = "test_1_b";

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

        if expResponse in actResponse:
                print "Inline updateSchedule message post success";
                print "Waiting to get status"
                sleep(120);
                genOut = recorderlib.readGenerationId(ip)
                if genOut == genIdInput:
                                print "GenerationId (%s) matches with expected value(%s)"%(genIdInput,genOut);
				#STEP2: WAIT FOR RECORDING TO COMPLETE AND GET THE RECORDING STATUS
				response = recorderlib.callServerHandler('clearStatus',ip);
                                print "Wait for 60s for the recording to be completed"
                                sleep(60);
                                jsonMsgNoUpdate = "{\"updateSchedule\":{\"generationId\":\"0\"}}";
                                actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                                sleep(60);
                                print "Sending getRecordings to get the recording list"
                                recorderlib.callServerHandler('clearStatus',ip);
				recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                print "Wait for 60 seconds to get response from the recorder"
                                sleep(60);
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                                print recordingData
                                if 'NOTFOUND' not in recordingData:
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        print "Successfully retrieved the recording list from recorder"
                                        if "COMPLETE" in value.upper():
                                                print "Scheduled recording completed successfully";
				                #STEP3: SEND inline "updateRecordings" payload containing "generationId": "test1bb AND EXPECT "generationId": "test1b"
                                                genIdInput = "test1b";
                                                jsonMsg = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"requestId\":\""+requestID+"\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P2\",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"}}]}}";
                                                expResponse = "updateRecordings";
                                                actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
                                                print "Update Recordings Details: %s"%actResponse;

                                                if expResponse in actResponse:
                                                        print "update recordings message post success";
                                                        print "Waiting to get status"
                                                        sleep(120);
                                                        genOut = recorderlib.readGenerationId(ip)
                                                        if genOut == genIdInput:
							        print "GenerationId (%s) matches with expected value(%s)"%(genIdInput,genOut);
								#STEP4: RWS "updateSchedule" without generationId and expect genId="test1b"
                                                                jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\"}}";
                                                                expResponse = "updateSchedule";
                                                                actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
                                                                print "Update Schedule Details: %s"%actResponse;
                                                                if expResponse in actResponse:
                                                                    print "updateSchedule message post success";
                                                                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
				                                    print "Step4: Retrieve Status Details: %s"%actResponse;
                                                                    genOut = recorderlib.readGenerationId(ip)
								    if genOut == genIdInput:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
									print "GenerationId (%s) matches with expected value(%s)"%(genIdInput,genOut);
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
									print "GenerationId does not match with expected value";
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                    print "updateSchedule message post failure";
				                        else:
							    tdkTestObj.setResultStatus("FAILURE");
							    print "GenerationId does not match with expected value";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "update recordings message post failure";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Scheduled recording not completed successfully";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to retrieve the recording list from recorder";
		else:
		        tdkTestObj.setResultStatus("FAILURE");
			print "GenerationId does not match with expected value";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Inline updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
