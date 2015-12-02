'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_FutureP4Rec_OnDiskFull_Check_AfterFreeingSpace_119</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that additional segment is created for new future P4 recording after manually deleting old P4 recording before scheduled end time</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_FutureP4Rec_OnDiskFull_Check_AfterFreeingSpace_119');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Pre-req: hdd should be full with P4 recodings. There should be at least one P4 recording of 1 min duration

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
	       sleep(300);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        #Get the list of recordings
        jsonMsg = "{\"getRecordings\":{}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        if 'getRecordings' in serverResponse:
                print "getRecordings message post success"
                print "Waiting to get recording list"
                sleep(60)
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                print "Retrieve Status Details: %s"%recResponse;
                status = recorderlib.getStatusMessage(recResponse)
                print "get reclist status: ",status
                if ("NOSTATUS" != status):
                        #Find one recording of duration 1 min (max 2 min)
                        recordings = recorderlib.getRecordings(recResponse)
                        recIdExist = "0"
                        for i in range(0, len(recordings)):
                                if ( (recordings[i]['expectedDuration'] >= 60000) and (recordings[i]['expectedDuration'] <= 120000) and (recordings[i]['size'] > 0)):
                                        recIdExist = str(recordings[i]['recordingId'])
                                        break

                        if "0" != recIdExist:
                                print "Found recording to be deleted: ",recIdExist
                                #Execute updateSchedule for scheduling new recording

                                response = recorderlib.callServerHandler('clearStatus',ip);

                                requestID = str(randint(10, 500));
                                recordingID = str(randint(10000, 500000));
                                duration = "60000";
                                startTime = "60000";
                                ocapId = tdkTestObj.getStreamDetails('02').getOCAPID()
                                now = "curTime"

                                #Frame json message
                                jsonMsgNew = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";
                                serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNew,ip);
                                if 'updateSchedule' in serverResponse:
                                        print "updateSchedule message post success";
                                        print "Waiting to get acknowledgement from recorder"
                                        sleep(30)
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Retrieve Status Details: %s"%recResponse;
                                        if 'ack' in recResponse:
                                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                print "recording data from response: ",recordingData
                                                status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                error = recorderlib.getValueFromKeyInRecording(recordingData,'error')

                                                if ( ("SPACE_FULL" == error) and ("FAILED" == status.upper()) ):
                                                        print "DiskFull!! Delete an existing P4 recording"
                                                        response = recorderlib.callServerHandler('clearStatus',ip);
                                                        #Frame json message for update recording
                                                        jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"dvrProtocolVersion\":\"7\",\"recordings\":[{\"recordingId\":\""+recIdExist+"\",\"deletePriority\":\"P0\"}]}}";

                                                        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);
                                                        print "Server response for updateRecordings: ",actResponse;
                                                        if 'updateRecordings' in actResponse:
                                                                print "updateRecordings message post success";
                                                                print "Waiting to get acknowledgement"
                                                                sleep(30);
                                                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                                print "Retrieve Status Details: %s"%actResponse
                                                                if 'ack' in actResponse:
                                                                        print "Successfully retrieved acknowledgement from recorder";
                                                                        print "Get recording list to check deleted recording status"
                                                                        response = recorderlib.callServerHandler('clearStatus',ip);
                                                                        jsonMsg = "{\"getRecordings\":{}}";
                                                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
                                                                        print "Server response for getRecordings: ",serverResponse;

                                                                        if 'getRecordings' in serverResponse:
                                                                               print "getRecordings message post success";
                                                                               #wait to get list
                                                                               sleep(100)
                                                                               recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                                               print "Retrieve Status Details: ",recResponse
                                                                               status = recorderlib.getStatusMessage(recResponse)
                                                                               if ("NOSTATUS" == status):
                                                                                        print "Timeout!Failed to get recording list. Exiting...";
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                               else:
                                                                                        recordingData = recorderlib.getRecordingFromRecId(recResponse,recIdExist)
                                                                                        print recordingData
                                                                                        if 'NOTFOUND' == recordingData:
                                                                                                print "Successfully deleted existing recording";
                                                                                                response = recorderlib.callServerHandler('clearStatus',ip);
                                                                                                print "create new recording again after deleting old rec"
                                                                                                recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNew,ip);
                                                                                                print "Waiting to get acknowledgement from recorder"
                                                                                                sleep(60)
                                                                                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                                                                print "Retrieve Status Details: %s"%recResponse;
                                                                                                recData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                                                                print "recording data from response: ",recData
                                                                                                error = recorderlib.getValueFromKeyInRecording(recData,'error')
                                                                                                if "SPACE_FULL" == error:
                                                                                                        print "Failed to create new rec after deleting old rec"
                                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                                else:
                                                                                                        print "Successfully created new rec after deleting old rec"
                                                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                                        else:
                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                                print "Failed to delete existing recording";
                                                                        else:
                                                                                print "getRecordings message post failed"
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                else:
                                                                        print "Failed to get acknowledgement from recorder"
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        else:
                                                                print "updateRecordings message post failed"
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                        print "Disk not full yet. Pre-req not met. Exiting!"
                                                        tdkTestObj.setResultStatus("FAILURE");
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Failed to retrieve acknowledgement from recorder"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print "updateSchedule message post failed"
                        else:
                                print "No recording found with duration between 1min-2min to delete"
                                tdkTestObj.setResultStatus("FAILURE");

                else:
                        print "Timeout!Failed to get recording list. Exiting...";
                        tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "getRecordings message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
