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
  <id>387</id>
  <version>1</version>
  <name>CC_SetGet_Invalid_AnalogChannel_20</name>
  <primitive_test_id>196</primitive_test_id>
  <primitive_test_name>CC_SetGet_AnalogChannel</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script is used to Set and get analog channel number.
Test Case ID : CT_ClosedCaption_20</synopsis>
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
    <test_case_id>CT_ClosedCaption_20</test_case_id>
    <test_objective>Closed Caption - Set and get analog channel number.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()        ccSetAnalogChannel(analogChannel) ccGetAnalogChannel(&amp;channel)</api_or_interface_used>
    <input_parameters>Categories : CCSetGetAnalogChannel :  Status (0 - CCStatus_OFF, 1 - CCStatus_ON), Userselection - A channel number must be &lt;= 8 (Since, analog channel support 8 channels).                         Example : 11</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the  ClosedCaption Manager component.                                 3. ClosedCaption_Manager_Agent will send a request to set analog channel (Invalid : 11) to the ClosedCaption Manager.                                                                    4. ClosedCaption Manager is unable to set the invalid value and sends message "Invalid Analog Channel" to the ClosedCaption_Manager_Agent. 5.ClosedCaption_Manager_Agent will return SUCCESS/FAILURE to the TM.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.          Checkpoint 2.Check the value which is being set is being got back by the get API.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_CC_Init    TestMgr_CC_SetGetAnalogChannel</test_stub_interface>
    <test_script>CC_SetGet_Invalid_AnalogChannel_20</test_script>
    <skipped>No</skipped>
    <release_version>M-21</release_version>
    <remarks/>
  </test_cases>
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
obj.configureTestCase(ip,port,'CC_SetGet_Invalid_AnalogChannel_20');

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
		  
    #calling closed caption API CC_SetGetAnalogChannel to set the analog channel number of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGet_AnalogChannel');
    analog_channel_num = 10; # 1 - 8
					
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("analog_channel_num", analog_channel_num);
    				
    #Execute the test case in STB
    cc_AnalogChannel_expectedresult="SUCCESS"
				
    tdkTestObj.executeTestCase(cc_AnalogChannel_expectedresult);
    cc_AnalogChannel_actualresult = tdkTestObj.getResult();
    cc_AnalogChannel_details = tdkTestObj.getResultDetails();
    print "cc_AnalogChannel_actualresult :%s" %cc_AnalogChannel_actualresult;
    analog_channel_num = "%s" %analog_channel_num ;
    print "Set analog_channel_num %s" %analog_channel_num;

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_AnalogChannel_expectedresult in cc_AnalogChannel_actualresult:
      print "Get analog channel number %s" %cc_AnalogChannel_details;
      if analog_channel_num in cc_AnalogChannel_details:
        tdkTestObj.setResultStatus("FAILURE");
        print "-- Get and set values of analog channel number are same --";
      else:
        tdkTestObj.setResultStatus("SUCCESS");
        print "--SUCCESS: Get and set values of analog channel number are not same --";
        print "SUCCESS: with %s" %tdkTestObj.getResultDetails();
    else:
      tdkTestObj.setResultStatus("SUCCESS");
      print "SUCCESS: Analog channel number is not set with %s" %tdkTestObj.getResultDetails();

  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In Initializing closed caption with %s " %cc_AnalogChannel_details;   
    print "Initialization result of closed caption : %s" %cc_Init_actualresult;
  
#Unload the cc module
  obj.unloadModule("cc");

else:
        print"Load module failed";	
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");				
