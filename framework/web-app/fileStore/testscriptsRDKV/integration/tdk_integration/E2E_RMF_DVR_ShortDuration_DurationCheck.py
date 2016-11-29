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
  <version>14</version>
  <name>E2E_RMF_DVR_ShortDuration_DurationCheck</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To schedule the  short duration recording and check the duration of the recorded content</synopsis>
  <groups_id/>
  <execution_time>14</execution_time>
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
    <test_case_id>E2E_DVR_37</test_case_id>
    <test_objective>Recorder-Schedule a short duration recording and check the size of the Recording</test_objective>
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
7.Check the size of the recording
8.The size must be similar to the time given
9.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.
15.Depends on the result of above step agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapRI_log to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>Recorder_Stub
MediaFramework_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_ShortDuration_DurationCheck</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
from tdkintegration import sched_rec

#Test component to be tested
media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_ShortDuration_DurationCheck');
media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_ShortDuration_DurationCheck');

loadmodulestatus = rec_obj.getLoadModuleResult();
loadmodulestatus1 = media_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;

loadmoduledetails1 = media_obj.getLoadModuleDetails();

if "FAILURE" in loadmodulestatus1.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails1:
                print "rmfStreamer is not running. Rebooting STB"
                media_obj.initiateReboot();
                #Reload Test component to be tested
                media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_ShortDuration_DurationCheck');
                #Get the result of connection with test component and STB
                loadmodulestatus1 = media_obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadmodulestatus1;
                loadmoduledetails1 = media_obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails1;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    media_obj.setLoadModuleStatus("SUCCESS");
    rec_obj.setLoadModuleStatus("SUCCESS");
    rec_duration = '60000';
    start_time = '0';
    result1,recording_id = sched_rec(rec_obj,'01',start_time,rec_duration);
        
    if ("SUCCESS" in result1.upper()):
	media_obj.initiateReboot();
	rec_obj.resetConnectionAfterReboot();
        print "Execution  Success"
        #Prmitive test case which associated to this Script
        tdkTestObj = media_obj.createTestStep('RMF_DVRManager_GetRecordingDuration');

        expectedRes = "SUCCESS"
        recordingId = recording_id;
        print "Requested record ID: %s"%recordingId
        tdkTestObj.addParameter("recordingId",recordingId);

        streamDetails = tdkTestObj.getStreamDetails('01');
        playUrl = tdkintegration.E2E_getStreamingURL(media_obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if playUrl == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");

        print "Requested play url : %s" %playUrl;
        tdkTestObj.addParameter("playUrl",playUrl);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedRes);

        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result.upper():
            #Set the result status of execution
            mylist = details.split(" ");
            print mylist[1];
            if( (int(mylist[1]) <= ((int(rec_duration)/1000) + 3)) and (int(mylist[1]) >= ((int(rec_duration)/1000) - 3))):
                tdkTestObj.setResultStatus("SUCCESS");
                print "DVRManager GetRecordingDuration Successful: %s" %details;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "DVRManager GetRecordingDuration Failed: The Recording Duration is not in range limit [%s]"%details;
        else:
             tdkTestObj.setResultStatus("FAILURE");
             print "DVRManager GetRecordingDuration Failed: [%s]"%details;

    else:            
        print "Execution  failure"
         
    media_obj.unloadModule("mediaframework");
    rec_obj.unloadModule("rmfapp");
    
else:
    print "Failed to load media framework module";
    media_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load recorder module";
    rec_obj.setLoadModuleStatus("FAILURE");
				
