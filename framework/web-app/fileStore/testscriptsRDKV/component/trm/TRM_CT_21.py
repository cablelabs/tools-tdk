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
  <id>1631</id>
  <version>1</version>
  <name>TRM_CT_21</name>
  <primitive_test_id>613</primitive_test_id>
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests recording multiple stations from same terminal.
Test Case ID: CT_TRM_21
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TRM_21</test_case_id>
    <test_objective>To validate recording multiple stations from same terminal</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo
STRING    recordingId
STRING    locator
DOUBLE  duration	
DOUBLE  startTime
INTEGER hot</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.  
2. TM will invoke “TRMAgent_TunerReserveForRecord” in TRMAgent from a terminal. 
3. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post 2 HTTP TRM ReserveTuner for record request messages with different locator and recording Id values but same devicename. Pass duration value =10000 (10s), startTime=0 and hot=0 for all the recordings.
4. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and get the response from the TRM server.  
5. Depending on the return values of ReserveTuner TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForRecord</test_stub_interface>
    <test_script>TRM_CT_21</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import reserveForRecord

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_21');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_21');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    print "Start recording multiple stations from same terminal"
    duration = 10000
    startTime = 0
    hot = 0
    for deviceNo in range(0,2):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})
    # End of for loop

    #unloading trm module
    obj.unloadModule("trm");
