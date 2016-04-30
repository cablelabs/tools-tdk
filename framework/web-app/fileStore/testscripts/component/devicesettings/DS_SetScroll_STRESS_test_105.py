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
  <id>649</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetScroll_STRESS_test_105</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>84</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetScroll</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully change scroll settings value of the front panel continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_105</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_105');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                i = 0;
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling Device Settings - setScroll and getScroll APIs
                        tdkTestObj = obj.createTestStep('DS_SetScroll');
                        #setting scroll class parameters
                        viteration=2;
                        print "Viteration set to:%d" %viteration;
                        hiteration=4;
                        print "Hiteration set to:%d" %hiteration;
                        hold_duration=6;
                        print "Hold duration value set to:%d" %hold_duration;
                        tdkTestObj.addParameter("viteration",viteration);
                        tdkTestObj.addParameter("hiteration",hiteration);
                        tdkTestObj.addParameter("hold_duration",hold_duration);
                        tdkTestObj.addParameter("text","Text");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        scrolldetails = tdkTestObj.getResultDetails();
                        str_viteration="%s" %viteration;
                        str_hiteration="%s" %hiteration;
                        str_hold_duration="%s" %hold_duration;
                        #Check for SUCCESS/FAILURE return value of DS_SetScroll
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the scroll";
                                print "getScroll %s" %scrolldetails;
                                #comparing the scroll parameters before and after setting
                                if ((str_viteration in scrolldetails)and(str_hiteration in scrolldetails)and(str_hold_duration in scrolldetails)):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the scroll details are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "****************%d" %i;
                                        print "FAILURE: Both the scroll details are not same";
                        time.sleep(100/1000);
                        #calling Device Settings - setScroll and getScroll APIs
                        tdkTestObj = obj.createTestStep('DS_SetScroll');
                        #setting scroll class parameters
                        viteration=5;
                        print "Viteration set to:%d" %viteration; 
                        hiteration=6;
                        print "Hiteration set to:%d" %hiteration;
                        hold_duration=10;
                        print "Hold duration value set to:%d" %hold_duration;  
                        tdkTestObj.addParameter("viteration",viteration);
                        tdkTestObj.addParameter("hiteration",hiteration);
                        tdkTestObj.addParameter("hold_duration",hold_duration);
                        tdkTestObj.addParameter("text","Text");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        scrolldetails = tdkTestObj.getResultDetails();
                        str_viteration="%s" %viteration;
                        str_hiteration="%s" %hiteration;
                        str_hold_duration="%s" %hold_duration;
                        #Check for SUCCESS/FAILURE return value of DS_SetScroll
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the scroll";
                                print "getScroll %s" %scrolldetails;
                                #comparing the scroll parameters before and after setting
                                if ((str_viteration in scrolldetails)and(str_hiteration in scrolldetails)and(str_hold_duration in scrolldetails)):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the scroll details are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");

                                        print "FAILURE: Both the scroll details are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "Failure: Failed to get and set scroll details";
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
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
