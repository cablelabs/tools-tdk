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
  <id>1115</id>
  <version>1</version>
  <name>E2E_RMF_RF_Video_14</name>
  <primitive_test_id>558</primitive_test_id>
  <primitive_test_name>TDKE2E_RMF_Linear_Simultaneous_ChannelChange</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>E2E_RMF_RF_Video_14: To verify that fast channel change feature supports in all five linear TV signals tuned to XG1 from all five XI3 client boxes decoding only  HD services simultaneously.				
Note: Tested only with 2 XI3 client Boxes.</synopsis>
  <groups_id/>
  <execution_time>7</execution_time>
  <long_duration>false</long_duration>
  <remarks>This script is tested on the ipnetwork with two ipclient boxes connected, Not tested on Moca network</remarks>
  <skip>true</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <rdk_version>RDK1.3</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_RF_Video_14</test_case_id>
    <test_objective>To verify that fast channel change feature supports in all five 5 linear TV signals tuned to XG1 from all five XI3 client boxes decoding only  HD services simultaneously.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-XI3_1</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Input RF link should have six different services simultaneously    (Active signal should be available)    2. XG1 is connected through XI3 client box through RF.                       3. XG1 and XI3 board should be up and running in same network.</input_parameters>
    <automation_approch>1)Connect XI3 client box through XG1.                                2)Agent will be running in the xi3 box.                   3)Framework requests agents to tune to a HD channel.                       4) And framework schedules the agent to fast change the channel to another HD channel on the boxes</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's for success status.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>TDKIntegration_Stub</test_stub_interface>
    <test_script>E2E_RMF_RF_Video_14</test_script>
    <skipped>Yes</skipped>
    <release_version>M21</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
import tdklib;
import time;
from tdklib import CreateTestThread

#Add ip and portnumbers of the client boxes to be tested.
xi3_1 = "192.168.30.120"
xi3_1_port = 8087

xi3_2 = "192.168.30.122"
xi3_2_port = 8087

#Add ip and portnumber of the gateway box
xg1_ip = "192.168.30.65"
xg1_port = "8080"

request_url = "http://" + xg1_ip + ":" + xg1_port + "/vldms/tuner?ocap_locator=ocap://"

#Add the ocap_ids for channel tuning.
ocap_ids = ["0xa1","0xa3","0xa1","0xa3","0xa1","0xa3"];

SUCCESS = 0
FAILURE = 1

def TDKE2E_Linear_Simultaneous_ChannelChange(IP,portnumber,args=(),kwargs={}):

   #Test component to be tested
   obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

   #IP and Port of box, No need to change,
   #This will be replaced with corresponding Box Ip and port while executing script
   ip = IP
   port = portnumber

   print "E2e rmf scirpt called"
   obj.configureTestCase(ip,port,'TDKE2E_RMF_RF_Video_14');

   #Get the result of connection with test component and STB
   #Get the result of connection with test component and STB
   result =obj.getLoadModuleResult();
   print "e2e_rmf module [LIB LOAD STATUS]  :  %s" %result;

   if "SUCCESS" in result.upper():
       obj.setLoadModuleStatus("SUCCESS");
       print "e2e rmf module load successful";

       #Prmitive test case which associated to this Script
       tdkTestObj = obj.createTestStep('TDKE2E_RMF_Linear_Simultaneous_ChannelChange');

       for ocapId in ocap_ids:
           #set the tuning url
           url = request_url + ocapId

           print " "
           print "The Play Url Requested: %s"%url
           tdkTestObj.addParameter("playUrl",url);

           #Execute the test case in STB
           expectedresult="SUCCESS";
           tdkTestObj.executeTestCase(expectedresult);

           #Get the result of execution
           actualresult = tdkTestObj.getResult();
           details =  tdkTestObj.getResultDetails();
           print "Simultaneus tuning from client box [TEST EXECUTION RESULT] : %s" %actualresult;
           print "Channel tuning " + actualresult
           tdkTestObj.setResultStatus(actualresult);
           print "Simultaneous tuning: " + actualresult + " [%s]"%details;
           print " "
       
       obj.unloadModule("tdkintegration");
   else:
       print "Failed to load e2e_rmf module";
       obj.setLoadModuleStatus("FAILURE");

   return SUCCESS


# Create new threads
test1 = CreateTestThread(xi3_1,xi3_1_port,TDKE2E_Linear_Simultaneous_ChannelChange)

test2 = CreateTestThread(xi3_2,xi3_2_port,TDKE2E_Linear_Simultaneous_ChannelChange)


# Start new Threads
test1.start()
test2.start()
test1.join()
test2.join()
try:
    print "test1 return value = %s" %(test1.returnValue)
except AttributeError:
    print "No return value for test 1"
try:
    print "test2 return value = %s" %(test2.returnValue)
except AttributeError:
    print "No return value for test 2"
