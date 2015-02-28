'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1041</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_TrickPlay_50</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>534</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>E2E_RMF_DVR_TrickPlay_50: To verify the video playback when (Fast Forward/Rewind) is done at 4x speed from the starting point of the video and then (Skip Forward/Skip Backward) is done multiple times.</synopsis>
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
    <box_type>Hybrid-1</box_type>
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
forwardPlaySpeed = 4;

#Set the trick play speed for rewind
rewindPlaySpeed = -4;

#Set the Number of seconds to skipforward.
skipForwardSec = 10

#Set the Number of seconds to skipbackward.
skipBackwardSec = 10

#Number of repeatation
repeatCount = 5;

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_50');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "tdkintegration module loaded: %s" %result; 

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    #Prmitive test case which associated to this Script
    tdkTestObj =obj.createTestStep('TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB');

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_FF_FR_SF_SB');

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

         print "The trick play speed forward requested: %f"%forwardPlaySpeed
         tdkTestObj.addParameter("forwardSpeed",forwardPlaySpeed);

         print "The trick play speed rewind requested: %f"%rewindPlaySpeed
         tdkTestObj.addParameter("rewindSpeed",rewindPlaySpeed);

         print "The number of seconds to skip forward requested: %d"%skipForwardSec
         tdkTestObj.addParameter("sfSeconds",skipForwardSec);

         print "The number of seconds to skip backward requested: %d"%skipBackwardSec
         tdkTestObj.addParameter("sbSeconds",skipBackwardSec);

         print "The number of repeatation requested is %d"%repeatCount
         tdkTestObj.addParameter("rCount",repeatCount);

         #Execute the test case in STB
         expectedresult="SUCCESS";
         tdkTestObj.executeTestCase(expectedresult);
         #Get the result of execution
         actualresult = tdkTestObj.getResult();
         details =  tdkTestObj.getResultDetails();

         print "The E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time: %s" %actualresult;

         #compare the actual result with expected result
         if expectedresult in actualresult:
                 #Set the result status of execution
                 tdkTestObj.setResultStatus("SUCCESS");
                 print "E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time Successful: [%s]"%details;
         else:
                 tdkTestObj.setResultStatus("FAILURE");
                 print "E2E DVR to play, Forward/rewind and Skip forward/backward number of seconds multiple time Failed: [%s]"%details;
         time.sleep(40);
         obj.unloadModule("tdkintegration");
    else:
        print "No Matching recordings list found"
					 
        time.sleep(10);
        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
