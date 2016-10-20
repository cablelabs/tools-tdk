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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_HotRec_Inline_Error_Became_Playable_220</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should send Error=BECAME_PLAYABLE for hot inline recording if 5-second requirement is subsequently met after already sending NOT_YET_PLAYABLE</synopsis>
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
obj.configureTestCase(ip,port,'Recorder_RMF_HotRec_Inline_Error_Became_Playable_220');
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


        #Primitive test case for changing threshold value
        rmfConfObj = obj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RECORDER.INCOMPLETETHRESHOLD";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="1000";
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details = rmfConfObj.getResultDetails();
        print result,","," ",details
        if "FAILURE" in result:
                print "Failed to change the threshold value"
                rmfConfObj.setResultStatus("FAILURE");
                obj.unloadModule("Recorder");
                exit();
        print "Changed the threshold value"
        rmfConfObj.setResultStatus("SUCCESS");
        sleep(5);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        print "Sending noUpdate to get the recording list after full sync"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        sleep(10);
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #3mins duration
        duration = "600000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        ocapId3 = tdkTestObj.getStreamDetails('03').getOCAPID()
        ocapId4 = tdkTestObj.getStreamDetails('04').getOCAPID()

        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"locator\":[\"ocap://"+ocapId3+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+2)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+3)+"\",\"locator\":[\"ocap://"+ocapId4+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+3)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                sleep(10);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('acknowledgement' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        print actResponse
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                        print recordingData;
                        if ('NOTFOUND' not in recordingData):
                            key = 'Error'
                            value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                            print "key: ",key," value: ",value
                            if "BECAME_PLAYABLE" in value.upper():
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Recorder has sent Error = BECAME_PLAYABLE as expected";
                            else:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Recorder has not sent Error = BECAME_PLAYABLE";
                        else:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Recording not found";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #Primitive test case for changing threshold value
        rmfConfObj = obj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RECORDER.INCOMPLETETHRESHOLD";
        rmfConfObj.addParameter("Keyword",Keyword);
        # Reset to the previous value
        rmfConfObj.addParameter("Value",details);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details = rmfConfObj.getResultDetails();
        print result,","," ",details
        if "FAILURE" in result:
                print "Failed to revert the threshold value"
                rmfConfObj.setResultStatus("FAILURE");
                obj.unloadModule("Recorder");
                exit();
        print "Reverted the threshold value"

        #unloading Recorder module
        obj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
