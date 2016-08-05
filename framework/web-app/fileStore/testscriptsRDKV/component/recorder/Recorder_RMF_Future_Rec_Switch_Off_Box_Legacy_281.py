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
  <name>Recorder_RMF_Future_Rec_Switch_Off_Box_Legacy_281</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should sent erased status for a recording where the  box is in off state for the whole duration of that recording</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Future_Rec_Switch_Off_Box_Legacy_281');
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
        duration = "10000";
        startTime = "60000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

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
                print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Successfully retrieved acknowledgement from recorder";
                        sleep(30);
                        #Reboot the box
                        recObj.initiateReboot();
                        print "Waiting for 5min for recoder to be up"
                        sleep(300);
                        expResponse = "noUpdate";
		    	tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                    	tdkTestObj.executeTestCase(expectedResult);
                    	actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                    	if expResponse in actResponse:
                        	print "No Update Schedule message post success";
                        	print "Wait for some time to get the recording list"
	                        sleep(60);
	                        tdkTestObj.setResultStatus("SUCCESS");
        	                #Check for acknowledgement from recorder
                        	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
				print "Response after first full sync: " ,actResponse;
                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                 	       	print recordingData
      	                	if 'NOTFOUND' not in recordingData:
                                    key = 'status'
                                    value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                    print "key: ",key," value: ",value
                                    print "Successfully retrieved the recording list from recorder";
                                    if "ERASED" in value.upper():
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recorder sent ERASED status";
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder NOT sent ERASED status";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Failed to retrieve the recording list from recorder";
                        else:
                            print "No Update Schedule message post failed";
                            tdkTestObj.setResultStatus("FAILURE");   
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Simulator Server failed to receive acknowledgement from recorder";
        else:
            print "updateSchedule message post failure";
            tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");