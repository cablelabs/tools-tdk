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
  <name>Recorder_RMF_PowerInterrupt_Notification_53</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recoder_DVR_Protocol_53 - Recoder to send power interruption error notification for multiple scheduling at different timestamp</synopsis>
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
    <test_case_id>CT_Recoder_DVR_Protocol_53</test_case_id>
    <test_objective>Recoder to send power interruption error notification for multiple scheduling at different timestamp using legacy</test_objective>
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
3.RecorderAgent / Python lib interface will frame the json message to schedule the multiple current recordings using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4.Reboot the STB when the recordings are INPROGRESS
5. Check the status message sent by the recorder back to RWS
6. noUpdate schedule message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
7. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
8.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check the state of current and future recordings or verify the response from the RWS post server.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_PowerInterrupt_Notification_53</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_PowerInterrupt_Notification_53');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper())

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "540000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        SchedulejsonMsg = "{\"updateSchedule\":{\"requestId\":\""+str(int(requestID)+1)+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
	ScheduleResponse = recorderlib.callServerHandlerWithMsg('updateMessage',SchedulejsonMsg,ip);
        if expResponse in actResponse and expResponse in ScheduleResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
		loop = 0;
		while ( ('acknowledgement' not in actResponse) and (loop < 5)):
	                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			sleep(10);
			loop = loop+1;
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Successfully retrieved acknowledgement from recorder";
                        sleep(60);
                        response = recorderlib.callServerHandler('clearStatus',ip);
                        # Reboot the STB
                        print "Rebooting the STB to get the recording list from full sync"
                        recObj.initiateReboot();
                        print "Sleeping to wait for the recoder to be up"
                        sleep(300);
                        print "Wait for the recording to complete"
                        sleep(300)
			actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                        tdkTestObj1.executeTestCase(expectedResult);
                        sleep(60);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print actResponse;
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
			print "Recording 1 data : " , recordingData
                        SecondrecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1))
                        print "Recording 2 data : ", SecondrecordingData
			
                        if 'NOTFOUND' not in recordingData and 'NOTFOUND' not in SecondrecordingData:
                            key = 'status'
                            errorKey = 'error'
                           
			    print "Get status and error field from Recording 1" 
                            statusValue = recorderlib.getValueFromKeyInRecording(recordingData,key)
                            errorValue = recorderlib.getValueFromKeyInRecording(recordingData,errorKey)
			    print "Recording 1 status : ", statusValue," error: ",errorValue
			    print "Get status and error field from Recording 2"
                            secondStatusValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,key)
                            secondErrorValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,errorKey)
                            print "Recording 2 status : ", secondStatusValue," error: ",secondErrorValue
                            if "INCOMPLETE" in statusValue.upper() and "POWER_INTERRUPTION" in errorValue.upper() and "INCOMPLETE" in secondStatusValue.upper() and "POWER_INTERRUPTION" in secondErrorValue.upper():
                                print "Power interruption happened successfully";
				timestampList = recorderlib.getTimeStampListFromStatus(actResponse)
                                print "Timestamp list in recording status: ",timestampList
                                if timestampList != []:
                                	if ( (len(timestampList) > 1) and (timestampList[0] != timestampList[1])):
                                        	print "Recorder has send the recording status notification at different timestamp"
                                                tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                                print "Recorder has not send the recording status notification at different timestamp"
                                                tdkTestObj.setResultStatus("FAILURE");
                            	else:
                                	print "Recorder has not send the timestamp in  recording status"
                                	tdkTestObj.setResultStatus("FAILURE");
                            elif "BADVALUE" in statusValue.upper() or "BADVALUE" in errorValue.upper() or "BADVALUE" in secondStatusValue.upper() or "BADVALUE" in secondErrorValue.upper():
			    	tdkTestObj.setResultStatus("FAILURE");
                                print "Recording did not have error/status field";
                            else:
                                print "Recorder has not send recording status"
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj1.setResultStatus("FAILURE");
                            print "Failed to retrieve the recording list from recorder";
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
