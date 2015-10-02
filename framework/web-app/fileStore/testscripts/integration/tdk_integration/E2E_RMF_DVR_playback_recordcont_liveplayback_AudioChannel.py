'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1669</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>17</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_playback_recordcont_liveplayback_AudioChannel</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Try to playback the recorded when live playback in Audio channel</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>Cusing ABL mode in Pace Xi3</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import getURL_PlayURL,dvr_playback

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
obj.configureTestCase(ip,port,'E2E_RMF_DVR_playback_recordcont_liveplayback_AudioChannel');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successfuls";   
   
    #Calling getURL_PlayURL for Live playback of Radio Channel
    result1 = getURL_PlayURL(obj,'R01');

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TestMgr_LinearTv_AudioChannel_Play');

    duration = 1
    #recInfoAsList = [index,recordingId,recordingTitle,duration,segmentName]
    recInfoAsList = tdkTestObj.getRecordingDetails(duration);
    if not recInfoAsList:
           print "Recording details list is empty"; 
           tdkTestObj.setResultStatus("FAILURE");
    recording_id = recInfoAsList[1]

    #Calling DvrPlay_rec to play the recorded content
    result2 = dvr_playback(tdkTestObj,recording_id[:-1]);
    
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution Success"
    else:            
        print "Execution failure"
        obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load tdkintegration module";
    obj.setLoadModuleStatus("FAILURE");
