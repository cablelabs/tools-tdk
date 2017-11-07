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
  <id>1041</id>
  <version>5</version>
  <name>E2E_RMF_DVR_TrickPlay_50</name>
  <primitive_test_id>534</primitive_test_id>
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>E2E_RMF_DVR_TrickPlay_50: To verify the video playback when (Fast Forward/Rewind) is done at 4x speed from the starting point of the video and then (Skip Forward/Skip Backward) is done multiple times.</synopsis>
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
    <test_case_id>E2E_DVR_TrickPlay_50</test_case_id>
    <test_objective>To verify the video playback when (Fast Forward/Rewind) is done at 4x speed from the starting point of the video and then (Skip Forward/Skip Backward) is done multiple times</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-XI3_1</test_setup>
    <pre_requisite>- At least one video must be selected for playing from recording list.                                                          - No other recording is scheduled to start during the test.                                                                       - XG1 and XI3 board should be up and running in same network                                                                   - XG1 should have one or more recordings in it.
- Recording should be for long duration(2hrs).</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Parameters:
PlayURL: 'http://192.168.30.80:8080/vldms/dvr?rec_id=114556&amp;1&amp;play_speed=4.00&amp;time_pos=0.00' 
Skip Back: 10
Skip Forward: 10
Repeat Count: 5
Forward speed: 4.0
Rewind speed: -4.0</input_parameters>
    <automation_approch>1.TM loads endtoendrmf stub agent via the test agent.
2.TM frames and sends the request URL,skip forward/backward, speed and number of times to repeat for endtoendrmf agent to play a video.
3.The endtoendrmf agent will send URL to XG1 and XG1 starts pushing the recorded content requested and XI3 can play it.
4.endtoendrmf agent will play the video by creating the HNSrc and MPSink pipeline and monitors the checkpoint.
4.endtoendrmf  agent will send SUCCESS or FAILURE to TM based on the checkpoints..</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's for success status.
Checkpoint 2.Check the state returned by the getState API for pause state. 
Checkpoint 3. Check the /proc/video_status for video playing or not. If playing it will be “yes” else “no”.</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_TrickPlay_50</test_script>
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

#Set the trick play speed for forward
forwardPlaySpeed = 4;

#Set the trick play speed for rewind
rewindPlaySpeed = -4;

#Set the Number of seconds to skipforward.
skipForwardSec = 10

#Set the Number of seconds to skipbackward.
skipBackwardSec = 10

#Number of repeatation
repeatCount = 5;

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_50');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result; 
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_50');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    #Prmitive test case which associated to this Script
    tdkTestObj =obj.createTestStep('TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB');

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

         print "The trick play speed forward requested: %f"%forwardPlaySpeed
         tdkTestObj.addParameter("forwardSpeed",forwardPlaySpeed);

         print "The trick play speed rewind requested: %f"%rewindPlaySpeed
         tdkTestObj.addParameter("rewindSpeed",rewindPlaySpeed);

         print "The number of seconds to skip forward requested: %d"%skipForwardSec
         tdkTestObj.addParameter("sfSeconds",skipForwardSec);

         print "The number of seconds to skip backward requested: %d"%skipBackwardSec
         tdkTestObj.addParameter("sbSeconds",skipBackwardSec);

         print "The number of repeatation requested is %d"%repeatCount
         tdkTestObj.addParameter("rCount",repeatCount);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);
         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time: %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time Failed: [%s]"%details;
         
         obj.unloadModule("tdkintegration");
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
