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
  <version>5</version>
  <name>Recorder_RMF_Configure_WrongLongpoll_Url_238</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recorder_DVR_Protocol_238 - Recorder- To check whether recorder sends error or not for  the loss of connection with Long poll Server</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_238</test_case_id>
    <test_objective>To check whether recorder sends error or not for  the loss of connection with Long poll Server</test_objective>
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
3.Configure alternate URL for the long poll server and reboot the box
4. Wait for 1 minute for the error code to come after multiple retries
5.. Verify that error code RDK-10029 is available in ocapri log
6. Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 The error code should be avilable in Ocapri log</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_checkOcapri_log</test_stub_interface>
    <test_script>Recorder_RMF_Configure_WrongLongpoll_Url_238</test_script>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongLongpoll_Url_238');
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
	    print "Sleeping to wait for the recoder to be up"

        #To clear all the alternate URL's set for Servers
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','LPServer',ip);
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','RWSServer',ip);
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','RWSStatus',ip);
        print "Cleared all alternate URL's set in Servers";

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        #configure DVRSimulator to send bad Long Poll URL from Long Poll end point
        actResponse = recorderlib.callServerHandlerWithTypeAndNewUrl('configureAlternateURL','LPServer',ip,'wrongLongPoll');
        #Checking whether alternate wrong url is configured or not
        actResponse = recorderlib.callServerHandlerWithType('isAlternateURLEnabled','LPServer',ip);
        print actResponse;
        
        if "wrongLongPoll" in actResponse:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Alternate URL enabled for Long poll server";
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

            # Reboot the STB
            print "Rebooting the STB"
            recObj.initiateReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);
            #sleep to wait error code to come after multiple retries to get the connection to long poll
            print "Checking ocapri_log" 
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "RDK-10029"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);  
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            loop=0;
             
            while (('SUCCESS' not in result) and (loop < 5)):
                sleep(300);
                tdkTestObj2.executeTestCase(expectedResult);  
                result = tdkTestObj2.getResult();
                details = tdkTestObj2.getResultDetails();
                loop = loop+1;
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Error Log RDK-10029 for Long poll server connection lost is found ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Error Log RDK-10029 for Long poll server connection lost is NOT found "; 
           
            #To clear the wrong Long poll Url
            tdkTestObj2.executeTestCase(expectedResult);
            actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','LPServer',ip);
            print actResponse;
            if "cleared" in actResponse:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Alternate URL of Long poll Server reverted";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Alternate URL of Long poll Server is not reverted";

            recObj.initiateReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);

      
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Alternate URL NOT enabled for Long poll server";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE"); 
