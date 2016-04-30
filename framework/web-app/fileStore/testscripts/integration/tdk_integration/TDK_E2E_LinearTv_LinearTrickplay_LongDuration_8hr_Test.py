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
  <id>1647</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TDK_E2E_LinearTv_LinearTrickplay_LongDuration_8hr_Test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>577</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMF_TSB_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Trickplay stress test to check tsb live trickplay with 4x 15x, 30x and 60x speeds.
TestCase ID: E2E_RMF_TSB_56</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>600</execution_time>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
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
import tdkintegration;
import time;
import timeit;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

testTimeInHours = 8

obj.configureTestCase(ip,port,'TDK_E2E_LinearTv_LinearTrickplay_LongDuration');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "tdkintegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "tdkintegration module loaded successfully";
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url = tdkintegration.E2E_getStreamingURL(obj, "TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
        print "Request URL : %s" %url;
        tdkTestObj.addParameter("Validurl",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        print "Result of Json Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                print "Json Response Parameter is success";   
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                #Remove unwanted part from URL
                PLAYURL = details;
				
                testTime = testTimeInHours * 60 * 60
                timer = 0
                iteration = 0

                while (timer < testTime):

                    startTime = 0
                    startTime = timeit.default_timer()
                    iteration = iteration + 1
                    print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)
	
                    #Primitive test case which associated to this Script
                    tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
                    if iteration % 4 == 0:
                        rate = 4.0; 
                    elif  iteration % 4 == 1:
                        rate = 15.0; 
                    elif  iteration % 4 == 2:
                        rate = 30.0; 
                    elif  iteration % 4 == 3:
                        rate = 60.0; 

                    print "Speed rate value set : %f" %rate;
                    tdkTestObj.addParameter("SpeedRate",rate);
                    tdkTestObj.addParameter("VideostreamURL",PLAYURL);
                    #Execute the test case in STB and pass the expected result
                    expectedresult="SUCCESS";
                    tdkTestObj.executeTestCase(expectedresult);
                    #Get the actual result of execution
                    actualresult = tdkTestObj.getResult();
                    print "Result of TSB Play : %s" %actualresult;
                    #compare the actual result with expected result of Json response Parameter
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        details = tdkTestObj.getResultDetails();
                        print "E2E RMF TSB Playback Successful: [%s]"%details;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details =  tdkTestObj.getResultDetails();
                        print "E2E RMF TSB Playback Failed: [%s]"%details;
                        break;

                    						
                    stopTime = timeit.default_timer()
                    timer = timer + (stopTime - startTime)
					
                    print "Total Time in Seconds = %f" %(timer)		
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "Json Response Parameter is Failure";


        obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
