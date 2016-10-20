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
  <id>1074</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_LinearTV_MPEG2_AAC_19</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>529</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests the playback of MPEG2 video with AAC audio service in End-to-End scenario Test Case ID : E2E_LinearTV_19</synopsis>
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
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
obj.configureTestCase(ip,port,'E2E_LinearTV_MPEG2_AAC_19');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        #Calling LinearTV_URL Function to send Request url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_URL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('03');
        channeltype =streamDetails.getChannelType();
        #Framing URL for Request
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?recorderId="+streamDetails.getRecorderID()+"&video="+streamDetails.getVideoFormat()+"&audio=&"+streamDetails.getAudioFormat()+"live=ocap://"+streamDetails.getOCAPID();
        print "Request URL : %s" %url;
        #Passing Parameter as url
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
                #Adding Parameter as validURL
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
                        print "MPEG2/AAC streams Tuned and played successfully";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to Tune and  play MPEG2/AAC streams";

        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json response parameter is Failed";
        #Unloading tdkintegration module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load LinearTV module";
        obj.setLoadModuleStatus("FAILURE");
