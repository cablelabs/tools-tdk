'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1621</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MS_Incomplete_URL_Request</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>491</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MS_RMFStreamer_InterfaceTesting</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test is to check the response url for incomplete request URL
Test Case ID: CT_MediaStreamer_21</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMFMS_Without_StreamInit_23');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        #Calling the RMFStreamer_LiveTune_Request function
        tdkTestObj = obj.createTestStep('MS_RMFStreamer_InterfaceTesting');
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=oca"; 
        print "Request URL : %s" %url;
        tdkTestObj.addParameter("URL",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="FAILURE";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Live Tune Response of Json parameter : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print details;
                print "Json Response Parameter is Failed";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print details;
                print "Json response parameter is Success";
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");