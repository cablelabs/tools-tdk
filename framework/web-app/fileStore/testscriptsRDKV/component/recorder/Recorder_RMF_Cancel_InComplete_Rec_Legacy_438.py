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
  <version>3</version>
  <name>Recorder_RMF_Cancel_InComplete_Rec_Legacy_438</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should not change the status when cancelling a recording which is end with INCOMPLETE</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_438</test_case_id>
    <test_objective>Recorder should not change the status when cancelling a legacy recording which is end with status INCOMPLETE</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of stt_received and stage4 in /tmp path of device.
4. In rmfconfig.ini file the parameters FEATURE.LONGPOLL.URL,FEATURE.RWS.GET.URL and FEATURE.RWS.POST.URL should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.Schedule a hot legacy recording of 7 minute duration.
3.Reboot the box and wait for the recording to complete
4.Sent json message to cancel the recording
5.Check whether recorder has changed the status of recording from INCOMPLETE to some other status
6.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Recording details should be available as expected</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Cancel_InComplete_Rec_Legacy_438</test_script>
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
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_Cancel_InCompleteRec_Legacy_438');
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


	#Primitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('Recorder_SendRequest');
	expectedResult="SUCCESS";
	tdkTestObj.executeTestCase(expectedResult);		

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
	#5mins duration
        duration = "420000";
        startTime = "0";
	genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
		
	serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
	print "serverResponse : %s" %serverResponse;
				
	if "updateSchedule" in serverResponse:
		print "updateSchedule message post success";
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		retry = 0;
                while (( ([] == recResponse) or ('ack' not in recResponse) ) and (retry < 10 )):
			sleep(10);
			recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			retry += 1
		print "Retrieve Status Details: ",recResponse;
		if "ack" in recResponse:
			print "Simulator Server received the recorder acknowledgement";
                        print "Wait for the recording to complete partially"
                        sleep(60);
			print "Rebooting the box to interrupt the recording"
			obj.initiateReboot();
			print "Sleeping to wait for the recoder to be up and recording to complete partially"
			sleep(300);
                        recorderlib.callServerHandler('clearStatus',ip)
	                tdkTestObj = obj.createTestStep('Recorder_SendRequest');
                 	tdkTestObj.executeTestCase(expectedResult);		
                        print "Wait for the recording to complete"
                        sleep(60)
                        #Frame json message for update recording
                        jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":false,\"cancelRecordings\":[\""+recordingID+"\"]}}";

                        expResponse = "updateSchedule";
                        tdkTestObj.executeTestCase(expectedResult);
                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgCancelRecording,ip);
                        if expResponse in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "updateSchedule message post success";
                            sleep(10);
                            #Check for acknowledgement from recorder
                            tdkTestObj.executeTestCase(expectedResult);
		            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                            loop = 0;
                            while (('acknowledgement' not in actResponse) and (loop < 5)):
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10);
                                loop = loop+1;
	                    print "Retrieve Status Details: %s"%actResponse;
                            if 'acknowledgement' in actResponse:
                                print "Successfully retrieved acknowledgement from recorder";
                                sleep(30)
                                recorderlib.callServerHandler('clearStatus',ip)
                                recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                                print "Wait for 60 seconds to get response from recorder"
                                sleep(60)
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
	                        print "Retrieve Status Details: %s"%actResponse;
			        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
       	                        print recordingData
                                if 'NOTFOUND' not in recordingData:
				    status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
				    if "INCOMPLETE" in status.upper():
                                	tdkTestObj.setResultStatus("SUCCESS");
                                	print "INCOMPLETE Status NOT changed";
                            	    else:
                                	tdkTestObj.setResultStatus("FAILURE");
                                	print "INCOMPLETE Status changed";
			    else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Failed to retrieve recordingData";	
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        #unloading Recorder module
        obj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");

					

					
