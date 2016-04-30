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
  <id>1664</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_34</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>636</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_CancelRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests recording channel 6 when current state of reservation is (R1-R2-R3-R4-R5), cancel recording channel 1 and again start recording channel 6.
Test Case ID: CT_TRM_34
Test Type: Negative</synopsis>
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
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import trm;
from time import sleep;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_34');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
obj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Fetch max tuners supported
    maxTuner = trm.getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Step1: Start recording on all the tuners available
    for deviceNo in range(0,maxTuner):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step2: Record a new channel when all tuners are already busy recording
    streamId = '0'+str(maxTuner+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,'FAILURE',kwargs={'deviceNo':maxTuner,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step3: Cancel recording on channel 1
    trm.cancelRecording(obj,'SUCCESS',kwargs={'streamId':'01'})

    # Step4: Record the new channel again
    trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':maxTuner,'streamId':streamId,'duration':20000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Add sleep to release all reservations
    sleep(20)

    #unloading trm module
    obj.unloadModule("trm");
