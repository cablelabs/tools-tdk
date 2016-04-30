#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Verify_RedundantStatus_PowerInterrupt_146</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_146 - Recorder should not send redundant recording statuses; new status only needs to be sent if number of playable segments has changed or status has changed (change in Error code only does not require status to be re-sent) - Checking by creating power interruption failure</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Verify_RedundantStatus_PowerInterrupt_146');
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
        duration = "300000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                print "Waiting to get acknowledgement"
                sleep(10);
                #Check for acknowledgement from recorder
		print "Looping till acknowledgement is received"
		loop = 0;
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		while 'acknowledgement' not in actResponse and loop < 5:
	                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			sleep(10);
			loop = loop+1;
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    print "Wait for 60s for the recording to be partially completed"
		    sleep(60)
		    response = recorderlib.callServerHandler('clearStatus',ip);
                    # Reboot the STB
		    print "Rebooting the STB to cause power interrupt"
		    recObj.initiateReboot();
		    print "Sleeping to wait for the recoder to be up"
		    sleep(300);
		    #Frame json message
		    tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                    tdkTestObj.executeTestCase(expectedResult);
		    print "Get the recording list from recorder"
   		    recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
		    print "Wait for 60sec to get the recording list"
		    sleep(60)
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		    print "Recording List: ", actResponse;
                    recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                    print recordingData
                    if 'NOTFOUND' not in recordingData:
			    print "Successfully retrieved recording ID in recording list";
                            error = recorderlib.getValueFromKeyInRecording(recordingData,'error')
                            if "POWER_INTERRUPTION" in error.upper():
                                print "Power interruption happened properly when recording is inprogress";
                                response = recorderlib.callServerHandler('clearStatus',ip);
                                print "Clear Status after getting status from RWS: %s"%response;
                                response = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(60);
                                print "Retrieve Status after getting status from RWS: %s"%response;
                                recordingData = recorderlib.getRecordingFromRecId(response,recordingID)
                                print recordingData
                                if 'NOTFOUND' in recordingData:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "No redundant recording status retrieved from recorder"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Redundant recording status retrieved from recorder"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Power interruption not happened properly when recording is inprogress";
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve recording ID in recording list";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
