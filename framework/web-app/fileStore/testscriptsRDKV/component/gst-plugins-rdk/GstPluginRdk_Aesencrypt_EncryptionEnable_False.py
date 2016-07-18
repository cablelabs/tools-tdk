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
  <id>1462</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>GstPluginRdk_Aesencrypt_EncryptionEnable_False</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>612</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Gst_Aesencrypt_EncryptEnable_Set_Prop</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective:To set the aesencrypt plugin property, "encryption-enable" with false to disable encryption of mpegts packets.
Test CaseID:CT_GST_PLUGINS_RDK_19.
Test Type: Positive.</synopsis>
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
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("gstpluginsrdk","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'GstPluginRdk_Aesencrypt_EncryptionEnable_False');

#Get the result of connection with test component and STB
loadStatusResult =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadStatusResult;

loadStatusExpected = "SUCCESS"

if loadStatusExpected not in loadStatusResult.upper():
        print "[Failed To Load gstPluginsRdk Module]"
        print "[Exiting the Script]"
        exit();

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('Gst_Aesencrypt_EncryptEnable_Set_Prop');

expectedResult = "SUCCESS"

#Set the encryption-enable_False
#1 = true, 0 = false
value = 0;
tdkTestObj.addParameter("propValue",value)

#Execute the test case in STB
tdkTestObj.executeTestCase(expectedResult);

#Get the result of execution
result = tdkTestObj.getResult();
print "[TEST EXECUTION RESULT] : %s" %result;
details = tdkTestObj.getResultDetails();
print "[TEST EXCEUTION DETAILS] : %s"%details;

tdkTestObj.setResultStatus(result);
obj.unloadModule("gstpluginsrdk");	
