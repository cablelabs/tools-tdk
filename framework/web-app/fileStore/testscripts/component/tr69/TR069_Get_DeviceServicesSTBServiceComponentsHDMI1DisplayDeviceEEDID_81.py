'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1558</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceEEDID_81</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>585</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To fetch the Enhanced Extended Display Information Data (E-EDID) retrieved from the connected HDMI device by querying tr69Hostif through curl.  Query string "Device.Services.STBService.1.Components.HDMI.1.DisplayDevice.EEDID". No set operation avaliable f</synopsis>
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
    <box_type>IPClient-4</box_type>
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
obj.configureTestCase(ip,port,'TR069_Get_DeviceServicesSTBServiceComponentsHDMI1DisplayDeviceEEDID_81');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load Tr069 Module]"
        print "[Exiting the Script]"
        exit();

#Parameter is the profile path to be queried
profilePath = "Device.Services.STBService.1.Components.HDMI.1.DisplayDevice.EEDID"

actualresult,tdkTestObj,details = tdklib.Create_ExecuteTestcase(obj,'Tr069_Get_Profile_Parameter_Values', 'SUCCESS',verifyList ={},path = profilePath);

if "\"" in details:
        details = details[2:-1]

if 0 == len(details):
        print "[TEST EXCEUTION DETAILS] : [%sEmpty]"%details;
        print "[PRE-REQUSITE] Please!!!! Connect the HDMI Cable from STB to TV to fetch the value before testing";
        tdkTestObj.setResultStatus("FAILURE");
else:
        print "[TEST EXCEUTION DETAILS] : %s"%details;
        tdkTestObj.setResultStatus(actualresult);

obj.unloadModule("tr069module");
