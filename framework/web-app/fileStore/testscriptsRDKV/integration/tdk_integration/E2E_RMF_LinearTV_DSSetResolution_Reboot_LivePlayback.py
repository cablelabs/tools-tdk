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
  <id>1590</id>
  <version>4</version>
  <name>E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the Resolution value sets by device settings component after and before reboots the STB while playing the video.	E2E_LinearTV_13</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_31</test_case_id>
    <test_objective>To check the Resolution value sets by device settings component after and before reboots the STB while playing the video.</test_objective>
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
7.Device_Settings_Agent will get the list resolution supported by a given port.
8.Device_Settings_Agent will get the default resolution supported by a given port.
9.Device_Settings_Agent will get the status of display connection.
10.Device_Settings_Agent will get the display resolution.
11. Device_Settings_Agent will set the new display resolution.
12. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result. 
13. Initiate device Reboot
14. Device_Settings_Agent will get the status of display connection.
15. Check the resolution is persistent after reboot and return SUCCESS or FAILURE"</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3 Check the Resolution before and after reboot the box</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKIntegrationStub
Devicesettings_stub</test_stub_interface>
    <test_script>E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback</test_script>
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
import devicesettings;

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dev_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");    

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');
dev_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = dev_obj.getLoadModuleResult();

print "[tdkintegration LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                dev_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetResolution_Reboot_LivePlayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = dev_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    dev_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");    

    displayStatus = "FALSE"
    #calling DS_ManagerInitialize to check Intialize API.
    actualresult = devicesettings.dsManagerInitialize(dev_obj)

    #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
    if "SUCCESS" in actualresult:
        #Calling DS_IsDisplayConnectedStatus function to check for display connection status
        displayStatus = devicesettings.dsIsDisplayConnected(dev_obj)
        if "TRUE" in displayStatus:

		actualresult,dsTdkObj,supportedResolutions = tdklib.Create_ExecuteTestcase(dev_obj,'DS_Resolution', 'SUCCESS',verifyList ={}, port_name = "HDMI0");

		print "Get current resolution"
		copyResolution = devicesettings.dsGetResolution(dev_obj,"SUCCESS",kwargs={'portName':"HDMI0"});
        	#Set resolution value to 720p
        	setresolution="720p";
        	#Check if current value is already 720p
		if setresolution not in supportedResolutions:
			print setresolution, " Resolution not supported"
		elif setresolution in copyResolution:
			print "Resolution value already at ",copyResolution
			#Calling the getURL_PlayURL to get the URL and playback
                	result = getURL_PlayURL(tdk_obj,'01');
                	if "SUCCESS" in result:
                    		print "Sucessfully executed the getURL_PlayURL function"
                	else:
                    		print "Failure: getURL_PlayURL function"
        	else:
			devicesettings.dsSetResolution(dev_obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':setresolution});
                        #Calling the getURL_PlayURL to get the URL and playback
                        result = getURL_PlayURL(tdk_obj,'01');
                        if "SUCCESS" in result:
                                print "Sucessfully executed the getURL_PlayURL function"
                        else:
                                print "Failure: getURL_PlayURL function"
        #calling DS_ManagerDeInitialize to DeInitialize API
	result = devicesettings.dsManagerDeInitialize(dev_obj)

    #unloading the module
    tdk_obj.unloadModule("tdkintegration");

    if "TRUE" in displayStatus:
    	dev_obj.initiateReboot();
    	dev_obj.resetConnectionAfterReboot();

    	print "#--------------------------------------After Reboot--------------------------------------#";

	setresolution="720p";	

    	#calling DS_ManagerInitialize to check Intialize API.
    	actualresult = devicesettings.dsManagerInitialize(dev_obj)
    	if "SUCCESS" in actualresult:
		actualresult,tdkObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_SetResolution', 'SUCCESS', verifyList = {'resolution':setresolution},resolution = setresolution, port_name = "HDMI0",get_only = 1);
        	#calling DS_ManagerDeInitialize to DeInitialize API
		result = devicesettings.dsManagerDeInitialize(dev_obj)

    #Unload the modules
    dev_obj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    dev_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");
