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
  <name>Recorder_RMF_EOR_StartedOnTime_EndedEarly_Legacy_132</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder must always send an end-of-recording status if it ever sent any start-of-recording status.</synopsis>
  <groups_id/>
  <execution_time>100</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_132</test_case_id>
    <test_objective>check that Recorder sends an end-of-recording status if it ever sent any start-of-recording status for recording started on time and ended early.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets a source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.Frame the legacy json message through RecorderAgent/Python lib interface to schedule the current recording 
  of 5 minutes and send to TDK Recorder Simulator server which is present in TM.
4.Wait for the recording to completes partially.
5.Reboot the STB so that recording is partial and ends early.
6.noUpdate schedule message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
7.Retrieve the status from Recorder to TDK Recorder Simulator server, it will be extracted by the TM.
8.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 : Acknowledgement status from the DVRSimulator.
Checkpoint 2 : Get the response from recorder in full sync and verify that status has been set to startedIncomplete.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_EOR_StartedOnTime_EndedEarly_Legacy_132</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import recorderlib
from random import randint
from time import sleep
#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_EOR_StartedOnTime_EndedEarly_Legacy_132');
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
	sleep(30);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10,500));
        recordingID = str(randint(10000, 500000));
	genIdInput = recordingID;
	duration = "300000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                tdkTestObj.executeTestCase(expectedResult);
		print "Waiting to get acknowledgment status"
		sleep(5);
		retry=0
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
			sleep(5);
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			retry += 1
		print "Retrieve Status Details: %s"%actResponse;
                if (('ERROR' in actResponse)):
	                tdkTestObj.setResultStatus("FAILURE");
        	        print "Received Empty/Error status";
                elif 'acknowledgement' in actResponse:
                	tdkTestObj.setResultStatus("SUCCESS");
	                print "Successfully retrieved acknowledgement from recorder";
		    	print "Clear Status Details: %s"%response;
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        print "Wait for 60 seconds to get response from recorder"
			sleep(60);
			tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                        tdkTestObj1.executeTestCase(expectedResult);
                        tdkTestObj1.setResultStatus("SUCCESS")
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse;
                        msg = recorderlib.getStatusMessage(actResponse);
			print "Get Status Message Details: %s"%msg;
                       	if "" == msg:
                            value = "FALSE";
	                    print "No status message retrieved"
	        	    tdkTestObj.setResultStatus("FAILURE");
        	        else:
		 	    value = msg['recordingStatus']["initializing"];
			    print "Initializing value: %s"%value;
			    if "TRUE" in value.upper():
        	                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
	                	print recordingData
        	                if 'NOTFOUND' not in recordingData:
                	            key = 'status'
                        	    value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	                            print "key: ",key," value: ",value
        	                    print "Successfully retrieved the recording list from recorder";
                	            if "" != value.upper():
	                                print "Recording status set";
                        	        tdkTestObj1.setResultStatus("SUCCESS");
                	        	if "COMPLETE" != value.upper():
                        	            tdkTestObj1.setResultStatus("SUCCESS");
		                	    print "Recording not marked as COMPLETE as expected";
        		                else:
                		            tdkTestObj1.setResultStatus("FAILURE");
	                		    print "Recording marked as COMPLETE, it was not expected";
        		            else:
	                	        print "Recording status not set";
                		        tdkTestObj1.setResultStatus("FAILURE");
			        else:
                	            tdkTestObj1.setResultStatus("FAILURE");
                        	    print "Failed to get the recording data";
		            else:
        		        tdkTestObj1.setResultStatus("FAILURE");
                	        print "Failed to retrieve the recording list from recorder";
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                    	print "Failed to retrieve acknowledgement from recorder";
        else:
	        tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failure";
        recObj.unloadModule("Recorder");
else:
	print "Failed to load Recorder module";
    	#Set the module loading status
    	recObj.setLoadModuleStatus("FAILURE");
