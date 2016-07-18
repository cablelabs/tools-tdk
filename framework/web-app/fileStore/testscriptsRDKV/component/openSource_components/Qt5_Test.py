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
  <id>336</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Qt5_Test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>53</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>OpenSource_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script will execute qt5 non-graphics and graphics test suite.
This test script will be applicable to XG1 with RDK version 1.3 running boxes with qt5 used.</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#Use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("opensourcetestsuite","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Qt5Test');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
if "Success" in result:
  print "Opensource test module successfully loaded";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");

  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('OpenSource_Comp_Test');

  # Configuring the test object for qt5 test suites execution 
  tdkTestObj.addParameter("Opensource_component_type","qt5");

  #Execute the test case in STB
  Qt5_Expectedresult="Test Suite Executed"
  tdkTestObj.executeTestCase(Qt5_Expectedresult);

  #Get the result of execution
  Qt5_result = tdkTestObj.getResult();
  print "%s" %Qt5_result;
    
  #To Validate the Execution of Test Suites 
  details = tdkTestObj.getResultDetails();
  if "TotalSuite" in details:
     print "Qt5  Execution status details : %s" %details;
     details=dict(item.split(":") for item in details.split(" "))
     Resultvalue=details.values();
     #Printing the results of Qt5 Test suite
     print "Expected result:%s" %Qt5_Expectedresult;
     print "Actual result:%s" %Qt5_result;
     if int(Resultvalue[0])==(int(Resultvalue[1])+int(Resultvalue[2])) and int(Resultvalue[2])==0 and Qt5_Expectedresult in Qt5_result:
        tdkTestObj.setResultStatus("SUCCESS");
     else:
         tdkTestObj.setResultStatus("FAILURE");
          
     #Get the log path of the Qt Graphics Testsuite
     logpath =tdkTestObj.getLogPath();
     if "TestSummary.log" in logpath:
        print "Log Path :%s"%logpath;
        #Transferring the Qt 5 Testsuite Logs
        tdkTestObj.transferLogs( logpath, "true" );
     else:
        print "Log path is not available and transfer of logs will not be initialised";
  else :
     print " Qt5 status details:%s" %details;
     print "Proper Execution details are not received due to error in execution ";
     tdkTestObj.setResultStatus("FAILURE");
	   
  #Unloading the opensource test suite module
  obj.unloadModule("opensourcetestsuite");

else:
  print "Failed to load Opensource test module";				
  #Set the module loading status
  obj.setLoadModuleStatus("FAILURE");