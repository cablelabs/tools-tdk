#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>923</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_MS_RecordingPlayback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>493</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>MS_RMFStreamer_Player</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This scripts test the  Requesting  Recorded content playback via streaming Interface.
Test case Id: CT_RMFStreamer_17</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediastreamer","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
 
obj.configureTestCase(ip,port,'RMF_MS_RecordingPlayback_26');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "RMFStreamer module :  %s" %result;

if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "RmfStreamer load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------

         duration = 4
         matchList = []
         matchList = tdkTestObj.getRecordingDetails(duration);
         obj.resetConnectionAfterReboot()
         tdkTestObj = obj.createTestStep('MS_RMFStreamer_Player');
	#-----------End-----------------
         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");
         time.sleep(2)
		 
         if matchList:
		 
              print "Recording Details : " , matchList

              #fetch recording id from list matchList.
              recordID = matchList[1]
        
              #url = 'http://169.254.224.174:8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=1.00&time_pos=0.00'
              url = "http://"+ streamDetails.getGatewayIp() + ":8080/vldms/dvr?rec_id=" + recordID[:-1]; 
              print "The Play DVR Url Requested: %s"%url
              tdkTestObj.addParameter("VideostreamURL",url);
              playtime = 30;
              tdkTestObj.addParameter("play_time",playtime);         
              #Execute the test case in STB
              expectedresult="SUCCESS";
              tdkTestObj.executeTestCase(expectedresult);
          
              #Get the result of execution
              actualresult = tdkTestObj.getResult();
         

              print "The DVR to play in normal speed : %s" %actualresult;

              #compare the actual result with expected result
              if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "DVR Playback in normal speed";
              else:
                 tdkTestObj.setResultStatus("FAILURE");
                 details =  tdkTestObj.getResultDetails();
                 print "DVR Play in normal speed Failed :[%s]"%details;

         else:
               print "No Matching recordings list found"
               obj.unloadModule("mediastreamer");
else:
         print "Failed to RmfStreamer module";
         obj.setLoadModuleStatus("FAILURE");
