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
  <id>1498</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CC_SetGet_Attribute_FontColor_196</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>194</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CC should be displayed font color : white and background color :yellow				
Test case Id - CT_ClosedCaption_196</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_FontColor_196');

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
    iterator = ['000000', 'FFFFFF', 'FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF'];
    iterator1 =['0','FFFFFF','FF0000','FF00','FF','FFFF00','FF00FF','FFFF'];

    #calling closed caption API "CC_SetGetAttribute" to set the attribute (FGColor-White) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    attrib_type = 1; # To set Font color
    color_type1 = 1; # color type White
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
    FG_color = "%s" %color_type1;
    print "Expected  font color  value is:  %s" %iterator1[color_type1];

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get font color value %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[color_type1] in retattribute:
        flag = 0;
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- value of font color is as expected --";
      else:
        flag =1;
        tdkTestObj.setResultStatus("FAILURE");
        print "--  value of font color is not as expected --";

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the font color attribute" ;
    #calling closed caption API "CC_SetGetAttribute" to set the attribute (BGColor-Yellow) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    attrib_type = 2; # To set BG color
    color_type2 = 5; # color Yellow
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
    BG_Color = "%s" %color_type2;
    print "Expected  BG color value is:  %s" %iterator1[color_type2];

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get BG color value %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[color_type2] in retattribute:
        flag = 0;
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- value of BG color is as expected --";
      else:
        flag =1;
        tdkTestObj.setResultStatus("FAILURE");
        print "--  value of Bg color is not as expected --";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the BG color attribute" ;

    #calling closed caption API "CC_SetGetAttribute" to set the attribute (Default_FGColor) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "color";
    print "Categories value set to: %s" %categories
    attrib_type = 1; # To set Font color
    print "Attrib type value set to: %s" %attrib_type
    color_type3 = 1001; # default color type
    print "Color type value set to: %s" %color_type3
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
    Default_Fg_color = "%s" %color_type3;
    print "Expected default font color is:  %s" %iterator1[color_type1];

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "get font color %s" %cc_Get_Attribute_details;
      retattribute=cc_Get_Attribute_details.upper();
      print "returned attribute =%s" %retattribute;
      if iterator1[color_type1] in retattribute:
        flag = 0;
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- default value of font color is as expected --";
      else:
        flag =1;
        tdkTestObj.setResultStatus("FAILURE");
        print "-- default value of font color is not as expected --";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Did not return the default  font color attribute" ;

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
