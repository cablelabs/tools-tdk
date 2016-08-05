#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>999</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>23</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_04</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>556</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_LinearTv_Dvr_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_04: To verify the video playback when Fast Forward is done at 32x speed from the starting point of the video.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>25</execution_time>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_04');
expected_Result="SUCCESS"

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "tdkintegration module loading status :%s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_04');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
#Acquiring the instance of TDKScriptingLibrary for checking and verifying the DVR content.
if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------

         duration = 10
         matchList = []
         matchList = tdkTestObj.getRecordingDetails(duration);
         obj.resetConnectionAfterReboot()
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         time.sleep(10)
#The Pre-requisite success. Proceed to execute the test case.
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_04');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result;

if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "Tdkintegration module load successful";

		 
         if matchList:
		 
               print "Recording Details : " , matchList

               #fetch recording id from list matchList.
               recordID = matchList[1]

               url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );

               if url == "NULL":
                   print "Failed to generate the Streaming URL";
                   tdkTestObj.setResultStatus("FAILURE");
               url = url + "&play_speed=32.00&time_pos=0.00"

               print "The Play DVR Url Requested: %s"%url
               tdkTestObj.addParameter("playUrl",url);

               #Execute the test case in STB
               expectedresult="SUCCESS";
               tdkTestObj.executeTestCase(expectedresult);

               #Get the result of execution
               actualresult = tdkTestObj.getResult();
               details =  tdkTestObj.getResultDetails();

               print "The E2E DVR playback when Fast Forward is done at 32x Speed from starting point of the video: %s" %actualresult;

               #compare the actual result with expected result
               if expectedresult in actualresult:
                      #Set the result status of execution
                      tdkTestObj.setResultStatus("SUCCESS");
                      print "E2E DVR Playback Successful: [%s]"%details;
               else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "E2E DVR Playback Failed: [%s]"%details;
               
               obj.unloadModule("tdkintegration");
         else:
               print "No Matching recordings list found"
					 
               time.sleep(10);
               obj.unloadModule("tdkintegration");

else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");