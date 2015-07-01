'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_GenerationId_noUpdate_RWS_16</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder- To accept Generation ID via noUpdate retrieved from RWS</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>25</execution_time>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_noUpdate_RWS_16');
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

        genIdInput = "test2c";

        #Execute Inline noUpdate
        jsonMsgNoUpdate = "{\"noUpdate\":{\"generationId\":\""+genIdInput+"\"}}";
        serverResponse =recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsgNoUpdate,ip);
        print "Server response for Inline NoUpdate: %s"%serverResponse;

        if 'noUpdate' in serverResponse:
        	print "Inline noUpdate message post success";
                #Check that no status is POST is received from recorder for noupdate
                sleep(30)
                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                print "Retrieve Status Details: %s"%recResponse;

		if 'ERROR' in recResponse:
			print "Received Error status";
			tdkTestObj.setResultStatus("FAILURE");
		elif '[]' in recResponse:
			print "Recorder did not make any POST request to RWS with noUpdate"
                        #Execute updateSchedule
                        requestID = str(randint(10, 500));
                        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\"}}";
                        serverResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
                        print "Server response for UpdateSchedule: %s"%serverResponse;

                        if 'updateSchedule' in serverResponse:
                                print "updateSchedule message post success";
                                sleep(20)
                                retry = 0;
                                recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                while ( ('[]' in recResponse) and ('ERROR' not in recResponse) and (retry < 15)):
                                        sleep(10);
                                        recResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        retry += 1
                                print "Retrieve Status Details: %s"%recResponse;

                                if (('[]' in recResponse) or ('ERROR' in recResponse)):
                                        print "Received Empty/Error status";
                                        tdkTestObj.setResultStatus("FAILURE");
                                else:
                                        genOut = recorderlib.getGenerationId(recResponse)
                                        if genOut == genIdInput:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "GenerationId retrieved (%s) matches with expected (%s)"%(genOut,genIdInput);
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "GenerationId retrieved (%s) does not match with expected (%s)"%(genOut,genIdInput);
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "updateSchedule message post failed";
		else:
			tdkTestObj.setResultStatus("FAILURE");
			print "Recorder sent POST request to RWS with noUpdate"
        else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Inline noUpdate message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
