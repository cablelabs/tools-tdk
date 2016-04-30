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
  <name>Recorder_RMF_Inline_HotRec_LPSDownFor90Sec_FullSched_79</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that recorder requests a full schedule when heartbeat dots are not received on Longpoll connection for 90 seconds when inline hot recording is scheduled</synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import recorderlib
from time import sleep
from random import randint

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Inline_HotRec_LPSDownFor90Sec_FullSched_79');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

        print "Rebooting box for setting configuration"
	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);

        print "Sleeping to wait for the recoder to be up"


        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Inline HotRecording updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #2min duration
        duration = "120000";
        startTime = "0";
        genIdInput = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                #Wait for acknowlegment
                sleep(60);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                print "Retrieve Status Details: ",recResponse;
                if "ack" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        response = recorderlib.callServerHandler('clearStatus',ip);
                        print "Disable LPServer"
                        #Disable LPServer
                        recorderlib.callServerHandlerWithType('disableServer','LPServer',ip)
                        status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
                        print "Longpoll server status: ",status
                        if "FALSE" in status.upper():
                                print "Wait for more than 90sec"
                                sleep (100)
                                print "Enable longpoll server connection"
                                recorderlib.callServerHandlerWithType('enableServer','LPServer',ip)
                                status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
                                print "Longpoll server status: ",status
                                if "FALSE" in status.upper():
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to enable LP Server"
                                else:
                                        print "Enabled LP Server"
                                        print "Wait for recorder to establish connection with longpoll server"
                                        sleep (220)
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Recorder response: %s" %actResponse;
                                        print "Sending getRecordings to get the recording list"
                                        recorderlib.callServerHandler('clearStatus',ip)
                                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                        print "Wait for 60 seconds to get response from recorder"
                                        sleep(60);
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                        print "Recording List: %s" %actResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                        print recordingData
                                        if 'NOTFOUND' == recordingData:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "Recording not found in list";
                                        else:
                                            key = 'status'
                                            value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                            print "key: ",key," value: ",value
                                            if "COMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Scheduled recording completed successfully";
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Scheduled recording did not complete successfully";
                        else:
                                print "Failed to disable LP Server"
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");

