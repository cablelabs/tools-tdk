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
  <name>Recorder_RMF_ChecksumChange_fullSync_Inline_60</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should do a full sync only on reboot, but only if there has been any change in completed recordings checksum</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>100</execution_time>
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
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import recorderlib
from random import randint
from time import sleep
#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>
#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_ChecksumChange_fullSync_Inline_60');
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

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10,500));
        recordingID = str(randint(10000, 500000));
	genId = "TDK123";
	duration = "60000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genId+"\",\"fullSchedule\":true,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                tdkTestObj.executeTestCase(expectedResult);
		print "Waiting to get acknowledgment status"
		retry=0
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (( ('ack' not in actResponse) ) and (retry < 5)):
			sleep(10);
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			retry += 1
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                	tdkTestObj.setResultStatus("SUCCESS");
	                print "Successfully retrieved acknowledgement from recorder";
	                print "Wait for 70s for the recording to be completed"
		   	sleep(70);
                    	# Reboot the STB
			response = recorderlib.callServerHandler('clearStatus',ip);
		    	print "Rebooting the STB to get the recording list from full sync"
		    	recObj.initiateReboot();
		    	print "Sleeping to wait for the recoder to be up"
		   	sleep(300);
                    	expResponse = "noUpdate";
		    	tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                    	tdkTestObj.executeTestCase(expectedResult);
                    	actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
                    	if expResponse in actResponse:
                        	print "No Update Schedule message post success";
                        	print "Wait for some time to get the recording list"
	                        sleep(60);
	                        tdkTestObj.setResultStatus("SUCCESS");
        	                #Check for acknowledgement from recorder
                        	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
				print "Response after first full sync: " ,actResponse;
				msg = recorderlib.getStatusMessage(actResponse);
                        	if "NOSTATUS" == msg:
					print "Full sync failed";
	        			tdkTestObj.setResultStatus("FAILURE");
        	                else:
					print "Full sync successful";
        	                	recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
	                	       	print recordingData
        	                	if 'NOTFOUND' not in recordingData:
                                        	status = recorderlib.getValueFromKeyInRecording(recordingData,'status')
						if "COMPLETE" in status.upper():
	                        			tdkTestObj.setResultStatus("SUCCESS");
                                			# Reboot the STB again
                                			response = recorderlib.callServerHandler('clearStatus',ip);
                                			print "Rebooting the STB again to get the recording list from full sync"
                                			print "This reboot is without recording changes, full sync should not happen"
                                			recObj.initiateReboot();
                                			print "Sleeping to wait for the recoder to be up"
                                			sleep(300);
                                			expResponse = "noUpdate";
                                			tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                                			tdkTestObj.executeTestCase(expectedResult);
                                			actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
                                			if expResponse in actResponse:
                                        			print "No Update Schedule message post success";
                                        			print "Wait for some time to get the recording list"
                                        			sleep(60);
                                        			tdkTestObj.setResultStatus("SUCCESS");
                                        			tdkTestObj.executeTestCase(expectedResult);
                                        			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        			print "Response after second full sync: " ,actResponse;
                                        			msg = recorderlib.getStatusMessage(actResponse);
                                        			if 'NOSTATUS' == msg:
                                                			print "Full sync did not happen as expected"
                                                			tdkTestObj.setResultStatus("SUCCESS");
                                    				else:
					                                print "Full sync happened again"
									tdkTestObj.setResultStatus("FAILURE");
                                        				recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
                                        				print recordingData
                                			else:
                                        			print "No Update Schedule message post failed";
                                        			tdkTestObj.setResultStatus("FAILURE");
						else:
							tdkTestObj.setResultStatus("FAILURE");
							print "Scheduled recording not in complete state";
					else:
                	        	       	tdkTestObj.setResultStatus("FAILURE");
                        	        	print "Failed to get the recording data";
                    	else:
                        	print "No Update Schedule message post failed";
	                        tdkTestObj.setResultStatus("FAILURE");
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                    	print "Failed to retrieve acknowledgement from recorder";
        else:
	        tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failure";

        recObj.unloadModule("Recorder");
