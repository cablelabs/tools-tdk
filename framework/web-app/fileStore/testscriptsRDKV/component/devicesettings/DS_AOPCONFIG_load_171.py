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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_AOPCONFIG_load_171</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_AOPCONFIG_load</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective:
Test Case ID: CT_DS_171
Test Type: Positive</synopsis>
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'DS_AOPCONFIG_load_171');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper())

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

                tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPorts');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
		portDetails = tdkTestObj.getResultDetails();
                print "[TEST EXECUTION RESULT] : %s" %actualresult;
                print "Details: [%s]"%portDetails;
		if expectedresult in actualresult:
			tdkTestObj.setResultStatus("SUCCESS");
		else:
			tdkTestObj.setResultStatus("FAILURE");
			
                #calling Device Settings - Audio Release.
                tdkTestObj = obj.createTestStep('DS_AOPCONFIG_release');
                expectedresult="SUCCESS"
                print " "
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails()
                print "[DS_AOPCONFIG_release RESULT] : %s" %actualresult;
                print "[DS_AOPCONFIG_release DETAILS] : %s" %details;

                #Check for SUCCESS/FAILURE return value of DS_AOPCONFIG_release
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get DS_AOPCONFIG_release";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get DS_AOPCONFIG_release"

                #calling Device Settings - Audio Load.
                tdkTestObj = obj.createTestStep('DS_AOPCONFIG_load');
                expectedresult="SUCCESS"
                print " "
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                loadDetails = tdkTestObj.getResultDetails()
                print "[DS_AOPCONFIG_load RESULT] : %s" %actualresult;
                print "[DS_AOPCONFIG_load DETAILS] : %s" %loadDetails;

                #Check for SUCCESS/FAILURE return value of DS_AOPCONFIG_load
                if expectedresult in actualresult:
			if portDetails == loadDetails:
				tdkTestObj.setResultStatus("SUCCESS");
			else:
				tdkTestObj.setResultStatus("FAILURE");
				print "Audio output ports not loaded correctly"
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                print " "
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;

                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
