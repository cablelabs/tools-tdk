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
  <id>506</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_DVRSrcMPSink_SkipToEnd_05</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests the RDK Mediaframework DVRSrc element to skip to the end of the play.
Test Case ID: CT_RMF_DVRSrc_MPSink_05.	
Test Type: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRSrcMPSink_SkipToEnd_05');

expected_Failure="FAILURE"
expected_Result="SUCCESS"
currentTime = 0.0
pTime = 0.0
playTime = 0.0

startTime = 0.0
durationTime = 0.0
matchList = []

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global details
    global tdkTestObj
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

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if teststep != 'RMF_Element_GetState' and teststep != 'RMF_Element_Getmediatime':
        tdkTestObj.setResultStatus(result);

    if teststep == 'RMF_Element_Getmediatime':
        pos = details.find('MediaTime:');
        value = details[pos:];
        mediaTime = value[10:];
        print mediaTime;
        playTime = float(mediaTime);

    if teststep == 'RMF_Element_GetMediaInfo':
        pos = details.find('MediaStartTime');
        value = details[pos:]
        parts = value.partition(' ');
        partOne = parts[0];
        partTwo = parts[2];
        start = partOne[15:];
        end = partTwo[14:];
        print start;
        print end;
        startTime = float(start);
        durationTime = float(end);


    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;
   
    return result

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadModuleStatus;
loadmoduledetails = obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in loadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                obj.configureTestCase(ip,port,'RMF_DVRSrcMPSink_SkipToEnd_05');
                #Get the result of connection with test component and STB
                loadModuleStatus = obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %loadModuleStatus;
                loadmoduledetails = obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;
  
if expected_Result in loadModuleStatus.upper():
	tdkTestObj =obj.createTestStep('RMF_Element_Create_Instance');
	print "Load Module Status :  %s" %loadModuleStatus;
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
                                src_element=["MPSink"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                if expected_Result in result.upper():
                                        src_parameter=["rmfElement"]
                                        src_element=["MPSink"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                        if expected_Result in result.upper():
                                                src_parameter=["X","Y","width","height"];
                                                src_element=[0,0,1280,720];
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,expected_Result,src_parameter,src_element);
                                                if expected_Result in result.upper():
                                                        src_parameter=["rmfSourceElement","rmfSinkElement"];
                                                        src_element=["DVRSrc","MPSink"];
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,expected_Result,src_parameter,src_element);
                                                        if expected_Result in result.upper():
                                                                src_parameter=["rmfElement"];
                                                                src_element=["DVRSrc"];
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,expected_Result,src_parameter,src_element);
                                                                time.sleep(30);

                                                                if expected_Result in result.upper():
                                                                        src_parameter=["rmfElement"];
                                                                        src_element=["DVRSrc"];
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,expected_Result,src_parameter,src_element);
                                                                        if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                tdkTestObj.setResultStatus(result);
                                                                                src_parameter=["rmfElement"];
                                                                                src_element=["DVRSrc"];
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_GetMediaInfo',obj,expected_Result,src_parameter,src_element);
                                                                                if expected_Result in result.upper():
                                                                                        src_parameter=["rmfElement"];
                                                                                        src_element=["DVRSrc"];
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,expected_Result,src_parameter,src_element);
                                                                                        currentTime = playTime;
                                                                                        print "CurrentTime:",currentTime
                                                                                        setTime = startTime + durationTime;
                                                                                        print setTime;
                                                                                        if expected_Result in result.upper():
                                                                                                src_parameter=["rmfElement","mediaTime"];
                                                                                                src_element=["DVRSrc",setTime];
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Setmediatime',obj,expected_Result,src_parameter,src_element);

                                                                                                if expected_Result in result.upper():
                                                                                                        src_parameter=["rmfElement"];
                                                                                                        src_element=["DVRSrc"];
                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime',obj,expected_Result,src_parameter,src_element);
                                                                                                        pTime = playTime;
                                                                                                        print "Present Time:",pTime

                                                                                                        if pTime == 0.0:
                                                                                                                tdkTestObj.setResultStatus(result);
                                                                                                                print "DVRSource skiping to the end of the record Successful";
                                                                                                        else:

                                                                                                                tdkTestObj.setResultStatus(expected_Failure);
                                                                                                                print "DVRSource skiping to the end of the record Failed";
                                                                        else:
                                                                                tdkTestObj.setResultStatus(expected_Failure);
                                                src_parameter=["rmfElement"]
                                		src_element=["DVRSrc"]
                                                #src_element=["MPSink"]
                                                #result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                		result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["MPSink"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                        #result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                src_parameter=["rmfElement"]
                                src_element=["DVRSrc"]
                                #result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                        	result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        #result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                	result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                src_parameter=["rmfElement"]
                #src_element=["DVRSrc"]
                src_element=["MPSink"]
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");
