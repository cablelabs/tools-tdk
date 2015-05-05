'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>430</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_GetBufferedRanges_04</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_HNSrc_GetBufferedRanges</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>These Script tests the RDK Mediaframework HNSrc element to Get the range of buffer.
Test Case ID: CT_RMF_HNSrc_05.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>RDKTT-34</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;
import time
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_HNSrc_GetBufferedRanges_04');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaframework module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediaframework module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('RMF_HNSrc_GetBufferedRanges');
        streamDetails = tdkTestObj.getStreamDetails('01'); 
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "PLAY URL : %s" %url;
        tdkTestObj.addParameter("playuri",url);
        #Execute the test case in STB
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result of HNSrc Get buffer range : %s" %actualresult;
        #compare the actual result with expected result
        if expectedresult in actualresult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "HNSrc Get buffer range is Success";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failure secnario : %s" %details;
                print "Failed to Get buffer range of HNSrc";
                time.sleep(40);
        #unloading mediastreamer module
        obj.unloadModule("mediaframework");
else:
        print "Failed to load mediaframework module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
