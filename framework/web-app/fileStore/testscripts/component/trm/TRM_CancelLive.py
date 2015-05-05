'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1494</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CancelLive</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>637</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_CancelLive</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests cancel ongoing live viewing.
Test Case ID: CT_TRM_10
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>As per XONE-15184, CancelLive is an internal message between TRM and QAMSrc module. It is sent from TRM to QAMSrc only and does not modify the state of the tuners.</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CancelLive');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Reserve tuner for live
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');

    duration = 10000
    startTime = 0
    locator = tdkTestObj.getStreamDetails('02').getOCAPID()
    deviceNo = 1

    print "Live tune DeviceNo:%d Locator:%s duration:%d startTime:%d"%(deviceNo,locator,duration,startTime)

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);

    expectedRes = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[LIVE TUNE RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[LIVE TUNE DETAILS] : %s" %details;

    if "SUCCESS" in result.upper():
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    time.sleep(2)

    #Cancel live
    tdkTestObj = obj.createTestStep('TRM_CancelLive');

    print "Cancel live for locator:%s"%(locator)

    tdkTestObj.addParameter("locator",locator);

    expectedRes = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[TEST EXECUTION DETAILS] : %s" %details;

    if "SUCCESS" in result.upper():
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    # Get all Tuner states
    print "Get all Tuner states"
    tdkTestObj = obj.createTestStep('TRM_GetAllTunerStates');

    expectedRes = "SUCCESS"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[TEST EXECUTION DETAILS] : %s" %details;

    #Set the result status of execution
    if expectedRes in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");
    # Get all Tuner states End

    #unloading trm module
    obj.unloadModule("trm");
else:
    print "Failed to load trm module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
