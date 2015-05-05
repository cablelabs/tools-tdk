'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>XUPNP_CheckXDiscOutputFile</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>XUPNP_CheckXDiscOutputFile</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that xdiscovery process creates output.json file successfully.
TestcaseID: CT_XUPNP_01</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

xUpnpObj = tdklib.TDKScriptingLibrary("xupnp","2.0");
xUpnpObj.configureTestCase(ip,port,'XUPNP_CheckXDiscOutputFile');
#Get the result of connection with test component and STB
xupnpLoadStatus = xUpnpObj.getLoadModuleResult();
print "XUPNP module loading status : %s" %xupnpLoadStatus;
#Set the module loading status
xUpnpObj.setLoadModuleStatus(xupnpLoadStatus);

if "SUCCESS" in xupnpLoadStatus.upper():
        tdkTestObj = xUpnpObj.createTestStep('XUPNP_CheckXDiscOutputFile');
        expectedresult="SUCCESS";
        #Configuring the test object for starting test execution
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(actualresult,details);
        #Check for SUCCESS return value of XUPNP_CheckXDiscOutputFile
        if "SUCCESS" in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");
        #Unload xupnp module
        xUpnpObj.unloadModule("xupnp");
