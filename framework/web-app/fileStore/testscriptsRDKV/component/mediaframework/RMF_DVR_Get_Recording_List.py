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
  <id>1168</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_DVR_Get_Recording_List</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>488</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_GetDvr_Recording_List</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Get the List and details of the DVR recordings.</synopsis>
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
import time;
import os;

logpath = ""
numOfRecordings = 0
def rmfAppMod():

    print "Entering into rmfApp function"
    obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

    #IP and Port of box, No need to change,
    #This will be replaced with corresponding Box Ip and port while executing script
    ip = <ipaddress>
    port = <port>
    obj.configureTestCase(ip,port,'TdkRmfApp_CreateRecording');

    #Get the result of connection with test component and STB
    result =obj.getLoadModuleResult();
    print "[LIB LOAD STATUS]  :  %s" %result;

    print "rmfApp module loading status :%s" %result;

    if "SUCCESS" not in result.upper():
         print "Failed to load rmfapp module";
         obj.setLoadModuleStatus("FAILURE");
         return 0;

    obj.setLoadModuleStatus(result);

    #Prmitive test case which initiates recording if no recordings found
    tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

    streamDetails = tdkTestObj.getStreamDetails('01');

    recordtitle = "test_dvr"
    recordid = "11111114"
    recordduration = "1"
    ocapid = streamDetails.getOCAPID();

    print "Record ID : ", recordid
    print "Duration : ", recordduration
    print "Title : ", recordtitle
    print "Ocap ID : ", ocapid

    tdkTestObj.addParameter("recordId",recordid);
    tdkTestObj.addParameter("recordDuration",recordduration);
    tdkTestObj.addParameter("recordTitle",recordtitle);
    tdkTestObj.addParameter("ocapId",ocapid);

    expectedresult="SUCCESS"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    print "[TEST EXECUTION RESULT] : %s" %result;

    if expectedresult in result:
        tdkTestObj.setResultStatus("SUCCESS");
	print "SUCCESS: command was processed by rmfApp application."
        duration = int(recordduration)
        time.sleep(duration * 60) #delay so that recording will happen.
	time.sleep(10)
        obj.initiateReboot()

    else:
        tdkTestObj.setResultStatus("FAILURE");
        details=tdkTestObj.getResultDetails();
        print "FAILURE: rmfApp failed. Details: %s" %details;

    obj.unloadModule("rmfapp");

    return 0;

def getRecordList():
     #Test component to be tested
     obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

     #IP and Port of box, No need to change,
     #This will be replaced with correspoing Box Ip and port while executing script
     ip = <ipaddress>
     port = <port>
     obj.configureTestCase(ip,port,'RMF_DVR_Get_Recording_List');

     #Get the result of connection with test component and STB
     result =obj.getLoadModuleResult();
     print "[LIB LOAD STATUS]  :  %s" %result;
     loadmoduledetails = obj.getLoadModuleDetails();
     print "Load Module Details : %s" %loadmoduledetails;

     if "FAILURE" in result.upper():
		if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
			print "rmfStreamer is not running. Rebooting STB"
			obj.initiateReboot();
			#Reload Test component to be tested
			obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
			obj.configureTestCase(ip,port,'RMF_DVR_Get_Recording_List');
			#Get the result of connection with test component and STB
			result = obj.getLoadModuleResult();
			print "Re-Load Module Status :  %s" %result;
			loadmoduledetails = obj.getLoadModuleDetails();
			print "Re-Load Module Details : %s" %loadmoduledetails;

     print "Mediaframework module loading status :%s" %result;

     if "SUCCESS" in result.upper():
          obj.setLoadModuleStatus("SUCCESS");
          #Prmitive test case which associated to this Script
          tdkTestObj = obj.createTestStep('RMF_GetDvr_Recording_List');

          expectedRes = "SUCCESS"

          #Execute the test case in STB
          tdkTestObj.executeTestCase(expectedRes );

          #Get the result of execution
          result = tdkTestObj.getResult();
          print "[TEST EXECUTION RESULT] : %s" %result;

          #Get the log path of the Dvr Record List

          global logpath
          logpath  = tdkTestObj.getLogPath();
          print "Recording List File Path: %s"%logpath;

          if "NULL" in logpath.upper():
               tdkTestObj.setResultStatus("FAILURE");
               details=tdkTestObj.getResultDetails();
               print "FAILURE: Details: %s" %details;
               obj.unloadModule("mediaframework");
               return 0;

          recordingObj = tdkTestObj.getRecordingDetails(1,logpath);

          global numOfRecordings
          numOfRecordings = recordingObj.getTotalRecordings();

          print "Number of recordings: %d"%numOfRecordings
          #Set the result status of execution
          tdkTestObj.setResultStatus("SUCCESS");

          obj.unloadModule("mediaframework");
     else:
          print "Failed to load mediaframework module";
          obj.setLoadModuleStatus("FAILURE");

     return 0

#Fetch the recording list.
getRecordList();
print "Finished call to get RecordList"

#If recordDetails file Creation fails, exit without running other scripts
if "NULL" not in logpath.upper():
     #check if numOfRecordings is 0, then initiate the recording.
     if 0 == numOfRecordings:
          rmfAppMod();
          getRecordList();
          print "Finished call to rmfAppMod"
