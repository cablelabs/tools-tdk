#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_RecStartedEarly_StartedIncomplete_Legacy_85</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder must parse properties.requestedStart and send STARTED_EARLY/STARTED_LATE if actual start varies by
more than 30 seconds from requested (note: not to be confused with expectedStart, which is the air time listed in the guide)</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>100</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>DELIA-5685-Conversion of TSB to recording mechanism is removed</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
import tdklib;
import mediaframework;
import time;
import recorderlib
from sys import exit
from random import randint
from time import sleep

ip = <ipaddress>
port = <port>

src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
sink_element=["MPSink"]
sink_parameter=["rmfElement"]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]
mediatime_parameter_name=["mediaTime","rmfElement"]
mediatime_parameter_value=[2000,"HNSrc"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
videorec_parameter_name=["X","Y","width","apply","height"]
videorec_parameter_value=[0,0,1280,0,720]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]

mfObj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
mfObj.configureTestCase(ip,port,'Recorder_RMF_RecStartedEarly_StartedIncomplete_Legacy_85');
mfLoadStatus = mfObj.getLoadModuleResult();
print "mediaframework load Module Status :  %s" %mfLoadStatus;
#Set the module loading status
mfObj.setLoadModuleStatus(mfLoadStatus.upper())

def ScheduleRec():
	recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
	recObj.configureTestCase(ip,port,'Recorder_RMF_RecStartedEarly_StartedIncomplete_Legacy_85');
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
        	actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
		sleep(10);

	        #Pre-requisite
        	response = recorderlib.callServerHandler('clearStatus',ip);

        	#Primitive test case which associated to this script
	        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        	expectedResult="SUCCESS";

	        #Execute updateSchedule
        	requestID = str(randint(10,500));
	        recordingID = str(randint(10000, 500000));
		genIdInput = recordingID;
		duration = "180000";
	        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID();
	        now = "curTime";
        	startTime = "0";

        	#Frame json message
		jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"6\",\"schedule\":[{\"recordingId\":\""+ recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"

	        expResponse = "updateSchedule";
	        tdkTestObj.executeTestCase(expectedResult);
        	actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
	        if expResponse in actResponse:
        	        tdkTestObj.setResultStatus("SUCCESS");
                	print "updateSchedule message post success";
	                tdkTestObj.executeTestCase(expectedResult);
			print "Waiting to get acknowledgment status"
			sleep(10);
			retry=0	
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                	while (( ('ack' not in actResponse) ) and (retry < 5)):
				sleep(5);
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
				retry += 1
			print "Retrieve Status Details: %s"%actResponse;
        	        if 'acknowledgement' in actResponse:
                		tdkTestObj.setResultStatus("SUCCESS");
	                	print "Successfully retrieved acknowledgement from recorder";
                                print "Wait for the recording to complete"
                                sleep(180);
				print "Sending getRecordings to get the recording list"
				recorderlib.callServerHandler('clearStatus',ip)
				recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
				print "Wait for 60 seconds to get response from recorder"
				sleep(60)
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
				print "Recording List: %s" %actResponse;
				tdkTestObj1 = recObj.createTestStep('Recorder_SendRequest');
                                tdkTestObj1.executeTestCase(expectedResult);
				msg = recorderlib.getStatusMessage(actResponse);
				print "Get Status Message Details: %s"%msg;
                	        if "NOSTATUS" == msg:
                        	       	value = "FALSE";
	                                print "No status message retrieved"
	        			tdkTestObj1.setResultStatus("FAILURE");
        		        else:
					value = msg['recordingStatus']["initializing"];
					print "Initializing value: %s"%value;
					if "TRUE" in value.upper():
        	        	       		recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
	                	       		print recordingData
        	                		if 'NOTFOUND' not in recordingData:
	                	       			key = 'status'
        	                    			value = recorderlib.getValueFromKeyInRecording(recordingData,key)
	        	               	    		print "key: ",key," value: ",value
        	        	       			print "Successfully retrieved the recording list from recorder";
                	            			if "STARTEDINCOMPLETE" in value.upper():
                        	       				tdkTestObj1.setResultStatus("SUCCESS");
	                	               			print "Recording marked as STARTEDINCOMPLETE as expected";
        	        	       				key = 'error'
	        	               	    			value = recorderlib.getValueFromKeyInRecording(recordingData,key)
		        	               	    		print "key: ",key," value: ",value
                	            				if "STARTED_EARLY" in value.upper():
                        	       					tdkTestObj1.setResultStatus("SUCCESS");
		                        		       		print "error set to STARTED_EARLY as expected";
	        	                			else:
	                	                			tdkTestObj1.setResultStatus("FAILURE");
			                	                	print "error NOT set to STARTED_EARLY as expected";
        		                    		else:
                		                		tdkTestObj1.setResultStatus("FAILURE");
	                		               		print "Recording NOT marked as STARTEDINCOMPLETE as expected";
						else:
                	        	       		tdkTestObj1.setResultStatus("FAILURE");
	                        	        	print "Failed to get the recording data";
			                else:
        			                tdkTestObj1.setResultStatus("FAILURE");
                			        print "Failed to retrieve the recording list from recorder";
			else:
                		tdkTestObj.setResultStatus("FAILURE");
	                    	print "Failed to retrieve acknowledgement from recorder";
        	else:
	        	tdkTestObj.setResultStatus("FAILURE");
	                print "updateSchedule message post failure";

        	recObj.unloadModule("Recorder");


def Create_and_ExecuteTestStep(teststep, testmfObject, expectedresult,parametername, parametervalue):
    global Mediatime
    global tdkTestObj
    #Primitive test case which associated to this Script
    tdkTestObj =testmfObject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = mediaframework.getStreamingURL("TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    details = tdkTestObj.getResultDetails();
    print "Status of "+ teststep+":  %s" %result;
    print "Details of "+ teststep+":  %s" %details;
    if teststep == "RMF_Element_Getmediatime":
        if "SUCCESS" in result.upper():
                Mediatime=details.split(":");
                print Mediatime[1];

    return result


if Expected_Result in mfLoadStatus.upper():

        #Prmitive test case which associated to this Script
        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mfObj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mfObj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',mfObj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',mfObj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',mfObj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',mfObj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',mfObj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',mfObj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        #Get the Mediatime value
									time.sleep(5);
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',mfObj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper():
                                                                                initialmediatime=float(Mediatime[1]);
										print "Filling TSB for 2 minutes";
                                                                                time.sleep(120);
										print "Actual test starts ...";
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',mfObj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper():
                                                                                        Mediatime[1]=float(Mediatime[1]);
                                                                                        if Mediatime[1] < initialmediatime:
                                                                                                print "success"
                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                        else:
                                                                                                print "failure"
                                                                                                tdkTestObj.setResultStatus("FAILURE");
									ScheduleRec();

                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',mfObj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',mfObj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',mfObj,Expected_Result,src_parameter,src_element);
                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mfObj,Expected_Result,sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mfObj,Expected_Result,src_parameter,src_element);
                time.sleep(40);
        mfObj.unloadModule("mediaframework");
