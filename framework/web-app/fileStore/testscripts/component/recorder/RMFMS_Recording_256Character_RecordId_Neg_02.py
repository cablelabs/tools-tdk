'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>14</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Recording_256Character_RecordId_Neg_02</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To Initiate recording with recording Id of length 256 characters and value given is negative.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_02
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>25</execution_time>
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
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_Neg_02');
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

        response = recorderlib.callServerHandler('clearStatus',ip);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        negate = "-"
        rec_id = random.randrange(10**9, 10**255)
        recording_id = negate + str(rec_id);
        duration = "60000";
        start_time = "0";
        requestID = str(randint(10,500));
	genIdInput = requestID;
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
     	        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"schedule\":[{\"recordingId\":\""+recording_id+"\",\"locator\":[\"ocap://0x125d\"],\"epoch\":curTime,\"start\":0,\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recording_id+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        status_expected = "updateSchedule";
        		expectedResult="SUCCESS";
			tdkTestObj.executeTestCase(expectedResult);
			status_actual = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        if status_expected in status_actual:
                                tdkTestObj.setResultStatus("SUCCESS");
                		print "updateSchedule message post success";
                		tdkTestObj.executeTestCase(expectedResult);
				print "Waiting to get acknowledgment status"
				sleep(10);
				retry=0
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		                while (('ack' not in actResponse) and (retry < 5)):
					sleep(10);
					actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
					retry += 1
				print "Retrieve Status Details:\n %s \n"%actResponse;
		                if 'acknowledgement' in actResponse:
                			tdkTestObj.setResultStatus("SUCCESS");
		                    	print "Successfully retrieved acknowledgement from recorder";

					print "Wait for recording to complete"
					sleep(60)

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
                                                print "As expected failed to schedule a Recording with negative recordID";
                                        else:
                                                print "Recorder scheduled a Recording with negative recordID";
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                if "COMPLETE" in value.upper():
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Created recording with negative recordID";
                                                else:
                                                        tdkTestObj.setResultStatus("SUCCESS");
							print "Failed to create recording with negative recordID";
	                    	else:
        	                	print "Failed to retrieve acknowledgement from recorder";
                	                tdkTestObj.setResultStatus("FAILURE");
	        	else:
        	           tdkTestObj.setResultStatus("FAILURE");
                	   print "updateSchedule message post failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Requested url not formed, Please check precondition";
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");

	#unloading Recorder module
	obj.unloadModule("Recorder");
