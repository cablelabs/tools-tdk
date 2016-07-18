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
  <id>1651</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration_8hr_test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>577</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMF_TSB_Play</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Channel Change and Linear Trickplay for long duration (8hr)
Test case ID - E2E_LinearTV_41</synopsis>
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
# use tdklib library,which provides a wrapper for tdk test case script
import tdklib;
import tdkintegration;
import time;
import timeit;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
#Long duration test time period
testTimeInHours = 8
#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def getURL_PlayURL(obj,streamId):
    
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");
	return "FAILURE";

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);        

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    
    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        details =  tdkTestObj.getResultDetails();
        
        #Remove unwanted part from URL
        PLAYURL = details.split("[RESULTDETAILS]");
        ValidURL = PLAYURL[-1];        

        expectedresult="SUCCESS";
        
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        print "Play Url Requested: %s"%(ValidURL);
        tdkTestObj.addParameter("playUrl",ValidURL);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();        
        print "The E2E LinearTv Play : %s" %actualresult;

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "E2E LinearTv Playback Successful: [%s]"%details;
            retValue = "SUCCESS"
            
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details =  tdkTestObj.getResultDetails();            
            print "Execution Failed: [%s]"%(details);
            retValue = "FAILURE";
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Json Response Parameter is Failure";
        retValue = "FAILURE";
    
    
    return retValue
                                        
obj.configureTestCase(ip,port,'TDK_E2E_RMF_LinearTV_ChannelChange_Trickplay_LongDuration');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";	
    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0
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
        while (timer < testTime):
            startTime = 0
            startTime = timeit.default_timer()
            iteration = iteration + 1
            print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)
	
            #Calling the getURL_PlayURL function for the requested StreamID
            result1 = getURL_PlayURL(obj,'01');
            if ("SUCCESS" in result1.upper()):                                        
                print "Execution Success at iteration %d"%iteration;
            else:            
                print "Execution failure at iteration %d"%iteration;
                break;  
            #Calling the getURL_PlayURL function for the requested StreamID
            result2 = getURL_PlayURL(obj,'02');
    
            if ("SUCCESS" in result2.upper()):                                        
                print "Execution Success at iteration %d"%iteration;
            else:            
                print "Execution failure at iteration %d"%iteration;
                break;                                        

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
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "Json Response Parameter is Failure";		
		
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
