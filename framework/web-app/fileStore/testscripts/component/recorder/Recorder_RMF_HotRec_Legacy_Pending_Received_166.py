'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_HotRec_Legacy_Pending_Received_166</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should send Pending status in a full sync when a hot legacy recording is scheduled</synopsis>
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
obj.configureTestCase(ip,port,'Recorder_RMF_HotRec_Legacy_Pending_Received_166');
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
        #For full sync, schedule a small recording with 1 min duration and wait till it ends
        duration = "60000";
        startTime = "0";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
        print "serverResponse recording 1: %s" %serverResponse;
        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success for first recording before reboot";
                sleep(90);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('acknowledgement' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement for recording 1";
                        print "Reboot the box and schedule new recording 2";
                        obj.initiateReboot();
                        print "Waiting for the recoder to be up"
                        sleep(300);

                        #Execute updateSchedule
                        requestID2 = str(randint(10, 500));
                        recordingID2 = str(randint(10000, 500000));
                        # After reboot schedule Hot Legacy recording in order to get pending status
                        startTime2 = "0";

                        # Keep checking the status for every 10sec, so calculate loop time in seconds: startTime + duration + 1min offset
                        endtime = (int(duration)/1000) + (int(startTime2)/1000) + 30;
                        print('Wait time: '+str(endtime));

                        #Frame json message
                        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        print "serverResponse recording 2 after reboot: %s" %serverResponse;
                        if "updateSchedule" in serverResponse:
                                print "updateSchedule message post success for second recording after reboot";
                                ackflag = 0;
                                pendingflag = 0;

                                while (endtime > 0):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);

                                        if ('acknowledgement' in recResponse):
                                                ackflag = 1;

                                        recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID2);
                                        if ('NOTFOUND' not in recordingData):
                                                key = 'status'
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                                print "key: ",key," value: ",value
                                                if "PENDING" in value.upper():
                                                        print "Recorder has sent status = Pending";
                                                        pendingflag = 1;
                                                        break;

                                        endtime = endtime - 10;

                                print "Retrieve Status Details: ",recResponse;
                                print "Printing recording data:";
                                print recordingData;

                                if (ackflag == 0):
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Simulator Server failed to receive acknowledgement from recorder";
                                elif (pendingflag == 0):
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder has not sent pending status";
                                else:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Acknowledgement received and also recorder has sent pending status";
        else:
                print "updateSchedule message post failed for first recording before reboot";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");

