'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>998</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_03</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>556</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_LinearTv_Dvr_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_03: To verify the video playback when Fast Forward is done at 16x speed from the starting point of the video.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>12</execution_time>
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
import tdkintegration;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_03');
expected_Result="SUCCESS"

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %result;

#Acquiring the instance of TDKScriptingLibrary for checking and verifying the DVR content.
if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";

         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------
         matchList = []
         if expected_Result in result.upper():
                  #Get DVR pre req done.
                  matchList = obj.checkAndVerifyDvrRecording(3);
                  if len(matchList) == 0:
                           print "DVR required Recording Not Found!!! Status: FAILURE"
                           print "DVR Test case execution skipped!!!."
                           exit()
                  else:
                           print "DVR required Recording Found. Proceeding to excute Test Case."
                           print "Record Details: ",matchList
         else:
                  print "Loading Module Failed."
                  print "Exiting the script without running the TC"
                  exit();
        #--------End-----------------------

time.sleep(10)

#The Pre-requisite success. Proceed to execute the test case.
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_03');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result;

if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "tdkintegration module load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         #fetch recording id from list matchList.
         recordID = matchList[1]

         url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );
         if url == "NULL":
             print "Failed to generate the Streaming URL";
             tdkTestObj.setResultStatus("FAILURE");

         print "The Play DVR Url Requested: %s"%url
         tdkTestObj.addParameter("playUrl",url);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR playback when Fast Forward is done at 16x Speed from starting point of the video: %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Playback Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Playback Failed: [%s]"%details;
         time.sleep(40);
         obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
