'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1378</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKLogger_Log_Trace6</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>591</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RDKLogger_Log_Msg</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To log a TRACE6 level message.
Test Case ID: CT_RDKLogger_19
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdklogger","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKLogger_Log_Trace6');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

print "rdklogger module loading status :%s" %result;

#Check for SUCCESS/FAILURE of rdklogger module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RDKLogger_Log_Msg');

    expectedRes = "SUCCESS"

    module = "TEST4"
    print "Requested module: %s"%module
    tdkTestObj.addParameter("module",module);
    level = "TRACE6"
    print "Requested level: %s"%level
    tdkTestObj.addParameter("level",level);
    msg = "Test Trace6 message"
    print "Requested message: %s"%msg
    tdkTestObj.addParameter("msg",msg);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
        print "rdklogger logging Successful";
    else:
         tdkTestObj.setResultStatus("FAILURE");
         print "rdklogger logging Failed: [%s]"%details;

    #unloading rdklogger module
    obj.unloadModule("rdklogger");
else:
    print "Failed to load rdklogger module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");