'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>396</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>test_newrmf_play</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>207</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Test_newrmf_play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
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
  </box_types>
  <rdk_versions />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","rdk2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'test_newrmf_play');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('Test_newrmf_play');
play_exceptedresult="SUCCESS";

#Execute the test case in STB
tdkTestObj.executeTestCase("play_exceptedresult");


tdkTestObj.executeTestCase(play_expectedresult);
cc_Init_actualresult = tdkTestObj.getResult();
details=tdkTestObj.getResultDetails();
print "play_actualresult  :%s" %play_actualresult; 

#Get the result of execution
result = tdkTestObj.getResult();
print "[TEST EXECUTION RESULT] : %s" %result;

#Set the result status of execution
tdkTestObj.setResultStatus("SUCCESS");

obj.unloadModule("mediaframework");