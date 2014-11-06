'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1675</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_standbymode_beforeRecording</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>XG1 in standby mode before start of scheduled recording</synopsis>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkintegration import sched_rec
from iarmbus import change_powermode

#Test component to be tested
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");        

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

rec_obj.configureTestCase(ip,port,'E2E_RMF_standbymode_beforeRecording');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_standbymode_beforeRecording');

loadmodulestatus = rec_obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    iarm_obj.setLoadModuleStatus("SUCCESS");
    rec_obj.setLoadModuleStatus("SUCCESS");
    
    actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
        
    #Check for SUCCESS/FAILURE return value of IARMBUS_Init
    if ("SUCCESS" in actualresult):               
        print "SUCCESS :Application successfully initialized with IARMBUS library";
        #calling IARMBUS API "IARM_Bus_Connect"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});    
        
        expectedresult="SUCCESS";
        #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
        if expectedresult in actualresult:                    
            print "SUCCESS: Querying STB power state -RPC method invoked successfully";
            result1 = change_powermode(iarm_obj,1);
            if "SUCCESS" in result1.upper():
                result2 = sched_rec(rec_obj,'01','0','120000');              
        
            # Calling IARM_Bus_DisConnect API
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});                                 
        
        else:
            print "FAILURE: IARM_Bus_Connect failed. %s" %details;
        #calling IARMBUS API "IARM_Bus_Term"
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});            
        
    else:
        print "FAILURE: IARM_Bus_Init failed. %s " %details;             

    #Unload the modules
    iarm_obj.unloadModule("iarmbus");
    rec_obj.unloadModule("rmfapp");
else:
    print"Load module failed";
    #Set the module loading status
    iarm_obj.setLoadModuleStatus("FAILURE");
    rec_obj.setLoadModuleStatus("FAILURE");


