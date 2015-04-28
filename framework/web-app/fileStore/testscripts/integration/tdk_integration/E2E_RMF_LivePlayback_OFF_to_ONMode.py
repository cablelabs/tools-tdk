'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LivePlayback_OFF_to_ONMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To Verify Live Playback During and After STB from OFF mode</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from iarmbus import change_powermode
from tdkintegration import getURL_PlayURL

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();
print "Tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper() and ("SUCCESS" in loadmodulestatus1.upper()):
        obj.setLoadModuleStatus("SUCCESS");
        iarm_obj.setLoadModuleStatus("SUCCESS");
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
                #Setting Power mode to OFF
                result1 = change_powermode(iarm_obj,0);
                if "SUCCESS" in result1.upper():
                    result2= getURL_PlayURL(obj,'01');
                    #Setting Power mode to ON
                    result3 = change_powermode(iarm_obj,2);
                    if "SUCCESS" in result3.upper():
                        result4 = getURL_PlayURL(obj,'01');
                    
            
                # Calling IARM_Bus_DisConnect API
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});                                 
            
            else:
                print "FAILURE: IARM_Bus_Connect failed. %s" %details;
            #calling IARMBUS API "IARM_Bus_Term"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});            
            
        else:
            print "FAILURE: IARM_Bus_Init failed. %s " %details;
        print "Tdkintegration module loaded successfully";
        obj.unloadModule("tdkintegration");
        iarm_obj.unloadModule("iarmbus");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
         iarm_obj.setLoadModuleStatus("FAILURE");
				
