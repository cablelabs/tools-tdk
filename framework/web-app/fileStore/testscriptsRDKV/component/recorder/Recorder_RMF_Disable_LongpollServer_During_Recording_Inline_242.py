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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Disable_LongpollServer_During_Recording_Inline_242</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recorder_DVR_Protocol_242 - Recorder- To check whether recorder sends error or not for  the loss of connection with Long poll Server during recording operations</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <script_tags />
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Disable_LongpollServer_During_Recording_Inline_242');
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
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "600000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
        
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

        #Frame json message to schedule a recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        sleep(10);
     
        #To disable the long poll server
        actResponse = recorderlib.callServerHandlerWithType('disableServer','LPServer',ip);
        print actResponse;
        
        if "Disabled" in actResponse:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Long poll server is disabled";
            print "Checking ocapri_log"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "RDK-10029"
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
                print "Error Log RDK-10029 for Long poll server connection lost is found ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Error Log RDK-10029 for Long poll server connection lost is NOT found "; 
           
            #To clear the wrong Long poll Url
            tdkTestObj.executeTestCase(expectedResult);
            actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','LPServer',ip);
            print actResponse

            #To enable the long poll server
            actResponse = recorderlib.callServerHandlerWithType('enableServer','LPServer',ip);
            print actResponse
            print "Wait for recorder to connect to longpoll server"
            sleep(250);
      
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Unable to disable Long poll server";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE"); 

