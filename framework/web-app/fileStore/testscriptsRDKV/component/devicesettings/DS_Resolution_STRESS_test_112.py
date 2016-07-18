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
  <id>656</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Resolution_STRESS_test_112</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>83</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully change the Resolution format  continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_112</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
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
obj.configureTestCase(ip,port,'CT_DS_112');
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
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                    tdkTestObj.setResultStatus("SUCCESS");
                    tdkTestObj = obj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    resolutiondetails = tdkTestObj.getResultDetails();
                    #Check for SUCCESS/FAILURE return value of DS_Resolution
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported and default resolutions";
                        print "%s" %resolutiondetails;
                        i = 0;
                        for i in range(0,100):
                            print "****************%d" %i;
                            #calling DS_SetResolution to set and get the display resolutions
                           
                            resolution="480i";
                            print "Resolution value set to:%s" %resolution;
                            if resolution in resolutiondetails:
                                    tdkTestObj = obj.createTestStep('DS_SetResolution');
                                    tdkTestObj.addParameter("resolution",resolution);
                                    tdkTestObj.addParameter("port_name","HDMI0");
                                    expectedresult="SUCCESS"
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult = tdkTestObj.getResult();
                                    resolutiondetails1 = tdkTestObj.getResultDetails();
                                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                                    if expectedresult in actualresult:
                                        print "SUCCESS:set and get resolution Success";
                                        print "getresolution %s" %resolutiondetails1;
                                        #comparing the resolution before and after setting
                                        if resolution in resolutiondetails1 :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Both the resolutions are same";
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Both the resolutions are not same";
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "****************%d" %i;
                                        print "FAILURE:set and get resolution fails";
                            else:
                                    print "FAILURE:Requested resolution are not supported by this device";            
                            time.sleep(100/1000);
                            #calling DS_SetResolution to set and get the display resolutions
                            
                            resolution="720p";
                            print "Resolution value set to:%s" %resolution;
                            if resolution in resolutiondetails:
                                tdkTestObj = obj.createTestStep('DS_SetResolution');
                                tdkTestObj.addParameter("resolution",resolution);
                                tdkTestObj.addParameter("port_name","HDMI0");
                                expectedresult="SUCCESS"
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                resolutiondetails2 = tdkTestObj.getResultDetails();
                                #Check for SUCCESS/FAILURE return value of DS_SetResolution
                                if expectedresult in actualresult:
                                    print "SUCCESS:set and get resolution Success";
                                    print "getresolution %s" %resolutiondetails2;
                                    #comparing the resolution before and after setting
                                    if resolution in resolutiondetails2 :
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print "SUCCESS: Both the resolutions are same";
                                    else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print "FAILURE: Both the resolutions are not same";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "****************%d" %i;
                                    print "FAILURE:set and get resolution fails";                        
                            else:
                                print "FAILURE:Requested resolution are not supported by this device";        
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the list of supported resolutions";                
                
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
                    print "FAILURE:Connection Failed";                         
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
