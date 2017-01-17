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
  <name>Recorder_RMF_Cancel_Erased_Rec_Inline_443</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should not change the status when cancelling a recording which is end with ERASED</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_443</test_case_id>
    <test_objective>Recorder should not change the status when cancelling a legacy recording which is end with status ERASED</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of stt_received and stage4 in /tmp path of device.
4. In rmfconfig.ini file the parameters FEATURE.LONGPOLL.URL,FEATURE.RWS.GET.URL and FEATURE.RWS.POST.URL should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.Schedule a future inline recording of 5 minute duration with 3 minutes start time
3.Schedule a hot recording 1 minute duration with fullSchedule values as true
4.Check whether the recording in step 2 is ERASED or not.
5.Sent json message to cancel the recording
6.Check whether recorder has changed the status of recording from ERASED to some other status
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Recording details should be available as expected</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Cancel_Erased_Rec_Inline_443</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Cancel_Erased_Rec_Inline_443');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);
	print "Sleeping to wait for the recoder to be up"

        
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
        duration = "60000";
	longDuration = "300000";
        startTime = "0";
        futureStartTime = "180000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        futureOcapId = tdkTestObj.getStreamDetails('02').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+futureOcapId+"\"],\"epoch\":"+now+",\"start\":"+futureStartTime+",\"duration\":"+longDuration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

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
                    print "Received Empty/Error status";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
		    print "Successfully retrieved acknowledgement from recorder";
                    sleep(30);

                    #Frame json message for update recording
                    jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+str(int(requestID)+1)+"\",\"generationId\":\"TDK123\",\"fullSchedule\":true,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                    expResponse = "updateSchedule";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgCancelRecording,ip);
                    sleep(30);
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    print actResponse
                    recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
	            print recordingData
                    if 'NOTFOUND' not in recordingData:
            	        key = 'error'
			statusKey = 'status'
                	value = recorderlib.getValueFromKeyInRecording(recordingData,key)
			statusValue = recorderlib.getValueFromKeyInRecording(recordingData,statusKey)
                        print "key: ",key," value: ",value
			print "statusKey: ",statusKey," statusValue: ",statusValue
                        print "Successfully retrieved the recording list from recorder";
			if "USER_STOP" in value.upper() and "ERASED" in statusValue.upper():
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Cancelled future recording successfully";
                        elif "BADVALUE" in value.upper() and "BADVALUE" not in statusValue.upper():
                            tdkTestObj.setResultStatus("FAILURE");
                            print "No error/status field in recording status";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to cancel future recording/Status received as Erased";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to retrieve the recording list from recorder";	
                   
                    response = recorderlib.callServerHandler('clearStatus',ip);
                    #Frame json message for update recording
                    jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":false,\"cancelRecordings\":[\""+recordingID+"\"]}}";

                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgCancelRecording,ip);
                    sleep(30);
                    recorderlib.callServerHandler('clearStatus',ip)
                    recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                    print "Wait for 60 seconds to get response from recorder"
                    sleep(60)
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                    print "Recording List: %s" %actResponse;
                    recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                    print recordingData
                    if 'NOTFOUND' not in recordingData:
                        status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                        if "ERASED" in status.upper():
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "ERASED Status NOT changed";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "ERASED status changed";
                    else:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "ERASED recordings are not available";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
