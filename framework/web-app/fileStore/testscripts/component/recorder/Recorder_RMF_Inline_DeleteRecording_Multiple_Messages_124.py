'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Inline_DeleteRecording_Multiple_Messages_124</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_124 -  Recorder to delete multiple recordings via inline longpoll</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Inline_DeleteRecording_Multiple_Messages_124');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

        recObj.initiateReboot();
	print "Sleeping to wait for the recoder to be up"
        sleep(300);
        
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
        duration = "240000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        ocapId3 = tdkTestObj.getStreamDetails('03').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P2\"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P2\"},{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"locator\":[\"ocap://"+ocapId3+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+str(int(recordingID)+2)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P2\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

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
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    print "Wait for 60s for the recording to be completed"
		    jsonMsgNoUpdate = "{\"updateSchedule\":{\"generationId\":\"0\"}}";
		    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
                    sleep(60);

                    #Frame json message for update recording
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recordingID+"\",\"deletePriority\":\"P0\"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"deletePriority\":\"P0\"},{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"deletePriority\":\"P0\"}]}}";

                    expResponse = "updateRecordings";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgUpdateRecording,ip);
                    print "updateRecordings Details: %s"%actResponse;
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateRecordings message post success";
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
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                            # Reboot the STB
                            print "Rebooting the STB to get the recording list from full sync"
                            recObj.initiateReboot();
                            print "Sleeping to wait for the recoder to be up"
                            sleep(300);
                            response = recorderlib.callServerHandler('clearStatus',ip);
                            print "Clear Status Details: %s"%response;
                            #Frame json message
                            jsonMsgNoUpdate = "{\"noUpdate\":{\"generationId\":\"0\"}}";
                            expResponse = "noUpdate";
                            tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                            tdkTestObj1.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                            print "No Update Schedule Details: %s"%actResponse;
                            if expResponse in actResponse:
                                print "No Update Schedule message post success";
                                print "Wait for 60s to get the recording list"
                                sleep(120);
                                tdkTestObj1.setResultStatus("SUCCESS");
                                #Check for acknowledgement from recorder
                                tdkTestObj1.executeTestCase(expectedResult);
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print actResponse;
                                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                                secondRecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1))
                                thirdRecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+2))
                                print recordingData,secondRecordingData,thirdRecordingData
                                if 'NOTFOUND' not in recordingData or 'NOTFOUND' not in secondRecordingData or 'NOTFOUND' not in thirdRecordingData:
                                        key = 'status'
                                        value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                        secondRecValue = recorderlib.getValueFromKeyInRecording(secondRecordingData,key)
                                        thirdRecValue = recorderlib.getValueFromKeyInRecording(thirdRecordingData,key)
                                        print "key: ",key," value: ",value," secondRecValue: ",secondRecValue," thirdRecValue: ",thirdRecValue
                                        print "Successfully retrieved the recording list from recorder";
                                        if "ERASED" in value.upper() and "ERASED" in secondRecValue.upper() and "ERASED" in thirdRecValue.upper():
                                                tdkTestObj1.setResultStatus("SUCCESS");
                                                print "Delete recording happened properly";
                                        else:
                                                tdkTestObj1.setResultStatus("FAILURE");
                                                print "Delete recording not happened properly";
                                else:
                                        tdkTestObj1.setResultStatus("FAILURE");
                                        print "Failed to retrieve the recording list from recorder";
                            else:
                                    print "No Update Schedule message post failed";
                                    tdkTestObj1.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
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
