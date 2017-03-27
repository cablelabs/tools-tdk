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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_VideoApplicationEventsService_SetEnableDisable_13978_3</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_VideoApplicationEventsService_IsEnableEvent</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if Video Application events service can be enabled and disabled</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <except_output></except_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import servicemanager;

#Test component to be tested
smObj = tdklib.TDKScriptingLibrary("servicemanager","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
smObj.configureTestCase(ip,port,'SM_VideoApplicationEventsService_SetEnableDisable_13978_3');

#Get the result of connection with test component and STB
smLoadStatus =smObj.getLoadModuleResult();
print "[SM LIB LOAD STATUS]  :  %s" %smLoadStatus;

if "SUCCESS" in smLoadStatus.upper():
        serviceName = "org.openrdk.videoApplicationEvents_1";
        #Register Service
        register = servicemanager.registerService(smObj,serviceName);

        if "SUCCESS" in register:
                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_SetEnable');
                valueToSetEnabled = 1;
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        resultDetails = tdkTestObj.getResultDetails();
                        print "Event enabling status: %s\n" %resultDetails;
                        #Prmitive test case which associated to this Script
                        tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_IsEnableEvent');
                        expectedresult = "SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                resultDetails = tdkTestObj.getResultDetails();
                                if valueToSetEnabled == int(resultDetails):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Video application event service enabled successfully\n";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "video application ervice event enabling failed\n";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to check event enable status\n";

                else:
                        print "Failed to set event enable status";
                        tdkTestObj.setResultStatus("FAILURE");

                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_SetEnable');
                valueToSetEnabled = 0;
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        resultDetails = tdkTestObj.getResultDetails();
                        print "Event enabling status: %s\n" %resultDetails;
                        #Prmitive test case which associated to this Script
                        tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_IsEnableEvent');
                        expectedresult = "SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                resultDetails = tdkTestObj.getResultDetails();
                                if valueToSetEnabled == int(resultDetails):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Video application event service Disabled successfully\n";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "video application service event disabling failed\n";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to check event enable status\n";

                else:
                        print "Failed to set event enable status";
                        tdkTestObj.setResultStatus("FAILURE");

                #Prmitive test case which associated to this Script
                tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_SetEnable');
                valueToSetEnabled = 1;
                expectedresult = "SUCCESS";
                tdkTestObj.addParameter("valueToSetEnabled",valueToSetEnabled);
                tdkTestObj.executeTestCase(expectedresult);
                #Get the result of execution
                actualresult = tdkTestObj.getResult();
                if expectedresult in actualresult:
                        resultDetails = tdkTestObj.getResultDetails();
                        print "Event enabling status: %s\n" %resultDetails;
                        #Prmitive test case which associated to this Script
                        tdkTestObj = smObj.createTestStep('SM_VideoApplicationEventsService_IsEnableEvent');
                        expectedresult = "SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                resultDetails = tdkTestObj.getResultDetails();
                                if valueToSetEnabled == int(resultDetails):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "Video application event service enabled successfully\n";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "video application ervice event enabling failed\n";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to check event enable status\n";

                else:
                        print "Failed to set event enable status";
                        tdkTestObj.setResultStatus("FAILURE");
                
		unregister = servicemanager.unRegisterService(smObj,serviceName);
        smObj.unloadModule("servicemanager");
else:
#         tdkTestObj.setResultStatus("FAILURE");
         print "Failed to load service manager module\n";


					
