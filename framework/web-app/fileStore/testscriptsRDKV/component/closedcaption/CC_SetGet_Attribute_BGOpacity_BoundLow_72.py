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
  <id>1242</id>
  <version>1</version>
  <name>CC_SetGet_Attribute_BGOpacity_BoundLow_72</name>
  <primitive_test_id>194</primitive_test_id>
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Closed Caption - Set and get the  closed caption attribute of background opacity - Lower boundary value.	
Test case Id - CT_ClosedCaption_72</synopsis>
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
    <test_case_id>CT_ClosedCaption_72</test_case_id>
    <test_objective>Closed Caption - Set and get the  closed caption attribute of background opacity - Lower boundary value.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()                     ccSetAttributes(&amp;CCAttribute, AttributeType, ccType))                  ccGetAttributes(&amp;CCGetAttribute, ccType)</api_or_interface_used>
    <input_parameters>Categories : CCSetGetAttribute : *attrib - Pointer to cc attribute structure list, type - 4 (list value of charBgOpacity in the structure)(lower value), ccType - Digital/Analog.</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the closed caption manager with ClosedCaption Manager component.                        3.ClosedCaption_Manager_Agent will set the background opacity of the closed caption manager with ClosedCaption Manager component.                           4. ClosedCaption Manager component will return the foreground opacity through the ClosedCaption_Manager_Agent to the TM.                  5. ClosedCaption_Manager_Agent will return SUCCESS/FAILURE status based on the return value of  APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.          Checkpoint 2.Check the value which is being set is being got back by the get API.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_CC_Init  TestMgr_CC_SetGetAttribute</test_stub_interface>
    <test_script>CC_SetGet_Attribute_BGOpacity_BoundLow_72</test_script>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_BGOpacity_BoundLow_72');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "Closed caption module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "Closed caption module loaded successfully";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");
  
  #calling Closed Caption API "CC_Initialization"
  tdkTestObj = obj.createTestStep('CC_Initialization');
  cc_Init_expectedresult="SUCCESS";

  tdkTestObj.executeTestCase(cc_Init_expectedresult);
  cc_Init_actualresult = tdkTestObj.getResult();
  details=tdkTestObj.getResultDetails();
  print " cc_Init_actualresult  :%s" % cc_Init_actualresult;
  
  #Check for SUCCESS/FAILURE return value of CC_Initialization
  if "SUCCESS" in loadmodulestatus.upper():
    print "SUCCESS: Application successfully initialized with Closed Caption";
		  
    #calling closed caption API "CC_SetGetAttribute" to set the attribute (BGOpacity) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "Opacity";
    print "Categories value set to: %s" %categories	
    attrib_type = 8; 
    print "attrib_type value set to: %d" %attrib_type
    opacity_type = 0;
    print "Opacity type low bound value set to: %d" %opacity_type 
    cc_type = 0  #Digital / Analog
    print "cc_type value set to: %d" %cc_type
					
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", opacity_type);
    tdkTestObj.addParameter("ccType", cc_type);
    
    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS";			
    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    attrib_type = "%s" %opacity_type;
    print "Set Bg opacity low bound %s" %opacity_type;

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "Get Bg opacity %s" %cc_Get_Attribute_details;
      if attrib_type in cc_Get_Attribute_details:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- Get and set values of Bg opacity low bound are same --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "-- Get and set values of Bg opacity low bound are not same --";
        print "FAILURE: with %s " %tdkTestObj.getResultDetails(); 

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Bg opacity low bound attribute is not set with %s" %tdkTestObj.getResultDetails();

  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In Initializing closed caption with %s " %cc_Get_Attribute_details;   
    print "Initialization result of closed caption : %s" %cc_Init_actualresult;

  #Unload the cc module
  obj.unloadModule("cc");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
