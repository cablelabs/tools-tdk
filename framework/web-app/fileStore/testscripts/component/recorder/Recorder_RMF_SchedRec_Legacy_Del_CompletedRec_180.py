'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_SchedRec_Legacy_Del_CompletedRec_180</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should include in full sync future legacy recording that are deleted by user but not previously notified to RWS with Status=Erased</synopsis>
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
obj.configureTestCase(ip,port,'Recorder_RMF_SchedRec_Legacy_Del_CompletedRec_180');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

	loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               obj.initiateReboot();
               print "Waiting for the recorder to be up"
	       sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #Recording with 1 min duration
        duration = "60000";
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                sleep(20);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while (('statusMessage' not in recResponse) and (retry < 10 )):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknowledgement" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        recResponse = recorderlib.callServerHandler('clearStatus',ip);
                        print "Wait 60s for recording to complete";
                        sleep(60)
                        print "Delete the recording";
                        #Frame json message for update recording
                        requestID = str(randint(10, 500));
                        jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"}]}}";
                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
                        if "updateRecordings" in actResponse:
                                print "updateRecordings message post success";
                                sleep(30);
                                retry = 0
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while (('statusMessage' not in recResponse) and (retry < 10 )):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                                print "Retrieve Status Details: ",recResponse;
                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                                if ('NOTFOUND' not in recordingData):
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                        print "recordingID: ",recordingID," status: ",value
                                        if "ERASED" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Recorder sent Erased notification to the RWS for deleted recording";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recording is not in erased state";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recorder did not send recordingStatus notification to the RWS for deleted recording";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateRecordings message post failed";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Simulator Server did not receive recorder acknowledgement";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failed";

        #unloading Recorder module
        obj.unloadModule("Recorder");
