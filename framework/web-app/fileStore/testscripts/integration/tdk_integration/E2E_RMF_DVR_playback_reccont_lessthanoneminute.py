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
  <id>1666</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>11</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_playback_reccont_lessthanoneminute</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Try to playback the recorded content below 1 min from XG1</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <box_type>Emulator-HYB</box_type>
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
import time;
from tdkintegration import sched_rec,dvr_playback;

#Test component to be tested
#rec_obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>                                        

tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_playback_reccont_lessthanoneminute');
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_playback_reccont_lessthanoneminute');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = rec_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;


if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):

    #Set the module loading status
    rec_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");
   
    #Schedule the record for less than a minute
    result1,recording_id = sched_rec(rec_obj,'01','0',duration = "60000");
    
    time.sleep(60);

    tdk_obj.initiateReboot();
    rec_obj.resetConnectionAfterReboot()

    #Prmitive test case which associated to this Script
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #Playback the recorded content
    result2 = dvr_playback(tdkTestObj,recording_id);
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution Success"
    else:            
        print "Execution failure"
         
    #rec_obj.unloadModule("Recorder");
    rec_obj.unloadModule("rmfapp");
    tdk_obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load tdkintegration module";
    tdk_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load rmfapp module";
    rec_obj.setLoadModuleStatus("FAILURE");
