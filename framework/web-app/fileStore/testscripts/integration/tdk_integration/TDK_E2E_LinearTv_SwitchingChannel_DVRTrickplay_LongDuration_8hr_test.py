'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1628</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TDK_E2E_LinearTv_SwitchingChannel_DVRTrickplay_LongDuration_8hr_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Continuous Channel change, DVR playback and trickplay for a period of time (8hr)
Testcase ID: E2E_LinearTV_42</synopsis>
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
import time;
import timeit;
import tdkintegration;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

testTimeInHours = 8

def getURL_PlayURL(obj,streamId):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');

    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);
    url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");
	return "FAILURE";

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();


    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        details =  tdkTestObj.getResultDetails();

        #Remove unwanted part from URL
        PLAYURL = details.split("[RESULTDETAILS]");
        ValidURL = PLAYURL[-1];

        expectedresult="SUCCESS";

        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        print "Play Url Requested: %s"%(ValidURL);
        tdkTestObj.addParameter("playUrl",ValidURL);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        print "The E2E LinearTv Play : %s" %actualresult;

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "E2E LinearTv Playback Successful: [%s]"%details;
            retValue = "SUCCESS"

        else:
            tdkTestObj.setResultStatus("FAILURE");
            details =  tdkTestObj.getResultDetails();
            print "Execution Failed: [%s]"%(details);
            retValue = "FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Json Response Parameter is Failure";
        retValue = "FAILURE";

    return retValue


def DVR_PlayURL(obj):

         #Primitive test case which associated to this Script
         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

         #set the dvr play url
         streamDetails = tdkTestObj.getStreamDetails("01");

         recordingObj = tdkTestObj.getRecordingDetails(duration);
         numberOfRecordings = recordingObj.getTotalRecordings();
         print "\nNumber of recordings: %d" %numberOfRecordings

         recordID = recordingObj.getRecordingId (numberOfRecordings - 1);
         print "\nRecord ID = %s" %recordID

         playSpeedlist = ['1.00','4.00','8.00','15.00','30.00','60.00']
         print "Play speed list : %s " %playSpeedlist

         for i in range (0, len(playSpeedlist)):

                 url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=' + playSpeedlist[i] +'&time_pos=0.00'
                 print "The Play DVR Url Requested: %s" %url

                 tdkTestObj.addParameter("playUrl",url);

                 #Execute the test case in STB
                 expectedresult="SUCCESS";
                 tdkTestObj.executeTestCase(expectedresult);

                 #Get the result of execution
                 actualresult = tdkTestObj.getResult();
                 details =  tdkTestObj.getResultDetails();

                 print "The E2E DVR playback of Fast Forward is tested with " + playSpeedlist[i].replace(".00","") + "x Speed from starting point of the video: %s" %actualresult;

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

                 time.sleep(40);

         return retValue


obj.configureTestCase(ip,port,'TDK_E2E_LinearTv_SwitchingChannel_DVRTrickplay_LongDuration');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():

    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0

    while (timer < testTime):

        startTime = 0
        startTime = timeit.default_timer()
        iteration = iteration + 1
        print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)

        #Calling the getURL_PlayURL function for the requested StreamID
        print "\nPlaying Channel 1"
        result1 = getURL_PlayURL(obj,'01');

        #Calling the getURL_PlayURL function for the requested StreamID
        print "\nPlaying Channel 2"
        result2 = getURL_PlayURL(obj,'02');

        #Calling the DVR_PlayURL function for playing recorded content and DVR trickplay
        print "\nPlaying DVR in different speed"
        resultDVR = DVR_PlayURL(obj);

        if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()) and ("SUCCESS" in resultDVR.upper()):                         
            print "Execution Success at iteration %d" %(iteration);
        else:
            print "Execution failure at iteration %d" %(iteration);
            break;

        stopTime = timeit.default_timer()
        timer = timer + (stopTime - startTime)
      
    print "Total Time in Seconds = %f" %(timer) 
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
