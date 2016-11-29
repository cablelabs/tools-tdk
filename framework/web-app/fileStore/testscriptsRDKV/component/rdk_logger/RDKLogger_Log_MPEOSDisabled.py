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
  <id>1441</id>
  <version>1</version>
  <name>RDKLogger_Log_MPEOSDisabled</name>
  <primitive_test_id>407</primitive_test_id>
  <primitive_test_name>RDKLogger_Log</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check that no message is logged when MPEOS debug support is disabled.
Test Case ID: CT_RDKLogger_37
Test Type: Negative</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks>Running this testcase would cause subsequent rdklogger testcases to fail</remarks>
  <skip>true</skip>
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
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RDKLogger_37</test_case_id>
    <test_objective>To add a log message when MPEOS debug support is disabled</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. RDK debug manager module should be intialized     2. EnableMPELog should be set to FALSE in debug.ini file</pre_requisite>
    <api_or_interface_used>rdk_dbg_MsgRaw()</api_or_interface_used>
    <input_parameters>rdk_dbg_MsgRaw:  

string – module (e.g., TEST)
String – level (e.g., INFO)
string - message (e.g., "Test Log message")</input_parameters>
    <automation_approch>1. TM loads RDKLoggerStub_agent via the test agent.
2. TM will invoke “TestMgr_RDKLogger_Log” in RDKLoggerStub_agent.
3. RDKLoggerStub_agent will call rdk_logger_init() API of the component and get the result.  
4. On success of rdk_logger_init() API, RDKLoggerStub_agent will call RDK_LOG() API of the component.
5. RDKLoggerStub_Agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1..Check that log message is not logged by the API.
Checkpoint 2.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>librdkloggerstub.so 
TestMgr_RDKLogger_Log</test_stub_interface>
    <test_script>RDKLogger_Log_MPEOSDisabled</test_script>
    <skipped>Yes</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
from tdklib import TDKScriptingLibrary;

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = TDKScriptingLibrary("rdklogger","2.0");
obj.configureTestCase(ip,port,'RDKLogger_Log_MPEOSDisabled');
#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RDKLogger_Log_MPEOSDisabled');

    expectedRes = "SUCCESS"

    module = "TEST1"
    print "Requested module: %s"%module
    tdkTestObj.addParameter("module",module);
    level = "ERROR"
    print "Requested level: %s"%level
    tdkTestObj.addParameter("level",level);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
        print "Logging failed with MPEOS Disabled as expected";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Logging successful with MPEOS Disabled: [%s]"%details;

    #Reset the logging to default
    obj.initiateReboot();

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
