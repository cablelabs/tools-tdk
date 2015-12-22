'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Recording_Grt_Than_256Character_RecordId_05</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To Initiate recording with recording Id of length more then 256 characters.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_05
Test Type: Negative</synopsis>
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
obj.configureTestCase(ip,port,'RMFMS_Recording_Grt_Than_256Character_RecordId_05');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
               sleep(300);

	recorderlib.callServerHandler('clearStatus',ip)

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        rec_id = random.randrange(10**9, 10**258)
        recording_id = str(rec_id);
        duration = "60000";
        start_time = "0";
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
                Jsonurldetails = tdkTestObj.getResultDetails();
		RequestURL = Jsonurldetails.replace("${now}","curTime");
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        time.sleep(10);
			RequestURL="{\"updateSchedule\":{\"requestId\":\"7\",\"generationId\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recording_id))+"\",\"locator\":[\"ocap://"+validid+"\"],\"epoch\":curTime,\"start\":"+start_time+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+str(int(recording_id))+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
			serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
			if "updateSchedule" in serverResponse:
                                print "updateSchedule message post success";
                                sleep(10);
                                retry = 0;
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while ( ('acknow' not in recResponse) and (retry < 10)):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                                print "Retrieve Status Details: %s" %recResponse;						
				if "acknow" in recResponse:
					tdkTestObj.setResultStatus("SUCCESS");
					print "Received acknowlegement from recorder";
					print "Wait for recording to complete"
					time.sleep(60);

                        		print "Sending getRecordings to get the recording list"
                        		recorderlib.callServerHandler('clearStatus',ip)
                        		recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        		print "Wait for 1 min to get response from recorder"
                        		sleep(60)
                        		actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        		print "Recording List: %s" %actResponse;
                        		recordingData = recorderlib.getRecordingFromRecId(actResponse,recording_id);
                        		print recordingData;
                        		if 'NOTFOUND' in recordingData:
						tdkTestObj.setResultStatus("SUCCESS");
						print "Recorder did not create recording with ID more than 256 characters";
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print "Recorder created recording with ID more than 256 characters";
				else:
					tdkTestObj.setResultStatus("FAILURE");
					print "Failed to Receive acknowledgement from recorder";
			else:
				tdkTestObj.setResultStatus("FAILURE");
                                print "updateSchedule message post failed";			
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Recorder Failed to receive the requested request-Please check precondition";

        #unloading Recorder module
        obj.unloadModule("Recorder");
