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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1726</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_Gst_LongDuration_Check_GstQamTune_Crash_56</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: Tune to a particular channel. Play for 2 hrs and change the channel and play it continuously for 8 hrs and check if rmfstreamer crashes at gst_qamtunersrc_pump_data_callback(void*, int).
Test CaseID: CT_RMF_HNSRC_MPSink_56
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>623</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
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
videorec_parameter_value=[0,0,1280,0,720]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]
exitFlag = 0
openCount = 0
ip = <ipaddress>
port = <port>
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_Gst_LongDuration_Check_GstQamTune_Crash_56');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    global tdkTestObj
    global openCount
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        if openCount == 0:
                streamDetails = tdkTestObj.getStreamDetails('01');
                print "Open Channel 1"
        else:
                streamDetails = tdkTestObj.getStreamDetails('02');
                print "Open Channel 2"
        url = mediaframework.getStreamingURL("Live" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);
        openCount = openCount + 1

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep != "CheckLogForCrash":
        tdkTestObj.setResultStatus(result);
        print "Status of "+ teststep+":  %s" %result;
        print "Status of "+ teststep+":  %s" %details;

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
                obj.configureTestCase(ip,port,'RMF_Gst_LongDuration_Check_GstQamTune_Crash_56');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;


if Expected_Result in loadModuleStatus.upper():

        #Prmitive test case which associated to this Script
        #Creating the Hnsrc instance
        log_param_name = ["logFileToClear"]
        log_param_value = ["ocapri_log.txt"]
        result=Create_and_ExecuteTestStep('ClearLogFile',obj,Expected_Result,log_param_name,log_param_value);
        if Expected_Result not in result.upper():
                print "Log file not cleared, exiting the script"
                obj.unloadModule("mediaframework");
                exit()

        #Tune and play for 2hrs.
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
                                                                        time.sleep(60);

                                                                        loop = 1
                                                                        while loop <= 120:

                                                                                result1=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                                param_name = ["logFile","FileNameToCpTdkPath","patternToSearch"]
                                                                                param_value = ["ocapri_log.txt","gst_crash_check.txt","rebooting due to rmfStreamer-crash"]
                                                                                result0=Create_and_ExecuteTestStep('CheckLogForCrash',obj,Expected_Result,param_name,param_value);
                                                                                if (Expected_Result not in result0.upper()):
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        if (Expected_Result in result1.upper()):
                                                                                                time.sleep(60)
                                                                                                print "Playing fine."
                                                                                        else:
                                                                                                print "Live play failed: Get State returned failure."
                                                                                                exitFlag = 1
                                                                                                break;
                                                                                else:
                                                                                        print "Live play failed due to crash."
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        exitFlag = 1
                                                                                        break;
                                                                                print "loop ",loop," success"
                                                                                loop = loop + 1


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
                time.sleep(5);
                if exitFlag == 1:
                        print "Exiting the script, Due to Live play failed."
                        exit()

        #Change channel and play for 8hrs.
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
                                                                        time.sleep(60);

                                                                        loop = 1
                                                                        while loop <= 480:

                                                                                result1=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                                param_name = ["logFile","FileNameToCpTdkPath","patternToSearch"]
                                                                                param_value = ["ocapri_log.txt","gst_crash_check.txt","rebooting due to rmfStreamer-crash"]
                                                                                result0=Create_and_ExecuteTestStep('CheckLogForCrash',obj,Expected_Result,param_name,param_value);
                                                                                if (Expected_Result not in result0.upper()):
                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                        if (Expected_Result in result1.upper()):
                                                                                                time.sleep(60)
                                                                                                print "Playing fine."
                                                                                        else:
                                                                                                print "Live play failed: Get State returned failure."
                                                                                                break;
                                                                                else:
                                                                                        print "Live play failed due to crash."
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        break;
                                                                                print "loop ",loop," success"
                                                                                loop = loop + 1

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
                time.sleep(5);

        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
