# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>900</id>
  <version>1</version>
  <name>RMF_HNSrc_Open_invalidurl_07</name>
  <primitive_test_id>495</primitive_test_id>
  <primitive_test_name>RMF_Element_Init</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>These Script tests the RDK Mediaframework HNSrc element to set the invalid string in to open method of RMF.
Test Case ID: CT_RMF_HNSource_07.</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_HNSource_07</test_case_id>
    <test_objective>RMF_HNSrc – Passing some invalid string,which doesnt start with http  , in to HNSource open method</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>init()
Open()
term()</api_or_interface_used>
    <input_parameters>init:  None
Open: char* -url ,char*-mimetype
term: None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.mediaframework agent will create the instance for Hnsrc and  initialize the Hnsrc element.
3.mediaframework agent will open the  Hnsrc element with invalid string which doesnt have http in to it for url parameter.
4.mediaframework agent will terminate the  Hnsrc element .
5..For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_HNSrc_Open_invalidurl_07</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj = testobject.createTestStep(teststep);

    for item in range(len(parametername)):
        print "%s : %s" %(parametername[item],parametervalue[item]);
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();

    if expectedresult in result.upper():
	tdkTestObj.setResultStatus("SUCCESS");
    else:
	tdkTestObj.setResultStatus("FAILURE");

    print "Status of "+ teststep+":  %s" %result;
    return result

#Load Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSrc_Open_invalidurl_07');
#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_HNSrc_Open_invalidurl_07');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in loadModuleStatus.upper():
	#Set module load status
	obj.setLoadModuleStatus("SUCCESS");

	src_element=["HNSrc"]
	src_parameter=["rmfElement"]
	open_parameter_name=["rmfElement","url"]
	open_parameter_value=["HNSrc",""]

        #Prmitive test case which associated to this Script
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,"SUCCESS",src_parameter,src_element);
        if "SUCCESS" in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,"SUCCESS",src_parameter,src_element);
                if "SUCCESS" in result.upper():
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,"FAILURE",open_parameter_name,open_parameter_value);
			if "SUCCESS" in result.upper():
				result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,"SUCCESS",src_parameter,src_element);
                	result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,"SUCCESS",src_parameter,src_element);
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,"SUCCESS",src_parameter,src_element);

	#Unload Test component
        obj.unloadModule("mediaframework");
else:
	#Set module load status
        obj.setLoadModuleStatus("FAILURE");
