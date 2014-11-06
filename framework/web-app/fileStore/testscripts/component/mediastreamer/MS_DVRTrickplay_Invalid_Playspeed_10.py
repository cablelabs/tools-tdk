'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>813</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>MS_DVRTrickplay_Invalid_Playspeed_10</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>95</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MediaStreamer_DVR_Trickplay</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This script tests Requesting DVR Streaming url from Mediastreamer and playing it with invalid trickplay speeds.Test Case ID:CT_Mediastreamer_10.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test will get fail because of bug in Mediastreamer. As per RDKTT-10 test case skipped</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Mediastreamer_10');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        #Calling the MediaStreamer_DVR_Trickplay function
        tdkTestObj=obj.createTestStep('MediaStreamer_DVR_Trickplay');
        #Pass the invalid play_speed
        tdkTestObj.addParameter("PlaySpeed","6");
        tdkTestObj.addParameter("timePosition","8000");
        #Execute the test case in STB and pass the expected result
        expectedresult="FAILURE";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        #compare the actual result with expected result
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Mediastreamer can not streaming the video ";
                print "Failure secnario : %s" %details;

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Mediastreamer streaming the video Successfully";
                print "Failure secnario : %s" %details;
        #Unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");