'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1011</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_16</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>548</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_16: To verify the video playback when Fast rewind is done at -32x speed from the middle of the playback.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>12</execution_time>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>


obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_15');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();

if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         recordingObj = tdkTestObj.getRecordingDetails();
         num = recordingObj.getTotalRecordings();
         print "Number of recordings: %d"%num

         recordID = recordingObj.getRecordingId(num - 1);

         url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=1.00&time_pos=0.00'

         print "The Play DVR Url Requested: %s"%url
         tdkTestObj.addParameter("playUrl",url);

         #set the trick play speed
         trickPlayRate = -16.0
         print "The trick play rate: %f"%trickPlayRate
         tdkTestObj.addParameter("speed",trickPlayRate);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR playback when fast rewind is done at -16x speed from the middle of the video: %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Playback -16x speed Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Playback -16x speed Failed: [%s]"%details;
         time.sleep(40);
         obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");