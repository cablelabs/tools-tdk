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
  <name>Recorder_RMF_GenerationId_In_Recording_Status_19</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder- To check if generation Id is sent with recording status</synopsis>
  <groups_id/>
  <execution_time>25</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_19</test_case_id>
    <test_objective>Recorder- To check if generation Id is sent with recording status</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to 
  RecorderAgent to generate request url.
3.RecorderAgent/Python lib interface will frame the json message to Simulate a longpoll notification with an inline 
  "updateSchedule" payload containing a new hot recording (starting now and lasting 30 seconds) and "generationId": "test4a",
  and send to TDK Recorder Simulator server which is present in TM.
4.Wait 15 seconds and then simulate a longpoll notification with an inline "updateSchedule" 
payload that causes the new recording to be deleted (e.g. send an empty schedule with fullSchedule:true) and 
"generationId": "test4b" through RecorderAgent/Python lib interface and TDK Recorder Simulator server.
5.Recorder makes a POST request to RWS bearing HTTP header "X-Parker-Generation-ID: 
  test4b" and "recordingStatus" payload.(CP)
6.Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.</automation_approch>
    <except_output>Checkpoint : Acknowledgement status from the DVRSimulator AND value of generationId from http header at step 5.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_GenerationId_In_Recording_Status_19</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_In_Recording_Status_19');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

genIdInput1 = "test4a";
genIdInput2 = "test4b";
#genIdInput2 = "1431877561793;321744722806850394"

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);

        print "Sleeping to wait for the recoder to be up"


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
        duration = "30000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
	fullSch = "true";

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput1+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details for first json: %s"%actResponse;
	
	sleep(15);
        #expResponse = "updateSchedule";
        #tdkTestObj.executeTestCase(expectedResult);
        response = recorderlib.callServerHandler('clearStatus',ip);
	#jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":"+fullSch+",\"generationId\":\""+genIdInput2+"\",\"schedule\":[{}]}}";
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":"+fullSch+",\"generationId\":\""+genIdInput2+"\"}}";

        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details for the second json: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule Inline message post success";
                print "Wait for 60s to get acknowledgement"
                sleep(60);
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
                print "Looping till acknowledgement is received"

                retry = 0;
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while ( ('ERROR' not in actResponse) and (retry < 15)):
                        sleep(10);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: %s"%actResponse;

		if ( ('ERROR' in actResponse)):
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received Empty/Error status";
                else:
                    genOut = recorderlib.readGenerationId(ip)
		    if genOut == genIdInput2:
                        tdkTestObj.setResultStatus("SUCCESS");
			print "GenerationId retrieved (%s) match with the expected (%s)"%(genOut,genIdInput2);
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        print "Wait for 3 min to get response from recorder"
                        sleep(60)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse;
			recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
			print "Recording data details: %s"%recordingData;
			if 'NOTFOUND' not in recordingData:
				print "Recording is present";
			else:
                        	tdkTestObj.setResultStatus("FAILURE");
				print "Recording is NOT present";

                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "GenerationId retrieved (%s) does not match with the expected (%s)"%(genOut,genIdInput2);

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule Inline message post failed";


        #unloading Recorder module
        recObj.unloadModule("Recorder");

