'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVRPlayback_Change_Zoom</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test tries to change the Zoom during DVR playback</synopsis>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from tdkintegration import dvr_playback
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
tdk_obj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 = tdk_obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        tdk_obj.setLoadModuleStatus("SUCCESS");

        #Prmitive test case which associated to this Script
        tdkTestObj = tdk_obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        recordingObj = tdkTestObj.getRecordingDetails();
        num = recordingObj.getTotalRecordings();
        print "Number of recordings: %d"%num    
        recording_id = recordingObj.getRecordingId(num - 1);

                    
        #Calling DvrPlay_rec to play the recorded content
        result = dvr_playback(tdkTestObj,recording_id);
        if ("SUCCESS" in result.upper()):
        
            #calling Device Settings - initialize API
            tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS :Application successfully initialized with Device Settings library";
                    #calling DS_SetDFC to get and set the zoom settings 
                    tdkTestObj = obj.createTestStep('DS_SetDFC');
                    #zoom="Full";
                    zoom="Platform";
                    print "Zoom value set to :%s" %zoom;
                    tdkTestObj.addParameter("zoom_setting",zoom);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    dfcdetails = tdkTestObj.getResultDetails();
                    setdfc="%s" %zoom;
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                            print "SUCCESS :Application successfully gets and sets the zoom settings for the video device";
                            print "getdfc %s" %dfcdetails;
                            #comparing the DFC (zoomSettings) before and after setting
                            if setdfc in dfcdetails:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "SUCCESS: Both the zoomsettings values are equal";
                            else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print "FAILURE: Get and Set APi's are Success But the zoomsettings values are not equal";
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE :Failed to get and set the zoom settings";
                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                    if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE: Deinitalize failed" ;
            else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE: Device Setting Initialize failed";
            print "[TEST EXECUTION RESULT] : %s" %actualresult;
        else:
            print "Execution  failure"
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
        tdk_obj.unloadModule("tdkintegration");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
        tdk_obj.setLoadModuleStatus("FAILURE");
