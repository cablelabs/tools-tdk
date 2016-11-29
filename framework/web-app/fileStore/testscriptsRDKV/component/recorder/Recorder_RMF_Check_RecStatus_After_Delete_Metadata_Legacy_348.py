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
  <name>Recorder_RMF_Check_RecStatus_After_Delete_Metadata_Legacy_348</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recording details should be there after deleting metadata unless there is a reboot happened in the box</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_348</test_case_id>
    <test_objective>Recording details should be there after deleting metadata unless there is a reboot happened in the box using legacy</test_objective>
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
3.Schedule a hot recording of 2 minute duration  using legacy
4.Wait for the recording to complete
5. Delete the meta data of the recording including backup file
6. Using getRecordings message retrieve the recording details and check the recording details are there.
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Recording details should be available</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_ExecuteCmd</test_stub_interface>
    <test_script>Recorder_RMF_Check_RecStatus_After_Delete_Metadata_Legacy_348</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import recorderlib
from sys import exit
from random import randint
from time import sleep

#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_RecStatus_After_Delete_Metadata_Legacy_348');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);
	#print "Sleeping to wait for the recoder to be up"

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10,500));
        recordingID = str(randint(10000, 500000));
	duration = "120000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";
	genIdInput = recordingID;

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        print "Schedule new recording"
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

        if "updateSchedule" not in actResponse:
	        tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failure";
        	recObj.unloadModule("Recorder");
		exit();
        print "updateSchedule message post success";
        tdkTestObj.executeTestCase(expectedResult);
	print "Waiting to get acknowledgment status"
	sleep(5);
	retry=0
	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
        while (('acknowledgement' not in actResponse) and (retry < 15)):
		sleep(5);
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		retry += 1
	print "Retrieve Status Details: %s"%actResponse;
      	if 'acknowledgement' not in actResponse:
        	tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve acknowledgement from recorder";
        	recObj.unloadModule("Recorder");
		exit();
        print "Successfully retrieved acknowledgement from recorder";
	print "Wait for the recording to complete "
	sleep(130);

        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        print "Sending getRecordings to get the recording list"
        recorderlib.callServerHandler('clearStatus',ip)
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 60 seconds to get response from recorder"
        sleep(60)
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print recordingData
        if 'NOTFOUND' in recordingData:
        	tdkTestObj.setResultStatus("FAILURE");
        	print "Failed to get the recording data";
        	recObj.unloadModule("Recorder");
		exit();
        print "Successfully retrieved the recording data";
 	key = 'status'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	print "key: ",key," value: ",value
        if "" == value.upper():
		print "Recording status not set";
                tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording status set";
	if "COMPLETE" not in value.upper():
       		tdkTestObj.setResultStatus("FAILURE");
	        print "Recording not marked as COMPLETE";
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording marked as COMPLETE ";
    
        print "Deleting Blobs including backup"
        tdkTestObj1 = recObj.createTestStep('Recorder_ExecuteCmd');
        expectedResult="SUCCESS";
        tdkTestObj1.addParameter("command","find /tmp/mnt/diska3/persistent/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");


        tdkTestObj1.addParameter("command","find /mnt/nvram1/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");


        tdkTestObj1.addParameter("command","find /opt/persistent/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");
       
        tdkTestObj1.addParameter("command","find /tmp/mnt/diska3/dvr_persistent/dvr/recdbser -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        print "Deleting XML's including backup"
        tdkTestObj1 = recObj.createTestStep('Recorder_ExecuteCmd');
        expectedResult="SUCCESS";
        tdkTestObj1.addParameter("command","find /opt/data/OCAP_MSV/0/0/DEFAULT_RECORDING_VOLUME/dvr -type f -name \"*.xml*\" -mmin -3 | xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        sleep(10);

        tdkTestObj.executeTestCase(expectedResult);
        #Frame json message
        print "Sending getRecordings to get the recording list"
        recorderlib.callServerHandler('clearStatus',ip)
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        sleep(60)
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recording List: %s" %actResponse;
        print "Retrieved the recording list from recorder after deleting metadata";
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print recordingData
        if 'NOTFOUND' in recordingData:
        	tdkTestObj.setResultStatus("FAILURE");
        	print "Failed to get the recording data of recording";
        	recObj.unloadModule("Recorder");
		exit();
        print "Successfully retrieved the recording data";
 	key = 'status'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	print "key: ",key," value: ",value
        if "" == value.upper():
		print "Recording status not set";
                tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording status set";
	if "COMPLETE" not in value.upper():
       		tdkTestObj.setResultStatus("FAILURE");
	        print "Recording not marked as COMPLETE";
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording details are available and  marked as COMPLETE";
        tdkTestObj.setResultStatus("SUCCESS");
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");

