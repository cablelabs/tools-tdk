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
  <id>992</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Schedule_MinDuration_Recording_18</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test is to check scheduling a recording for minimum duration.
Test Case Id: CT_Recorder_7</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
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
obj.configureTestCase(ip,port,'RMFMS_Schedule_MinDuration_Recording_18');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               obj.initiateReboot();
               print "Waiting for the recoder to be up"
	       sleep(300);

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Complete a recording to change check sum
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #3mins duration
        duration = "30000";
        startTime = "0";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
        sleep(40);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #5mins duration
        duration = "6000";
        startTime = "60000";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                sleep(10);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ('acknow' not in recResponse) ) and (retry < 5 )):
                        sleep(5);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknow" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
			#WAIT for start time to elapse
			sleep(60);
			#WAIT for recording duration to elapse
                        sleep(10);
			print "Sending getRecordings to get the recording list"
			recorderlib.callServerHandler('clearStatus',ip)
			recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
			print "Wait for 60s to get response from recorder"
			sleep(60)
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
			print "Recording List: %s" %actResponse;
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                        print recordingData
                        if ('NOTFOUND' not in recordingData):
                                key = 'status'
                                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                print "key: ",key," value: ",value
                                if "COMPLETE" in value.upper():
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recording has complete status for the duration=5seconds";
                                elif "BADVALUE" == value.upper():
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording did not have status field";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording not have complete status for the duration=5seconds";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Recording not found";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");
