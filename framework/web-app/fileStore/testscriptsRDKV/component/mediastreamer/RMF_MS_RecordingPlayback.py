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
  <id>923</id>
  <version>4</version>
  <name>RMF_MS_RecordingPlayback</name>
  <primitive_test_id>493</primitive_test_id>
  <primitive_test_name>MS_RMFStreamer_Player</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>This scripts test the  Requesting  Recorded content playback via streaming Interface.
Test case Id: CT_RMFStreamer_17</synopsis>
  <groups_id/>
  <execution_time>12</execution_time>
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
    <test_case_id>CT_Mediastreamer_17</test_case_id>
    <test_objective>RMFStreamer – Requesting  Recorded content playback via streaming Interface.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.RMFStreamer executable should be running
2.XG1 should have one or more recordings in it.</pre_requisite>
    <api_or_interface_used>Streaming Interface</api_or_interface_used>
    <input_parameters>String-Url
Eg: http://IP:Port/VideoStreamInit?recId</input_parameters>
    <automation_approch>1.TM loads Mediastreamer_agent via the test agent. 
2.TM gets a rec_Id from the TM and generates the video url.
3. Mediastreamer_agent will get the video url and play with Rmf Elements.
4.Mediastreamer_agent will play the video and capture the State of Video and send to TM via Test Agent.
5.TM will do the error checking by verifying the Rmf State of Video.</automation_approch>
    <except_output>Checkpoint 1.RMFState of Hnsource and Mpsink pipeline is verified as success or failure</except_output>
    <priority>High</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_RMFStreamer_Player</test_stub_interface>
    <test_script>RMF_MS_RecordingPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
 
obj.configureTestCase(ip,port,'RMF_MS_RecordingPlayback_26');
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");
                obj.configureTestCase(ip,port,'RMF_MS_RecordingPlayback_26');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in loadModuleStatus.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "RmfStreamer load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------

         duration = 4
         matchList = []
         matchList = tdkTestObj.getRecordingDetails(duration);
         obj.resetConnectionAfterReboot()
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
	#-----------End-----------------
         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");
         time.sleep(2)
		 
         if matchList:
		 
              print "Recording Details : " , matchList

              #fetch recording id from list matchList.
              recordID = matchList[1]
        
              url = "http://"+ streamDetails.getGatewayIp() + ":8080/vldms/dvr?rec_id=" + recordID[:-1]; 
              print "The Play DVR Url Requested: %s"%url
              tdkTestObj.addParameter("VideostreamURL",url);
              playtime = 30;
              tdkTestObj.addParameter("play_time",playtime);         
              #Execute the test case in STB
              expectedresult="SUCCESS";
              tdkTestObj.executeTestCase(expectedresult);
          
              #Get the result of execution
              actualresult = tdkTestObj.getResult();
         

              print "The DVR to play in normal speed : %s" %actualresult;

              #compare the actual result with expected result
              if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "DVR Playback in normal speed";
              else:
                 tdkTestObj.setResultStatus("FAILURE");
                 details =  tdkTestObj.getResultDetails();
                 print "DVR Play in normal speed Failed :[%s]"%details;

         else:
               print "No Matching recordings list found"
         obj.unloadModule("mediastreamer");
else:
         print "Failed to RmfStreamer module";
         obj.setLoadModuleStatus("FAILURE");
