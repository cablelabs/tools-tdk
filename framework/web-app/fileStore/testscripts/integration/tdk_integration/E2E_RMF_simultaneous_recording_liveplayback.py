'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1683</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_simultaneous_recording_liveplayback</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Simultaneous Record 2 Booked Clear Programme Instances with Live view - Channel Change whilst recording</synopsis>
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
import time;
from tdkintegration import getURL_PlayURL,sched_rec

#Test component to be tested
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
tdk_obj.configureTestCase(ip,port,'E2E_RMF_simultaneous_recording_liveplayback');
rec_obj.configureTestCase(ip,port,'E2E_RMF_simultaneous_recording_liveplayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = rec_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    rec_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");

    #Schedule record for the given StreamID
    result1,recording_id = sched_rec(rec_obj,'01','0','120000');

    #Schedule record for the given StreamID
    result2,recording_id = sched_rec(rec_obj,'02','0','120000');

    #Calling getURL_PlayURL for live playback
    result3 = getURL_PlayURL(tdk_obj,'01');
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()) and ("SUCCESS" in result3.upper()):                                        
        print "Execution Success"
    else:            
        print "Execution failure"
         
    rec_obj.unloadModule("rmfapp");
    tdk_obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load rmfapp module";
    rec_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load TDK module";
    tdk_obj.setLoadModuleStatus("FAILURE");
