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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>MediaUtils_Start_AudioCapture_NullFifosize</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MediaUtils_AudioCaptureStart</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This is a negative test to check if audio capture happens when fifosize and threshold = 0</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
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
  <test_cases>
    <test_case_id>CT_MediaUtils_10</test_case_id>
    <test_objective>This is a negative test to see if audio capturing occurs when fifo size is NULL</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Xg1V3</test_setup>
    <pre_requisite>1. audiocapturemgr.service should not be up and running
2. Audio should be playing</pre_requisite>
    <api_or_interface_used>MediaUtils_ExecuteCmd,
MediaUtils_AudioCapture_Open,
MediaUtils_AudioCaptureStart
MediaUtils_AudioCaptureStop
MediaUtils_AudioCapture_Close</api_or_interface_used>
    <input_parameters>MediaUtils_ExecuteCmd - input command
MediaUtils_AudioCaptureStart - string "VALID", "NOTREADY", "NULL"
MediaUtils_AudioCaptureStop - string "VALID"
MediaUtils_AudioCapture_Close - string "VALID"</input_parameters>
    <automation_approch>1. TM loads the MediaUtils_Agent via the test agent.
2. MediaUtils_Agent should kill the audiocapturemgr.service successfully.
3.Call the API to open audio capture
4.Call the API to start audio capture
5. Sleep for sometime
6.MediaUtils_Agent will return SUCCESS or FAILURE based on the result of above step
7.Call the API to stop audio capture
8.Call the API to close audio capture</automation_approch>
    <except_output>Checkpoint 1: MediaUtils_ExecuteCmd should be success and audio playing should start
Checkpoint 2:MediaUtils_AudioCapture_Open should be success
Checkpoint 3:MediaUtils_AudioCapture_Start should be a failure
Checkpoint 4:MediaUtils_AudioCapture_Stop should be success
Checkpoint 5:MediaUtils_AudioCapture_Close should close successfully</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediautilsstub.so.0.0.0</test_stub_interface>
    <test_script>MediaUtils_Start_AudioCapture_NullFifosize</test_script>
    <skipped>No</skipped>
    <release_version>M52</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script ^M
import tdklib;
import time;

#Test component to be tested^M^M
obj = tdklib.TDKScriptingLibrary("mediautils","2.0");

#IP and Port of box, No need to change,^M^M
#This will be replaced with correspoing Box Ip and port while executing script^M^M
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'MediaUtils_Start_AudioCapture_NullFifosize');

#Get the result of connection with test component and STB^M
loadStatus =obj.getLoadModuleResult();
print "[MEDIAUTILS LOAD STATUS]  :  %s" %loadStatus;
obj.setLoadModuleStatus(loadStatus.upper());

if "SUCCESS" in loadStatus.upper():
        tdkTestObj = obj.createTestStep('MediaUtils_ExecuteCmd');
        tdkTestObj.addParameter("command","/opt/tdkplayer.sh > /dev/null 2>&1 &" );
        expectedresult = "SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "MediaUtils_ExecuteCmd call is Successful";
                tdkTestObj = obj.createTestStep('MediaUtils_AudioCapture_Open');
                expectedresult="SUCCESS"
                #Execute the test case in STB^M^M
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "MediaUtils_AudioCapture_Open call : SUCCESS";
                        tdkTestObj = obj.createTestStep('MediaUtils_AudioCaptureStart');
                        tdkTestObj.addParameter("paramBufferReady","READY");
			tdkTestObj.addParameter("paramFifosize","NULL");
                        tdkTestObj.addParameter("paramHandle","VALID");
                        expectedresult="FAILURE"
                        tdkTestObj.executeTestCase(expectedresult);

                        time.sleep(120);

                        actualresult = tdkTestObj.getResult();
                        print "EXPECTED RESULT : FAILURE";
                        print "ACTUAL RESULT : ", actualresult;
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "MediaUtils_AudioCaptureStart call NOT SUCCESSFUL when Fifosize is zero";

                        else:
                                print "MediaUtils_AudioCaptureStart call is SUCCESSFUL when Fifosize is zero";
                                tdkTestObj.setResultStatus("FAILURE");
                                tdkTestObj = obj.createTestStep('MediaUtils_AudioCaptureStop');
                                expectedresult="SUCCESS"
                                tdkTestObj.addParameter("paramHandle","VALID");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "MediaUtils_AudioCaptureStop call : SUCCESS";
                                else:
                                        print "MediaUtils_AudioCaptureStop call : FAILURE";
                                        tdkTestObj.setResultStatus("FAILURE");

                        tdkTestObj = obj.createTestStep('MediaUtils_AudioCapture_Close');
                        expectedresult="SUCCESS"
                        tdkTestObj.addParameter("paramHandle","VALID");
                        #Execute the test case in STB^M^M
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "MediaUtils_AudioCapture_Close : SUCCESS";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "MediaUtils_AudioCapture_Close : FAILURE";

                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "MediaUtils_AudioCapture_Open call : FAILURE "
        else:
                print "ExecuteCmd call is NOT successful";
                tdkTestObj.setResultStatus("FAILURE");

        #Unloading mediautils module^M
        obj.unloadModule("mediautils");

else:
        print "Failed to load mediautils module\n";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");

