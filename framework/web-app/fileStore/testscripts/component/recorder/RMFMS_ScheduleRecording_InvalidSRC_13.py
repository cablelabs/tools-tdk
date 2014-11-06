'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>987</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMFMS_ScheduleRecording_InvalidSRC_13</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>540</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_ScheduleRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test is to check scheduling current recording with Invalid sourceID.
Test Case Id: CT_Recorder_02</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test causes the RMFStreamer to crash and reboot the box. This is a bug in RDK</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
obj = tdklib.TDKScriptingLibrary("Recorder","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMFMS_ScheduleRecording_InvalidSRC_13');

#Get the result of connection with test component and STB
loadmodulestatus =obj.getLoadModuleResult();
print "Recorder module loading status :%s" %loadmodulestatus ;
#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in loadmodulestatus.upper():

        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        obj.initiateReboot();
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_ScheduleRecording');
        rec_id = random.randint(10000, 500000);
        recording_id = str(rec_id);
        duration = "180000";
        start_time = "0";
        validid = "0x@@";
        utctime=tdkTestObj.getUTCTime();
        tdkTestObj.addParameter("UTCTime",utctime);
        tdkTestObj.addParameter("Duration",duration);
        tdkTestObj.addParameter("Recording_Id",recording_id);
        tdkTestObj.addParameter("Start_time",start_time);
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
        if "SUCCESS" in actualresult:
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
                        PATTERN = "Complete";
                        tdkTestObj.addParameter("Recording_Id",recording_id);
                        #Execute the test case in STB
                        expectedresult="FAILURE";
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
                                        print "Successfully scheduled a Recording";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "Recording is not scheduled with requested duration";
                        else:
                                print "Failed to schedule a Recording";
                                tdkTestObj.setResultStatus("FAILURE");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to Receive Json Message";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Recorder Failed to receive the requested recording url";
        #unloading Recorder module
        obj.unloadModule("Recorder");
else:
        print "Failed to load Recorder module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
