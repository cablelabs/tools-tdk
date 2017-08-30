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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_HDCPProfile_GetSettopHDCPSupport_20083</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_Generic_CallMethod</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
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
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
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
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script  
import tdklib;  
import devicesettings;
import getImageName;

 
#IP and Port of box, No need to change, 
#This will be replaced with correspoing Box Ip and port while executing script 
ip = <ipaddress> 
port = <port> 
imagename= tdklib.getImageName(ip,port);
print "Image Name: %s" %imagename;
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0"); 

dsObj.configureTestCase(ip,port,'CT_SM_HDCPProfile_GetSettopHDCPSupport_20083');
result = dsObj.getLoadModuleResult(); 
print "[devicesettings LIB LOAD STATUS]  :  %s" %result; 
dsObj.setLoadModuleStatus(result.upper());
 
if "SUCCESS" in result.upper(): 
        isDisplayConnected = "FALSE" 
        result = devicesettings.dsManagerInitialize(dsObj); 
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
        if "SUCCESS" in result: 
                #Check for display connection status 
                isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj) 
        if "FALSE" == isDisplayConnected: 
                result = devicesettings.dsManagerDeInitialize(dsObj) 
                dsObj.unloadModule("devicesettings"); 
                print "\nPlease test with HDMI device connected. Exiting....!!!" 
                exit() 
else: 
        exit()

#Get the result of connection with test component and STB
smobj = tdklib.TDKScriptingLibrary("servicemanager","2.0");
smobj.configureTestCase(ip,port,'CT_SM_HDCPProfile_GetSettopHDCPSupport_20083'); 
result =smobj.getLoadModuleResult(); 
print "[LIB LOAD STATUS]  :  %s" %result; 
if "SUCCESS" in result.upper(): 
        #Set the module loading status 
        smobj.setLoadModuleStatus("SUCCESS");
        tdkTestObj = smobj.createTestStep('SM_RegisterService'); 
        expectedresult = "SUCCESS" 
        service_name = "com.comcast.HDCPProfile" 
        tdkTestObj.addParameter("service_name",service_name); 
        tdkTestObj.executeTestCase(expectedresult); 
        actualresult = tdkTestObj.getResult(); 
        serviceDetail = tdkTestObj.getResultDetails(); 
        print "[REGISTRATION DETAILS] : %s"%serviceDetail; 
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult: 
                tdkTestObj.setResultStatus("SUCCESS"); 
                print "SUCCESS: Registered %s with serviceManager"%service_name
                tdkTestObj = dsObj.createTestStep('SM_SetAPIVersion');
                expectedresult="SUCCESS"
                apiVersion=4;
                tdkTestObj.addParameter("apiVersion",apiVersion);
                tdkTestObj.addParameter("service_name", service_name);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                apiversiondetail =tdkTestObj.getResultDetails();
                print "[EXECUTION DETAILS] APi Version : %s"%apiversiondetail;
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "setApiVersionNumber successfully";
                else:
                        print "setApiVersionNumber failed";
                        tdkTestObj.setResultStatus("FAILURE");
                #Prmitive test case which associated to this Script
 
 
                tdkTestObj = smobj.createTestStep('SM_Generic_CallMethod'); 
                expectedresult="SUCCESS" 
 
                tdkTestObj.addParameter("service_name", service_name); 
                tdkTestObj.addParameter("method_name", "getSettopHDCPSupport"); 
                tdkTestObj.executeTestCase(expectedresult); 
                actualresult = tdkTestObj.getResult(); 
                serviceDetail = tdkTestObj.getResultDetails(); 
                print "[TEST EXECUTION DETAILS] supported ports are: %s"%serviceDetail; 
                #Check for SUCCESS/FAILURE return value of SM_DisplaySetting_SetSoundMode
                if ("AX014" or "AX061") in imagename:
                        if ((expectedresult in actualresult) and ("2.2" in serviceDetail)): 
                                print "SUCCESS:GetSettopHDCPSupport successful"; 
                                tdkTestObj.setResultStatus("SUCCESS"); 
                        else: 
                                print "FAILURE: GetSettopHDCPSupport failure"; 
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        if expectedresult in actualresult:
                                print "SUCCESS:GetSettopHDCPSupport successful"; 
                                tdkTestObj.setResultStatus("SUCCESS"); 
                        else: 
                                print "FAILURE: GetSettopHDCPSupport failure"; 
                                tdkTestObj.setResultStatus("FAILURE");
                                
                #Call ServiceManger - UnregisterService API 
                tdkTestObj = smobj.createTestStep('SM_UnRegisterService'); 
                expectedresult="SUCCESS" 
                tdkTestObj.addParameter("service_name",service_name); 
                tdkTestObj.executeTestCase(expectedresult); 
                actualresult = tdkTestObj.getResult(); 
                serviceDetail = tdkTestObj.getResultDetails(); 
                print "[UNREGISTRATION DETAILS] : %s"%serviceDetail; 
                #Check for SUCCESS/FAILURE return value of SM_UnRegisterService 
                if expectedresult in actualresult: 
                        tdkTestObj.setResultStatus("SUCCESS"); 
                        print "SUCCESS: UnRegistered %s with serviceManager"%service_name 
                else: 
                        tdkTestObj.setResultStatus("FAILURE"); 
                        print "FAILURE: Failed to unRegister service %s"%service_name 
        else: 
                tdkTestObj.setResultStatus("FAILURE"); 
                print "FAILURE: Failed to register service %s"%service_name; 
        #Unload the servicemanager module 
        smobj.unloadModule("servicemanager"); 
else: 
        print"Load module failed"; 
        #Set the module loading status 
        smobj.setLoadModuleStatus("FAILURE"); 
 
result = devicesettings.dsManagerDeInitialize(dsObj) 
dsObj.unloadModule("devicesettings");
