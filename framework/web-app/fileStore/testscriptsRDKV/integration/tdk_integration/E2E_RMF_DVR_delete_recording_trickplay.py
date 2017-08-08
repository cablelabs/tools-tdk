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
  <version>9</version>
  <name>E2E_RMF_DVR_delete_recording_trickplay</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Try to delete the recorded when XG1  playing trick mode in same recorded content.</synopsis>
  <groups_id/>
  <execution_time>18</execution_time>
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
    <test_case_id>E2E_DVR_26</test_case_id>
    <test_objective>Try to delete the recorded when XG1  is in DVR Trickplay</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the LinearTV_agent for tune
3.LinearTV_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the HnSrc-&gt;Mpsink pipeline.
5.Play the Recorded content using HnSrc-&gt; Mpsink pipeline doing trickplay.
6.TM loads RMFStub_agent via the test agent.
7.TM will invoke “TestMgr_ deleteRecording"" with recordingId as a parameter in RMFStub_agent.
8.TM pass the parameters like duration and recording_id to Recorder_agent.
9.RMFStub_agent will call getinstance of Dvr Manager 
10.Call the methods  deleteRecording 
11 On success of API execution RMFStub_agent will send SUCCESS or FAILURE to TM."
12.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.
13.Depends on the result of above step agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from live playback
Checkpoint 2.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>MediaFramework_Stub
TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_delete_recording_trickplay</test_script>
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
import time;
from tdkintegration import deleteRecording,dvr_playback

#Test component to be tested
media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_delete_recording_trickplay');
media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_delete_recording_trickplay');

loadmodulestatus = tdk_obj.getLoadModuleResult();
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
                media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_delete_recording_trickplay');
                #Get the result of connection with test component and STB
                loadmodulestatus1 = media_obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadmodulestatus1;
                loadmoduledetails1 = media_obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails1;


if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    media_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");

    #Prmitive test case which associated to this Script
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    tdk_obj.resetConnectionAfterReboot()
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    

    if matchList:
		 
         print "Recording Details : " , matchList
         #fetch recording id from list matchList.
         recording_id = matchList[1]
         recording_id = recording_id.strip()
         result1 = dvr_playback(tdkTestObj,recording_id,play = 'trickplay');

         result2 = deleteRecording(media_obj,'01',recording_id);
        
         if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
               print "Execution  Success"  
     
        
	 else:            
                     print "Execution  failure"
	 media_obj.unloadModule("mediaframework");
         tdk_obj.unloadModule("tdkintegration");
  
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        media_obj.unloadModule("mediaframework");
        tdk_obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load media framework module";
    media_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load TDK module";
    tdk_obj.setLoadModuleStatus("FAILURE");
