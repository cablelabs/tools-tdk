# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1579</id>
  <version>4</version>
  <name>E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Continuous switching of between live play and dvr playback for long duration(10hrs) - E2E_LinearTV_46</synopsis>
  <groups_id/>
  <execution_time>630</execution_time>
  <long_duration>true</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_39</test_case_id>
    <test_objective>LinearTV-Continuous switching of between live play and dvr playback for long duration(10hrs)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2. TM reads the property file and get the number of channels to tune.
3.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
4.Tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
5. TM Checks the validity of the urls.
6.TM sends the Response Url to the LinearTV_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds"
5. loop the steps 2-6  for a DVR playback and continue for ten hours
6. tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration</test_script>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def PlayURL(obj,ValidURL):    
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    print "Play Url Requested: %s"%(ValidURL);
    tdkTestObj.addParameter("playUrl",ValidURL);

    expectedresult = "SUCCESS";
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
        retValue = "FAILURE"
    
    return retValue
                                        
obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration');

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
                obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
        
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails('01');
    
    #Framing URL for Live Play Request
    url1 = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url1 == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");

    print "Request URL : %s" %url1;
    tdkTestObj.addParameter("Validurl",url1);

    expectedresult = "SUCCESS";

    #Execute the test case in STB 
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();

    #Remove unwanted part from URL
    PLAYURL = details.split("[RESULTDETAILS]");
    url1 = PLAYURL[-1];

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)
		 
    if matchList:
		 
         print "Recording Details : " , matchList

         #fetch recording id from list matchList.
         recordID = matchList[1]
         #Framing URL for DVR Play Request
         url2 = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1]);
         if url2 == "NULL":
           print "Failed to generate the Streaming URL";
           tdkTestObj.setResultStatus("FAILURE");

    
         if expectedresult in actualresult:

            for i in range(1,600):        
                                        
                #Calling the PlayURL function to play the requested URL
                result1 = PlayURL(obj,url1);
          
                #Calling the PlayURL function to play the requested URL
                result2 = PlayURL(obj,url2);
        
                if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
                    print "Execution Success at iteration %d"%i;
                else:            
                   print "Execution failure at iteration %d"%i;
                   break;
         else:
              tdkTestObj.setResultStatus("FAILURE");
              print "Json Response Parameter is Failure";
         
              obj.unloadModule("tdkintegration");
			  
    else:
         print "No Matching recordings list found"
					 
         time.sleep(10);
         obj.unloadModule("tdkintegration");
	
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
