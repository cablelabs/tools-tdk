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
  <id>1702</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_30</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_ReleaseTunerReservation</primitive_test_name>
  <!--  -->
  <primitive_test_version>5</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests release live reservation on channel 1 and again reserve it for recording when current state of reservation is (L-L-L-R-R).
Test Case ID: CT_TRM_30
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import reserveForRecord,reserveForLive,releaseReservation,getAllTunerStates;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_30');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_30');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Pre-condition: Device1 L1, Device2 L2, Device3 L3, Device4 R4, Device5 R5
    duration = 10000
    startTime = 0

    # Live tune channel 1
    print "Live tune channel 1"
    deviceNo = 0
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'01','duration':duration,'startTime':startTime})

    # Live tune channel 2
    print "Live tune channel 2"
    deviceNo = 1
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'02','duration':duration,'startTime':startTime})

    # Live tune channel 3
    print "Live tune channel 3"
    deviceNo = 2
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'03','duration':duration,'startTime':startTime})

    # Recording channel 4
    print "Recording channel 4"
    deviceNo = 3
    hot = 0
    recordingId = 'RecordIdCh04'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'04','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})

    # Recording channel 5
    print "Recording channel 5"
    deviceNo = 4
    hot = 0
    recordingId = 'RecordIdCh05'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'05','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})
    # End of pre-condition

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    # Release live tune on channel 1
    print "Release live tune on channel 1"
    deviceNo = 0
    releaseReservation(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'activity':1,'streamId':'01'})

    # Recording channel 1
    print "Recording channel 1"
    deviceNo = 0
    hot = 0
    recordingId = 'RecordIdCh01'
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':'01','duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
