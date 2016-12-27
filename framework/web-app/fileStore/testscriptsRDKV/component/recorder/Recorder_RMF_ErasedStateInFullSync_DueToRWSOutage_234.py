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
  <version>2</version>
  <name>Recorder_RMF_ErasedStateInFullSync_DueToRWSOutage_234</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should include in full sync any recordings that are deleted by user but not previously notified due to RWS outage</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_234</test_case_id>
    <test_objective>To verify if recorder includes in full sync any recordings that are deleted by user but not previously notified due to RWS outage</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. TM loads RecorderAgent via the test agent.
2. TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3. RecorderAgent / Python lib interface will frame the json message to schedule a hot P3 recording of 1min duration using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4. Wait for 1 minute for recording to complete.
5. Disable RWS status server and RWS server
6. Delete the recording
7. Reboot the STB for getting full sync message from recorder
8. Once STB is up, restore RWS status server and RWS server
9. Wait for 60s for recorder to connect to RWS
10. Fetch recording list after full sync
11. Verify that deleted recording is in ERASED state as expected
12. Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>CheckPoint:
1. Recorder should send acknowledgement for updateSchedule request
2. Recorder should send status of deleted recording as ERASED</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_ErasedStateInFullSync_DueToRWSOutage_234</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
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
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_ErasedStateInFullSync_DueToRWSOutage_234');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recorder to be up"
	       sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Prmitive test case which associated to this Script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #Recording with 1 min duration
        duration = "60000";
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (('statusMessage' not in recResponse) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if 'statusMessage' in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        print "Wait for 60s for recording to complete";
                        sleep(70)
                 
                        #Disable RWS status server
                        recorderlib.callServerHandlerWithType('disableServer','RWSStatus',ip)
                        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSStatus',ip)
                        print "RWSStatus server status: ",status

                        #Disable RWS server
                        recorderlib.callServerHandlerWithType('disableServer','RWSServer',ip)
                        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
                        print "RWSserver status: ",status
              
                        print "Wait for recorder to start connection retries"
                        sleep(60)

                        recResponse = recorderlib.callServerHandler('clearStatus',ip);
                        print "Delete the recording...";
                        #Frame json message for update recording
                        requestID = str(randint(10, 500));
                        jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";
                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
                        if "updateRecordings" in actResponse:
                                print "updateRecordings message post success";
                                #Wait for 60s and retrieve status - expect no response 
                                sleep(60);
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print "Retrieve Status with RWS down: ",recResponse;
                                if 'statusMessage' in recResponse:
                                        print "Simulator received response with RWS down"
                                        tdkTestObj.setResultStatus("FAILURE");
                                else:
                                        print "Recorder did not send recordingStatus notification to the RWS for deleted recording"
                                        print "Restore RWS"
                                        #Enable RWS status server
                                        recorderlib.callServerHandlerWithType('enableServer','RWSStatus',ip)
                                        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSStatus',ip)
                                        print "RWSStatus server status: ",status

                                        #Enable RWS server
                                        recorderlib.callServerHandlerWithType('enableServer','RWSServer',ip)
                                        status = recorderlib.callServerHandlerWithType('isEnabledServer','RWSServer',ip)
                                        print "RWSserver status: ",status

                                        #wait for 60s for recorder to connect to rws
                                        sleep(60)
                                        print "Rebooting STB for full sync"
                                        recObj.initiateReboot();
                                        print "Waiting for the recorder to be up"
                                        sleep(300)

                                        print "Sending noUpdate to get the recording list after full sync"
                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip)
                                        sleep(60)
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Recording List: ",recResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                        if ('NOTFOUND' not in recordingData):
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                print "recordingID: ",recordingID," status: ",value
                                                #Recording should be there untill any space requirement arises
                                                if "COMPLETE" in value.upper():
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "Recording is in COMPLETE state as expected";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Recording is not in COMPLETE state";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder did not update recording list with deleted recording";

                                        # Test start -- Full Sync not working
                                        recResponse = recorderlib.callServerHandler('clearStatus',ip);
                                        print "Sending getRecordings to get the recording list"
                                        jsonMsgGetRec = "{\"getRecordings\":{}}";
                                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgGetRec,ip);
                                        sleep(30)
                                        retry = 0
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        while (('statusMessage' not in recResponse) and (retry < 10 )):
                                                sleep(20);
                                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                retry += 1
                                        print "Recording List: ",recResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                        print "RecordingData from getRecordings: " ,recordingData
                                        if ('NOTFOUND' not in recordingData):
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                print "recordingID: ",recordingID," status: ",value
                                                #Recording should be there untill any space requirement arises
                                                if "COMPLETE" in value.upper():
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "Recording is in COMPLETE state as expected";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Recording is not in COMPLETE state";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder did not update recording list with deleted recording";
                                        # Test end
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateRecordings message post failed";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server did not receive recorder acknowledgement";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failed";

        #Post-requisite
        recorderlib.callServerHandlerWithType('enableServer','RWSStatus',ip)
        recorderlib.callServerHandlerWithType('enableServer','RWSServer',ip)
        #unloading Recorder module
        recObj.unloadModule("Recorder");
