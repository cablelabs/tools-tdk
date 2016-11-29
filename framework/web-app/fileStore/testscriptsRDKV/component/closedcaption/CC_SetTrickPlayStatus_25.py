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
  <id>364</id>
  <version>1</version>
  <name>CC_SetTrickPlayStatus_25</name>
  <primitive_test_id>192</primitive_test_id>
  <primitive_test_name>CC_SetTrickPlayStatus</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script is used to set the trickplay status of the closed caption to ON / OFF.
Test Case ID :CT_ClosedCaption_25</synopsis>
  <groups_id/>
  <execution_time>1</execution_time>
  <long_duration>false</long_duration>
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
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_ClosedCaption_25</test_case_id>
    <test_objective>Closed Caption - To set trickplay status of the closed caption to ON / OFF.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()                              ccSetTrickPlayStatus(status)</api_or_interface_used>
    <input_parameters>CCSetTrickPlayStatus : Status - 0 - OFF Trickplay, 1 - ON Trickplay</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the ClosedCaption Manager.                                                                      4. ClosedCaption Manager will set ON /OFF through the ClosedCaption_Manager_Agent to the TM.                                                                             5. ClosedCaption_Manager_Agent will return SUCCESS/FAILURE status based on the return value of  APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_CC_Init   TestMgr_CC_SetTrickPlayStatus</test_stub_interface>
    <test_script>CC_SetTrickPlayStatus_25</test_script>
    <skipped>No</skipped>
    <release_version>M-21</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("cc","1.3");

#Ip address of the selected STB for testing
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CC_SetTrickPlayStatus_25');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "Closed caption module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "Closed caption module loaded successfully";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");
  
  #calling Closed Caption API "CC_Initialization"
  tdkTestObj = obj.createTestStep('CC_Initialization');
  cc_Init_expectedresult="SUCCESS"
  
  tdkTestObj.executeTestCase(cc_Init_expectedresult);
  cc_Init_actualresult = tdkTestObj.getResult();
  details=tdkTestObj.getResultDetails();
  print "cc_Init_actualresult :%s" %cc_Init_actualresult;
  
  #Check for SUCCESS/FAILURE return value of CC_Initialization
  if "SUCCESS" in loadmodulestatus.upper():
    print "SUCCESS: Application successfully initialized with Closed Caption";
		  
    #calling closed caption API to set the attribute  of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetTrickPlayStatus');
    				
    #Execute the test case in STB
    cc_ResetTrickPlayStatus_expectedresult="SUCCESS"
    trickPlayStatus = 1;

    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("trickPlayStatus", trickPlayStatus);
				
    tdkTestObj.executeTestCase(cc_ResetTrickPlayStatus_expectedresult);
    cc_ResetTrickPlayStatus_actualresult = tdkTestObj.getResult();
    details=tdkTestObj.getResultDetails();
    print " cc_ResetTrickPlayStatus_actualresult :%s" % cc_ResetTrickPlayStatus_actualresult;
    print "trickPlayStatus :%s" %trickPlayStatus;
	  
    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_ResetTrickPlayStatus_expectedresult in cc_ResetTrickPlayStatus_actualresult:
      tdkTestObj.setResultStatus("SUCCESS");
      print "SUCCESS: In setting trickplay status";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Setting trickplay status %s" %details;
    
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In Initializing closed caption with %s " %details;   
    print "Initialization result of closed caption : %s" %cc_Init_actualresult;

  #Unload the cc module
  obj.unloadModule("cc");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");				
