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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Recorder_RMF_LPServerOutage_CheckConnectionRetrial_61</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check that after Longpoll server outage recorder attempts no more than 1 concurrent connection with randomized  exponentially-longer retry intervals each time, to avoid overwhelming the server after a systemwide outage</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
#use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import recorderlib
from time import sleep


#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_LPServerOutage_CheckConnectionRetrial_61');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        #Set the module loading status
        recObj.setLoadModuleStatus(recLoadStatus);
	
	print "Rebooting box for setting configuration"
	loadmoduledetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in loadmoduledetails:
               recObj.initiateReboot();
	       sleep(300);

        print "Waiting for the recoder to be up"


        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-requisite
        recorderlib.callServerHandlerWithType('clearDisabledStatus','LPServer',ip)
        recorderlib.callServerHandler('clearStatus',ip)

        #Disable LPServer
        recorderlib.callServerHandlerWithType('disableServer','LPServer',ip)
        status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
        print "Longpoll server status: ",status
        if "FALSE" in status.upper():
		print "Waiting to get connection retrial attempts from recorder"
		#sleep(550)
		sleep(300)
		#Checkpoint-1: Get the time between each re-trials
		print "Checking status of disabled servers"
                lpstatus = recorderlib.callServerHandlerWithType('retrieveDisabledStatus','LPServer',ip)
		print "LPServer Status: ",lpstatus
        	#Check if status is not empty
        	if ( '[]' in lpstatus ):
                	print "ERROR: No status available for LPServer"
			tdkTestObj.setResultStatus("FAILURE")
		else:
			MINDELAY = 40
			RETRYCOUNT = 3
			intervalPrev = 0
			ret = recorderlib.getTimeListFromStatus(lpstatus)
			print "LP server timelist = ",ret
			for x in range(RETRYCOUNT):
				intervalCurr = int( (ret[x+1] - ret[x])/1000 )
				print "Retry interval for LPServer: ",intervalCurr,"sec"
				if intervalCurr < MINDELAY:
					print "Retry interval for LPServer less than ",intervalCurr,"secs"
					tdkTestObj.setResultStatus("FAILURE")
				if intervalCurr <= intervalPrev:
					print "Retry interval for LPServer not incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
					tdkTestObj.setResultStatus("FAILURE")
				else:
					print "Retry interval for LPServer incrementing from ",intervalPrev,"sec to ",intervalCurr,"sec"
				intervalPrev = intervalCurr

                #Checkpoint-2: Check no status from LPServer
                response = recorderlib.callServerHandler('retrieveStatus',ip);
		print "response = ",response
		if 'LPServer' in response:
			print "Recorder communicated with LPServer in disabled state"
			tdkTestObj.setResultStatus("FAILURE")
		else:
			print "Recorder did not communicate with LPServer in disabled state as expected"

                #post-req: Enable LPServer
                recorderlib.callServerHandlerWithType('enableServer','LPServer',ip)
                status = recorderlib.callServerHandlerWithType('isEnabledServer','LPServer',ip)
                print "Longpoll server status: ",status
                if "FALSE" in status.upper():
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failed to enable LP Server"
                else:
                        tdkTestObj.setResultStatus("SUCCESS");
			print "Enabled LP Server"
	else:
		print "Failed to disable LP Server. Exiting.."
		tdkTestObj.setResultStatus("FAILURE");

        #unloading Recorder module
        recObj.unloadModule("Recorder");
