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
  <name>TRM_CT_47</name>
  <primitive_test_id/>
  <primitive_test_name>TRM_TunerReserveForLive</primitive_test_name>
  <primitive_test_version>4</primitive_test_version>
  <status>FREE</status>
  <synopsis>Automation of RDK-16023 to verify that repeated reserve tuner requests fail with "InvalidToken" reserveTunerResponse when requested with same token and different device IDs. Testcase ID: CT_TRM_47</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_TRM_47</test_case_id>
    <test_objective>Automation of RDK-16023 to verify that repeated reserve tuner requests fail with "InvalidToken" reserveTunerResponse when requested with same token and different device IDs</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1-1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>ReserveTuner</api_or_interface_used>
    <input_parameters>INTEGER  deviceNo
STRING    locator
DOUBLE  duration
DOUBLE  startTime
STRING    token</input_parameters>
    <automation_approch>1. TM loads TRMAgent via the test agent.  
2. TM will invoke “TRMAgent_TunerReserveForLive” in TRMAgent for a channel from a terminal with duration value 20s and startTime=0 and get the reservation token T1
3. TM will invoke “TRMAgent_TunerReserveForLive” in TRMAgent for same channel from 9 different terminals using token T1 and duration value 20s and startTime=0. 
4. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and post HTTP TRM ReserveTuner for tuning request messages in step 2 and 3
5. TRMAgent will connect to TRM Server on IP 127.0.0.1 port 9987 and get the response from the TRM server.  
6. Depending on the return values of ReserveTuner TRMRequest API, TRMAgent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>1. Check the return value of API for success in step2
2. Check the return value of API in step3 such that all requests fail with "InvalidToken" response code</except_output>
    <priority>High</priority>
    <test_stub_interface>libtrmstub.so
TestMgr_TRM_TunerReserveForLive</test_stub_interface>
    <test_script>TRM_CT_47</test_script>
    <skipped>No</skipped>
    <release_version>M36</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import getMaxTuner,reserveForLive
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_47');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_47');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    duration = 20000
    startTime = 0
    streamId = '01'

    token = reserveForLive(obj,"SUCCESS",kwargs={'deviceNo':0,'streamId':streamId,'duration':duration,'startTime':startTime})

    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()
    #Use same token to reserve tuner multiple times and expect all reservations to fail with InvalidState or InvalidToken Error OR all should be success
    for deviceNo in range(1,10):

        print "DeviceNo:%d Locator:%s duration:%d startTime:%d token:%s"%(deviceNo,locator,duration,startTime,token)

        tdkTestObj.addParameter("deviceNo",deviceNo);
        tdkTestObj.addParameter("duration",duration);
        tdkTestObj.addParameter("locator",locator);
        tdkTestObj.addParameter("startTime", startTime);
        tdkTestObj.addParameter("token", token);

        expectedRes = "FAILURE"

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedRes);

        #Get the result of execution
        result = tdkTestObj.getResult();
        print "Result: [%s]"%result
        details = tdkTestObj.getResultDetails();
        print "Details: [%s]"%details;

        #Set the result status of execution
        if "FAILURE" in result.upper():
            if "InvalidToken" in details:
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Reservation did not fail with InvalidToken response code"
        else:
                tdkTestObj.setResultStatus("FAILURE");
        print "\n"
    # End for loop

    # Add sleep to release all reservations
    sleep(10)

    #unloading trm module
    obj.unloadModule("trm");
