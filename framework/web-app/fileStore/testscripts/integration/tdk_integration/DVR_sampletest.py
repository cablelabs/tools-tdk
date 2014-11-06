'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1623</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DVR_sampletest</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import random;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRManager_DeleteRecording');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

print "Mediaframework Dvr Mgr module loading status :%s" %result;

#Check for SUCCESS/FAILURE of Mediaframework module
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('RMF_DVRManager_DeleteRecording');

    expectedRes = "SUCCESS"

    recordingId = [157018,408562,79997 ,75630 ,33175 ,172687,22837 ,393486,15760 ,350217,452712,455309,194454,302372,135652,386470,332483,469160,205758,36969 ,381457,129228,229704,261124,46698 ,223648,428537,180664,453337,158578,336960,184389,10748 ,449533 ]
    for x in recordingId :
        print "Requested record ID: %s"%recordingId
        tdkTestObj.addParameter("recordingId",str(x));       

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
            tdkTestObj.setResultStatus("SUCCESS");
            print "DVRManager DeleteRecording Successful";
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "DVRManager DeleteRecording Failed: [%s]"%details;

    #unloading mediastreamer module
    obj.unloadModule("mediaframework");
else:
    print "Failed to load mediaframework module";
    obj.setLoadModuleStatus("FAILURE");
