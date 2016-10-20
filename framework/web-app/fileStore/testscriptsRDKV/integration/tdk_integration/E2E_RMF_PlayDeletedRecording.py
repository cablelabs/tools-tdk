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
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_PlayDeletedRecording</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests attempt to playback deleted recording content.</synopsis>
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
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from mediaframework import createRecording,deleteRecording;
from tdkintegration import dvrPlayUrl;
from random import randint

#IP and Port of DVR box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Load mediaframework module
mfObj = tdklib.TDKScriptingLibrary('mediaframework','2.0');
mfObj.configureTestCase(ip,port,'E2E_RMF_PlayDeletedRecording');
mfLoadStatus = mfObj.getLoadModuleResult();
print '[mediaframework LIB LOAD STATUS] : %s'%mfLoadStatus;
mfObj.setLoadModuleStatus(mfLoadStatus);

mfLoadModuleDetails = mfObj.getLoadModuleDetails();
if "FAILURE" in mfLoadStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in mfLoadModuleDetails:
                print "rmfStreamer is not running. Rebooting STB"
                mfObj.initiateReboot();
                #Reload Test component to be tested
                mfObj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                mfObj.configureTestCase(ip,port,'E2E_RMF_PlayDeletedRecording');
                #Get the result of connection with test component and STB
		mfLoadStatus = mfObj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %mfLoadStatus;
                mfLoadModuleDetails = mfObj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %mfLoadModuleDetails;

if 'SUCCESS' in mfLoadStatus.upper():

        Id = randint(1000,10000)
        recordingId = str(Id)
        title = 'test_dvr_'+recordingId
        duration = '1'
        streamId = '01'

        #Record stream1
        result = createRecording(mfObj, kwargs={"ID":recordingId,"TITLE":title,"DURATION":duration,"STREAMID":streamId})
        if 'SUCCESS' in result:
                #Reboot the box
                mfObj.initiateReboot();

                #Load tdkintegration module
                tdkIntObj = tdklib.TDKScriptingLibrary('tdkintegration','2.0');
                tdkIntObj.configureTestCase(ip,port,'E2E_RMF_PlayDeletedRecording');
                tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
                print '[tdkintegration LIB LOAD STATUS] : %s'%tdkIntLoadStatus;
                tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

                if 'SUCCESS' in tdkIntLoadStatus.upper():
                        #Playback recorded content
                        result = dvrPlayUrl(tdkIntObj, kwargs={"ID":recordingId,"STREAMID":streamId})
                        #Delete recorded content
                        result = deleteRecording(mfObj,kwargs={'ID':recordingId,'STREAMID':streamId})
                        #Playback deleted recording
                        result = dvrPlayUrl(tdkIntObj, kwargs={"expectedResult":'FAILURE',"ID":recordingId,"STREAMID":streamId})
                        #unload tdkintegration module
                        tdkIntObj.unloadModule('tdkintegration');
        mfObj.unloadModule('mediaframework');
