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
  <name>Recorder_RMF_SixTuner_DVR_Seven_Recordings_13</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder-To check scheduling seven consecutive current recording. </synopsis>
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
from trm import getMaxTuner


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_SixTuner_DVR_Seven_Recordings_13');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
trmObj.configureTestCase(ip,port,'Recorder_RMF_SixTuner_DVR_Seven_Recordings_13');
#Get the result of connection with test component and STB
result = trmObj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
trmObj.setLoadModuleStatus(result);

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    trmObj.initiateReboot();
    trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
    trmObj.configureTestCase(ip,port,'Recorder_RMF_SixTuner_DVR_Seven_Recordings_13');
    #Get the result of connection with test component and STB
    result = trmObj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;
    trmObj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);
        loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
               sleep(300);

        #Giving no update here to get the recording list in case the previous generation id is set to zero before reboot
	jsonMsgNoUpdate = "{\"noUpdate\":{}}";        
        actResponse =recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgNoUpdate,ip);
 	print "No Update Schedule Details: %s"%actResponse;
	sleep(60);

        #Pre-requisite to clear any recording status
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
        duration = "120000";
        startTime = "0";
        now = "curTime"

        tdkTestObj.executeTestCase(expectedResult);

        maxTuner = getMaxTuner(trmObj,'SUCCESS')
        if ( 0 == maxTuner ):
                print "Invalid number of tuners"
        else:
                print "MaxTuner: %d"%maxTuner;
                for deviceNo in range(0,maxTuner):
                	Id = '0'+str(deviceNo+1)
	                recId = str(randint(10000, 500000));
			streamId = tdkTestObj.getStreamDetails(Id).getOCAPID()

	                #Frame json message
        	        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recId+"\",\"locator\":[\"ocap://"+streamId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recId+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                	expResponse = "updateSchedule";
                	tdkTestObj.executeTestCase(expectedResult);
               		actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
                	print "Update Schedule Details: %s"%actResponse;

                if expResponse in actResponse:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "updateSchedule message post success";
                        print "Wait for 60s to get acknowledgement"
                        sleep(20);
                        #Check for acknowledgement from recorder
                        tdkTestObj.executeTestCase(expectedResult);
                        print "Looping till acknowledgement is received"
                        loop = 0;
                        while loop < 5:
                                actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                print "Retrieve Status Details: %s"%actResponse;
                                sleep(10);
                                loop = loop+1;
                        if 'acknowledgement' in actResponse:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "Successfully retrieved acknowledgement from recorder";
                            print "Wait for 60s for the recording to be completed"

                            #Frame json message for update recording
                            Id = '0'+str(maxTuner+1)
                            ocapId = tdkTestObj.getStreamDetails(Id).getOCAPID()

                            jsonMsgFullSchedule = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

                            expResponse = "updateSchedule";
                            tdkTestObj.executeTestCase(expectedResult);
                            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgFullSchedule,ip);
                            print "updateSchedule Details for rescheduling: %s"%actResponse;
                            if expResponse in actResponse:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "updateSchedule message post success";
                                print "Wait for 60s to get acknowledgement"
                                sleep(120);
                                #Check for acknowledgement from recorder
                                tdkTestObj.executeTestCase(expectedResult);
                                print "Looping till acknowledgement is received"
                                loop = 0;
                                while loop < 5:
                                        actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
                                        print "Retrieve Status Details: %s"%actResponse;
                                        sleep(10);
                                        loop = loop+1;
                                if 'acknowledgement' in actResponse:
                                        print "Successfully retrieved acknowledgement from recorder";
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "Failed to retrieve acknowledgement from recorder";
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "Failed to retrieve acknowledgement from recorder";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "updateSchedule message post failed";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
        trmObj.unloadModule("trm");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
