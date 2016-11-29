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
  <version>4</version>
  <name>Recorder_RMF_Check_HTTP_500_RWSServer_Bootup_306</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>RWS server should send HTTP 500 when the server is enabled with HTTP 500error and also during boot up after retry recorder should send error code RDK-10028</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_306</test_case_id>
    <test_objective>RWS server should send HTTP 500 when the server is enabled with HTTP 500 error and also during boot up after retry recorder should send error code RDK-10028</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface</api_or_interface_used>
    <input_parameters>Json Interface- source id, duration recording_id, start_time.</input_parameters>
    <automation_approch>1. TM loads RecorderAgent via the test agent.
2. Configure RWS server and RWS secure server with error 500 and reboot the box
3. Immeadiately after reboot schedule a 2 min legacy recording
4.Check ocapri log for error code 500 and connection retry requests
5. Also check the ocapri log for RDK error code RDK-10028 for connection lost with RWS server.
6.Clear the RWS server and RWS secure server error 500
7.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.

Checkpoint 2 Check whether the error codes are available in ocapri log</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_clearOcapri_log
3.TestMgr_Recorder_checkOcapri_log
4.TestMgr_Recorder_ExecuteCmd</test_stub_interface>
    <test_script>Recorder_RMF_Check_HTTP_500_RWSServer_Bootup_306</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
  <script_tags/>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_500_RWSServer_Bootup_306');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_500_RWSServer_Bootup_306');
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
        Keyword="FEATURE.RWS.GET.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://"+tm_ip+":8080/DVRSimulator/recorder/updateSchedule";
        print "Value" , Value
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details1 = rmfConfObj.getResultDetails();
        print result,","," ",details1
        if "FAILURE" in result:
                print "Failed to change the RWS Server Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the RWS Server Url"
        rmfConfObj.setResultStatus("SUCCESS");

        #To change the url in rmfconfig.ini
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        Keyword="FEATURE.SECURE_RWS.GET.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="https://"+tm_ip+":8443/DVRSimulator/recorder/secureUpdateSchedule";
        print "Value" , Value
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details2= rmfConfObj.getResultDetails();
        print result,","," ",details2
        if "FAILURE" in result:
                print "Failed to change the Secure RWS Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the Secure RWS Url"
        rmfConfObj.setResultStatus("SUCCESS");

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
 
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSServer',ip,'500');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSSecureServer',ip,'500');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSServer',ip);
 
        #unloading Recorder module
        recObj.unloadModule("Recorder");
        sleep(10);
        #Reboot the STB
        obj.initiateReboot();
        sleep(20);

        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "120000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
          
        #Frame json message to schedule a recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        rec_actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

        sleep(240);

        #Test component to be tested
        recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
        recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_500_RWSServer_Bootup_306');
        #Get the result of connection with test component and STB
        recLoadStatus = recObj.getLoadModuleResult();
        print "Recorder module loading status : %s" %recLoadStatus;
        recObj.setLoadModuleStatus(recLoadStatus);
   
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj.executeTestCase(expectedResult);

        if "true" in actResponse: 
            print "Checking ocapri_log"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "Received HTTP response code: 500"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "HTTP 500 error received ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "HTTP 500 error NOT received ";

            print "Checking ocapri_log for retry request"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "Connection to host not successfull waiting for"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "RWS server connection retry is happening";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "RWS server connection retry is NOT happening";

            print "Checking ocapri_log for RWS server connection error codes"
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
                print "Error Log RDK-10028 for RWS server connection lost is found ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Error Log RDK-10028 for RWS server connection lost is NOT found ";
              
            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSServer',ip);
            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSSecureServer',ip);
            actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSServer',ip);
            #Waiting for connection reset
            if "false" in actResponse:
                print "Waiting for connection re-establishment with RWS server "
                sleep(60)
        
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Error NOT enabled for RWS server";

        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.GET.URL";
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
            print "Failed to revert the RWS Server Url"
            rmfConfObj.setResultStatus("FAILURE");
            recObj.unloadModule("Recorder");
            exit();
        print "Reverted the RWS Server Url"
        rmfConfObj.setResultStatus("SUCCESS");        

        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.SECURE_RWS.GET.URL";
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
            print "Failed to revert the Secure RWS Server Url"
            rmfConfObj.setResultStatus("FAILURE");
            recObj.unloadModule("Recorder");
            exit();
        print "Reverted the Secure RWS Server Url"
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
