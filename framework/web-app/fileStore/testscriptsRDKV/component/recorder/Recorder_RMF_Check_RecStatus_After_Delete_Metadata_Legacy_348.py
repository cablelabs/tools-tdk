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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Check_RecStatus_After_Delete_Metadata_Legacy_348</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recording details should be there after deleting metadata unless there is a reboot happened in the box</synopsis>
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

        print "Deleting recording Metadata"
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
