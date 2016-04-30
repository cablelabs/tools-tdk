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
  <id>954</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_rmfapp_record_and_quit</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>512</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>E2E_rmfapp_record_url</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>E2E_rmfapp_record_and_quit: To initiate the recording from rmfApp.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_rmfapp_record_and_quit');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper():
    print "rmf app module loaded successfully"
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('E2E_rmfapp_record_url');
    
    streamDetails = tdkTestObj.getStreamDetails('01');

    cmd = 'record -id 11770011 -duration 1 -title test_dvr http://' + streamDetails.getGatewayIp() + ':8080/vldms/tuner?ocap_locator=ocap://' + streamDetails.getOCAPID();

    print streamDetails.getOCAPID()

    print "Request record URL : %s" %cmd;
    tdkTestObj.addParameter("rmfapp_command",cmd);

    expectedresult="Test Suite Executed"

    print "Sending command to CLI interface of application..."

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;

    if expectedresult in result:
        tdkTestObj.setResultStatus("SUCCESS");
        print "SUCCESS: command was processed by rmfApp application."
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details=tdkTestObj.getResultDetails();
        print "FAILURE: rmfApp failed. Details: %s" %details;

    time.sleep(60) #delay so that playback can be observed.

    logpath =tdkTestObj.getLogPath();
    print "Log Path :%s"%logpath;

    if ".log" in logpath:
       #Transferring the application logs
       tdkTestObj.transferLogs( logpath, "false" );
    else:
       print "Log path is not available and transfer of logs will not be initialised";

    obj.unloadModule("rmfapp");

else:
    print "Failed to load rmfapp module"
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
