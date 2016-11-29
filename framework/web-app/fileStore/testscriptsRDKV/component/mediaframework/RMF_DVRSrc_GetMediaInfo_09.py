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
  <id>847</id>
  <version>37</version>
  <name>RMF_DVRSrc_GetMediaInfo_09</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This script tests the RDK Mediaframework DVRSrc element to get mediaInfo i.e start time and total duration for the recorded content, by getMediaInfo API of DVRSource element.
Test Case ID: CT_RMF_DVRSrc_09.	
Test Type: Positive.</synopsis>
  <groups_id/>
  <execution_time>25</execution_time>
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
    <test_case_id>CT_RMF_DVRSrc_09</test_case_id>
    <test_objective>RMF_DVRSrc  – To get mediaInfo i.e start time and total duration for the recorded content, by getMediaInfo API of DVRSource element.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>The recorded content should be available.</pre_requisite>
    <api_or_interface_used>RMFResult init()     
RMFResult open()  
RMFResult getMediaInfo()
RMFResult close()
RMFResult    term()</api_or_interface_used>
    <input_parameters>Init(): None   
open():char*-dvr locator,char*- mimetype
getMediaInfo():RMFMediaInfo &amp;info 
close():None 
term(): None</input_parameters>
    <automation_approch>1. TM loads mediaframework agent via the test agent.
2. Mediaframework agent will create the instance for DVRSrc and  initialize the DVRSrc element.
3. Mediaframework agent will open the DVRSrc element with the valid url being framed with dvrlocator (Ex: dvr://local/record_id#segment number i.e, dvr://local/390206#0).
4. Mediaframework agent will call getMediaInfo API of DVRSrc element.
5. Mediaframework agent will close the DVRSrc element.
6. Mediaframework agent will terminate the  DVRSrc element.
7. For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to TM via the test agent by comparing the return value of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
Checkpoint 2.Compare the duration with value returned from getMediaInfo API for success.</except_output>
    <priority>Medium</priority>
    <test_stub_interface>libmediaframeworkstub.so</test_stub_interface>
    <test_script>RMF_DVRSrc_GetMediaInfo_09</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import mediaframework;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRSrc_GetMediaInfo_09');

expected_Result="SUCCESS"
duration = 0.0;
expected_Failure = "FAILURE"

def compareGetMediaInfo(tdkObj,sTime,tDuration):
        global duration

        if tDuration == duration:
                print "DVRSrc getMediaInfo() success"
                tdkObj.setResultStatus("SUCCESS");
        else:
                print "DVRSrc getMediaInfo() failed"
                tdkObj.setResultStatus("FAILURE");
        return ;

matchList = []
def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global matchList
    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
   
    if teststep == 'RMF_Element_Open':		
	#fetch recording id from list matchList.
        recordID = matchList[1]
        parametername.append("url");
        dvrLocator = "dvr://local/" + recordID[:-1] + "#0"
        print dvrLocator
        parametervalue.append(dvrLocator);
        global duration
        duration = matchList[3]

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep == 'RMF_Element_GetMediaInfo':
        pos = details.find('MediaStartTime');
        value = details[pos:]
        parts = value.partition(' ');
        partOne = parts[0];
        partTwo = parts[2];
        start = partOne[15:];
        end = partTwo[14:];
        startTime = float(start);
        durationTime = float(end);
        compareGetMediaInfo(tdkTestObj,startTime,durationTime);
    else:
        tdkTestObj.setResultStatus(result);


    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;
    
    return result

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
                obj.configureTestCase(ip,port,'RMF_DVRSrc_GetMediaInfo_09');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;


if expected_Result in loadModuleStatus.upper():
	tdkTestObj =obj.createTestStep('RMF_Element_Create_Instance');
#Pre-requisite to Check and verify required recording is present or not.
#---------Start-----------------

	duration = 3
	matchList = tdkTestObj.getRecordingDetails(duration);
	obj.resetConnectionAfterReboot()
#---------End-------------------

if expected_Result in loadModuleStatus.upper():
        #Prmitive test case which associated to this Script
        #Change the List according to Prmitive test case
        src_parameter=["rmfElement"]
        src_element=["DVRSrc"]
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
        if expected_Result in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                if expected_Result in result.upper():
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["DVRSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_GetMediaInfo',obj,expected_Result,src_parameter,src_element);
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                src_parameter=["rmfElement"]
                src_element=["DVRSrc"]
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
