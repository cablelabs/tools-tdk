'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>10</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_Set_Resolution_During_Standby</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test to change the resolution during Standby Mode</synopsis>
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
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode

def SetResolution(obj):
        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                        tdkTestObj.setResultStatus("SUCCESS");
                        #calling DS_Resolution get list of supported resolutions and the default resolution
                        tdkTestObj = obj.createTestStep('DS_Resolution');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="FAILURE"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        resolutiondetails = tdkTestObj.getResultDetails();
                        print "%s" %resolutiondetails;
                        #Check for SUCCESS/FAILURE return value of DS_Resolution
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application was unable to get the list of supported and default resolutions";
                                retval="SUCCESS";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE :Application was able to get the list of supported resolutions";
                                retval="FAILURE";
                        #calling DS_SetResolution to set and get the display resolution as 720p    
                        resolution="720p";
                        print "Resolution value set to:%s" %resolution;
                        if resolution in resolutiondetails:
                                tdkTestObj = obj.createTestStep('DS_SetResolution');
                                tdkTestObj.addParameter("resolution",resolution);
                                tdkTestObj.addParameter("port_name","HDMI0");
                                expectedresult="FAILURE"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                resolutiondetails = tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of DS_SetResolution
                                if expectedresult in actualresult:
                                        print "SUCCESS:set and get resolution fails to execute during STANDBY";
                                        print "getresolution %s" %resolutiondetails;
                                        #comparing the resolution before and after setting
                                        if resolution in resolutiondetails :
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "FAILURE: Both the resolutions are same and resolution is set during standby";
                                                retval="FAILURE";
                                        else:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print "SUCCESS: Both the resolutions are not same";
                                                retval="SUCCESS";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE:set and get resolution API executes successfully during STANDBY";
                                        retval="FAILURE";
                        else:
                                print "FAILURE:Requested resolution are not supported by this device";
                                #calling DS_ManagerDeInitialize to DeInitialize API
                                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                                if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Deinitalize failed" ;
                                        retval="FAILURE";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:Connection Failed";
                        retval="FAILURE";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
                retval="FAILURE";
        return retval;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_Set_Resolution_During_Standby');
iarm_obj.configureTestCase(ip,port,'E2E_Set_Resolution_During_Standby');
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper() and ("SUCCESS" in loadmodulestatus1.upper()):
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        iarm_obj.setLoadModuleStatus("SUCCESS");
        print "SUCCESS: Querying STB power state -RPC method invoked successfully";
        result1 = change_powermode(iarm_obj,1);
        if "SUCCESS" in result1.upper():
                result2=SetResolution(obj);
                                              
        change_powermode(iarm_obj,2);                    
        
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
        iarm_obj.unloadModule("iarmbus");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");