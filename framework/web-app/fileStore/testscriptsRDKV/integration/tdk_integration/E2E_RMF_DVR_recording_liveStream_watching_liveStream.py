# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>3</version>
  <name>E2E_RMF_DVR_recording_liveStream_watching_liveStream</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis/>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>E2E_DVR_23</test_case_id>
    <test_objective>Recorder-Schedule a recording while watching live program of a different channel</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the LinearTV_agent for tune
3.LinearTV_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the HnSrc-&gt;Mpsink pipeline.
5. Play the recorded content using HnSrc-&gt; Mpsink pipeline.
6.TM loads Recorder_agent via the test agent.
7.TM gets an source_id of a different channel from the streaming details page of the FW and sends it to Recorder_agent to generate request url.
8.TM pass the parameters like duration and recording_id to Recorder_agent.
9.Recorder_agent will frame the json message to schedule the recording and send to TDK_Recorder_server which is present in TM.
10.Status of the Json response from Mediastreamer to TDK_Recorder_Server getting extracted by TM.
11 Recorder_agent  will do the error checking by verifying ocapri_logs.
12.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.
13.Depends on the result of above step agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from live TSB playback
Checkpoint 2 Status from the TDK_Recorder_server.
Checkpoint 3 Verifying the ocapRI_log to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>Recorder_Stub
TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_recording_liveStream_watching_liveStream</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import getURL_PlayURL,sched_rec

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_recording_liveStream_watching_liveStream');
tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_recording_liveStream_watching_liveStream');

loadmodulestatus = rec_obj.getLoadModuleResult();
loadmodulestatus1 = tdk_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                rec_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_recording_liveStream_watching_liveStream');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = rec_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    tdk_obj.setLoadModuleStatus("SUCCESS");
    rec_obj.setLoadModuleStatus("SUCCESS");
    
    result1,recording_id = sched_rec(rec_obj,'01','0',duration = "120000");

    result2 = getURL_PlayURL(tdk_obj,'02');  
    tdk_obj.initiateReboot();
    rec_obj.resetConnectionAfterReboot();
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution  Success"
    else:            
        print "Execution  failure"
         
    tdk_obj.unloadModule("tdkintegration");
    rec_obj.unloadModule("rmfapp");
    
else:
    print "Failed to load tdk module";
    tdk_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load recorder module";
    rec_obj.setLoadModuleStatus("FAILURE");
