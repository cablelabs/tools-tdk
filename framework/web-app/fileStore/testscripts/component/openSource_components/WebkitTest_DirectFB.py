'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>185</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>WebkitTest_DirectFB</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>53</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>OpenSource_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script will execute webkit test suite.
This test script will be applicable to XI3 with RDK version 1.2 running boxes. And display option used as directfb.</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#Use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("opensourcetestsuite","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'WebkitTest');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
if "Success" in result:
  print "Opensource test module successfully loaded";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");
  
  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('OpenSource_Comp_Test');

  # Configuring the test object for webkit test suites execution
  tdkTestObj.addParameter("Opensource_component_type","webkit");
  tdkTestObj.addParameter("Display_option","directfb");

  #Execute the test case in STB
  expectedresult="Test Suite Executed"
  tdkTestObj.executeTestCase(expectedresult);

  #Get the result of execution
  actualresult = tdkTestObj.getResult();
  print "Webkit Test Results : %s" %actualresult;

  #To Validate the Execution of Test Suites 
  details = tdkTestObj.getResultDetails();
  if "TotalSuite" in details:
    print "Webkit status details : %s" %details;
    details=dict(item.split(":") for item in details.split(" "))
    Resultvalue=details.values();
    if int(Resultvalue[0])==(int(Resultvalue[1])+int(Resultvalue[2])) and int(Resultvalue[2])==0 and expectedresult in actualresult :
       tdkTestObj.setResultStatus("SUCCESS");
    else:
       tdkTestObj.setResultStatus("FAILURE");
     
    #Get the log path of the webkit Testsuite
    logpath =tdkTestObj.getLogPath();
    if "TestSummary.log" in logpath:
       print "Log Path :%s"%logpath;
       #Transferring the webkit Testsuite Logs
       tdkTestObj.transferLogs( logpath, "true" );
    else:
       print "Log path is not available and transfer of logs will not be initialised";
  else :
     print " Webkit status details:%s" %details;
     print "Proper Execution details are not received due to error in execution ";
     tdkTestObj.setResultStatus("FAILURE");
	 
  #Unloading the opensource test suite module
  obj.unloadModule("opensourcetestsuite");

else:
  print "Failed to load Opensource test module";
  #Set the module loading status
  obj.setLoadModuleStatus("FAILURE");