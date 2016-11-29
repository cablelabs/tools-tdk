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
  <id>1651</id>
  <version>1</version>
  <name>TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test</name>
  <primitive_test_id>577</primitive_test_id>
  <primitive_test_name>TDKE2E_RMF_TSB_Play</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Channel Change and Linear Trickplay for long duration (8hr)
Test case ID - E2E_LinearTV_41</synopsis>
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
    <test_case_id>E2E_LinearTV_41</test_case_id>
    <test_objective>LinearTV-Channel Change and Linear Trickplay for longduration (8hr)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads Tdkintegration_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds"
5. TM selects a url for Trickplay
6 TM run the trickplay in 4x 15x 30x and 60x speeds
7. loop the steps 2-6  for each  channels  and trickplay rates
8. tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3 . Response logs verified to check the trickplay occur at the corresponding speeds.
Checkpoint 4. Script to check whether the audio pid and video pid is set</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import tdkintegration;
import time;
import timeit;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#Long duration test time period
testTimeInHours = 8
#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def getURL_PlayURL(obj,streamId):
    
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");
	return "FAILURE";

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
        
        #Primitive test case which associated to this Script
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
                                        
obj.configureTestCase(ip,port,'TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration');

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
                obj.configureTestCase(ip,port,'TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";	
    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
    #Stream details for tuning
    streamDetails = tdkTestObj.getStreamDetails('01');
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
        print "Json Response Parameter is success";   
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        #Remove unwanted part from URL
        PLAYURL = details;
        while (timer < testTime):
            startTime = 0
            startTime = timeit.default_timer()
            iteration = iteration + 1
            print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)
	
            #Calling the getURL_PlayURL function for the requested StreamID
            result1 = getURL_PlayURL(obj,'01');
            if ("SUCCESS" in result1.upper()):                                        
                print "Execution Success at iteration %d"%iteration;
            else:            
                print "Execution failure at iteration %d"%iteration;
                break;  
            #Calling the getURL_PlayURL function for the requested StreamID
            result2 = getURL_PlayURL(obj,'02');
    
            if ("SUCCESS" in result2.upper()):                                        
                print "Execution Success at iteration %d"%iteration;
            else:            
                print "Execution failure at iteration %d"%iteration;
                break;                                        

            #Primitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
            if iteration % 4 == 0:
                rate = 4.0; 
            elif  iteration % 4 == 1:
                rate = 15.0; 
            elif  iteration % 4 == 2:
                rate = 30.0; 
            elif  iteration % 4 == 3:
                rate = 60.0; 

            print "Speed rate value set : %f" %rate;
            tdkTestObj.addParameter("SpeedRate",rate);
            tdkTestObj.addParameter("VideostreamURL",PLAYURL);
            #Execute the test case in STB and pass the expected result
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            #Get the actual result of execution
            actualresult = tdkTestObj.getResult();
            print "Result of TSB Play : %s" %actualresult;
            #compare the actual result with expected result of Json response Parameter
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                print "E2E RMF TSB Playback Successful: [%s]"%details;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details =  tdkTestObj.getResultDetails();
                print "E2E RMF TSB Playback Failed: [%s]"%details;
                break;

	    			
            stopTime = timeit.default_timer()
            timer = timer + (stopTime - startTime)				
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Json Response Parameter is Failure";		
		
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
