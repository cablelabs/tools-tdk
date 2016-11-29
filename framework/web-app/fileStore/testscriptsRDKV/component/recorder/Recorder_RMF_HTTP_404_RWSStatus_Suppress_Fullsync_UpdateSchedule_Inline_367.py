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
  <name>Recorder_RMF_HTTP_404_RWSStatus_Suppress_Fullsync_UpdateSchedule_Inline_367</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Recorder should send the full sync details for an updateSchedule message if the last full sync was suppressed with server connection issue</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_367</test_case_id>
    <test_objective>Recorder should send the full sync details for an updateSchedule message if the last full sync was suppressed with server connection issue using inline</test_objective>
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
3.Schedule a hot recording using inline and wait for the recording to complete
4. Configure RWS Status server with HTTP 404 error and Reboot the box
5. Wait for full sync to fail and check RDK-10028 error code is getting.
6. Schedule a hot recording with bad ocap using inline and wait for the connection fall back in RWS status server then check RDK-10028 error code. 
7.Wait for 10 minutes
8.Clear the RWS Status server HTTP 404 error and wait for RWS Status server connection re-establishment
9.Send an updateSchedule using inline message and check whether recorder responds to this updateSchedule message with full sync details
10.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Check the full sync is happening or not</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_clearOcapri_log
3.TestMgr_Recorder_checkOcapri_log</test_stub_interface>
    <test_script>Recorder_RMF_HTTP_404_RWSStatus_Suppress_Fullsync_UpdateSchedule_Inline_367</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_HTTP_404_RWSStatus_Suppress_Fullsync_UpdateSchedule_Inline_367');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_HTTP_404_RWSStatus_Suppress_Fullsync_UpdateSchedule_Inline_367');
MFLoadStatus = obj.getLoadModuleResult();
print "MF module loading status : %s" %MFLoadStatus

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       print "Sleeping to wait for the recoder to be up"
	       sleep(300);

        jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
        sleep(10);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        
        tm_ip = recorderlib.get_ip_address('eth0')

        #To change the url in rmfconfig.ini
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        Keyword="FEATURE.SECURE_RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="https://"+tm_ip+":8443/DVRSimulator/recorder/secureStatus";
        print "Value" , Value
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details1 = rmfConfObj.getResultDetails();
        print result,","," ",details1
        if "FAILURE" in result:
                print "Failed to change the Secure RWS status Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the Secure RWS Status Url"
        rmfConfObj.setResultStatus("SUCCESS");

        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://"+tm_ip+":8080/DVRSimulator/recorder/status";
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details2 = rmfConfObj.getResultDetails();
        print result,","," ",details2
        if "FAILURE" in result:
                print "Failed to change the RWS status Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the RWS Status Url"
        rmfConfObj.setResultStatus("SUCCESS");
       
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
        
        #Frame json message to schedule a recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Waiting for the recording to complete"
        sleep(70) 

        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSStatus',ip,'404');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSSecureStatus',ip,'404');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSStatus',ip);
        if "true" in actResponse:
            #To clear the ocapri log
            tdkTestObj1 = recObj.createTestStep('Recorder_clearOcapri_log');
            tdkTestObj1.executeTestCase(expectedResult);
            result = tdkTestObj1.getResult();
            if "SUCCESS" in result:
                tdkTestObj1.setResultStatus("SUCCESS");
                print "Cleared the ocapri log ";
            else:
                tdkTestObj1.setResultStatus("FAILURE");
                print "Ocapri log is not cleared ";

            #unloading Recorder module
            recObj.unloadModule("Recorder");
            sleep(10);
            #Reboot the STB
            obj.initiateReboot();
            sleep(240);

            #Test component to be tested
            recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
            recObj.configureTestCase(ip,port,'Recorder_RMF_HTTP_404_RWSStatus_Suppress_Fullsync_UpdateSchedule_Inline_367');
            #Get the result of connection with test component and STB
            recLoadStatus = recObj.getLoadModuleResult();
            print "Recorder module loading status : %s" %recLoadStatus;
            recObj.setLoadModuleStatus(recLoadStatus);

            tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
            tdkTestObj.executeTestCase(expectedResult);
         
            print "Checking ocapri_log for server connection error codes"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "RDK-10028"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();

            loop=0
            while (('SUCCESS' not in result) and (loop < 5)):
                sleep(300);
                tdkTestObj2.executeTestCase(expectedResult);
                result = tdkTestObj2.getResult();
                details = tdkTestObj2.getResultDetails();
                loop = loop+1;
            print result,",Details of log ",details

            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Error Log RDK-10028 for RWS Status server connection lost is found ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Error Log RDK-10028 for RWS Status server connection lost is NOT found ";

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Error NOT enabled for RWS Status";

        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;

        #Execute updateSchedule to fallback again and to get error RDK-10028
        requestID = str(randint(10, 500));
        recordingID1 = str(randint(10000, 500000));
        duration = "600000";
        startTime = "0";
        ocapId = "0xbad1"
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID1+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID1+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;
        #Wait for getting the error code again
        print "Waiting for 5 minutes getting the error code RDK-10028 again"
        sleep(300) 

        actResponse = recorderlib.callServerHandlerWithType('clearError','RWSStatus',ip);
        actResponse = recorderlib.callServerHandlerWithType('clearError','RWSSecureStatus',ip);
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSStatus',ip);
        #Waiting for connection reset
        if "false" in actResponse:
            print "Waiting for RWS Status server connection re-establishment"
            sleep(60)

        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID2 = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID2+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID2+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;
        sleep(60)
        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
        print "RESPONSE" , actResponse
        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID);
        recordingData1 = recorderlib.getRecordingFromRecId(actResponse,recordingID1);
        print recordingData
        print recordingData1

        if 'NOTFOUND' not in (recordingData or recordingData1):
            print "Successfully retrieved the recording details from recorder";
            statusKey = 'status'
            statusValue = recorderlib.getValueFromKeyInRecording(recordingData,statusKey)
            statusValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,statusKey)
            if "COMPLETE" in statusValue.upper() and "FAILED" in statusValue1.upper():
                print "Both recordings have expected status like COMPLETE and FAILED"
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Recordings not have the expected status like COMPLETE and FAILED"
        else:
            print "NOT retrieved the recording list from recorder";
            tdkTestObj.setResultStatus("FAILURE");
        
        #Rever the modified URL's 
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.SECURE_RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        rmfConfObj.addParameter("Value",details1);
        expectedResult="SUCCESS";
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details = rmfConfObj.getResultDetails();
        print result,","," ",details
        if "FAILURE" in result:
            print "Failed to revert the Secure RWS status Url"
            rmfConfObj.setResultStatus("FAILURE");
            recObj.unloadModule("Recorder");
            exit();
        print "Reverted the Secure RWS status Url"
        rmfConfObj.setResultStatus("SUCCESS");

        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        rmfConfObj.addParameter("Value",details2);
        expectedResult="SUCCESS";
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details = rmfConfObj.getResultDetails();
        print result,","," ",details
        if "FAILURE" in result:
            print "Failed to revert the RWS status Url"
            rmfConfObj.setResultStatus("FAILURE");
            recObj.unloadModule("Recorder");
            exit();
        print "Reverted the RWS status Url"
        rmfConfObj.setResultStatus("SUCCESS");
                 
        recObj.initiateReboot();
        obj.resetConnectionAfterReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300);
        #unloading Recorder module
        recObj.unloadModule("Recorder");
        obj.unloadModule("mediaframework");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
