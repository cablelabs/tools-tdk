'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>363</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CC_ResetTrickPlayStatus_24</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>191</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>CC_ResetTrickPlayStatus</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script sets trickplay status of the closed caption to ON / OFF.
Test Case ID :CT_ClosedCaption_24</synopsis>
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
obj.configureTestCase(ip,port,'CC_ResetTrickPlayStatus_24');

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
		  
    #calling closed caption API CC_SetGetDigitalChannel to set the attribute  of the closed caption
    tdkTestObj = obj.createTestStep('CC_ResetTrickPlayStatus');
    				
    #Execute the test case in STB
    cc_ResetTrickPlayStatus_expectedresult="SUCCESS"
				

    tdkTestObj.executeTestCase(cc_ResetTrickPlayStatus_expectedresult);
    cc_ResetTrickPlayStatus_actualresult = tdkTestObj.getResult();
    cc_ResetTrickPlayStatus_details=tdkTestObj.getResultDetails();
    print "cc_ResetTrickPlayStatus_actualresult :%s" % cc_ResetTrickPlayStatus_actualresult;
   
 #Check for SUCCESSreturn value of closed capiton set attribute
    if cc_ResetTrickPlayStatus_expectedresult in cc_ResetTrickPlayStatus_actualresult:
      print "SUCCESS : In resetting the value";
      tdkTestObj.setResultStatus("SUCCESS");
    else:
      tdkTestObj.setResultStatus("FAILURE");
      print "FAILURE: Setting trickplay status %s" %tdkTestObj.getValue("details");
    
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE: In Initializing closed caption with %s " %tdkTestObj.getValue("details");   
    print "Initialization result of closed caption : %s" %cc_Init_actualresult;
  #Unload the cc module
  obj.unloadModule("cc");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");				