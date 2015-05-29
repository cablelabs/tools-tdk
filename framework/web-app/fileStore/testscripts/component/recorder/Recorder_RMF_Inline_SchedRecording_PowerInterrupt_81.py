'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Inline_SchedRecording_PowerInterrupt_81</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that an inline recording scheduled for future time is iterrupted by settop reboot is reported with Error=POWER_INTERRUPTION</synopsis>
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
obj.configureTestCase(ip,port,'Recorder_RMF_Inline_SchedRecording_PowerInterrupt_81');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

	print "Rebooting box for setting configuration"
	obj.initiateReboot();
	print "Waiting for the recoder to be up"
	sleep(300);

	#Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #5mins duration
        duration = "300000";
        startTime = "60000";
        genIdInput = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                sleep(90);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (( ([] == recResponse) or ('ack' not in recResponse) ) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "ack" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        print "Rebooting the box to get full sync..."

                        obj.initiateReboot();
                        print "Sleeping to wait for the recoder to be up"
                        sleep(300);
			response = recorderlib.callServerHandler('clearStatus',ip);
                        print "Sending noUpdate to get the recording list"
                        RequestURL = "{\"noUpdate\":{}}";
                        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        if "noUpdate" in serverResponse:
                                print "NoUpdate message post success";
                                print "Wait for 180sec to get the recording list"
                                sleep(180);
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print "Recording List: %s" %actResponse;

                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                print recordingData;
                                if ('NOTFOUND' not in recordingData):
                                        key = 'error'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        print "key: ",key," value: ",value
                                        if "POWER_INTERRUPTION" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recording had power interruption";
                                        elif "BADVALUE" == value.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recording did not have error field";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recording did not have power interruption";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording not found";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "NoUpdate message post failed";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        obj.unloadModule("Recorder");

