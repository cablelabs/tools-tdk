##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_Configure_WrongRWSUrl_Rmfconfig_255</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_Recoder_DVR_Protocol_255 - Check the error code after Bad RWS URL configured in the rmfconfig.ini</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>90</execution_time>
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
recObj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSUrl_Rmfconfig_255');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSUrl_Rmfconfig_255');
MFLoadStatus = obj.getLoadModuleResult();
print "MF module loading status : %s" %MFLoadStatus

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper() and "SUCCESS" in MFLoadStatus.upper() :

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
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.GET.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://96.114.220.106:8080/DVRSimulator/wrongRWS";
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

        Keyword="FEATURE.SECURE_RWS.GET.URL";
        rmfConfObj.addParameter("Keyword",Keyword);
        Value="http://96.114.220.106:8080/DVRSimulator/wrongRWS";
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
        sleep(10);      
 
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

        #unloading Recorder module
        recObj.unloadModule("Recorder");
        sleep(30);
        #Reboot the STB
        obj.initiateReboot();
        print "Sleeping to wait for the recoder to be up"
        sleep(300); 
   
        #Test component to be tested
        recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
        recObj.configureTestCase(ip,port,'Recorder_RMF_Configure_WrongRWSUrl_Rmfconfig_255');
        #Get the result of connection with test component and STB
        recLoadStatus = recObj.getLoadModuleResult();
        print "Recorder module loading status : %s" %recLoadStatus;
        recObj.setLoadModuleStatus(recLoadStatus);
       
        print "Checking ocapri_log" 
        tdkTestObj2=recObj.createTestStep('Recorder_checkOcapri_log');
        pattern = "RDK-10028"
        tdkTestObj2.addParameter("pattern",pattern);
        tdkTestObj2.executeTestCase(expectedResult);  
        result = tdkTestObj2.getResult();
        details = tdkTestObj2.getResultDetails();

        loop=0
        while (('SUCCESS' not in result) and (loop < 10)):
            sleep(400);
            tdkTestObj2.executeTestCase(expectedResult);
            result = tdkTestObj2.getResult();
            details = tdkTestObj2.getResultDetails();
            loop = loop+1;

        print result,",Details of log ",details
        if "SUCCESS" in result:
            tdkTestObj2.setResultStatus("SUCCESS");
            print "Error Log RDK-10028 for RWS server connection lost is found ";
        else:
            tdkTestObj2.setResultStatus("FAILURE");
            print "Error Log RDK-10028 for RWS server connection lost is NOT found "; 
       
        rmfConfObj = recObj.createTestStep('Recorder_SetValuesInRmfconfig');
        expectedResult="SUCCESS";
        #Set 2 parameters
        Keyword="FEATURE.RWS.GET.URL";
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

        Keyword="FEATURE.SECURE_RWS.GET.URL";
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

        #unloading Recorder module
        recObj.unloadModule("Recorder");
        obj.unloadModule("mediaframework");
else:
    print "Failed to load Recorder module";
    #Set the module loading status
    recObj.setLoadModuleStatus("FAILURE"); 
