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
  <version>21</version>
  <name>RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04</name>
  <primitive_test_id>540</primitive_test_id>
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <primitive_test_version>0</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: To Initiate recording with recording Id of length 256 characters and verify it is successful or not. And do the DVR playback of the recorded content.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_04
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RECORDER_RECORDID_256CHARCTER_04</test_case_id>
    <test_objective>To Initiate recording with recording Id of length 256 characters and verify it is successful or not. And do the DVR playback of the recorded content.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>1. rmfStreamer executable should be running.
2. Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “/tmp” path of device.
4. In rmfconfig.ini file the parameters “FEATURE.LONGPOLL.URL”,"FEATURE.RWS.GET.URL" and "FEATURE.RWS.POST.URL" should be pointing to DVRSimulator</pre_requisite>
    <api_or_interface_used>Json Interface

"RMFResult HnSource-&gt;init()
RMFResult HnSource-&gt;open(url,mimetype)
RMFResult HnSource-&gt;play()
RMFResult HnSource-&gt;getState()
RMFResult HnSource-&gt;pause()
RMFResult HnSource-&gt;close()
RMFResult HnSource-&gt;term()
RMFResult DvrSink-&gt;term()
RMFResult MPSink-&gt;init()
RMFResult MPSink-&gt; setVideoRectangle(x,y,width,height,applynow)
RMFResult MPSink-&gt;setSource(HnSource)
RMFResult MPSink-&gt;term()</api_or_interface_used>
    <input_parameters>Json Interface- source id = &lt;256 character length&gt;, duration recording_id, start_time.

HnSource-&gt;Init() - None
HnSource-&gt;Open() - char*-url,char*- mimetype
HnSource-&gt;play() - None
HnSource-&gt;pause() - None
HnSource-&gt;getState() - RMFState
HnSource-&gt;getMediaTime() - double
HnSource-&gt;getSpeed() - None
HnSource-&gt;close() - None
HnSource-&gt;term() - None
DvrSink-&gt;term() - None.
MpSink-&gt;Init() - None.
MpSink-&gt;setVideoRectangle() - unsigned – x,unsigned – y,unsigned – width,unsigned – height, bool – false.
MpSink-&gt;setSource() - RMFMediaSourceBase* - HnSource.
MpSink-&gt;term() - None.</input_parameters>
    <automation_approch>1. Test Mgr loads the RecorderAgent via tdk test agent.
2. Test Mgr fetches the source_id/ocap_id mapped in streaming details page in test manager, frames 256 character length recordId, duration, 
record start time (0-record immediately, else specify time), and get UTC time. Pass all the values to RecorderAgent.
3. The RecorderAgent will frame the final RWS record request json message to start the recording
and  send to TDK recorder simulator server which is in Test Mgr. 
4. The json message will be of the form " {"updateSchedule" : {"requestId" : "7", "schedule" : [ 
{"recordingId" : "&lt;256 length recordId&gt;","locator" : [ "ocap://0x5f43" ] ,"epoch" : ${now} ,"start" : "0" ,"duration" : 180000 ,
"properties":{"title":"Recording_&lt;256 character recordid&gt;&gt;"},"bitRate" : "HIGH_BIT_RATE" ,"deletePriority" : "P3" }]}} "
5. The TDK recorder simulator server will pass it to the comcast rmfStreamer process to initiate recording requested.
6. The comcast rmfStreamer will send the acknowledgement json message to TDK recorder simulator server and is passed to Test mgr. 
7. Test Mgr verifies the acknowledgement json message for SUCCESS/FAILURE.
8. And RecorderAgent also verifies the status of the recording by verifying ocapri_log.txt.txt.
9. The Final result after verifying ocapri_log.txt.txt RecorderAgent will send the SUCCESS/FAILURE to Test Mgr.
10. After recording is success. Verfying recording by doing the play back of the recording.
11. Test Mgr loads the mediaframework_agent via test agent.
12. Mediaframework_agent will create the instance for HNSource and  initialize the HnSource element HnSource-&gt;init().
13. On success, Mediaframework_agent will call HNSource-&gt;open() with the valid url(Ex: http://&lt;StreamingIP&gt;:8080/hnStreamStart?recordingId=&lt;RecordId&gt;&amp;segmentId=0). And request to playback will be served by comcast mfStreamer process.
14. On success, Mediaframework_agent will create the instance for MPSink and  initialize the MPSink element MpSink-&gt;init().
15. On success, Mediaframework_agent will call MpSink-&gt;setVideoRectangle() to set the video co-ordinates.
16. On success, Mediaframework_agent will call MpSink-&gt;setSource() to connect the source element with sink element.
17. On success, Mediaframework_agent will call HnSource-&gt;play() to playback the recorded content.
18. On success, Mediaframework_agent will call HnSource-&gt;getState() to check the playback is successful.
19.  On success, Mediaframework_agent will call HnSource-&gt;pause() to pause the playback before closing the pipeline.
20. On success, Mediaframework_agent will call MpSink-&gt;term() to terminate the  MPSink element..
21. On success, Mediaframework_agent will call HnSource-&gt;close() to close HnSource element.
27. On success, Mediaframework_agent will call HnSource-&gt;term() to terminate the  HNSource element.
28. On success, Mediaframework_agent will remove all the instance.
29. For each API called in the script, mediaframework_agent will send SUCCESS or FAILURE status to Test Mgr via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapri_log.txt to check the state of Recording. 
Checkpoint 3 Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>RecorderAgent
1.TestMgr_Recorder_SendRequest
2.TestMgr_Recorder_checkRecording_status

Mediaframework_agent</test_stub_interface>
    <test_script>RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import re;
import random;
import time;
import mediaframework;
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
sink_element=["MPSink"]
sink_parameter=["rmfElement"]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
videorec_parameter_name=["X","Y","width","apply","height"]
videorec_parameter_value=[0,0,1280,0,720]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]
recording_id_256 = str(random.randrange(10**9, 10**256));
details = " "

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    #Primitive test case which associated to this Script
    global mf_tdkTestObj
    global details
    mf_tdkTestObj =testobject.createTestStep(teststep);
    if teststep == 'RMF_Element_Open':
        streamDetails = mf_tdkTestObj.getStreamDetails('01');

        #fetch recording id from list matchList.
        url = mediaframework.getStreamingURL("DVR" , streamDetails.getGatewayIp() , recording_id_256 );
        print url
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            mf_tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print url;
        open_parameter_value.append(url);
    for item in range(len(parametername)):
        mf_tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    mf_tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = mf_tdkTestObj.getResult();
    details = mf_tdkTestObj.getResultDetails();
    if teststep != 'RMF_Element_Getstate':
        mf_tdkTestObj.setResultStatus(result);

    print "Status of "+ teststep+":  %s" %result;
    print "Details of "+ teststep+":  %s" %details;

    return result


#DVR playback function
def dvr_playBack():

        mf_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
        mf_obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04');

        mf_loadmodulestatus = mf_obj.getLoadModuleResult();
        print "Mediaframework module loading status :%s" %mf_loadmodulestatus ;
	#Set the module loading status
	mf_obj.setLoadModuleStatus(mf_loadmodulestatus.upper())

        if "SUCCESS" in mf_loadmodulestatus.upper():

                #--------------------PlayBack the Recording----------------

                #Prmitive test case which associated to this Script
                #Creating the Hnsrc instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mf_obj,Expected_Result,src_parameter,src_element);
                if Expected_Result in result.upper():
                        #Creating the MPSink instance
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mf_obj,Expected_Result,sink_parameter,sink_element);
                        if Expected_Result in result.upper():
                                #Initiazing the Hnsrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',mf_obj,Expected_Result,src_parameter,src_element);
                                if Expected_Result in result.upper():
                                        #Initiazing the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Init',mf_obj,Expected_Result,sink_parameter,sink_element);
                                        if Expected_Result in result.upper():
                                                #Opening the Hnsrc Element with playurl
                                                result=Create_and_ExecuteTestStep('RMF_Element_Open',mf_obj,Expected_Result,open_parameter_name,open_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Setting the MPSink Element with x,y co-ordiantes
                                                        result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',mf_obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Selecting the source for MPSink
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',mf_obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        #Play the HNSRC-->MPSINK pipeline
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play',mf_obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                        if Expected_Result in result.upper():
                                                                                time.sleep(20);
                                                                                #Check the get state of current pipeline
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_GetState',mf_obj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                        print "DVR playback successful"
                                                                                        mf_tdkTestObj.setResultStatus(result);
                                                                                else:
                                                                                        print "DVR playback successful"
                                                                                        mf_tdkTestObj.setResultStatus("FAILURE");

                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',mf_obj,Expected_Result,src_parameter,src_element);
                                                        #Close the Hnsrc Element
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Close',mf_obj,Expected_Result,src_parameter,src_element);
                                                #Terminating the MPSink Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Term',mf_obj,Expected_Result,sink_parameter,sink_element);
                                        #Terminating the HNSrc Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',mf_obj,Expected_Result,src_parameter,src_element);
                                #Removing the MPSink Element Instances
                                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mf_obj,Expected_Result,sink_parameter,sink_element);
                        #Removing the HNSrc Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mf_obj,Expected_Result,src_parameter,src_element);
                        #time.sleep(40);

                #Delete the Recording after testing to not mesh up with storage space.
                mf_obj.unloadModule("mediaframework")
                #--------------------Done--------------------------------

        return 0

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper())

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
               print "Waiting 300 seconds for STB to reboot";
               sleep(300);

        response = recorderlib.callServerHandler('clearStatus',ip);

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
	genIdInput = "TDK12345";
        duration = "30000";
        start_time = "0";
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
     	        RequestURL = "{\"updateSchedule\":{\"requestId\":\"789"+"\",\"generationId\":\""+genIdInput+"\",\"schedule\":[{\"recordingId\":\""+recording_id_256+"\",\"locator\":[\"ocap://0x125d\"],\"epoch\":curTime,\"start\":0,\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_256_Dvr_PlayBack_04"+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        status_expected = "updateSchedule";
        		expectedResult="SUCCESS";
			tdkTestObj.executeTestCase(expectedResult);
			sleep(5);
			status_actual = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        if status_expected in status_actual:
                                tdkTestObj.setResultStatus("SUCCESS");
                		print "updateSchedule message post success";
                		tdkTestObj.executeTestCase(expectedResult);
				print "Waiting to get acknowledgment status"
				sleep(10);
				retry=0
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		                while (('ack' not in actResponse) and (retry < 5)):
					sleep(10);
					actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
					retry += 1
				print "Retrieve Status Details: %s"%actResponse;
		                if ('acknowledgement' not in actResponse):
	        		        tdkTestObj.setResultStatus("FAILURE");
		        	        print "Failed to receive acknowledgement from recorder";
		                else:
                			tdkTestObj.setResultStatus("SUCCESS");
		                    	print "Successfully retrieved acknowledgement from recorder";

                                        print "Wait for recording to complete"
                                        sleep(30);

                                        print "Sending getRecordings to get the recording list"
                                        recorderlib.callServerHandler('clearStatus',ip)
                                        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
                                        print "Wait for 1 min to get response from recorder"
                                        sleep(60)
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                        print "Recording List: %s" %actResponse;
                                        recordingData = recorderlib.getRecordingFromRecId(actResponse,recording_id_256);
                                        print recordingData;
                                        if ('NOTFOUND' in recordingData):
                                                tdkTestObj.setResultStatus("FAILURE");
                                        else:
                                                tdkTestObj.setResultStatus("SUCCESS");
						#DVR Playback
						dvr_playBack()
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                		print "updateSchedule message post failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Requested recording url not formed";
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");

	#unloading Recorder module
	obj.unloadModule("Recorder");
