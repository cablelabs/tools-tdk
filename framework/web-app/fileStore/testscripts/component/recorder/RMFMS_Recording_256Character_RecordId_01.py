'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>8</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Recording_256Character_RecordId_01</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To Initiate recording with recording Id of length 256 characters and verify it is successful or not.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_01
Test Type: Positive</synopsis>
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
    <box_type>Emulator-HYB</box_type>
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
import re;
import random;
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
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_01');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
               print "Sleeping to wait for the recoder to be up"
               sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

	#Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        rec_id = random.randrange(10**9, 10**256)
        recording_id = str(rec_id);
	requestID = "7";
        duration = "180000";
        start_time = "0";
	now = "curTime"
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                print "ocapid : %s" %validid;
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
                Jsonurldetails = tdkTestObj.getResultDetails();
                print "Result of scheduling : %s" %actualresult;
                print "Jsonurldetails is : %s" %Jsonurldetails;
                if expectedresult in actualresult:
                        print "Recorder received the requested recording url";
                        tdkTestObj.setResultStatus("SUCCESS");
                        time.sleep(30);
			RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recording_id+"\",\"locator\":[\"ocap://"+validid+"\"],\"epoch\":"+now+",\"start\":"+start_time+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_256\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
			print "RequestURL (HARD CODED) is : %s" %RequestURL ;
			serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        print "serverResponse : %s" %serverResponse;
                        if "updateSchedule" in serverResponse:
                                print "updateSchedule message post success";
				sleep(60);				
                                retry = 0;
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while (( ('[]' in recResponse) or ('ack' not in recResponse) ) and ('ERROR' not in recResponse) and (retry < 10)):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
					print "Retrieve Status Details: %s" %recResponse;
                                if "acknowledgement" in recResponse:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "TDK_Server received the recorder acknowledgement";
                                        time.sleep(100);
                                        #Prmitive test case which associated to this Script
                                        tdkTestObj = obj.createTestStep('Recorder_checkRecording_status');
                                        PATTERN = recording_id;
                                        tdkTestObj.addParameter("Recording_Id",recording_id);
                                        #Execute the test case in STB
                                        expectedresult="SUCCESS";
                                        tdkTestObj.executeTestCase(expectedresult);
                                        #Get the Actual result of streaming Interface
                                        actualresult = tdkTestObj.getResult();
                                        print "In script **********************"
                                        patterndetails = tdkTestObj.getResultDetails();
                                        print "Pattern details is : %s" %patterndetails;
                                        duration_int = int(duration);
                                        duration_sec = duration_int/1000;
                                        duration_string = str(duration_sec);
                                        print duration_string;
					#compare the actual result with expected result
                                        if expectedresult in actualresult:
                                                if (PATTERN in patterndetails):
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        #Getting the mplayer log file from DUT
                                                        logpath=tdkTestObj.getLogPath();
                                                        print "Log path : %s" %logpath;
                                                        tdkTestObj.transferLogs(logpath,"false");
                                                        print "Successfully scheduled a Recording";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        #Getting the mplayer log file from DUT
                                                        logpath=tdkTestObj.getLogPath();
                                                        print "Log path : %s" %logpath;
                                                        tdkTestObj.transferLogs(logpath,"false");
                                                        print "Recording is not completed with requested duration";
                                        else:
                                                print "Failed to schedule a Recording";
                                                tdkTestObj.setResultStatus("FAILURE");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "TDK_Server failed to receive the recorder acknowledgement";
                        else:
                                print "updateSchedule message post failure";
                                tdkTestObj.setResultStatus("FAILURE");
                else:
			tdkTestObj.setResultStatus("FAILURE");
			print "Recorder NOT received the requested recording url";
                #unloading Recorder module
                obj.unloadModule("Recorder");
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");

