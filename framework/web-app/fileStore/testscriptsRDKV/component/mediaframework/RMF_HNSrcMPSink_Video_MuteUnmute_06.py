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
  <id>461</id>
  <version>1</version>
  <name>RMF_HNSrcMPSink_Video_MuteUnmute_06</name>
  <primitive_test_id>287</primitive_test_id>
  <primitive_test_name>RMF_HNSrcMPSink_Video_MuteUnmute</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>These Script tests the RDK Mediaframework to enable mute and unmute in video in HNSrc MPSink pipeline. Test Case ID: CT_RMF_HNSrc_MPSink_06.</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
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
    <test_case_id>CT_RMF_HNSrc_MPSink_06</test_case_id>
    <test_objective>RMF_HNSRC_MPSink –To check the mute &amp; unmute functionality of the HNSRC-MPSINK pipeline</test_objective>
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
MPSink SetMuted()
MPSink GetMuted()
HNSrc close()
MPSink term()
HNSrc term()</api_or_interface_used>
    <input_parameters>init: None
open:Char *,Char *
play:None
GetState:RMFState
setMuted: bool – muted
GetMuted:none
SetVideoRectangle: unsigned.
unsigned, unsigned, 
Unsigned, bool apply_now – x,y,h,w,false
setSource: RMFMediaSourceBase*
close:None
term:None</input_parameters>
    <automation_approch>1.TM loads RMFStub_agent via the test agent.
2.TM will invoke “TestMgr_HNSrcMPSink_Video_MuteUnmute”.
3.RMFStub_agent will Initialize the Hnsrc element using init() and return the status based on the API return.
4.On success of init(),RMFStub_agent will input the streaming URL using open() and return the status based on the API return .
5.On success of open(),RMFStub_agent will call init api of MPsink return the status based on the API return
6.On success of setVideoRectangle(),RMFStub_agent will connect the source with sink using setSource() and return the status based on the API return.
7.On success of setSource(),RMFStub_agent will mute the audio using SetMuted() and return the status based on the API return.
8.On success of setMued(),RMFStub_agent will check the mute value using GetMuted() and return the status based on the API return.
9.On success of SetSource(),RMFStub_agent will play the stream using play() through connected sink and return the status based on the API return.
10.After defined period of play,Unmute the audio using SetMuted() and return the status based on the API return. 
11.On success of setMued(),RMFStub_agent will check the mute value using GetMuted() and return the status based on the API return.
12.On Success of getstate(),close the video using close() and return the status based on the API return.
13.On success of close,RMFStub_agent will terminate using term() and return the status based on the API return 
14.RMFStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_HNSrcMPSink_Video_MuteUnmute_06</test_script>
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
obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_MuteUnmute_06');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaframework module loading status :%s" %loadmodulestatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_MuteUnmute_06');
                #Get the result of connection with test component and STB
                loadmodulestatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadmodulestatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediaframework module loaded successfully";
	#Prmitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('RMF_HNSrcMPSink_Video_MuteUnmute');
        streamDetails = tdkTestObj.getStreamDetails('01');       
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "PLAY URL : %s" %url;
        tdkTestObj.addParameter("playuri",url);
	#Execute the test case in STB
	expectedresult="SUCCESS";
	tdkTestObj.executeTestCase(expectedresult);
	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	
	print "Video Mute using HNSrc MPSink Pipeline : %s" %actualresult;
	#compare the actual result with expected result
	if expectedresult in actualresult:
		#Set the result status of execution
		tdkTestObj.setResultStatus("SUCCESS");
		print "Video Mute using HNSrc MPSink Pipeline is success";
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
