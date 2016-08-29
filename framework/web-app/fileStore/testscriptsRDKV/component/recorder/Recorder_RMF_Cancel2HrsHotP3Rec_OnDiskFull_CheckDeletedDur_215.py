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
  <name>Recorder_RMF_Cancel2HrsHotP3Rec_OnDiskFull_CheckDeletedDur_215</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Recorder_SendRequest</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Schedule a new hot P3 recording for 2 hrs and cancel after 5 mins of recordings. Check that an existing P3 recording of duration not more than 10 min duration is deleted and not big P3 recording</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>660</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
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
import recorderlib
from recorderlib import checkDiskFullWithRecordings
from time import sleep
from random import randint
from trm import getMaxTuner

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
trmObj.configureTestCase(ip,port,'Recorder_RMF_Cancel2HrsHotP3Rec_OnDiskFull_CheckDeletedDur_215');
#Get the result of connection with test component and STB
trmLoadStatus = trmObj.getLoadModuleResult();
print "TRM module loading status  :  %s" %trmLoadStatus;
#Set the module loading status
trmObj.setLoadModuleStatus(trmLoadStatus);

NUMOFTUNERS = 5

if "FAILURE" in trmLoadStatus.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    trmObj.initiateReboot();
    trmObj = tdklib.TDKScriptingLibrary("trm","2.0");
    trmObj.configureTestCase(ip,port,'Recorder_RMF_Cancel2HrsHotP3Rec_OnDiskFull_CheckDeletedDur_215');
    #Get the result of connection with test component and STB
    trmLoadStatus = trmObj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %trmLoadStatus;
    sleep(300)

trmObj.setLoadModuleStatus(trmLoadStatus);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in trmLoadStatus.upper():
        #Fetch max tuner supported
        NUMOFTUNERS = getMaxTuner(trmObj,'SUCCESS')
        trmObj.unloadModule("trm")

if NUMOFTUNERS < 5:
        NUMOFTUNERS = 5

#Test component to be tested
recObj = tdklib.TDKScriptingLibrary("Recorder","2.0");
recObj.configureTestCase(ip,port,'Recorder_RMF_Cancel2HrsHotP3Rec_OnDiskFull_CheckDeletedDur_215');
#Get the result of connection with test component and STB
recLoadStatus = recObj.getLoadModuleResult();
print "Recorder module loading status : %s" %recLoadStatus;
#Set the module loading status
recObj.setLoadModuleStatus(recLoadStatus);

#Check for SUCCESS/FAILURE of Recorder module
if "SUCCESS" in recLoadStatus.upper():

        recLoadDetails = recObj.getLoadModuleDetails();
        if "REBOOT_REQUESTED" in recLoadDetails:
               print "Rebooting box for setting configuration"
               recObj.initiateReboot()
               print "Waiting for 5min for recoder to be up"
	       sleep(300)

        #Primitive test case which associated to this script
        tdkTestObj = recObj.createTestStep('Recorder_SendRequest');
        expectedResult="SUCCESS";
        tdkTestObj.executeTestCase(expectedResult);

        #Pre-Req start: Disk should be full before starting test
        print "Schedule 2hrs P3 recordings on all the tuners"
	for i in range(0,2):
        	diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,7200000,"P3")
		if 1 == diskFull:
			break
        print "Schedule 1hr P3 recordings on all the tuners"
	for i in range(0,2):
        	diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,3600000,"P3")
		if 1 == diskFull:
			break
        #Repeat for 10 times
        print "Schedule 30min P3 recordings on all the tuners"
        for i in range(0,10):
                diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,1800000,"P3")
                if 1 == diskFull:
                        break
        #Repeat for 4 times
        print "Schedule 10min P3 recordings on all the tuners"
        for i in range(0,4):
                diskFull = checkDiskFullWithRecordings(ip,tdkTestObj,NUMOFTUNERS,600000,"P3")
                if 1 == diskFull:
                        break
		else:
			sleep(120)

        #Check if disk is full now
        if 1 == diskFull:
                print "DISKFULL! Pre-requisite met"

		#Save the list of completed recodings before starting test
        	recorderlib.callServerHandler('clearStatus',ip)
        	recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        	#Wait to get response from recorder
        	sleep(120)
        	recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        	#Look for recordings field in response
        	recordings = recorderlib.getRecordings(recResponse)
        	if [] == recordings:
                	print "No recordings found in response: ",recResponse
        	else:
        		completeRecList = []
        		for item in recordings:
                        	if "Complete" == item['status']:
					completeRecList.append(item)
			if [] == completeRecList:
				print "Disk does not contain any completed recording! Pre-requisite not met"
				tdkTestObj.setResultStatus("FAILURE");
				#unloading Recorder module
				recObj.unloadModule("Recorder")
				exit()
        else:
                print "DISK NOT FULL! Pre-requisite not met"
                tdkTestObj.setResultStatus("FAILURE");
                #unloading Recorder module
                recObj.unloadModule("Recorder");
                exit()
        #Pre-Req end: Disk should be full before starting test

        #STEP1: Start hot P3 recording for 2hr
        requestID = str(randint(10, 500))
        recordingID = str(randint(10000, 500000))
        startTime = "0"
        duration = "7200000"
        ocapId = tdkTestObj.getStreamDetails('07').getOCAPID()
        now = "curTime"
        priority = "P3"

        #Frame json message to schedule recording
        jsonMsg = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"fullSchedule\":false,\"dvrProtocolVersion\":\"7\",\"schedule\":[{\"recordingId\":\""+recordingID+"\",\"locator\":[\"ocap://"+ocapId+"\"],\"epoch\":"+now+",\"start\":"+startTime+",\"duration\":"+duration+",\"properties\":{\"requestedStart\":0,\"title\":\"RecordingTitle_"+recordingID+"\"},\"bitRate\":\"HIGH_BIT_RATE\",\"deletePriority\":\""+priority+"\"}]}}"
        #Send update msg to simulator server
        recorderlib.callServerHandler('clearStatus',ip)
        recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsg,ip)
        #Wait to send next request
        sleep(30)
	recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
	print "Recorder Response ",recResponse

	#STEP2: Wait for 5 min and cancel the recording
	sleep(300)
	jsonMsgCancelRecording = "{\"updateSchedule\":{\"requestId\":\""+requestID+"\",\"cancelRecordings\":[\""+recordingID+"\"]}}"
	recorderlib.callServerHandlerWithMsg('updateMessage',jsonMsgCancelRecording,ip)

	#STEP3: Check that an existing P3 recording of duration not more than 10 min duration is deleted
        #Get recordings list and check for error code of recordings
        recorderlib.callServerHandler('clearStatus',ip)
        recorderlib.callServerHandlerWithMsg('updateInlineMessage','{\"getRecordings\":{}}',ip)
        #Wait to get response from recorder
        sleep(120)
        recResponse = recorderlib.callServerHandler('retrieveStatus',ip)
        #Look for recordings field in response
        recordings = recorderlib.getRecordings(recResponse)
        if [] == recordings:
                print "No recordings found in response: ",recResponse
		tdkTestObj.setResultStatus("FAILURE")
        else:
		#Get new list of recordings in completed state
		completeRecListNew = []
		for item in recordings:
			if "Complete" == item['status']:
				completeRecListNew.append(item)
		
		delRec = 0
		#Check if any of previously completed is missing now
		for rec in completeRecList:
        		if rec not in completeRecListNew:
				delRec = 1
				duration = recorderlib.getValueFromKeyInRecording(rec,'duration')
				print "Recording deleted ",rec['recordingId'],"duration ",duration
				#Check if the deleted recording is more than 10 min long
				if duration > 600000:
					print "Deleted big recording"
					tdkTestObj.setResultStatus("FAILURE")
				else:
					print "Deleted small recording"
					tdkTestObj.setResultStatus("SUCCESS")
		if 0 == delRec:
			print "No recording deleted"
			tdkTestObj.setResultStatus("SUCCESS")
        #Testcase end

        #unloading Recorder module
        recObj.unloadModule("Recorder")
