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
  <id>854</id>
  <version>1</version>
  <name>RMF_DVRSrc_Open_13</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>This script tests the RDK Mediaframework DVRSrc element to call Open API by passing valid url but invalid record_id as input to its url parameter and Close a DVRsource element.
Test Case ID: CT_RMF_DVRSrc_13.
Test Type: Negative.</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_DVRSrc_13</test_case_id>
    <test_objective>RMF_DVRSrc  – To call Open API by passing valid url but invalid record_id as input to its url parameter and Close a DVRsource element.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>RMFResult init()     
RMFResult open()  
RMFResult close()
RMFResult    term()</api_or_interface_used>
    <input_parameters>Init(): None   
open():char*-dvr locator(invalidurl),char*- mimetype(NULL)
close():None 
term(): None</input_parameters>
    <automation_approch>1. TM loads mediaframework agent via the test agent.
2. Mediaframework agent will create the instance for DVRSrc and  initialize the DVRSrc element.
3. Mediaframework agent will open the DVRSrc element with the valid url being framed with dvrlocator (Ex: dvr://local/record_id#segment number i.e, dvr://local/390206#0).
4. Mediaframework agent will close the DVRSrc element.
5. Mediaframework agent will terminate the  DVRSrc element.
6. For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
Checkpoint 2. Check the return value of open API  “RMF_RESULT_INVALID_ARGUMENT” for success.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_DVRSrc_Open_13</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import mediaframework;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRSrc_Open_13');

expected_Result="SUCCESS"
expected_Failure = "FAILURE"

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Open':
        parametername.append("url");
        #Invalid recordID
        recordID = "00000000"        
        dvrLocator = "dvr://local/" + recordID + "#0"
        print dvrLocator
        parametervalue.append(dvrLocator);

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep == 'RMF_Element_Open':
        if expected_Failure in result:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus(result);

    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;

    return result

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
                obj.configureTestCase(ip,port,'RMF_DVRSrc_Open_13');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;


if expected_Result in loadModuleStatus.upper():
        #Prmitive test case which associated to this Script
        #Change the List according to Prmitive test case
        src_parameter=["rmfElement"]
        src_element=["DVRSrc"]
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
        if expected_Result in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                if expected_Result in result.upper():
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["DVRSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                src_parameter=["rmfElement"]
                src_element=["DVRSrc"]
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
