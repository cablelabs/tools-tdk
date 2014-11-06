'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1729</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_26</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>620</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForLive</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests if tuner enters hybrid mode when recording tuner reservation on a channel is started followed by live reservation request.
Test Case ID: CT_TRM_26
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_26');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    expectedRes = "SUCCESS"
    deviceNo = 0
    duration = 10000
    startTime = 0

    # Start recording channel7
    print "Start recording on channel 7"
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForRecord');

    hot = 0
    recordingId = "RecordIdCh07"
    locator = tdkTestObj.getStreamDetails('07').getOCAPID()
    print "DeviceNo:%d Locator:%s hot=%d recordingId:%s duration:%d startTime:%d"%(deviceNo,locator,hot,recordingId,duration,startTime)

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);
    tdkTestObj.addParameter("recordingId",recordingId);
    tdkTestObj.addParameter("hot",hot);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[RECORDING RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[RECORDING DETAILS] : %s" %details;

    #Set the result status of execution
    if expectedRes in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");
    # End Start recording channel 7

    # Start live tuning channel 7
    print "Start tuning to channel 7"
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');

    print "DeviceNo:%d Locator:%s duration:%d startTime:%d"%(deviceNo,locator,duration,startTime)

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedRes);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[LIVE TUNE RESULT] : %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[LIVE TUNE DETAILS] : %s" %details;

    #Set the result status of execution
    if expectedRes in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");
    # End of Start live tuning channel 7

    # Get all Tuner states
    print "Get all Tuner states"
    tdkTestObj = obj.createTestStep('TRM_GetAllTunerStates');

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