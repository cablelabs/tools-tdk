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
  <id>1655</id>
  <version>1</version>
  <name>TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Continuous channel change for long duration (8hr). 
Test case ID - E2E_LinearTV_40</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
  <long_duration>true</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_40</test_case_id>
    <test_objective>LinearTV-Continuous channel up  for long duration(8hr)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads Tdkintegration_agent via the test agent 
2. TM reads the channel information from the configuration file.
3.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
4.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
5.TM sends the Response Url to the LinearTV_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds"
6. loop the steps 2-5  for each channel listed in the configuration file and continue for eight hours
7. tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3. Script to check whether the audio pid and video pid is set</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
import timeit;
import os;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

testTimeInHours = 8
configFile = 'testscriptsRDKV/integration/tdk_integration/TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test.config'

def getURL_PlayURL(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);        

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    
    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        details =  tdkTestObj.getResultDetails();
        
        #Remove unwanted part from URL
        PLAYURL = details.split("[RESULTDETAILS]");
        ValidURL = PLAYURL[-1];        

        expectedresult="SUCCESS";
        
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        print "Play Url Requested: %s"%(ValidURL);
        tdkTestObj.addParameter("playUrl",ValidURL);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();        
        print "The E2E LinearTv Play : %s" %actualresult;

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "E2E LinearTv Playback Successful: [%s]"%details;
            retValue = "SUCCESS"
            
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details =  tdkTestObj.getResultDetails();            
            print "Execution Failed: [%s]"%(details);
            retValue = "FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Json Response Parameter is Failure";
        retValue = "FAILURE";    
    
    return retValue
                                        
obj.configureTestCase(ip,port,'TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test');

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
                obj.configureTestCase(ip,port,'TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    # Fetching list of actions to be performed from configuration file
    itemList = obj.readConfigFile(configFile)
	
    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0

    while (timer < testTime):

        startTime = 0
        startTime = timeit.default_timer()
        iteration = iteration + 1
        print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)

        # Parsing through list and executing each step
        for step in range(0,len(itemList)):

            if itemList[step][0] == '#':
                continue

            if "START" in itemList[step]:
                print "Starting Execution"

            elif "END" in itemList[step]:
                print "End of Execution"

            elif "CHANNEL_ID" in itemList[step]:
                channelID = ''.join(itemList[step].splitlines()).split(":")[-1]
                print "Tuning to channel with stream ID : " , channelID

                #Calling the getURL_PlayURL function for the requested StreamID
                result = getURL_PlayURL(obj,channelID);
                if ("SUCCESS" in result.upper()):
                    print "Execution Success at iteration";
                else:
                    print "Execution failure at iteration";

            elif "DELAY" in itemList[step]:
                delayTime = itemList[step].split(":")[-1]
                print "Delay for " + delayTime + " seconds"
                time.sleep(int(delayTime))
				
        stopTime = timeit.default_timer()
        timer = timer + (stopTime - startTime)
					
    print "Total Time in Seconds = %f" %(timer)		
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
