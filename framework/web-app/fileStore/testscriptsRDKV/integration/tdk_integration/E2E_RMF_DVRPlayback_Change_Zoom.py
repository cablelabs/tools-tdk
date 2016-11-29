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
  <id/>
  <version>22</version>
  <name>E2E_RMF_DVRPlayback_Change_Zoom</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test tries to change the Zoom during DVR playback</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_30</test_case_id>
    <test_objective>Try to change Zoom during DVR playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads TDKIntegration_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds
5. TM loads the DS_Agent via the test agent
6. The Ds_Agent changes the Zoom settings
7. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's</except_output>
    <priority>High</priority>
    <test_stub_interface>DS_Stub
TDK_Integration_Stub</test_stub_interface>
    <test_script>E2E_RMF_DVRPlayback_Change_Zoom</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkintegration import dvr_playback

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
tdkIntObj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
print "[TDKINTEGRATION LIB LOAD STATUS]  :  %s" %tdkIntLoadStatus ;
loadmoduledetails = tdkIntObj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in tdkIntLoadStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdkIntObj.initiateReboot();
                #Reload Test component to be tested
                tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdkIntObj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
                #Get the result of connection with test component and STB
                tdkIntLoadStatus =tdkIntObj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %tdkIntLoadStatus;
if "SUCCESS" in tdkIntLoadStatus.upper():
    #Set the module loading status
    tdkIntObj.setLoadModuleStatus("SUCCESS");
    tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    global matchList 
    matchList = tdkTestObj.getRecordingDetails(duration);
    tdkIntObj.resetConnectionAfterReboot()
    tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #set the dvr play url 
    if matchList:
       print "Recording Details : " , matchList
       #fetch recording id from list matchList.
       recordID = matchList[1]
       recordID = recordID.strip()
                    
       #Calling DvrPlay_rec to play the recorded content
       result = dvr_playback(tdkTestObj,recordID );
       if "SUCCESS" in result.upper():
       
	 #devicesettings component to be tested
	 dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
	 dsObj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
	 dsLoadStatus = dsObj.getLoadModuleResult();
	 print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
	 if "SUCCESS" in dsLoadStatus.upper():
            dsObj.setLoadModuleStatus("SUCCESS");
            #calling Device Settings - initialize API
            tdkTestObj = dsObj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS :Application successfully initialized with Device Settings library";
                    #calling DS_SetDFC to get and set the zoom settings 
                    tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                    #zoom="Full";
                    zoom="Full";
                    print "Zoom value set to : %s" %zoom;
                    tdkTestObj.addParameter("zoom_setting",zoom);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    dfcdetails = tdkTestObj.getResultDetails();
		    print dfcdetails
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                            print "SUCCESS :Application successfully gets and sets the zoom settings for the video device";
                            tdkTestObj.setResultStatus("SUCCESS");
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE :Failed to get and set the zoom settings";

		    #Calling DvrPlay_rec to play the recorded content with full zoom
    		    tdkIntTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
                    result = dvr_playback(tdkIntTestObj,recordID );

                    print "Revert zoom to None"
                    zoom="None";
                    #calling DS_SetDFC to get and set the zoom settings
                    tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                    print "Zoom value set to %s" %zoom;
                    tdkTestObj.addParameter("zoom_setting",zoom);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    dfcdetails = tdkTestObj.getResultDetails();
                    print "Details: ",dfcdetails
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                         tdkTestObj.setResultStatus("SUCCESS");
                    else:
                         tdkTestObj.setResultStatus("FAILURE");

                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = dsObj.createTestStep('DS_ManagerDeInitialize');
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                    if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE: Deinitalize failed" ;
            else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Device Setting Initialize failed";
	    #Unload the deviceSettings module
	    dsObj.unloadModule("devicesettings");
         else:
            #Set the module loading status
            dsObj.setLoadModuleStatus("FAILURE");
       else:
            print "Failed to play the recorded content"
    tdkIntObj.unloadModule("tdkintegration");
else:
    print"Load module failed";
    #Set the module loading status
    tdkIntObj.setLoadModuleStatus("FAILURE");
