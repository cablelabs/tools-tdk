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
  <name>Recorder_RMF_GenerationId_Reset_OnCorruption_LegacyFutureRec_171</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Generation ID is reset if corruption occurs on reboot</synopsis>
  <groups_id/>
  <execution_time>60</execution_time>
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
    <test_case_id>CT_Recoder_DVR_Protocol_171</test_case_id>
    <test_objective>Verify that generation ID is reset on reboot if corruption happens after scheduling legacy future recording</test_objective>
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
3.RecorderAgent / Python lib interface will frame the json message to schedule a future recording legacy inline mechanism with genid=test3b and send to TDK Recorder Simulator server which is present in TM.
4. Wait for 5sec, corrupt and again wait for 5sec.
5. Reboot and retrieve status
6. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the response from recorder and verify that genid=0</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequestToDeleteFile
2.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_GenerationId_Reset_OnCorruption_LegacyFutureRec_171</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Reset_OnCorruption_LegacyFutureRec_171');
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
        print "Clear Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "180000";
        startTime = "120000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        genIdIn = "test3b";

        #Frame json message for legacy future sched
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdIn+"\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Server response for legacy updateSchedule: ",serverResponse;

        if 'updateSchedule' in serverResponse:
                print "Legacy updateSchedule message post success";
                sleep(20)
                retry = 0;
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while ( ('[]' == recResponse) and (retry < 15) ):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: %s"%recResponse;

                if (('[]' == recResponse) or ('ERROR' == recResponse)):
                        print "Received Empty/Error status";
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                        sleep(5)
                        #Delete the properties file
                        propFile = '/opt/data/recorder/recorder.props'

                        #Primitive test case which associated to this script
                        testObj = recObj.createTestStep('Recorder_SendRequestToDeleteFile');
                        expectedResult="SUCCESS";
                        #Delete properties file
                        testObj.addParameter("filename",propFile);
                        #Execute the test case in STB
                        testObj.executeTestCase(expectedResult);
                        #Get the actual result and details of execution
                        result = testObj.getResult();
                        details = testObj.getResultDetails();
                        print result,",",propFile," ",details

                        if "FAILURE" in result:
                                print "Failed to corrupt recording properties"
                                testObj.setResultStatus("FAILURE");
                        else:
                                print "recorder properties corrupted"
                                testObj.setResultStatus("SUCCESS")
                                sleep(5)
                        recObj.initiateReboot();
                        print "Waiting for the recoder to be up"
                        sleep(300);
                        genIdOut = recorderlib.readGenerationId(ip)
                        print "GenerationId retrieved after reboot: ",genIdOut
                        if "0" == genIdOut:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "GenerationId is successfully reset to 0"
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "GenerationId failed to reset to 0"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Legacy updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
