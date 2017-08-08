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
  <id>462</id>
  <version>1</version>
  <name>RMF_HNSrcMPSink_Video_Volume_07</name>
  <primitive_test_id>289</primitive_test_id>
  <primitive_test_name>RMF_HNSrcMPSink_Video_Volume</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>These Script tests the RDK Mediaframework to get and set of volume in video in HNSrc MPSink pipeline. Test Case ID: CT_RMF_HNSrcMPSink_07.</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_HNSrc_MPSink_07</test_case_id>
    <test_objective>RMF_HNSRC_MPSink –To check the set &amp; get volume functionality of the HNSRC-MPSINK pipeline</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>HNSrc init()
HNSrc open()
MPSink init()
MPSink SetVideoRectangle()
MPSink SetSource()
HNSrc play()
HNSrc getState
HNSrc SetVolume()
HNSrc GetVolume()
HNSrc close()
MPSink term()
HNSrc term()</api_or_interface_used>
    <input_parameters>init: None
open:Char *,Char *
play:None
GetState:RMFState
setVolume: float – volume
GetVolume: None
SetVideoRectangle: unsigned.
unsigned, unsigned, 
Unsigned, bool apply_now – x,y,h,w,false
setSource: RMFMediaSourceBase*
close:None
term:None</input_parameters>
    <automation_approch>1.TM loads RMFStub_agent via the test agent.
2.TM will invoke “TestMgr_HNSrcMPSink_Video_Volume”.
3.RMFStub_agent will Initialize the Hnsrc element using init() and return the status based on the API return.
4.On success of init(),RMFStub_agent will input the streaming URL using open() and return the status based on the API return .
5.On success of open(),RMFStub_agent will the set the video co-ordinates using the setVideoRectangle() and return the status based on the API return.
6.On success of setVideoRectangle(),RMFStub_agent will connect the source with sink using setSource() and return the status based on the API return.
7.On success of SetSource(),RMFStub_agent will set the volume using SetVolume() and return the status based on the API return.
8.On success of SetVolume(),RMFStub_agent will play the stream using play() through connected sink and return the status based on the API return.
9.On success of play(),RMFStub_agent will get the volume value using GetVolume() and return the status based on the API return.
10.On Success of GetVolume(),close the video using close() and return the status based on the API return.
11.On success of close,RMFStub_agent will terminate using term() and return the status based on the API return 
12.RMFStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_HNSrcMPSink_Video_Volume_07</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import mediaframework;
import time; 
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_Volume_07');
#Get the result of connection with test component and STB
loadModuleStatus =obj.getLoadModuleResult();
print "Mediaframework module loading status :%s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_Volume_07');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in loadModuleStatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediaframework module loaded successfully";
	#Prmitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('RMF_HNSrcMPSink_Video_Volume');
        streamDetails = tdkTestObj.getStreamDetails('01'); 
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "PLAY URL : %s" %url;
        tdkTestObj.addParameter("playuri",url);

	volume = 0.9
	tdkTestObj.addParameter("Volume",volume);

	#Execute the test case in STB
	expectedresult="SUCCESS";
	tdkTestObj.executeTestCase(expectedresult);
	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	
	print "Setting Volume in Video using HNSrc MPSink Pipeline : %s" %actualresult;
	#compare the actual result with expected result
	if expectedresult in actualresult:
		#Set the result status of execution
		tdkTestObj.setResultStatus("SUCCESS");
		print "Setting Volume in Video using HNSrc MPSink Pipeline is success";
		time.sleep(20);
	else:
		tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();  
		print "Failure secnario : %s" %details;
		
	#unloading mediastreamer module
	obj.unloadModule("mediaframework");
else:
	print "Failed to load mediaframework module";
	obj.setLoadModuleStatus("FAILURE");
