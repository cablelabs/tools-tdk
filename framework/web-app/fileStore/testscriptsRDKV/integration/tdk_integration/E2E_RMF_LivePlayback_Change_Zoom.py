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
  <version>1</version>
  <name>E2E_RMF_LivePlayback_Change_Zoom</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test tries to change the Zoom settings during Live Playback</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_49</test_case_id>
    <test_objective>Try to change Zoom during Live Trickplay</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads TDKIntegration_agent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds
5. TM loads the DS_Agent via the test agent
6. The Ds_Agent changes the Zoom settings
7. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's</except_output>
    <priority>Medium</priority>
    <test_stub_interface>DS_Stub
TDK_Integration_Stub</test_stub_interface>
    <test_script>E2E_RMF_LivePlayback_Change_Zoom</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkintegration import getURL_PlayURL

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
tdkObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dsObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_Change_Zoom');
tdkObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_Change_Zoom');
dsLoadStatus = dsObj.getLoadModuleResult();
tdkIntLoadStatus = tdkObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
print "[tdkintegration LIB LOAD STATUS]  :  %s" %tdkIntLoadStatus
loadmoduledetails = tdkObj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in tdkIntLoadStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdkObj.initiateReboot();
                dsObj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdkObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdkObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_Change_Zoom');
                #Get the result of connection with test component and STB
                tdkIntLoadStatus =tdkObj.getLoadModuleResult();
                dsLoadStatus = dsObj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %tdkIntLoadStatus;
if ("SUCCESS" in dsLoadStatus.upper()) and ("SUCCESS" in tdkIntLoadStatus.upper()):

        #Set the module loading status
        dsObj.setLoadModuleStatus("SUCCESS");
        tdkObj.setLoadModuleStatus("SUCCESS");

        result = getURL_PlayURL(tdkObj,'01');
        if ("SUCCESS" in result.upper()):

       	    print "Live Playback execution successful"
 
            #calling Device Settings - initialize API
            tdkTestObj = dsObj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS :Application successfully initialized with Device Settings library";

                    #Invoke primitive testcase
                    tdkTestObj = dsObj.createTestStep('DS_VD_getSupportedDFCs');
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    supportedDFCs = tdkTestObj.getResultDetails();
                    print "Details: ",supportedDFCs
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                        zoom="Full";
                        if zoom.upper() in supportedDFCs.upper():
                                #calling DS_SetDFC to get and set the zoom settings
                                tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                                print "Zoom value set to %s" %zoom;
                                tdkTestObj.addParameter("zoom_setting",zoom);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                dfcdetails = tdkTestObj.getResultDetails();
                                print "Details: ",dfcdetails
                                #Check for SUCCESS/FAILURE return value of DS_SetDFC
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS :Application successfully gets and sets the zoom settings to Full for the video device";
	        			result = getURL_PlayURL(tdkObj,'01');
        				if ("SUCCESS" in result.upper()):
            					print "Live Playback execution successful after changing zoom settings"
        				else:
            					print "Live Playback execution failed after changing zoom settings"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE :Failed to get and set the Full zoom";

				print "Revert zoom to None"
				zoom="None";
                                #calling DS_SetDFC to get and set the zoom settings
                                tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                                print "Zoom value set to %s" %zoom;
                                tdkTestObj.addParameter("zoom_setting",zoom);
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                dfcdetails = tdkTestObj.getResultDetails();
                                print "Details: ",dfcdetails
                                #Check for SUCCESS/FAILURE return value of DS_SetDFC
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE : Full is not a supported value"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get SupportedDFCs";

                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = dsObj.createTestStep('DS_ManagerDeInitialize');
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
            else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Device Setting Initialize failed";
        else:
            print "Live Playback execution failed"

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
        tdkObj.unloadModule("tdkintegration");
else:
        print"Load module failed";
        #Set the module loading status
        dsObj.setLoadModuleStatus("FAILURE");
        tdkObj.setLoadModuleStatus("FAILURE");
