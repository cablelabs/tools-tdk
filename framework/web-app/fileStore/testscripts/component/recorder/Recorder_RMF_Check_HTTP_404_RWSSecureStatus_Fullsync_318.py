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
  <name>Recorder_RMF_Check_HTTP_404_RWSSecureStatus_Fullsync_318</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>RWS secure status server should send HTTP 404 when the server is enabled with HTTP 404 error and recorder should send full sync in boot up after falling back to HTTP connection</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_404_RWSSecureStatus_Fullsync_318');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus.upper());

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_404_RWSSecureStatus_Fullsync_318');
MFLoadStatus = obj.getLoadModuleResult();
print "MF module loading status : %s" %MFLoadStatus

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

        tm_ip = recorderlib.get_ip_address('eth0')
                

        #To change the url in rmfconfig.ini
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        Keyword="FEATURE.SECURE_RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="https://"+tm_ip+":8443/DVRSimulator/recorder/secureStatus";
        print "Value" , Value
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details1 = rmfConfObj.getResultDetails();
        print result,","," ",details1
        if "FAILURE" in result:
                print "Failed to change the Secure RWS Status Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the Secure RWS Status Url"
        rmfConfObj.setResultStatus("SUCCESS");

       
        requestID = str(randint(10, 500));
        recordingID = str(randint(10000, 500000));
        duration = "60000";
        startTime = "0";
        ocapId = tdkTestObj.getStreamDetails('01').getOCAPID()
        now = "curTime"
        
        #Frame json message to schedule a recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

        actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
        print "Waiting for the recording to complete"
        sleep(70) 
 
        actResponse = recorderlib.callServerHandlerWithTypeAndError('enableError','RWSSecureStatus',ip,'404');
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

        print "Enable HTTPS Server"
        #Enable HTTPSStatus Server
        actresponse = recorderlib.callServerHandler('enableHTTPS',ip)
        print "HTTPS Status :",actresponse
        #unloading Recorder module
        recObj.unloadModule("Recorder");
        sleep(10);
        #Reboot the STB
        obj.initiateReboot();
        sleep(240);

        #Test component to be tested
        recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
        recObj.configureTestCase(ip,port,'Recorder_RMF_Check_HTTP_404_RWSSecureStatus_Fullsync_318');
        #Get the result of connection with test component and STB
        recLoadStatus = recObj.getLoadModuleResult();
        print "Recorder module loading status : %s" %recLoadStatus;
        recObj.setLoadModuleStatus(recLoadStatus);
   
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        tdkTestObj.executeTestCase(expectedResult);

        if "true" in actResponse:

            print "Checking application log for HTTP error code"
            tdkTestObj2=recObj.createTestStep('Recorder_ExecuteCmd');
            
            tdkTestObj2.addParameter("command","(cat /opt/logs/applications.log; cat /opt/logs/ocapri_log.txt) | grep \"HTTP/1.1 404 Not Found\"");
            #Execute the test case in STB
            tdkTestObj2.executeTestCase("SUCCESS");
            result = tdkTestObj2.getResultDetails();
            print "[TEST EXECUTION RESULT] : %s" %result;
            if result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "HTTP 404 error received ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "HTTP 404 error NOT received "; 

            print "Checking ocapri_log for connection retry request"
            tdkTestObj3=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "Connection to host not successfull waiting for"
            tdkTestObj3.addParameter("pattern",pattern);
            tdkTestObj3.executeTestCase(expectedResult);
            result = tdkTestObj3.getResult();
            details = tdkTestObj3.getResultDetails();
            print result,",Details of log ",details
            if "SUCCESS" in result:
                tdkTestObj3.setResultStatus("SUCCESS");
                print "RWS Secure server connection retry is happening";
            else:
                tdkTestObj3.setResultStatus("FAILURE");
                print "RWS Secure server connection retry is NOT happening";
        
            print "Waiting for fallback to HTTP URL"
            actResponse = recorderlib.callServerHandler('retrieveStatus',ip);
            print "Response after first full sync: " ,actResponse; 
            recordingData = recorderlib.getRecordingFromRecId(actResponse,recordingID)
    	    print recordingData
            if 'NOTFOUND' not in recordingData:        
                tdkTestObj.setResultStatus("SUCCESS");
                print "Full sync successfull and recording details found"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Full sync is NOT successfull"

            actResponse = recorderlib.callServerHandlerWithType('clearError','RWSSecureStatus',ip);

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Error NOT enabled for RWS Secure Status";

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

        #revert the secure rws url
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.SECURE_RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        rmfConfObj.addParameter("Value",details1);
        expectedResult="SUCCESS";
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details = rmfConfObj.getResultDetails();
        print result,","," ",details
        if "FAILURE" in result:
            print "Failed to revert Secure RWS Url"
            rmfConfObj.setResultStatus("FAILURE");
            recObj.unloadModule("Recorder");
            exit();
        print "Reverted the Secure RWS Status Url"
        rmfConfObj.setResultStatus("SUCCESS");

        recObj.initiateReboot();
        obj.resetConnectionAfterReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300);
        
        #unloading Recorder module
        recObj.unloadModule("Recorder");
        obj.unloadModule("mediaframework");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE"); 
