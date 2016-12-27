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
  <version>9</version>
  <name>RMFMS_Recording_256Character_RecordId_01</name>
  <primitive_test_id>540</primitive_test_id>
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <primitive_test_version>0</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: To Initiate recording with recording Id of length 256 characters and verify it is successful or not.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_01
Test Type: Positive</synopsis>
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
    <test_case_id>CT_RECORDER_RECORDID_256CHARCTER_01</test_case_id>
    <test_objective>To Initiate recording with recording Id of length 256 characters and verify it is successful or not.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id = &lt;256 character length&gt;, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. Test Mgr loads the RecorderAgent via tdk test agent.
2. Test Mgr fetches the source_id/ocap_id mapped in streaming details page in test manager, frames 256 character length recordId, duration, 
record start time (0-record immediately, else specify time), and get UTC time. Pass all the values to RecorderAgent.
3. The RecorderAgent will frame the final RWS record request json message to start the recording
and  send to TDK recorder simulator server which is in Test Mgr. 
4. The json message will be of the form " {"updateSchedule" : {"requestId" : "7", "schedule" : [ 
{"recordingId" : "&lt;256 length recordId&gt;","locator" : [ "ocap://0x5f43" ] ,"epoch" : ${now} ,"start" : "0" ,"duration" : 180000 ,
"properties":{"title":"Recording_&lt;256 character recordid&gt;&gt;"},"bitRate" : "HIGH_BIT_RATE" ,"deletePriority" : "P3" }]}} "
5. The TDK recorder simulator server will pass it to the comcast rmfStreamer process to initiate recording requested.
6. The comcast rmfStreamer will send the acknowledgement json message to TDK recorder simulator server and is passed to Test mgr. 
7. Test Mgr verifies the acknowledgement json message for SUCCESS/FAILURE.
8. And RecorderAgent also verifies the status of the recording by verifying ocapri_log.txt.txt.
9. The Final result after verifying ocapri_log.txt.txt RecorderAgent will send the SUCCESS/FAILURE to Test Mgr.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapri_log.txt to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_checkRecording_status</test_stub_interface>
    <test_script>RMFMS_Recording_256Character_RecordId_01</test_script>
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
import re;
import random;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_01');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
               print "Sleeping to wait for the recoder to be up"
               sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

	#Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        rec_id = random.randrange(10**9, 10**256)
        recording_id = str(rec_id);
	requestID = "7";
        duration = "60000";
        start_time = "0";
	now = "curTime"
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                print "ocapid : %s" %validid;
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
                Jsonurldetails = tdkTestObj.getResultDetails();
                if expectedresult in actualresult:
                        print "Recorder received the requested recording url";
                        tdkTestObj.setResultStatus("SUCCESS");
			RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recording_id+"\",\"locator\":[\"ocap://"+validid+"\"],\"epoch\":"+now+",\"start\":"+start_time+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_256\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
			serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        if "updateSchedule" in serverResponse:
                                print "updateSchedule message post success";
				sleep(10);				
                                retry = 0;
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while ( ('acknowledgement' not in recResponse) and (retry < 10)):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
				print "Retrieve Status Details: %s" %recResponse;
                                if "acknowledgement" in recResponse:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Received the recorder acknowledgement";
					print "Wait for recording to complete"
                                        sleep(60);

					tdkTestObj = obj.createTestStep('Recorder_SendRequest');
					tdkTestObj.executeTestCase(expectedresult);
                                        print "Sending getRecordings to get the recording list"
                                        recorderlib.callServerHandler('clearStatus',ip)
                                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                        print "Wait for 1 min to get response from recorder"
                                        sleep(60)
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                        print "Recording List: %s" %actResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recording_id);
                                        print recordingData;
                                        if ('NOTFOUND' in recordingData):
                                                tdkTestObj.setResultStatus("FAILURE");
                                        else:
						tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to receive the recorder acknowledgement";
                        else:
                                print "updateSchedule message post failure";
                                tdkTestObj.setResultStatus("FAILURE");
                else:
			tdkTestObj.setResultStatus("FAILURE");
			print "Recorder NOT received the requested recording url";
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");

	#unloading Recorder module
	obj.unloadModule("Recorder");
