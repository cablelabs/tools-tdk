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
  <id>1489</id>
  <version>1</version>
  <name>CC_SetGet_Attribute_FontColor_190</name>
  <primitive_test_id>194</primitive_test_id>
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>When CC text color is Black and background color is Blue, CC text color looks White
Test case ID- CT_ClosedCaption_190</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_ClosedCaption_190</test_case_id>
    <test_objective>Closed Caption - When CC text color is Black and background color is Blue, CC text color looks White</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>vlGfxInit(0)                                                     vlMpeosCCManagerInit()                  ccSetAttributes(&amp;CCAttribute, AttributeType, ccType))                  ccGetAttributes(&amp;CCGetAttribute, ccType)</api_or_interface_used>
    <input_parameters>Categories : CCSetGetAttribute : *attrib - Pointer to cc attribute structure list, type - 1 (list value of fontUnderline in the structure), Pointer to cc attribute structure list,         type - 0 (list value of charBgColor in the structure) BgColor, ccType - Digital/Analog.</input_parameters>
    <automation_approch>1. TM loads the ClosedCaption_Manager_Agent via the test agent.
2.ClosedCaption_Manager_Agent will initialize/start the  ClosedCaption Manager.                        3.ClosedCaption_Manager_Agent will set the font color  to (black)the ClosedCaption Manager.                                                    4.ClosedCaption_Manager_Agent will set the BG color  to (blue)                                                     
5.Test Manger will request the font color by calling get attributes.                                                                          6. ClosedCaption_Manager_Agent will return SUCCESS status based on the return value of  APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.          Checkpoint 2.Check the value which is being set is being got back by the get API.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_CC_Init  TestMgr_CC_SetGetAttribute</test_stub_interface>
    <test_script>CC_SetGet_Attribute_FontColor_190</test_script>
    <skipped>No</skipped>
    <release_version/>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_FontColor_190');

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
  if "SUCCESS" in cc_Init_actualresult.upper():
    print "SUCCESS: Application successfully initialized with Closed Caption";
    iterator = ['000000', 'FFFFFF', 'FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF'];
    iterator1 =['0','FFFFFF','FF0000','FF00','FF','FFFF00','FF00FF','FFFF'];

    #calling closed caption API "CC_SetGetAttribute" to set the attribute (FGColor-Black) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    attrib_type = 1; # To set Font color
    color_type1 = 0; # color type black
    cc_type = 0  #Digital / Analog

    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", color_type1);
    tdkTestObj.addParameter("ccType", cc_type);

    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS"

    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    #FG_color = "%s" %color_type1;
    print "Expected  font color  value is:  %s" %iterator1[color_type1];

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get font color value %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[color_type1] in retattribute:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- value of font color is as expected --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "FAILURE: value of font color is not as expected";

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the font color attribute" ;
    #calling closed caption API "CC_SetGetAttribute" to set the attribute (BGColor-Blue) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    attrib_type = 2; # To set BG color
    color_type2 = 4; # color blue
    cc_type = 0  #Digital / Analog

    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", color_type2);
    tdkTestObj.addParameter("ccType", cc_type);

    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS"

    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    #BG_Color = "%s" %color_type2;
    print "Expected  BG color value is:  %s" %iterator1[color_type2];

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get BG color value %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[color_type2] in retattribute:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- value of BG color is as expected --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "FAILURE: value of Bg color is not as expected";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the BG color attribute" ;

    #calling closed caption API "CC_SetGetAttribute" to get the attribute (FGColor) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    print "Categories value set to: %s" %categories
    attrib_type = 1; # To set Font color
    print "Attrib type value set to: %s" %attrib_type
    color_type3 = 1001; # default color type
    #print "Color type value set to: %s" %color_type3
    cc_type = 0  #Digital / Analog
    print "cc_type value set to: %s" %cc_type
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", color_type3);
    tdkTestObj.addParameter("ccType", cc_type);

    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS"

    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    #Default_Fg_color = "%s" %color_type3;
    print "Expected font color is:%s" %iterator1[1];
	
    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get font color %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[1] in retattribute:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- value of font color is as expected --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "FAILURE: value of font color is not as expected";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the default font color attribute" ;

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
