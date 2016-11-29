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
  <name>Recorder_RMF_PurgeNonP4_OnDiskFull_SchedHotP4Rec_87</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that recorder deletes non-P4 recordings before disk is completely full to allow new scheduled hot P4 recording. Pre-requisite: HDD should be full with at least 1 P3 and P4 recodings</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
  <long_duration>true</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_87</test_case_id>
    <test_objective>Verify that recorder deletes non-P4 recordings before disk is completely full to allow new scheduled hot P4 recording</test_objective>
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
3. Get the list of all P3 recordings
4.RecorderAgent / Python lib interface will frame the json message to schedule a hot P4 recording for 1 min and send to TDK Recorder Simulator server which is present in TM.
5. check oldest P3 recording gets deleted and new recording is completed. Check for rws notification.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Check the oldest P3 recording deleted
Checkpoint 3 Check new recording completed</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_PurgeNonP4_OnDiskFull_SchedHotP4Rec_87</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_PurgeNonP4_OnDiskFull_SchedHotP4Rec_87');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
	       sleep(300);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        #Get the list of recordings
    	jsonMsg = "{\"getRecordings\":{}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Server response for getRecordings: ",serverResponse;
        if 'getRecordings' in serverResponse:
                print "getRecordings message post success"
        	print "Waiting to get recording list"
        	sleep(60)
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
        	status = recorderlib.getStatusMessage(recResponse)
        	print "status message containing recording list: ",status
                if ("NOSTATUS" != status):
                        #From the list get all P3 recordings Ids
                        recordings = recorderlib.getRecordings(recResponse)
                        recP3List = []
                        for i in range(0, len(recordings)):
                                if ( (recordings[i]['deletePriority'] == "P3") and (recordings[i]['size'] > 0) ):
					recP3List.append(recordings[i]['recordingId'])

                        if ( [] != recP3List ):
                        	print "Found P3 recordings: ",recP3List
				response = recorderlib.callServerHandler('clearStatus',ip);

                                #Execute updateSchedule for scheduling new recording
                                requestID = str(randint(10, 500));
                                recordingID = str(randint(10000, 500000));
                                duration = "60000";
                                startTime = "0";
                                ocapId = tdkTestObj.getStreamDetails('02').getOCAPID()
                                now = "curTime"

                                #Frame json message
                                jsonMsgNew = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";
                                serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNew,ip);
                                print "Server response for updateSchedule: ",serverResponse;

                                if 'updateSchedule' in serverResponse:
                                        print "updateSchedule message post success";
                                        print "Waiting to get acknowledgement from recorder"
                                        sleep(30)
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Retrieve Status Details: %s"%recResponse;
                                        if 'ack' in recResponse:
                                        	recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                print "recording data from response: ",recordingData
						if "NOTFOUND" != recordingData:
                                                    status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                        	    error = recorderlib.getValueFromKeyInRecording(recordingData,'error')
                                                    if ( ("SPACE_FULL" == error) and ("FAILED" == status.upper()) ):
                                                        print "Space Full!! Check if old P3 recording is purged by recorder"
                                               		response = recorderlib.callServerHandler('clearStatus',ip);
                                                        jsonMsg = "{\"getRecordings\":{}}";
                                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
                                                        print "Server response for getRecordings: ",serverResponse;
								
                                                        if 'getRecordings' in serverResponse:
                                                        	print "getRecordings message post success";
                                                                #wait to get list
                                                                sleep(60)
                                                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                               	print "Retrieve Status Details: ",recResponse
                                                               	status = recorderlib.getStatusMessage(recResponse)
                                                                if ("NOSTATUS" != status):
									#Check if any old P3 recording is missing
									deleteFlag = 0
				                        		for i in range(0, len(recP3List)):
										recordingData = recorderlib.getRecordingFromRecId(recResponse,recP3List[i])
										if 'NOTFOUND' == recordingData:
											print "Successfully deleted existing recording ",recP3List[i];
											deleteFlag = 1

									if 1 == deleteFlag:
                                                                                print "Recorder purged old P3 recording"
										print "Check status of new recording"
										recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                				print "recording data from response: ",recordingData
                                                				status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
										if "COMPLETED" == status.upper():
											print "New recording completed after purging old recording"
											tdkTestObj.setResultStatus("SUCCESS");
										else:
											print "New recording not completed even after purging old recording"
											tdkTestObj.setResultStatus("FAILURE");
                                                                        else:
                                                                                print "None of P3 recordings deleted to free up space"
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                else:
                                                                        print "Timeout!Failed to get recording list. Exiting...";
                                                                        tdkTestObj.setResultStatus("FAILURE");
        						else:
            							tdkTestObj.setResultStatus("FAILURE");
            							print "getRecordings message post failed";
                                                    else:
                                                        print "Disk not full yet. Pre-req not met. Exiting!"
                                                        tdkTestObj.setResultStatus("FAILURE");
					    	else:
						    print "New recording allowed. Disk not full yet. Pre-req not met. Exiting!"
						    tdkTestObj.setResultStatus("FAILURE");
                                        else:
                                        	print "Failed to get acknowledgement from recorder"
                                                tdkTestObj.setResultStatus("FAILURE");
                                else:
                                        print "updateRecordings message post failed"
                                       	tdkTestObj.setResultStatus("FAILURE")
                        else:
				print "Did not find P3 recordings.Pre-req not met. Exiting!"
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        print "Timeout!Failed to get recording list. Exiting...";
                        tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "getRecordings message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
