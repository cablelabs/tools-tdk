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
  <id>1081</id>
  <version>2</version>
  <name>E2E_LinearTV_H.264_AAC_26</name>
  <primitive_test_id>528</primitive_test_id>
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script tests the playback of H.264 video with AAC audio service in End-to-End scenario Test Case ID : E2E_LinearTV_26</synopsis>
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
    <test_case_id>E2E_LinearTV_26</test_case_id>
    <test_objective>LinearTV – To Verify Playback of a stream with H.264 (Transport Stream) Video with AAC.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the LinearTV_agent for tune
3.LinearTV_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the mplayer application.</automation_approch>
    <except_output>Checkpoint 1.Verifying the mplayer log for successful playback of H.264/AAC streams. Mplayer log will have the pattern "+++" for Successful play back.
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TDKIntegrationStub</test_stub_interface>
    <test_script>E2E_LinearTV_H.264_AAC_26</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_Rmf_LinearTV_H.264_AAC_26');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "TDKIntegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "TDKIntegration module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://"+streamDetails.getOCAPID();
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
                PLAYURL = details.split("[RESULTDETAILS]");
                ValidURL = PLAYURL[-1];
                print "Json Response Parameter is success";
                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_Play_URL');

                tdkTestObj.addParameter("playUrl",ValidURL);

                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);

                #Get the result of execution
                actualresult = tdkTestObj.getResult();


                print "The E2E LinearTv Play : %s" %actualresult;

                #compare the actual result with expected result
                if expectedresult in actualresult:
                      #Set the result status of execution
                      tdkTestObj.setResultStatus("SUCCESS");

                      print "E2E LinearTv Playback Successful: [%s]"%details;
                else:
                      tdkTestObj.setResultStatus("FAILURE");
                      details =  tdkTestObj.getResultDetails();
                      print "E2E LinearTv Playback Failed: [%s]"%details;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json Response Parameter is Failure";
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
