# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>3</version>
  <name>E2E_DVRTrickplay_ChannelSwitch_LongDuration_MonitorCPUTemp</name>
  <primitive_test_id>541</primitive_test_id>
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Continuous channel change, DVR playback and trickplay for a period of time (8hr) and fetch CPU temp in each iteration.
Testcase ID: E2E_LinearTV_55</synopsis>
  <groups_id/>
  <execution_time>600</execution_time>
  <long_duration>true</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>IPClient-3</box_type>
    <box_type>IPClient-4</box_type>
    <box_type>Emulator-Client</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>E2E_LinearTV_54</test_case_id>
    <test_objective>LinearTV-Channel Change, DVR playback and Trickplay for longduration (8hr) and monitoring CPU temperature via devicesetting.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>X13_1</test_setup>
    <pre_requisite>Requesturl: http://Ipaddress:port /videoStreamInit?live=ocap://ID</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.XG1 and XI3 should be up and running                  2.Only one XG1 should be up in a network</input_parameters>
    <automation_approch>1.TM loads Tdkintegration_agent and DeviceSettingsAgent via the test agent 
2.TM Frames the request URL and makes a RPC calls to the tdkintegration_agent for tune
3.tdkintegration_agent will get request url from TM and sends to the XG1.Upon receiving the response (Json response) the agent should extract the response url and send to TM.
4.TM sends the Response Url to the LinearTV_agent for playback with the hnsrc-mpsink pipeline  for 60 seconds"
5 Repeat the steps 3 and 4
6. tdkintegration_agent will get request url from TM 
7. TM sends the Response Url for DVR playback for 60 seconds"
8 TM run the trickplay in 4x 15x 30x and 60x speeds
9. Get the CPU temperature from DeviceSettingsAgent.
10. loop the steps 2-9  for a different service and continue for eight hours
11. tdkintegration_agent will send SUCCESS or FAILURE to TM.</automation_approch>
    <except_output>Checkpoint 1.Verifying the playback of player and get the state of play
Checkpoint 2 Error code parameter of Json response is verified as success or failure. 
Checkpoint 3 Response logs verified to check the trickplay occur at the corresponding speeds.
Checkpoint 4. Script to check whether the audio pid and video pid is set
Checkpoint 5. Verify if the cpu temperature is within limit, more than 0 and less than 125 C.</except_output>
    <priority>High</priority>
    <test_stub_interface>libdevicesettingsstub.so
tdkIntegrationstub.so</test_stub_interface>
    <test_script>E2E_DVRTrickplay_ChannelSwitch_LongDuration_MonitorCPUTemp</test_script>
    <skipped>No</skipped>
    <release_version/>
    <remarks/>
  </test_cases>
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
