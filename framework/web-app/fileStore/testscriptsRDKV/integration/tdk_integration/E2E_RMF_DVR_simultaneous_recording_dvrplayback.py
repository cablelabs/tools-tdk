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
  <id>1682</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_simultaneous_recording_dvrplayback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Simultaneous Record 2 Booked Clear Programme Instances with Playback from Disk</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
from tdkintegration import sched_rec,dvr_playback

#Test component to be tested
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_simultaneous_recording_dvrplayback');
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_simultaneous_recording_dvrplayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = rec_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                rec_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVR_simultaneous_recording_dvrplayback');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = rec_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    rec_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");

    #Schedule record for the given StreamID
    result1,recording_id = sched_rec(rec_obj,'01','0','120000');

    #Schedule record for the given StreamID
    result2,recording_id = sched_rec(rec_obj,'02','0','120000');

    tdk_obj.initiateReboot();
    rec_obj.resetConnectionAfterReboot()

    #Prmitive test case which associated to this Script
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    tdk_obj.resetConnectionAfterReboot()
    tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_RewindFromEndPoint');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)
		 
    if matchList:
		 
         print "Recording Details : " , matchList

         #fetch recording id from list matchList.
         recordID = matchList[1]

         result3 = dvr_playback(tdkTestObj,recording_id);
        
         if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()) and ("SUCCESS" in result3.upper()):                                        
             print "Execution  Success"
         else:           
		    print "Execution  failure"
		    rec_obj.unloadModule("rmfapp");
		    tdk_obj.unloadModule("tdkintegration");
    else:
         print "No Matching recordings list found"
	 obj.unloadModule("tdkintegration");			 
         time.sleep(10);
    
else:
    print "Failed to load rmfapp module";
    rec_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load TDK module";
    tdk_obj.setLoadModuleStatus("FAILURE");
