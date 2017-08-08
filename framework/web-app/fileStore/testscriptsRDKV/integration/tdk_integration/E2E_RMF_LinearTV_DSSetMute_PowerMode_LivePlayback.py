# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1581</id>
  <version>7</version>
  <name>E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the DS set Mute while live playback and sets the power state of STB using DS.	E2E_LinearTV_16</synopsis>
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
    <test_case_id>E2E_LinearTV_34</test_case_id>
    <test_objective>To check the DS set Mute while live playback and sets the power state of STB using DS.</test_objective>
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
6. TM loads the Device_Settings_Agent via the test agent.
7. TM loads the Device_Settings_Agent via the test agent.
8. TM loads the Device Settings_Agent via the test agent
9.Device_Settings_Agent will check for the status of audio mute status.
10. Device_Settings_Agent will enable/disable audio mute status of audio port.
11. Device_Settings_Agent will check for the status of audio mute and will return SUCCESS or FAILURE based on the result. 
12.Device_Settings_Agent will add listener for power mode change.
13.Device_Settings_Agent will set the desired power state of STB.
14.Device_Settings_Agent will check for the state of STB and will return SUCCESS or FAILURE based on the result. 
15.tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3 Check the Mute status</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub
Devicesettings_stub</test_stub_interface>
    <test_script>E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
from tdkintegration import getURL_PlayURL;
from iarmbus import change_powermode

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dev_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
dev_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = dev_obj.getLoadModuleResult();
loadmodulestatus2 = iarm_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus2 ;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                dev_obj.resetConnectionAfterReboot();
                iarm_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetMute_PowerMode_LivePlayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = dev_obj.getLoadModuleResult();
                loadmodulestatus2 = iarm_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()) and ("SUCCESS" in loadmodulestatus2.upper()):
    #Set the module loading status
    dev_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");
    iarm_obj.setLoadModuleStatus("SUCCESS");

    #calling getURL_PlayURL to get and play the URL
    result = getURL_PlayURL(tdk_obj,'01');                
    
    if "SUCCESS" in result:     
                
        #calling DS_ManagerInitialize to check Intialize API.
        actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerInitialize', 'SUCCESS',verifyList ={});
                
        mutestatus=0;
        print "Port name value set to:%s" %mutestatus;                               
                
        portname = "HDMI0";                
        print "Port name value set to:%s" %portname;

        powermode=0;
        print "Power Mode value set to %s" %powermode;
                
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in actualresult:
            
            #calling DS_MuteStatus to check audio mute for a port.
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_MuteStatus', 'SUCCESS',verifyList = {'mute_status':str(mutestatus)},port_name = portname, mute_status = mutestatus);                    
            if "SUCCESS" in actualresult:
                
                #calling DS_SetPowerMode to set the power mode of STB
                change_powermode(iarm_obj,2);                        

            #calling DS_ManagerDeInitialize to DeInitialize API
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerDeInitialize', 'SUCCESS',verifyList ={});                                    
                            

        else:
            print "FAILURE :DS Manager Intialize";    
              
    else:                
        print "FAILURE: getURL_PlayURL function";               
        
        
    #Unload the deviceSettings module
    dev_obj.unloadModule("devicesettings");
    tdk_obj.unloadModule("tdkintegration");
    iarm_obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        dev_obj.setLoadModuleStatus("FAILURE");
        iarm_obj.setLoadModuleStatus("FAILURE");
        tdk_obj.setLoadModuleStatus("FAILURE");

