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
  <name>SM_FP_Is_24Hours_Disable_16066_4</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_FP_Is_24_Hour_Clock</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
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
    <box_type>Hybrid-5</box_type>
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
  <script_tags />
</xml>
'''
																								# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
dsobj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'SM_FP_Is_24Hours_Disable_16066_4');
dsobj.configureTestCase(ip,port,'SM_FP_Is_24Hours_Disable_16066_4');

loadmodulestatus1 =dsobj.getLoadModuleResult();
#Get the result of connection with test component and STB
loadmodulestatus=obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");
    dsobj.setLoadModuleStatus("SUCCESS");
    result = devicesettings.dsManagerInitialize(dsobj)
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
    #Prmitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('SM_FP_Set_24_Hour_Clock');
            expectedresult="SUCCESS"
            is_24hour=0;
            tdkTestObj.addParameter("is24hour",is_24hour);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of SM_FP_Set_24Hours
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully unset to 24hours";
                #Primitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('SM_FP_Is_24_Hour_Clock');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of SM_FP_Is_24_Hour_Clock
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS :Application successfully checked is_24_hour_clock";
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Application Failed to execute SM_FP_Is_24_Hour_clock API";
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Application Failed to execute SM_FP_Set24Hour_clock API";
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
                
                    

					

					

					

					