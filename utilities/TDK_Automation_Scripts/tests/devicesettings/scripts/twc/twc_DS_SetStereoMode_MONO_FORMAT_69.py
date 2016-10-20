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

#This python script is autogenerated by parsing the original scripts imported from the Database
#This script is supposed to be called from the genericscript.py 
#TODO:replace this caling script name with correct one


'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>619</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetStereoMode_MONO_FORMAT_69</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>85</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the MONO Stereo Mode of Audio.
Test Case ID:CT_DS_69.
Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS.</synopsis>
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
    <box_type>IPClient-3</box_type>
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
#TODO: validate which imports are necessary and remove others
import sys;
from time import gmtime, strftime;
import tdklib;
import time;
import datalib;
import numpy as np;




def executeTests(obj):
	
	loadmodulestatus =obj.getLoadModuleResult();
	print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
	if "SUCCESS" in loadmodulestatus.upper():
	        #Set the module loading status
	        obj.setLoadModuleStatus("SUCCESS");
	
	        #calling Device Settings - initialize API
	        tdkTestObj = obj.createTestStep('DS_ManagerInitialize',0);
	        expectedresult="SUCCESS"
	        tdkTestObj.executeTestCase(expectedresult);
	        actualresult = tdkTestObj.getResult();
	        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
	        if expectedresult in actualresult:
	                tdkTestObj.setResultStatus("SUCCESS");
	                #calling DS_GetSupportedStereoModes get list of StereoModes.
	                tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes',0);
	                tdkTestObj.addParameter("port_name","HDMI0");
	                expectedresult="SUCCESS"
	                tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
	                stereomodedetails = tdkTestObj.getResultDetails();
	                #Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
	                if expectedresult in actualresult:
	                        print "SUCCESS :Application successfully gets the list of supported StereoModes";
	                        print "%s" %stereomodedetails
	                else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "FAILURE :Failed to get supported streoe modes";
	                #calling DS_SetStereoMode to get and set the stereo modes
	                tdkTestObj = obj.createTestStep('DS_SetStereoMode',5);
	                stereomode="MONO";
	                print "Stereo mode value set to:%s" %stereomode;  
	                tdkTestObj.addParameter("stereo_mode",stereomode);
	                expectedresult="SUCCESS"
	                tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
	                stereomodedetails = tdkTestObj.getResultDetails();
	                #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
	                if expectedresult in actualresult:
	                        print "SUCCESS :Application successfully get and set the MONO stereo mode";
	                        print "getstereomode: %s" %stereomodedetails;
	                        #comparing stereo modes before and after setting
	                        if stereomode in stereomodedetails:
	                                tdkTestObj.setResultStatus("SUCCESS");
	                                print "SUCCESS: Both the stereo modes are same";
	                        else:
	                                tdkTestObj.setResultStatus("FAILURE");
	                                print "FAILURE: Both the stereo modes are not same";
	                else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "FAILURE :Application failed to set and get the MONO stereo mode";
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
