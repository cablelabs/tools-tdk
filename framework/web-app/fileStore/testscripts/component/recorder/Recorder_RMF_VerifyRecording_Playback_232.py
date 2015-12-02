'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_VerifyRecording_Playback_232</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify successful playback of recorded content</synopsis>
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
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import recorderlib
from random import randint
from time import sleep
from tdkintegration import dvr_playback;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_VerifyRecording_Playback_232');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus ;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

recordingSuccess = 'FALSE'
recordingID = str(randint(10000, 500000))

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
               sleep(300);

        #Primitive test case which associated to this Script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult = "SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        #2mins duration
        duration = "120000"
        startTime = "0"
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',RequestURL,ip);

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                sleep(15);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                retry = 0;
                while ( ('acknow' not in recResponse) and (retry < 10 ) ):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: ",recResponse;
                if "acknow" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        response = recorderlib.callServerHandler('clearStatus',ip)
                        print "Wait for 2 min for recording to complete"
                        sleep(120)
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        print "Wait for 3 min to get response from recorder"
                        sleep(180)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse;
                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                        print recordingData
                        if ('NOTFOUND' in recordingData):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get recording info"
                        else:
                                reqRecording = {"recordingId":recordingID,"duration":120000,"deletePriority":"P3"}
                                ret = recorderlib.verifyCompletedRecording(recordingData,reqRecording)
                                if "FALSE" in ret:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording failed verification"
                                else:
                                        recordingSuccess = 'TRUE'
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Recording passed verification"
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");

if 'TRUE' == recordingSuccess:
        # Playback the recorded content
        tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
        tdkIntObj.configureTestCase(ip,port,'Recorder_RMF_VerifyRecording_Playback_232');
        tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
        print "TDKINTEGRATION module loading status : %s" %tdkIntLoadStatus;
        #Set the module loading status
        tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

        #Check for SUCCESS/FAILURE of tdkintegration module
        if "SUCCESS" in tdkIntLoadStatus.upper():

                #Primitive test case which associated to this script
                tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
                result = dvr_playback(tdkTestObj,recordingID);

                if "SUCCESS" in result.upper():
                        print "Recording playback Success"
                else:
                        print "Recording playback Failed"

                #unloading tdkintegration module
                tdkIntObj.unloadModule("tdkintegration");
else:
        print "Skipping playback for failed recording"
