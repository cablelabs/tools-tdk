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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Check_HTTP_404_LPSecureServer_Legacy_307</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Long poll secure server should send HTTP 404 when server is enabled with HTTP 404 error and after clearing the error  legacy recording should get complete</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_404_LPSecureServer_Legacy_307');
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

        #Pre-requisite
        response = recorderlib.callServerHandler('clearStatus',ip);
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
 
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','LPSecureServer',ip,'404');
        print "Enable error :", actResponse
        actResponse = recorderlib.callServerHandlerWithType('isEnabledError','LPSecureServer',ip);

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
        
            # Reboot the STB
            print "Rebooting the STB"
            recObj.initiateReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);

            requestID = str(randint(10, 500));
            recordingID = str(randint(10000, 500000));
            duration = "60000";
            startTime = "0";
            ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
            now = "curTime"
           
            #Frame json message to schedule a recording
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);

            print "Checking ocapri_log for HTTP error code"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "Received HTTP response code: 404"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "HTTP 404 error received ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "HTTP 404 error NOT received "; 
            
            print "Checking ocapri_log for retry request"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "NULL data from long poll.  Restarting request after"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Longpoll secure server connection retry is happening";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Longpoll secure server connection retry is NOT happening";

            print "Clear the Longpoll secure server error"
            actResponse = recorderlib.callServerHandlerWithType('clearError','LPSecureServer',ip);
            print "Waiting for the connection re-establishment and recording to get compeleted"
            sleep(180);

            tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
            tdkTestObj.executeTestCase(expectedResult);
            print "Sending getRecordings to get the recording list"
            recorderlib.callServerHandler('clearStatus',ip)
            recorderlib.callServerHandlerWithMsg('updateMessage','{\"getRecordings\":{}}',ip)
            print "Wait for 1 min to get response from recorder"
            sleep(60)
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip)
            print "Recording List: %s" %actResponse;
            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
            print recordingData
            if 'NOTFOUND' not in recordingData:
                key = 'status'
                value = recorderlib.getValueFromKeyInRecording(recordingData,key)
                print "key: ",key," value: ",value
                print "Successfully retrieved the recording list from recorder";
                if "COMPLETE" in value.upper():
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Recording completed successfully";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Recording NOT completed successfully";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failed to retrieve the recording list from recorder";

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
            print "Error NOT enabled for Long poll secure server";
        
        #unloading Recorder module
        recObj.unloadModule("Recorder");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE");
