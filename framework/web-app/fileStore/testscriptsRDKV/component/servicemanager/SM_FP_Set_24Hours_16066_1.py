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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_FP_Set_24Hours_16066_1</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_FP_Set_24_Hour_Clock</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <except_output></except_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
												# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
dsobj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_FP_Set_24Hours_16066_1');
dsobj.configureTestCase(ip,port,'SM_FP_Set_24Hours_16066_1');

loadmodulestatus1 =dsobj.getLoadModuleResult();
#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");
    dsobj.setLoadModuleStatus("SUCCESS");
    result = devicesettings.dsManagerInitialize(dsobj)
    if "SUCCESS" in result.upper():
        
        #calling ServiceManger - registerService API
        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult="SUCCESS"
        serviceName="FrontPanelService";
        tdkTestObj.addParameter("service_name",serviceName);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print "SUCCESS :Application successfully registered a service with serviceManger";
            tdkTestObj = obj.createTestStep('SM_FP_SetAPIVersion');
            expectedresult="SUCCESS"
            apiVersion=5;
            tdkTestObj.addParameter("apiVersion",apiVersion);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            apiversiondetail =tdkTestObj.getResultDetails();
            print "[EXECUTION DETAILS] APi Version : %s"%apiversiondetail;
            print "Registered Service:%s" %serviceName;
            #Prmitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('SM_FP_Set_24_Hour_Clock');
            expectedresult="SUCCESS"
            is_24hour=1;
            tdkTestObj.addParameter("is24hour",is_24hour);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of SM_FP_Set_24Hours
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully set to 24hours";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Application Failed to execute SM_FP_Set24Hour_clock API";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "FAILURE: Application failed to register a service";
        
        result = devicesettings.dsManagerDeInitialize(dsobj)
    print "[TEST EXECUTION RESULT] : %s" %actualresult;
    #Unload the servicemanager module
    obj.unloadModule("servicemanager");
    dsobj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");

					

					
