'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1684</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>LinearTV – Try to select trick play when device is in Radio channel</synopsis>
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
    <box_type>IPClient-3</box_type>
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

from tdkintegration import getURL_PlayURL,dvr_playback;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
                                        
obj.configureTestCase(ip,port,'E2E_RMF_DVR_trickplay_recordcont_liveplayback_radiochannel');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successfuls";   
   
    #Calling getURL_PlayURL with valid Stream ID
    result1 = getURL_PlayURL(obj,'R01');
    
    time.sleep(150);

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
    
    recordingObj = tdkTestObj.getRecordingDetails();
    num = recordingObj.getTotalRecordings();
    print "Number of recordings: %d"%num

    recordID = recordingObj.getRecordingId(num - 1);

    #Calling getURL_PlayURL with valid Stream ID
    result2 = dvr_playback(tdkTestObj,recordID,play = 'trickplay');
        
    if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
        print "Execution Success"
    else:            
        print "Execution is failure"
         
    obj.unloadModule("tdkintegration");
    
else:
    print "Failed to load tdkintegration module";
    obj.setLoadModuleStatus("FAILURE");
