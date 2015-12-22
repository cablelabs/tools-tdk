'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_GenerationId_Inline_UpdateSchedule_11</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder- To accept Generation ID via inline updateSchedule, basic test.</synopsis>
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
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_GenerationId_Inline_UpdateSchedule_11');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot();
               print "Waiting for the recoder to be up"
	       sleep(300);

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";

        #Execute updateSchedule
        requestID = str(randint(10,500));
	genIdInput = "test1a";

        #Frame json message
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\""+genIdInput+"\",\"dvrProtocolVersion\":\"7\"}}";

        expResponse = "updateSchedule";
        tdkTestObj.executeTestCase(expectedResult);
        actResponse = recorderlib.callServerHandlerWithMsg('updateInlineMessage',jsonMsg,ip);

        if expResponse in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Inline updateSchedule message post success";
		print "Waiting to get acknowledgment status"
		sleep(10);
		retry=0
		actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                while ( ('acknowledgement' not in actResponse) and (retry < 15)):
			sleep(10);
			actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
			retry += 1
		print "Retrieve Status Details: %s"%actResponse;
                if 'acknowledgement' in actResponse:
                	tdkTestObj.setResultStatus("SUCCESS");
                    	print "Successfully retrieved acknowledgement from recorder";
			genOut = recorderlib.readGenerationId(ip)
		    	if genOut == genIdInput:
                    		tdkTestObj.setResultStatus("SUCCESS");
                    		print "GenerationId matches with the expected value ",genIdInput
			
                                response = recorderlib.callServerHandler('clearStatus',ip);
        			jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"dvrProtocolVersion\":\"7\"}}";
			        expResponse = "updateSchedule";
			        tdkTestObj.executeTestCase(expectedResult);
			        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

		        	if expResponse in actResponse:
                			tdkTestObj.setResultStatus("SUCCESS");
			               	print "Legacy updateSchedule message post success";
					genOut = recorderlib.readGenerationId(ip)
					if genOut == genIdInput:
			                        tdkTestObj.setResultStatus("SUCCESS");
				                print "GenerationId matches with the expected value ",genIdInput;
					else:
			        	       	tdkTestObj.setResultStatus("FAILURE");
                			   	print "GenerationId does not match with the expected value ",genIdInput;
				else:
                			tdkTestObj.setResultStatus("FAILURE");
			               	print "Legacy updateSchedule message post failure";
		    	else:
                    		tdkTestObj.setResultStatus("FAILURE");
                                print "GenerationId does not match with the expected value ",genIdInput;
		else:
                	tdkTestObj.setResultStatus("FAILURE");
                    	print "Failed to retrieve acknowledgement from recorder";
        else:
	        tdkTestObj.setResultStatus("FAILURE");
                print "Inline updateSchedule message post failure";
        recObj.unloadModule("Recorder");
