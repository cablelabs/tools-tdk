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
  <id>1685</id>
  <version>1</version>
  <name>E2E_RMF_MDVR_TrickPlay_RadioChannel</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>LinearTV – Try to select trick play when device is in Radio channel</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_46</test_case_id>
    <test_objective>LinearTV-Switching between live and TSB mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>"1.TM loads TDKIntegration_agent via the test agent
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM for an ocap-idand sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds
5.tdkintegration_agent will get request url from TM for the HD channel ocap-idand sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
6.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds"
7.TM loads TDKIntegration_agent via the test agent 
8.TDKIntegration_agent Frames the request URL after getting ocapId from the TM and  makes a RPC calls to the TDKIntegration_agent for tune.
9.TDKIntegration_agent will  send framed url to the rmfStreamer.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
10.TM sends the Response Url to the TDKIntegration_agent for playback with the HnSrc-&gt;MPSink Pipeline.
11.TM Sends the speed value to TDKIntegration_agent to achieve Live trickplay. 
12.By Comparing Set and GetSpeed API of HNSrc,</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and gett the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>E2E_RMF_MDVR_TrickPlay_RadioChannel</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_MDVR_TrickPlay_RadioChannel');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_MDVR_TrickPlay_RadioChannel');
                #Get the result of connection with test component and STB
                loadmodulestatus =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "tdkintegration module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('R01');
        #Framing URL for Request
        url = tdkintegration.E2E_getStreamingURL(obj, "TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "Request URL : %s" %url;
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
                PLAYURL = details;
                
                print "Json Response Parameter is success";
                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
                rate = 0.5;
                tdkTestObj.addParameter("SpeedRate",rate);
                tdkTestObj.addParameter("VideostreamURL",PLAYURL);
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
                        print "E2E RMF TSB Playback Successful: [%s]"%details;
                else:
                	tdkTestObj.setResultStatus("FAILURE");
                        details =  tdkTestObj.getResultDetails();
                        print "E2E RMF TSB Playback Failed: [%s]"%details;
        else:
        	tdkTestObj.setResultStatus("FAILURE");
                print "Json Response Parameter is Failure";
        
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
