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
  <id>1001</id>
  <version>12</version>
  <name>E2E_RMF_DVR_TrickPlay_06</name>
  <primitive_test_id>548</primitive_test_id>
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>E2E_RMF_DVR_TrickPlay_06: To verify the video playback when Fast Forward is done at 4x speed from the middle of the playback.</synopsis>
  <groups_id/>
  <execution_time>18</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
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
    <test_case_id>E2E_DVR_TrickPlay_06</test_case_id>
    <test_objective>To verify the video playback when Fast Forward is done at 4x speed from the middle of the playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-XI3_1</test_setup>
    <pre_requisite>- At least one video must be selected for playing from recording list with minimum duration of 3mins.             - No other recording is scheduled to start during the test.                                                                       - XG1 and XI3 board should be up and running in same network                                                      
- XG1 should have one or more recordings in it.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Parameters:
PlayURL: 'http://192.168.30.80:8080/vldms/dvr?rec_id=114556&amp;1&amp;play_speed=4.00&amp;time_pos=0.00' 
Speed: 4.0</input_parameters>
    <automation_approch>1.TM loads endtoendrmf stub agent via the test agent.
2.TM frames and sends the request URL and speed for endtoendrmf agent to play a video.
3.The endtoendrmf agent will send URL to XG1 and XG1 starts pushing the recorded content requested and XI3 can play it.
4.endtoendrmf agent will play the video by creating the HNSrc and MPSink pipeline and monitors the checkpoint.
4.endtoendrmf  agent will send SUCCESS or FAILURE to TM based on the checkpoints..</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's for success status.
Checkpoint 2.Check the speed retuned by HNSource getSpeed() API.
Checkpoint 3.Check the /proc/video_status for video playing or not. If playing it will be “yes” else “no”.</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_TrickPlay_06</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>1.URL to get the list of recordings from XG1 in not working. 
2.Hardcoding the resquest URL for playing the video from XI3.</remarks>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_01');
expected_Result="SUCCESS"

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
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_01');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
#Acquiring the instance of TDKScriptingLibrary for checking and verifying the DVR content.
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)

#The Pre-requisite success. Proceed to execute the test case.
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_06');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result;

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
		 
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

         #set the trick play speed
         trickPlayRate = 4.0
         print "The trick play rate: %f"%trickPlayRate
         tdkTestObj.addParameter("speed",trickPlayRate);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR playback when fast forward is done at 4x speed from the middle of the video : %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Playback 4x speed Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Playback 4x speed Failed: [%s]"%details;
         
         obj.unloadModule("tdkintegration");
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
