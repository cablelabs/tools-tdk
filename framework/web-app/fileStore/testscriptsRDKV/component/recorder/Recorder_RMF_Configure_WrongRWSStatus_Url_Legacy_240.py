#  ============================================================================
#  COMCAST CONFIDENTIAL AND PROPRIETARY
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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Configure_WrongRWSStatus_Url_Legacy_240</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_240 - Recorder- To check whether recorder sends error or not for  the loss of connection with RWS Status Server</synopsis>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSStatus_Url_Legacy_240');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSStatus_Url_Legacy_240');
MFLoadStatus = obj.getLoadModuleResult();
print "MF module loading status : %s" %MFLoadStatus


#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);

	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
            recObj.initiateReboot();
	    sleep(300);
	    print "Sleeping to wait for the recoder to be up"

        #To clear all the alternate URL's set for Servers
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','LPServer',ip);
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','RWSServer',ip);
        actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','RWSStatus',ip);       
        print "Cleared all alternate URL's set in Servers";

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);
        #configure DVRSimulator to send bad Long Poll URL from Long Poll end point
        actResponse = recorderlib.callServerHandlerWithTypeAndNewUrl('configureAlternateURL','RWSStatus',ip,'wrongRWSStatus');
        #Checking whether alternate wrong url is configured or not
        actResponse = recorderlib.callServerHandlerWithType('isAlternateURLEnabled','RWSStatus',ip);
        print actResponse; 

        #Primitive test case which associated to this script
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://96.114.220.106:80/DVRSimulator/wrongRWSStatus";
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details1 = rmfConfObj.getResultDetails();
        print result,","," ",details1
        if "FAILURE" in result:
                print "Failed to change the RWS Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the RWS Url"
        rmfConfObj.setResultStatus("SUCCESS");

        Keyword="FEATURE.SECURE_RWS.POST.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://96.114.220.106:80/DVRSimulator/wrongRWSStatus";
        rmfConfObj.addParameter("Value",Value);
        #Execute the test case in STB
        rmfConfObj.executeTestCase(expectedResult);
        #Get the actual result and details of execution
        result = rmfConfObj.getResult();
        details2 = rmfConfObj.getResultDetails();
        print result,","," ",details1
        if "FAILURE" in result:
                print "Failed to change the RWS Secure Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
        print "Changed the RWS Secure Url"
        rmfConfObj.setResultStatus("SUCCESS");

        if "wrongRWSStatus" in actResponse:
            tdkTestObj.setResultStatus("SUCCESS");
            print "Alternate URL enabled for RWS Status server";

            tdkTestObj1 = recObj.createTestStep('Recorder_clearOcapri_log');
            tdkTestObj1.executeTestCase(expectedResult);
            result = tdkTestObj1.getResult();
            if "SUCCESS" in result:
                tdkTestObj1.setResultStatus("SUCCESS");
                print "Cleared the ocapri log ";
            else:
                tdkTestObj1.setResultStatus("FAILURE");
                print "Ocapri log is not cleared ";
    
            #unloading Recorder module
            recObj.unloadModule("Recorder");
            sleep(30);
            #Reboot the STB
            obj.initiateReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);
        
            #Test component to be tested
            recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
            recObj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSStatus_Url_Legacy_240');
            #Get the result of connection with test component and STB
            recLoadStatus = recObj.getLoadModuleResult();
            print "Recorder module loading status : %s" %recLoadStatus;
            recObj.setLoadModuleStatus(recLoadStatus);
            tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
            tdkTestObj.executeTestCase(expectedResult);

            requestID = str(randint(10, 500));
            recordingID = str(randint(10000, 500000));
            duration = "60000";
            startTime = "0";
            ocapId = "0x@@";
            now = "curTime"
           
            #Frame json message
            jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"generationId\":\"TDK123\",\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"Recording_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\"P3\"}]}}";

            actResponse = recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip);
            print "Checking ocapri_log"
            tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
            pattern = "RDK-10028"
            tdkTestObj2.addParameter("pattern",pattern);
            tdkTestObj2.executeTestCase(expectedResult);  
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            
            loop=0
            while (('SUCCESS' not in result) and (loop < 5)):
                sleep(300);
                tdkTestObj2.executeTestCase(expectedResult);
                result = tdkTestObj2.getResult();
                details = tdkTestObj2.getResultDetails();
                loop = loop+1;
            print result,",Details of log ",details

            if "SUCCESS" in result:
                tdkTestObj2.setResultStatus("SUCCESS");
                print "Error Log RDK-10028 for RWS Status server connection lost is found ";
            else:
                tdkTestObj2.setResultStatus("FAILURE");
                print "Error Log RDK-10028 for RWS Status server connection lost is NOT found "; 
            
            #To clear the wrong RWS Status Server Url
            actResponse = recorderlib.callServerHandlerWithType('clearAlternateURL','RWSStatus',ip);
            print actResponse;
            if "cleared" in actResponse:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Alternate URL of RWSStatus server reverted";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Alternate URL of RWSStatus server is not reverted";
     
            rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
            expectedResult="SUCCESS";
            #Set 2 parameters
            Keyword="FEATURE.RWS.POST.URL";
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
                print "Failed to revert the RWS Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
            print "Reverted the RWS Url"
            rmfConfObj.setResultStatus("SUCCESS");

            Keyword="FEATURE.SECURE_RWS.POST.URL";
            rmfConfObj.addParameter("Keyword",Keyword);
            rmfConfObj.addParameter("Value",details2);
            expectedResult="SUCCESS";
            #Execute the test case in STB
            rmfConfObj.executeTestCase(expectedResult);
            #Get the actual result and details of execution
            result = rmfConfObj.getResult();
            details = rmfConfObj.getResultDetails();
            print result,","," ",details
            if "FAILURE" in result:
                print "Failed to revert the Secure RWS Url"
                rmfConfObj.setResultStatus("FAILURE");
                recObj.unloadModule("Recorder");
                exit();
            print "Reverted the RWS Secure Url"
            rmfConfObj.setResultStatus("SUCCESS");

            recObj.initiateReboot();
            obj.resetConnectionAfterReboot();
            print "Sleeping to wait for the recoder to be up"
            sleep(300);

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Alternate URL NOT enabled for RWS Status server";

        #unloading Recorder module
        recObj.unloadModule("Recorder");
        obj.unloadModule("mediaframework");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE"); 
