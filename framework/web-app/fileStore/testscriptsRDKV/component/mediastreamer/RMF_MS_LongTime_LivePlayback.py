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
  <id>922</id>
  <version>3</version>
  <name>RMF_MS_LongTime_LivePlayback</name>
  <primitive_test_id>493</primitive_test_id>
  <primitive_test_name>MS_RMFStreamer_Player</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script test the Live playback of HD/SD content  via streaming Interface for a long period of time without changing the channel. CT_RMFStreamer_16</synopsis>
  <groups_id/>
  <execution_time>22</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Mediastreamer_16</test_case_id>
    <test_objective>RMFStreamer – Live playback of HD/SD content  via streaming Interface for a long period of time without changing the channel.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.RMFStreamer executable should be running</pre_requisite>
    <api_or_interface_used>Streaming Interface</api_or_interface_used>
    <input_parameters>String-Url
Eg: http://IP:Port/VideoStreamInit?srcId</input_parameters>
    <automation_approch>1.TM loads Mediastreamer_agent via the test agent. 
2.TM gets an ocapid from the streaming details page of the FW and generates the request url.
3.MediaStreamer_agent will get the request url and send to mediastreamer.
4.Upon receiving the Json response from mediastreamer, Mediastreamer_agent will extract the videoStreamingurl and play with Rmf Elements.
5.Mediastreamer_agent will play the video and capture the State of Video and send to TM via Test Agent.
6.TM will do the error checking by verifying the Rmf State of Video</automation_approch>
    <except_output>Checkpoint 1.RMFState of Hnsource and Mpsink pipeline is verified as success or failure</except_output>
    <priority>High</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_RMFStreamer_InterfaceTesting</test_stub_interface>
    <test_script>RMF_MS_LongTime_LivePlayback</test_script>
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
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_MS_LongTime_LivePlayback_25');
#Get the result of connection with test component and STB
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
                obj.configureTestCase(ip,port,'RMF_MS_LongTime_LivePlayback_25');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in loadModuleStatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediastreamer module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
        streamDetails = tdkTestObj.getStreamDetails('01');
        ValidURL = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
        print "Response URL : %s" %ValidURL;
        playtime = 600;
        tdkTestObj.addParameter("VideostreamURL",ValidURL);
        tdkTestObj.addParameter("play_time",playtime);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "Live Tune Playback : %s" %actualresult;
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Long Time Live Playback is Success";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "Long Time Live Playback is Failure: [%s]"%details;
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
