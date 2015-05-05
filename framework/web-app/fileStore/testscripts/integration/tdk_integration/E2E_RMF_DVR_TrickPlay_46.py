'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1038</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_46</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>537</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_Pause_FF_FR</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_46: To verify the transition in the video playback by allowing the video to play for sometime, then pause the video and then do Fast Rewind at 4x speed while the video is paused.</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
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
import tdkintegration;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Set the trick play speed for forward
rewindPlaySpeed = -4.0

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_46');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result; 

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    #Prmitive test case which associated to this Script
    tdkTestObj =obj.createTestStep('TDKE2E_Rmf_Dvr_Play_Pause_FF_FR');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_Pause_FF_FR');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    

    if matchList:
		 
         print "Recording Details : " , matchList
         #fetch recording id from list matchList.
         recordID = matchList[1]
         url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );
         if url == "NULL":
             print "Failed to generate the Streaming URL";
             tdkTestObj.setResultStatus("FAILURE");
         print "The Play DVR Url Requested: %s"%url
         tdkTestObj.addParameter("playUrl",url);

         print "The trick play speed for rewind requested: %f"%rewindPlaySpeed
         tdkTestObj.addParameter("trickPlayRate",rewindPlaySpeed);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);

         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR to play in normal speed, pause and rewind in -4x : %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR Play in normal speed, pause and rewind in -4x Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR Play in normal speed, pause and rewind in -4x Failed: [%s]"%details;
         time.sleep(40);
         obj.unloadModule("tdkintegration");
    else:
         time.sleep(40);
         obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
