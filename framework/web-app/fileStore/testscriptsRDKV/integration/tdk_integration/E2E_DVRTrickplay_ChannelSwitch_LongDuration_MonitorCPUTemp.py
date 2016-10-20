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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_DVRTrickplay_ChannelSwitch_LongDuration_MonitorCPUTemp</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Continuous channel change, DVR playback and trickplay for a period of time (8hr) and fetch CPU temp in each iteration.
Testcase ID: E2E_LinearTV_55</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>600</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
from tdkintegration import getURL_PlayURL;
from devicesettings import dsManagerInitialize,dsManagerDeInitialize,dsGetCPUTemp;
from time import sleep;
from timeit import default_timer;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#### Start DVR_PlayURL ####
def DVR_PlayURL(tdkIntObj):

        #Primitive test case which associated to this Script
        tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        #set the dvr play url
        streamDetails = tdkTestObj.getStreamDetails("01");

        duration = 4
        recordingObj = tdkTestObj.getRecordingDetails(duration);
        if recordingObj:
                #fetch recording id from recordingObj
                recordID = recordingObj[1]
                print "Record ID = %s" %recordID
                playSpeedlist = ['1.00','4.00','8.00','15.00','30.00','60.00']
                for speed in playSpeedlist:
                        url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=' + speed +'&time_pos=0.00'
                        print "The Play DVR Url Requested: %s" %url
                        tdkTestObj.addParameter("playUrl",url);
                        #Execute the test case in STB
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the result of execution
                        actualresult = tdkTestObj.getResult();
                        details =  tdkTestObj.getResultDetails();
                        print "E2E DVR FF playback tested with " + speed.replace(".00","") + "x Speed from starting point of the video: %s" %actualresult;

                        #compare the actual result with expected result
                        if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "E2E DVR Playback Successful: [%s]"%details;
                                retValue = "SUCCESS"
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "E2E DVR Playback Failed: [%s]"%details;
                                retValue = "FAILURE"
                                break;
        else:
                print "No Matching recordings list found"
                retValue = "FAILURE"

        return retValue

#### End DVR_PlayURL ####

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'E2E_DVRTrickplay_ChannelSwitch_LongDuration_MonitorCPUTemp');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" not in result:
                print "Failed to Initialize device setting. Exiting..."
                #Unload the deviceSettings module
                dsObj.unloadModule("devicesettings");
                exit()

        #Load tdkintegration module
        tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
        tdkIntObj.configureTestCase(ip,port,'E2E_DVRTrickplay_ChannelSwitch_LongDuration_MonitorCPUTemp');
        #Get the result of connection with test component and STB
        tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
        print "tdkintegration module loading status : %s" %tdkIntLoadStatus;
        tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

        if "SUCCESS" in tdkIntLoadStatus.upper():
                testTimeInHours = 8
                testTime = testTimeInHours * 60 * 60
                timer = 0
                iteration = 0

                while (timer < testTime):

                        startTime = 0
                        startTime = default_timer()
                        iteration = iteration + 1
                        print "\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)

                        #Calling the getURL_PlayURL function for the requested StreamID
                        print "\nPlaying Channel 1"
                        result1 = getURL_PlayURL(tdkIntObj,'01');

                        #Calling the getURL_PlayURL function for the requested StreamID
                        print "\nPlaying Channel 2"
                        result2 = getURL_PlayURL(tdkIntObj,'02');

                        #Calling the DVR_PlayURL function for playing recorded content and DVR trickplay
                        print "\nPlaying DVR in different speed"
                        resultDVR = DVR_PlayURL(tdkIntObj);

                        if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()) and ("SUCCESS" in resultDVR.upper()):
                                print "Execution Success at iteration %d" %(iteration);
                        else:
                                print "Execution failure at iteration %d" %(iteration);
                                break;

                        #Calling Device Setting Get CPU Temperature
                        dsResult,dsDetails = dsGetCPUTemp(dsObj,"SUCCESS")

                        sleep(40);

                        stopTime = default_timer()
                        timer = timer + (stopTime - startTime)

                        print "Total Time in Seconds = %f" %(timer)

                #Unload the tdkintegration module
                tdkIntObj.unloadModule("tdkintegration");

        #Calling DS_ManagerDeInitialize to DeInitialize API
        result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
