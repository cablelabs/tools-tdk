#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>22</version>
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
  <execution_time>15</execution_time>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
tdkIntObj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
print "[TDKINTEGRATION LIB LOAD STATUS]  :  %s" %tdkIntLoadStatus ;

if "SUCCESS" in tdkIntLoadStatus.upper():
    #Set the module loading status
    tdkIntObj.setLoadModuleStatus("SUCCESS");
    tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    global matchList 
    matchList = tdkTestObj.getRecordingDetails(duration);
    tdkIntObj.resetConnectionAfterReboot()
    tdkTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    #set the dvr play url 
    if matchList:
       print "Recording Details : " , matchList
       #fetch recording id from list matchList.
       recordID = matchList[1]
       recordID = recordID.strip()
                    
       #Calling DvrPlay_rec to play the recorded content
       result = dvr_playback(tdkTestObj,recordID );
       if "SUCCESS" in result.upper():
       
	 #devicesettings component to be tested
	 dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
	 dsObj.configureTestCase(ip,port,'E2E_RMF_DVRPlayback_Change_Zoom');
	 dsLoadStatus = dsObj.getLoadModuleResult();
	 print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
	 if "SUCCESS" in dsLoadStatus.upper():
            dsObj.setLoadModuleStatus("SUCCESS");
            #calling Device Settings - initialize API
            tdkTestObj = dsObj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "SUCCESS :Application successfully initialized with Device Settings library";
                    #calling DS_SetDFC to get and set the zoom settings 
                    tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                    #zoom="Full";
                    zoom="Full";
                    print "Zoom value set to : %s" %zoom;
                    tdkTestObj.addParameter("zoom_setting",zoom);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    dfcdetails = tdkTestObj.getResultDetails();
		    print dfcdetails
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                            print "SUCCESS :Application successfully gets and sets the zoom settings for the video device";
                            tdkTestObj.setResultStatus("SUCCESS");
                    else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print "FAILURE :Failed to get and set the zoom settings";

		    #Calling DvrPlay_rec to play the recorded content with full zoom
    		    tdkIntTestObj = tdkIntObj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
                    result = dvr_playback(tdkIntTestObj,recordID );

                    print "Revert zoom to None"
                    zoom="None";
                    #calling DS_SetDFC to get and set the zoom settings
                    tdkTestObj = dsObj.createTestStep('DS_SetDFC');
                    print "Zoom value set to %s" %zoom;
                    tdkTestObj.addParameter("zoom_setting",zoom);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    dfcdetails = tdkTestObj.getResultDetails();
                    print "Details: ",dfcdetails
                    #Check for SUCCESS/FAILURE return value of DS_SetDFC
                    if expectedresult in actualresult:
                         tdkTestObj.setResultStatus("SUCCESS");
                    else:
                         tdkTestObj.setResultStatus("FAILURE");

                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = dsObj.createTestStep('DS_ManagerDeInitialize');
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
	    #Unload the deviceSettings module
	    dsObj.unloadModule("devicesettings");
         else:
            #Set the module loading status
            dsObj.setLoadModuleStatus("FAILURE");
       else:
            print "Failed to play the recorded content"
    tdkIntObj.unloadModule("tdkintegration");
else:
    print"Load module failed";
    #Set the module loading status
    tdkIntObj.setLoadModuleStatus("FAILURE");
