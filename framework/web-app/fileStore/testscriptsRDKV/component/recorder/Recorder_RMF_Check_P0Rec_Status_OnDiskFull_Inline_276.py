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
  <name>Recorder_RMF_Check_P0Rec_Status_OnDiskFull_Inline_276</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Delete P0 Recordings Only When Space is Needed</synopsis>
  <groups_id/>
  <execution_time>120</execution_time>
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
    <test_case_id>CT_Recorder_DVR_Protocol_276</test_case_id>
    <test_objective>Delete P0 Recordings Only When Space is Needed using inline</test_objective>
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
3.Schedule a P4 recording and change the priority to P0.
4.Schedule multiple long duration recordings  to get Disk Full error
5.After getting Disk Full error wait for 7 minutes.
6.getrecordings message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
7Check P0 Recording meta data should not be there.
8.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 The recording metadata should not be available in inside ‘/tmp/mnt/diska3/persistent/dvr/recdbuser</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_PresenceOfRecordingMetaData</test_stub_interface>
    <test_script>Recorder_RMF_Check_P0Rec_Status_OnDiskFull_Inline_276</test_script>
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
from recorderlib import checkDiskFullWithRecordings
from random import randint
from time import sleep
from trm import getMaxTuner
#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
trmObj.configureTestCase(ip,port,'Recorder_RMF_Check_P0Rec_Status_OnDiskFull_Inline_276');
#Get the result of connection with test component and STB
trmLoadStatus = trmObj.getLoadModuleResult();
print "TRM module loading status  :  %s" %trmLoadStatus;
#Set the module loading status
trmObj.setLoadModuleStatus(trmLoadStatus);

NUMOFTUNERS = 5

if "FAILURE" in trmLoadStatus.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    trmObj.initiateReboot();
    trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
    trmObj.configureTestCase(ip,port,'Recorder_RMF_Check_P0Rec_Status_OnDiskFull_Inline_276');
    #Get the result of connection with test component and STB
    trmLoadStatus = trmObj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %trmLoadStatus;
    sleep(300)

trmObj.setLoadModuleStatus(trmLoadStatus);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in trmLoadStatus.upper():
    	#Fetch max tuner supported
    	NUMOFTUNERS = getMaxTuner(trmObj,'SUCCESS')
        trmObj.unloadModule("trm")

if NUMOFTUNERS < 5:
	NUMOFTUNERS = 5

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_P0Rec_Status_OnDiskFull_Inline_276');
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
        actResponse =recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

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
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
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
                    print "Wait for the recording to be completed"
                    sleep(70)
                    #Frame json message for update recording
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";

                    expResponse = "updateRecordings";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgUpdateRecording,ip);
                    print "updateRecordings Details: %s"%actResponse;
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateRecordings message post success";
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
                            sleep(60);
                            print "Sending getRecordings to get the recording list"
                            recorderlib.callServerHandler('clearStatus',ip)
                            recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                            print "Wait for 1 min to get response from recorder"
                            sleep(60)
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording list after moving to priority P0",actResponse
                            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                            print recordingData
                            if 'NOTFOUND' not in recordingData:
                                key = 'deletePriority'
                                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                print "key: ",key," value: ",value
                                print "Successfully retrieved the recording list from recorder";
                                if "P0" in value.upper():
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Recording moved to P0 priority successfully";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording NOT moved to P0 priority successfully";
                            else:
                                 tdkTestObj.setResultStatus("FAILURE");
                                 print "Failed to retrieve the recording list from recorder";

                            loop=0;
                            diskFull=0;
                            while (( diskFull!=1) and (loop < 5)):

	     		        #Pre-Req start: Disk should be full before starting test
	                        print "Schedule 2hrs P4 recordings on all the tuners"
	                        diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,7200000,"P4")
                                if 1 == diskFull:
                                    break
 
	                        print "Schedule 1hr P4 recordings on all the tuners"
	                        diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,3600000,"P4")
                                if 1 == diskFull:
                                    break
	                        #Repeat for 5 times
	                        print "Schedule 30min P4 recordings on all the tuners"
	                        for i in range(0,5):
		                    diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,1800000,"P4")
		                if 1 == diskFull:
			            break
                                #Repeat for 2 times
                                print "Schedule 10min P4 recordings on all the tuners"
                                for i in range(0,2):
                                    diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,600000,"P4")
		                    if 1 == diskFull:
			                break

	                    if 1 == diskFull:
		                print "DISKFULL! Pre-requisite met"
	                    else:
		                print "DISK NOT FULL! Pre-requisite not met"
		                tdkTestObj.setResultStatus("FAILURE");
				recObj.unloadModule("Recorder");
		                exit()
	                    #Pre-Req end: Disk should be full before starting test

                            #Waiting for the recording to get deleted
                            sleep(700);
                            print "Sending getRecordings to get the recording list"
                            recorderlib.callServerHandler('clearStatus',ip)
                            recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                            print "Wait for 1 min to get response from recorder"
                            sleep(60)
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording list after disk full",actResponse
                            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                            print "After disk full" ,recordingData
                            # code for checking the presence of recording data
                            tdkTestObj2=recObj.createTestStep('Recorder_PresenceOfRecordingMetaData');
                            expectedResult="SUCCESS";
                            tdkTestObj2.addParameter("Recording_Id",recordingID);
                            #Execute the test case in STB
                            tdkTestObj2.executeTestCase(expectedResult);
                            #Get the actual result and details of execution
                            result = tdkTestObj2.getResult();
                            details = tdkTestObj2.getResultDetails();
                            print result,",Metadata of ",recordingID," ",details
                            if "FAILURE" in result:
                                print "Metadata should not available at location /tmp/mnt/diska3/persistent/dvr/recdbser"
                                tdkTestObj2.setResultStatus("SUCCESS");
                            else:
                                print "Meta data is available /tmp/mnt/diska3/persistent/dvr/recdbser"
                                tdkTestObj2.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
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
