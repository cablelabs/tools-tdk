##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1649</id>
  <version>10</version>
  <name>RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: RMF_HNSRC_MPSink –After 5 mins of tsb, Do FF from the middle of buffer to the live point and do RW. And make sure no freeze while approaching the live point.
Test CaseID: CT_RMF_HNSRC_MPSink_51
Test Type: Positive</synopsis>
  <groups_id/>
  <execution_time>13</execution_time>
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
    <test_case_id>CT_RMF_HNSRC_MPSink_51</test_case_id>
    <test_objective>RMF_HNSRC_MPSink –After 5 mins of tsb, Do FF from the middle of buffer to the live point and do RW. And make sure no freeze while approaching the live point.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>No</pre_requisite>
    <api_or_interface_used>HNSrc init()
HNSrc open()
MPSink init()
MPSink SetVideoRectangle()
MPSink SetSource()
HNSrc play()
HNSrc getState()
HNSrc SetSpeed()
HNSrc GetSpeed()
HNSrc close()
MPSink term()
HNSrc term()</api_or_interface_used>
    <input_parameters>init: None
open:Char *,Char *
play:None
GetState:RMFState
SetSpeed: float – speed
GetSpeed: None
SetVideoRectangle: unsigned.
unsigned, unsigned, 
Unsigned, bool apply_now – x,y,h,w,false
setSource: RMFMediaSourceBase*
close:None
term:None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.Mediaframework agent will create the instance for Hnsrc and  initialize the Hnsrc element.
3.Mediaframework agent will create the instance for Mpsink and initialize the Mpsink element.
4.Form the pipeline Hnsrc-&gt;Mpsink using set source ().
5.Mediaframework agent will open and play the  Hnsrc element.
6.Mediaframework agent will set speed as 4.0 and get the speed of the pipeline.
7. Mediaframework agent will call get speed to fetch the speed, which is expected to be 1.0 as it reached the live streaming.
8. Mediaframework agent will call set speed as -4.0 to rewind and the speed of the pipeline.
9.Mediaframework agent will terminate the Hnsrc element .
10.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
CheckPoint 2. Check the Audio and Video quality using CheckAudioStatus.sh and CheckVideoStatus.sh scripts.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
speed_parameter_name=["playSpeed","rmfElement"]
speed_parameter_value=[4.0,"HNSrc"]

ip = <ipaddress>
port = <port>

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    #Primitive test case which associated to this Script
    global Mediatime
    global tdkTestObj
    global Mediaspeed
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = mediaframework.getStreamingURL("TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
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
        	print Mediatime[1];
    if teststep == "RMF_Element_Getspeed":
	if "SUCCESS" in result.upper():
	        Mediaspeed=details.split(":");
        	print Mediaspeed[1];

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
                obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_FF_RW_CheckMacroblocking_51');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if Expected_Result in loadModuleStatus.upper():

        #Prmitive test case which associated to this Script
        obj.setLoadModuleStatus("SUCCESS");
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
                                                                        time.sleep(15)

                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                        print "Video check Done. Status: ",result;
									
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,Expected_Result,src_parameter,src_element);
									
                                                                        #Pause the HNSRC-->MPSINK pipeline
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper():
                                                                                #Get the Mediatime value
                                                                                time.sleep(30);
                                                                                if Expected_Result in result.upper():
                                                                                        #initialmediatime=Mediatime[1]
                                                                                        #FF with 4x
                                                                                        play_parameter_value=["HNSrc",1,0.0,4.0]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
											
                                                                                        if Expected_Result in result.upper():
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getspeed',obj,Expected_Result,src_parameter,src_element);
                                                                                                if Expected_Result in result.upper():
                                                                                                        time.sleep(15);


                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                                                        print "Video check Done. Status: ",result;

                                                                                                   
													if Expected_Result in result.upper():
														result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,Expected_Result,src_parameter,src_element);
														result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);
														if Expected_Result in result.upper():

															time.sleep(20)
															
															Curr_mediatime=Mediatime[1]
															Curr_mediatime=float(Curr_mediatime)
		                                                                                                        speed_parameter_name=["playSpeed","rmfElement"]
															play_parameter_value=["HNSrc",1,Curr_mediatime,-4.0] 
                                		                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                		                                                        if Expected_Result in result.upper():

                		                                                                                                checkStatusParameter=["audioVideoStatus"]
                                		                                                                                checkStatusFor=["CheckVideoStatus.sh"]
                                                		                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                		                                                print "Video check Done. Status: ",result;

                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                time.sleep(5);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
