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
  <id>575</id>
  <version>1</version>
  <name>RMF_DVRManager_GetRecordingInfoById</name>
  <primitive_test_id>435</primitive_test_id>
  <primitive_test_name>RMF_DVRManager_GetRecordingInfoById</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This tests the get recording Info by Id functionality of DVR Manager class.
Test Case ID: CT_RMF_DVRMgr_04
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_DVRMgr_04</test_case_id>
    <test_objective>RMF_DVRMgr – To get the recording info by using the Id</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>valid recordingId</pre_requisite>
    <api_or_interface_used>DVRManager::getInstance()
GetRecordingInfoById</api_or_interface_used>
    <input_parameters>getRecordingInfoById:long long recordingId</input_parameters>
    <automation_approch>2.TM loads RMFStub_agent via the test agent.
2.TM will invoke “TestMgr_ getRecordingInfoById” with recordingId as a parameter in RMFStub_agent.
3.RMFStub_agent will call getinstance of Dvr Manager 
4.Call the methods  getRecordingInfoById() 
5.On success of API execution RMFStub_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status. Checkpoint 2.Check the return value of the recording Id and title and compare against the actual value.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_DVRManager_GetRecordingInfoById</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;
import random;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRManager_GetRecordingInfoById');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_DVRManager_GetRecordingInfoById');
                #Get the result of connection with test component and STB
                result = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %result;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

print "Mediaframework Dvr Mgr module loading status :%s" %result;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RMF_DVRManager_GetRecordingInfoById');

    expectedRes = "SUCCESS"
    recordingId = "6343"
    print "Requested record ID: %s"%recordingId
    tdkTestObj.addParameter("recordingId",recordingId);

    streamDetails = tdkTestObj.getStreamDetails('01');
    playUrl = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if playUrl == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");
    print "Requested play url : %s" %playUrl;
    tdkTestObj.addParameter("playUrl",playUrl);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    if "SUCCESS" in result.upper():
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "DVRManager GetRecordingInfoById Successful: [%s]" %details;
    else:
         tdkTestObj.setResultStatus("FAILURE");
         print "DVRManager GetRecordingInfoById Failed: [%s]"%details;

    #unloading mediastreamer module
    obj.unloadModule("mediaframework");
else:
    print "Failed to load mediaframework module";
    obj.setLoadModuleStatus("FAILURE");
