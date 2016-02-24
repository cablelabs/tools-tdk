'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_HotRec_Legacy_IncompleteStatus_114</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should send Incomplete notification if the recording(hot, Legacy) has been interrupted by another recording before the first recording completed</synopsis>
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
obj.configureTestCase(ip,port,'Recorder_RMF_HotRec_Legacy_IncompleteStatus_114');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
	       print "Rebooting box for setting configuration"
               obj.initiateReboot();
	       print "Waiting for the recoder to be up"
	       sleep(300);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',"{\"noUpdate\":{}}",ip);
        sleep(10);
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #3mins duration
        duration = "180000";
        startTime = "0";
        genIdInput = "TDK456";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success for recording 1";
                sleep(10);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (('acknowledgement' not in recResponse) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details for recording 1: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement for recording 1";
                        print "Wait for some time to make partial recording 1";
                        sleep(20);
                        print "Send request for recording 2";

                        requestID2 = str(randint(10, 500));
                        recordingID2 = str(randint(10000, 500000));
			duration = "60000";
			
			response = recorderlib.callServerHandler('clearStatus',ip);
                        #Frame json message
                        RequestURL2 = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                        serverResponse2 = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL2,ip);
                        if "updateSchedule" in serverResponse2:
                                print "updateSchedule message post success for recording 2";
                                recResponse2 = recorderlib.callServerHandler('retrieveStatus',ip);
                                retry = 0;
                                while (('acknowledgement' not in recResponse2) and (retry < 10 )):
                                        sleep(10);
                                        recResponse2 = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                                print "Retrieve Status Details for recording 2: ",recResponse2;
                                print "Wait for recording 2 to complete";
                                sleep(60);
				response = recorderlib.callServerHandler('clearStatus',ip);
				print "Get the list of recordings"
				recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
				print "Wait for 60 sec to fetch the list"
				sleep(60);
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print "Recording list: ",actResponse;
                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                print "Printing recording data: ", recordingData;
                                if ('NOTFOUND' not in recordingData):
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        if "INCOMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recorder has sent status = InComplete";
                                        elif "COMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = complete";
                                        elif "STARTED" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = started";
                                        elif "FAILED" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = Failed";
                                        elif "STARTEDINCOMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = StartedIncomplete";
                                        elif "PENDING" in value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent status = pending";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recorder has sent some other status";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder not sent any status for the recording 1 which was interrupted";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateSchedule message post failed for recording 2";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server NOT received the recorder acknowledgement for recording 1";
        else:
                print "updateSchedule message post failed for recording 1";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");
