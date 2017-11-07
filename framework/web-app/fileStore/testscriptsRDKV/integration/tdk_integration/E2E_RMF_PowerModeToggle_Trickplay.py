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
  <version>13</version>
  <name>E2E_RMF_PowerModeToggle_Trickplay</name>
  <primitive_test_id>528</primitive_test_id>
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Tests if STB is able to tune to linear channel when going from standby to on state.</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>IPClient-3</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_RMF_PowerModeToggle_Trickplay</test_case_id>
    <test_objective>Check if STB is able to tune to linear channel when going from StandBy to On state.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1/XI3-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. “IARMDaemonMain” Process should be running.
2. “pwrMgrMain” process should be running.
3. RMFMediastreamer executable should be running.</input_parameters>
    <automation_approch>1.TM loads the IARMBUS_Agent via the test agent.
2.The IARMBUS_Agent initializes and registers with IARM Bus Daemon. 
3.pwrMgrMain registers a RPC methods for setting the power state and this RPC can be invoked by IARMBUS_Agent application.
4.IARMBUS_Agent Invoke the RPC method of pwrMgrMain application to set the power state of STB to STANDBY (1).
5.TDKIntegrationStub Agent will play the live Url after changing the power mode and return SUCCESS or FAILURE based on the result.
6.IARMBUS_Agent Invoke the RPC method of pwrMgrMain application to set the power state of STB to ON (2).
7.TDKIntegrationStub Agent will play the live Url after changing the power mode and return SUCCESS or FAILURE based on the result.
8.IARMBUS_Agent deregister from the IARM Bus Daemon.
9.For each API called in the script, IARMBUS_Agent will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>IARMBUS_Stub
TDK_Integration_Stub</test_stub_interface>
    <test_script>E2E_RMF_PowerModeToggle_Trickplay</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode
from tdkintegration import dvrPlayUrl;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
iarmObj.configureTestCase(ip,port,'E2E_RMF_PowerModeToggle_Trickplay');
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[IARMBUS LIB LOAD STATUS] : %s"%iarmLoadStatus ;
iarmObj.setLoadModuleStatus(iarmLoadStatus);

tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
tdkIntObj.configureTestCase(ip,port,'E2E_RMF_PowerModeToggle_Trickplay');
tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
print "TDKIntegration LIB LOAD STATUS :  %s" %tdkIntLoadStatus;
tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

expectedresult="SUCCESS"
tdkIntLoaddetails = tdkIntObj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in tdkIntLoadStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in tdkIntLoaddetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdkIntObj.initiateReboot();
                iarmObj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdkIntObj.configureTestCase(ip,port,'E2E_RMF_simultaneous_recording_liveplayback');
                #Get the result of connection with test component and STB
                tdkIntLoadStatus =tdkIntObj.getLoadModuleResult();
                iarmLoadStatus = iarmObj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %tdkIntLoadStatus;
if (expectedresult in iarmLoadStatus.upper()) and (expectedresult not in tdkIntLoadStatus.upper()):
        iarmObj.unloadModule("iarmbus");
elif (expectedresult in tdkIntLoadStatus.upper()) and (expectedresult not in iarmLoadStatus.upper()):
        tdkIntObj.unloadModule("tdkintegration");
else:
        # Toggle between state values STANDBY (1) / ON (2)
        for powermode in range(1,3):
            actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init',expectedresult,verifyList ={});
            print "IARMBUS_Init result: [%s]"%actualresult;
            #Check for return value of IARMBUS_Init
            if expectedresult in actualresult:
                #Calling "IARM_Bus_Connect"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect',expectedresult,verifyList ={});
                print "IARMBUS_Connect result: [%s]"%actualresult;
                #Check for return value of IARMBUS_Connect
                if expectedresult in actualresult:
                        #Calling change_powermode
                        result = change_powermode(iarmObj,powermode);
                        print "Set PowerMode to %d: %s"%(powermode,result);

                        #Trickplay channel 2
                        streamId = '02'
                        result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                        print "Tuning to stream %s is [%s] with PowerMode=%d"%(streamId,result,powermode)

                        #Calling IARMBus_DisConnect API
                        actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect',expectedresult,verifyList ={});
                        print "IARMBUS_DisConnect result: [%s]"%actualresult;
                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term',expectedresult,verifyList ={});
                print "IARMBUS_Term result: [%s]"%actualresult;
        #End of loop for powermode toggle
		
		#calling IARMBUS API "IARM_Bus_Init"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});

        #calling IARMBUS API "IARM_Bus_Connect"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});

        #Setting Power mode to ON
        change_powermode(iarmObj,2);

        #Calling IARM_Bus_DisConnect API
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});

        #calling IARMBUS API "IARM_Bus_Term"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
        #Unload modules
        iarmObj.unloadModule("iarmbus");
        tdkIntObj.unloadModule("tdkintegration");
