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
  <id>1677</id>
  <version>2</version>
  <name>E2E_RMF_backtoback_record_samechannel</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Back to back recordings of multiple programs on the same channel</synopsis>
  <groups_id/>
  <execution_time>20</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_DVR_13</test_case_id>
    <test_objective>Recorder-Back to back recordings of multiple programs on the same channel</test_objective>
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
6. Repeat the above steps again for the next program.
7.Depends on the result of above step Recorder_agent sends SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1 Status from the TDK_Recorder_server.
Checkpoint 2 Verifying the ocapRI_log to check the state of Recording.</except_output>
    <priority>High</priority>
    <test_stub_interface>Recorder_agent</test_stub_interface>
    <test_script>E2E_RMF_backtoback_record_samechannel</test_script>
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

                                        
obj.configureTestCase(ip,port,'E2E_RMF_backtoback_record_samechannel');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "Recorder module loading status : %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
print "Recorder module loading details : %s" %loadmoduledetails;
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_backtoback_record_samechannel');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Recorder module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "Recorder module load successfuls";
    starttime = 0;
   
    for i in range(1,4):        
        
        #Calling getURL_PlayURL with valid Stream ID
        result1,recording_id = sched_rec(obj,'01',starttime,'120000');
        obj.initiateReboot();
        obj.resetConnectionAfterReboot()

        starttime = starttime + 30;
            
        if ("SUCCESS" in result1.upper()):                                        
            print "Execution Success at itersation %d"%i;
        else:            
            print "Execution Failure at iteration %d"%i;
         
    #unloading Recorder module
    obj.unloadModule("rmfapp");
    
else:
    print "Failed to load Recorder module";
    obj.setLoadModuleStatus("FAILURE");
