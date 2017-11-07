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
  <version>9</version>
  <name>E2E_RMF_LivePlayback_TSB_Increase_StandbyMode</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check the TSB increasing when box is in STANDBY Mode</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <box_type>Terminal-RNG</box_type>
    <box_type>Emulator-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_RMF_TSB_59</test_case_id>
    <test_objective>E2E_TSB-To check the TSB increase during STANDBY</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1-X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID SpeedRate: 30.0</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be connected in moca</input_parameters>
    <automation_approch>1.TM loads TDKIntegration_agent via the test agent 
2.TDKIntegration_agent Frames the request URL after getting ocapId from the TM and  makes a RPC calls to the TDKIntegration_agent for tune.
3.TDKIntegration_agent will  send framed url to the rmfStreamer.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the TDKIntegration_agent for playback with the HnSrc-&gt;MPSink Pipeline.
5.IARMBUs_Agent changes the powermode to STANDBY.
6. Using getMediaTime check the time before and after Standby</automation_approch>
    <except_output>Checkpoint 1. Set and Get Speed APIs return values of HNSrc Element  is verified as success or failure.
Checkpoint 2 Error code parameter of Json response is verified as success or failure.</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkIntegrationstub.so
TestMgr_LiveTune_GETURL
TestMgr_TSB_Play</test_stub_interface>
    <test_script>E2E_RMF_LivePlayback_TSB_Increase_StandbyMode</test_script>
    <skipped>No</skipped>
    <release_version>NA</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
import tdklib;
import tdkintegration;
import time;
from iarmbus import change_powermode

src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
sink_element=["MPSink"]
sink_parameter=["rmfElement"]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]
mediatime_parameter_name=["mediaTime","rmfElement"]
mediatime_parameter_value=[2000,"HNSrc"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
videorec_parameter_name=["X","Y","width","apply","height"]
videorec_parameter_value=[0,0,1280,0,720]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]

ip = <ipaddress>
port = <port>

mfObj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");
mfObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_TSB_Increase_StandbyMode');
iarmObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_TSB_Increase_StandbyMode');

def Create_and_ExecuteTestStep(teststep, testmfObject, expectedresult,parametername, parametervalue):
    global Mediatime
    global tdkTestObj
    #Primitive test case which associated to this Script
    tdkTestObj =testmfObject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = tdkintegration.E2E_getStreamingURL(mfObj, "TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
	    return "FAILURE";
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    details = tdkTestObj.getResultDetails();
    print "Status of "+ teststep+":  %s" %result;
    print "Details of "+ teststep+":  %s" %details;
    if teststep == "RMF_Element_Getmediatime":
        if "SUCCESS" in result.upper():
                Mediatime=details.split(":");

    return result

def Change_Power(iarmObj, powermode):
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
            
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):               
            print "SUCCESS :Application successfully initialized with IARMBUS library";
            #calling IARMBUS API "IARM_Bus_Connect"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});    
            
            expectedresult="SUCCESS";
            #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
            if expectedresult in actualresult:                    
                print "SUCCESS: Querying STB power state -RPC method invoked successfully";
                                                    
                change_powermode(iarmObj,powermode); 
                print "Power mode set to ",powermode            
            
                # Calling IARM_Bus_DisConnect API
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});
            else:
                print "FAILURE: IARM_Bus_Connect failed. %s" %details;
            #calling IARMBUS API "IARM_Bus_Term"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});       

#Get the result of connection with test component and STB
mfLoadModuleStatus = mfObj.getLoadModuleResult();
iarmModuleStatus = iarmObj.getLoadModuleResult();
print "Mediaframework Load Module Status :  %s" %mfLoadModuleStatus;
print "IARMBus Load Module Status :  %s" %iarmModuleStatus
mfObj.setLoadModuleStatus(mfLoadModuleStatus.upper());
iarmObj.setLoadModuleStatus(iarmModuleStatus.upper());

mfLoadModuleDetails = mfObj.getLoadModuleDetails();

if "FAILURE" in mfLoadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in mfLoadModuleDetails:
                print "rmfStreamer is not running. Rebooting STB"
                mfObj.initiateReboot();
                #Reload Test component to be tested
                mfObj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                mfObj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_TSB_Increase_StandbyMode');
                #Get the result of connection with test component and STB
                mfLoadModuleStatus = mfObj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %mfLoadModuleStatus;
		mfLoadModuleDetails = mfObj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %mfLoadModuleDetails;


if "SUCCESS" in mfLoadModuleStatus.upper() and "SUCCESS" in iarmModuleStatus.upper():

        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mfObj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mfObj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',mfObj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',mfObj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',mfObj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',mfObj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',mfObj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',mfObj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        #Get the Mediatime value
                                                                        time.sleep(5);
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',mfObj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper():
                                                                                initialmediatime=float(Mediatime[1]);
                                                                                #Changing Power mode to STANDBY
                                                                                Change_Power(iarmObj, 1);
                                                                                #time.sleep(1000);
										print "Sleep for 60 secs"
										time.sleep(60);
                                                                                #Changing Power mode to ON
                                                                                Change_Power(iarmObj, 2)
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',mfObj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper():
                                                                                        Mediatime[1]=float(Mediatime[1]);
											print "New Time ", Mediatime[1], "Initial Time", initialmediatime
                                                                                        if Mediatime[1] >= initialmediatime:
                                                                                                print "SUCCESS: Mediatime will increase during standby because the buffer position will keep remains "
                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                        else:
                                                                                                print "FAILURE: Mediatime increased during standby"
                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',mfObj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',mfObj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',mfObj,Expected_Result,src_parameter,src_element);
                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mfObj,Expected_Result,sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',mfObj,Expected_Result,src_parameter,src_element);

	print "Changing Power mode to ON state"
        Change_Power(iarmObj, 2)

        mfObj.unloadModule("mediaframework");
	iarmObj.unloadModule("iarmbus");
