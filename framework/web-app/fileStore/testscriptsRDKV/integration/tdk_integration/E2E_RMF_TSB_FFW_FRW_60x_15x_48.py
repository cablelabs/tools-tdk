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
  <id>1211</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_TSB_FFW_FRW_60x_15x_48</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check tsb live trickplay playback with 60x FFW speed followed by -15x FRW speed. Test case ID-E2E_RMF_TSB_48</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
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
obj.configureTestCase(ip,port,'E2E_Rmf_TSB_48');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_Rmf_TSB_48');
                #Get the result of connection with test component and STB
                loadmodulestatus =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "tdkintegration module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url = tdkintegration.E2E_getStreamingURL(obj, "TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
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
                PLAYURL = details;
                print "Json Response Parameter is success";
                #Primitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
                rate =    60.0;
                print "Speed rate value set : %f" %rate;
                tdkTestObj.addParameter("SpeedRate",rate);
                tdkTestObj.addParameter("VideostreamURL",PLAYURL);
                #Execute the test case in STB and pass the expected result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                print "Result of TSB Play : %s" %actualresult;
                #compare the actual result with expected result of Json response Parameter
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        details = tdkTestObj.getResultDetails();
                        print "E2E RMF TSB Playback Successful: [%s]"%details;
                        #Prmitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
                        #Stream details for tuning
                        streamDetails = tdkTestObj.getStreamDetails('01');
                        #Framing URL for Request
			url = tdkintegration.E2E_getStreamingURL(obj, "TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
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
                                PLAYURL = details;
                                print "Json Response Parameter is success";
                                #Primitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
                                rate =  -15.0;
                                print "Speed rate value set : %f" %rate;
                                tdkTestObj.addParameter("SpeedRate",rate);
                                tdkTestObj.addParameter("VideostreamURL",PLAYURL);
                                #Execute the test case in STB and pass the expected result
                                expectedresult="SUCCESS";
                                tdkTestObj.executeTestCase(expectedresult);
                                #Get the actual result of execution
                                actualresult = tdkTestObj.getResult();
                                print "Result of TSB Play : %s" %actualresult;
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        details = tdkTestObj.getResultDetails();
                                        print "E2E RMF TSB Playback of consecutive speeds: [%s]"%details;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        details =  tdkTestObj.getResultDetails();
                                        print "E2E RMF TSB Playback of consecutive speeds: [%s]"%details;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Json Response Parameter is Failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details =  tdkTestObj.getResultDetails();
                        print "E2E RMF TSB Playback Failed: [%s]"%details;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json Response Parameter is Failure";
                print "Json Response Parameter is Failure";
        
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
