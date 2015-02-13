# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkintegration;
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_RMF_DVR_TrickPlay_09');
expected_Result="SUCCESS"

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module load successful";

#Acquiring the instance of TDKScriptingLibrary for checking and verifying the DVR content.
if "SUCCESS" in result.upper():
         obj.setLoadModuleStatus("SUCCESS");
         print "TDKIntegration module load successful";
	 #primitive test case which associated to this script 
         tdkTestObj=obj.CreateTestSetup("TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR")
         #Pre-requisite to Check and verify required recording is present or not.
         #---------Start-----------------
 	 duration=4
         matchList =[]
	 matchList=tdkTestObj.getRecordingDetails(duration);
	 obj.resetConnectionAfterReboot()

         tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Play_TrickPlay_FF_FR');
        #--------End-----------------------

         #fetch Streaming details
         streamDetails = tdkTestObj.getStreamDetails("01");
         time.sleep(50)
         if matchList:
         
                   print "Recording details: ",matchList
                   #fetch recording id from list matchList.
      		   recordID = matchList[1]
         url = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1] );
         if url == "NULL":
             print "Failed to generate the Streaming URL";
             tdkTestObj.setResultStatus("FAILURE");

		   print "The Play DVR Url Requested: %s"%url
		   tdkTestObj.addParameter("playUrl",url);


		   #Execute the test case in STB
      		   expectedresult="SUCCESS";
                   tdkTestObj.executeTestCase(expectedresult);

                   #Get the result of execution
                   actualresult = tdkTestObj.getResult();
                   details =  tdkTestObj.getResultDetails();

                   print "The E2E DVR playback when fast forward is done at 32x speed from the middle of the video: %s" %actualresult;

                   #compare the actual result with expected result
                   if expectedresult in actualresult:
                   #Set the result status of execution
                   	tdkTestObj.setResultStatus("SUCCESS");
                  	print "E2E DVR Playback 32x speed Successful: [%s]"%details;
         	   else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "E2E DVR Playback 32x speed Failed: [%s]"%details;
	else:
                   print "no Matching recordings are found"
                   time.sleep(10);
                   obj.unloadModule("tdkintegration");
else:
         print "Failed to load TDKIntegration module";
         obj.setLoadModuleStatus("FAILURE");
