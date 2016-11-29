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
  <name>Recorder_RMF_Legacy_SchedRecording_LPServerConnInterrupt_68</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check that longpoll connection interruption during legacy scheduled future recording resumes by recorder requesting a full schedule once the connection is re-established</synopsis>
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
    <test_case_id>CT_Recoder_DVR_Protocol_68</test_case_id>
    <test_objective>Check that longpoll connection interruption during legacy scheduled future recording resumes by recorder requesting a full schedule once the connection is re-established</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to RecorderAgent to generate request url.
3.RecorderAgent / Python lib interface will frame the json message to schedule future recording using legacy mechanism and send to TDK Recorder Simulator server which is present in TM.
4.RecorderAgent / Python lib interface will down the Long poll server URL 
5.RecorderAgent / Python lib interface will bring up/activate the Long poll server URL 
6. After getting the list of recordings , check the Recording status.
6. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check all current and future recordings</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Legacy_SchedRecording_LPServerConnInterrupt_68</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from time import sleep
from random import randint

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Legacy_SchedRecording_LPServerConnInterrupt_68');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

        print "Rebooting box for setting configuration"
	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);

        print "Sleeping to wait for the recoder to be up"


        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

	response = recorderlib.callServerHandler('clearStatus',ip);

        #Legacy sched Recording updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        #2min duration
        duration = "120000";
        startTime = "60000";
        genIdInput = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "serverResponse : %s" %serverResponse;

        if "updateSchedule" in serverResponse:
                print "updateSchedule message post success";
                #Wait for recording start acknowlegment
                sleep(60);
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                print "Retrieve Status Details: ",recResponse;
                if "ack" in recResponse:
                        print "Simulator Server received the recorder acknowledgement";
                        print "Disable LPServer for longpoll connection interruption"
                        #Disable LPServer
                        recorderlib.callServerHandlerWithType('disableServer','LPServer',ip)
                        status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
                        print "Longpoll server status: ",status
                        if "FALSE" in status.upper():
                                print "Wait for more than 90sec"
                                sleep (100)
                                print "Enable longpoll server connection"
                                recorderlib.callServerHandlerWithType('enableServer','LPServer',ip)
                                status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
                                print "Longpoll server status: ",status
                                if "FALSE" in status.upper():
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Failed to enable LP Server"
                                else:
                                        print "Enabled LP Server"
                                        print "Wait for recording to be completed"
                                        sleep (100)
                                        print "Sending getRecordings to get the recording list"
                                        recorderlib.callServerHandler('clearStatus',ip)
                                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                        print "Wait for 60 seconds to get response from recorder"
                                        sleep(60);
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                        print "Recording List: %s" %actResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
                                        print recordingData
                                        if 'NOTFOUND' == recordingData:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "Recording not found in list";
                                        else:
                                            key = 'status'
                                            value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                            print "key: ",key," value: ",value
                                            if "COMPLETE" in value.upper():
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "Scheduled recording completed successfully";
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Scheduled recording did not complete successfully";
                        else:
                                print "Failed to disable LP Server"
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to receive acknowledgement from recorder";
        else:
                print "updateSchedule message post failure";
                tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");

