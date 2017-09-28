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
  <version>4</version>
  <name>MediaUtils_Get_DefaultSettings</name>
  <primitive_test_id/>
  <primitive_test_name>MediaUtils_Get_DefaultSettings</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>to get default settings</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_MediaUtils_01</test_case_id>
    <test_objective>To get the default settings for audio capture</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1V3</test_setup>
    <pre_requisite>1. audiocapturemgr.service should not be up and running</pre_requisite>
    <api_or_interface_used>MediaUtils_ExecuteCmd,
MediaUtils_AudioCapture_Open,
MediaUtils_Get_DefaultSettings,
MediaUtils_AudioCapture_Close</api_or_interface_used>
    <input_parameters>MediaUtils_ExecuteCmd - input command
</input_parameters>
    <automation_approch>1. TM loads the MediaUtils_Agent via the test agent.
2. MediaUtils_Agent should kill the audiocapturemgr.service successfully.
3.Call the API to get default settings
4.MediaUtils_Agent will return SUCCESS or FAILURE based on the result of above step</automation_approch>
    <except_output>Checkpoint 1: MediaUtils_ExecuteCmd should be success and audio playing should start
Checkpoint 2:MediaUtils_AudioCapture_Open should be success
Checkpoint 3:MediaUtils_Get_DefaultSettings should return the default settings
Checkpoint 4:MediaUtils_AudioCapture_Close should close successfully</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediautilsstub.so.0.0.0</test_stub_interface>
    <test_script>MediaUtils_Get_DefaultSettings</test_script>
    <skipped>No</skipped>
    <release_version>M52</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import time;

#Test component to be tested^M
obj = tdklib.TDKScriptingLibrary("mediautils","2.0");

#IP and Port of box, No need to change,^M
#This will be replaced with correspoing Box Ip and port while executing script^M
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'MediaUtils_Get_DefaultSettings');

#Get the result of connection with test component and STB
loadStatus =obj.getLoadModuleResult();
print "[MEDIAUTILS LOAD STATUS]  :  %s" %loadStatus;
obj.setLoadModuleStatus(loadStatus.upper());

if "SUCCESS" in loadStatus.upper():
        tdkTestObj = obj.createTestStep('MediaUtils_ExecuteCmd');      
	tdkTestObj.addParameter("command","/opt/tdkplayer.sh > /dev/null 2>&1 &" );
	expectedresult = "SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        if expectedresult in actualresult:
		tdkTestObj.setResultStatus("SUCCESS");
		Details = tdkTestObj.getResultDetails();
#		print "[TEST EXECUTION RESULT] : %s" %Details;
       	        tdkTestObj = obj.createTestStep('MediaUtils_AudioCapture_Open');
                expectedresult="SUCCESS"
                #Execute the test case in STB^M
                tdkTestObj.executeTestCase(expectedresult);
		actualresult = tdkTestObj.getResult();
		if expectedresult in actualresult:
			tdkTestObj.setResultStatus("SUCCESS");
			print "MediaUtils_AudioCapture_Open call :SUCCESS";
			expectedresult="SUCCESS"
 			tdkTestObj = obj.createTestStep('MediaUtils_Get_DefaultSettings');
			tdkTestObj.executeTestCase(expectedresult);
			actualresult = tdkTestObj.getResult();
			if expectedresult in actualresult:
				print "MediaUtils_Get_DefaultSettings call : SUCCESS";
				tdkTestObj.setResultStatus("SUCCESS");
				defsettingDetails = tdkTestObj.getResultDetails();
				print "DEFAULT SETTINGS: " , defsettingDetails;
		
			else:
				print "MediaUtils_Get_DefaultSettings call : FAILURE";
				tdkTestObj.setResultStatus("FAILURE");			

	                tdkTestObj = obj.createTestStep('MediaUtils_AudioCapture_Close');
	                expectedresult="SUCCESS"
			tdkTestObj.addParameter("paramHandle","VALID");
        	        #Execute the test case in STB^M^M
                	tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
                	if expectedresult in actualresult:
                        	tdkTestObj.setResultStatus("SUCCESS");
				print "MediaUtils_AudioCapture_Close : SUCCESS"
			else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "MediaUtils_AudioCapture_Close :FAILURE"
		else:
			tdkTestObj.setResultStatus("FAILURE");
			print "MediaUtils_AudioCapture_Open : FAILURE"
  	else:
                print "ExecuteCmd call is NOT successful";
                tdkTestObj.setResultStatus("FAILURE");

        #Unloading mediautils module
	obj.unloadModule("mediautils");

else:
        print "Failed to load mediautils module\n";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
