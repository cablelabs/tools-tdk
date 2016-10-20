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
  <id>593</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetblueColor_REMOTE_LED_30</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>77</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetColor</primitive_test_name>
  <!--  -->
  <primitive_test_version>6</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script Sets and gets the Blue Color for the Remote Front panel Indicator
Test Case ID : CT_DS_30</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-4</box_type>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_30');
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
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                tdkTestObj = obj.createTestStep('DS_GetSupportedColors');
                tdkTestObj.addParameter("indicator_name","Remote");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedColors
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported colors";
                        print "%s" %colordetails
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the color list";
                print "SUCCESS :Application successfully initialized with Device Settings library";
                print "0-Blue";
                print "1-Green";
                print "2-Red";
                print "3-Yellow";
                print "4-Orange";
                tdkTestObj = obj.createTestStep('DS_SetColor');
                #setting color parameter value
                color = 0;
                print "Color value set to:%d" %color;
                indicator = "Remote";
                print "Indicator value set to:%s" %indicator;
                tdkTestObj.addParameter("color",color);
                tdkTestObj.addParameter("indicator_name",indicator);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                setColor = "%s" %color;
                list = ['255','65280','16711680','1677184','16747520']
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets and sets the color";
                        print "getColor %s" %colordetails;
                        print "Color to be verified: %s"%list[int(setColor)];
                        #comparing the color before and after setting
                        if list[int(setColor)] in colordetails :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the colors are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the colors are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set color for LED";
                time.sleep(10);
                #calling DS_ManagerDeInitialize to DeInitialize API 
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize 
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
