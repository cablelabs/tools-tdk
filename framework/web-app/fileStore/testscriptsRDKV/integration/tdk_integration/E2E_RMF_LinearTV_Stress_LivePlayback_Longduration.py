#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1570</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_Stress_LivePlayback_Longduration</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Live play back for long duration(10hrs). E2E_LinearTV_44</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>630</execution_time>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
src_element=["HNSrc"]
Expected_Result = "SUCCESS"
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


#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LivePlayback_Longduration');
media_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LivePlayback_Longduration');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
    
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
        
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    if (teststep == "RMF_Element_GetState"):
        details =  tdkTestObj.getResultDetails();
        if "PLAYING" in details:
            print details;
            print "Current State is: PLAYING";
        else:
            print "Failure. Current State is not Playing %s" %details;
    print "Status of "+ teststep+":  %s" %result;
    return result


#Get the result of connection with test component and STB
result = tdk_obj.getLoadModuleResult();
result1 = media_obj.getLoadModuleResult();

print "Load Module Status of tdkintegration:  %s\n Load Module Status of mediaframework:  %s" %(result,result1);

details1 = media_obj.getLoadModuleDetails();

if "FAILURE" in result1.upper():
        if "RMF_STREAMER_NOT_RUNNING" in details1:
                print "rmfStreamer is not running. Rebooting STB"
                media_obj.initiateReboot();
                #Reload Test component to be tested
                media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                media_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LivePlayback_Longduration');
                #Get the result of connection with test component and STB
                result1 = media_obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %result1;
                details1 = media_obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %details1;


if ("SUCCESS" in result.upper()) and ("SUCCESS" in result1.upper()):
     
    tdk_obj.setLoadModuleStatus("SUCCESS");
    media_obj.setLoadModuleStatus("SUCCESS");     

    #Prmitive test case which associated to this Script
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");
 
        url = tdkintegration.E2E_getStreamingURL(media_obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();
    
    #Remove unwanted part from URL
    PLAYURL = details.split("[RESULTDETAILS]");
    ValidURL = PLAYURL[-1];
     
    open_parameter_value.append(ValidURL); 

    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print "E2E DVR Playback Successful: [%s]"%details;
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',media_obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
            #Creating the MPSink instance
            result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',media_obj,Expected_Result,sink_parameter,sink_element);
            if Expected_Result in result.upper():
                #Initiazing the Hnsrc Element
                result=Create_and_ExecuteTestStep('RMF_Element_Init',media_obj,Expected_Result,src_parameter,src_element);
                if Expected_Result in result.upper():
                    #Initiazing the MPSink Element
                    result=Create_and_ExecuteTestStep('RMF_Element_Init',media_obj,Expected_Result,sink_parameter,sink_element);
                    if Expected_Result in result.upper():
                        #Opening the Hnsrc Element with playurl
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',media_obj,Expected_Result,open_parameter_name,open_parameter_value);
                        if Expected_Result in result.upper():
                            #Setting the MPSink Element with x,y co-ordiantes
                            result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',media_obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                            if Expected_Result in result.upper():
                                #Selecting the source for MPSink
                                result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',media_obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                if Expected_Result in result.upper():
                                    #Play the HNSRC-->MPSINK pipeline
                                    result=Create_and_ExecuteTestStep('RMF_Element_Play',media_obj,Expected_Result,play_parameter_name,play_parameter_value);
                                    time.sleep(10);
                                    if Expected_Result in result.upper():
                                        for i in range(1,600):                                            
                                            
                                            result=Create_and_ExecuteTestStep('RMF_Element_GetState',media_obj,Expected_Result,src_parameter,src_element);                                            
                                            if Expected_Result in result.upper():
                                                time.sleep(60);
                                                print "Execution Success for iteration %d"%i
                                            else:
                                                print "Execution failure at iteration %d"%i
                                                break;
                                            
                            #Close the Hnsrc Element
                            result=Create_and_ExecuteTestStep('RMF_Element_Close',media_obj,Expected_Result,src_parameter,src_element);
                            
                        #Terminating the MPSink Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Term',media_obj,Expected_Result,sink_parameter,sink_element);
                    #Terminating the HNSrc Element
                    result=Create_and_ExecuteTestStep('RMF_Element_Term',media_obj,Expected_Result,src_parameter,src_element);
                #Removing the MPSink Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',media_obj,Expected_Result,sink_parameter,sink_element);
                
            #Removing the HNSrc Element Instances
            result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',media_obj,Expected_Result,src_parameter,src_element);
          
        else:
            print "Status of RMF_Element_Create_Instance:  %s" %result;
        
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Failed: TDKE2E_RMFLinearTV_GetURL";
        
    tdk_obj.unloadModule("tdkintegration");
    media_obj.unloadModule("mediaframework");
        
else:
    print "Failed to load tdkintegration module";
    tdk_obj.setLoadModuleStatus("FAILURE");
    media_obj.setLoadModuleStatus("FAILURE");
