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
  <version>1</version>
  <name>Recorder_RMF_GenerationId_Inline_UpdateRecording_12</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder accepts Generation ID via inline updateRecordings</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_12</test_case_id>
    <test_objective>Recorder- To accept  Generation ID via inline updateRecordings</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to 
  RecorderAgent to generate request url.
3.RecorderAgent/Python lib interface will frame the json message to simulate a 
  longpoll notification with an inline "updateRecordings" payload containing "generationId": "test1b"
  and send to TDK Recorder Simulator server which is present in TM.
4.STB (Recorder) makes a POST request to RWS bearing HTTP header "X-Parker-Generation-ID: test1b" (CP).
5.Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
8.RecorderAgent/Python lib interface will frame the json message to simulate a legacy longpoll notification 
  (no inline payload, only RWS GET URL).
9.STB (Recorder) makes a GET request to RWS bearing HTTP header "X-Parker-Generation-ID: test1b" (CP)</automation_approch>
    <except_output>Checkpoint : Acknowledgement status from the DVRSimulator AND value of generationId from http header at step 4 and 9</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_GenerationId_Inline_UpdateRecording_12</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
