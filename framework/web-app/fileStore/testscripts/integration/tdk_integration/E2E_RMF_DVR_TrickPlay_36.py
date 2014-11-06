'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1029</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_36</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>551</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_Dvr_Skip_Backward_From_Middle</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_36: To verify the video playback when Skip backward is done once from the middle of the video playback.</synopsis>
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
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Number of times the pause/play should repeat.
skipNumOfSec = 10;

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_36');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();

if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";

         #Prmitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Skip_Backward_From_Middle');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         recordingObj = tdkTestObj.getRecordingDetails();
         num = recordingObj.getTotalRecordings();
         print "Number of recordings: %d"%num

         recordID = recordingObj.getRecordingId(num - 1);

         url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=1.00&time_pos=0.00'
         print "The Play DVR Url Requested: %s"%url
         tdkTestObj.addParameter("playUrl",url);

         print "The number of seconds to be skiped from end of video: %d"%skipNumOfSec
         tdkTestObj.addParameter("seconds",skipNumOfSec);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR Skip number of seconds from middle: %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Skip number of seconds from middle Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Skip number of seconds from middle Failed: [%s]"%details;
         time.sleep(40);
         obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKintegration module";
         obj.setLoadModuleStatus("FAILURE");