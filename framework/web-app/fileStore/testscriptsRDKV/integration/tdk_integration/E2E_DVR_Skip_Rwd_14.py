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
  <id>1099</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_DVR_Skip_Rwd_14</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>530</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Get_Record_URLS</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests rewind operation than normal stream speed in reverse direction for playback.
Test Case ID:E2E_DVR_Skip_Rwd_14</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import dvrlib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_DVR_Skip_Rwd_14');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus ;
if "Success" in loadmodulestatus:
  obj.setLoadModuleStatus("SUCCESS");
  print "tdkintegration module loaded successfully";

  #Prmitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('TDKE2E_Get_Record_URLS');
  streamDetails = tdkTestObj.getStreamDetails('01');

  #Framing URL for slow rewind Request
  url="http://"+streamDetails.getGatewayIp()+":8080/vldms/info/recordingurls"
  print "RecordURL : %s" %url;

  #Configuring the test object for test execution
  tdkTestObj.addParameter("RecordURL",url);

  #Execute the test case in STB
  Recording_urls_expectedresult="SUCCESS";
  tdkTestObj.executeTestCase(Recording_urls_expectedresult);

  #Get the result of execution
  Recording_urls_actualresult = tdkTestObj.getResult();
  print "Dvr TrickPlay Result : %s" %Recording_urls_actualresult;

  Url_Array = [];
  if Recording_urls_expectedresult in Recording_urls_actualresult:
    #Get the log path of the Dvr Test
    logpath =tdkTestObj.getLogPath();
    print "Log Path :%s"%logpath;

    #Transferring the Dvr_Trick Play Test Logs
    tdkTestObj.transferLogs( logpath, "false" );

    #Get the list of recorded urls and details from the logpath
    dvrObj = tdkTestObj.getDVRDetails(logpath);
    urlList= dvrObj.getURLList();

    #Find total number of recorded contents available
    Total_Num_Urls=len(urlList)
    print Total_Num_Urls;
    if (Total_Num_Urls > 0):
      #Parsing each recorded contents
      for url in range(len(urlList)):
        print urlList[url];

        #Prmitive test case which associated to play the Script
        tdkTestObj = obj.createTestStep('TDKE2E_Play_URL');

        #Calling 'TDKE2E_PlayURL' function to send the url
        playurl=urlList[url]+"time_pos=-30000";

        #Configuring the test object for play url test execution
        tdkTestObj.addParameter("videoStreamURL",playurl);

        #Execute the test case in STB
        mplayer_expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(mplayer_expectedresult);

        #Get the result of execution
        mplayer_actualresult = tdkTestObj.getResult();
        print " mplayer_actualresult :%s" % mplayer_actualresult;

        #Get the log path of the Dvr Trickplay Test
        logpath =tdkTestObj.getLogPath();
        print "Log Path :%s"%logpath;

        #Transferring the Dvr Trickplay Test Logs
        tdkTestObj.transferLogs( logpath, "false" );

        if mplayer_expectedresult in mplayer_actualresult:
          Url_Array.append('SUCCESS');
          tdkTestObj.setResultStatus("SUCCESS");
        else:
          Url_Array.append('FAILURE');
          tdkTestObj.setResultStatus("FAILURE");
    else:
      print "There is no recorded items to play";
      tdkTestObj.setResultStatus("SUCCESS");

  else:
    tdkTestObj.setResultStatus("FAILURE");

  for list in range(len(Url_Array)-1):
     print "Array result : %s" %Url_Array[list];
     Url=Url_Array[list];
     print "Url : %s" %Url;
     if Url == "FAILURE":
        tdkTestObj.setResultStatus("FAILURE");
     else:
        tdkTestObj.setResultStatus("SUCCESS");

  #Unload the Dvr Trickplay test module
  obj.unloadModule("tdkintegration");
else:
  print "Failed to load Dvr Trickplay";
  obj.setLoadModuleStatus("FAILURE");
