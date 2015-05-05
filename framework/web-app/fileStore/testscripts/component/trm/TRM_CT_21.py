'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1631</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_21</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>613</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests recording multiple stations from same terminal.
Test Case ID: CT_TRM_21
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
    <box_type>Emulator-HYB</box_type>
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
obj.configureTestCase(ip,port,'TRM_CT_21');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForRecord');

    duration = 10000
    startTime = 0
    hot = 0

    for deviceNo in range(0,2):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        locator = tdkTestObj.getStreamDetails(streamId).getOCAPID()

        print "Record DeviceNo:%d Locator:%s hot=%d recordingId:%s duration:%d startTime:%d"%(deviceNo,locator,hot,recordingId,duration,startTime)

        tdkTestObj.addParameter("deviceNo",0);
        tdkTestObj.addParameter("duration",duration);
        tdkTestObj.addParameter("locator",locator);
        tdkTestObj.addParameter("startTime",startTime);
        tdkTestObj.addParameter("recordingId",recordingId);
        tdkTestObj.addParameter("hot",hot);

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
    # End of for loop

    #unloading trm module
    obj.unloadModule("trm");
else:
    print "Failed to load trm module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");