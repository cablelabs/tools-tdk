'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_PowerInterrupt_Notification_53</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_53 - Recoder to send power interruption error notification for multiple scheduling at different timestamp</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_PowerInterrupt_Notification_53');
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

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "300000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        ocapId2 = tdkTestObj.getStreamDetails('02').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        SchedulejsonMsg = "{\"updateSchedule\":{\"requestId\":\""+str(int(requestID)+1)+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId2+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
	ScheduleResponse = recorderlib.callServerHandlerWithMsg('updateMessage',SchedulejsonMsg,ip);
        if expResponse in actResponse and expResponse in ScheduleResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
		loop = 0;
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
                        # Reboot the STB
                        print "Rebooting the STB to get the recording list from full sync"
                        recObj.initiateReboot();
                        print "Sleeping to wait for the recoder to be up"
                        sleep(300);
			actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                        tdkTestObj1.executeTestCase(expectedResult);
                        sleep(60);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print actResponse;
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
			print "Recording 1 data : " , recordingData
                        SecondrecordingData = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1))
                        print "Recording 2 data : ", SecondrecordingData
			
                        if 'NOTFOUND' not in recordingData and 'NOTFOUND' not in SecondrecordingData:
                            key = 'status'
                            errorKey = 'error'
                           
			    print "Get status and error field from Recording 1" 
                            statusValue = recorderlib.getValueFromKeyInRecording(recordingData,key)
                            errorValue = recorderlib.getValueFromKeyInRecording(recordingData,errorKey)
			    print "Recording 1 status : ", statusValue," error: ",errorValue
			    print "Get status and error field from Recording 2"
                            secondStatusValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,key)
                            secondErrorValue = recorderlib.getValueFromKeyInRecording(SecondrecordingData,errorKey)
                            print "Recording 2 status : ", secondStatusValue," error: ",secondErrorValue
                            if "INCOMPLETE" in statusValue.upper() and "POWER_INTERRUPTION" in errorValue.upper() and "INCOMPLETE" in secondStatusValue.upper() and "POWER_INTERRUPTION" in secondErrorValue.upper():
                                print "Power interruption happened successfully";
				timestampList = recorderlib.getTimeStampListFromStatus(actResponse)
                                print "Timestamp list in recording status: ",timestampList
                                if timestampList != []:
                                	if ( (len(timestampList) > 1) and (timestampList[0] != timestampList[1])):
                                        	print "Recorder has send the recording status notification at different timestamp"
                                                tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                                print "Recorder has not send the recording status notification at different timestamp"
                                                tdkTestObj.setResultStatus("FAILURE");
                            	else:
                                	print "Recorder has not send the timestamp in  recording status"
                                	tdkTestObj.setResultStatus("FAILURE");
                            elif "BADVALUE" in statusValue.upper() or "BADVALUE" in errorValue.upper() or "BADVALUE" in secondStatusValue.upper() or "BADVALUE" in secondErrorValue.upper():
			    	tdkTestObj.setResultStatus("FAILURE");
                                print "Recording did not have error/status field";
                            else:
                                print "Recorder has not send recording status"
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj1.setResultStatus("FAILURE");
                            print "Failed to retrieve the recording list from recorder";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
