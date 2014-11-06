'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1663</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_RadioChannel_Recording</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Try to  record the radio chennal in XG1</synopsis>
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
obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_RadioChannel_Recording');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

if "SUCCESS" not in result.upper():
    obj.setLoadModuleStatus("FAILURE");
    exit;

obj.setLoadModuleStatus(result);
print "rmfApp module loading status :%s" %result;

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

streamDetails = tdkTestObj.getStreamDetails('R01');

recordtitle = "test_dvr"
rec_id = random.randint(10000, 500000);
recordid = str(rec_id);
recordduration = "2"
ocapid = streamDetails.getOCAPID();

print recordid
print recordduration
print recordtitle
print ocapid

tdkTestObj.addParameter("recordId",recordid);
tdkTestObj.addParameter("recordDuration",recordduration);
tdkTestObj.addParameter("recordTitle",recordtitle);
tdkTestObj.addParameter("ocapId",ocapid);

expectedresult="SUCCESS"

#Execute the test case in STB
tdkTestObj.executeTestCase(expectedresult);

print "After execution"

#Get the result of execution
result = tdkTestObj.getResult();

if expectedresult in result:
    tdkTestObj.setResultStatus("SUCCESS");
    details=tdkTestObj.getResultDetails();
else:
    tdkTestObj.setResultStatus("FAILURE");
    details=tdkTestObj.getResultDetails();

obj.unloadModule("rmfapp");



''''

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Tune_RadioChannel_Recording');

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
        rec_id = random.randint(10000, 500000);
        recording_id = str(rec_id);
        duration = "180000";
        start_time = "0";
        utctime=tdkTestObj.getUTCTime();
        tdkTestObj.addParameter("UTCTime",utctime);
        tdkTestObj.addParameter("Duration",duration);
        tdkTestObj.addParameter("Recording_Id",recording_id);
        tdkTestObj.addParameter("Start_time",start_time);
        streamDetails = tdkTestObj.getStreamDetails('13');
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
                                print "TDK_Server received the Json Message";
                                #Prmitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('Recorder_checkRecording_status');
                                PATTERN = validid;
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
                                        if (PATTERN in patterndetails)and(duration_string in patterndetails):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                #Getting the mplayer log file from DUT
                                                logpath=tdkTestObj.getLogPath();
                                                print "Log path : %s" %logpath;
                                                tdkTestObj.transferLogs(logpath,"false");
                                                print "Successfully scheduled a Recording";
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
'''

