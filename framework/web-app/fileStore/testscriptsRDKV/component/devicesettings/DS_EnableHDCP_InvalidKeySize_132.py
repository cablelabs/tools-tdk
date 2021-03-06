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
  <version>1</version>
  <name>DS_EnableHDCP_InvalidKeySize_132</name>
  <primitive_test_id/>
  <primitive_test_name>DS_EnableHDCP</primitive_test_name>
  <primitive_test_version>3</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test enable HDCP authentication using invalid key size.
TestcaseID: CT_DS132</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS132</test_case_id>
    <test_objective>Test enable HDCP authentication using invalid key size.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.</pre_requisite>
    <api_or_interface_used>device::Manager::Initialize() 
device::VideoOutputPortType::enabledHDCP(protectContent,hdcpKey,keySize)
device::Host::getVideoOutputPort.getHDCPStatus()
device::Manager::DeInitialize()</api_or_interface_used>
    <input_parameters>bool protectContent = 1, string key = '0', int keySize = 1281, bool useMfrKey = 0</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will enable HDCP and get the status of authentication.
3. Device_Settings_Agent will return SUCCESS or FAILURE based on whether hdcp status is authenticated.</automation_approch>
    <except_output>Checkpoint 1.Check HDCP enable should execute without error.
Checkpoint 2.HDCP status should not be authenticated</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TestMgr_DS_managerInitialize
TestMgr_DS_VOPTYPE_enableHDCP
TestMgr_DS_VOP_getHDCPStatus
TestMgr_DS_managerDeinitialize</test_stub_interface>
    <test_script>DS_EnableHDCP_InvalidKeySize_132</test_script>
    <skipped>No</skipped>
    <release_version>M23</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load module to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'DS_EnableHDCP_InvalidKeySize_132');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:

                        #Enable HDCP
                        tdkTestObj = obj.createTestStep('DS_EnableHDCP');
                        #Passing invalid key value for enabling HDCP
                        key = '0'
                        keySize = 1281
                        protectContent = 1
                        tdkTestObj.addParameter("hdcpKey",key);
                        tdkTestObj.addParameter("keySize",keySize);
                        tdkTestObj.addParameter("protectContent",protectContent);
                        expectedresult="FAILURE"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "protectContent: %d HDCP key: %s keySize: %d"%(protectContent,key,keySize)
                        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                        print "Details: [%s]"%details;
                        #Check for SUCCESS/FAILURE return value of DS_GetHDCPStatus
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                else:
                        print "HDMI display not connected. Exiting..."
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
