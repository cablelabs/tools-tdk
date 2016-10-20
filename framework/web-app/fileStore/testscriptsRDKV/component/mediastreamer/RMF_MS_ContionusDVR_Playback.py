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
  <id>913</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MS_ContionusDVR_Playback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>493</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MS_RMFStreamer_Player</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script test the Dvr playback via streaming Interface by continuous channel change every 10 seconds. Test Case Id: CT_RMFStreamer_19</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RMF_MS_ContionusDVRPlayback_28');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "RMFStreamer module  %s" %result;
if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "RmfStreamer load successful";
         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
         #---------Start-----------------

	 duration = 4
	 matchList = []
	 matchList = tdkTestObj.getRecordingDetails(duration);
         obj.resetConnectionAfterReboot()
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");
         time.sleep(2) 
         
         if matchList:
		 
            print "Recording Details : " , matchList

            #fetch recording id from list matchList.
            recordID = matchList[1]
         else:
             print "No Matching recordings list found"
         i = 0;
         for i in range(0,2):
                print "****************%d" %i;
                url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1];
                print "The Play DVR Url Requested: %s"%url
                tdkTestObj.addParameter("VideostreamURL",url);
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                print "The DVR to play in normal speed : %s" %actualresult;
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        details =  tdkTestObj.getResultDetails();
                        print "DVR Playback in normal speed:[%s]"%details;
                        time.sleep(2);
                        #Prmitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
                        if matchList:
		 
                             print "Recording Details : " , matchList

                             #fetch recording id from list matchList.
                             recordID = matchList[1]
                        else:
                             print "No Matching recordings list found"
                        url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1];
                        print "The Play DVR Url Requested: %s"%url
                        tdkTestObj.addParameter("VideostreamURL",url);
                        playtime = 10;
                        tdkTestObj.addParameter("play_time",playtime);
                        #Execute the test case in STB
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        print "The DVR to play in normal speed  : %s" %actualresult;
                        #compare the actual result with expected result
                        if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                details =  tdkTestObj.getResultDetails();
                                print "DVR Playback in normal speed :[%s]" %details;

                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                details =  tdkTestObj.getResultDetails();
                                print "DVR Play in normal speed Failed: [%s]" %details;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details =  tdkTestObj.getResultDetails();
                        print "DVR Play in normal speed Failed:[%s]" %details;

         obj.unloadModule("mediastreamer");
else:
         print "Failed to RmfStreamer module";
         obj.setLoadModuleStatus("FAILURE");
