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
  <name>Recorder_RMF_Check_Status_Four_Parallel_Inprogress_Recordings_Inline_252</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recoder_DVR_Protocol_252 - Schedule four recordings then reboot during recording and check the status of recordings</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_252</test_case_id>
    <test_objective>Schedule 4 recordings using inline at same time and then reboot during when recording progressing and verify all the four recordings are started and is getting over with status incomplete</test_objective>
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
3.RecorderAgent / Python lib interface will frame the json message to Schedule 4 recordings
4.Reboot the box when the recordings are in progress 
5.All the four recordings should get started and is getting over with status incomplete
6.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check the state of current recording</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Check_Status_Four_Parallel_Inprogress_Recordings_Inline_252</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_Status_Four_Parallel_Inprogress_Recordings_Inline_252');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
	       print "Sleeping to wait for the recoder to be up"
               recObj.initiateReboot();
	       sleep(300);


        #Giving no update here to get the recording list in case the previous generation id is set to zero before reboot
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

        #Pre-requisite to clear any recording status
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
        duration = "120000";
        startTime = "0";
        now = "curTime"

        tdkTestObj.executeTestCase(expectedResult);

        maxRec = 4;
        list=[]
        loop=0
        for deviceNo in range(0,maxRec):
            Id = '0'+str(deviceNo+1)
	    recId = str(randint(10000, 500000));
	    streamId = tdkTestObj.getStreamDetails(Id).getOCAPID()

	    #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recId+"\",\"locator\":[\"ocap://"+streamId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recId+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
         
            list.insert(loop,recId)
            loop = loop+1
            expResponse = "updateSchedule";
            tdkTestObj.executeTestCase(expectedResult);
            actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
            print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
            tdkTestObj.setResultStatus("SUCCESS");
            print "updateSchedule message post success";
            print "Wait for 60s to get acknowledgement"
            sleep(20);
            #Check for acknowledgement from recorder
            tdkTestObj.executeTestCase(expectedResult);    
            print "Looping till acknowledgement is received"
            loop = 0;
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
            while (('ack' not in actResponse) and (loop < 5)):
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                sleep(10);
                loop = loop+1;
                print "Retrieve Status Details: ",actResponse;

            if 'acknowledgement' not in actResponse:
                tdkTestObj.setResultStatus("FAILURE");
                print "Received Empty/Error status";
            elif 'acknowledgement' in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Successfully retrieved acknowledgement from recorder";
                sleep(40);
                # Reboot the STB
                print "Rebooting the STB to get the recording list from full sync"
                recObj.initiateReboot();
                print "Sleeping to wait for the recoder to be up"
                sleep(300);

                tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                tdkTestObj.executeTestCase(expectedResult);
                print "Sending getRecordings to get the recording list"
                recorderlib.callServerHandler('clearStatus',ip)
                recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                print "Wait for 1 min to get response from recorder"
                sleep(60)
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                print "Recording List: %s" %actResponse;
                recordingData1 = recorderlib.getRecordingFromRecId(actResponse,list[0]);
                recordingData2 = recorderlib.getRecordingFromRecId(actResponse,list[1]);
                recordingData3 = recorderlib.getRecordingFromRecId(actResponse,list[2]);
                recordingData4 = recorderlib.getRecordingFromRecId(actResponse,list[3]);
                print recordingData1;
                print recordingData2;
                print recordingData3;
                print recordingData4;
                if 'NOTFOUND' not in (recordingData1,recordingData2,recordingData3 and recordingData4):
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved the recording list from recorder";
                    statusKey = 'status'
                    statusValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,statusKey)
                    statusValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,statusKey)
                    statusValue3 = recorderlib.getValueFromKeyInRecording(recordingData3,statusKey)
                    statusValue4 = recorderlib.getValueFromKeyInRecording(recordingData4,statusKey)
                    if "INCOMPLETE" in (statusValue1.upper(),statusValue2.upper(),statusValue3.upper() and statusValue4.upper()):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "All Four Recordings are started and Incompleted";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Recordings not started successfully";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
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
