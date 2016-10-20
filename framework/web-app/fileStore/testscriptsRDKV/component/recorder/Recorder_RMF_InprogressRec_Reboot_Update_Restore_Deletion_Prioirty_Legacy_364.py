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
  <name>Recorder_RMF_InprogressRec_Reboot_Update_Restore_Deletion_Prioirty_Legacy_364</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To update and restore the deletion priority of an in progress recording which is incomplete due to POWER_INTERRUPTION</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_InprogressRec_Reboot_Update_Restore_Deletion_Prioirty_Legacy_364');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
            print "Rebooting box for setting configuration"
            recObj.initiateReboot();
            print "Waiting for 5min for the recoder to be up"
	    sleep(300);
        
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
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
        duration = "500000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
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
                    print "Received Empty/Error statussss";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    print "Wait for the recording to be completed partially"
                    sleep(70);
                    #Reboot the box
                    recObj.initiateReboot();
                    print "Waiting for 5 min for recoder to be up"
                    sleep(300);
                    tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                    tdkTestObj.executeTestCase(expectedResult);
                    #Frame json message for update recording
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";

                    expResponse = "updateRecordings";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
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
                            sleep(120);
                            #Frame json message for update recording
			    jsonMsgRestoreRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P4\"}]}}";
			    expResponse = "updateRecordings";
                            tdkTestObj.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgRestoreRecording,ip);
                            print "updateRecordings Details: %s"%actResponse;
                            if expResponse in actResponse:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "updateRecordings message post success2";
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
                                    sleep(120);
                                    print "Sending getRecordings to get the recording list"
                                    recorderlib.callServerHandler('clearStatus',ip)
                                    recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                    print "Wait for 60 seconds to get response from recorder"
                                    sleep(60)
                                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                    print "Recording List: %s" %actResponse;
                                    recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                    print recordingData
                                    if 'NOTFOUND' not in recordingData:
                                        print "Successfully retrieved the recording list from recorder";
                                        statusValue = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                        deletePriority = recorderlib.getValueFromKeyInRecording(recordingData,'deletePriority')
                                        if "INCOMPLETE" in statusValue.upper() and "P4" in deletePriority.upper():
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "Recording delete priority updated successfully";
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "Recording delete priority NOT updated successfully";

                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to retrieve the recording list from recorder";
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

