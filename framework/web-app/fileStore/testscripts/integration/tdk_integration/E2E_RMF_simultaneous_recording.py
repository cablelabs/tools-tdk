'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1680</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_simultaneous_recording</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Simultaneous Record 2 Clear Programme Instances with no Live view</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
from tdkintegration import sched_rec

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
obj.configureTestCase(ip,port,'E2E_RMF_simultaneous_recording');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "Recorder module loading status :%s" %result ;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "Recorder module load successfully";      

    #Schedule record for the given StreamID
    result1,recording_id = sched_rec(obj,'01','0','120000');

    #Schedule record for the given StreamID
    result2,recording_id = sched_rec(obj,'02','0','120000');
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution  Success"
    else:            
        print "Execution  failure"
         
    #unloading Recorder module
    obj.unloadModule("rmfapp");
    
else:
    print "Failed to load rmfapp module";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
