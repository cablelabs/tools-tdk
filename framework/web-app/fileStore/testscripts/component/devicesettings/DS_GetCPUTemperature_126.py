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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_GetCPUTemperature_126</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_GetCPUTemperature</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script gets the STB CPU Temperature.
Test Case ID : CT_DS_126</synopsis>
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
    <box_type>IPClient-4</box_type>
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

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_GetCPUTemperature_126');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling Device Setting - Get CPU Temperature
                dsTestObj = dsObj.createTestStep('DS_GetCPUTemperature');
                expectedresult = "SUCCESS"
                dsTestObj.executeTestCase(expectedresult);
                actualresult = dsTestObj.getResult();
                details = dsTestObj.getResultDetails();
                print "Result : [%s] "%actualresult,
                #Check for SUCCESS/FAILURE return value of DS_GetCPUTemperature
                if expectedresult in actualresult:
                        print "Details : [+%sC]" %details;
                        if ((float(details) <= float(0)) or (float(details) > float(125))):
                                print "Temperature out of range";
                                dsTestObj.setResultStatus("FAILURE");
                        else:
                                dsTestObj.setResultStatus("SUCCESS");
                else:
                        dsTestObj.setResultStatus("FAILURE");
                        print "Details : [%s]" %details;
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
