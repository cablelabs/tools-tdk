'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_LegacyInline_Full_Schedule_True_27</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_27 - Recorder-To replace all current and future schedules when updateSchedule is received with fullSchedule=true. Perform first updateSchedule as legacy and second as inline</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_LegacyInline_Full_Schedule_True_27');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper())

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

        #Giving no update here to get the recording list in case the previous generation id is set to zero before reboot
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite to clear any recording status
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "120000";
        startTime = "0";
        futureStartTime = "120000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        futureOcapId= tdkTestObj.getStreamDetails('02').getOCAPID()
	fullScheduleOcapId= tdkTestObj.getStreamDetails('03').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"},{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+futureOcapId+"\"],\"epoch\":"+now+",\"start\":"+futureStartTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
		loop = 0;
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		while ( ('acknowledgement' not in actResponse) and (loop < 5)):
	                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			sleep(10);
			loop = loop+1;
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Successfully retrieved acknowledgement from recorder";
                    sleep(60);
		    response = recorderlib.callServerHandler('clearStatus',ip);

                    #Frame json message for update recording
                    jsonMsgFullSchedule = "{\"updateSchedule\":{\"requestId\":\""+str(int(requestID)+1)+"\",\"generationId\":\"0\",\"fullSchedule\":true,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+2)+"\",\"locator\":[\"ocap://"+fullScheduleOcapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+2)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                    expResponse = "updateSchedule";
                    tdkTestObj.executeTestCase(expectedResult);
                    actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgFullSchedule,ip);
                    if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateSchedule message with fullSchedule true post success";
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        while ( ('acknowledgement' not in actResponse) and (loop < 5)):
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10);
                                loop = loop+1;
			print "Retrieve Status Details: %s"%actResponse;
                        if 'acknowledgement' in actResponse:
                        	print "Successfully retrieved acknowledgement from recorder";
			   	tdkTestObj.setResultStatus("SUCCESS");
                                sleep(30)
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                           	tdkTestObj.executeTestCase(expectedResult);
                            	recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                            	print recordingData
                            	if 'NOTFOUND' not in recordingData:
                            		key = 'error'
                                	value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                	print "recordingId: ",recordingID," key: ",key," value: ",value
                                	if "USER_STOP" in value.upper():
                                        	print "Recording in progress cancelled successfully";
                                        	futurerecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1))
                                        	print futurerecordingData
                                                if 'NOTFOUND' not in futurerecordingData:
                                                        key = 'error'
                                                        value = recorderlib.getValueFromKeyInRecording(futurerecordingData,key)
                                                        print "recordingId: ",str(int(recordingID)+1), " key: ",key," value: ",value
                                                        if "USER_STOP" in value.upper():
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print "Future recording cancelled successfully";
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "Failed to cancel the recording the future recording";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Failed to retrieve the status of canceled future recording";
                                	else:
                                		tdkTestObj.setResultStatus("FAILURE");
                                        	print "Failed to cancel the recording in progress";
                              	else:
                              		tdkTestObj.setResultStatus("FAILURE");
                                	print "Failed to retrieve the status of canceled in progress recording";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
		    else:
			tdkTestObj.setResultStatus("FAILURE");
			print "updateSchedule message with fullSchedule true post failed";
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
