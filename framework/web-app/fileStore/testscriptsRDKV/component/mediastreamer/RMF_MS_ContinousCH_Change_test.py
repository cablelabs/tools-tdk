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
  <id>912</id>
  <version>4</version>
  <name>RMF_MS_ContinousCH_Change_test</name>
  <primitive_test_id>491</primitive_test_id>
  <primitive_test_name>MS_RMFStreamer_InterfaceTesting</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script test the Live playback via streaming Interface by continuous channel change every 60 seconds. Test Case Id: CT_RMFStreamer_18</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Mediastreamer_18</test_case_id>
    <test_objective>RMFStreamer – stability test. Live playback via streaming Interface by continuous channel change every 60 seconds. (over night) and checking the CPU usage.</test_objective>
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
6.TM will do the error checking by verifying the Rmf State of Video.
7.Above steps 3-6 will be repeated for n times and send the result to TM.</automation_approch>
    <except_output>Checkpoint 1.RMFState of Hnsource and Mpsink pipeline is verified as success or failure</except_output>
    <priority>High</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_RMFStreamer_InterfaceTesting
2.TestMgr_RMFStreamer_Player</test_stub_interface>
    <test_script>RMF_MS_ContinousCH_Change_test</test_script>
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
obj.configureTestCase(ip,port,'RMF_MS_ContinousCH_Change_test_27');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus ;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        i = 0;
        for i in range(0,2):
                print "****************%d" %i;

                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
                streamDetails = tdkTestObj.getStreamDetails('01');
                details_url = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
                print "Response URL : %s" %details_url;
                playtime = 10;
                tdkTestObj.addParameter("VideostreamURL",details_url);
                tdkTestObj.addParameter("play_time",playtime);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();

                print "Live Tune Playback : %s" %actualresult;
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Live Playback is Success";
                        time.sleep(2);
                        #Prmitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
                        streamDetails = tdkTestObj.getStreamDetails('01');
                        details_response = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
                        playtime = 10;
                        tdkTestObj.addParameter("VideostreamURL",details_response);
                        tdkTestObj.addParameter("play_time",playtime);
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        print "Live Tune Playback : %s" %actualresult;
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Continous channel change Playback is Success";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                details3 = tdkTestObj.getResultDetails();
                                print "Continous channel change Playback is Failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print "Live Playback is Failure:%s"%details;
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
