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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1607</id>
  <version>6</version>
  <name>TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86</name>
  <primitive_test_id>585</primitive_test_id>
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: To fetch Human-readable name associated with this video decoder by querying tr69Hostif through curl.  Query string "Device.Services.STBService.1.Components.VideoDecoder.N.Name". Where N is the value greater than number of VideoDecoderNumberOfEn</synopsis>
.This feature is not implemented inn RDK yet.  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>true</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <test_cases>
    <test_case_id>CT_TR69_86</test_case_id>
    <test_objective>To fetch Human-readable name associated with this video decoder by querying tr69Hostif through curl. 
Query string "Device.Services.STBService.1.Components.VideoDecoder.N.Name". Where N is the value greater than number of VideoDecoderNumberOfEntries.
No set operation avaliable for this parameter.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XI3</test_setup>
    <pre_requisite/>
    <api_or_interface_used>curl -d '{"paramList" : [{"name" : "Device.Services.STBService.1.Components.VideoDecoder.N.Name”}]}' http://127.0.0.1:10999</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. TM loads tr69Test agent via the test agent.
2. Tr69Test agent will frame the curl request message 
"Device.Services.STBService.1.Components.VideoDecoder.N.Name" to fetch Human-readable name associated with this video decoder.
3. Tr69Test agent will get the curl response which be a Empty string on SUCCESS.
4. If tr69Test agent will get the string as curl response, if FAILURE.
5. TM Unloads tr69Test agent.</automation_approch>
    <except_output>Checkpoint 1. Need to get Empty string value on SUCCESS. String value on FAILURE.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtr69stub.so</test_stub_interface>
    <test_script>TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86</test_script>
    <skipped>Yes</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
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
obj.configureTestCase(ip,port,'TR069_Get_DeviceSevicesSTBServiceComponentsVideoDecoderName_Neg_86');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load Tr069 Module]"
        print "[Exiting the Script]"
        exit();

#Parameter is the profile path to be queried
profilePath = "Device.Services.STBService.1.Components.VideoDecoderNumberOfEntries"

actualresult,tdkTestObj,details = tdklib.Create_ExecuteTestcase(obj,'Tr069_Get_Profile_Parameter_Values', 'SUCCESS',verifyList ={},path = profilePath);

if "\"" in details:
        details = details[2:-1]
print "[TEST EXCEUTION DETAILS] : %s"%details;

if 0 == len(details):
        print "Failed to fetch the Name Associated with the Video decoder"
else:
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Tr069_Get_Profile_Parameter_Values');

        number = int(details)
        print "Total Number of entries in the VideoDecoder: ",number
        number = number + 1
        profilePath = "Device.Services.STBService.1.Components.VideoDecoder." + str(number) + ".Name"

        tdkTestObj.addParameter("path",profilePath)

        #Execute the test case in STB
        tdkTestObj.executeTestCase(actualresult);

        print "Requested Parameter: ",profilePath
        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        if "\"" in details:
                details = details[2:-1]
        print "[TEST EXCEUTION DETAILS] : %s"%details;

        expectedOutput = " "
        print "[EXPECTED VALUES] : [Empty String]",expectedOutput

        if len(details) == len(expectedOutput):
                tdkTestObj.setResultStatus("SUCCESS");
                print "Success"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Failure"

obj.unloadModule("tr069module");
