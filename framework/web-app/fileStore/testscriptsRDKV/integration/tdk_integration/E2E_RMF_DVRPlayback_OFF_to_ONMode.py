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
  <version>27</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_DVRPlayback_OFF_to_ONMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify DVR playback during and after STB in OFF mode</synopsis>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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

import time;
from iarmbus import change_powermode
from tdkintegration import dvr_playback

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
iarm_obj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');
iarm_obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
loadmodulestatus1 = iarm_obj.getLoadModuleResult();
print "Tdkintegration module loading status :  %s" %loadmodulestatus;
loadmoduledetails = tdk_obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in loadmodulestatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                tdk_obj.initiateReboot();
                iarm_obj.resetConnectionAfterReboot();
                #Reload Test component to be tested
                tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                tdk_obj.configureTestCase(ip,port,'E2E_RMF_LivePlayback_StandbyMode');
                #Get the result of connection with test component and STB
                loadmodulestatus =tdk_obj.getLoadModuleResult();
                loadmodulestatus1 = iarm_obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper() and ("SUCCESS" in loadmodulestatus1.upper()):
        obj.setLoadModuleStatus("SUCCESS");
        iarm_obj.setLoadModuleStatus("SUCCESS");
        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
            
        #Check for SUCCESS/FAILURE return value of IARMBUS_Init
        if ("SUCCESS" in actualresult):               
            print "SUCCESS :Application successfully initialized with IARMBUS library";
            #calling IARMBUS API "IARM_Bus_Connect"
            actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});    

            expectedresult="SUCCESS";
            #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
            if expectedresult in actualresult:                   
 
                print "SUCCESS: Querying STB power state -RPC method invoked successfully";
                #Setting Power mode to OFF
                result1 = change_powermode(iarm_obj,0);

                #Calling IARM_Bus_DisConnect API
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});

                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});

                if "SUCCESS" in result1.upper():
                  #tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_RewindFromEndPoint'); 
                  tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play'); 
                  #Pre-requisite to Check and verify required recording is present or not.
                  #---------Start-----------------

                  duration = 4
                  matchList = []
                  matchList = tdkTestObj.getRecordingDetails(duration);
                  obj.resetConnectionAfterReboot()
                  #tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_RewindFromEndPoint');
                  tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

                  if matchList:

                    print "Recording Details : " , matchList

                    #fetch recording id from list matchList.
                    recordID = matchList[1]
                    
                    #Calling DvrPlay_rec to play the recorded content
                    result2 = dvr_playback(tdkTestObj,recordID[:-1]);

                    iarm_obj.resetConnectionAfterReboot()
                    #calling IARMBUS API "IARM_Bus_Init"
                    actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});

                    #calling IARMBUS API "IARM_Bus_Connect"
                    actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});

                    #Setting Power mode to ON
                    result3 = change_powermode(iarm_obj,2);

                    #Calling IARM_Bus_DisConnect API
                    actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});

                    #calling IARMBUS API "IARM_Bus_Term"
                    actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});

                    if "SUCCESS" in result3.upper():
                            #Prmitive test case which associated to this Script
                            tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
                            recordID = matchList[1]
                            recordID = recordID.strip()
                            
                            #Calling DvrPlay_rec to play the recorded content
                            result4 = dvr_playback(tdkTestObj,recordID);
                else:
	          	print "No Matching recordings list found"

	                iarm_obj.resetConnectionAfterReboot()
        	        #calling IARMBUS API "IARM_Bus_Init"
                	actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Init', 'SUCCESS',verifyList ={});

                        #calling IARMBUS API "IARM_Bus_Connect"
                        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});

                        #Setting Power mode to ON
                        change_powermode(iarm_obj,2);

                        #Calling IARM_Bus_DisConnect API
                        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});

                        #calling IARMBUS API "IARM_Bus_Term"
                        actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});

            else:
                print "FAILURE: IARM_Bus_Connect failed. %s" %details;
                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,tdkTestObj_iarm,details = tdklib.Create_ExecuteTestcase(iarm_obj,'IARMBUS_Term', 'SUCCESS',verifyList ={});            
            
        else:
            print "FAILURE: IARM_Bus_Init failed. %s " %details;
        print "Tdkintegration module loaded successfully";
        obj.unloadModule("tdkintegration");
        iarm_obj.unloadModule("iarmbus");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
         iarm_obj.setLoadModuleStatus("FAILURE");
