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
  <name>Recorder_RMF_Orphaned_Recording_Notification_Inline_427</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Once the full sync has been successfully sent, then STB can stop tracking the orphaned recordings.</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_427</test_case_id>
    <test_objective>Once the full sync has been successfully sent Recorder can stop tracking the orphaned recordings using inline</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of stt_received and stage4 in /tmp path of device.
4. In rmfconfig.ini file the parameters FEATURE.LONGPOLL.URL,FEATURE.RWS.GET.URL and FEATURE.RWS.POST.URL should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1.TM loads RecorderAgent via the test agent.
2.Schedule a hot recording of 1 minute duration using  inline
3.Wait for the recording to complete and delete the meta data (Including backup of Blobs and XML)
4.Reboot the box and wait for the full sync to happen
5.Check the status of recording, it should be ERASED and error should  set as ORPHANED
6.Schedule an another recording and complete it then reboot the box
7.Wait for the full sync to happen and make sure that there is no details about the orphaned recording which is notified earlier
8.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Recording details should be available as expected</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_DeleteRecordingMetaData</test_stub_interface>
    <test_script>Recorder_RMF_Orphaned_Recording_Notification_Inline_427</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import recorderlib
from sys import exit
from random import randint
from time import sleep

#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_Orphaned_Recording_Notification_Inline_427');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);
	#print "Sleeping to wait for the recoder to be up"

	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10,500));
        recordingID = str(randint(10000,500000));
	duration = "60000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";
	genIdInput = recordingID;

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

        print "Update Schedule Details: %s"%actResponse;
        print "Wait for the recordig to complete"
        sleep(70);
          
        print "Deleting Blobs including backup"
        tdkTestObj1 = recObj.createTestStep('Recorder_ExecuteCmd');
        expectedResult="SUCCESS";
        tdkTestObj1.addParameter("command","find /tmp/mnt/diska3/persistent/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        tdkTestObj1.addParameter("command","find /mnt/nvram1/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");


        tdkTestObj1.addParameter("command","find /opt/persistent/dvr/recdbser/ -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        tdkTestObj1.addParameter("command","find /tmp/mnt/diska3/dvr_persistent/dvr/recdbser -type f | xargs grep -rls " +recordingID+ "| xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        print "Deleting XML's including backup"
        tdkTestObj1 = recObj.createTestStep('Recorder_ExecuteCmd');
        expectedResult="SUCCESS";
        tdkTestObj1.addParameter("command","find /opt/data/OCAP_MSV/0/0/DEFAULT_RECORDING_VOLUME/dvr -type f -name \"*.xml*\" -mmin -3 | xargs rm -rf");
        #Execute the test case in STB
        tdkTestObj1.executeTestCase("SUCCESS");
        result = tdkTestObj1.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj1.setResultStatus("SUCCESS");
        else:
            tdkTestObj1.setResultStatus("FAILURE");

        sleep(10);

        #Reboot the box
        recObj.initiateReboot();
        print "Waiting for 5 min for recoder to be up"
	sleep(300);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
	print "Full sync response: %s" %actResponse;
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print "Recording details:" , recordingData
        if 'NOTFOUND' not in recordingData:
            key = 'status'
            status = recorderlib.getValueFromKeyInRecording(recordingData,key)
            key = 'error'
            error = recorderlib.getValueFromKeyInRecording(recordingData,key)
            if "ERASED" in status.upper() and "ORPHANED" in error.upper():
                tdkTestObj.setResultStatus("SUCCESS");
                print "Recording has status ERASED and error ORPHANED"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Recording has unexpected values"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Recording details are not available"

        #Execute updateSchedule
        requestID1= str(randint(10, 500));
        recordingID1 = str(randint(10000, 500000));
        duration = "30000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID1+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID1+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID1+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;
        
        print "Wait for the recordig to complete"
        sleep(40);

        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Reboot the box and check whether Orphaned recording details are still tracking in recorder"
        #Reboot the box
        recObj.initiateReboot();
        print "Waiting for 5 min for recoder to be up"
	sleep(300);
        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
	print "Full sync response: %s" %actResponse;
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
        print "Recording details:" , recordingData
        if 'NOTFOUND' in recordingData:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Orphaned recording details are available only in the very next full sync"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Orphaned recording details are available in next full sync also"
         
        recObj.unloadModule("Recorder");
else:
	print "Failed to load Recorder module";
    	#Set the module loading status
    	recObj.setLoadModuleStatus("FAILURE");