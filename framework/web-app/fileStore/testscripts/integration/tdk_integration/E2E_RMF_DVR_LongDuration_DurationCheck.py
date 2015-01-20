'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVR_LongDuration_DurationCheck</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To schedule the  long duration recording and check the duration of the recorded content</synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkintegration import sched_rec

#Test component to be tested
media_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
rec_obj = tdklib.TDKScriptingLibrary("rmfapp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

                                        
rec_obj.configureTestCase(ip,port,'E2E_RMF_DVR_LongDuration_DurationCheck');
media_obj.configureTestCase(ip,port,'E2E_RMF_DVR_LongDuration_DurationCheck');

loadmodulestatus = rec_obj.getLoadModuleResult();
loadmodulestatus1 = media_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    media_obj.setLoadModuleStatus("SUCCESS");
    rec_obj.setLoadModuleStatus("SUCCESS");
    rec_duration = "600000"
    start_time = '0';
    result1,recording_id = sched_rec(rec_obj,'01',start_time,duration = rec_duration);

        
    if ("SUCCESS" in result1.upper()):
        
        print "Execution  Success"
        #Prmitive test case which associated to this Script
        tdkTestObj = media_obj.createTestStep('RMF_DVRManager_GetRecordingDuration');

        expectedRes = "SUCCESS"
        recordingId = recording_id;
        print "Requested record ID: %s"%recordingId
        tdkTestObj.addParameter("recordingId",recordingId);

        streamDetails = tdkTestObj.getStreamDetails('01');
        playUrl = 'http://' + streamDetails.getGatewayIp() + ':8080/vldms/tuner?ocap_locator=ocap://'+streamDetails.getOCAPID();
        print "Requested play url : %s" %playUrl;
        tdkTestObj.addParameter("playUrl",playUrl);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedRes);

        #Get the result of execution
        result = tdkTestObj.getResult();
        print "[TEST EXECUTION RESULT] : %s" %result;
        details = tdkTestObj.getResultDetails();
        if "SUCCESS" in result.upper():
            #Set the result status of execution
            mylist = details.split(" ");
            if (int(mylist[1]) <= ((int(rec_duration)/1000) + 10) and int(mylist[1]) >= ((int(rec_duration)/1000) - 10)):
                tdkTestObj.setResultStatus("SUCCESS");
                print "DVRManager GetRecordingDuration Successful: %s" %details;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "DVRManager GetRecordingDuration Failed: The Recording Duration is not in range limit [%s]"%details;
        else:
             tdkTestObj.setResultStatus("FAILURE");
             print "DVRManager GetRecordingDuration Failed: [%s]"%details;

    else:            
        print "Execution  failure"
         
    media_obj.unloadModule("mediaframework");
    rec_obj.unloadModule("rmfapp");
    
else:
    print "Failed to load media framework module";
    media_obj.setLoadModuleStatus("FAILURE");
    print "Failed to load recorder module";
    rec_obj.setLoadModuleStatus("FAILURE");
				
