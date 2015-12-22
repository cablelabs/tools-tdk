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

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);
	print "Sleeping to wait for the recoder to be up"


	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
        actResponse =recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(30);

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
        recordingID = str(randint(10000, 500000));
	genIdInput = "FSL60";
	duration = "60000";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        startTime = "0";

        #Frame json message
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "updateSchedule message post success";
                tdkTestObj.executeTestCase(expectedResult);
		print "Waiting to get acknowledgment status"
		sleep(10);
		retry=0
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while (( ('ack' not in actResponse) ) and ('ERROR' not in actResponse) and (retry < 15)):
			sleep(10);
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			retry += 1
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                	tdkTestObj.setResultStatus("SUCCESS");
	                print "Successfully retrieved acknowledgement from recorder";
	                print "Wait for the recording to be completed"
		   	sleep(60);
                    	# Reboot the STB
		    	print "Rebooting the STB to get the recording list from full sync"
		    	recObj.initiateReboot();
		    	print "Sleeping to wait for the recoder to be up"
		   	sleep(300);
		    	response = recorderlib.callServerHandler('clearStatus',ip);
		    	print "Clear Status Details: %s"%response;
		    	#Frame json message
		    	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
                    	expResponse = "noUpdate";
		    	tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                    	tdkTestObj1.executeTestCase(expectedResult);
                    	actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
                    	print "No Update Schedule Details: %s"%actResponse;
                    	if expResponse in actResponse:
                        	print "No Update Schedule message post success";
                        	print "Wait for some time to get the recording list"
	                        sleep(300);
	                        tdkTestObj1.setResultStatus("SUCCESS");
        	                #Check for acknowledgement from recorder
                	        tdkTestObj1.executeTestCase(expectedResult);
                        	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
				print "Recording list" , actResponse;
				msg = recorderlib.getStatusMessage(actResponse);
				print "Get Status Message Details: %s"%msg;
                        	if "" == msg:
                                	value = "FALSE";
	                                print "No status message retrieved"
	        			tdkTestObj.setResultStatus("FAILURE");
        	                else:
					value = msg['recordingStatus']["initializing"];
					print "Initializing value: %s"%value;
					if "TRUE" in value.upper():
        	                		recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
	                	       		print recordingData
        	                		if 'NOTFOUND' not in recordingData:
	                        			tdkTestObj1.setResultStatus("SUCCESS");
                	            			key = 'status'
                        	    			value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	                        	    		print "key: ",key," value: ",value
        	                    			print "Successfully retrieved the recording list from recorder";
        	                    			print "Full sync successfull";
						else:
                	        	        	tdkTestObj1.setResultStatus("FAILURE");
                        	        		print "Failed to get the recording data";
        	                    			print "Full sync failed";
                    		# Reboot the STB
			    	print "Rebooting the STB again to get the recording list from full sync"
			    	print "This reboot is without recording changes, full sync should not happen"
			    	recObj.initiateReboot();
			    	print "Sleeping to wait for the recoder to be up"
			   	sleep(300);
		    		response = recorderlib.callServerHandler('clearStatus',ip);
			    	print "Clear Status Details: %s"%response;
			    	#Frame json message
			    	jsonMsgNoUpdate = "{\"noUpdate\":{}}";
	                    	expResponse = "noUpdate";
			    	tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                	    	tdkTestObj1.executeTestCase(expectedResult);
                    		actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
	                    	print "No Update Schedule Details: %s"%actResponse;
        	            	if expResponse in actResponse:
	                        	print "No Update Schedule message post success";
        	                	print "Wait for some time to get the recording list"
	        	                sleep(300);
	                	        tdkTestObj1.setResultStatus("SUCCESS");
	        	                #Check for acknowledgement from recorder
        	        	        tdkTestObj1.executeTestCase(expectedResult);
                	        	actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
					print actResponse;
					msg = recorderlib.getStatusMessage(actResponse);
					print "Get Status Message Details: %s"%msg;
                	        	if (("" == msg) or ('NOSTATUS' == msg) or ("recordingStatus" not in msg)):
	                        	        print "No status message retrieved as expected"
	        				tdkTestObj.setResultStatus("SUCCESS");
	        	                else:
						value = msg['recordingStatus']["initializing"];
						print "Initializing value: %s"%value;
						if "TRUE" in value.upper():
        	                			recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
		                	       		print recordingData
        		                		if 'NOTFOUND' not in recordingData:
	                	        			tdkTestObj1.setResultStatus("SUCCESS");
                	        	        		print "Failed to get the recording data as expected";
        	        	            			print "Full sync failed";
							else:
        	        	        	        	tdkTestObj1.setResultStatus("FAILURE");
                		            			key = 'status'
                        		    			value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	                        		    		print "key: ",key," value: ",value
        	                    				print "Successfully retrieved the recording list from recorder";
        	                    				print "Full sync successfull, it was not expected";
						else:
		        		        	tdkTestObj1.setResultStatus("FAILURE");
                				        print "Failed to retrieve the recording list from recorder";
                    		else:
                        		print "No Update Schedule message post failed";
		                        tdkTestObj1.setResultStatus("FAILURE");
                    	else:
                        	print "No Update Schedule message post failed";
	                        tdkTestObj1.setResultStatus("FAILURE");
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                    	print "Failed to retrieve acknowledgement from recorder";
        else:
	        tdkTestObj.setResultStatus("FAILURE");
                print "updateSchedule message post failure";
        recObj.unloadModule("Recorder");
else:
	print "Failed to load Recorder module";
    	#Set the module loading status
    	recObj.setLoadModuleStatus("FAILURE");
