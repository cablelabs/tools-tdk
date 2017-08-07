#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ===========================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_FP_setLED_min_2424</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_FP_SetLED</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>SM_FP_setLED_min_value
RDK-2424</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
dsobj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_FP_setLED_min_2424');
dsobj.configureTestCase(ip,port,'SM_FP_setLED_min_2424');
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =dsobj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        dsobj.setLoadModuleStatus("SUCCESS");
        result = devicesettings.dsManagerInitialize(dsobj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                    #calling ServiceManger - registerService API
                    tdkTestObj = obj.createTestStep('SM_RegisterService');
                    expectedresult="SUCCESS"
                    serviceName="FrontPanelService";
                    tdkTestObj.addParameter("service_name",serviceName);
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    #Check for SUCCESS/FAILURE return value of SM_RegisterService
                    if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS :Application successfully registered a service with serviceManger";
                            tdkTestObj = obj.createTestStep('SM_FP_SetAPIVersion');
                            expectedresult="SUCCESS"
                            apiVersion=5;
                            tdkTestObj.addParameter("apiVersion",apiVersion);
                            
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            apiversiondetail =tdkTestObj.getResultDetails();
                            print "[EXECUTION DETAILS] APi Version : %s"%apiversiondetail;
                            print "Registered Service:%s" %serviceName;
                            tdkTestObj = obj.createTestStep('SM_FP_SetLED');
                            expectedresult="SUCCESS"
                            RedColor = 1;
                            BlueColor = 1;
                            GreenColor = 1;
                            setbrightness = 1;
                            tdkTestObj.addParameter("LEDName","power_led");
                            tdkTestObj.addParameter("LEDColorRed",RedColor);
                            tdkTestObj.addParameter("LEDColorBlue",BlueColor);
                            tdkTestObj.addParameter("LEDColorGreen",GreenColor);
                            tdkTestObj.addParameter("LEDBrightness",setbrightness);
                            print "RedColor = %d, BlueColor = %d , GreenColor =%d , setbrightness = %d"%(RedColor,BlueColor,GreenColor,setbrightness);
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult= tdkTestObj.getResult();
                            brightnessdetails= tdkTestObj.getResultDetails();
                            #Check for SUCCESS/FAILURE return value of SM_DisplaySetting_SetbrightnessSettings
                            if expectedresult in actualresult:
                                    print "SUCCESS: Application succesfully executes SM_FP_SetLED API";
                                    print brightnessdetails;
                            else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "FAILURE: Application Failed to execute SM_FP_SetLED API";
                            # calling SM_UnRegisterService to unregister service
                            tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                            expectedresult="SUCCESS"
                            tdkTestObj.addParameter("service_name",serviceName);
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                            if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "SUCCESS :Application successfully unRegisteres a service";
                            else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "FAILURE: Failed to unRegister the service" ;
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE: Application failed to register a service";
          

                    result = devicesettings.dsManagerDeInitialize(dsobj)
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
        dsobj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
        dsobj.setLoadModuleStatus("FAILURE");
				
