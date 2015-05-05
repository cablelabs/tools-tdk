'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1655</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Continuous channel change for long duration (8hr). 
Test case ID - E2E_LinearTV_40</synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;
import timeit;
import os;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

testTimeInHours = 8
configFile = "TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test.config"

def getURL_PlayURL(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");

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
        
        #Prmitive test case which associated to this Script
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
                                        
obj.configureTestCase(ip,port,'TDK_E2E_LinearTV_Channelchange_LongDuration_8hr_test');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";

    # Fetching list of actions to be performed from configuration file
    itemList = obj.readConfigFile(configFile)
	
    testTime = testTimeInHours * 60 * 60
    timer = 0
    iteration = 0

    while (timer < testTime):

        startTime = 0
        startTime = timeit.default_timer()
        iteration = iteration + 1
        print "\n\n----------------------------  Iteration : %d  ----------------------------\n" %(iteration)

        # Parsing through list and executing each step
        for step in range(0,len(itemList)):

            if "START" in itemList[step]:
                print "Starting Execution"

            elif "END" in itemList[step]:
                print "End of Execution"

            elif "CHANNEL_ID" in itemList[step]:
                channelID = itemList[step].split(":")[-1]
                print "Tuning to channel with stream ID : " , channelID

                #Calling the getURL_PlayURL function for the requested StreamID
                result = getURL_PlayURL(obj,channelID);
                if ("SUCCESS" in result.upper()):
                    print "Execution Success at iteration";
                else:
                    print "Execution failure at iteration";

            elif "DELAY" in itemList[step]:
                delayTime = itemList[step].split(":")[-1]
                print "Delay for " + delayTime + " seconds"
                time.sleep(int(delayTime))
				
        stopTime = timeit.default_timer()
        timer = timer + (stopTime - startTime)
					
    print "Total Time in Seconds = %f" %(timer)		
    obj.unloadModule("tdkintegration");
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
