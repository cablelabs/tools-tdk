#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_PurgeNonP4_OnDiskFull_SchedFutureP4Rec_126</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that recorder deletes non-P4 recordings before disk is completely full to allow new scheduled future P4 recording</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_PurgeNonP4_OnDiskFull_SchedFutureP4Rec_126');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

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
        print "Server response for getRecordings: ",serverResponse;
        if 'getRecordings' in serverResponse:
                print "getRecordings message post success"
                print "Wait 60 seconds to get response from recorder"
                sleep(60)
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                status = recorderlib.getStatusMessage(recResponse)
                print "status message containing recording list: ",status
                if ("NOSTATUS" != status):
                        #From the list get all P3 recordings Ids
                        recordings = recorderlib.getRecordings(recResponse)
                        recP3List = []
                        for i in range(0, len(recordings)):
                                if ( (recordings[i]['deletePriority'] == "P3") and (recordings[i]['size'] > 0) ):
                                        recP3List.append(recordings[i]['recordingId'])

                        if ( [] != recP3List ):
                                print "Found P3 recordings: ",recP3List
                                response = recorderlib.callServerHandler('clearStatus',ip);

                                #Execute updateSchedule for scheduling new recording
                                requestID = str(randint(10, 500));
                                recordingID = str(randint(10000, 500000));
                                duration = "60000";
                                startTime = "60000";
                                ocapId = tdkTestObj.getStreamDetails('02').getOCAPID()
                                now = "curTime"

                                #Frame json message
                                jsonMsgNew = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"0\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";
                                serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNew,ip);
                                print "Server response for updateSchedule: ",serverResponse;

                                if 'updateSchedule' in serverResponse:
                                        print "updateSchedule message post success";
                                        print "Waiting to get acknowledgement from recorder"
                                        sleep(30)
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Retrieve Status Details: %s"%recResponse;
                                        if 'ack' in recResponse:
                                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                print "recording data from response: ",recordingData
                                                if "NOTFOUND" != recordingData:
                                                    status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                    error = recorderlib.getValueFromKeyInRecording(recordingData,'error')
                                                    if ( ("SPACE_FULL" == error) and ("FAILED" == status.upper()) ):
                                                        print "Space Full!! Check if old P3 recording is purged by recorder"
                                                        response = recorderlib.callServerHandler('clearStatus',ip);
                                                        jsonMsg = "{\"getRecordings\":{}}";
                                                        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
                                                        print "Server response for getRecordings: ",serverResponse;

							#Wait for recording to be complete
							print "wait 60 seconds to get response from recorder"
							sleep(60)
                                                        if 'getRecordings' in serverResponse:
                                                                print "getRecordings message post success";
                                                                #wait to get list
                                                                sleep(100)
                                                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                                                print "Retrieve Status Details: ",recResponse
                                                                status = recorderlib.getStatusMessage(recResponse)
                                                                if ("NOSTATUS" != status):
                                                                        #Check if any old P3 recording is missing
                                                                        deleteFlag = 0
                                                                        for i in range(0, len(recP3List)):
                                                                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recP3List[i])
                                                                                if 'NOTFOUND' == recordingData:
                                                                                        print "Successfully deleted existing recording ",recP3List[i];
                                                                                        deleteFlag = 1

                                                                        if 1 == deleteFlag:
                                                                                print "Recorder purged old P3 recording"
                                                                                print "Check status of new recording"
                                                                                recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID)
                                                                                print "recording data from response: ",recordingData
                                                                                status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
                                                                                if "COMPLETED" == status.upper():
                                                                                        print "New recording completed after purging old recording"
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                else:
                                                                                        print "New recording not completed even after purging old recording"
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        else:
                                                                                print "None of P3 recordings deleted to free up space"
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                else:
                                                                        print "Timeout!Failed to get recording list. Exiting...";
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print "getRecordings message post failed";
                                                    else:
                                                        print "Disk not full yet. Pre-req not met. Exiting!"
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                else:
                                                    print "New recording allowed. Disk not full yet. Pre-req not met. Exiting!"
                                                    tdkTestObj.setResultStatus("FAILURE");
                                        else:
                                               print "Failed to get acknowledgement from recorder"
                                               tdkTestObj.setResultStatus("FAILURE");
                                else:
                                        print "updateRecordings message post failed"
                                        tdkTestObj.setResultStatus("FAILURE")
                        else:
                                print "Did not find P3 recordings.Pre-req not met. Exiting!"
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        print "Timeout!Failed to get recording list. Exiting...";
                        tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "getRecordings message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
