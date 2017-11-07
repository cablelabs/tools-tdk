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
  <id>453</id>
  <version>1</version>
  <name>RMF_MPSink_SetGetVolume_04</name>
  <primitive_test_id>279</primitive_test_id>
  <primitive_test_name>RMF_MPSink_SetGetVolume</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>These Script tests the RDK Mediaframework MPSink element to Set and get Volume.
Test Case ID: CT_RMF_MPSink_04</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_MPSink_04</test_case_id>
    <test_objective>RMF_MPSink – To set and get volume</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>init()
setVolume()
GetVolume()
term()</api_or_interface_used>
    <input_parameters>init:  None
setVolume: float – volume
GetVolume: None
term: None</input_parameters>
    <automation_approch>1.TM loads RMFStub_agent via the test agent.
2.TM will invoke “TestMgr_MPSink_SetGetVolume” in RMFStub_agent.
3.RMFStub_agent will call init() API of the component and get the result.
4.On the Success of init() API, RMFStub_agent will call setVolume() API of the component and get the result. 
5.On the Success of setVolume() API,RMFStub will call getVolume API of the component and get the result.
6.On success of getVolume() API, RMFStub_agent will call term() API of the component and get the result.
7.RMFStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1..Check for the value of  Volume after and before setting.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_MPSink_SetGetVolume_04</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_MPSink_SetGetVolume_04');
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
                obj.configureTestCase(ip,port,'RMF_MPSink_SetGetVolume_04');
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
        tdkTestObj = obj.createTestStep('RMF_MPSink_SetGetVolume');
        #Execute the test case in STB
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        #details = tdkTestObj.getResultDetails();
        print "MPSink initialized and Terminated : %s" %actualresult;
        #compare the actual result with expected result
        if expectedresult in actualresult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "MPSink Volume setted Successfully";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                #print "Failure secnario : %s" %details;
                print "Failed to do volume setting MPSink";
        #unloading mediastreamer module
        obj.unloadModule("mediaframework");
else:

        print "Failed to load mediaframework module";
        obj.setLoadModuleStatus("FAILURE");
