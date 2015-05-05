'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>819</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>MS_Recording_Improper_Requesturl_04</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>111</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MediaStreamer_Recording_Request</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This script tests response of Mediastreamer for Requesting  recorded content with Improper url
Test Case ID:CT_Mediastreamer_04</synopsis>
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
    <box_type>Emulator-HYB</box_type>
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
obj.configureTestCase(ip,port,'CT_Mediastreamer_04');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        #Calling the MediaStreamer_Recording_Request function
        tdkTestObj = obj.createTestStep('MediaStreamer_Recording_Request');
        #Passing the parameter  
        tdkTestObj.addParameter("recordingId","");
        #Execute the test case in STB and pass the expected result
        expectedresult="1";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Recoded response of Json parameter : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Json Response Parameter is Failure,testing sucess";
                print "Recorded request description:General Error";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                
                print "Failure scenarios : %s" %details;
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");