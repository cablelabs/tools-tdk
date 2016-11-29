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
  <id>1148</id>
  <version>1</version>
  <name>E2E_LinearTV_Live_Trickplay_FFW_15x_11</name>
  <primitive_test_id>575</primitive_test_id>
  <primitive_test_name>TDKE2E_LinearTV_T2p_Tuning</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script tests the playback of Fast forward with play speed 15x in LinearTV trickplay scenario Test Case ID : E2E_LinearTV_11</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_LiveTrickplay_11</test_case_id>
    <test_objective>LinearTV – To verify  trickplay rates of 15x than normal stream speed in forward directions for playback.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. XG1 should be up and running                                                             2. The scripts T2pTuning.sh and T2pTrickMode.sh should be in the tdk path directory.</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent                        
2.TM request the ocapId of the channel to be tuned and makes a RPC calls to the LinearTV_agent for tuning.             
3.LinearTV_agent will get ocapId and tunes to that ocapId through T2p message. Upon receiving the T2p response the agent should extract the status of tuning and send to TM.      
4.TM will send T2p msg for pause for about minimum of 15 seconds so that the content is recorded in TSB
5.TM passes the playback rate to the LinearTV_agent.           
6.LinearTV_agent creates the t2p message request and sends it to video proxy. Upon receiving the t2p message response the LinearTV_agent extracts Success or Failure message and sends it to TM.</automation_approch>
    <except_output>Checkpoint 1. Verifying the response of t2p message from the video proxy for successful playback trick play with “15x”  forward direction. T2p message will have the response message as rate=15, status=”OK” and statusMessage=”Trick Mode request successful”.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_LinearTV_Live_Trickplay_FFW_15x_11</test_script>
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
obj = tdklib.TDKScriptingLibrary("tdkintegration","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_LinearTV_Live_Trickplay11');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "TDKintegration module loading status :  %s" %loadmodulestatus;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_LinearTV_Live_Trickplay11');
                #Get the result of connection with test component and STB
                loadmodulestatus =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        print "TDKintegration module loaded successfully.";
        obj.setLoadModuleStatus("SUCCESS");
        #Calling LinearTV_URL function to send the url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_Tuning');

        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');

        ocapId = "ocap://"+streamDetails.getOCAPID();
        print "Request OCAP ID for tuning : %s" %ocapId;
        tdkTestObj.addParameter("ValidocapId",ocapId);

        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);

        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        #print "Tuned result log-path = %s" %tdkTestObj.getValue("log-path");
        print "Result of Json Response for Tuning : %s" %actualresult;

        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Json Response tuning is success";

                #Sleep for 2 second before pausing. After tuning to different frequency.
                time.sleep(2);
                #Calling LinearTV_T2p_TrickMode Function for pausing the stream.
                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_TrickMode');
                pauserate = 0.0;
                tdkTestObj.addParameter("trickPlayRate",pauserate);
                tdkTestObj.addParameter("VideostreamURL",details);
                 #Execute the test case in STB and pass the expected result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);

                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                print "Result of T2p Trick Mode Pause: %s" %actualresult;

                #compare the actual result with expected result from the T2p trick mode response.
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Paused Successfully ";

                        #Sleep for 15 seconds for recording the content into TSB.
                        print "Paused for 15 seconds.. Please wait"
                        time.sleep(15);

                        #Calling LinearTV_T2p_TrickMode Function by passing the play back rate.
                        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_TrickMode');
                        rate = 15.0;
                        tdkTestObj.addParameter("trickPlayRate",rate);
                        tdkTestObj.addParameter("VideostreamURL",details);
                        #Execute the test case in STB and pass the expected result
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);

                        #Get the actual result of execution
                        actualresult = tdkTestObj.getResult();
                        print "Result of T2p Trick Mode: %s" %actualresult;
                        #print "TricK Mode result log-path = %s" %tdkTestObj.getValue("log-path");

                        #compare the actual result with expected result from the T2p trick mode response.
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Fast forward with 15.0x is played successfully ";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to play fast forwad with 15.0x";
                else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "Json response Failed to Pause";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json response Failed to tune";

        #Unloading Tdkintegration module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load LinearTV module";
        obj.setLoadModuleStatus("FAILURE");
