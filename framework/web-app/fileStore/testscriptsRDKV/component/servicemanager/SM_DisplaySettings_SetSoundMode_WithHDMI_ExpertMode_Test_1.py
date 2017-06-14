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
  <version>8</version>
  <name>SM_DisplaySettings_SetSoundMode_WithHDMI_ExpertMode_Test_1</name>
  <primitive_test_id/>
  <primitive_test_name>SM_DisplaySetting_SetSoundMode</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test setSoundMode on a connected HDMI port with a valid audio expert mode
  Test Case Id : CT_14319_15</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <test_case_id>CT_18842_01</test_case_id>
    <test_objective>Service Manager â&#128;&#147;Test DisplaySettingService::setSoundMode()  on a connected HDMI port with a valid audio mode
</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-V3</test_setup>
    <pre_requisite>HDMI out of STB should be connected to a TV
</pre_requisite>
    <api_or_interface_used>"bool registerService(const QString&amp; , ServiceStruct )
Service* getGlobalService(const QString&amp; serviceName) virtual ServiceParams callMethod(const QString&amp; method,const ServiceParams&amp; params)
bool unregisterService(const QString&amp; )                                  "
                            "</api_or_interface_used>
    <input_parameters>"registerService : Qstring-serviceName, ServiceStruct - serviceStruct (function ptr)
GetGlobalService: const Qstring â&#128;&#147; serviceName                                CallMethod : const QString - ""setSoundMode"" ,const ServiceParams - bool                             
UnregisterService : Qstring-serviceName"
</input_parameters>
    <automation_approch>"1. TM loads the Service_Manager_Agent via the test agent.
2.Service_Manager_Agent will register DisplaySettingService with ServiceManager component.
3.On Success of registerService , calls DisplaySettingService setSoundMode callMethod with HDMI as parameter
4.Service_Manager_Agent will check setSoundmode status and return SUCCESS/FAILURE status. 
5.Service_Manager_Agent will deregister a given service from ServiceManager component.
"
</automation_approch>
    <except_output>"Checkpoint 1.Check the return value of APIs for success status.

"
</except_output>
    <priority>High</priority>
    <test_stub_interface>"libservicemanagerstub.so
"</test_stub_interface>
    <test_script>SM_DisplaySettings_SetSoundMode_WithHDMI_ExpertMode_Test_1</test_script>
    <skipped>No</skipped>
    <release_version>M49</release_version>
    <remarks>Set Expert Mode</remarks>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;
import servicemanager;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'SM_DisplaySettings_SetSoundMode_WithHDMI_ExpertMode_Test_1');

result = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" in result.upper():
	isDisplayConnected = "FALSE"
        result = devicesettings.dsManagerInitialize(dsObj);
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                isDisplayConnected = devicesettings.dsIsDisplayConnected(dsObj);
        if "FALSE" == isDisplayConnected:
                result = devicesettings.dsManagerDeInitialize(dsObj)
                dsObj.unloadModule("devicesettings");
                print "\nPlease test with HDMI device connected. Exiting....!!!"
                exit()
else:
        exit()

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");

obj.configureTestCase(ip,port,'SM_DisplaySettings_SetSoundMode_WithHDMI_ExpertMode_Test_1');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
if "SUCCESS" in result.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        tdkTestObj = obj.createTestStep('SM_RegisterService');
        expectedresult = "SUCCESS"
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

                #calling GetSoundMode
		get_ret = servicemanager.DS_getSoundMode(obj,"HDMI0");
		if expectedresult in get_ret[0]:
			print "SUCCESS: GetSoundMode() successful";
			if "PASSTHRU" in get_ret[1]:
				tdkTestObj.setResultStatus("SUCCESS");
				print "The Audio mode is allready set to PASSTHRU:No need to set the same again"
				
			else:
		                audioMode = "passthru";
                                tdkTestObj = obj.createTestStep('SM_DisplaySetting_SetSoundMode');
                                expectedresult="SUCCESS"
                                portName = "HDMI0";
                                tdkTestObj.addParameter("portName", portName);
                                tdkTestObj.addParameter("audioMode", audioMode);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                serviceDetail = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] : %s"%serviceDetail;
                                #Check for SUCCESS/FAILURE return value of SM_DeviceSetting_GetAppInfo
                                if expectedresult in actualresult:
                                        print "SUCCESS: SetAudiomode successful";
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        print "FAILURE: SetAudiomode failure";
                                        tdkTestObj.setResultStatus("FAILURE");

                                tdkTestObj = obj.createTestStep('SM_DisplaySetting_GetSoundMode');
                                expectedresult="SUCCESS"
                                portName = "HDMI0";
                                tdkTestObj.addParameter("portName", portName);
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                serviceDetail = tdkTestObj.getResultDetails();
                                print "[TEST EXECUTION DETAILS] soundmode is: %s"%serviceDetail;
                                #Check for SUCCESS/FAILURE return value of SM_DeviceSetting_GetAppInfo
                                if expectedresult in actualresult:
                                        print "SUCCESS: GetSoundMode() successful";
		                	if audioMode.upper() in serviceDetail:
		                		print "SUCCESS: audiomode set for connected port"
	                                        tdkTestObj.setResultStatus("SUCCESS");
		                	else:
                                                print "FAILURE: audiomode not set for connected port"
                                                tdkTestObj.setResultStatus("FAILURE");				
                                else:
                                        print "FAILURE: GetSoundMode() failure";
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
