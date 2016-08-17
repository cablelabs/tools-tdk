#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1710</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_38</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>613</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests hot record channel 1 with start time 2s from now for 10s and again request hot record channel1 with start time 4s from now for 5s. 
Test Case ID: CT_TRM_38
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from trm import reserveForRecord, getAllTunerStates;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'TRM_CT_38');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_38');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Schedule future recordings on same channel
    # Hot recording channel 1 with start time 2s from now for 10s
    print "Schedule recording on channel 1 with start time 2s from now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':10000,'startTime':2,'recordingId':'RecordIdDevice1','hot':1})
    # Hot recording channel 1 with start time 4s from now for 5s
    print "Schedule recording on channel 1 with start time 4s from now for 5s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':'01','duration':5000,'startTime':4,'recordingId':'RecordIdDevice2','hot':1})
    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    # Schedule hot recordings on same channel
    # Send first recording request from device 3 starting now for 10s
    streamId = '01'
    print "Schedule hot recordings on channel 1 starting now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':2,'streamId':streamId,'duration':10000,'startTime':0,'recordingId':'RecordId03','hot':1})
    # Send second recording request from device 4 starting 5s from now for 10s
    print "Schedule recording on channel 1 starting 5s from now for 10s"
    reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':3,'streamId':streamId,'duration':10000,'startTime':5,'recordingId':'RecordId04','hot':0})
    # Get all Tuner states
    print "Get all Tuner states"
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
