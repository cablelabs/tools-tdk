'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>187</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>QtTest_DirectFB</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>53</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>OpenSource_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script will execute qt non-graphics and qt graphics test suites.
This test script will be applicable to XI3 boxes and only for RDK version 1.2 running boxes. And display option given as directfb.</synopsis>
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
obj.configureTestCase(ip,port,'QtTest');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
if "Success" in result:
  print "Opensource test module successfully loaded";
  #Set the module loading status
  obj.setLoadModuleStatus("SUCCESS");

  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('OpenSource_Comp_Test');

  # Configuring the test object for non gfx qt test suites execution 
  tdkTestObj.addParameter("Opensource_component_type","qt_non_gfx");

  #Execute the test case in STB
  NonGfx_Expectedresult="Test Suite Executed"
  tdkTestObj.executeTestCase(NonGfx_Expectedresult);

  #Get the result of execution
  NonGfx_result = tdkTestObj.getResult();
    
  #To Validate the Execution of Test Suites 
  details = tdkTestObj.getResultDetails();
  if "TotalSuite" in details:
    print " Qt Non Graphics Execution status details : %s" %details;
    details=dict(item.split(":") for item in details.split(" "))
    Resultvalue=details.values();
         
    #Get the log path of the Qt Non-Graphics Testsuite
    logpath =tdkTestObj.getLogPath();
    if "TestSummary.log" in logpath:
       print "Log Path :%s"%logpath;
       #Transferring the Qt Non-Graphics Testsuite Logs
       tdkTestObj.transferLogs( logpath, "true" );
    else:
       print "Log path is not available and transfer of logs will not be initialised";
  else :
     print " Qt Non-Graphics status details:%s" %details;
     print "Proper Execution details are not received due to error in execution";
     tdkTestObj.setResultStatus("FAILURE");
  
  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('OpenSource_Comp_Test');

  # Configuring the test object for gfx test suites execution
  tdkTestObj.addParameter("Opensource_component_type","qt_gfx");
  tdkTestObj.addParameter("Display_option","directfb");
  
  #Execute the test case in STB
  GFX_Expectedresult="Test Suite Executed"
  tdkTestObj.executeTestCase(GFX_Expectedresult);

  #Get the result of execution
  GFX_result = tdkTestObj.getResult();
  
  #To Validate the Execution of Test Suites 
  details_Graphics = tdkTestObj.getResultDetails();
  if "TotalSuite" in details_Graphics:
    print "Qt Graphics Execution status details : %s" %details_Graphics;
    details_Graphics=dict(item.split(":") for item in details_Graphics.split(" "))
    Resultvalue_Graphics=details_Graphics.values();
         
    #Get the log path of the Qt Graphics Testsuite
    logpath =tdkTestObj.getLogPath();
    if "TestSummary.log" in logpath:
       print "Log Path :%s"%logpath;
       #Transferring the Qt Graphics Testsuite Logs
       tdkTestObj.transferLogs( logpath, "true" );
    else:
       print "Log path is not available and transfer of logs will not be initialised";
  else :
     print " Qt Graphics status details:%s" %details;
     print "Proper Execution details are not received due to error in execution";
     tdkTestObj.setResultStatus("FAILURE");
	 
  #Printing the results of both Graphics and Non-Graphics
  print "gfx actual%s" %GFX_result;
  print "gfx expected:%s" %GFX_Expectedresult;
  print "non gfx exp:%s" %NonGfx_Expectedresult;
  print "non gfx actual%s" %NonGfx_result;
  
  if int(Resultvalue[0])==(int(Resultvalue[1])+int(Resultvalue[2])) and int(Resultvalue[2])==0 and int(Resultvalue_Graphics[0])==(int(Resultvalue_Graphics[1])+int(Resultvalue_Graphics[2])) and int(Resultvalue_Graphics[2])==0 and NonGfx_Expectedresult in NonGfx_result and GFX_Expectedresult in GFX_result :
     tdkTestObj.setResultStatus("SUCCESS");
  else:
     tdkTestObj.setResultStatus("FAILURE");
  
  #Unloading the opensource test suite module
  obj.unloadModule("opensourcetestsuite");

else:
  print "Failed to load Opensource test module";
  #Set the module loading status
  obj.setLoadModuleStatus("FAILURE");