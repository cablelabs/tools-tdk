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
  <id>665</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Resolution_1080i50_test_90</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>83</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the 1080i50 Resolution of Video Output Port
Test Case ID:CT_DS_90.
Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
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
obj.configureTestCase(ip,port,'CT_DS_90');
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
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                    tdkTestObj.setResultStatus("SUCCESS");
                    #calling DS_Resolution get list of support.ed resolutions and the default resolution
                    tdkTestObj = obj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    resolutiondetails = tdkTestObj.getResultDetails();
                    #Check for SUCCESS/FAILURE return value of DS_Resolution
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported and default resolutions";
                        print "%s" %resolutiondetails;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the list of supported resolutions";
                    #calling DS_SetResolution to set and get the display resolution as 1080i50    
                    resolution="1080i50";
                    print "Resolution value set to:%s" %resolution;
                    if resolution in resolutiondetails:
                        tdkTestObj = obj.createTestStep('DS_SetResolution');
                        tdkTestObj.addParameter("resolution",resolution);
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        resolutiondetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetResolution
                        if expectedresult in actualresult:
                                print "SUCCESS:set and get resolution Success";
                                print "getresolution %s" %resolutiondetails;
                                #comparing the resolution before and after setting
                                if resolution in resolutiondetails :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the resolutions are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the resolutions are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:set and get resolution fails";
                    else:
                        print "FAILURE:Requested resolution are not supported by this device";
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
                    print "FAILURE:Connection Failed"; 
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
