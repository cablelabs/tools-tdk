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
  <name>Recorder_RMF_PowerInterrupt_CheckRecRestart_228</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that recording will restart/resume after a power interruption</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>90</execution_time>
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
obj.configureTestCase(ip,port,'Recorder_RMF_PowerInterrupt_CheckRecRestart_228');
#Get the result of connection with test component and STB
recLoadStatus = obj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus ;
#Set the module loading status
obj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               obj.initiateReboot();
               print "Waiting for 5min for the recoder to be up"
	       sleep(300);

	#Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #10mins duration
        duration = "600000"
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                print "Looping till acknowledgement is received"
                loop = 0;
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (('ack' not in actResponse) and (loop < 5)):
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    sleep(10);
                    loop = loop+1;
                print "Retrieve Status Details: ",actResponse
                if "acknowledgement" in actResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        response = recorderlib.callServerHandler('clearStatus',ip)
                        print "Wait for 5 min before causing power interrupt"
                        sleep(120)
                        obj.initiateReboot();
                        print "Waiting for 5min for recoder to be up"
                        sleep(300);
                        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Wait for remaining 5 min recording to complete"
                        sleep(200)
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                        #Wait to get response from recorder
                        sleep(60)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                        if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE")
                                print "RecordingId not found in list"
			else:
                                print "Recording data for recordingID ",recordingID, " is ",recordingData
                                statusValue = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                actualduration = recorderlib.getValueFromKeyInRecording(recordingData,'duration')
                                totalduration = actualduration[0] + actualduration[1]
                                print "status: ", statusValue
                                print "actualduration:" , totalduration
                                if "INCOMPLETE" in statusValue.upper() and (len(actualduration) == 2): 
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recording passed verification after power interruption"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording NOT passed verification after power interruption"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");
