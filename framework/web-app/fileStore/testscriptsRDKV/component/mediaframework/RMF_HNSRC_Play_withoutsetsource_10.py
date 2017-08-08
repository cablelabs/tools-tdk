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
  <id>905</id>
  <version>1</version>
  <name>RMF_HNSRC_Play_withoutsetsource_10</name>
  <primitive_test_id>495</primitive_test_id>
  <primitive_test_name>RMF_Element_Init</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>ALLOCATED</status>
  <synopsis>These Script tests the RDK Mediaframework HNSrc element to set play with out  sink connected. 
Test Case ID: CT_RMF_HNSource_10.</synopsis>
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
    <test_case_id>CT_RMF_HNSource_10</test_case_id>
    <test_objective>RMF_HNSrc – Without connecting sink element, play the HNSrc element</test_objective>
    <test_type>Negative</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>init()
Open()
Play()
term()</api_or_interface_used>
    <input_parameters>init:  None
Open: char* -url ,char*-mimetype
Play:float -speed,double -time
term: None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.mediaframework agent will create the instance for Hnsrc and  initialize the Hnsrc element.
3.mediaframework agent will open the  Hnsrc element with http url string for url parameter
4.mediaframework agent will play the  Hnsrc element with default speed
4.mediaframework agent will terminate the  Hnsrc element .
5..For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_HNSRC_Play_withoutsetsource_10</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
import tdklib;
import mediaframework;
src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_HNSRC_Play_withoutsetsource_10');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    if teststep == "RMF_Element_Play":
        expectedresult ="FAILURE"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    if teststep == "RMF_Element_Play":
        if "FAILURE" in result.upper():
                result = "SUCCESS";
        else:
                result = "FAILURE";

    print "RMF_Element Status:  %s" %result;
    tdkTestObj.setResultStatus(result);
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
                obj.configureTestCase(ip,port,'RMF_HNSRC_Play_withoutsetsource_10');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if Expected_Result in loadModuleStatus.upper():

        #Prmitive test case which associated to this Script
        obj.setLoadModuleStatus("SUCCESS");
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Init status:  %s" %result;
                if Expected_Result in result.upper():
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,Expected_Result,open_parameter_name,open_parameter_value);
                        if Expected_Result in result.upper():
                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Term status:  %s" %result;
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Term status:  %s" %result;
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
