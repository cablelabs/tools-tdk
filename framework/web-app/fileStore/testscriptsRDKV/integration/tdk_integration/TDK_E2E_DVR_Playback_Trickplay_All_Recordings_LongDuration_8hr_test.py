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
  <id>1627</id>
  <version>11</version>
  <name>TDK_E2E_DVR_Playback_Trickplay_All_Recordings_LongDuration_8hr_test</name>
  <primitive_test_id>556</primitive_test_id>
  <primitive_test_name>TDKE2E_Rmf_LinearTv_Dvr_Play</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>DVRTrick – To verify the  trickplay (4x 15x 30x and 60x) speeds are working the DVR recordings for long duration
Testcase Id: E2E_DVR_Skip_Fwd_16</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
  <long_duration>true</long_duration>
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
    <test_case_id>E2E_DVR_Skip_Fwd_16</test_case_id>
    <test_objective>DVRTrick – To verify the  trickplay (4x 15x 30x and 60x) speeds are working the DVR recordings for long duration(8hr)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-XI3_2</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>XG1 and XI3 board should be Up and running in same network

XG1 should have one or more recordings in it.</input_parameters>
    <automation_approch>1.TM loads Tdkintegration_agent via the test agent.
2. TM Frames the request url "http://ipaddress:8080/vldms/info/recordingurls" and makes a RPC call to the DVR_agent to get the list of recorded urls.
3. DVR_agent will send the url to XG1 and response is captured into the log file and send it to TM.
4. TM reads the log file to extract each recorded url and appends speed = trickspeed  and send it to the DVR_agent to play trhough mplayer.     
repeat the step4 for different trickspeds for 8hours</automation_approch>
    <except_output>Checkpoint 1.mplayer_actualresult value returned from the stub.</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>TDK_E2E_DVR_Playback_Trickplay_All_Recordings_LongDuration_8hr_test</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
import timeit;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

testTimeInHours = 8

obj.configureTestCase(ip,port,'TDK_E2E_DVR_Playback_Trickplay_All_Recordings');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'TDK_E2E_DVR_Playback_Trickplay_All_Recordings');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";

         #Primitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------
 
         duration = 4
         global matchList
         matchList = tdkTestObj.getRecordingDetails(duration);
         obj.resetConnectionAfterReboot()
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
         if matchList:
		 
             print "Recording Details : " , matchList

             #fetch recording id from list matchList.
             recordID = matchList[1]
             playSpeedlist = ['1.00','4.00','8.00','15.00','30.00','60.00']
             print "Play speed list : %s " %playSpeedlist

             testTime = testTimeInHours * 60 * 60
             testTime = 25 * 60
             timer = 0
             iteration = 0

             while (timer < testTime):

                 startTime = 0
                 startTime = timeit.default_timer()
                 iteration = iteration + 1
                 print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)
                 numberOfRecordings = 2
                 
                 for index in range (0, numberOfRecordings):
                     #recordID = recordingObj.getRecordingId(index)                   
                     print "\nRecord ID = %s" %recordID

                     for i in range (0, len(playSpeedlist)):

                         url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );

                         if url == "NULL":
                             print "Failed to generate the Streaming URL";
                             tdkTestObj.setResultStatus("FAILURE");
                         url = url + "&play_speed=" + playSpeedlist[i] + "&time_pos=0.00"

                         print "The Play DVR Url Requested: %s" %url
  
                         tdkTestObj.addParameter("playUrl",url);

                         #Execute the test case in STB
                         expectedresult="SUCCESS";
                         tdkTestObj.executeTestCase(expectedresult);

                         #Get the result of execution
                         actualresult = tdkTestObj.getResult();
                         details =  tdkTestObj.getResultDetails();

                         print "The E2E DVR playback of Fast Forward is tested with " + playSpeedlist[i].replace(".00","") + "x Speed from starting point of the video: %s" %actualresult;

                         #compare the actual result with expected result
                         if expectedresult in actualresult:
                             #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "E2E DVR Playback Successful: [%s]"%details;
                         else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "E2E DVR Playback Failed: [%s]"%details;

                         

                 stopTime = timeit.default_timer()
                 timer = timer + (stopTime - startTime)
      
             print "Total Time in Seconds = %f" %(timer) 
             obj.unloadModule("tdkintegration");
         else:
	 	   print "no mathching records are found"
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
