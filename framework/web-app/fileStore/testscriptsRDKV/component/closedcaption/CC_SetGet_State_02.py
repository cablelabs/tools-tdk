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
  <id>352</id>
  <version>1</version>
  <name>CC_SetGet_State_02</name>
  <primitive_test_id>182</primitive_test_id>
  <primitive_test_name>CC_SetGet_State</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script is used to Start and stop closed caption renderring.
Test Case ID :CT_ClosedCaption_02</synopsis>
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
    <test_case_id>CT_ClosedCaption_02</test_case_id>
    <test_objective>Closed Caption – Start and stop closed caption renderring.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()                          ccSetCCState(ccStatus, 0)</api_or_interface_used>
    <input_parameters>0 - CCStatus_OFF
1 - CCStatus_ON</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the  ClosedCaption Manager.                        3.ClosedCaption_Manager_Agent will stop the closed  ClosedCaption Manager.
4. ClosedCaption_Manager_Agent will return SUCCESS/FAILURE status based on the return value of  APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>TestMgr_CC_Init TestMgr_CC_SetGetState</test_stub_interface>
    <test_script>CC_SetGet_State_02</test_script>
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
obj.configureTestCase(ip,port,'CC_SetGet_State_02');

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
  print " cc_Init_actualresult  :%s" % cc_Init_actualresult;
  
  #Check for SUCCESS/FAILURE return value of CC_Initialization
  if "SUCCESS" in loadmodulestatus.upper():
    print "SUCCESS: Application successfully initialized with Closed Caption";
    
    #calling closed caption API "CC_SetGet_Status" to set the closed caption status
    tdkTestObj = obj.createTestStep('CC_SetGet_State');
    Status = 1; # Must be either 0 or 1, 0 - OFF and 1 - ON
				
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("status", Status);
				
    #Execute the test case in STB
    cc_Set_expectedresult="SUCCESS"
				
    tdkTestObj.executeTestCase(cc_Set_expectedresult);
    cc_Set_actualresult = tdkTestObj.getResult();
    print "cc_Set_actualresult :%s" %cc_Set_actualresult;
    Setstatusdetails =tdkTestObj.getResultDetails();
    print "Set statusdetails : %s" %Status;
    Status = "%s" %Status;
	  
    #Check for SUCCESS/FAILURE return value for the closed caption status set.
    if cc_Set_expectedresult in cc_Set_actualresult:
      print "CC is set to render successfully";
      print "get status details %s" %Setstatusdetails;
      if Status in Setstatusdetails:
        tdkTestObj.setResultStatus("SUCCESS");
        print "SUCCESS: Set and Get values of status is same";


 #calling closed caption API "CC_SetGet_Status" to set the closed caption status
    tdkTestObj = obj.createTestStep('CC_SetGet_State');
    Status = 0; # Must be either 0 or 1, 0 - OFF and 1 - ON
				
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("status", Status);
				
    #Execute the test case in STB
    cc_Set_expectedresult="SUCCESS"
				
    tdkTestObj.executeTestCase(cc_Set_expectedresult);
    cc_Set_actualresult = tdkTestObj.getResult();
    print "cc_Set_actualresult :%s" %cc_Set_actualresult;
    Setstatusdetails =tdkTestObj.getResultDetails();
    print "Set statusdetails : %s" %Status;
    Status = "%s" %Status;
	  
    #Check for SUCCESS/FAILURE return value for the closed caption status set.
    if cc_Set_expectedresult in cc_Set_actualresult:
      print "CC is set to render successfully";
      print "get status details %s" %Setstatusdetails;
      if Status in Setstatusdetails:
        tdkTestObj.setResultStatus("SUCCESS");
        print "SUCCESS: Set and Get values of status is same";


      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "FAILURE: Set and Get values of status is not same with %s" %tdkTestObj.getResultDetails();   

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: with %s" %tdkTestObj.getResultDetails();   
	
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In Initializing closed caption with %s " %tdkTestObj.getResultDetails();   
    print "Initialization result of closed caption : %s" %cc_Init_actualresult;

  #Unload the cc module
  obj.unloadModule("cc");

else:
        print"Load module failed";	
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
