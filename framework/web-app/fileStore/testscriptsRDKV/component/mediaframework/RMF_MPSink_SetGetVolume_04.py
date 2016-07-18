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
  <id>453</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MPSink_SetGetVolume_04</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>279</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_MPSink_SetGetVolume</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>These Script tests the RDK Mediaframework MPSink element to Set and get Volume.
Test Case ID: CT_RMF_MPSink_04</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>6</execution_time>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
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
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_MPSink_SetGetVolume_04');
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
                obj.configureTestCase(ip,port,'RMF_MPSink_SetGetVolume_04');
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
        tdkTestObj = obj.createTestStep('RMF_MPSink_SetGetVolume');
        #Execute the test case in STB
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        #details = tdkTestObj.getResultDetails();
        print "MPSink initialized and Terminated : %s" %actualresult;
        #compare the actual result with expected result
        if expectedresult in actualresult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print "MPSink Volume setted Successfully";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                #print "Failure secnario : %s" %details;
                print "Failed to do volume setting MPSink";
        #unloading mediastreamer module
        obj.unloadModule("mediaframework");
else:

        print "Failed to load mediaframework module";
        obj.setLoadModuleStatus("FAILURE");
