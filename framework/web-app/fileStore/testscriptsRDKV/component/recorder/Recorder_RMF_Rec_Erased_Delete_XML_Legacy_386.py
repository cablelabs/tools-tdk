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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Rec_Erased_Delete_XML_Legacy_386</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check the status of a completed recording after deleting it's XML's</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script 
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Rec_Erased_Delete_XML_Legacy_386');
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
	msg = recorderlib.getStatusMessage(actResponse);
        if "" == msg:
               	value = "FALSE";
	        print "No status message retrieved"
	     	tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
        print "Retrieved status message";
	value = msg['recordingStatus']["initializing"];
	print "Initializing value: %s"%value;
	if "TRUE" not in value.upper():
           	print "Failed to retrieve the recording list from recorder";
	        tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
        print "Retrieved the recording list from recorder";
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

        requestID2 = str(randint(10,500));
        recordingID2 = str(randint(10000, 500000));
	duration = "120000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse not in actResponse:
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
        while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
		sleep(5);
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		retry += 1
	#print "Retrieve Status Details: %s"%actResponse;
        if (('ERROR' in actResponse)):
		tdkTestObj.setResultStatus("FAILURE");
        	print "Received Empty/Error status";
        	recObj.unloadModule("Recorder");
		exit();
        print "Received status";
      	if 'acknowledgement' not in actResponse:
        	tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve acknowledgement from recorder";
        	recObj.unloadModule("Recorder");
		exit();
        print "Successfully retrieved acknowledgement from recorder";
	print "Wait for the recording to complete "
	sleep(150);
        recorderlib.callServerHandler('clearStatus',ip)
	# end of Perform 2nd  recording
        #Reboot the STB before starting the recording
        print "Rebooting the STB to get the recording list from full sync"
        recObj.initiateReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300);

        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        #Frame json message
        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip)
        sleep(60)
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recording List: %s" %actResponse;
        print "Retrieved the recording list from recorder";
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print recordingData
        if 'NOTFOUND' in recordingData:
        	tdkTestObj.setResultStatus("FAILURE");
        	print "Failed to get the recording data of first recording";
        	recObj.unloadModule("Recorder");
		exit();
        print "Successfully retrieved the recording data";
	# end of full sync for recording list 
	# check for status and error of 1st recording ... erased and orphaned 
 	key = 'status'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	print "key: ",key," value: ",value
        if "" == value.upper():
		print "Recording status not set";
                tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording status set";
	if "ERASED" not in value.upper():
       		tdkTestObj.setResultStatus("FAILURE");
	        print "Recording not marked as ERASED when it's XML's are missing";
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording marked as ERASED when it's XML's are missing";
 	key = 'error'
        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	print "key: ",key," value: ",value
        if "" == value.upper():
		print "Recording error not set";
                tdkTestObj.setResultStatus("FAILURE");
        	recObj.unloadModule("Recorder");
		exit();
	print "Recording error set";
	if "ORPHANED" not in value.upper():
       		tdkTestObj.setResultStatus("FAILURE");
	        print "error not marked as ORPHANED when it's XML's are missing";
        	recObj.unloadModule("Recorder");
		exit();
	print "error marked as ORPHANED when it's XML's are missing";
	# end of check for status and error of 1st recording ... erased and orphaned 
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");

					
