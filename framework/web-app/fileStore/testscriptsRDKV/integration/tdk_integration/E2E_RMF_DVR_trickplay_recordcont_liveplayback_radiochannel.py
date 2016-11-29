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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1684</id>
  <version>15</version>
  <name>E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>LinearTV ? Try to select trick play when device is in Radio channel</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <remarks>Causing ABL mode In Pace Xi3 box</remarks>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_21</test_case_id>
    <test_objective>Recorder-Try to select trick play in recorded content from XG1 when live playback is in radio channel</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads LinearTV_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the LinearTV_agent for tune
3.LinearTV_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the HnSrc-&gt;Mpsink pipeline.
5. Perform Trick Play on the recorded content using HnSrc-&gt; Mpsink pipeline.
6.Depends on the result of above step agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from live playback</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;

from tdkintegration import getURL_PlayURL_Audio,dvr_playback;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
                                        
obj.configureTestCase(ip,port,'E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successfuls";   
   
    #Calling getURL_PlayURL with valid Stream ID
    result1 = getURL_PlayURL_Audio(obj,'R01');
    
    time.sleep(150);

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.initiateReboot();
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)
    if matchList:
         print "Recording Details : " , matchList
         #fetch recording id from list matchList.
         recordID = matchList[1]
         recordID = recordID.strip()
         #Calling getURL_PlayURL with valid Stream ID
         result2 = dvr_playback(tdkTestObj,recordID,play = 'trickplay');
         if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                       
               print "Execution Success"
               obj.unloadModule("tdkintegration");
         else:
               print "Execution is failure"
               obj.unloadModule("tdkintegration");
    else:
         print "No Matching recordings list found"
else:
    print "Failed to load tdkintegration module";
    obj.setLoadModuleStatus("FAILURE");
