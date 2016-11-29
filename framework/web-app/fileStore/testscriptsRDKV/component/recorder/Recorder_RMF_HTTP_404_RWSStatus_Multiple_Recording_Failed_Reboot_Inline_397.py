##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>Recorder_RMF_HTTP_404_RWSStatus_Multiple_Recording_Failed_Reboot_Inline_397</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Checking whether the Multiple Failed recording details are getting synced with RWS after reboot  or not when the server is up after reconnecting</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recorder_DVR_Protocol_397</test_case_id>
    <test_objective>After reboot check whether the Multiple Failed recording details using inline are getting synced with RWS  or not when the server is up after reconnecting</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. TM loads RecorderAgent via the test agent.
2. Configure RWS status servers with error 404
3. Schedule two 1 min inline recording with an invalid ocap id
4.Wait for 30 seconds for connection retry requests to happen and reboot the box.
5. Clear the RWS status server error 404
6.Check whether Recorder has send the FAILED status for both recordings after reconnecting to RWS Status Server
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Recording details should be available as expected</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_HTTP_404_RWSStatus_Multiple_Recording_Failed_Reboot_Inline_397</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_HTTP_404_RWSStatus_Multiple_Recording_Failed_Reboot_Inline_397');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

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
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
       
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSStatus',ip,'404');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSSecureStatus',ip,'404');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSStatus',ip);

        if "true" in actResponse:
            #Execute updateSchedule
            requestID1 = str(randint(10, 500));
            recordingID1 = str(randint(10000, 500000));
            duration = "60000";
            startTime = "0";
            ocapId = "0xbad1"
            now = "curTime"

            #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID1+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID1+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID1+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

            expResponse = "updateSchedule";
            tdkTestObj.executeTestCase(expectedResult);
            actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
            print "Update Schedule Details: %s"%actResponse;

            sleep(5);
         
            #Execute updateSchedule
            requestID2 = str(randint(10, 500));
            recordingID2 = str(randint(10000, 500000));
            ocapId = "0x@@@1"

            #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID2+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

            expResponse = "updateSchedule";
            tdkTestObj.executeTestCase(expectedResult);
            actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
            print "Update Schedule Details: %s"%actResponse;
          
            print "Waiting for connection retry to happen"
            sleep(30);
 
            #Reboot the box
            recObj.initiateReboot();
            print "Waiting for 5 min for recoder to be up" 
            
            print "Clearing the RWS Status server errors"
            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSStatus',ip);
            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSSecureStatus',ip);
            actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSStatus',ip);

            sleep(300);
            #Waiting for connection reset
            if "false" in actResponse:
               print "Waiting for RWS Status server connection re-establishment"
               sleep(60)
            
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
            print "RESPONSE" , actResponse
            recordingData1 = recorderlib.getRecordingFromRecId(actResponse,recordingID1);
            recordingData2 = recorderlib.getRecordingFromRecId(actResponse,recordingID2);
            print recordingData1
            print recordingData2
            
            if 'NOTFOUND' not in (recordingData1 and recordingData2):
                print "Successfully retrieved the recording details from recorder";
                statusKey = 'status'
                statusValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,statusKey)
                statusValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,statusKey)

                if "FAILED" in (statusValue1.upper() and statusValue2.upper()):
                    print "Recorder has send the FAILED status for both recordings after reconnecting to RWS Status Server"
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Recorder NOT send the FAILED status for both recordings after reconnecting to RWS Status Server"
            else:
                print "NOT retrieved the recording list from recorder";
                tdkTestObj.setResultStatus("FAILURE"); 

        else:
           print "Unable to set server error HTTP 404"
           tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
