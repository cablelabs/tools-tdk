'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Inline_Verify_NoAck_NoUpdate_143</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_143 - Recorder should do nothing upon receiving NoUpdate message with dvrProtocolVersion field	via inline</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Inline_Verify_NoAck_NoUpdate_143');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

        recObj.initiateReboot();
	print "Sleeping to wait for the recoder to be up"
        sleep(300);

	#Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "10000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
        
	jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Update Schedule Details: %s"%actResponse;
	sleep(60);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;
        response = recorderlib.callServerHandler('retrieveStatus',ip);
        print "Retrieve Status Details: %s"%response;

        #Frame json message
        jsonMsgNoUpdate = "{\"noUpdate\":{\"dvrProtocolVersion\":\"6\"}}";

        expResponse = "noUpdate";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
        print "noUpdate Details: %s"%actResponse;

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "noUpdate message post success";
                print "Wait for 60s to get acknowledgement"
                sleep(60);
                #Check for acknowledgement from recorder
                tdkTestObj.executeTestCase(expectedResult);
		print "Looping till acknowledgement is received"
		loop = 0;
		while loop < 5:
	                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
	                #print "Retrieve Status Details: %s"%actResponse;
			sleep(10);
			loop = loop+1;
		if 'acknowledgement' in actResponse:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Received acknowledgement from recoder";
                elif 'acknowledgement' not in actResponse:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "No acknowledgement from recorder";	    
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
                    actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                    print "No Update Schedule Details: %s"%actResponse;
                    if expResponse in actResponse:
                        print "No Update message post success";
                        print "Wait for 60s to get the recording list"
                        sleep(120);
                        tdkTestObj1.setResultStatus("SUCCESS");
                        #Check for acknowledgement from recorder
                        tdkTestObj1.executeTestCase(expectedResult);
                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			print actResponse;
			actResponse = actResponse.replace("\"","");
                        print "Response Details: %s"%actResponse;
                        if "dvrProtocolVersion:7" in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Recorder did nothing upon receiving noUpdate message"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Recorder updated dvrProtocolVersion upon receiving noUpdate message"
                    else:
                            print "No Update message post failed";
                            tdkTestObj1.setResultStatus("FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to retrieve acknowledgement from recorder";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "noUpdate message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
