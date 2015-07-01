'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>12</version>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_Neg_02');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        obj.initiateReboot();
	print "Sleeping to wait for the recoder to be up"
	sleep(300);

        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        negate = "-"
        rec_id = random.randrange(10**9, 10**255)
        recording_id = negate + str(rec_id);
        duration = "180000";
        start_time = "0";
        requestID = str(randint(10,500));
	genIdInput = requestID;
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
########################## SINCE THERE WAS SOME ISSUE IN USING THE STUBS URL, USING THE HARD CODED VALUE #################################
     	        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"schedule\":[{\"recordingId\":\""+recording_id+"\",\"locator\":[\"ocap://0x125d\"],\"epoch\":curTime,\"start\":0,\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recording_id+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
                print "RequestURL  is : %s" %RequestURL;
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        print "Requested recording url is formed";
                        #status_expected = "acknowledgement";
                        status_expected = "updateSchedule";
                        #status_actual =tdkTestObj.initiateRecorderApp(RequestURL);
        		expectedResult="SUCCESS";
			tdkTestObj.executeTestCase(expectedResult);
			sleep(5);
			status_actual = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        print "Status string is: %s"%status_actual;
                        if status_expected in status_actual:
                                tdkTestObj.setResultStatus("SUCCESS");
                		print "updateSchedule message post success";
                		tdkTestObj.executeTestCase(expectedResult);
				print "Waiting to get acknowledgment status"
				sleep(10);
				retry=0
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		                while ((('[]' in actResponse) or ('ack' not in actResponse)) and ('ERROR' not in actResponse) and (retry < 15)):
					sleep(10);
					actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
					retry += 1
					print "Retrieve Status Details:\n %s \n"%actResponse;
		                if (('[]' in actResponse) or ('ERROR' in actResponse)):
	        		        tdkTestObj.setResultStatus("FAILURE");
		        	        print "Received Empty/Error status";
		                elif 'acknowledgement' in actResponse:
                			tdkTestObj.setResultStatus("SUCCESS");
		                    	print "Successfully retrieved acknowledgement from recorder";
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
        	                                print "As expected failed to schedule a Recording with negative recordID";
                	            	else:
                        	        	tdkTestObj.setResultStatus("FAILURE");
                                	        #Getting the mplayer log file from DUT
	                                        logpath=tdkTestObj.getLogPath();
        	                                print "Log path : %s" %logpath;
                	                        tdkTestObj.transferLogs(logpath,"false");
                        	                print "Failed to search the pattern in the logfile";
	                    	else:
        	                	print "Failed to schedule a Recording";
                	                tdkTestObj.setResultStatus("FAILURE");
	        	else:
        	           tdkTestObj.setResultStatus("FAILURE");
                	   print "updateSchedule message post failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Requested url not formed, Please check precondition";
                #unloading Recorder module
                obj.unloadModule("Recorder");
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");
else:
        print "Failed to load Recorder module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
