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
  <id>1565</id>
  <version>24</version>
  <name>RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: Tune to a particular channel, and change the channel after play back for sometime, and check if channel change happened successfully or any SPTS read timeout error is occurring. 
Test CaseId: CT_RMF_QAMSrc_MPSink_15
Test Case Type: Positive</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
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
    <test_case_id>CT_RMF_QAMSrc_MPSink_15</test_case_id>
    <test_objective>RMFQAMSrc –  Tune to a particular channel, and change the channel after play back for sometime, and check if channel change happened successfully or any SPTS read timeout error is occurring.  When factory method flag is set to true.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>monitorRMF.sh
RmfStreamer
Process should be stopped before runing the script.</pre_requisite>
    <api_or_interface_used>rmf_Error init RMFResult RMFQAMSrc::init_platform()           RMFQAMSrc* RMFQAMSrc::getQAMSourceInstance()
RMFResult play() 
RMFResult pause()
RMFQAMSrc ::changeUri()
Void RMFQAMSrc::freeQAMSourceInstance()           
RMFResult RMFQAMSrc::uninit_platform()       rmf_Error uninit()</api_or_interface_used>
    <input_parameters>rmf_platform Init(): int- argc, char * argv[]            RMFQAMSrc::init_platform() : None                                      RMFQAMSrc::getQAMSourceInstance(): char* uri       
play(): float speed, double time
changeURI(): char* uri,RMFQAMSrc* old, RMFQAMSrc** updated, bool new_instance.                  RMFQAMSrc::freeQAMSourceInstance(): RMFQAMSrc* uri RMFQAMSrc::uninit_platform() : None                                rmf_platform Uninit(): None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent via the test agent.
2.Mediaframework agent will call init() of rmfPlaftorm for initializing rmfplatform and get the result.
3.On success, Mediaframework agent will call RMFQAMSrc init_platform() for initializing platform dependent functionalties and get the result.
4.On success, Mediaframework agent will create the instance of QAMSrc by calling factory method RMFQAMSrc getQAMSourceInstance() and initialize the QAMSrc element.
5.On success, Mediaframework agent will call RMFQAMSrc play() by passing the speed and time parameters. Play for some duration.
6.On success, Mediaframework agent will call RMFQAMSrc pause().
7. On success, Mediaframework agent will call RMFQAMSc changeUri() API to tune to new channel with new ocapid.
8.On success, Mediaframework agent will call RMFQAMSrc play() by passing the speed and time parameters new qam source instance returned by changeUri API. Play for some duration.
9.On success, Mediaframework agent will call RMFQAMSrc pause().
10.On success, Mediaframework agent will call RMFQAMSrc freeQAMSourceInstance().
11.On success, Mediaframework agent will call RMFQAMSrc uninit_platform().
12.On success, Mediaframework agent will call rmfplatform uninit().
13.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for not null and return success status.
Checkpoint 2. Search the log of the API() calls to see “SPTS Read Timeout Error” as occured or not.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15</test_script>
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
createCount = 0

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global details
    global tdkTestObj
    global createCount
    #Primitive test case which associated to this Script
    tdkTestObj = testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Create_Instance':
        #Stream details for tuning
        if parametervalue[0] == "QAMSrc":
                createCount = createCount + 1
                #temproary need to be removed
                if createCount == 3:
                        createCount = 1
                print "QAMSrc ceateCount increament"

        print "createCount=",createCount
        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        ocapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("qamSrcUrl");
        parametervalue.append(ocapLocator);
        print "OcapLocator:",ocapLocator

        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        newOcapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("newQamSrcUrl");
        parametervalue.append(ocapLocator);
        print "New OcapLocator:",newOcapLocator

    if teststep == 'RmfElement_QAMSrc_ChangeURI':
        #Stream details for tuning
        print "createCount=",createCount
        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        changeUri = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(changeUri);
        print "ChangeUri:",changeUri

    for item in range(len(parametername)):
	print "%s : %s"%(parametername[item],parametervalue[item]);
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep != 'RMF_Element_GetState' and teststep != 'RmfElement_CheckFor_SPTSReadError':
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
                obj.configureTestCase(ip,port,'RMF_QAMSource_ChangeChannel_Check_SPTS_Error_15');
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
                        src_element=["QAMSrc","true"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
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

                                                                        #Change made based on the comment made in RDKTT-108.
                                                                        #if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                        if expected_Result in result.upper():
                                                                                print "QAMSource play successful"
                                                                                tdkTestObj.setResultStatus(result);
                                                                                src_parameter=["rmfElement"]
                                                                                src_element=["QAMSrc"]
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                                                if expected_Result in result.upper():
                                                                                        time.sleep(5);
                                                                                        print "QAMSource pause successful"
                                                                                        tdkTestObj.setResultStatus(result);
                                                                                        src_parameter=["rmfElement","factoryEnable","newQamSrc"]
                                                                                        src_element=["QAMSrc","true","true"]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                                                                        if expected_Result in result.upper():
                                                                                                src_parameter=[]
                                                                                                src_element=[]
                                                                                                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_ChangeURI',obj,expected_Result,src_parameter,src_element);
                                                                                                #time.sleep(10);

                                                                                                if expected_Result in result.upper():
                                                                                                        src_parameter=["rmfSourceElement","rmfSinkElement","newQamSrc"]
                                                                                                        src_element=["QAMSrc","MPSink","true"]
                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,expected_Result,src_parameter,src_element);
                                                                                                        if expected_Result in result.upper():
                                                                                                                src_parameter=["rmfElement","defaultPlay","playSpeed","playTime","newQamSrc"]
                                                                                                                src_element=["QAMSrc",1,1.0,0.0,"true"]
                                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,expected_Result,src_parameter,src_element);
                                                                                                                time.sleep(10);
                                                                                                                if expected_Result in result.upper():
                                                                                                                        print "QAMSource channel change play successful"
                                                                                                                        tdkTestObj.setResultStatus(result);
                                                                                                                        src_parameter=["rmfElement","newQamSrc"]
                                                                                                                        src_element=["QAMSrc","true"]
                                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                                                                                        if expected_Result in result.upper():
                                                                                                                                time.sleep(5);
                                                                                                                                print "QAMSource channel change pause successful"
                                                                                                                                tdkTestObj.setResultStatus(result);

                                                                                        src_parameter=["rmfElement","factoryEnable","newQamSrc"]
                                                                                        src_element=["QAMSrc","true","true"]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                                                                else:
                                                                                        print "QAMSource pause failed"
                                                                                        tdkTestObj.setResultStatus(failure);
                                                                        else:
                                                                                print "QAMSource play failed"
                                                                                tdkTestObj.setResultStatus(failure);


#                                                                src_parameter=["rmfElement"]
#                                                               src_element=["QAMSrc"]
                                                                #result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                src_parameter=["rmfElement"]
                                                src_element=["MPSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["MPSink"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                src_parameter=["rmfElement","factoryEnable"]
                                src_element=["QAMSrc","true"]
                                #result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                        src_parameter=[];
                        src_element=[];
                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_UninitPlatform',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Uninit',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_CheckFor_SPTSReadError',obj,failure,src_parameter,src_element);
                if expected_Result in result.upper():
                        tdkTestObj.setResultStatus(failure);
                else:
                        tdkTestObj.setResultStatus(expected_Result);

	#obj.initiateReboot();
	#Unload Test component
        obj.unloadModule("mediaframework");
else:
	#Set module load status
        obj.setLoadModuleStatus("FAILURE");
