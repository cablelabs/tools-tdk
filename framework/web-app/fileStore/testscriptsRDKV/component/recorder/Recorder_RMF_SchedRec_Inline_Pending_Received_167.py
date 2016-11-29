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
  <name>Recorder_RMF_SchedRec_Inline_Pending_Received_167</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should send Pending status in a full sync when a future inline recording is scheduled</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_167</test_case_id>
    <test_objective>Check that recorder should send Pending status in a full sync when a future inline recording is scheduled</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1/Emu-hyb</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent / Python lib interface will frame the json message to schedule a future recording using inline mechanism and send to TDK Recorder Simulator server which is present in TM.
4. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM
5.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the response from recorder and verify that status=Pending has been sent for the recording from recorder.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_SchedRec_Inline_Pending_Received_167</test_script>
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
obj.configureTestCase(ip,port,'Recorder_RMF_SchedRec_Inline_Pending_Received_167');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        print "Rebooting box for setting configuration"
	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
	       sleep(300);
        print "Waiting for the recoder to be up"


        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        print "Sending noUpdate to get the recording list after full sync"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        sleep(10);
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        #print "Retrieve Status Details: %s"%response;

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #For full sync, schedule a small recording with 1 min duration and wait till it ends
        duration = "60000";
        startTime = "0";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
        print "serverResponse recording 1: %s" %serverResponse;
        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success for first recording before reboot";
                sleep(90);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('acknowledgement' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement for recording 1";
                        print "Reboot the box and schedule new recording 2";
                        obj.initiateReboot();
                        print "Waiting for the recoder to be up"
                        sleep(300);

                        #Execute updateSchedule
                        requestID2 = str(randint(10, 500));
                        recordingID2 = str(randint(10000, 500000));
                        # After reboot schedule Future Inline recording in order to get pending status
                        startTime2 = "60000";

                        # Keep checking the status for every 10sec, so calculate loop time in seconds: startTime + duration + 1min offset
                        endtime = (int(duration)/1000) + (int(startTime2)/1000) + 30;
                        print('Wait time: '+str(endtime));

                        #Frame json message
                        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
                        print "serverResponse recording 2 after reboot: %s" %serverResponse;
                        if "updateSchedule" in serverResponse:
                                print "updateSchedule message post success for second recording after reboot";
                                ackflag = 0;
                                pendingflag = 0;

                                while (endtime > 0):
                                        sleep(10);
                                        print "Sending getRecordings to get the recording list"
                                        recorderlib.callServerHandler('clearStatus',ip)
                                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                        print "Wait for 60 seconds to get response from recorder"
                                        sleep(60)
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                        print recResponse

                                        if ('acknowledgement' in recResponse):
                                                ackflag = 1;

                                        recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID2);
                                        print recordingData
                                        if ('NOTFOUND' not in recordingData):
                                                key = 'status'
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                                print "key: ",key," value: ",value
                                                if "PENDING" in value.upper():
                                                        print "Recorder has sent status = Pending";
                                                        pendingflag = 1;
                                                        break;

                                        endtime = endtime - 10;

                                print "Retrieve Status Details: ",recResponse;
                                print "Printing recording data:";
                                print recordingData;

                                if (ackflag == 0):
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Simulator Server failed to receive acknowledgement from recorder";
                                elif (pendingflag == 0):
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder has not sent pending status";
                                else:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Acknowledgement received and also recorder has sent pending status";
        else:
                print "updateSchedule message post failed for first recording before reboot";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");

