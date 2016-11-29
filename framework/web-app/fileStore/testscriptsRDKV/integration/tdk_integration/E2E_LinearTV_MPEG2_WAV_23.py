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
  <id>1078</id>
  <version>2</version>
  <name>E2E_LinearTV_MPEG2_WAV_23</name>
  <primitive_test_id>529</primitive_test_id>
  <primitive_test_name>TDKE2E_LinearTV_URL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script tests the playback of MPEG2 video with WAV audio service in End-to-End scenario Test Case ID : E2E_LinearTV_23</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_23</test_case_id>
    <test_objective>LinearTV – To Verify Playback of a stream with MPEG-2(Transport Stream) Video with WAV.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the LinearTV_agent for tune
3.LinearTV_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the mplayer application.</automation_approch>
    <except_output>Checkpoint 1.Verifying the mplayer log for successful playback of MPEG-2/WAV streams. Mplayer log will have the pattern "+++" for Successful play back.
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>E2E_LinearTV_MPEG2_WAV_23</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","1.2");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_LinearTV_MPEG2_WAV_23');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("FAILURE");
        #Calling LinearTV_URL Function to send Request url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        channeltype =streamDetails.getChannelType();
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?recorderId="+streamDetails.getRecorderID()+"&video="+streamDetails.getVideoFormat()+"&audio=&"+streamDetails.getAudioFormat()+"live=ocap://"+streamDetails.getOCAPID();
        print "Request URL : %s" %url;
        #Passing Parameter as url
        tdkTestObj.addParameter("Validurl",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();

        print "Result of Json Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                #Remove unwanted part from URL
                PLAYURL = details.split("[RESULTDETAILS]");
                print "PLAY URL = "+PLAYURL[-1];
                print "Json Response Parameter is success";
                #Calling LinearTV_Play_URL Function to play the stream
                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_Play_URL');
                #Adding Parameter as validURL
                tdkTestObj.addParameter("videoStreamURL",PLAYURL[-1]);
                #Execute the test case in STB and pass the expexted result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                print "Result of Player : %s" %actualresult;
                #compare the actual result with expected result of playing video
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "MPEG2/WAV streams Tuned and played successfully";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to Tune and  play MPEG2/WAV streams";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json response parameter is Failed";
        #Unloading tdkintegration module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load tdkintegration module";
        obj.setLoadModuleStatus("FAILURE");
