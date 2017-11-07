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
  <id>1157</id>
  <version>1</version>
  <name>RMF_QAMSrc_HNSink_04</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>RMF_QAMSrc – To Stream out the live content through HNSink on to the network when factory method flag is set to false and when dtcp_enabled is true.
Test Case ID: CT_RMF_QAMSrc_HNSink_04
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>14</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_QAMSrc_HNSink_04</test_case_id>
    <test_objective>RMF_QAMSrc – To Stream out the live content through HNSink on to the network when factory method flag is set to false and when dtcp_enabled is set to true(Data pushed onto the network is encrypted)..</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>


monitorRMF.sh
RmfStreamer
Process should be stopped before runing the script.
Streaming should be happening.</pre_requisite>
    <api_or_interface_used>rmf_Error init RMFResult RMFQAMSrc::init_platform()        RMFQAMSrc::disableCaching();  RMFResult init()     
RMFResult open()   
RMFResult play() 
RMFStateChangeReturn getState()
RMFResult close()     RMFResult term()  RMFResult RMFQAMSrc::uninit_platform()    rmf_Error uninit()


HNSink::init_platform()
Init()
SetHNSinkProperties()
SetSourceType()
SetSource()
Term()
HNSink::uninit_platform()</api_or_interface_used>
    <input_parameters>rmf_platform Init(): int- argc, char * argv[]            RMFQAMSrc::init_platform() : None                       RMFQAMSrc::disableCaching() : None                           rmfqamsrc Init(): None           open(): char* uri, char* mimetype play(): float speed, double time   
getState():RMFState currentstate, RMFState pendingstate
close(): None              rmfqamsrc Term(): None   RMFQAMSrc::uninit_platform() : None                                rmf_platform Uninit(): None

HNSink::init_platform(): None
SetHNSinkProperties(): HNSinkProperties_t properties
SetSourceType(): char* sourcetype
SetSource(): RMFMediaSourceBase*
HNSink::uninit_platform():  None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.Mediaframework agent will call init() of rmfPlaftorm for initializing rmfplatform and get the result.
3.On success, Mediaframework agent will call RMFQAMSrc init_platform() for initializing platform dependent functionalties and get the result.
4.On success, Mediaframework agent will call RMFQAMSrc disableCaching().
5.On success, Mediaframework agent will create the instance of QAMSrc by calling init() and initialize the QAMSrc element.
6.On success, Mediaframework agent will call open() of  QAMSrc element.
7.On success, Mediaframework agent will call HNSink init_platform().
8. On success, Mediaframework agent will call HNSink  setProperties() and the attributes.
9. On success, Mediaframework agent will call HNSink  base class init() to initialize the hnsink instance.
10. On success, Mediaframework agent will call HNSink setHNSinkProperties() and set dtcp_enabled flag to true.
11. On success, Mediaframework agent will call HNSink setSourceType().
12. On success, Mediaframework agent will call HnSink setSource()
13.On success, Mediaframework agent will call RMFQAMSrc play().
14. On success, Mediaframework agent will call the HNSink base class term.
15. On Success, mediaframework agent will call the HNSink uninit_platform()
16.On success, Mediaframework agent will call close() of  QAMSrc element.
17.On success, Mediaframework agent will call term() and de-initialize the QAMSrc element.
18.On success, Mediaframework agent will call RMFQAMSrc uninit_platform().
19.On success, Mediaframework agent will call rmfplatform uninit().
20.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for notnull and return success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_QAMSrc_HNSink_04</test_script>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

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

    if teststep == 'RmfElement_HNSink_SetProperties':
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(url);
        print "hnsink url:",url

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

    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;

    return result

#Load Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_QAMSrc_HNSink_04');
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
                obj.configureTestCase(ip,port,'RMF_QAMSrc_HNSink_04');
        	#Get the result of connection with test component and STB
        	loadModuleStatus = obj.getLoadModuleResult();
        	print "Re-Load Module Status :  %s" %loadModuleStatus;
        	loadmoduledetails = obj.getLoadModuleDetails();
        	print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in loadModuleStatus.upper():
	#Set module load status
	obj.setLoadModuleStatus("SUCCESS");

        #Prmitive test case which associated to this Script
        #Change the List according to Prmitive test case
        src_parameter=[];
        src_element=[];
        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Init',obj,"SUCCESS",src_parameter,src_element);
        if "SUCCESS" in result.upper():
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_InitPlatform',obj,"SUCCESS",src_parameter,src_element);
                if "SUCCESS" in result.upper():
                        src_parameter=["rmfElement","factoryEnable"]
                        src_element=["QAMSrc","false"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,"SUCCESS",src_parameter,src_element);
                        if "SUCCESS" in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["QAMSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,"SUCCESS",src_parameter,src_element);
                                if "SUCCESS" in result.upper():
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,"SUCCESS",src_parameter,src_element);
                                        if "SUCCESS" in result.upper():
                                                src_parameter=["rmfElement"]
                                                src_element=["HNSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,"SUCCESS",src_parameter,src_element);
                                                if "SUCCESS" in result.upper():
                                                        src_parameter=[]
                                                        src_element=[]
                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_InitPlatform',obj,"SUCCESS",src_parameter,src_element);

                                                        if "SUCCESS" in result.upper():
                                                                src_parameter=["rmfElement"]
                                                                src_element=["HNSink"]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,"SUCCESS",src_parameter,src_element);
                                                                if "SUCCESS" in result.upper():
                                                                        src_parameter=["dctpEnable","typeFlag"]
                                                                        src_element=["true",0]
                                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetProperties',obj,"SUCCESS",src_parameter,src_element);
                                                                        if "SUCCESS" in result.upper():
                                                                                src_parameter=["rmfElement"]
                                                                                src_element=["QAM_SRC"]
                                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetSourceType',obj,"SUCCESS",src_parameter,src_element);
                                                                                if "SUCCESS" in result.upper():
                                                                                        src_parameter=["rmfSourceElement","rmfSinkElement"]
                                                                                        src_element=["QAMSrc","HNSink"]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,"SUCCESS",src_parameter,src_element);
                                                                                        if "SUCCESS" in result.upper():
                                                                                                src_parameter=["rmfElement","defaultPlay","playSpeed","playTime"]
                                                                                                src_element=["QAMSrc",1,1.0,0.0]
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,"SUCCESS",src_parameter,src_element);
                                                                                                if "SUCCESS" in result.upper():
                                                                                                        time.sleep(30);
                                                                                                        src_parameter=["rmfElement"]
                                                                                                        src_element=["QAMSrc"]
                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,"SUCCESS",src_parameter,src_element);
                                                                                                        if "SUCCESS" in result.upper() and "PLAYING" in details.upper():
                                                                                                                print "QAMSource play successful"
                                                                                                                tdkTestObj.setResultStatus(result);
                                                                                                        else:
                                                                                                                print "QAMSource play failed"
                                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                        src_parameter=["rmfElement"]
                                                                        src_element=["HNSink"]
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,"SUCCESS",src_parameter,src_element);
                                                                src_parameter=[]
                                                                src_element=[]
                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_UninitPlatform',obj,"SUCCESS",src_parameter,src_element);
                                                src_parameter=["rmfElement"]
                                                src_element=["QAMSrc"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,"SUCCESS",src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,"SUCCESS",src_parameter,src_element);
                                src_parameter=["rmfElement","factoryEnable"]
                                src_element=["QAMSrc","false"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,"SUCCESS",src_parameter,src_element);
                        src_parameter=[];
                        src_element=[];
                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_UninitPlatform',obj,"SUCCESS",src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Uninit',obj,"SUCCESS",src_parameter,src_element);

	#obj.initiateReboot();
	#Unload Test component
        obj.unloadModule("mediaframework");
else:
	#Set module load status
        obj.setLoadModuleStatus("FAILURE");
