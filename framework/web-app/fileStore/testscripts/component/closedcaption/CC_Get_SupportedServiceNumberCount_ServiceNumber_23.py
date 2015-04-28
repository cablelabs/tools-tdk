'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>351</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CC_Get_SupportedServiceNumberCount_ServiceNumber_23</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>178</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>CC_Get_SupportedServiceNumberCount</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script gets the supported service number count and the total service numbers
Test Case ID : CT_ClosedCaption_23</synopsis>
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
obj.configureTestCase(ip,port,'CC_Get_SupportedServiceNumberCount_ServiceNumber_23');

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
  
  #Check for SUCCESS/FAILURE return value of CC_Initialization
  if "SUCCESS" in loadmodulestatus.upper():
    print "SUCCESS: Application successfully initialized with Closed Caption";
		  
    #calling closed caption API CC_SetGetAnalogChannel to set the analog channel number of the closed caption
    tdkTestObj = obj.createTestStep('CC_Get_SupportedServiceNumberCount');
	
    #Execute the test case in STB
    cc_Get_SupportedServiceNumberCount_expectedresult="SUCCESS";
				
    tdkTestObj.executeTestCase(cc_Get_SupportedServiceNumberCount_expectedresult);
    cc_Get_SupportedServiceNumberCount_actualresult = tdkTestObj.getResult();
    details=tdkTestObj.getResultDetails();
    print "details :%s" %details;
	  
    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Get_SupportedServiceNumberCount_expectedresult in cc_Get_SupportedServiceNumberCount_actualresult:
      tdkTestObj.setResultStatus("SUCCESS");
      print "Total service number count :%s" %details;
      print "SUCCESS: Application successfully started with Closed Caption ";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: In starting Closed Caption %s" %details;
	  
   #calling closed caption API CC_SetGetAnalogChannel to set the analog channel number of the closed caption
    tdkTestObj = obj.createTestStep('CC_Get_SupportedServiceNumber');
	
    #Execute the test case in STB
    cc_Get_SupportedServiceNumber_expectedresult="SUCCESS"		
    tdkTestObj.executeTestCase(cc_Get_SupportedServiceNumber_expectedresult);
    cc_Get_SupportedServiceNumber_actualresult = tdkTestObj.getResult();
    details=tdkTestObj.getResultDetails();
	  
    #Check for SUCCESS/FAILURE return value of closed capiton set attribute
    if cc_Get_SupportedServiceNumber_expectedresult in cc_Get_SupportedServiceNumber_actualresult:
      tdkTestObj.setResultStatus("SUCCESS");
      print "Services : %s" %details;
      print "SUCCESS: In getting the supported service number";
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: In getting the supported service number %s" %details;

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