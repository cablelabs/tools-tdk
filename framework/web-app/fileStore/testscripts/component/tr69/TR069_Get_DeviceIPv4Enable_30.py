'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1343</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TR069_Get_DeviceIPv4Enable_30</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>585</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To fetch  the status (enabled/disabled) of the IPv4 stack on a device by querying tr69Hostif through curl.  Query string "Device.IP.IPv4Enable".  
TestCaseID: CT_TR69_30
TestType: Positive</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tr069module","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TR069_Get_DeviceIPv4Enable_30');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load Tr069 Module]"
        print "[Exiting the Script]"
        exit();

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('Tr069_Get_Profile_Parameter_Values');

expectedResult = "SUCCESS"

#Parameter is the profile path to be queried
profilePath = "Device.IP.IPv4Enable"
tdkTestObj.addParameter("path",profilePath)

#Execute the test case in STB
tdkTestObj.executeTestCase(expectedResult);

print "Requested Parameter: ",profilePath
#Get the result of execution
result = tdkTestObj.getResult();
print "[TEST EXECUTION RESULT] : %s" %result;
details = tdkTestObj.getResultDetails();
if "\"" in details:
        details = details[2:-1]
print "[TEST EXCEUTION DETAILS] : %s"%details;

if "Empty" not in details: 
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Tr069_Verify_Profile_Parameter_Values');

        expectedResult = "SUCCESS"

        #Parameter is the profile path to be queried
        tdkTestObj.addParameter("path",profilePath)
        tdkTestObj.addParameter("paramValue",details)

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        
        print "Requested Parameter To Verify: ",profilePath
        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        print "[TEST EXCEUTION DETAILS] : %s"%details;

        tdkTestObj.setResultStatus(result);
else:
        tdkTestObj.setResultStatus(result);

obj.unloadModule("tr069module");	