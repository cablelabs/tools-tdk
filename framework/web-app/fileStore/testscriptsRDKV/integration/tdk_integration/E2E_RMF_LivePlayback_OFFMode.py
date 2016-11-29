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
  <version>2</version>
  <name>E2E_RMF_LivePlayback_OFFMode</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To Verify Live Playback when STB in OFF Mode</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_51</test_case_id>
    <test_objective>Try to playback when box is in OFF mode</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads TDKIntegration_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds
5. TM loads the IARMBus_Agent via the test agent
6. The IARMBus_Agent changes power setting to OFF
7.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>IARMBUS_Stub
TDK_Integration_Stub</test_stub_interface>
    <test_script>E2E_RMF_LivePlayback_OFFMode</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from iarmbus import change_powermode
from tdkintegration import getURL_PlayURL

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();
print "Tdkintegration module loading status :  %s" %loadmodulestatus;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                iarm_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');
                #Get the result of connection with test component and STB
                loadmodulestatus =obj.getLoadModuleResult();
                loadmodulestatus1 = iarm_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;

#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper() and ("SUCCESS" in loadmodulestatus1.upper()):
        obj.setLoadModuleStatus("SUCCESS");
        iarm_obj.setLoadModuleStatus("SUCCESS");
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
            
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):               
            print "SUCCESS :Application successfully initialized with IARMBUS library";
            #calling IARMBUS API "IARM_Bus_Connect"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});    
            
            expectedresult="SUCCESS";
            #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
            if expectedresult in actualresult:                    
                print "SUCCESS: Querying STB power state -RPC method invoked successfully";
                #Setting Power mode to OFF
                result1 = change_powermode(iarm_obj,0);
                if "SUCCESS" in result1.upper():
                    result2= getURL_PlayURL(obj,'01');
                    #Setting Power mode to ON
                    change_powermode(iarm_obj,2);                    
                else:
                    change_powermode(iarm_obj,2);
                # Calling IARM_Bus_DisConnect API
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});                                 
            
            else:
                print "FAILURE: IARM_Bus_Connect failed. %s" %details;
            #calling IARMBUS API "IARM_Bus_Term"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});            
            
        else:
            print "FAILURE: IARM_Bus_Init failed. %s " %details;
        print "Tdkintegration module loaded successfully";
        obj.unloadModule("tdkintegration");
        iarm_obj.unloadModule("iarmbus");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
         iarm_obj.setLoadModuleStatus("FAILURE");
				
