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
  <id>1159</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_QAMSrc_HNSink_08</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>RMF_QAMSrc – To Stream out the live content through HNSink on to the network when factory method flag is set to false but set random socketId to hnsink properties..
Test CaseID: CT_RMF_QAMSrc_HNSink_08
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>14</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
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
obj.configureTestCase(ip,port,'RMF_QAMSrc_HNSink_08');

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
                obj.configureTestCase(ip,port,'RMF_QAMSrc_HNSink_08');
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
                                                src_element=["HNSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                                if expected_Result in result.upper():
                                                        src_parameter=[]
                                                        src_element=[]
                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_InitPlatform',obj,expected_Result,src_parameter,src_element);
                                                        if expected_Result in result.upper():
                                                                src_parameter=["rmfElement"]
                                                                src_element=["HNSink"]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                                                if expected_Result in result.upper():
                                                                        src_parameter=["dctpEnable","typeFlag","socketId"]
                                                                        src_element=["false",1,9]
                                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetProperties',obj,expected_Result,src_parameter,src_element);
                                                                        if expected_Result in result.upper():
                                                                                src_parameter=["rmfElement"]
                                                                                src_element=["QAM_SRC"]
                                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetSourceType',obj,expected_Result,src_parameter,src_element);
                                                                                if expected_Result in result.upper():
                                                                                        src_parameter=["rmfSourceElement","rmfSinkElement"]
                                                                                        src_element=["QAMSrc","HNSink"]
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
                                                                                                        if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                                                print "QAMSource play successful"
                                                                                                                tdkTestObj.setResultStatus(result);
                                                                                                        else:
                                                                                                                print "QAMSource play failed"
                                                                                                                tdkTestObj.setResultStatus(failure);

                                                                        src_parameter=["rmfElement"]
                                                                        src_element=["HNSink"]
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                                                src_parameter=[]
                                                                src_element=[]
                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_UninitPlatform',obj,expected_Result,src_parameter,src_element);
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
