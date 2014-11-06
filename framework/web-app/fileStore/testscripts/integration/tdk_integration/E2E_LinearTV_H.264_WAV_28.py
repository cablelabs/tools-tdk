'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1083</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_LinearTV_H.264_WAV_28</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>529</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests the playback of H.264 video with WAV audio service in End-to-End scenario Test Case ID : E2E_LinearTV_28</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","1.2");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_LinearTV_H.264_WAV_28');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "TDKIntegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        #Calling LinearTV_URL Function to send Request url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('12');
        channeltype =streamDetails.getChannelType();
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?recorderId="+streamDetails.getRecorderID()+"&video="+streamDetails.getVideoFormat()+"&audio=&"+streamDetails.getAudioFormat()+"live=ocap://"+streamDetails.getOCAPID();
        print "Request URL : %s" %url;
        tdkTestObj.addParameter("Validurl",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();

        print "Result of Json Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                #Remove unwanted part from URL
                PLAYURL = details.split("[RESULTDETAILS]");
                print "PLAY URL = "+PLAYURL[-1];
                print "Json Response Parameter is success";
                #Calling LinearTV_Play_URL Function to play the stream
                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_Play_URL');
                tdkTestObj.addParameter("videoStreamURL",PLAYURL[-1]);
                #Execute the test case in STB and pass the expected result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                print "Result of Player : %s" %actualresult;
                #compare the actual result with expected result of playing video
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "H.264/WAV streams Tuned and played successfully";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to Tune and  play H.264/WAV streams";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json response parameter is Failed";
        #Unloading LinearTV module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load TDKIntegration module";
        obj.setLoadModuleStatus("FAILURE");