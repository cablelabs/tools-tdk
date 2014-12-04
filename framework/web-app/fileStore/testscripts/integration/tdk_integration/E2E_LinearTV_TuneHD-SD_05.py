'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1070</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_LinearTV_TuneHD-SD_05</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>529</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests tuning of an HD service from another SD service in End-to-End scenario
Test Case ID : E2E_LinearTV_05</synopsis>
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
obj.configureTestCase(ip,port,'E2E_LinearTV_TuneHD-SD_05');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        print "tdkintegration module loaded successfully";
        obj.setLoadModuleStatus("SUCCESS");
        #Calling LinearTV_GetURL function to send request url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('02');
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?recorderId="+streamDetails.getRecorderID()+"live=ocap://"+streamDetails.getOCAPID();
        print "Request URL : %s" %url;
        tdkTestObj.addParameter("Validurl",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        #Remove unwanted part from URL
        PLAYURL = details.split("[RESULTDETAILS]");
        print "PLAY URL = "+PLAYURL[-1];
        print "Result of Json Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Pre condition-Json Response received successfully";
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
                        print "Pre condition-HD channel Tuned and played successfully";

                        #Calling LinearTV_GetURL function to send request url
                        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
                        streamDetails = tdkTestObj.getStreamDetails('01');
                        url2="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?recorderId="+streamDetails.getRecorderID()+"live=ocap://"+streamDetails.getOCAPID();
                        print "Request URL : %s" %url;
                        tdkTestObj.addParameter("Validurl",url2);
                        #Execute the test case in STB and pass the expected result
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the actual result of execution
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        #Remove unwanted part from URL
                        PLAYURL2 = url.split("[RESULTDETAILS]");
                        print "PLAY URL2 = "+PLAYURL2[-1];
                        print "Result of Json Response : %s" %actualresult;
                        #compare the actual result with expected result of Json response Parameter
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "HD-SD channel tune response received successfully";
                                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_Play_URL');
                                tdkTestObj.addParameter("videoStreamURL",PLAYURL2[-1]);
                                #Execute the test case in STB and pass the expected result
                                expectedresult="SUCCESS";
                                tdkTestObj.executeTestCase(expectedresult);
                                #Get the actual result of execution
                                actualresult = tdkTestObj.getResult();
                                print "Result of Player : %s" %actualresult;
                                #compare the actual result with expected result of playing video
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "HD-SD channel tuned and played successfully";

                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to tune and play HD-SD channel";

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to receive tune response HD-SD channel";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Pre condiition-Failed to Tune and Play the HD channel";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Pre condition-Json response parameter is Failed";
        #Unloading tdkintegration module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load tdkintegration module";
        obj.setLoadModuleStatus("FAILURE");
