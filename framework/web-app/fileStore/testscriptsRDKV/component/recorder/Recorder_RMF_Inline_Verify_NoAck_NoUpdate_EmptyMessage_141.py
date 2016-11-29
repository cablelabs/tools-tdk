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
  <name>Recorder_RMF_Inline_Verify_NoAck_NoUpdate_EmptyMessage_141</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recoder_DVR_Protocol_141 - Recorder should do nothing upon receiving NoUpdate empty message	via inline</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Recoder_DVR_Protocol_141</test_case_id>
    <test_objective>Recorder should do nothing upon receiving NoUpdate empty message   via inline</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,""FEATURE.RWS.GET.URL"" and ""FEATURE.RWS.POST.URL"" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to 
  RecorderAgent to generate request url.
3.RecorderAgent/Python lib interface will frame the json message to Simulate a longpoll notification with an 
  inline "noUpdate" with no data and send to TDK Recorder Simulator server which 
  is present in TM.
4.STB (Recorder) will not send any acknowledgement for this message. (CP)
5.Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
8.RecorderAgent/Python lib interface will frame the json message to Simulate a legacy longpoll 
  notification (no inline payload, only RWS GET URL). </automation_approch>
    <except_output>Checkpoint : No Acknowlegment should be received</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Inline_Verify_NoAck_NoUpdate_EmptyMessage_141</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Inline_Verify_NoAck_NoUpdate_EmptyMessage_141');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
               print "Sleeping to wait for the recoder to be up"
	       sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Frame json message
        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        expResponse = "noUpdate";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "noUpdate message post success";
                print "Wait to get acknowledgement"
                sleep(30);
                #Check for acknowledgement from recorder
	        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
	        print "Retrieve Status Details: %s"%actResponse;
		if 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "No acknowledgment from recorder for noUpdate";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received acknowledgement from recorder for noUpdate";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "noUpdate message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
