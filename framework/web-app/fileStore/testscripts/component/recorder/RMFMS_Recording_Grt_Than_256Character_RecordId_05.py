'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_Recording_Grt_Than_256Character_RecordId_05</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To Initiate recording with recording Id of length more then 256 characters.
Test Case Id: CT_RECORDER_RECORDID_256CHARCTER_05
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>Emulator-HYB</box_type>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMFMS_Recording_Grt_Than_256Character_RecordId_05');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        obj.initiateReboot();
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_ScheduleRecording');
        rec_id = random.randrange(10**9, 10**258)
        recording_id = str(rec_id);
        duration = "180000";
        start_time = "0";
        #utctime=tdkTestObj.getUTCTime();
        #tdkTestObj.addParameter("UTCTime",utctime);
        tdkTestObj.addParameter("Duration",duration);
        tdkTestObj.addParameter("Recording_Id",recording_id);
        tdkTestObj.addParameter("Start_time",start_time);
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
                print "ocapid : %s" %validid;
                tdkTestObj.addParameter("Source_id",validid);
                #Execute the test case in STB
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                #Get the Actual result of streaming Interface
                actualresult = tdkTestObj.getResult();
                Jsonurldetails = tdkTestObj.getResultDetails();
                print "Result of scheduling : %s" %actualresult;
                print "Jsonurldetails is : %s" %Jsonurldetails;
                RequestURL = Jsonurldetails.replace("\\","");
                print "RequestURL  is : %s" %RequestURL ;
                #compare the actual result with expected result
                if expectedresult in actualresult:
                        status_expected = "acknowledgement";
                        print "Recorder received the requested recording url";
                        time.sleep(30);
                        status_actual =tdkTestObj.initiateRecorderApp(RequestURL);
                        print "Status string is: %s"%status_actual;
                        if status_expected in status_actual:
                                tdkTestObj.setResultStatus("SUCCESS");
                                time.sleep(100);
                                print "TDK_Server received the Json Message";
                                #Prmitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('Recorder_checkRecording_status');
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
                                                print "Failed to schedule a Recording with recordID length greater than 256 character";
                                        else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                #Getting the mplayer log file from DUT
                                                logpath=tdkTestObj.getLogPath();
                                                print "Log path : %s" %logpath;
                                                tdkTestObj.transferLogs(logpath,"false");
                                                print "Failed to search the pattern in the logfile";
                                else:
                                        print "Failed to schedule a Recording";
                                        tdkTestObj.setResultStatus("FAILURE");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to Receive acknowledgement from rmfStreamer";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Recorder Failed to receive the requested request-Please check precondition";
                #unloading Recorder module
                obj.unloadModule("Recorder");
        else:
                print "getSourceId is failed";
                tdkTestObj.setResultStatus("FAILURE");
else:
        print "Failed to load Recorder module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
