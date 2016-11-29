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
  <version>11</version>
  <name>E2E_Set_Resolution_During_Standby</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test to change the resolution during Standby Mode</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
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
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_48</test_case_id>
    <test_objective>Set the Resolutions during STANDBY</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite/>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>TV must be connected</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent and IARMBus Agent via the test agent.
2.Device_Settings_Agent will get the status of display connection.
3. IARMBus Agent sets the powermode to STANDBY
4.Device_Settings_Agent should not be able to get the list resolution supported by a given port.
5.Device_Settings_Agent should not be able to get the default resolution supported by a given port.
6. Device_Settings_Agent will get the display resolution.
6. Device_Settings_Agent will set the new display resolution.
7. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's</except_output>
    <priority>Medium</priority>
    <test_stub_interface>DS_Stub</test_stub_interface>
    <test_script>E2E_Set_Resolution_During_Standby</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode

def SetResolution(obj):
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
                        #calling DS_Resolution get list of supported resolutions and the default resolution
                        tdkTestObj = obj.createTestStep('DS_Resolution');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        resolutiondetails = tdkTestObj.getResultDetails();
                        print "%s" %resolutiondetails;
                        #Check for SUCCESS/FAILURE return value of DS_Resolution
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application was able to get the list of supported and default resolutions";
                                retval="SUCCESS";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE :Application was unable to get the list of supported resolutions";
                                retval="FAILURE";
                        #calling DS_SetResolution to set and get the display resolution as 720p    
                        resolution="720p";
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
                                        print "SUCCESS:set and get resolution executes during STANDBY";
                                        print "getresolution %s" %resolutiondetails;
                                        #comparing the resolution before and after setting
                                        if resolution in resolutiondetails :
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Both the resolutions are same and resolution is set during standby";
                                                retval="SUCCESS";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Both the resolutions are not same";
                                                retval="FAILURE";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE:set and get resolution API failed to execute successfully during STANDBY";
                                        retval="FAILURE";
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
                                        retval="FAILURE";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:Connection Failed";
                        retval="FAILURE";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
                retval="FAILURE";
        return retval;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_Set_Resolution_During_Standby');
iarm_obj.configureTestCase(ip,port,'E2E_Set_Resolution_During_Standby');
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                iarm_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_Set_Resolution_During_Standby');
                #Get the result of connection with test component and STB
                loadmodulestatus =obj.getLoadModuleResult();
                loadmodulestatus1 = iarm_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if "SUCCESS" in loadmodulestatus.upper() and ("SUCCESS" in loadmodulestatus1.upper()):
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        iarm_obj.setLoadModuleStatus("SUCCESS");
        print "SUCCESS: Querying STB power state -RPC method invoked successfully";
        result1 = change_powermode(iarm_obj,1);
        if "SUCCESS" in result1.upper():
                result2=SetResolution(obj);
                                              
        change_powermode(iarm_obj,2);                    
        
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
        iarm_obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
