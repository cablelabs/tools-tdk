'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_GenerationId_Reset_OnCorruption_InlineHotRec_170</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Generation ID is reset if corruption occurs on reboot</synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import recorderlib
from random import randint
from time import sleep

#IP and Port of box, No need to change,
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
#This will be replaced with correspoing Box Ip and port while executing script
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Reset_OnCorruption_InlineHotRec_170');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        print "Rebooting box for setting configuration"
	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);

        print "Waiting for the recoder to be up"


        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        print "Clear Status Details: %s"%response;

        #Execute updateSchedule
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "180000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime";
        genIdIn = "test3b";

        #Frame json message for inline hot sched
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdIn+"\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        serverResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);
        print "Server response for inline updateSchedule: ",serverResponse;

        if 'updateSchedule' in serverResponse:
                print "Inline updateSchedule message post success";
                sleep(20)
                retry = 0;
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while ( ('[]' == recResponse) and (retry < 15) ):
                        sleep(10);
                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                        retry += 1
                print "Retrieve Status Details: %s"%recResponse;

                if (('[]' == recResponse) or ('ERROR' == recResponse)):
                        print "Received Empty/Error status";
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                	sleep(5)
                	#Delete the properties file
                	propFile = '/opt/data/recorder/recorder.props'

                        #Primitive test case which associated to this script
                        testObj = recObj.createTestStep('Recorder_SendRequestToDeleteFile');
                        expectedResult="SUCCESS";
                	#Delete properties file
                	testObj.addParameter("filename",propFile);
                	#Execute the test case in STB
                        testObj.executeTestCase(expectedResult);
                        #Get the actual result and details of execution
                        result = testObj.getResult();
                        details = testObj.getResultDetails();
                	print result,",",propFile," ",details

                	if "FAILURE" in result:
                        	print "Failed to corrupt recording properties"
                        	testObj.setResultStatus("FAILURE");
                	else:
                        	print "recorder properties corrupted"
                        	testObj.setResultStatus("SUCCESS")
                        	sleep(5)

                	response = recorderlib.callServerHandler('clearStatus',ip);
                        print "Rebooting box for properties file restoration"
                        recObj.initiateReboot();
                        print "Waiting for the recoder to be up"
                        sleep(300);

                        #Execute noUpdate
                        jsonMsgNoUpdate = "{\"noUpdate\":{}}";
                        serverResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
                        print "Server response for NoUpdate: %s"%serverResponse;

                        if 'noUpdate' in serverResponse:
                                print "noUpdate message post success";
                        	print "Waiting to get response from RWS"
                                sleep(30)
                                retry = 0
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
                                while ( ('[]' == recResponse) and (retry < 15) ):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                        	print "Retrieve Status Details: ",recResponse;
                                genIdOut = recorderlib.getGenerationId(recResponse)
                        	print "GenerationId retrieved after reboot: ",genIdOut
                                if "0" == genIdOut:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "GenerationId is successfully reset to 0"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                	print "GenerationId failed to reset to 0"
                	else:
                        	tdkTestObj.setResultStatus("FAILURE");
                        	print "noUpdate message post failed";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Inline updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
