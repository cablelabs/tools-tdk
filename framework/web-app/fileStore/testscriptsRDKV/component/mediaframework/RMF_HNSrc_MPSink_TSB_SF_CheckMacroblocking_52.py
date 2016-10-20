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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1650</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: RMF_HNSRC_MPSink –After 5 mins of tsb, Skip front 50 sec three times from the middle of buffer and play till  live point. And make sure no freeze while approaching the live point also during the trickplay.
Test CaseID: CT_RMF_HNSRC_MPSink_52</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>13</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
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

ip = <ipaddress>
port = <port>

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52');

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
                obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_SF_CheckMacroblocking_52');
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

                                                                        #Pause the HNSRC-->MPSINK pipeline
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper():
                                                                                #Get the Mediatime value
                                                                                time.sleep(300);
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper():
                                                                                        initialmediatime=Mediatime[1]
                                                                                        #Skip Forward with 50 secs 3 times.


                                                                                        i = 0
                                                                                        while i < 3:
                                                                                                skip_parameter_name=["mediaTime","rmfElement"]
                                                                                                skip_parameter_value=[50,"HNSrc"]
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Setmediatime',obj,Expected_Result,skip_parameter_name,skip_parameter_value);
                                                                                                if Expected_Result in result.upper():
                                                                                                        time.sleep(15);


                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                                                        print "Video check Done. Status: ",result;
                                                                                                i = i + 1
                                                                                                print "Skiped Forward: ",i

                                                                                        #Pause the HNSRC-->MPSINK pipeline
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);

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
