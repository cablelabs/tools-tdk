##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1018</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_25</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>536</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_Pause</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_25: To verify pause on a video which is playing.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
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

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_25');
expected_Result="SUCCESS"

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result; 
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_25');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
#Acquiring the instance of TDKScriptingLibrary for checking and verifying the DVR content.
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_Pause');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_Pause');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)
#The Pre-requisite success. Proceed to execute the test case.
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_25');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result;

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
		 
    if matchList:
		 
         print "Recording Details : " , matchList

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

         print "The E2E DVR Pause on the video which is playing : %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Pause on the video playing Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Pause on the video playing Failed: [%s]"%details;
         
         obj.unloadModule("tdkintegration");
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
