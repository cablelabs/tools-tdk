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
  <id>1460</id>
  <version>1</version>
  <name>GstPluginRdk_Aesdecrypt_DecryptEnable_Negative</name>
  <primitive_test_id>596</primitive_test_id>
  <primitive_test_name>Gst_Aesdecrypt_DecryptEnable_Property</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective:To set the aesdecrypt plugin property, "decryption-enable" with negative value and should fail to set the value. 
Test CaseID: CT_GST_PLUGINS_RDK_26.
Test Type: Negative.</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_GST_PLUGINS_RDK_26</test_case_id>
    <test_objective>To set the aesdecrypt plugin property, "decryption-enable" with negative value and should fail to set the value.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1/XI3</test_setup>
    <pre_requisite>Gstcheck – g_object_set(),
g_object_get(),</pre_requisite>
    <api_or_interface_used>gpointer object,
Const gchar *property name,
Gboolean value,
NULL</api_or_interface_used>
    <input_parameters>No</input_parameters>
    <automation_approch>1. TM loads gstpluginsrdkTest agent via the test agent.
2. gstpluginsrdkTest agent will call gstcheck tool by passing the value to be set to the property of the gst plugin (aesdecrypt).
3. gstcheck tool sets the property value, and validates it and sends SUCCESS or FAILURE to gstpluginsrdkTest agent.
4. gstpluginsrdkTest agent will send the result back to the TM.
5. Then, TM Unloads gstpluginsrdkTest agent.</automation_approch>
    <except_output>Checkpoint 1. GstCheck should return SUCCESS for success status else FAILURE.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libgstpluginsrdkstub.so</test_stub_interface>
    <test_script>GstPluginRdk_Aesdecrypt_DecryptEnable_Negative</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("gstpluginsrdk","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'GstPluginRdk_Aesdecrypt_DecryptEnable_Negative');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load gstPluginsRdk Module]"
        print "[Exiting the Script]"
        exit();

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('Gst_Aesdecrypt_DecryptEnable_Property');

expectedResult = "FAILURE"

#Set the DecryptEnable_negative
#1 = true, 0 = false
value = -1;
tdkTestObj.addParameter("propValue",value)

#Execute the test case in STB
tdkTestObj.executeTestCase(expectedResult);

#Get the result of execution
result = tdkTestObj.getResult();
print "[TEST EXECUTION RESULT] : %s" %result;
details = tdkTestObj.getResultDetails();
print "[TEST EXCEUTION DETAILS] : %s"%details;

#Negative test case expecting FAILURE
if 'FAILURE' in result:
        tdkTestObj.setResultStatus("SUCCESS");
else:
        tdkTestObj.setResultStatus("FAILURE");

obj.unloadModule("gstpluginsrdk");	
