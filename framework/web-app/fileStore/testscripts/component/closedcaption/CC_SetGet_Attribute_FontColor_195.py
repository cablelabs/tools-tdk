'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1497</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CC_SetGet_Attribute_FontColor_195</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>194</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>CC_SetGetAttribute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Set the CC font size attribute as large or small or standard with cc_type as analog value
Test case Id - CT_ClosedCaption_195</synopsis>
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
    <box_type>Terminal-RNG</box_type>
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
obj.configureTestCase(ip,port,'CC_SetGet_Attribute_FontSize_195');

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
		  
    #calling closed caption API "CC_SetGetAttribute" to get the attribute (Font Size) of the closed caption
    tdkTestObj = obj.createTestStep('CC_SetGetAttribute');
    categories = "size";
    print "Categories value set to: %s" %categories	
    attrib_type = 32;
    print "attrib_type value set to: %d" %attrib_type 
    font_size = 2; 
    print "font Size value set to: %d" %font_size 
    cc_type = 1  #Digital / Analog
    print "cc_type value set to: %d" %cc_type 
					
    #Configuring the test object for starting test execution
    tdkTestObj.addParameter("Categories", categories);
    tdkTestObj.addParameter("ccAttribute", attrib_type);
    tdkTestObj.addParameter("value", font_size);
    tdkTestObj.addParameter("ccType", cc_type);
    
    #Execute the test case in STB
    cc_Set_Attribute_expectedresult="SUCCESS";			
    tdkTestObj.executeTestCase(cc_Set_Attribute_expectedresult);
    cc_Set_Attribute_actualresult = tdkTestObj.getResult();
    cc_Get_Attribute_details = tdkTestObj.getResultDetails();
    print "cc_Set_Attribute_actualresult :%s" %cc_Set_Attribute_actualresult;
    print "Set font size %d" %font_size;

    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Set_Attribute_expectedresult in cc_Set_Attribute_actualresult:
      print "Get Font Size %s" %cc_Get_Attribute_details;
      if str(font_size) in cc_Get_Attribute_details:
        tdkTestObj.setResultStatus("SUCCESS");
        print "-- Get and set values of font size are same --";
      else:
        tdkTestObj.setResultStatus("FAILURE");
        print "-- Get and set values of font size are not same --";
        print "FAILURE: with %s " %tdkTestObj.getResultDetails(); 

    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE:font size attribute is not set with %s" %tdkTestObj.getValue("details");
	  

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