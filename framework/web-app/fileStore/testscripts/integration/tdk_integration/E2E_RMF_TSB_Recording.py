'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1676</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_TSB_Recording</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Set a recording while TSB is present on the tuned program</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>12</execution_time>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
from tdkintegration import TSB_play,sched_rec

#Test component to be tested
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");    
     
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_TSB_Recording');
rec_obj.configureTestCase(ip,port,'E2E_RMF_TSB_Recording');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = rec_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    rec_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");       
    
    #calling TSB_play to play the given program with TSB
    result1 = TSB_play(tdk_obj,'01');
    
    #Calling sched_rec to schedule the  record with TSB
    result2,recording_id = sched_rec(rec_obj,'01','0','120000');
    tdk_obj.initiateReboot();
    rec_obj.resetConnectionAfterReboot()

    time.sleep(120);    
    
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()) :
        print "Execution Success";
    else:
        print "Execution Failure";               

    #Unload the modules
    print "Before unloaded the rmfapp module"
    rec_obj.unloadModule("rmfapp");
    print "Successfully unloaded the rmfapp module"
    tdk_obj.unloadModule("tdkintegration");
    print "Successfully unloaded the tdkintegration module"
    
    
else:
    print"Load module failed";
    #Set the module loading status
    rec_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");   
    


