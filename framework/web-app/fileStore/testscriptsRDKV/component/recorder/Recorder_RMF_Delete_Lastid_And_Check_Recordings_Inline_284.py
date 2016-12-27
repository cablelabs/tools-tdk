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
  <name>Recorder_RMF_Delete_Lastid_And_Check_Recordings_Inline_284</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Reboot the box after removing lastid.dat file from recdbser folder and reboot.All the recordings  should be available in box</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
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
    <test_case_id>CT_Recorder_DVR_Protocol_284</test_case_id>
    <test_objective>Reboot the box after removing lastid.dat file from recdbser folder and reboot.All the recordings  should be available in box using inline</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. TM loads RecorderAgent via the test agent.
2. TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3. Delete the lastid.dat file from /tmp/mnt/diska3/persistent/dvr/recdbser/
4.reboot the box
5.check whether all the recordings are still there in the box
6.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Check whether all the recordings are still there in the box</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Delete_Lastid_And_Check_Recordings_Inline_284</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Delete_Lastid_And_Check_Recordings_Inline_284');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper())

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        expectedResult="SUCCESS";
        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj1.executeTestCase(expectedResult);
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 1 min to get response from recorder"
        sleep(60);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recordings in the box before reboot " , actResponse;
        totalrec_before = recorderlib.getTotalNumberofRecordings(actResponse)
        print "Total number of recordings before reboot " ,totalrec_before
        
        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_ExecuteCmd');
        tdkTestObj.addParameter("command","rm /tmp/mnt/diska3/persistent/dvr/recdbser/lastid.dat");
        #Execute the test case in STB
        tdkTestObj.executeTestCase("SUCCESS");
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "lastid.dat file deleted succesfully"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "lastid.dat file NOT deleted"
        sleep(30);
       
        # Reboot the STB
        print "Rebooting the STB"
        recObj.initiateReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300);
        tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj1.executeTestCase(expectedResult);
        response = recorderlib.callServerHandler('clearStatus',ip);
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        print "Wait for 1 min to get response from recorder"
        sleep(60);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        print "Recordings in the box after reboot" , actResponse;
        totalrec_after = recorderlib.getTotalNumberofRecordings(actResponse)
        print "Total number of recordings after reboot " ,totalrec_after
        if totalrec_before <= totalrec_after:
            tdkTestObj1.setResultStatus("SUCCESS");
            print "No recordings got deleted"
        else:
          tdkTestObj1.setResultStatus("FAILURE");
          print "Recordings got deleted"

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module"
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
