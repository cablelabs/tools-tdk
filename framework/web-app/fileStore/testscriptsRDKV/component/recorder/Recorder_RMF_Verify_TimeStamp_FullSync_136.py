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
  <name>Recorder_RMF_Verify_TimeStamp_FullSync_136</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recoder_DVR_Protocol_136 - Recorder should send timestamp=&lt;the time in millis that something last changed&gt; in full sync</synopsis>
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
    <test_case_id>CT_Recoder_DVR_Protocol_136</test_case_id>
    <test_objective>Recorder should send timestamp=&amp;lt;the time inÂ millis that something last changed&amp;gt; in full sync</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent / Python lib interface will frame the json message to schedule recording using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4. STB will be rebooted after a sleep of recording duration.
5. noUpdate schedule message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
6. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check all current and future recordings</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Verify_TimeStamp_FullSync_136</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
import time
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Verify_TimeStamp_FullSync_136');
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
	print "Sleeping to wait for the recoder to be up"

        
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
                print "Looping till acknowledgement is received"
                loop = 0;
        	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while ( ('acknowledgement' not in actResponse) and (loop < 5)):
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    sleep(10);
                    loop = loop+1;
	        print "Retrieve Status Details: %s"%actResponse;
		if 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received Empty/Error status";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    #Waiting for the recording to complete
                    sleep(70);
		    response = recorderlib.callServerHandler('clearStatus',ip);
                    # Reboot the STB
		    print "Rebooting the STB to get the recording list from full sync"
		    recObj.initiateReboot();
		    print "Sleeping to wait for the recoder to be up"
		    sleep(300);
		    #Frame json message
		    jsonMsgNoUpdate = "{\"noUpdate\":{}}";
                    expResponse = "noUpdate";
		    tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                    tdkTestObj1.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                    print "No Update Schedule Details: %s"%actResponse;
                    if expResponse in actResponse:
                        print "No Update Schedule message post success";
                        print "Wait for 60s to get the recording list"
                        tdkTestObj1.setResultStatus("SUCCESS");
                        sleep(60);
                        #Check for acknowledgement from recorder
                        tdkTestObj1.executeTestCase(expectedResult);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			print actResponse;
			msg = recorderlib.getStatusMessage(actResponse);
			print "Get Status Message Details after first full sync: %s"%msg;
                        if "" == msg or "recordingStatus" not in msg:
                                tdkTestObj1.setResultStatus("FAILURE");
                                print "No status message retrieved"
                        else:
				value1 = msg['recordingStatus']["timestamp"];
				print "Timestamp value after first full sync: %s"%value1;
                       
                                #Execute updateSchedule
                                requestID2 = str(randint(10, 500));
                                recordingID2 = str(randint(10000, 500000));
                                ocapId = tdkTestObj.getStreamDetails('02').getOCAPID()
                                now = "curTime"

                                #Frame json message
                                jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                                tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                                expResponse = "updateSchedule";
                                tdkTestObj.executeTestCase(expectedResult);
                                actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
                                print "Update Schedule Details: %s"%actResponse;

                                if expResponse in actResponse:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "updateSchedule message post success";
                                    #Check for acknowledgement from recorder
                                    tdkTestObj.executeTestCase(expectedResult);
                                    print "Looping till acknowledgement is received"
                                    loop = 0;
                                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                    while ( ('acknowledgement' not in actResponse) and (loop < 5)):
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        sleep(10);
                                        loop = loop+1;
                     	            print "Retrieve Status Details: %s"%actResponse;
                       		    if 'acknowledgement' not in actResponse:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Received Empty/Error status";
                                    elif 'acknowledgement' in actResponse:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Successfully retrieved acknowledgement from recorder";
                                        #Waiting for the recording to complete
                                        sleep(70);
                                        response = recorderlib.callServerHandler('clearStatus',ip);
                                        # Reboot the STB
                       		        print "Rebooting the STB to get the recording list from full sync"
                                        recObj.initiateReboot();
                        	        print "Sleeping to wait for the recoder to be up"
     		                        sleep(300);
		                        #Frame json message
                                        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
                                        expResponse = "noUpdate";
                            	        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                                        tdkTestObj1.executeTestCase(expectedResult);
                                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                                        print "No Update Schedule Details: %s"%actResponse;
                                        if expResponse in actResponse:
                                            print "No Update Schedule message post success";
                                            print "Wait for 60s to get the recording list"
                                            tdkTestObj1.setResultStatus("SUCCESS");
                                            sleep(60);
                                            #Check for acknowledgement from recorder
                                            tdkTestObj1.executeTestCase(expectedResult);
                                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		                            print actResponse;
                         		    msg = recorderlib.getStatusMessage(actResponse);
              			            print "Get Status Message Details after second full sync: %s"%msg;
                                            if "" == msg or "recordingStatus" not in msg:
                                                tdkTestObj1.setResultStatus("FAILURE");
                                                print "No status message retrieved"
                                            else:
		                  		value2 = msg['recordingStatus']["timestamp"];
				                print "Timestamp value after second full sync: %s"%value2;
                   				currentTime = int(round(time.time() * 1000))
                                                if value1 < value2:
                                                    print "Second full sync timestamp value is greater than first full sync timestamp"
                                                    tdkTestObj1.setResultStatus("SUCCESS");
                                                else:
                                                    print "Second full sync timestamp value is NOT greater than first full sync timestamp"
                                                    tdkTestObj1.setResultStatus("FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
