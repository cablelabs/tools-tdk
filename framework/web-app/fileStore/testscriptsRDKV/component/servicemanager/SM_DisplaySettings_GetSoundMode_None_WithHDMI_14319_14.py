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
  <name>SM_DisplaySettings_GetSoundMode_None_WithHDMI_14319_14</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_GetSupportedAudioModes</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Checks getSoundMode() with no parameter and HDMI connected
  Test Case ID : CT_14319_14</synopsis>
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
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");

#To Check whether HDMI device is connected or not
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'DS_isDisplayConnected');
#Get the result of connection with test component and STB
result = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %result;
dsObj.setLoadModuleStatus(result.upper());

if "SUCCESS" in result.upper():
        isDisplayConnected = "FALSE"
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj);
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj)
                #Calling DS_ManagerDeInitialize to DeInitialize API
                #result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        #dsObj.unloadModule("devicesettings");

        if "FALSE" == isDisplayConnected:
		result = devicesettings.dsManagerDeInitialize(dsObj)
		dsObj.unloadModule("devicesettings");
                print "\nPlease test with HDMI device connected. Exiting....!!!"
                exit()
else:
        exit()

obj.configureTestCase(ip,port,'SM_DisplaySettings_GetSoundMode_None_WithHDMI_14319_14');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult = "SUCCESS"
        #service_name = "DisplaySettings_4"
        service_name = "org.openrdk.DisplaySettings"
        tdkTestObj.addParameter("service_name",service_name);
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        serviceDetail = tdkTestObj.getResultDetails();
        print "[REGISTRATION DETAILS] : %s"%serviceDetail;
        #Check for SUCCESS/FAILURE return value of SM_RegisterService
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Registered %s with serviceManager"%service_name

                tdkTestObj = obj.createTestStep('SM_DisplaySetting_GetSoundMode');
                expectedresult="SUCCESS"

                portName = "";
                tdkTestObj.addParameter("portName", portName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceDetail_none = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] soundmode is: %s"%serviceDetail_none;
                if expectedresult in actualresult:
                        print "SUCCESS: GetSoundMode() successful";
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        print "FAILURE: GetSoundMode() failure";
                        tdkTestObj.setResultStatus("FAILURE");

                portName = "HDMI0";
                tdkTestObj.addParameter("portName", portName);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceDetail_hdmi = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] soundmode is: %s"%serviceDetail_hdmi;
                if expectedresult in actualresult:
                        print "SUCCESS: GetSoundMode(HDMI) successful";
                        tdkTestObj.setResultStatus("SUCCESS");

                        if serviceDetail_none==serviceDetail_hdmi :
                                print "SUCCESS: GetSoundMode(HDMI)==GetSoundMode()";
                                tdkTestObj.setResultStatus("SUCCESS");
                        else:
                                print "FAILURE: GetSoundMode(HDMI)!=GetSoundMode()";
                                tdkTestObj.setResultStatus("FAILURE");

                else:
                        print "FAILURE: GetSoundMode(HDMI) failure";
                        tdkTestObj.setResultStatus("FAILURE");

                #Call ServiceManger - UnregisterService API
                tdkTestObj = obj.createTestStep('SM_UnRegisterService');
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
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");

result = devicesettings.dsManagerDeInitialize(dsObj)
dsObj.unloadModule("devicesettings");           
