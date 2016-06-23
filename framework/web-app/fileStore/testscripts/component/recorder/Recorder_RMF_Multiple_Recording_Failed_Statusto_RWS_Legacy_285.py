#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ===========================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Multiple_Recording_Failed_Statusto_RWS_Legacy_285</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Recorder should send status to RWS POST URL  when two failed recordings happens back to back after recorder is already retry the connection to Secure HTTPS RWS POST</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>60</execution_time>
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
  <script_tags />
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Multiple_Recording_Failed_Statusto_RWS_Legacy_285');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

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
        response = recorderlib.callServerHandler('clearStatus',ip);

        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Schedule a recording and wait till it is completed
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
           
        #Frame json message to schedule a recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        sleep(70) 
        #rebooting the box so full sync can be avoided in the reboot after https enabled
        recObj.initiateReboot();
        sleep(300);
        response = recorderlib.callServerHandler('clearStatus',ip);
 
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSSecureStatus',ip,'401');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','RWSSecureStatus',ip);

        #To configure ssl cerificate location for dvr simulator
        tdkTestObj = recObj.createTestStep('Recorder_ExecuteCmd');
        expectedResult="SUCCESS";
        tdkTestObj.addParameter("command","sed -i '/FEATURE.RECORDER.AUTHSERVICEURL/ a FEATURE.RECORDER.CACERTIFICATE=/opt/CERT/cacert.crt' /opt/rmfconfig.ini");
        #Execute the test case in STB
        tdkTestObj.executeTestCase("SUCCESS");
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print " Configured self signed certificate for secure LP /RWS communication in /opt/CERT/"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Failed to configure self signed certificate for secure LP /RWS communication in /opt/CERT/"
 
        print "Enable HTTPS Server"
        #Enable HTTPSStatus Server
        actresponse = recorderlib.callServerHandler('enableHTTPS',ip)
        print "HTTPS Status :",actresponse
        recObj.initiateReboot();
        sleep(300);

        if "true" in actResponse:
            #To clear the ocapri log
            tdkTestObj1 = recObj.createTestStep('Recorder_clearOcapri_log');
            tdkTestObj1.executeTestCase(expectedResult);
            result = tdkTestObj1.getResult();
            if "SUCCESS" in result:
                tdkTestObj1.setResultStatus("SUCCESS");
                print "Cleared the ocapri log ";
            else:
                tdkTestObj1.setResultStatus("FAILURE");
                print "Ocapri log is not cleared ";

            requestID = str(randint(10, 500));
            recordingID = str(randint(10000, 500000));
            duration = "60000";
            startTime = "0";
            ocapId = "0x@@";
            now = "curTime"

            #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
 
            sleep(5);
 
            requestID1 = str(randint(10, 500));
            recordingID1 = str(randint(10000, 500000));
            ocapId = "0x@bb";

            #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID1+"\",\"generationId\":\"TDK123\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID1+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID1+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
             
            print "Waiting for fallback to HTTP Connection"
            sleep(200); 
        
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
            print "Retrieve Status Details: %s"%actResponse;
            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
            recordingData1 = recorderlib.getRecordingFromRecId(actResponse,recordingID1)
            print recordingData
            print recordingData1
            if 'NOTFOUND' not in (recordingData and recordingData1):
                key = 'status'
                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                value1 = recorderlib.getValueFromKeyInRecording(recordingData1,key)
                print "key: ",key," value: ",value
                print "Successfully retrieved the recording list from recorder";
                if "FAILED" in (value.upper() and value1.upper()):
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Failed status of both the recordings are available";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed status of both the recordings are NOT available";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve the recording list from recorder";
            
            print "Clearing the RWS Secure Status error"
            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSSecureStatus',ip);

            #To remove the rmfconfig.ini changes
            tdkTestObj = recObj.createTestStep('Recorder_ExecuteCmd');
            tdkTestObj.addParameter("command","sed -i '/FEATURE.RECORDER.CACERTIFICATE/d' /opt/rmfconfig.ini");
            #Execute the test case in STB
            tdkTestObj.executeTestCase("SUCCESS");
            result = tdkTestObj.getResult();
            print "[TEST EXECUTION RESULT] : %s" %result;
            if "SUCCESS" in result:
                tdkTestObj.setResultStatus("SUCCESS");
                print " Reverted self signed certificate for secure LP /RWS communication in /opt/CERT/"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to revert self signed certificate for secure LP /RWS communication in /opt/CERT/"


            print "Disable HTTPS Server"
            #Disable HTTPSStatus Server
            actresponse = recorderlib.callServerHandler('disableHTTPS',ip)
            print "HTTPS Status :",actresponse
            recObj.initiateReboot();
            sleep(300);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Error NOT enabled for RWS Secure Status";
        
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");           
