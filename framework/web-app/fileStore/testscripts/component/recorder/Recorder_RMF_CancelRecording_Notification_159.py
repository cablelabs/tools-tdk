'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_CancelRecording_Notification_159</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_159 - Recoder to send USER_STOP error notification at different timestamp when multiple recording in progress are cancelled</synopsis>
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
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
from time import sleep


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_CancelRecording_Notification_159');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);
	print "Sleeping to wait for the recoder to be up"

        
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(60);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "120000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        SchedulejsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;
	ScheduleResponse = recorderlib.callServerHandlerWithMsg('updateMessage',SchedulejsonMsg,ip);
        print "Update Schedule Details: %s"%ScheduleResponse;

        if expResponse in actResponse and expResponse in ScheduleResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                print "Wait for 60s to get acknowledgement"
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
		loop = 0;
		while loop < 5:
	                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
	                print "Retrieve Status Details: %s"%actResponse;
			sleep(10);
			loop = loop+1;
		if 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received Empty/Error status";
                elif 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    response = recorderlib.callServerHandler('clearStatus',ip);
                    print "Clear Status Details: %s"%response;

                    #Frame json message for update recording
                    jsonMsgUpdateRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"cancelRecordings\":[\""+recordingID+"\",\""+str(int(recordingID)+1)+"\"]}}";

                    expResponse = "updateSchedule";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
                    print "updateSchedule Details: %s"%actResponse;
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateSchedule message post success";
                        print "Wait for 60s to get acknowledgement"
                        sleep(60);
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        while loop < 5:
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                #print "Retrieve Status Details: %s"%actResponse;
                                sleep(10);
                                loop = loop+1;
			if 'acknowledgement' not in actResponse:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Received Empty/Error status";
                        elif 'acknowledgement' in actResponse:
                            print "Successfully retrieved acknowledgement from recorder";
	                    #Check for acknowledgement from recorder
                            tdkTestObj.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			    recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
			    SecondrecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1))
	                    print recordingData,SecondrecordingData
                            if 'NOTFOUND' not in recordingData or 'NOTFOUND' not in SecondrecordingData:
            	            	key = 'status'
                                errorKey = 'error'
				
                	        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                errorValue = recorderlib.getValueFromKeyInRecording(recordingData,errorKey)
                                    
                                secondValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,key)
                                secondErrorValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,errorKey)

                        	print "key: ",key," value: ",value
                                print "Successfully retrieved the recording list from recorder";
				if "INCOMPLETE" in value.upper() and "USER_STOP" in errorValue.upper() and "INCOMPLETE" in secondValue.upper() and "USER_STOP" in secondErrorValue.upper():
                                	print "Scheduled recording error recieved successfully";
                                	timestampValue = recorderlib.getTimeStampListFromStatus(actResponse)
                                        print "Timestamp in recording status: ",timestampValue
                                        if timestampValue != []:
                                                if timestampValue[0] != timestampValue[1]:
                                                        print "Recorder has send the recording status notification at different timestamp"
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                else:
                                                        print "Recorder has not send the recording status notification at different timestamp"
                                                        tdkTestObj.setResultStatus("FAILURE");
                                        else:
                                                print "Recorder has not send recording status"
                                                tdkTestObj.setResultStatus("FAILURE");
                                elif "BADVALUE" in value.upper() and "BADVALUE" in errorValue.upper() and "BADVALUE" in secondValue.upper() and "BADVALUE" in secondErrorValue.upper():
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Recording did not have error/status field";
                            	else:
                                	tdkTestObj.setResultStatus("FAILURE");
                                	print "Scheduled recording error not received";
			    else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Failed to retrieve the recording list from recorder";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
