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
  <id>1028</id>
  <version>4</version>
  <name>E2E_RMF_DVR_TrickPlay_35</name>
  <primitive_test_id>550</primitive_test_id>
  <primitive_test_name>TDKE2E_Rmf_Dvr_Skip_Backward_From_End</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>E2E_RMF_DVR_TrickPlay_35: To verify the video playback when Skip backward is done multiple times after the video has reached the end point.</synopsis>
  <groups_id/>
  <execution_time>20</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_TrickPlay_35</test_case_id>
    <test_objective>To verify the video playback when Skip backward is done multiple times after the video has reached the end point</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-XI3_1</test_setup>
    <pre_requisite>- At least one video must be selected for playing from recording list  with minimum duration of 3mins.           - No other recording is scheduled to start during the test.                                                                       - XG1 and XI3 board should be up and running in same network                                                                   - XG1 should have one or more recordings in it.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Parameters:
PlayURL: 'http://192.168.30.80:8080/vldms/dvr?rec_id=114556&amp;1&amp;play_speed=4.00&amp;time_pos=0.00' 
Rcount: 5
Seconds: 10</input_parameters>
    <automation_approch>1.TM loads endtoendrmf stub agent via the test agent.
2.TM frames and sends the request URL, number of times play pause sequence as to repeat and number of seconds to skip for endtoendrmf agent to play a video.
3.The endtoendrmf agent will send URL to XG1 and XG1 starts pushing the recorded content requested and XI3 can play it.
4.endtoendrmf agent will play the video by creating the HNSrc and MPSink pipeline and monitors the checkpoint.
4.endtoendrmf  agent will send SUCCESS or FAILURE to TM based on the checkpoints..</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's for success status.
Checkpoint 2: Check the /proc/video_status for video playing or not. If playing it will be “yes” else “no”.</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_TrickPlay_35</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>1.URL to get the list of recordings from XG1 in not working. 
2.Hardcoding the resquest URL for playing the video from XI3.</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Number of times the pause/play should repeat.
skipNumOfSec = 10;

#Number of repeatation
repeatCount = 5;

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_35');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_35');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKintegration module load successful";
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Skip_Backward_From_End');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Skip_Backward_From_End');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    

    if matchList:
		 
         print "Recording Details : " , matchList
         #fetch recording id from list matchList.
         recordID = matchList[1]
         url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );
         if url == "NULL":
             print "Failed to generate the Streaming URL";
             tdkTestObj.setResultStatus("FAILURE");

         print "The Play DVR Url Requested: %s"%url
         tdkTestObj.addParameter("playUrl",url);

         print "The number of seconds to be skiped from end of video: %d"%skipNumOfSec
         tdkTestObj.addParameter("seconds",skipNumOfSec);

         print "The number of repeatation requested is %d"%repeatCount
         tdkTestObj.addParameter("rCount",repeatCount);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR Skip number of seconds from end multiple times : %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Skip number of seconds from end multiple times Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Skip number of seconds from end multiple times Failed: [%s]"%details;
         
         obj.unloadModule("tdkintegration");
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKintegration module";
         obj.setLoadModuleStatus("FAILURE");
