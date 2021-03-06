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
  <id/>
  <version>3</version>
  <name>DS_FP_getBrightnessLevels_152</name>
  <primitive_test_id/>
  <primitive_test_name>DS_FP_getBrightnessLevels</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test script gets the maximum brightness, minimum brightness and the brightness level.
TestcaseID: CT_DS152</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_152</test_case_id>
    <test_objective>This test script gets the maximum brightness, minimum brightness and the brightness level.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XI3-1/XG1-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>void getBrightnessLevels(int &amp;levels, int &amp;min, int &amp;max)</api_or_interface_used>
    <input_parameters>string indicator_name ("Message", "Power", "Record", "Remote" and "RfByPass")</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the brightness levels, min value and max value for given front panel indicator.
3.Device_Settings_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <except_output>Checkpoint 1. Check if brightness levels are retrieved successfully</except_output>
    <priority>High</priority>
    <test_stub_interface>none</test_stub_interface>
    <test_script>DS_FP_getBrightnessLevels_152</test_script>
    <skipped>No</skipped>
    <release_version>M27</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'DS_FP_getBrightnessLevels_152');

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
                        print "Indicators:%s" %indicatordetails
			indicatorList = indicatordetails.split(",")
			#Primitive test case which associated to this Script
			tdkTestObj = obj.createTestStep('DS_FP_getBrightnessLevels');
			for indicator_name in indicatorList:
				print "Getting the Brightness levels for : ", indicator_name	
				tdkTestObj.addParameter("indicator_name", indicator_name);
		                expectedresult="SUCCESS"
		                tdkTestObj.executeTestCase(expectedresult);
		                actualresult = tdkTestObj.getResult();
		                details = tdkTestObj.getResultDetails();
		                print "[TEST EXECUTION RESULT] : %s" %actualresult;
		                print "Details: [%s]"%details;
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
	print "Failed to Load Module "
	
obj.unloadModule("devicesettings");
