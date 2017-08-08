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
  <id/>
  <version>2</version>
  <name>RMF_TSB_SlowRewind_Error_Check_03</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check the defect: STB switches to 2x rewind trick mode instead of slow rewind, on initiating slow rewind at the LIVE point(1.3.3p2s1)
TCID: CT_RMF_DEFECTS_03</synopsis>
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
    <test_case_id>CT_RMF_QAMSrc_HNSink_03</test_case_id>
    <test_objective>RMF_QAMSrc – To Stream out the live content through HNSink on to the network when factory method flag is set to true and when dtcp_enabled is set to true(Data pushed onto the network is encrypted).</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>monitorRMF.sh
RmfStreamer
Process should be stopped before runing the script.
Streaming should be happening.</pre_requisite>
    <api_or_interface_used>rmf_Error init RMFResult RMFQAMSrc::init_platform()        RMFQAMSrc::disableCaching();  RMFQAMSrc* RMFQAMSrc::getQAMSourceInstance()           
RMFQAMSrc play()
RMFStateChangeRetrun getState() RMFQAMSrc::freeQAMSourceInstance()           RMFResult RMFQAMSrc::uninit_platform()    rmf_Error uninit()

HNSink::init_platform()
Init()
setHNSinkProperties()
SetSourceType()
SetSource()
Term()
HNSink::uninit_platform()</api_or_interface_used>
    <input_parameters>rmf_platform Init(): int- argc, char * argv[]            RMFQAMSrc::init_platform() : None                       RMFQAMSrc::disableCaching() : None                               RMFQAMSrc::getQAMSourceInstance(): char* uri    
play(): float speed, double time
getState():RMFState currentstate, RMFState pendingstate RMFQAMSrc::freeQAMSourceInstance(): RMFQAMSrc* uri RMFQAMSrc::uninit_platform() : None                                rmf_platform Uninit(): None

HNSink::init_platform(): None
SetHNSinkProperties(): HNSinkProperties_t properties
SetSourceType(): char* sourcetype
SetSource(): RMFMediaSourceBase*
HNSink::uninit_platform():  None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.Mediaframework agent will call init() of rmfPlaftorm for initializing rmfplatform and get the result.
3.On success, Mediaframework agent will call RMFQAMSrc init_platform() for initializing platform dependent functionalties and get the result.
4.On success, Mediaframework agent will call RMFQAMSrc disableCaching().
5.On success, Mediaframework agent will create the instance of QAMSrc by calling factory method RMFQAMSrc getQAMSourceInstance() and initialize the QAMSrc element.
6.On success, Mediaframework agent will call HNSink init_platform().
7. On success, Mediaframework agent will call HNSink  setProperties() and the attributes.
8. On success, Mediaframework agent will call HNSink  base class init() to initialize the hnsink instance.
9. On success, Mediaframework agent will call HNSink setHNSinkProperties() and set the flag dtcp_enabled to true.
10. On success, Mediaframework agent will call HNSink setSourceType().
11. On success, Mediaframework agent will call HnSink setSource()
12.On success, Mediaframework agent will call RMFQAMSrc play().
13. On success, Mediaframework agent will call the HNSink base class term.
14. On Success, mediaframework agent will call the HNSink uninit_platform()
15.On success, Mediaframework agent will call RMFQAMSrc freeQAMSourceInstance().
16.On success, Mediaframework agent will call RMFQAMSrc uninit_platform().
17.On success, Mediaframework agent will call rmfplatform uninit().
18.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for notnull and return success status.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_TSB_SlowRewind_Error_Check_03</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
import tdklib;
import mediaframework;
import time;
src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
sink_element=["MPSink"]
sink_parameter=["rmfElement"]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
videorec_parameter_name=["X","Y","width","apply","height"]
videorec_parameter_value=[0,0,720,0,1280]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]
speed_parameter_name=["playSpeed","rmfElement"]
speed_parameter_value=[-0.5,"HNSrc"]

ip = <ipaddress>
port = <port>
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_TSB_SlowRewind_Error_Check_03');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    #Primitive test case which associated to this Script
    global tdkTestObj
    global Mediastate
    global details
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == 'RMF_Element_Open':
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = mediaframework.getStreamingURL("TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print url;
        open_parameter_value.append(url);
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if teststep != 'RMF_Element_Getstate':
        tdkTestObj.setResultStatus(result);
    print "Status of "+ teststep+":  %s" %result;
    print "Details of "+ teststep+":  %s" %details;
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
                obj.configureTestCase(ip,port,'RMF_TSB_SlowRewind_Error_Check_03');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;


if Expected_Result in loadModuleStatus.upper():

        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        time.sleep(10);
                                                                        #Check the get state of current pipeline
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper():
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                                        if Expected_Result in result.upper() and "PAUSE" in details.upper():
                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Setspeed',obj,Expected_Result,speed_parameter_name,speed_parameter_value);
                                                                                                if Expected_Result in result.upper():
                                                                                                        time.sleep(10);
                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getspeed',obj,Expected_Result,src_parameter,src_element);
																										#stateresult=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                                                        if Expected_Result in result.upper():
                                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                                        else:
                                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                        else:
                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                        else:
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                        #Close the Hnsrc Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);

                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                time.sleep(20);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
