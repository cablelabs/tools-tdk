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
  <id>202</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetCompression test_11</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>78</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetCompression</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the Compression Format of Audio Test Case ID : CT_DS_11.Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS.</synopsis>
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
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_11');
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
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_GetSupportedCompression get list of compressions.
                tdkTestObj = obj.createTestStep('DS_GetSupportedCompressions');
                tdkTestObj.addParameter("port_name","HDMI0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                compressiondetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedCompression
                if expectedresult in actualresult:
                       tdkTestObj.setResultStatus("SUCCESS");
                       print "SUCCESS :Application successfully gets the list compression supported";
                       print "%s" %compressiondetails
                else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "FAILURE :Failed to get supported compression list";
                #calling DS_SetCompression to get and set the compression
                tdkTestObj = obj.createTestStep('DS_SetCompression');
                compression="MEDIUM";
                print "Compression value set to:%s" %compression;
                tdkTestObj.addParameter("compression_format",compression);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                compressiondetails = tdkTestObj.getResultDetails();
                setcompression = "Compression format:%s" %compression;
                #Check for SUCCESS/FAILURE return value of DS_SetCompression
                print "compression:%s" %compressiondetails;
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully get and set the compression";
                        print "setcompression: %s" %setcompression;
                        print "getcompression: %s" %compressiondetails;
                        #comparing compression before and after setting
                        if compression in compressiondetails:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the compression formats are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the compression formats are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Application failed to set and get the compression formats";
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
