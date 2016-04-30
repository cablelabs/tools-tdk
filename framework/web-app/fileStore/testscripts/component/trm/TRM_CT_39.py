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
  <id>1695</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_39</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>613</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests creating conflict by recording channel 6 on (L1-L2-Hot R3-Hot R4-Hot R5) and cancel L1 and record ch 6 again and check its state. 
Test Case ID: CT_TRM_39
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_39');
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

    duration = 10000
    startTime = 0

    # Step1: Start live tuning two different channels on first 2 tuners
    for deviceNo in range(0,2):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        trm.reserveForLive(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':duration,'startTime':startTime})

    # Step2: Start hot recording different channels on all the tuners except 2 tuners
    for deviceNo in range(2,maxTuner):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':1})

    # Step3: Start creating conflict by hot recording new channel
    deviceNo = maxTuner
    streamId = '0'+str(deviceNo+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,"FAILURE",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':1})

    # Step4: Release live reservation on channel 1 on device1
    trm.releaseReservation(obj,"SUCCESS",kwargs={'deviceNo':0,'activity':1,'streamId':'01'})

    # Step5: Start hot recording new channel again
    deviceNo = maxTuner
    streamId = '0'+str(deviceNo+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':1})

    # Get all Tuner states
    trm.getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
