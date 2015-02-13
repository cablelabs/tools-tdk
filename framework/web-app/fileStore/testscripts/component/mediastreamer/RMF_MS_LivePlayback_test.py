'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>920</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MS_LivePlayback_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>491</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MS_RMFStreamer_InterfaceTesting</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script test Live playback of HD/SD content  via streaming Interface. Test case ID:CT_RMFMediaStreamer_15</synopsis>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_MS_LivePlayback_Test_25');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus ;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediastreamer module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
        streamDetails = tdkTestObj.getStreamDetails('01');
        details = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
        print "Response URL : %s" %details;
        playtime = 10;
        tdkTestObj.addParameter("VideostreamURL",details);
        tdkTestObj.addParameter("play_time",playtime);
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        
        print "Live Tune Playback : %s" %actualresult;
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print " Live Playback is Success";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print "Live Playback is Failure [%s]"%details;
        
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
