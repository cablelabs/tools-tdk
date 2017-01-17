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
  <name>Recorder_RMF_Update_Deletion_Priority_Cancel_Rec_Inline_449</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recording field values should persist after cancelling a recording which was updated to priority p1</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_449</test_case_id>
    <test_objective>Recorder should persist the recording field values after cancelling a inline recording which was updated to priority P1.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of stt_received and stage4 in /tmp path of device.
4. In rmfconfig.ini file the parameters FEATURE.LONGPOLL.URL,FEATURE.RWS.GET.URL and FEATURE.RWS.POST.URL should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.Schedule a hot inlineP4 recording of 4 minutes duration
3.Update the recording priority to P1 from P4
4.Cancel the recording with fullSchedule as false
5.Check the cancelled recording details from the response received in RWS after cancelling the recording.
6.Check the recording details using getRecordings message also.
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check whether fields are updated for the specified recording Id.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Update_Deletion_Priority_Cancel_Rec_Inline_449</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Update_Deletion_Priority_Cancel_Rec_Inline_449');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
            print "Rebooting box for setting configuration"
            recObj.initiateReboot();
            print "Waiting for 5min for the recoder to be up"
	    sleep(300);
        
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "240000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
                loop = 0;
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (('ack' not in actResponse) and (loop < 5)):
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    sleep(10);
                    loop = loop+1;
                print "Retrieve Status Details: ",actResponse;
		if 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received Empty/Error statussss";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    print "Wait for the recording to be completed partially"
                    sleep(60);
                    #Frame json message for update recording priority to P1
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P1\"}]}}";

                    expResponse = "updateRecordings";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgUpdateRecording,ip);
                    print "updateRecordings Details: %s"%actResponse;
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateRecordings message post success";
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        while (('ack' not in actResponse) and (loop < 5)):
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                            sleep(10);
                            loop = loop+1;
                        print "Retrieve Status Details: ",actResponse;
			if 'acknowledgement' not in actResponse:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Received Empty/Error status";
                        elif 'acknowledgement' in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                            sleep(60);
                            #Frame json message for cancel recording
                            jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":false,\"cancelRecordings\":[\""+recordingID+"\"]}}";

                            expResponse = "updateSchedule";
                            tdkTestObj.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgCancelRecording,ip);
                            sleep(30);
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording data notified to RWS: %s" %actResponse;
                            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                            print recordingData
                            if 'NOTFOUND' not in recordingData:
                                status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                error = recorderlib.getValueFromKeyInRecording(recordingData,'error')
                                deletePriority = recorderlib.getValueFromKeyInRecording(recordingData,'deletePriority')
                                if "INCOMPLETE" in status.upper() and "USER_STOP" in error.upper() and "P1" in deletePriority.upper():
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Recording field notified to RWS has expected values"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording field notified to RWS has Unexpected values"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to retrieve the recording list from recorder";
                            recorderlib.callServerHandler('clearStatus',ip)
                            recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                            print "Wait for 60 seconds to get response from recorder"
                            sleep(60)
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording data from getRecordings: %s" %actResponse;
                            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                            print recordingData
                            if 'NOTFOUND' not in recordingData:
                                status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                error = recorderlib.getValueFromKeyInRecording(recordingData,'error')
                                deletePriority = recorderlib.getValueFromKeyInRecording(recordingData,'deletePriority')
                                if "INCOMPLETE" in status.upper() and "USER_STOP" in error.upper() and "P1" in deletePriority.upper():
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Recording field has expected values"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording field has Unexpected values"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to retrieve the recording list from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
