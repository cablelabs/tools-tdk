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
  <id/>
  <version>4</version>
  <name>E2E_RMF_Resolution480p_Trickplay</name>
  <primitive_test_id>528</primitive_test_id>
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests if trickplay is successful after changing Device Settings HDMI Video resolution to 480p and rebooting the Box.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
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
    <test_case_id>E2E_RMF_Resolution480p_Trickplay</test_case_id>
    <test_objective>Verify if trickplay is successful after changing Device Settings Video resolution for HDMI to 480p and rebooting the Box.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. dsMgrMain should be up and running.
2. IARMDaemonMain should be up and running.
3. RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2. Device_Settings_Agent will set the new display resolution.
3. Reboot the STB.
4. TDKIntegrationStub Agent will play the live Url after changing the resolution and return SUCCESS or FAILURE based on the result.</automation_approch>
    <except_output>Checkpoint 1. Check the display Resolution value before and after setting it.
Checkpoint 2. Check if the live trickplay is successful.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>DS_Stub
TDK_Integration_Stub</test_stub_interface>
    <test_script>E2E_RMF_Resolution480p_Trickplay</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;
from tdkintegration import dvrPlayUrl;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

# Step1: Change Device Settings Video resolution for HDMI to 480p
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'E2E_RMF_Resolution480p_Trickplay');
loadmodulestatus = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
dsObj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                isDisplay = devicesettings.dsIsDisplayConnected(dsObj)
		getResolution = ""
                if "TRUE" in isDisplay:
                    #Save a copy of current resolution
                    copyResolution = devicesettings.dsGetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0"});
                    # Set resolution value to 480p
                    resolution="480p";
                    # Check if current value is already 480p
                    if resolution not in copyResolution:
			    #Check if 480p is a supported resolution
			    actualresult,dstdkObj,resolutions = tdklib.Create_ExecuteTestcase(dsObj,'DS_Resolution', 'SUCCESS', verifyList ={},port_name = "HDMI0");
			    if resolution in resolutions:
				getResolution = devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                    else:
                            print "Resolution value already at %s"%copyResolution
		
                #calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)

                if "TRUE" in isDisplay and resolution in getResolution:
                    # Step2: Reboot the box
                    dsObj.initiateReboot();

                    # Step3: Trickplay channel 2 and then channel 1
                    tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                    tdkIntObj.configureTestCase(ip,port,'E2E_RMF_Resolution480p_Trickplay');
                    loadmodulestatus = tdkIntObj.getLoadModuleResult();
                    print "TDKIntegration module loading status :  %s" %loadmodulestatus;
                    tdkIntObj.setLoadModuleStatus(loadmodulestatus);
		    loadmoduledetails = tdkIntObj.getLoadModuleDetails();
		    #Reboot if rmfstreamer is not running
		    if "FAILURE" in loadmodulestatus.upper():
        		if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                	    print "rmfStreamer is not running. Rebooting STB"
                	    tdkIntObj.initiateReboot();
			    dsObj.resetConnectionAfterReboot();
                	    #Reload Test component to be tested
                	    tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                	    tdkIntObj.configureTestCase(ip,port,'E2E_RMF_Resolution480p_Trickplay');
                	    #Get the result of connection with test component and STB
                	    loadmodulestatus =tdkIntObj.getLoadModuleResult();
                	    #print "Re-Load Module Details : %s" %loadmoduledetails1;
                	    print "Tdkintegration module loading status :  %s" %loadmodulestatus;

                    if "SUCCESS" in loadmodulestatus.upper():
                        # Tune to channel 2
                        streamId = '02'
                        result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                        print "Tuning to stream %s is [%s]"%(streamId,result)
                        if "SUCCESS" in result:
                            # Tune to channel 1
                            streamId = '01'
                            result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                            print "Tuning to stream %s is [%s]"%(streamId,result)
                        tdkIntObj.unloadModule("tdkintegration");

                    # Step4: Revert to original value of resolution unless original value was already 480p
                    if resolution not in copyResolution:
                        #calling Device Settings - initialize API
                        result = devicesettings.dsManagerInitialize(dsObj)
                        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
                        if "SUCCESS" in result:
                            devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':copyResolution});
                            #Calling DS_ManagerDeInitialize to DeInitialize API
                            result = devicesettings.dsManagerDeInitialize(dsObj)

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
