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
  <name>Recorder_RMF_UpdateRecording_WithNoRecordingProperties_233</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify state of recording after updating with no recording properties</synopsis>
  <groups_id/>
  <execution_time>45</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_233</test_case_id>
    <test_objective>To verify state of recording after updating with no recording properties</test_objective>
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
5. Inline updateSchedule message will be sent to TDK Recorder Simulator to start a new recording.
6. Once acknowledgment is received updateRecordings without any properties will be sent to TDK Recorder Simulator
7. getRecordings request will be send to TDK Recorder Simulator to check the completion status of the recordings 
8. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
9. Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>CheckPoint:
1. Recorder should send acknowledgement for inline updateSchedule request
2. Recorder should send acknowledgement for updateRecordings request
3. Recorder should send complete recording list in response to getRecordings request
4. The recording should be completed without any issues</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_UpdateRecording_WithNoRecordingProperties_233</test_script>
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
from time import sleep, time

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_UpdateRecording_WithNoRecordingProperties_233');
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

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
       
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

        if "updateSchedule" in actResponse:
                print "Inline updateSchedule message post success";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while ( ('acknowledgement' not in recResponse) and (retry < 10) ):
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        sleep(10);
                        retry += 1
                print "Retrieve Status Details: ",recResponse

                if 'acknowledgement' in recResponse:

                    print "Successfully retrieved acknowledgement from recorder for updateSchedule";
                    sleep(70);

                    response = recorderlib.callServerHandler('clearStatus',ip);
                    tdkTestObj.executeTestCase(expectedResult);
                    #Frame json message for update recording
                    requestID = str(randint(10, 500))
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"recordings\":[{\"recordingId\":\""+recordingID+"\"}]}}"
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);

                    if "updateRecordings" in actResponse:
                        print "updateRecordings message post success";
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry = 0;
                        while ( ('acknowledgement' not in recResponse) and (retry < 10) ):
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10)
                                retry += 1
                        print "Retrieve Status Details: ",recResponse

                        if 'acknowledgement' in recResponse:
                            print "Successfully retrieved acknowledgement from recorder for updateRecordings";
                            sleep(30);
                            print "Sending getRecordings request to get the recording list"
                            response = recorderlib.callServerHandler('clearStatus',ip)

                            jsonMsg = "{\"getRecordings\":{}}"
                            serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip)
                            print "Waiting for 1 mins to get recording list"
                            sleep(60)
                            recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording List: %s" %recResponse;
                            recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                            print recordingData
                            if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get recording info using getRecordings"
                            else:
                                reqRecording = {"recordingId":recordingID,"duration":60000,"deletePriority":"P3"}
                                ret = recorderlib.verifyCompletedRecording(recordingData,reqRecording)
                                if "FALSE" in ret:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording failed verification"
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Recording passed verification"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder for updateRecordings";
                    else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "updateRecordings message post failed";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder for updateSchedule";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Inline updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
