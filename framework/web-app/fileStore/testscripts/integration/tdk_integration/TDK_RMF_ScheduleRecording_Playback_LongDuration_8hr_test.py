'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1657</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TDK_RMF_ScheduleRecording_Playback_LongDuration_8hr_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>556</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_Rmf_LinearTv_Dvr_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Continuously run the DVR schedule and playback for a period of time(8hr)
Testcase ID: E2E_DVR_PlayBack_02</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>600</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>Scheduling of recording not working</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import random;
import timeit;
import time;
import tdkintegration;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

testTimeInHours = 8


def playDVR (recordingId):

    #Test component to be tested
    obj1 = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

    obj1.configureTestCase(ip,port,'RMF_ScheduleRecording_Playback_LongDuration_8hr_test');

    #Get the result of connection with test component and STB
    result =obj1.getLoadModuleResult();
    print "tdkintegration module loading status :%s" %result;

    #Check for SUCCESS/FAILURE of tdkintegration module
    if "SUCCESS" in result.upper():
        obj1.setLoadModuleStatus("SUCCESS");
	
        #Prmitive test case which associated to this Script
        tdkTestObj = obj1.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        #set the dvr play url
        streamDetails = tdkTestObj.getStreamDetails("01");

        recordingObj = tdkTestObj.getRecordingDetails();
        numberOfRecordings = recordingObj.getTotalRecordings();
        print "\nNumber of recordings: %d" %numberOfRecordings
        recordID = recordingObj.getRecordingId(numberOfRecordings - 1)
        print "\nRecord ID = %s" %recordID        

        recordID = recordingId
        print "\nRecord ID = %s" %recordID

        url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );
        if url == "NULL":
             print "Failed to generate the Streaming URL";
             tdkTestObj.setResultStatus("FAILURE");
        print "The Play DVR Url Requested: %s" %url

        tdkTestObj.addParameter("playUrl",url);

        #Execute the test case in STB
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();
        details =  tdkTestObj.getResultDetails();

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

        #unloading tdkintegration module
        obj1.unloadModule("tdkintegration");

    else:
        print "Failed to load tdkintegration module";
        obj1.setLoadModuleStatus("FAILURE");
        retValue = "FAILURE"

    time.sleep(40);

    return retValue



obj.configureTestCase(ip,port,'RMF_ScheduleRecording_Playback_LongDuration_8hr_test');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "Mediaframework Dvr Mgr module loading status :%s" %result;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
	
    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0

    while (timer < testTime):

        startTime = 0
        startTime = timeit.default_timer()
        iteration = iteration + 1
        print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)
	
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('RMF_DVRManager_CreateRecording');
        expectedRes = "SUCCESS"
        rec_id = random.randint(10000, 500000);
        recordingId = str(rec_id);
        print "Requested record ID: %s" %recordingId;
        tdkTestObj.addParameter("recordingId",recordingId);

        duration = 120000
        print "Requested duration: %d"%duration;
        tdkTestObj.addParameter("recordDuration",duration);

        streamDetails = tdkTestObj.getStreamDetails('01');
        playUrl = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if playUrl == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "Requested url : %s" %playUrl;
        tdkTestObj.addParameter("qamLocator",playUrl);

        title = "TDK DVR Manager test create recording-" + recordingId
        print "Requested title : %s"%title;
        tdkTestObj.addParameter("recordingTitle",title);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedRes);

        #Get the result of execution
        result = tdkTestObj.getResult();
        print "Execution Result : %s" %result;
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result.upper():
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print "DVRManager CreateRecording Successful";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "DVRManager CreateRecording Failed: [%s]"%details;
            print "Recording Failed at iteration : " , iteration
            break;
		
        time.sleep(180);		
        retValue = playDVR(recordingId)
        if "SUCCESS" in retValue.upper():                         
            print "\nExecution Success at iteration %d" %(iteration);
        else:
            print "\nExecution failure at iteration %d" %(iteration);
            break;
			
        stopTime = timeit.default_timer()
        timer = timer + (stopTime - startTime)
					
    print "Total Time in Seconds = %f" %(timer)

    #unloading mediastreamer module
    obj.unloadModule("mediaframework");
else:
    print "Failed to load mediaframework module";
    obj.setLoadModuleStatus("FAILURE");
