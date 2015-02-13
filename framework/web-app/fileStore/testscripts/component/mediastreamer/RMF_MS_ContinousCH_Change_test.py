'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>912</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MS_ContinousCH_Change_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>491</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MS_RMFStreamer_InterfaceTesting</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script test the Live playback via streaming Interface by continuous channel change every 60 seconds. Test Case Id: CT_RMFStreamer_18</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>8</execution_time>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_MS_ContinousCH_Change_test_27');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Mediaastreamer module loading status :%s" %loadmodulestatus ;
#Check for SUCCESS/FAILURE of Mediastreamer module
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        print "Mediastreamer module loaded successfully";
        i = 0;
        for i in range(0,2):
                print "****************%d" %i;

                #Prmitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
                streamDetails = tdkTestObj.getStreamDetails('01');
                details_url = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
                print "Response URL : %s" %details_url;
                playtime = 10;
                tdkTestObj.addParameter("VideostreamURL",details_url);
                tdkTestObj.addParameter("play_time",playtime);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();

                print "Live Tune Playback : %s" %actualresult;
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Live Playback is Success";
                        time.sleep(10);
                        #Prmitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
                        streamDetails = tdkTestObj.getStreamDetails('01');
                        details_response = 'http://' + streamDetails.getGatewayIp() + ':8080/hnStreamStart?live=ocap://'+ streamDetails.getOCAPID();
                        playtime = 10;
                        tdkTestObj.addParameter("VideostreamURL",details_response);
                        tdkTestObj.addParameter("play_time",playtime);
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        print "Live Tune Playback : %s" %actualresult;
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Continous channel change Playback is Success";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                details3 = tdkTestObj.getResultDetails();
                                print "Continous channel change Playback is Failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print "Live Playback is Failure:%s"%details;
        #unloading mediastreamer module
        obj.unloadModule("mediastreamer");
else:
        print "Failed to load mediastreamer module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
