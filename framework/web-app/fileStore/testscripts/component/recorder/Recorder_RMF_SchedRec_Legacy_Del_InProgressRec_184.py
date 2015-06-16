'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_SchedRec_Legacy_Del_InProgressRec_184</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should include in full sync future legacy recording which is in progress that are deleted by user but not previously notified to RWS with Status=Erased</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
obj.configureTestCase(ip,port,'Recorder_RMF_SchedRec_Legacy_Del_InProgressRec_184');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        print "Rebooting box for setting configuration"
        obj.initiateReboot();
        print "Waiting for the recorder to be up"
        sleep(300);

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
        #Schedule Future Legacy Recording with 5 min duration
        duration = "300000";
        startTime = "60000";
        genIdInput = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success 1";
                sleep(90);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('acknowledgement' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";

                        #Cancel recording before deleting it
                        jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"cancelRecordings\":[\""+recordingID+"\"]}}";
                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgCancelRecording,ip);
                        print "updateSchedule Details for CancelRecording: %s"%actResponse;
                        sleep(30);

                        print "Delete the recording";
                        #Frame json message for update recording
                        jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";
                        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgUpdateRecording,ip);
                        print "updateRecordings Details: %s"%actResponse;
                        if "updateRecordings" in actResponse:
                                print "updateRecordings message post success";
                                sleep(30);
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                if ('NOTFOUND' not in recordingData):
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        if "ERASED" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recorder has sent status = Erased";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has not Erased";
                                else:
                                        print "Recording not found, so reboot the box for the full sync";
                                        #Execute updateSchedule
                                        requestID2 = str(randint(10, 500));
                                        recordingID2 = str(randint(10000, 500000));
                                        #Schedule a small recording and complete it for the full sync
                                        startTime2 = "0";
                                        duration = "60000"

                                        #Frame json message
                                        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
                                        print "serverResponse : %s" %serverResponse;
                                        sleep(90);

                                        obj.initiateReboot();
                                        print "Waiting for the recorder to be up"
                                        sleep(300);

                                        #Execute updateSchedule
                                        requestID2 = str(randint(10, 500));
                                        recordingID2 = str(randint(10000, 500000));
                                        #Schedule Hot Inline Recording with 1 min duration
                                        startTime2 = "0";

                                        #Frame json message
                                        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime2+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
                                        print "serverResponse : %s" %serverResponse;

                                        if "updateSchedule" in serverResponse:
                                                print "updateSchedule message post success 2";
                                                sleep(180);
                                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                print "Retrieve Status Details: ",recResponse;
                                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                                if ('NOTFOUND' not in recordingData):
                                                        key = 'status'
                                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                                        print "key: ",key," value: ",value
                                                        if "ERASED" in value.upper():
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "Recorder has sent status = Erased";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "Recorder has not sent Erased status";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Recording not found even after full sync";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "updateSchedule message post failed 2";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateRecordings message post failed";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server NOT received the recorder acknowledgement";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failed 1";

        #unloading Recorder module
        obj.unloadModule("Recorder");

