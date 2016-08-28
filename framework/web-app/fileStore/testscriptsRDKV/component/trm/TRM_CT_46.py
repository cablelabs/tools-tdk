#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2014 Comcast. All rights reserved.
#  ===========================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_46</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>598</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForLive</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Automation of RDK-16023 to verify that repeated reserve tuner requests either all succeed or all fail with "InvalidState" reserveTunerResponse when requested with same token and device ID. Testcase ID: CT_TRM_46</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
from trm import reserveForLive
from time import sleep

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_46');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;

if "FAILURE" in result.upper():
    #Reboot and reload trm component
    print "Reboot and reload TRM"
    obj.initiateReboot();
    obj = tdklib.TDKScriptingLibrary("trm","2.0");
    obj.configureTestCase(ip,port,'TRM_CT_46');
    #Get the result of connection with test component and STB
    result = obj.getLoadModuleResult();
    print "[TRM LIB RELOAD STATUS]  :  %s" %result;

#Set the module loading status
obj.setLoadModuleStatus(result.upper());

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    duration = 900000
    startTime = 0
    streamId = '01'
    deviceNo = 0
    maxCount = 9

    token = reserveForLive(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':1200000,'startTime':startTime})

    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');
    locator = "ocap://"+tdkTestObj.getStreamDetails(streamId).getOCAPID()

    for loop in range(1,51):

        print "------ Test loop %d start ------ \n"%loop

        #Use same token to reserve tuner multiple times and expect all reservations to fail with InvalidState or InvalidToken Error OR all should be success
        successCount = 0
        for testCount in range(1,maxCount+1):

            print "DeviceNo:%d Locator:%s duration:%d startTime:%d token:%s"%(deviceNo,locator,duration,startTime,token)

            tdkTestObj.addParameter("deviceNo",deviceNo);
            tdkTestObj.addParameter("duration",duration);
            tdkTestObj.addParameter("locator",locator);
            tdkTestObj.addParameter("startTime", startTime);
            tdkTestObj.addParameter("token", token);

            expectedRes = "FAILURE"

            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedRes);

            #Get the result of execution
            result = tdkTestObj.getResult();
            print "Result: [%s]"%result
            details = tdkTestObj.getResultDetails();
            print "Details: [%s]"%details;

            if "SUCCESS" in result.upper():
                successCount += 1

            #Set the result status of execution
            if "FAILURE" in result.upper():
                if "InvalidState" in details:
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Reservation did not fail with InvalidState response code"
            else:
                if testCount == maxCount and successCount != maxCount:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "All reservations did not succeed"
                else:
                    tdkTestObj.setResultStatus("SUCCESS");
            print "\n"
        # End inner for loop

        print "------ Test loop %d end ------ \n"%loop
    # End outer for loop

    #Add sleep to release all reservations
    sleep(120)

    #unloading trm module
    obj.unloadModule("trm");
