'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1055</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_Rmf_LinearTV_MPEG4_AC3_18</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests the playback of MPEG4 video with AC3 audio service in End-to-End scenario Test Case ID : E2E_LinearTV_18</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
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
import tdkintegration;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_Rmf_LinearTV_MPEG4_AC3_18');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "tdkintegration module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
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
                ValidURL = PLAYURL[-1];
                print "Json Response Parameter is success";
                tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

                tdkTestObj.addParameter("playUrl",ValidURL);

                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);

                #Get the result of execution
                actualresult = tdkTestObj.getResult();


                print "The E2E LinearTv Play : %s" %actualresult;

                #compare the actual result with expected result
                if expectedresult in actualresult:
                      #Set the result status of execution
                      tdkTestObj.setResultStatus("SUCCESS");
                      details =  tdkTestObj.getResultDetails();
                      print "E2E LinearTv Playback Successful: [%s]"%details;
                else:
                      tdkTestObj.setResultStatus("FAILURE");
                      details =  tdkTestObj.getResultDetails();
                      print "E2E LinearTv Playback Failed: [%s]"%details;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                
        time.sleep(40);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");