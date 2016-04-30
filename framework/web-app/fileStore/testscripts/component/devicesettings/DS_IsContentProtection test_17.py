#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ===========================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>255</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_IsContentProtection test_17</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>101</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_IsContentProtected</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script checks for Content Protection support of Video Output Port
Test Case ID : CT_DS_17</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
from devicesettings import dsManagerInitialize,dsManagerDeInitialize;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load module to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'CT_DS_17');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Initialize Device Settings
        result = dsManagerInitialize(obj)
        #Check for return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check if Content is Protected
                tdkTestObj = obj.createTestStep('DS_IsContentProtected')
                tdkTestObj.addParameter("port_name",'HDMI0')
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult)
                actualresult = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                print "Details: [%s]"%details
                #Check for return value of DS_IsContentProtected
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS")
                else:
                        tdkTestObj.setResultStatus("FAILURE")
                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(obj)
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
