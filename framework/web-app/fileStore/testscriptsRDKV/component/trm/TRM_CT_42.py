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
  <id>1691</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_42</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests tuning to channel 6 from terminal 2 when current state of reservation is R1-R2-R3-R4-L5 on terminal 1.  
Test Case ID: CT_TRM_42
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
from trm import getMaxTuner,reserveForRecord,reserveForLive,getAllTunerStates;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_42');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_42');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    #Fetch max tuners supported
    print "Fetch max tuners supported"
    maxTuner = getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    # Start recording channel 1-4 from device 1
    print "\nStart " , maxTuner-1, " recordings from device 1 on different channels\n"
    duration = 10000
    startTime = 0
    hot = 0
    deviceNo1 = 0
    for channelNo in range(1,maxTuner):
        # Frame different request URL for each client box
        streamId = '0'+str(channelNo+1)
        recordingId = 'RecordIdCh'+streamId
        reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo1,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':hot})
    # End of for loop

    # Start live tuning channel5 from device 1
    print "\nStart live tuning from device 1 on another new channel\n"
    streamId = '0'+str(channelNo+2)
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo1,'streamId':streamId,'duration':duration,'startTime':startTime})

    # All tuners are busy now

    # Start live tuning channel 6 from device 2
    print "\nStart live tuning from device 2 on another new channel\n"
    deviceNo2 = 1
    streamId = '0'+str(channelNo+3)
    reserveForLive(obj,'FAILURE',kwargs={'deviceNo':deviceNo2,'streamId':streamId,'duration':duration,'startTime':startTime})

    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
