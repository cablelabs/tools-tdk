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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrcMPSink_Video_Volume_07_Emulator</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>289</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_HNSrcMPSink_Video_Volume</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>These Script tests the RDK Mediaframework to get and set of volume in video in HNSrc MPSink pipeline on Emulator platform. Test Case ID: CT_RMF_HNSrcMPSink_58.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>8</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import mediaframework;
import time; 
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_Volume_07');
#Get the result of connection with test component and STB
loadModuleStatus =obj.getLoadModuleResult();
print "Mediaframework module loading status :%s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_HNSrcMPSink_Video_Volume_07');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in loadModuleStatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "Mediaframework module loaded successfully";
	#Prmitive test case which associated to this Script
	tdkTestObj = obj.createTestStep('RMF_HNSrcMPSink_Video_Volume');
        streamDetails = tdkTestObj.getStreamDetails('01'); 
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "PLAY URL : %s" %url;
        tdkTestObj.addParameter("playuri",url);

	volume = 2
	tdkTestObj.addParameter("Volume",volume);

	#Execute the test case in STB
	expectedresult="SUCCESS";
	tdkTestObj.executeTestCase(expectedresult);
	#Get the result of execution
	actualresult = tdkTestObj.getResult();
	
	print "Setting Volume in Video using HNSrc MPSink Pipeline : %s" %actualresult;
	#compare the actual result with expected result
	if expectedresult in actualresult:
		#Set the result status of execution
		tdkTestObj.setResultStatus("SUCCESS");
		print "Setting Volume in Video using HNSrc MPSink Pipeline is success";
		time.sleep(20);
	else:
		tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();  
		print "Failure secnario : %s" %details;
		
	#unloading mediastreamer module
	obj.unloadModule("mediaframework");
else:
	print "Failed to load mediaframework module";
	obj.setLoadModuleStatus("FAILURE");
