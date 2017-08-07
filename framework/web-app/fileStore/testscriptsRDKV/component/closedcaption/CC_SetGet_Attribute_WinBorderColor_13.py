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
  <id>377</id>
  <version>1</version>
  <name>CC_SetGet_Attribute_WinBorderColor_13</name>
  <primitive_test_id>194</primitive_test_id>
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This test script is used to Set and get the  closed caption attribute of window border color.
Test Case ID :CT_ClosedCaption_13</synopsis>
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
    <test_case_id>CT_ClosedCaption_13</test_case_id>
    <test_objective>Closed Caption - Set and get the  closed caption attribute of window border color .</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()                      ccSetAttributes(&amp;CCAttribute, AttributeType, ccType))                  ccGetAttributes(&amp;CCGetAttribute, ccType)</api_or_interface_used>
    <input_parameters>Categories : CCSetGetAttribute : *attrib - Pointer to cc attribute structure list, type - 2 (list value of winColor in the structure), ccType - Digital/Analog.</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the closed caption manager with ClosedCaption Manager component.                        3.ClosedCaption_Manager_Agent will set the window color of the closed caption manager with ClosedCaption Manager component.                                                 4. ClosedCaption Manager component will return the window color through the ClosedCaption_Manager_Agent to the TM.                  5. ClosedCaption_Manager_Agent will return SUCCESS/FAILURE status based on the return value of  APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.          Checkpoint 2.Check the value which is being set is being got back by the get API.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_CC_Init  TestMgr_CC_SetGetAttribute</test_stub_interface>
    <test_script>CC_SetGet_Attribute_WinBorderColor_13</test_script>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_WinBorderColor_13');

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
    
    #calling closed caption API "CC_SetGetAttribute" to set the attribute (Win Border color) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    iterator = ['000000', 'FFFFFF', 'FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF'];
    categories = "color";
    attrib_type = 1024; # To set Win Border color
    border_type = 2;
    cc_type = 0  #Digital / Analog
					
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", border_type);
    tdkTestObj.addParameter("ccType", cc_type);

    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS";			
    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    attrib_type = "%s" %border_type;
    print "Set win  border color %s" %iterator[border_type];
    

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get win border color %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returened attirbute =%s" %retattribute;
      for cc_Get_Attribute_details in iterator:
        if iterator[border_type] in retattribute:
          flag = 0;           
        else:
          flag =1;
      if flag == 0:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- Get and set values of window border color are same --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "-- Get and set values of window border color are not same --";
        print "FAILURE: with %s" %tdkTestObj.getValue("details");

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: window border color attribute is not set with %s" %tdkTestObj.getValue("details");

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
