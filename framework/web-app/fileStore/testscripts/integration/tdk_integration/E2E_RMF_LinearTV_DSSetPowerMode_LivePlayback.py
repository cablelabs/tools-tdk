'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1583</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check the DS set power state while live playback. E2E_LinearTV_15</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkintegration import getURL_PlayURL;

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
dev_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");


#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback');
dev_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_DSSetPowerMode_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = dev_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    dev_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");        

    #calling getURL_PlayURL to get and play the URL
    result = getURL_PlayURL(tdk_obj,'01');              
        
    if "SUCCESS" in result:     
                
        #calling DS_ManagerInitialize to Intialize API.
        actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerInitialize', 'SUCCESS',verifyList ={});
                
        powermode=0;
        print "Power Mode value set to:%s" %powermode;                               
           
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in actualresult:
                    
            #calling DS_SetPowerMode to set the power mode of STB
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_SetPowerMode', 'SUCCESS', verifyList ={'new_power_state': str(powermode)},new_power_state = powermode);
                   
            #calling DS_ManagerDeInitialize to DeInitialize API
            actualresult,tdkTestObj_dev,details = tdklib.Create_ExecuteTestcase(dev_obj,'DS_ManagerDeInitialize', 'SUCCESS',verifyList ={});
                
        else:
            tdkTestObj_dev.setResultStatus("FAILURE");
            print "FAILURE :DS Manager Intialize";         
              
    else:                
        print "FAILURE: getURL_PlayURL function"; 
        
    #Unload the deviceSettings module
    dev_obj.unloadModule("devicesettings");
    tdk_obj.unloadModule("tdkintegration");
else:
    print"Load module failed";
    #Set the module loading status
    dev_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");


