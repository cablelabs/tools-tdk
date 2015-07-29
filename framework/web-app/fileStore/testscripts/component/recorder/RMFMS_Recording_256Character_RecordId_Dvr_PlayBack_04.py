'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>18</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To Initiate recording with recording Id of length 256 characters and verify it is successful or not. And do the DVR playback of the recorded content.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_04
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
recording_id_256 = " "
details = " "

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    #Primitive test case which associated to this Script
    global mf_tdkTestObj
    global recording_id_256
    global details
    mf_tdkTestObj =testobject.createTestStep(teststep);
    if teststep == 'RMF_Element_Open':
        streamDetails = mf_tdkTestObj.getStreamDetails('01');

        #fetch recording id from list matchList.
        recordID = recording_id_256
        url = mediaframework.getStreamingURL("DVR" , streamDetails.getGatewayIp() , recordID );
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

        if "SUCCESS" in mf_loadmodulestatus.upper():
                #Set the module loading status
                mf_obj.setLoadModuleStatus("SUCCESS");

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
        else:
                print "Failed to load mediaframework  module";
                #Set the module loading status
                mf_obj.setLoadModuleStatus("FAILURE");

        return 0

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
obj.configureTestCase(ip,port,'RMFMS_Recording_256Character_RecordId_Dvr_PlayBack_04');
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():
        global recording_id_256
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        loadmoduledetails = obj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               obj.initiateReboot();
               print "Waiting 300 seconds for STB to reboot";
               sleep(300);

        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_SendRequest');
        rec_id = random.randrange(10**9, 10**256);
	requestID = str(rec_id);
        recording_id_256 = str(rec_id);
	genIdInput = requestID;
        print "Record_256---->:",recording_id_256 
        duration = "180000";
        start_time = "0";
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                print "ocapid : %s" %validid;
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
     	        RequestURL = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"schedule\":[{\"recordingId\":\""+recording_id_256+"\",\"locator\":[\"ocap://0x125d\"],\"epoch\":curTime,\"start\":0,\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recording_id_256+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}"
                print "RequestURL  is : %s" %RequestURL ;
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Requested recording url is formed";
                        status_expected = "updateSchedule";
        		expectedResult="SUCCESS";
			tdkTestObj.executeTestCase(expectedResult);
			sleep(5);
			status_actual = recorderlib.callServerHandlerWithMsg('updateMessage',RequestURL,ip);
                        print "Status string is: %s"%status_actual;
                        if status_expected in status_actual:
                                tdkTestObj.setResultStatus("SUCCESS");
                		print "updateSchedule message post success";
                		tdkTestObj.executeTestCase(expectedResult);
				print "Waiting to get acknowledgment status"
				sleep(10);
				retry=0
				actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
		                while ((('[]' in actResponse) or ('ack' not in actResponse)) and ('ERROR' not in actResponse) and (retry < 15)):
					sleep(10);
					actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
					retry += 1
				print "Retrieve Status Details: %s"%actResponse;
		                if (('[]' in actResponse) or ('ERROR' in actResponse)):
	        		        tdkTestObj.setResultStatus("FAILURE");
		        	        print "Received Empty/Error status";
		                elif 'acknowledgement' in actResponse:
                			tdkTestObj.setResultStatus("SUCCESS");
		                    	print "Successfully retrieved acknowledgement from recorder";
                                #Prmitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('Recorder_checkRecording_status');
                                print "Record_256---->:",recording_id_256
                                PATTERN = recording_id_256;
                                print "PATTERN--->:",PATTERN
                                tdkTestObj.addParameter("Recording_Id",recording_id_256);
                                #Execute the test case in STB
                                expectedresult="SUCCESS";
                                tdkTestObj.executeTestCase(expectedresult);
                                #Get the Actual result of streaming Interface
                                actualresult = tdkTestObj.getResult();
                                print "In script **********************"
                                patterndetails = tdkTestObj.getResultDetails();
                                print "Pattern details is : %s" %patterndetails;
                                duration_int = int(duration);
                                duration_sec = duration_int/1000;
                                duration_string = str(duration_sec);
                                print duration_string;
                                #compare the actual result with expected result
                                if expectedresult in actualresult:
                                        if (PATTERN in patterndetails):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                #Getting the mplayer log file from DUT
                                                logpath=tdkTestObj.getLogPath();
                                                print "Log path : %s" %logpath;
                                                tdkTestObj.transferLogs(logpath,"false");
                                                print "Successfully scheduled a Recording";

                                                #DVR Playback.
                                                dvr_playBack()
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                #Getting the mplayer log file from DUT
                                                logpath=tdkTestObj.getLogPath();
                                                print "Log path : %s" %logpath;
                                                tdkTestObj.transferLogs(logpath,"false");
                                                print "Recording is not completed with requested duration";
                                else:
                                        print "Failed to schedule a Recording";
                                        tdkTestObj.setResultStatus("FAILURE");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                		print "updateSchedule message post failure";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Requested recording url not formed";
                #unloading Recorder module
                obj.unloadModule("Recorder");
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");
else:
        print "Failed to load Recorder module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
