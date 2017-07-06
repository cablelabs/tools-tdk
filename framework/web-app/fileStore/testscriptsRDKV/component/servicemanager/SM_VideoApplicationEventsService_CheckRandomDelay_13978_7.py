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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_VideoApplicationEventsService_CheckRandomDelay_13978_7</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_VideoApplicationEventsService_SetApplications</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks if random delay is calculated correctly with multiple applications set</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <except_output></except_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import json;
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_VideoApplicationEventsService_CheckRandomDelay_13978_7');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus;

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "org.openrdk.videoApplicationEvents_1";
        #Register Service
        register = servicemanager.registerService(smObj,serviceName);

        if "SUCCESS" in register:
                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                maxRandDelay = 5;
                inputList = []
                inputValue = {"applicationName": "advertisement", "maxRandomDelay": maxRandDelay, "filters": None}
                inputList.append(inputValue.copy())
                inputValue = {"applicationName": "buy_this1", "maxRandomDelay": 15, "filters": None}
                inputList.append(inputValue.copy())
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("service_name", serviceName);
                tdkTestObj.addParameter("method_name", "setApplications");
                tdkTestObj.addParameter("params", inputList);
                tdkTestObj.addParameter("inputCount", 1);
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        print "Application set successfully\n";
                        tdkTestObj.setResultStatus("SUCCESS");
                        #Prmitive test case which associated to this Script
                        tdkTestObj = smObj.createTestStep('SM_Generic_CallMethod');
                        expectedresult = "SUCCESS";
                        tdkTestObj.addParameter("service_name", serviceName);
                        tdkTestObj.addParameter("method_name", "getApplications");
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Application retrieved successfully";
                                resultDetails = tdkTestObj.getResultDetails();
                                outputList = json.loads(resultDetails);
                                print "RESULT DETAILS: %s" %outputList;
                                print "INPUTLIST: %s" %inputList;
                                logpath = "/opt/TDK/logs/AgentConsole.log";
                                filepath = tdkTestObj.transferLogs( logpath, "false" );
                                agentlog = open(filepath,'r');
                                actualresult = 'FAILURE';
                                for line in iter(agentlog):
                                        if ('Delay calculated' in line):
                                                randDelay = int(line.split('-')[1].strip());
                                                print "Random Delay Calulated is:%d" %randDelay;
                                                if randDelay >= 0 and randDelay <= (maxRandDelay * 1000):
                                                        print "Random Delay correct\n";
                                                        actualresult = 'SUCCESS';
                                                else:
                                                        print "Random Delay not correct\n";
                                                break;
                                tdkTestObj.setResultStatus(actualresult);

                        else:
                                print "Application retrieval failed\n";
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        print "Application set failed\n";
                        tdkTestObj.setResultStatus("FAILURE");

                print "[TEST EXECUTION RESULT] : %s" %actualresult;

                unregister = servicemanager.unRegisterService(smObj,serviceName);
        smObj.unloadModule("servicemanager");
else:
         print "Failed to load service manager module\n";

