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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_FP_getColorMode_153</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_FP_getColorMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script is used to get the color mode (single or multi color mode) of the front panel indicator.
TestcaseID: CT_DS153</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_FP_getColorMode_153');

#Get the result of connection with test component and STB
loadmodulestatus=obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                tdkTestObj = obj.createTestStep('DS_GetIndicators');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                indicatordetails = tdkTestObj.getResultDetails();
                if "SUCCESS" in actualresult:
                        print "SUCCESS :Application successfully gets the list of Indicators";
                        print "Indicators: %s" %indicatordetails
			indicatorList = indicatordetails.split(",")
                        for indicator_name in indicatorList:
				#Primitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('DS_FP_getColorMode');
				tdkTestObj.addParameter("indicator_name", indicator_name);
				expectedresult="SUCCESS"
				tdkTestObj.executeTestCase(expectedresult);
				actualresult = tdkTestObj.getResult();
				details = tdkTestObj.getResultDetails();
				print "[TEST EXECUTION RESULT] : %s" %actualresult;
				print "IndicatorName: %s ColorMode: [%s]"%(indicator_name,details);
				#Set the result status of execution
				if expectedresult in actualresult:
					tdkTestObj.setResultStatus("SUCCESS");
				else:
					tdkTestObj.setResultStatus("FAILURE");
		else :
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to get the indicators list"
		#Calling DS_ManagerDeInitialize to DeInitialize API
		result = devicesettings.dsManagerDeInitialize(obj)
else :
	print "Failed to Load Module"
	
obj.unloadModule("devicesettings");
