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
  <name>Recorder_RMF_SchedRec_Legacy_IncompleteStatus_116</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should send Incomplete notification if the recording(future, legacy) has been interrupted by another recording before the first recording completed.</synopsis>
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
    <test_case_id>CT_Recoder_DVR_Protocol_116</test_case_id>
    <test_objective>Check that recorder sending status = Incomplete message if a legacy future recording is scheduled and it is interrupted by another recording with full schedule=true</test_objective>
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
3.RecorderAgent / Python lib interface will frame the json message to schedule a future recording using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM
5.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the response from recorder and verify that status=Incomplete sent for the recording from recorder.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_SchedRec_Legacy_IncompleteStatus_116</test_script>
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
obj.configureTestCase(ip,port,'Recorder_RMF_SchedRec_Legacy_IncompleteStatus_116');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

if "SUCCESS" in loadmodulestatus.upper():

	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
	       print "Rebooting box for setting configuration"
               obj.initiateReboot();
	       print "Waiting for the recoder to be up"
	       sleep(300);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        sleep(10);
        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;


        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #3mins duration
        duration = "180000";
        startTime = "60000";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success for recording 1";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (('acknowledgement' not in recResponse) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details for recording 1: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement for recording 1";
                        print "Wait for some time to make partial recording 1";
                        sleep(90);
                        print "Send request for recording 2";

                        requestID2 = str(randint(10, 500));
                        recordingID2 = str(randint(10000, 500000));
			startTime2 = "0";
			duration = "60000";
			
			response = recorderlib.callServerHandler('clearStatus',ip);
                        #Frame json message
                        RequestURL2 = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"fullSchedule\":true,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                        serverResponse2 = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL2,ip);
                        if "updateSchedule" in serverResponse2:
                                print "updateSchedule message post success for recording 2";
                                recResponse2 = recorderlib.callServerHandler('retrieveStatus',ip);
                                retry = 0;
                                while (('acknowledgement' not in recResponse2) and (retry < 10 )):
                                        sleep(10);
                                        recResponse2 = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                                print "Retrieve Status Details for recording 2: ",recResponse2;
                                print "Wait for recording 2 to complete";
                                sleep(30);
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print "Recording list: ",actResponse;
                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                print "Printing recording data: ", recordingData;
                                if ('NOTFOUND' not in recordingData):
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        if "INCOMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recorder has sent status = InComplete";
                                        elif "COMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = complete";
                                        elif "STARTED" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = started";
                                        elif "FAILED" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = Failed";
                                        elif "STARTEDINCOMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = StartedIncomplete";
                                        elif "PENDING" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = pending";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent some other status";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder not sent any status for the recording 1 which was interrupted";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateSchedule message post failed for recording 2";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server NOT received the recorder acknowledgement for recording 1";
        else:
                print "updateSchedule message post failed for recording 1";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");

