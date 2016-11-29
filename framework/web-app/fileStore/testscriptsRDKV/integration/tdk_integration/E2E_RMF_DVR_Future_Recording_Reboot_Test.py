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
  <version>4</version>
  <name>E2E_RMF_DVR_Future_Recording_Reboot_Test</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the schedule a future recording using recorder component and Reboot the STB after schedule initiated and checks the recording initiated or not.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_36</test_case_id>
    <test_objective>Recorder-Schedule a future recording and rebbot the STB and check whether the recording exists</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads Recorder_agent via the test agent.
2.TM gets an source_id of a different channel from the streaming details page of the FW and sends it to Recorder_agent to generate request url.
3.TM pass the parameters like duration and recording_id to Recorder_agent.
4.Recorder_agent will frame the json message to schedule the recording and send to TDK_Recorder_server which is present in TM.
5.Status of the Json response from Mediastreamer to TDK_Recorder_Server getting extracted by TM.
6 Recorder_agent  will do the error checking by verifying ocapri_logs.
7.Reboot the STB
8. Check the status of the Recording after Reboot
9.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.
15.Depends on the result of above step agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapRI_log to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>Recorder_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_Future_Recording_Reboot_Test</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import sched_rec

#Test component to be tested
media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_Future_Recording_Reboot_Test');
media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_Future_Recording_Reboot_Test');

loadmodulestatus = rec_obj.getLoadModuleResult();
loadmodulestatus1 = media_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;

loadmoduledetails = rec_obj.getLoadModuleDetails();
loadmoduledetails1 = media_obj.getLoadModuleDetails();

if "FAILURE" in loadmodulestatus1.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails1:
                print "rmfStreamer is not running. Rebooting STB"
                media_obj.initiateReboot();
                #Reload Test component to be tested
                media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_Future_Recording_Reboot_Test');
                #Get the result of connection with test component and STB
                loadmodulestatus1 = media_obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadmodulestatus1;
                loadmoduledetails1 = media_obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails1;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    media_obj.setLoadModuleStatus("SUCCESS");
    rec_obj.setLoadModuleStatus("SUCCESS");
    
    #result1,recording_id = sched_rec(rec_obj,'01','100',duration = "60000");
    #result2 = deleteRecording(media_obj,'01',recording_id);

    rec_duration = '60000';
    start_time = '100';
    #result1,recording_id = sched_rec(rec_obj,'01',start_time,duration = rec_duration);
    result1,recording_id = sched_rec(rec_obj,'01',start_time,rec_duration);

    if ("SUCCESS" in result1.upper()):
        media_obj.initiateReboot();
        rec_obj.resetConnectionAfterReboot();
        print "Execution  Success"
        #Prmitive test case which associated to this Script
        tdkTestObj = media_obj.createTestStep('RMF_DVRManager_CheckRecordingInfoById');
    
        expectedRes = "SUCCESS"
        recordingId = recording_id
        print "Requested record ID: %s"%recordingId
        tdkTestObj.addParameter("recordingId",recordingId);
    
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedRes);
    
        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result.upper():
            if recordingId in details:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "DVRManager CheckRecordingInfoById Successful: [%s]" %details;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Recording Details not properly updated";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "DVRManager CheckRecordingInfoById Failed: [%s]"%details;
    else:            
        print "Execution  failure"
         
    media_obj.unloadModule("mediaframework");
    rec_obj.unloadModule("rmfapp");
    
else:
    print "Failed to load media framework module";
    media_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load recorder module";
    rec_obj.setLoadModuleStatus("FAILURE");
