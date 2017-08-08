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
  <id>1124</id>
  <version>1</version>
  <name>RMF_QAMSource_Pause_04</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>RMF_QAMSrc – To Pause the live content when factory method flag is set to false.
Test Case ID: CT_RMF_QAMSrc_MPSink_04.</synopsis>
  <groups_id/>
  <execution_time>16</execution_time>
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
    <test_case_id>CT_RMF_QAMSrc_MPSink_04</test_case_id>
    <test_objective>RMF_QAMSrc – To Pause the live content when factory method flag is set to false.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>monitorRMF.sh
RmfStreamer
Process should be stopped before runing the script.</pre_requisite>
    <api_or_interface_used>rmf_Error init RMFResult RMFQAMSrc::init_platform()                  RMFQAMSrc::disableCaching();             RMFResult init()     RMFResult open()   RMFResult play()          RMFResult pause()
RMFStateChangeReturn getState()
RMFResult close()     RMFResult term()  RMFResult RMFQAMSrc::uninit_platform()              rmf_Error uninit()</api_or_interface_used>
    <input_parameters>rmf_platform Init(): int- argc, char * argv[]            RMFQAMSrc::init_platform() : None                       RMFQAMSrc::disableCaching() : None                           rmfqamsrc Init(): None           open(): char* uri, char* mimetype play(): float speed, double time    pause(): None  
getState():RMFState currentstate, RMFState pendingstate
close(): None              rmfqamsrc Term(): None   RMFQAMSrc::uninit_platform() : None                                rmf_platform Uninit(): None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.Mediaframework agent will call init() of rmfPlaftorm for initializing rmfplatform and get the result.
3.On success, Mediaframework agent will call RMFQAMSrc init_platform() for initializing platform dependent functionalties and get the result.
4.On success, Mediaframework agent will call RMFQAMSrc disableCaching().
5.On success, Mediaframework agent will create the instance of QAMSrc by calling init() and initialize the QAMSrc element.
6.On success, Mediaframework agent will call open() of  QAMSrc element.
7.On success, Mediaframework agent will call play() of  QAMSrc element.
8.On success, Mediaframework agent will call pause() of  QAMSrc element.
9.On success, Mediaframework agent will call close() of  QAMSrc element.
10.On success, Mediaframework agent will call term() and de-initialize the QAMSrc element.
11.On success, Mediaframework agent will call RMFQAMSrc uninit_platform().
12.On success, Mediaframework agent will call rmfplatform uninit().
13.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return values of API's for success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_QAMSource_Pause_04</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;
import time;

expected_Result="SUCCESS"
failure = "FAILURE"

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_QAMSource_Pause_04');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global details
    global tdkTestObj
    #Primitive test case which associated to this Script
    tdkTestObj = testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Open':
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        ocapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(ocapLocator);
        print "OcapLocator:",ocapLocator

    for item in range(len(parametername)):
	print "%s : %s"%(parametername[item],parametervalue[item]);
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep != 'RMF_Element_GetState':
       tdkTestObj.setResultStatus(result);

    print "[%s Execution Result]:  %s" %(teststep,result);
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
                obj.configureTestCase(ip,port,'RMF_QAMSource_Pause_04');
        	#Get the result of connection with test component and STB
        	loadModuleStatus = obj.getLoadModuleResult();
        	print "Re-Load Module Status :  %s" %loadModuleStatus;
        	loadmoduledetails = obj.getLoadModuleDetails();
        	print "Re-Load Module Details : %s" %loadmoduledetails;

if expected_Result in loadModuleStatus.upper():
	#Set module load status
	obj.setLoadModuleStatus("SUCCESS");

        #Prmitive test case which associated to this Script
        #Change the List according to Prmitive test case
        src_parameter=[];
        src_element=[];
        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Init',obj,expected_Result,src_parameter,src_element);
        if expected_Result in result.upper():
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_InitPlatform',obj,expected_Result,src_parameter,src_element);
                if expected_Result in result.upper():
                        src_parameter=["rmfElement","factoryEnable"]
                        src_element=["QAMSrc","false"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["QAMSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                if expected_Result in result.upper():
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,expected_Result,src_parameter,src_element);
                                        if expected_Result in result.upper():
                                                src_parameter=["rmfElement"]
                                                src_element=["MPSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                                if expected_Result in result.upper():
                                                        src_parameter=["rmfElement"]
                                                        src_element=["MPSink"]
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                                        if expected_Result in result.upper():
                                                                src_parameter=["X","Y","width","apply","height"]
                                                                src_element=[0,0,1280,0,720]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,expected_Result,src_parameter,src_element);

                                                                if expected_Result in result.upper():
                                                                        src_parameter=["rmfSourceElement","rmfSinkElement"]
                                                                        src_element=["QAMSrc","MPSink"]
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,expected_Result,src_parameter,src_element);
                                                                        if expected_Result in result.upper():
                                                                                src_parameter=["rmfElement","defaultPlay","playSpeed","playTime"]
                                                                                src_element=["QAMSrc",1,1.0,0.0]
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,expected_Result,src_parameter,src_element);
                                                                                if expected_Result in result.upper():
                                                                                        time.sleep(30);
                                                                                        src_parameter=["rmfElement"]
                                                                                        src_element=["QAMSrc"]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,expected_Result,src_parameter,src_element);
                                                                                        #Change made based on the comment RDKTT-108
                                                                                        #if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                        if expected_Result in result.upper():
                                                                                                print "QAMSource play successful"
                                                                                                tdkTestObj.setResultStatus(result);
                                                                                                src_parameter=["rmfElement"]
                                                                                                src_element=["QAMSrc"]
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                                                                if expected_Result in result.upper():
                                                                                                        time.sleep(5);
                                                                                                        src_parameter=["rmfElement"]
                                                                                                        src_element=["QAMSrc"]
                                                                                                        #result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,expected_Result,src_parameter,src_element);

                                                                                                        #Change made based on the comment RDKTT-108
                                                                                                        #if expected_Result in result.upper() and "PAUSED" in details.upper():
                                                                                                        if expected_Result in result.upper():
                                                                                                                print "QAMSource pause successful"
                                                                                                                #tdkTestObj.setResultStatus(result);
                                                                                                        else:
                                                                                                                print "QAMSource pause failed"
                                                                                                                #tdkTestObj.setResultStatus(failure);

                                                                                        else:
                                                                                                print "QAMSource play failed"
                                                                                                tdkTestObj.setResultStatus(failure);
                                                                src_parameter=["rmfElement"]
                                                                src_element=["MPSink"]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                                        src_parameter=["rmfElement"]
                                                        src_element=["MPSink"]
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                                src_parameter=["rmfElement"]
                                                src_element=["QAMSrc"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                src_parameter=["rmfElement","factoryEnable"]
                                src_element=["QAMSrc","false"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                        src_parameter=[];
                        src_element=[];
                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_UninitPlatform',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Uninit',obj,expected_Result,src_parameter,src_element);
	
	#obj.initiateReboot();
	#Unload Test component
        obj.unloadModule("mediaframework");
else:
	#Set module load status
        obj.setLoadModuleStatus("FAILURE");
