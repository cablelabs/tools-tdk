'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_UpdateRecording_WithNoRecordingProperties_233</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify state of recording after updating with no recording properties</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>45</execution_time>
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
from time import sleep, time

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_UpdateRecording_WithNoRecordingProperties_233');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
               sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Execute updateSchedule
        requestID = str(randint(10, 500))
        recordingID = 'A'+str(randint(100000000, 500000000))+str(randint(10000000, 50000000))
        duration = "300000"
        epochTime = int(time()) * 1000
        epochTime += 30000
        startTime = str(epochTime)
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":true,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"start\":"+startTime+",\"duration\":"+duration+",\"ppv\":false,\"entitlementId\":0,\"properties\":{\"title\":\"Recording_"+recordingID+"\",\"requestedStart\":"+startTime+"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

        if "updateSchedule" in actResponse:
                print "Inline updateSchedule message post success";
                print "Waiting to get acknowledgement for updateSchedule"
                sleep(20);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while ( ('acknowledgement' not in recResponse) and (retry < 10) ):
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        sleep(10);
                        retry += 1
                print "Retrieve Status Details: ",recResponse

                if 'acknowledgement' in recResponse:

                    print "Successfully retrieved acknowledgement from recorder for updateSchedule";
                    response = recorderlib.callServerHandler('clearStatus',ip);
                    tdkTestObj.executeTestCase(expectedResult);
                    #Frame json message for update recording
                    requestID = str(randint(10, 500))
                    jsonMsgUpdateRecording = "{\"updateRecordings\":{\"requestId\":\""+requestID+"\",\"recordings\":[{\"recordingId\":\""+recordingID+"\"}]}}"
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgUpdateRecording,ip);

                    if "updateRecordings" in actResponse:
                        print "updateRecordings message post success";
                        print "Waiting to get acknowledgement for updateRecordings"
                        sleep(20);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry = 0;
                        while ( ('acknowledgement' not in recResponse) and (retry < 10) ):
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10)
                                retry += 1
                        print "Retrieve Status Details: ",recResponse

                        if 'acknowledgement' in recResponse:
                            print "Successfully retrieved acknowledgement from recorder for updateRecordings";
                            print "Waiting for 5 mins for recording to be completed"
                            sleep(300)
                            print "Sending getRecordings request to get the recording list"
                            response = recorderlib.callServerHandler('clearStatus',ip)

                            jsonMsg = "{\"getRecordings\":{}}"
                            serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip)
                            print "Waiting for 3 mins to get recording list"
                            sleep(180)
                            recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                            print "Recording List: %s" %recResponse;
                            recordingData = recorderlib.getRecordingFromRecId(recResponse,recordingID);
                            print recordingData
                            if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get recording info using getRecordings"
                            else:
                                reqRecording = {"recordingId":recordingID,"duration":120000,"deletePriority":"P3"}
                                ret = recorderlib.verifyCompletedRecording(recordingData,reqRecording)
                                if "FALSE" in ret:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Recording failed verification"
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Recording passed verification"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder for updateRecordings";
                    else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "updateRecordings message post failed";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder for updateSchedule";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Inline updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
