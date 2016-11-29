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
  <id>1582</id>
  <version>3</version>
  <name>E2E_RMF_LinearTV_ClosedCaption_LivePlayback</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Enable/Disable Closed Caption during live play. Enable/Disable Closed Caption during live play	
E2E_LinearTV_34.</synopsis>
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
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_35</test_case_id>
    <test_objective>To Enable/Disable Closed Caption during live play</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads TDKIntegration_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds
5. TM loads the ClosedCaption_Manager_Agent via the test agent.
6.ClosedCaption_Manager_Agent will initialize/start the  ClosedCaption Manager.                        
7.ClosedCaption_Manager_Agent will stop the closed  ClosedCaption Manager.
8. ClosedCaption_Manager_Agent will return SUCCESS/FAILURE status based on the return value of  APIs.""
9.tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3 Check the Closed caption  status</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub
ClosedCaption_stub</test_stub_interface>
    <test_script>E2E_RMF_LinearTV_ClosedCaption_LivePlayback</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
from tdkintegration import getURL_PlayURL;

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
cc_obj = tdklib.TDKScriptingLibrary("cc","2.0");
    

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_ClosedCaption_LivePlayback');
cc_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_ClosedCaption_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = cc_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                cc_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_ClosedCaption_LivePlayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = cc_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    cc_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");        

    #calling getURL_PlayURL to get and play the URL
    result = getURL_PlayURL(tdk_obj,'01');                
    
    if "SUCCESS" in result:
        print "Result: %s" %result;
        
        actualresult,tdkTestObj_cc,details = tdklib.Create_ExecuteTestcase(cc_obj,'CC_Initialization', 'SUCCESS',verifyList ={});        
        
        #Check for SUCCESS/FAILURE return value of CC_Initialization        
        if "SUCCESS" in actualresult:
            
            Status = 1; # Must be either 0 or 1, 0 - OFF and 1 - ON
            #calling closed caption API "CC_SetGet_Status" to set the closed caption status
            actualresult,tdkTestObj_cc,details = tdklib.Create_ExecuteTestcase(cc_obj,'CC_SetGet_State', 'SUCCESS', verifyList={'status':str(Status)},status = Status);            
           
            Status = 0; # Must be either 0 or 1, 0 - OFF and 1 - ON
            #calling closed caption API "CC_SetGet_Status" to set the closed caption status            
            actualresult,tdkTestObj_cc,details = tdklib.Create_ExecuteTestcase(cc_obj,'CC_SetGet_State', 'SUCCESS',verifyList={'status':str(Status)},status = Status);                   
			
        else:            
            print "FAILURE :CC_Initialization is not successful";
    else:
        print "FAILURE :getURL_PlayURL is not successful";       
                
    #Unload the modules
    cc_obj.unloadModule("cc");
    tdk_obj.unloadModule("tdkintegration");
else:
    print"Load module failed";
    #Set the module loading status
    cc_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");


