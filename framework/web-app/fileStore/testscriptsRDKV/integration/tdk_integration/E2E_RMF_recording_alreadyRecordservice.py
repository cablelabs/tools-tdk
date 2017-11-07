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
  <id>1678</id>
  <version>1</version>
  <name>E2E_RMF_recording_alreadyRecordservice</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Initiate recording of already recording service</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_14</test_case_id>
    <test_objective>Recorder-Initiate recording of already recording service</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.RMFMediastreamer executable should be running.
2.Device time should be in current time of UTC.
3. Two files should be created in the name of “stt_received” and “stage4” in “tmp” path of device.
4. In rmfconfig.ini file the parameter “FEATURE.LONGPOLL.URL” should be pointing to TM.</input_parameters>
    <automation_approch>1.TM loads Recorder_agent via the test agent.
2.TM gets an source_id from the streaming details page of the FW and sends it to Recorder_agent to generate request url.
3.TM pass the parameters like duration and recording_id to Recorder_agent.
3.Recorder_agent will frame the json message to schedule the recording and send to TDK_Recorder_server which is present in TM.
4.Status of the Json response from Mediastreamer to TDK_Recorder_Server getting extracted by TM.
5 Recorder_agent  will do the error checking by verifying ocapri_logs.
6. Repeat the above steps again for the same program.
7.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapRI_log to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>Recorder_agent</test_stub_interface>
    <test_script>E2E_RMF_recording_alreadyRecordservice</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import sched_rec

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
                                        
obj.configureTestCase(ip,port,'E2E_RMF_recording_alreadyRecordservice');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "Recorder module loading status : %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_recording_alreadyRecordservice');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Recorder module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "Recorder module load successfuls";   
   
    #Calling sched_rec with valid Stream ID
    #Duration value given in terms of milliseconds
    duration = "120000"; 
    result1,recordid = sched_rec(obj,'01',"0",duration);
    print "Result1:%s"%result1
    time.sleep(150);

    #Calling sched_rec with valid Stream ID
    result2,recordid = sched_rec(obj,'01','0',duration);
    print "Result2:%s"%result2
        
    if ("SUCCESS" in result1) and ("SUCCESS" in result2):                                        
        print "Execution Success"
    else:            
        print "Execution failure"
         
    #unloading Recorder module
    obj.unloadModule("rmfapp");
    
else:
    print "Failed to load Recorder module";
    obj.setLoadModuleStatus("FAILURE");
