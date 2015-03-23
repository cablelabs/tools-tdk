'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>24</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_SixTuner_DVR_Now_10</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>514</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_checkRecording_status</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test tests the current recording of six simultaneous recordings
Test case ID:CT_Recorder_10</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import re;
import random;
import time;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_SixTuner_DVR_Now_10');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status :%s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recObj.initiateReboot();
        recObj.resetConnectionAfterReboot();

        tdkTestObj = recObj.createTestStep('Recorder_checkRecording_status');
        rec_id = random.randint(10000, 500000);
        recording_id = str(rec_id);
        duration = "400000";
        start_time = "0";
        #utctime=tdkTestObj.getUTCTime();
        #tdkTestObj.addParameter("UTCTime",utctime);
        streamDetails1 = tdkTestObj.getStreamDetails('01');
        validid1 = streamDetails1.getOCAPID();
        streamDetails2 = tdkTestObj.getStreamDetails('02');
        validid2 = streamDetails2.getOCAPID();
        streamDetails3 = tdkTestObj.getStreamDetails('03');
        validid3 = streamDetails3.getOCAPID();
        streamDetails4 = tdkTestObj.getStreamDetails('04');
        validid4 = streamDetails4.getOCAPID();
        streamDetails5 = tdkTestObj.getStreamDetails('05');
        validid5 = streamDetails5.getOCAPID();
        streamDetails6 = tdkTestObj.getStreamDetails('06');
        validid6 = streamDetails6.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid1);
        if Id:
                RequestURL = "{\"updateSchedule\" : {\"requestId\" : \"7\", \"schedule\" : [{\"recordingId\" : \""+str(int(recording_id))+"\",\"locator\" : [ \"ocap://"+validid1+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id))+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" },{\"recordingId\" : \""+str(int(recording_id)+1)+"\",\"locator\" : [ \"ocap://"+validid2+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id)+1)+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" },{\"recordingId\" : \""+str(int(recording_id)+2)+"\",\"locator\" : [ \"ocap://"+validid3+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id)+2)+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" },{\"recordingId\" : \""+str(int(recording_id)+3)+"\",\"locator\" : [ \"ocap://"+validid4+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id)+3)+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" },{\"recordingId\" : \""+str(int(recording_id)+4)+"\",\"locator\" : [ \"ocap://"+validid5+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id)+4)+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" },{\"recordingId\" : \""+str(int(recording_id)+5)+"\",\"locator\" : [ \"ocap://"+validid6+"\" ] ,\"epoch\" : ${now} ,\"start\" : "+start_time+" ,\"duration\" : "+duration+" ,\"properties\":{\"title\":\"Recording_"+str(int(recording_id)+5)+"\"},\"bitRate\" : \"HIGH_BIT_RATE\" ,\"deletePriority\" : \"P3\" }]}}";
                print "RequestURL  is : %s" %RequestURL ;
                #compare the actual result with expected result
                #if expectedresult in actualresult:
                status_expected = "acknowledgement";
                print "Recorder received the requested recording url";
                time.sleep(30);
                status_actual =tdkTestObj.initiateRecorderApp(RequestURL);
                print "Status string is: %s"%status_actual;
                if status_expected in status_actual:
                        time.sleep(100);
                        print "TDK_Server received the Json Message";
                        #Prmitive test case which associated to this Script
                        PATTERN = recording_id;
                        tdkTestObj.addParameter("Recording_Id",recording_id);
                        #Execute the test case in STB
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        #Get the Actual result of streaming Interface
                        actualresult = tdkTestObj.getResult();
                        print "In script **********************"
                        patterndetails = tdkTestObj.getResultDetails();
                        print "Pattern details is : %s" %patterndetails;
                        duration_int = int(duration);
                        duration_sec = duration_int/1000;
                        duration_string = str(duration_sec);
                        print duration_string;
                        #compare the actual result with expected result
                        if expectedresult in actualresult:
                                if (PATTERN in patterndetails):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        #Getting the mplayer log file from DUT
                                        logpath=tdkTestObj.getLogPath();
                                        print "Log path : %s" %logpath;
                                        tdkTestObj.transferLogs(logpath,"false");
                                        print "Successfully scheduled a Recording";
                                        time.sleep(5);
                                        #Get the tuner States
                                        #Load trm module
                                        trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
                                        trmObj.configureTestCase(ip,port,'Recorder_RMF_SixTuner_DVR_Now_10');
                                        #Get the result of connection with test component and STB
                                        trmLoadStatus = trmObj.getLoadModuleResult();
                                        print "TRM module loading status :%s" %trmLoadStatus;
                                        #Set the module loading status
                                        trmObj.setLoadModuleStatus(trmLoadStatus);
                                        #Check for SUCCESS/FAILURE of Recorder module
                                        if "SUCCESS" in trmLoadStatus.upper():
                                                trmTestObj = trmObj.createTestStep('TRM_GetAllTunerStates');
                                                expectedresult="SUCCESS";
                                                #Execute the test case in STB
                                                trmTestObj.executeTestCase(expectedresult);
                                                #Get the result of execution
                                                result = trmTestObj.getResult();
                                                if "SUCCESS" in result.upper():
                                                        trmTestObj.setResultStatus("SUCCESS");
                                                else:
                                                        trmTestObj.setResultStatus("FAILURE");
                                                details = trmTestObj.getResultDetails();
                                                print details;
                                                trmObj.unloadModule("trm");
                                        else:
                                                print "Failed to load TRM module";
                                        #Sleep till the Recording is complete to avoid problem with next test
                                        time.sleep(300);
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        #Getting the mplayer log file from DUT
                                        logpath=tdkTestObj.getLogPath();
                                        print "Log path : %s" %logpath;
                                        tdkTestObj.transferLogs(logpath,"false");
                                        print "Recording is not completed with requested duration";
                        else:
                                print "Failed to schedule a Recording";
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to Receive Json Message-Please check precondition";
                #else:
                #       tdkTestObj.setResultStatus("FAILURE");
                #      print "Recorder Failed to receive the requested request-Please check precondition";
                #unloading Recorder module
                recObj.unloadModule("Recorder");
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");
else:
        print "Failed to load Recorder module";
