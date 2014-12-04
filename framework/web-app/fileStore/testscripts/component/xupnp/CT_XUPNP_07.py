'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1698</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CT_XUPNP_07</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>668</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TestMgr_XUPNPAgent_removeXmls</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>XUPNP –  Remove all the xml files refered by the xcal-dsevice and xdiscovery process and check the behavior. TCID :CT_XUPNP_07</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("xupnp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_XUPNP_07');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "XUPNP module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "XUPNP module loaded successfully";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");

  #calling XUPNP API "TestMgr_XUPNPAgent_removeXmls"
  tdkTestObj = obj.createTestStep('TestMgr_XUPNPAgent_removeXmls');
  expectedresult="SUCCESS";
  #Configuring the test object for starting test execution
  tdkTestObj.executeTestCase(expectedresult);
  actualresult = tdkTestObj.getResult();
  details=tdkTestObj.getResultDetails();
  print "XUPNPAgent_removeXmls_actualresult  :%s" %actualresult; 
  #Check for SUCCESS return value of XUPNPAgent_removeXmls
  if "SUCCESS" in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS");
    print "SUCCESS: XUPNPAgent_removeXmls";
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE:  XUPNPAgent_removeXmls %s " %details;   

  #Unload the xupnp module
  obj.unloadModule("xupnp");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
