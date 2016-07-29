#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ===========================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Schedule_Backto_Back_Recordings_AndExtend_Duration_Inline_321</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Extend durations of back to back recordings happens on different channels</synopsis>
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
import time
from random import randint
from time import sleep


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Schedule_Backto_Back_Recordings_AndExtend_Duration_Inline_321');
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
	print "Sleeping to wait for the recoder to be up"

        
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
        duration = "360000";
        newDuration = "480000";
        startTime = "0";
        startTime1 = "360000";
        startTime2 = "720000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        ocapId3 = tdkTestObj.getStreamDetails('03').getOCAPID()
        now = "curTime"
       
        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime1+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"locator\":[\"ocap://"+ocapId3+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+2)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
 
        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        epoch_time = str(int(time.time()* 1000))
        print "EPOCH",epoch_time

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
	        print "Retrieve Status Details: %s"%actResponse;
		if 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received Empty/Error status";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    #Extending the duration after a sleep of 30 seconds
                    sleep(30);
                    jsonMsgUpdateRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"epoch\":"+epoch_time+",\"start\":"+startTime+",\"duration\":"+newDuration+"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"epoch\":"+epoch_time+",\"start\":"+startTime1+",\"duration\":"+newDuration+"},{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"epoch\":"+epoch_time+",\"start\":"+startTime2+",\"duration\":"+newDuration+"}]}}";
 

                    expResponse = "updateSchedule";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgUpdateRecording,ip);
                    print "updateSchedule Details: %s"%actResponse;
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateSchedule message post success";
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        while (('acknowledgement' not in actResponse) and (loop < 5)):
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10);
                                loop = loop+1;
                        print "Retrieve Status Details: %s"%actResponse;
                        if 'acknowledgement' in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                            print "Wait 20 minutes for recording to complete"
                            sleep(1200)                     
                            tdkTestObj.executeTestCase(expectedResult);
                            print "Sending getRecordings to get the recording list"
                            recorderlib.callServerHandler('clearStatus',ip)
                            recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                            print "Wait for 60 seconds to get response from recorder"
                            sleep(60);
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording List: %s" %actResponse;
                            recordingData1 = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                            recordingData2 = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1));
                            recordingData3 = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+2));
                            print recordingData1
                            print recordingData2
                            print recordingData3
                            if 'NOTFOUND' not in (recordingData1,recordingData2 and recordingData3):
                                print "Successfully retrieved the recording list from recorder";
                                tdkTestObj.setResultStatus("SUCCESS");
                                statusKey = 'status'
                                statusValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,statusKey)
                                statusValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,statusKey)
                                statusValue3 = recorderlib.getValueFromKeyInRecording(recordingData3,statusKey)
                                expDurationValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,'expectedDuration')
                                expDurationValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,'expectedDuration')
                                expDurationValue3 = recorderlib.getValueFromKeyInRecording(recordingData3,'expectedDuration')
                                actDurationValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,'duration')
                                actDurationValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,'duration')
                                actDurationValue3 = recorderlib.getValueFromKeyInRecording(recordingData3,'duration')

                                difference_duration1 = expDurationValue1 - actDurationValue1[0]
                                difference_duration2 = expDurationValue2 - actDurationValue2[0]
                                difference_duration3 = expDurationValue3 - actDurationValue3[0]
                        
                                if "COMPLETE" in (statusValue1.upper(),statusValue2.upper()and statusValue3.upper()):
                                    if (int(newDuration)in (int(expDurationValue1),int(expDurationValue2) and int(expDurationValue3) and (difference_duration1,difference_duration2 and difference_duration3) < 10000)):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Duration updated for Inprogress recording as expected";
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Duration NOT updated for Inprogress recording";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording not completed successfully";
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to retrieve the recording list from recorder";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "updateSchedule message post failed";
               
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        recObj.unloadModule("Recorder");
else:
    print "Load Module Failed"
    recObj.setLoadModuleStatus("FAILURE");
