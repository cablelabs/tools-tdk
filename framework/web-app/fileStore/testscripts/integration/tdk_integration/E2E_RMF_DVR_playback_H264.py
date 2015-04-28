'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1668</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_playback_H264</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Try to playback H264 record in  (XI3)</synopsis>
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
    <box_type>Terminal-RNG</box_type>
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
import re;
from tdkintegration import sched_rec,dvr_playback;

#Test component to be tested
#rec_obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>


tdk_obj.configureTestCase(ip,port,'E2E_RMF_playback_H264');
rec_obj.configureTestCase(ip,port,'E2E_RMF_playback_H264');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = rec_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    rec_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");
   
    #Schedule the record for the radio channel
    result1,recording_id = sched_rec(rec_obj,'09','0','120000');
    
    time.sleep(180);

    #Prmitive test case which associated to this Script
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #Playback the radio channel
    result2 = dvr_playback(tdkTestObj,recording_id);
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution Success"
    else:            
        print "Execution failure"
         
    #rec_obj.unloadModule("Recorder");
    rec_obj.unloadModule("rmfapp");
    tdk_obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load rmfapp module";
    rec_bj.setLoadModuleStatus("FAILURE");
    print "Failed to load tdkintegration module"
    tdk_bj.setLoadModuleStatus("FAILURE");
