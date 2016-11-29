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
  <version>1</version>
  <name>Recorder_RMF_GenerationId_Preserve_CurrentId_Inline_Payload_23</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis/>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_23</test_case_id>
    <test_objective>Recorder- To verify whether lack of new Generation ID in inline payload preserves current ID.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent/Python lib interface will frame the json message to Simulate a longpoll notification with an inline 
  "noUpdate" payload containing "generationId": "test6b" and send to TDK Recorder Simulator server which is present 
  in TM.
4.STB (recorder) will not send any acknowledgement(CP).
5.Simulate a longpoll notification with an inline "updateSchedule" payload that does not contain any 
  "generationId" though RecorderAgent/Python lib interface and TDK Recorder Simulator server. 
6.Simulate a legacy longpoll notification (no inline payload, only RWS GET URL) through ecorder_agent/Python lib interface and TDK Recorder Simulator server. 
7.STB (recorder) makes a GET request to RWS bearing HTTP header "X-Parker-Generation-ID: test6b". (CP).
8.Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.</automation_approch>
    <except_output>Checkpoint : Acknowledgement status from the DVRSimulator AND value of generationId from http header at steps 4 and 7.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_GenerationId_Preserve_CurrentId_Inline_Payload_23</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Preserve_CurrentId_Inline_Payload_23');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
	       print "Rebooting box for setting configuration"
               recObj.initiateReboot();
	       print "Waiting for the recoder to be up"
	       sleep(300);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Execute Inline noUpdate
	genIdInput = "test6b";
        jsonMsgNoUpdate = "{\"noUpdate\":{\"generationId\":\""+genIdInput+"\"}}";
        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);

        if 'noUpdate' in serverResponse:
                print "Inline noUpdate message post success";
		# Verify that Recorder does not make any POST request to RWS
		sleep(30)
		recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		print "Retrieve Status for inline noUpdate message: ",recResponse;

		response = recorderlib.callServerHandler('clearStatus',ip);
                #Execute Inline updateSchedule
                requestID = str(randint(10, 500));
                jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\"}}";
                serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

                if 'updateSchedule' in serverResponse:
                        print "Inline updateSchedule message post success";
                        genOut = recorderlib.readGenerationId(ip)
                        if genOut == genIdInput:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "GenerationId retrieved matches with expected (%s)"%(genIdInput);
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "GenerationId retrieved does not match with expected (%s)"%(genIdInput);
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Inline updateSchedule message post failed";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Inline noUpdate message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
