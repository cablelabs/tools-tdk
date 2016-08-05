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
  <name>Recorder_RMF_GetRecordingsList_with_updateSchedule_43</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_43 - Recorder - To send initializing=true if and only if the recordingStatus contains ALL past, present, and future recordings on the box. Get recording list by sending updateSchedule after reboot</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
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
recObj.configureTestCase(ip,port,'Recorder_RMF_GetRecordingsList_with_updateSchedule_43');
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
	sleep(30);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

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
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                tdkTestObj.executeTestCase(expectedResult);
                print "Waiting to get acknowledgment status"
                sleep(5);
                retry = 0;
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
                        sleep(5);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry = retry+1;
                print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    print "Wait for 60s for the recording to be completed"
		    sleep(60);
		    print "Get the recording list from recorder"
		    response = recorderlib.callServerHandler('clearStatus',ip);
                    recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)		    
		    print "Wait for 60sec to get the recording list"
                    sleep(60);
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		    print actResponse;
		    msg = recorderlib.getStatusMessage(actResponse);
                    if "" == msg:
                            value = "FALSE";
                            print "No status message retrieved"
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
			    value = msg['recordingStatus']["initializing"];
			    print "Initializing value: %s"%value;
			    if "TRUE" in value.upper():
                                print "Successfully retrieved the recording list from recorder"
                        	recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                       		print recordingData
                        	if 'NOTFOUND' not in recordingData:
                            		key = 'status'
                            		value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                            		print "key: ",key," value: ",value
                            		print "Successfully retrieved the recording list from recorder";
                            		if "COMPLETE" in value.upper():
                                		tdkTestObj.setResultStatus("SUCCESS");
                                		print "Scheduled recording completed successfully";
                            		else:
                                		tdkTestObj.setResultStatus("FAILURE");
                                		print "Scheduled recording not completed successfully";
			        else:
                                	tdkTestObj.setResultStatus("FAILURE");
                                	print "Failed to get the recording data";
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