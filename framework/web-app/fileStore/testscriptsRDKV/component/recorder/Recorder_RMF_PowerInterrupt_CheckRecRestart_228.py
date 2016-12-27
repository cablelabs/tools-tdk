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
  <name>Recorder_RMF_PowerInterrupt_CheckRecRestart_228</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To verify that recording will restart/resume after a power interruption</synopsis>
  <groups_id/>
  <execution_time>90</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_228</test_case_id>
    <test_objective>To verify that recording will restart/resume after a power interruption</test_objective>
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
5. Legacy updateSchedule message will be sent to TDK Recorder Simulator to start a new recording for 25 min duration.
6. Once acknowledgment is received, wait for 10 min and reboot the box.
7. Wait for box and recorder component to be up.
8. Wait for remaining 15 min recording to complete.
9. Send getRecordings request to TDK Recorder Simulator to check the completion status of the recordings
10. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
11. Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>CheckPoint:
1. Recorder should send acknowledgement for updateSchedule request
2. Recorder should send complete recording list in response to getRecordings request
3. The recording should be completed without any issues.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_PowerInterrupt_CheckRecRestart_228</test_script>
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
obj.configureTestCase(ip,port,'Recorder_RMF_PowerInterrupt_CheckRecRestart_228');
#Get the result of connection with test component and STB
recLoadStatus = obj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus ;
#Set the module loading status
obj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               obj.initiateReboot();
               print "Waiting for 5min for the recoder to be up"
	       sleep(300);

	#Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #10mins duration
        duration = "600000"
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                print "Looping till acknowledgement is received"
                loop = 0;
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (('ack' not in actResponse) and (loop < 5)):
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    sleep(10);
                    loop = loop+1;
                print "Retrieve Status Details: ",actResponse
                if "acknowledgement" in actResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        response = recorderlib.callServerHandler('clearStatus',ip)
                        print "Wait for 5 min before causing power interrupt"
                        sleep(120)
                        obj.initiateReboot();
                        print "Waiting for 5min for recoder to be up"
                        sleep(300);
                        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Wait for remaining 5 min recording to complete"
                        sleep(200)
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                        #Wait to get response from recorder
                        sleep(60)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                        if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE")
                                print "RecordingId not found in list"
			else:
                                print "Recording data for recordingID ",recordingID, " is ",recordingData
                                statusValue = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                actualduration = recorderlib.getValueFromKeyInRecording(recordingData,'duration')
                                totalduration = actualduration[0] + actualduration[1]
                                print "status: ", statusValue
                                print "actualduration:" , totalduration
                                if "INCOMPLETE" in statusValue.upper() and (len(actualduration) == 2): 
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recording passed verification after power interruption"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording NOT passed verification after power interruption"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");
