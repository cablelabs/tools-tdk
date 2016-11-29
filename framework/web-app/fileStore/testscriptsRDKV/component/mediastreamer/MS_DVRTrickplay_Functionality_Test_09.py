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
  <id>812</id>
  <version>1</version>
  <name>MS_DVRTrickplay_Functionality_Test_09</name>
  <primitive_test_id>95</primitive_test_id>
  <primitive_test_name>MediaStreamer_DVR_Trickplay</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script tests Requesting DVR Streaming url from Mediastreamer and playing it with all tricplay speeds.Test Case ID:CT_Mediastreamer_09.</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Mediastreamer_09</test_case_id>
    <test_objective>Mediastreamer –  Requesting for DVR trickplay with all supported play speeds and valid time_position.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.Mediastreamer executable should be running
2.XG1 should have one or more recordings in it.</pre_requisite>
    <api_or_interface_used>Streaming Interface</api_or_interface_used>
    <input_parameters>String-reocrdingId, Play speed, Time position</input_parameters>
    <automation_approch>1.TM loads Mediastreamer_agent via the test agent. 
2.Mediastreamer_agent will get RecorderId from wbdevice.dat file in XG1 and frames the query url to get list of recordings. “http://localhostip:port/vldms/info/recordingurls” 
3.Mediastreamer_agent will send the query url to the mediastreamer.
4.Mediastreamer_agent will get the list of recordings,captures to log file send it to TM.
5.TM will fetch a random url from the log file and send the url, play_speed and time_pos to Mediastreamer_agent.
6.Mediastreamer_agent will frame the url with play_speed and time_pos for playback with gstreamer playbin plugin.
7.Mediastreamer_agent will play the video and capture the mediastreamer log send it to TM via Test Agent.
8.TM will do the error checking by verifying the mediastreamer log.</automation_approch>
    <except_output>Checkpoint 1.Verifying the Player log. Player application will give the current position of stream for Successful play back.
Verifying the mediastreamer log. Mediastreamer log will have the pattern “next_predicted frame", difference of consecutive frames will give play_speed of DVR trickplay.</except_output>
    <priority>High</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_MediaStreamer_DVR_Trickplay</test_stub_interface>
    <test_script>MS_DVRTrickplay_Functionality_Test_09</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>Valid only for RDK 1.3</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Mediastreamer_09');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS"); 

        print "Mediastreamer module loaded successfully";
        #Calling the MediaStreamer_DVR_Trickplay function
        tdkTestObj = obj.createTestStep('MediaStreamer_DVR_Trickplay');
        #Pass the Play_speed And Time_position
        tdkTestObj.addParameter("timePosition","30000");
        #Passing All trick speed in Loop
        speeds = ['0.500000','-0.500000','4','-4','15','-15'];
        for i in speeds:
                print i;
                tdkTestObj.addParameter("PlaySpeed", i);
                #Execute the Test case and pass expected result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                print "Result of streaming : %s" %actualresult;
                #compare the actual result with expected result of playing video
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Mediastreamer streaming the video Successfully";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure secnario : %s" %details;
                        print "Mediastreamer failed to streaming the video at: %s" %i;
        print "Played with all speeds";
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
