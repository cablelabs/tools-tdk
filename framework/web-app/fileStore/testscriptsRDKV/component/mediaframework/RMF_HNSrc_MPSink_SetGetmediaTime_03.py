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
  <id>951</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_MPSink_SetGetmediaTime_03</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>495</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>These Script tests the RDK Mediaframework HNSrc element to set and getMediatime without sink element Test Case ID: CT_RMF_HNSrc_03</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import mediaframework;
import time;

src_element=["HNSrc"]
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
mediatime_parameter_name=["mediaTime","rmfElement"]
mediatime_parameter_value=[2,"HNSrc"]

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
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
        print "%s : %s" %(parametername[item],parametervalue[item]);
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    print "Status of "+ teststep+":  %s" %result;
    return result

#Load Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSRC_MPSINK_Video_Play_01');
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
                obj.configureTestCase(ip,port,'RMF_HNSRC_MPSINK_Video_Play_01');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in loadModuleStatus.upper():
        #Set module load status
        obj.setLoadModuleStatus("SUCCESS");

        #Primitive test case which associated to this Script
        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,"SUCCESS",src_parameter,src_element);
        if "SUCCESS" in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,"SUCCESS",sink_parameter,sink_element);
                if "SUCCESS" in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,"SUCCESS",src_parameter,src_element);
                        if "SUCCESS" in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,"SUCCESS",sink_parameter,sink_element);
                                if "SUCCESS" in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,"SUCCESS",open_parameter_name,open_parameter_value);
                                        if "SUCCESS" in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,"SUCCESS",videorec_parameter_name,videorec_parameter_value);
                                                if "SUCCESS" in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,"SUCCESS",setsource_parameter_name,setsource_parameter_value);
                                                        if "SUCCESS" in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,"SUCCESS",play_parameter_name,play_parameter_value);
                                                                if "SUCCESS" in result.upper():
                                                                        time.sleep(10);
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,"SUCCESS",src_parameter,src_element);
                                                                        if "SUCCESS" in result.upper():
                                                                            result=Create_and_ExecuteTestStep('RMF_Element_Setmediatime',obj,"SUCCESS",mediatime_parameter_name,mediatime_parameter_value);
                                                                            if "SUCCESS" in result.upper():
                                                                                time.sleep(10);
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,"SUCCESS",src_parameter,src_element);
                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,"SUCCESS",src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,"SUCCESS",sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,"SUCCESS",src_parameter,src_element);
                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,"SUCCESS",sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,"SUCCESS",src_parameter,src_element);
                time.sleep(20);

	#Unload Test component
        obj.unloadModule("mediaframework");
else:
	#Set module load status
        obj.setLoadModuleStatus("FAILURE");
