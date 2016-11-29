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
  <id>818</id>
  <version>1</version>
  <name>MS_RecordingList_Format_Test_05</name>
  <primitive_test_id>90</primitive_test_id>
  <primitive_test_name>MediaStreamer_Recorded_Urls</primitive_test_name>
  <primitive_test_version>0</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script tests Requesting List of Recordings from Mediastreamer.
Test Case ID:CT_Mediastreamer_05</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Mediastreamer_05</test_case_id>
    <test_objective>Mediastreamer – Requesting to get the List of recordings via webservice interface</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1.Mediastreamer executable should be running
2.XG1 should have one or more recordings in it.</pre_requisite>
    <api_or_interface_used>Webservice Interface</api_or_interface_used>
    <input_parameters/>
    <automation_approch>1.TM loads Mediastreamer_agent via the test agent 
2.Mediastreamer_agent will get RecorderId from wbdevice.dat file in XG1 and frames the query url like “http://localhostip:port/vldms/info/recordingurls” to get list of recordings.
3.Mediastreamer_agent will send the query url to the mediastreamer.
4.Upon receiving the Html response, the Mediastreamer_agent will make it as a log file and send to TM.</automation_approch>
    <except_output>Checkpoint 1  Using the log file, verify at least one of the recording url is available.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>Mediastreamer_agent
1.TestMgr_MediaStreamer_Recorded_Urls</test_stub_interface>
    <test_script>MS_RecordingList_Format_Test_05</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>Valid only for RDK 1.3</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Mediastreamer_05');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        #Calling the MediaStreamer_Recorded_Urls function
        tdkTestObj = obj.createTestStep('MediaStreamer_Recorded_Urls');
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Mediastreamer Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "List of Recording content present";
                #Getting the URL List log file from DUT
                logpath=tdkTestObj.getLogPath();
                print "Log path in DUT : %s" %logpath;
                tdkTestObj.transferLogs(logpath,"false");

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "List of Recording content is not present";
                print "Failure secnario : %s" %details;
        #unloading Mediastreamer Module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load Mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
