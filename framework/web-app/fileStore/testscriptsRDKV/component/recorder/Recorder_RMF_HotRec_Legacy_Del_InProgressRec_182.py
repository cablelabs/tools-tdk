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
  <name>Recorder_RMF_HotRec_Legacy_Del_InProgressRec_182</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should include in full sync hot legacy recording which is in progress that are deleted by user but not previously notified to RWS with Status=Erased</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_182</test_case_id>
    <test_objective>After deleting a on-going hot legacy recording, check that recorder has sent status=Erased in a full sync</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent / Python lib interface will frame the json message to schedule a hot recording using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM
5.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the response from recorder and verify that status=Erased has been sent for the recording from recorder in a full sync.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_HotRec_Legacy_Del_InProgressRec_182</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_HotRec_Legacy_Del_InProgressRec_182');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        print "Rebooting box for setting configuration"
	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
	       sleep(300);
        print "Waiting for the recorder to be up"


        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        print "Sending noUpdate to get the recording list after full sync"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #Schedule Hot Inline Recording with 5 min duration
        duration = "300000";
        startTime = "0";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success 1";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('acknowledgement' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        sleep(30);

			#Cancel recording before deleting it
			jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"cancelRecordings\":[\""+recordingID+"\"]}}";
			actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgCancelRecording,ip);
			print "updateSchedule Details for CancelRecording: %s"%actResponse;
			sleep(30);

                        print "Delete the recording";
                        #Frame json message for update recording
                        jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";
                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
                        print "updateRecordings Details: %s"%actResponse;
                        if "updateRecordings" in actResponse:
                                print "updateRecordings message post success";
                                sleep(30);
                                print "Sending getRecordings to get the recording list"
                                recorderlib.callServerHandler('clearStatus',ip)
                                recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                                print "Wait for 1 min to get response from recorder"
                                sleep(60)
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                print recordingData
                                if ('NOTFOUND' not in recordingData):
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        if "INCOMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recorder has sent status = INCOMPLETE";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has not INCOMPLETE";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording details Not found "
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateRecordings message post failed";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server NOT received the recorder acknowledgement";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failed 1";

        #unloading Recorder module
        obj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");

