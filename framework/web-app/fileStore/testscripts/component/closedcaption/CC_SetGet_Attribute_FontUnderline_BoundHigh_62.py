'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1277</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CC_SetGet_Attribute_FontUnderline_BoundHigh_62</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>194</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Set and get the  closed caption attribute of font underline- Higher boundary value.
Test case ID - CT_ClosedCaption_62</synopsis>
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
    <box_type>IPClient-3</box_type>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_FontUnderline_10');

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

#calling closed caption API "CC_SetGetAttribute" to set the attribute (FontUnderline) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "fontUnderline";
    print "Categories value set to: %s" %categories
    attrib_type = 128; # To set FontUnderline
    print "attrib_type value set to: %d" %attrib_type
    fontUnderline = 1; #"0x0000ff"; # Blue
    print "Font underline bound high value set to: %d" %fontUnderline
    cc_type = 0  #Digital / Analog
    print "cc_type value set to: %d" %cc_type
					
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", fontUnderline);
    tdkTestObj.addParameter("ccType", cc_type);
				
    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS"
				
    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    attrib_type = "%s" %fontUnderline;
    print "Set font underline %s" %fontUnderline;

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "Get font underline high bound%s" %cc_Get_Attribute_details;
      if attrib_type in cc_Get_Attribute_details:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- Get and set values of font underline high bound are same --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "-- Get and set values of font underline high bound are not same --";
        print "FAILURE:with %s" %tdkTestObj.getValue("details");

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: font underline high bound attribute is not set with %s" %tdkTestObj.getValue("details");

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