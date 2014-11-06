'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1693</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>CT_XUPNP_04</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>665</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TestMgr_XUPNPAgent_checkPBurl</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>XUPNP –to check the playback url generated is valid or not
TCID :CT_XUPNP_04</synopsis>
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
obj.configureTestCase(ip,port,'CT_XUPNP_04');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "XUPNP module loading status :  %s" %loadmodulestatus;

if "Success" in loadmodulestatus:
  print "XUPNP module loaded successfully";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");

  #calling XUPNP API "TestMgr_XUPNPAgent_checkPBurl"
  tdkTestObj = obj.createTestStep('TestMgr_XUPNPAgent_checkPBurl');
  expectedresult="SUCCESS";
  #Configuring the test object for starting test execution
  tdkTestObj.executeTestCase(expectedresult);
  actualresult = tdkTestObj.getResult();
  details=tdkTestObj.getResultDetails();
  print "XUPNPAgent_checkjson_actualresult  :%s" %actualresult; 

  #Check for SUCCESS return value of XUPNPAgent_checkPBurl
  if "SUCCESS" in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS");
    print "SUCCESS: XUPNPAgent_checkPBurl";
  else:
    tdkTestObj.setResultStatus("FAILURE");
    print "FAILURE:  XUPNPAgent_checkPBurl %s " %details;   

  #Unload the xupnp module
  obj.unloadModule("xupnp");

else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");