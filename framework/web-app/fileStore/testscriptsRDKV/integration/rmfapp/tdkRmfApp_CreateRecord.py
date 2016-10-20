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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1241</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>tdkRmfApp_CreateRecord</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>582</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TdkRmfApp_CreateRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>8</execution_time>
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
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TdkRmfApp_CreateRecord');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" not in result.upper():
        obj.setLoadModuleStatus("FAILURE");
        exit;

obj.setLoadModuleStatus(result);
print "rmfApp module loading status :%s" %result;

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

streamDetails = tdkTestObj.getStreamDetails('01');

recordtitle = "test_dvr"
recordid = "11111114"
recordduration = "5"
ocapid = streamDetails.getOCAPID();

print recordid
print recordduration
print recordtitle
print ocapid

tdkTestObj.addParameter("recordId",recordid);
tdkTestObj.addParameter("recordDuration",recordduration);
tdkTestObj.addParameter("recordTitle",recordtitle);
tdkTestObj.addParameter("ocapId",ocapid);

expectedresult="SUCCESS"

#Execute the test case in STB
tdkTestObj.executeTestCase(expectedresult);

print "After execution"

#Get the result of execution
result = tdkTestObj.getResult();

if expectedresult in result:
        tdkTestObj.setResultStatus("SUCCESS");
        details=tdkTestObj.getResultDetails();
else:
        tdkTestObj.setResultStatus("FAILURE");
        details=tdkTestObj.getResultDetails();
        obj.unloadModule("rmfapp");
        exit;

duration = int(recordduration)

obj.unloadModule("rmfapp");
