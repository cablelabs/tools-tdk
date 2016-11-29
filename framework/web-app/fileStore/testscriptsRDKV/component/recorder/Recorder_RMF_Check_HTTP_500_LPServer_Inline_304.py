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
  <version>3</version>
  <name>Recorder_RMF_Check_HTTP_500_LPServer_Inline_304</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Long poll server should send HTTP 500 when server is enabled with HTTP 500 error and after clearing the error legacy recording should get complete</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_304</test_case_id>
    <test_objective>Long poll server should send HTTP 500 when server is enabled with HTTP 500 error and after clearing the error inline recording should get complete</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. TM loads RecorderAgent via the test agent.
2. Configure long poll server with error 500  and reboot the box
3. Schedule a 1 min inline recording
4.Check ocapri log for error code 500 and connection retry requests
5. Clear the lp server error and wait for the re-connection and also for the recording to get completed
6.Check the status of recording , it should be complete
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Check whether the error codes are available in ocapri log and also check the recording status.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_clearOcapri_log
3.TestMgr_Recorder_checkOcapri_log
4.TestMgr_Recorder_ExecuteCmd</test_stub_interface>
    <test_script>Recorder_RMF_Check_HTTP_500_LPServer_Inline_304</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_500_LPServer_Inline_304');
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
        tdkTestObj.executeTestCase(expectedResult);
 
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','LPServer',ip,'500');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','LPServer',ip);
        if "true" in actResponse:
            #To clear the ocapri log
            tdkTestObj1 = recObj.createTestStep('Recorder_clearOcapri_log');
            tdkTestObj1.executeTestCase(expectedResult);
            result = tdkTestObj1.getResult();
            if "SUCCESS" in result:
                tdkTestObj1.setResultStatus("SUCCESS");
                print "Cleared the ocapri log ";
            else:
                tdkTestObj1.setResultStatus("FAILURE");
                print "Ocapri log is not cleared ";
        
            # Reboot the STB
            print "Rebooting the STB"
            recObj.initiateReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);
      
            requestID = str(randint(10, 500));
            recordingID = str(randint(10000, 500000));
            duration = "60000";
            startTime = "0";
            ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
            now = "curTime"

            #Frame json message to schedule a recording
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

            actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

            print "Checking ocapri_log"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "Received HTTP response code: 500"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "HTTP 500 error received ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "HTTP 500 error NOT received "; 

            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "NULL data from long poll.  Restarting request after"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Longpoll server connection retry is happening";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Longpoll server connection retry is NOT happening";
             
            print "Clear the Longpoll server error" 
            actResponse = recorderlib.callServerHandlerWithType('clearError','LPServer',ip);
            print "Waiting for the connection re-establishment and recording to get completed"
            sleep(180);

            tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
            tdkTestObj.executeTestCase(expectedResult);
            print "Sending getRecordings to get the recording list"
            recorderlib.callServerHandler('clearStatus',ip)
            recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
            print "Wait for 1 min to get response from recorder"
            sleep(60)
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
            print "Recording List: %s" %actResponse;
            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
            print recordingData
            if 'NOTFOUND' not in recordingData:
                key = 'status'
                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                print "key: ",key," value: ",value
                print "Successfully retrieved the recording list from recorder";
                if "COMPLETE" in value.upper():
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Recording completed successfully";
                elif "STARTED" in value.upper():
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Recording started successfully";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Recording NOT completed successfully";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve the recording list from recorder";

            actResponse = recorderlib.callServerHandlerWithType('isEnabledError','LPServer',ip);
            if "false" in actResponse: 
                recObj.initiateReboot();
                print "Sleeping to wait for the recoder to be up"
                sleep(300);

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Error NOT enabled for Long poll server";
        
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");

