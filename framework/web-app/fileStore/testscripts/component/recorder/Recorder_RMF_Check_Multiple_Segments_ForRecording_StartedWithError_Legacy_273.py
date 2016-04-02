'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Check_Multiple_Segments_ForRecording_StartedWithError_Legacy_273</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_273 - Test for segmented recordings by rebooting the box when a recording is in StartedWithError</synopsis>
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
  <script_tags />
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_Multiple_Segments_ForRecording_StartedWithError_Legacy_273');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus ;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for 5min for the recoder to be up"
	       sleep(300);

        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
      	actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

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
        duration = "1200000";
        startTime = "120000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse; 
        
        if expResponse in actResponse:
            tdkTestObj.setResultStatus("SUCCESS");
            print "updateSchedule message post success";
            #Check for acknowledgement from recorder
            tdkTestObj.executeTestCase(expectedResult);
            print "Looping till acknowledgement is received"
            loop = 0;
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
            while (('ack' not in actResponse) and (loop < 5)):
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                sleep(10);
                loop = loop+1;
            print "Retrieve Status Details: ",actResponse;

            if 'acknowledgement' not in actResponse:
                tdkTestObj.setResultStatus("FAILURE");
                print "Received Empty/Error status";
            elif 'acknowledgement' in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Successfully retrieved acknowledgement from recorder";
                sleep(60)
                # Reboot the STB before starting the recording
                print "Rebooting the STB to get the recording list from full sync"
                recObj.initiateReboot();
                print "Sleeping to wait for the recoder to be up"
                sleep(300);
                print "Wait for the recording to complete partially"
                sleep(300);
                print "Sending getRecordings to get the recording list"
                recorderlib.callServerHandler('clearStatus',ip)
                recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                print "Wait for 1 min to get response from recorder"
                sleep(60)
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                print "Recording data after 1st reboot", recordingData
                if 'NOTFOUND' not in recordingData:
                    statusKey = 'status'
                    statusValue = recorderlib.getValueFromKeyInRecording(recordingData,statusKey)
                    print "Successfully retrieved the recording list from recorder";
                    tdkTestObj.setResultStatus("SUCCESS");
                    if "STARTEDINCOMPLETE" in statusValue.upper():
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Recording with status STARTEDINCOMPLETE";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Recording status STARTEDINCOMPLETE not set successfully";
                else:
                     tdkTestObj.setResultStatus("FAILURE");
                     print "Failed to retrieve the recording list from recorder";

                # Reboot the STB to get the recording as multiple segements
                print "Rebooting the STB to get the recording list from full sync"
                recObj.initiateReboot();
                print "Sleeping to wait for the recoder to be up"
                sleep(300);
                print "Wait for the recording to complete"
                #sleep(300);

                tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                tdkTestObj.executeTestCase(expectedResult);
                print "Sending getRecordings to get the recording list"
                recorderlib.callServerHandler('clearStatus',ip)
                recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
                print "Wait for 1 min to get response from recorder"
                sleep(60)
                actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                print "Recording List: %s" %actResponse;
                recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);            
                print recordingData
                if 'NOTFOUND' not in recordingData:
                    print "Successfully retrieved the recording list from recorder";
                    statusKey = 'status'
                    statusValue = recorderlib.getValueFromKeyInRecording(recordingData,statusKey)
                    durationList = recorderlib.getValueFromKeyInRecording(recordingData,'duration')
                    print "Durations in recording data " , durationList
                    tdkTestObj.setResultStatus("SUCCESS");
                    if "INCOMPLETE" in statusValue.upper():
                        if ((len(durationList) == 2)):
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Recording contains two segments after power interruption"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Recording not segmented after power interruption"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Recording not completed successfully";
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
