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
  <id>1592</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Brightness_Persistent_116</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>76</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that Front Panel power brightness value is persisted after STB reboot.
TestcaseID: CT_DS116</synopsis>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_Brightness_Persistent_116');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling Device Settings - Set/Get Brightness
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                #setting brightness parameter value
                brightness = 5;
                print "Setting brightness to %d" %brightness;
                indicator_name = "Power";
                print "Setting Indicator name to %s" %indicator_name;
                tdkTestObj.addParameter("brightness",brightness);
                tdkTestObj.addParameter("indicator_name",indicator_name);
                tdkTestObj.addParameter("get_only",0);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS SetBrightness RESULT] : %s" %actualresult;
                getBrightness = tdkTestObj.getResultDetails();
                setBrightness = "%s" %brightness;
                print "getBrightness:%s" %getBrightness;
                #Check for SUCCESS/FAILURE return value of DS_SetBrightness
                if expectedresult in actualresult:
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Get Brightness equal to Set Brightness";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Get Brightness not equal to Set Brightness";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set Brightness for LED";
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        # Reboot the box
        obj.initiateReboot();

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling Device Settings - Get Indicator Brightness
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                print "Brightness before reboot: %d" %brightness;
                print "Indicator name: %s" %indicator_name;
                tdkTestObj.addParameter("indicator_name",indicator_name);
                tdkTestObj.addParameter("get_only",1);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS GetBrightness RESULT] : %s" %actualresult;
                getBrightness = tdkTestObj.getResultDetails();
                print "Brightness after reboot:%s" %getBrightness;
                #Check for SUCCESS/FAILURE return value of DS_SetBrightness
                if expectedresult in actualresult:
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Brightness same after reboot";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Brightness changed after reboot";

                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
