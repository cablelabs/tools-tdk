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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Trm_Cancel_MaxTuners_Diff_OcapId_190</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_190 - Recorder to send TRM_CANCELLED error if recordings are scheduled on all max number of tuners available with different service locators and then schedule one more recording with different ocap id</synopsis>
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
</xml>
'''
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from random import randint
from time import sleep
from trm import getMaxTuner


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Trm_Cancel_MaxTuners_Diff_OcapId_190');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
trmObj.configureTestCase(ip,port,'Recorder_RMF_Trm_Cancel_MaxTuners_Diff_OcapId_190');
#Get the result of connection with test component and STB
result = trmObj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
trmObj.setLoadModuleStatus(result.upper());

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    trmObj.initiateReboot();
    trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
    trmObj.configureTestCase(ip,port,'Recorder_RMF_Trm_Cancel_MaxTuners_Diff_OcapId_190');
    #Get the result of connection with test component and STB
    result = trmObj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;
    sleep(300)

trmObj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
               print "Sleeping to wait for the recoder to be up"
	       sleep(300);

        #Giving no update here to get the recording list in case the previous generation id is set to zero before reboot
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
	sleep(10);

        #Pre-requisite to clear any recording status
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "120000";
        startTime = "0";
        now = "curTime"

        tdkTestObj.executeTestCase(expectedResult);

        maxTuner = getMaxTuner(trmObj,'SUCCESS')
        if ( 0 == maxTuner ):
                print "Exiting without executing the script"
                tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("SUCCESS");
                for deviceNo in range(0,maxTuner):
                	Id = '0'+str(deviceNo+1)
	                recId = str(randint(10000, 500000));
			streamId = tdkTestObj.getStreamDetails(Id).getOCAPID()

	                #Frame json message
        	        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recId+"\",\"locator\":[\"ocap://"+streamId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recId+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";
                	expResponse = "updateSchedule";
                        tdkTestObj.executeTestCase(expectedResult);
               		actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

                if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateSchedule message post success";
                        print "Wait for 60s to get acknowledgement"
                        sleep(20);
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        while (('acknowledgement' not in actResponse) and (loop < 5)):
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                sleep(10);
                                loop = loop+1;
                        print "Retrieve Status Details: %s"%actResponse;
                        if 'acknowledgement' in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                            print "Wait for 60s for the recording to be completed"

                            #Frame json message for update recording
                            Id = '0'+str(maxTuner+1)
                            ocapId = tdkTestObj.getStreamDetails(Id).getOCAPID()

                            jsonMsgFullSchedule = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                            expResponse = "updateSchedule";
                            tdkTestObj.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgFullSchedule,ip);
                            print "updateSchedule Details for rescheduling: %s"%actResponse;
                            if expResponse in actResponse:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "updateSchedule message post success";
                                print "Wait to get acknowledgement"
                                sleep(120);
                                #Check for acknowledgement from recorder
                                tdkTestObj.executeTestCase(expectedResult);
                                print "Looping till acknowledgement is received"
                                loop = 0;
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while (('acknowledgement' not in actResponse) and (loop < 5)):
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        sleep(10);
                                        loop = loop+1;
                                print "Retrieve Status Details: %s"%actResponse;
                                if 'acknowledgement' in actResponse:
                                        print "Successfully retrieved acknowledgement from recorder";
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                                        print recordingData
                                        if 'NOTFOUND' not in recordingData:
                                                key = 'error'
                                                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                                                print "key: ",key," value: ",value
                                                print "Successfully retrieved the recording status";
                                                if "TRM_CANCELLED" in value.upper():
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print "Recorder has send the TRM_CANCELLED error";
                                                elif "BADVALUE" in value.upper():
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "No error field in recording status";
                                                else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print "Recorder failed to send the TRM_CANCELLED error";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "Failed to retrieve the recording status";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Failed to retrieve acknowledgement from recorder";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
        trmObj.unloadModule("trm");
