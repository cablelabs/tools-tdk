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
  <name>Recorder_RMF_RecEndedLate_Incomplete_Legacy_224</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder must send Error=ENDED_LATE if actual end varies more than 30 seconds</synopsis>
  <groups_id/>
  <execution_time>100</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_224</test_case_id>
    <test_objective>Check that Recorder sends Error=ENDED_LATE if actual end varies more than 30 seconds</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request URL.
3.RecorderAgent/Python lib interface will frame the json message to schedule the current recording of 5 minutes and send 
  to TDK Recorder Simulator server which is present in TM.
4.Wait for the recording to complete partially (1 minute).
5.RecorderAgent/Python lib interface will frame the json message to schedule the current recording of 15 seconds with the same 
  recording id as before and send to TDK Recorder Simulator server which is present in TM.
6.Recording will stop immediately.
7.Reboot STB.
8.noUpdate schedule message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
10.Check the status of the recording, it should be INCOMPLETE and error should be set to ENDED_LATE.
11.Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
12.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM."</automation_approch>
    <except_output>Checkpoint Get the response from recorder and verify that status has been received in full sync after the reboot for the recording and verify the expected status and error.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_RecEndedLate_Incomplete_Legacy_224</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import recorderlib
from sys import exit
from random import randint
from time import sleep
#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_RecEndedLate_Incomplete_Legacy_224');
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
        #print "Sleeping to wait for the recoder to be up"


        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
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
        requestID = str(randint(10,500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";
	genIdInput = recordingID;

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse not in actResponse:
        	tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failure";
                recObj.unloadModule("Recorder");
                exit();
        print "updateSchedule message post success";
        tdkTestObj.executeTestCase(expectedResult);
        print "Waiting to get acknowledgment status"
        sleep(10);
        retry=0
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
        while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
        	sleep(10);
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry += 1
        print "Retrieve Status Details: %s"%actResponse;
        if (('ERROR' in actResponse)):
                tdkTestObj.setResultStatus("FAILURE");
                print "Received Empty/Error status";
                recObj.unloadModule("Recorder");
                exit();
        print "Received status";
        if 'acknowledgement' not in actResponse:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve acknowledgement from recorder";
                recObj.unloadModule("Recorder");
                exit();
        print "Successfully retrieved acknowledgement from recorder";
        print "Wait for the recording to complete partially "
        sleep(30);
	#Now send one more update schedule to change the duration of the recording, i.e set it to 15 seconds
        duration = "120000";

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "updateRecordings Details: %s"%actResponse;
        if expResponse not in actResponse:
                tdkTestObj.setResultStatus("FAILURE");
                print "updateRecordings message post failure";
                recObj.unloadModule("Recorder");
                exit();
        print "updateRecordings message post success";
        tdkTestObj.executeTestCase(expectedResult);
        print "Waiting to get acknowledgment status"
        sleep(10);
        retry=0
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
        while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
                sleep(10);
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry += 1
        print "Retrieve Status Details: %s"%actResponse;
        if (('ERROR' in actResponse)):
                tdkTestObj.setResultStatus("FAILURE");
                print "Received Empty/Error status";
                recObj.unloadModule("Recorder");
                exit();
        print "Received status";
        if 'acknowledgement' not in actResponse:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve acknowledgement from recorder";
                recObj.unloadModule("Recorder");
                exit();
        print "Successfully retrieved acknowledgement from recorder";
        print "Wait for 180s for the recording to be completed"
	sleep(180);		 
	tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj1.executeTestCase(expectedResult);
        print "Sending getRecordings to get the recording list"
        recorderlib.callServerHandler('clearStatus',ip)
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 60 seconds to get response from recorder"
        sleep(60)
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recording List: %s" %actResponse;
        msg = recorderlib.getStatusMessage(actResponse);
        print "Get Status Message Details: %s"%msg;
        if "" == msg:
                value = "FALSE";
                print "No status message retrieved"
                tdkTestObj1.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Retrieved status message";
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print recordingData
        if 'NOTFOUND' in recordingData:
                tdkTestObj1.setResultStatus("FAILURE");
                print "Failed to get the recording data";
                recObj.unloadModule("Recorder");
                exit();
        print "Successfully retrieved the recording data";
        key = 'status'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
        print "key: ",key," value: ",value
        if "" == value.upper():
                print "Recording status not set";
                tdkTestObj1.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Recording status set";
        if "INCOMPLETE" not in value.upper():
                tdkTestObj1.setResultStatus("FAILURE");
                print "Recording not marked as INCOMPLETE";
                recObj.unloadModule("Recorder");
                exit();
        print "Recording marked as INCOMPLETE ";
	key = 'error'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
        print "key: ",key," value: ",value
        if "" == value.upper():
                print "Recording error not set";
                tdkTestObj1.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Recording error set";
        if "ENDED_LATE" not in value.upper():
                tdkTestObj1.setResultStatus("FAILURE");
                print "error not marked as ENDED_LATE";
                recObj.unloadModule("Recorder");
                exit();
        print "error marked as ENDED_LATE";         
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
	print "Failed to load Recorder module";
        #Set the module loading status
        recObj.setLoadModuleStatus("FAILURE");
