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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1112</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_RF_Video_09</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>558</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMF_Linear_Simultaneous_ChannelChange</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_RF_Video_09: To verify tuning time for channel change.
Note: Tested only with 2 XI3 client Boxes.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This script is tested on the ipnetwork with two ipclient boxes connected, Not tested on Moca network</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
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
ocap_ids = ["0xa1","0xa3","0xa1","0xa3","0xa1","0x9d"];

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
   obj.configureTestCase(ip,port,'TDKE2E_RMF_RF_Video_09');

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
           tdkTestObj.setResultStatus(actualresult);
           if "SUCCESS" in actualresult:
               result = eval(details)
               print "Channel Tuning Time:  " + result["tuningtime"] +" in ms (milli seconds)."
               print "Box with IP: %s"%ip
               print "Simultaneous tuning: " + actualresult + " [" + result["summary"] + "]"
               print " "
           else:
               print "Channel Tuning Time:  0 in ms (milli seconds)."
               print "Box with IP: %s"%ip
               print "Simultaneous tuning: " + actualresult + " [" + details + "]"
       
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
