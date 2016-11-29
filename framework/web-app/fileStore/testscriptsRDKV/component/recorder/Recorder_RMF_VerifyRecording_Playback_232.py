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
  <name>Recorder_RMF_VerifyRecording_Playback_232</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify successful playback of recorded content</synopsis>
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
    <test_case_id>CT_Recoder_DVR_Protocol_232</test_case_id>
    <test_objective>To verify successful playback of recorded content</test_objective>
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
3. RecorderAgent / Python lib interface will frame the json message to send request message to TDK Recorder Simulator server which is present in TM.
4. STB will be rebooted after a sleep of recording duration.
5. Legacy updateSchedule message will be sent to TDK Recorder Simulator to start a new recording.
6. Once acknowledgment is received, wait for recording to complete
7. getRecordings request will be send to TDK Recorder Simulator to check the completion status of the recordings
8. Once the verification is complete, initiate dvr playback using TDKIntegrationStub  
9. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
10. Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>CheckPoint:
1. Recorder should send acknowledgement for updateSchedule request
2. Recorder should send complete recording list in response to getRecordings request
3. The recording should be completed without any issues.
4. Recording playback should be successful.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_VerifyRecording_Playback_232</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import recorderlib
from random import randint
from time import sleep
from tdkintegration import dvr_playback;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_VerifyRecording_Playback_232');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus ;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

recordingSuccess = 'FALSE'
recordingID = str(randint(10000, 500000))

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
               sleep(300);

        #Primitive test case which associated to this Script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        #2mins duration
        duration = "120000"
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while ( ('acknow' not in recResponse) and (retry < 10 ) ):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknow" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        response = recorderlib.callServerHandler('clearStatus',ip)
                        print "Wait for 2 min for recording to complete"
                        sleep(120)
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        print "Wait for 1 min to get response from recorder"
                        sleep(60)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse;
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                        print recordingData
                        if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get recording info"
                        else:
                                reqRecording = {"recordingId":recordingID,"duration":120000,"deletePriority":"P3"}
                                ret = recorderlib.verifyCompletedRecording(recordingData,reqRecording)
                                if "FALSE" in ret:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording failed verification"
                                else:
                                        recordingSuccess = 'TRUE'
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recording passed verification"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");

if 'TRUE' == recordingSuccess:
        # Playback the recorded content
        tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
        tdkIntObj.configureTestCase(ip,port,'Recorder_RMF_VerifyRecording_Playback_232');
        tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
        print "TDKINTEGRATION module loading status : %s" %tdkIntLoadStatus;
        #Set the module loading status
        tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

        #Check for SUCCESS/FAILURE of tdkintegration module
        if "SUCCESS" in tdkIntLoadStatus.upper():

                #Primitive test case which associated to this script
                tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
                result = dvr_playback(tdkTestObj,recordingID);

                if "SUCCESS" in result.upper():
                        print "Recording playback Success"
                else:
                        print "Recording playback Failed"

                #unloading tdkintegration module
                tdkIntObj.unloadModule("tdkintegration");
else:
        print "Skipping playback for failed recording"
