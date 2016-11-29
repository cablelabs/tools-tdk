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
  <name>Recorder_RMF_Tune_Live_Schedule_Overlap_Recordings_Inline_260</name>
  <primitive_test_id/>
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>CT_Recoder_DVR_Protocol_260 - Check whether overlapping recordings are completed successfully when live playback happens on the same channel</synopsis>
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
    <test_case_id>CT_Recorder_DVR_Protocol_260</test_case_id>
    <test_objective>To Check whether overlapping recordings are completed successfully when live playback happens on the same channel usnig inline</test_objective>
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
3.Tune to a live channel
4.RecorderAgent / Python lib interface will frame the json message to schedule a  recording of 6 min duration with  using inline mechanism and send to TDK Recorder Simulator server which is present in TM.
5.Wait for  5 mins then schedule an another recording on same channel for 6 mins 
6.getrecordings message will be send to TDK Recorder Simulator server once STB is up to get the list of recordings.
7. Status of the Json response from Recorder to TDK Recorder Simulator server getting extracted by TM.
8.Depends on the result of above step RecorderAgent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Acknowledgement status from the DVRSimulator.
Checkpoint 2 Get the list of recordings to check the state of current recordings</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest</test_stub_interface>
    <test_script>Recorder_RMF_Tune_Live_Schedule_Overlap_Recordings_Inline_260</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
import tdklib;
import mediaframework;
import time;
import recorderlib
from sys import exit
from random import randint
from time import sleep

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
ip = <ipaddress>
port = <port>

recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Tune_Live_Schedule_Overlap_Recordings_Inline_260');

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'SampleTest');

loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;

def ScheduleRec():

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
			print "Sleeping to wait for the recoder to be up"
		       	sleep(300);

        
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
                requestID = str(randint(10, 500));
                recordingID = str(randint(10000, 500000));
                duration = "360000";
                startTime = "0";
                ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
                now = "curTime"

                #Frame json message
                jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

                expResponse = "updateSchedule";
                tdkTestObj.executeTestCase(expectedResult);
                actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
                print "Update Schedule Details: %s"%actResponse; 
        
                if expResponse in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "updateSchedule message post success";
                    #Check for acknowledgement from recorder
                    tdkTestObj.executeTestCase(expectedResult);
                    print "Looping till acknowledgement is received"
                    loop = 0;
                    actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                    while (('ack' not in actResponse) and (loop < 5)):
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        sleep(10);
                        loop = loop+1;
                    print "Retrieve Status Details: ",actResponse;

                    if 'acknowledgement' not in actResponse:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Received Empty/Error status";
                    elif 'acknowledgement' in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Successfully retrieved acknowledgement from recorder";
                        #waiting for 5 mins 
                        sleep(300);

                        #Frame json message
                        jsonMsg_new = "{\"updateSchedule\":{\"requestId\":\""+str(int(requestID)+1)+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+str(int(recordingID)+1)+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"requestedStart\":0,\"title\":\"Recording_"+str(int(recordingID)+1)+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P4\"}]}}";

                        tdkTestObj.executeTestCase(expectedResult);
                        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg_new,ip);
                        print "updateSchedule Details: %s"%actResponse;
                        if expResponse in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "updateSchedule message post success";
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        while (('ack' not in actResponse) and (loop < 5)):
                            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                            sleep(10);
                            loop = loop+1;
                        print "Retrieve Status Details: ",actResponse;

                        if 'acknowledgement' not in actResponse:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Received Empty/Error status";
                        elif 'acknowledgement' in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                       
                        #Wait for 6 mins for recording to complete
                        sleep(360);
                        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Sending getRecordings to get the recording list"
                        recorderlib.callServerHandler('clearStatus',ip)
                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                        print "Wait for 1 min to get response from recorder"
                        sleep(60)
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                        print "Recording List: %s" %actResponse;
                        recordingData1 = recorderlib.getRecordingFromRecId(actResponse,recordingID);            
                        recordingData2 = recorderlib.getRecordingFromRecId(actResponse,str(int(recordingID)+1));            
                        print recordingData1,recordingData2
                        if 'NOTFOUND' not in (recordingData1 and recordingData2):
                            statusKey = 'status'
                            statusValue1 = recorderlib.getValueFromKeyInRecording(recordingData1,statusKey)
                            statusValue2 = recorderlib.getValueFromKeyInRecording(recordingData2,statusKey)
                            print "Successfully retrieved the recording list from recorder";
                            tdkTestObj.setResultStatus("SUCCESS");
                            if "COMPLETE" in (statusValue1.upper() and statusValue2.upper()):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Recording completed successfully.";
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Recording not completed successfully";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve the recording list from recorder";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to retrieve acknowledgement from recorder";
         
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "updateSchedule message post failed";    
 
                #unloading Recorder module
                recObj.unloadModule("Recorder");
	    
        else:
            print "Failed to load Recorder module";
	    #Set the module loading status
    	    recObj.setLoadModuleStatus("FAILURE");	  

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
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
    print "Status of "+ teststep+":  %s" %result;
    return result

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_HNSRC_MPSINK_Video_Play_01');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if Expected_Result in loadModuleStatus.upper():

        #Prmitive test case which associated to this Script
        obj.setLoadModuleStatus("SUCCESS");
        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        time.sleep(60);
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                ScheduleRec()
                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);
                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                time.sleep(20);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
