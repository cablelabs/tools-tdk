'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1148</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_LinearTV_Live_Trickplay_FFW_15x_11</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>575</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_T2p_Tuning</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script tests the playback of Fast forward with play speed 15x in LinearTV trickplay scenario Test Case ID : E2E_LinearTV_11</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","1.3");
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_LinearTV_Live_Trickplay11');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "TDKintegration module loading status :  %s" %loadmodulestatus;

#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        print "TDKintegration module loaded successfully.";
        obj.setLoadModuleStatus("SUCCESS");
        #Calling LinearTV_URL function to send the url
        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_Tuning');

        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');

        ocapId = "ocap://"+streamDetails.getOCAPID();
        print "Request OCAP ID for tuning : %s" %ocapId;
        tdkTestObj.addParameter("ValidocapId",ocapId);

        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);

        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        #print "Tuned result log-path = %s" %tdkTestObj.getValue("log-path");
        print "Result of Json Response for Tuning : %s" %actualresult;

        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "Json Response tuning is success";

                #Sleep for 2 second before pausing. After tuning to different frequency.
                time.sleep(2);
                #Calling LinearTV_T2p_TrickMode Function for pausing the stream.
                tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_TrickMode');
                pauserate = 0.0;
                tdkTestObj.addParameter("trickPlayRate",pauserate);
                tdkTestObj.addParameter("VideostreamURL",details);
                 #Execute the test case in STB and pass the expected result
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);

                #Get the actual result of execution
                actualresult = tdkTestObj.getResult();
                print "Result of T2p Trick Mode Pause: %s" %actualresult;

                #compare the actual result with expected result from the T2p trick mode response.
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "Paused Successfully ";

                        #Sleep for 15 seconds for recording the content into TSB.
                        print "Paused for 15 seconds.. Please wait"
                        time.sleep(15);

                        #Calling LinearTV_T2p_TrickMode Function by passing the play back rate.
                        tdkTestObj = obj.createTestStep('TDKE2E_LinearTV_T2p_TrickMode');
                        rate = 15.0;
                        tdkTestObj.addParameter("trickPlayRate",rate);
                        tdkTestObj.addParameter("VideostreamURL",details);
                        #Execute the test case in STB and pass the expected result
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);

                        #Get the actual result of execution
                        actualresult = tdkTestObj.getResult();
                        print "Result of T2p Trick Mode: %s" %actualresult;
                        #print "TricK Mode result log-path = %s" %tdkTestObj.getValue("log-path");

                        #compare the actual result with expected result from the T2p trick mode response.
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Fast forward with 15.0x is played successfully ";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to play fast forwad with 15.0x";
                else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print "Json response Failed to Pause";
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Json response Failed to tune";

        #Unloading Tdkintegration module
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load LinearTV module";
        obj.setLoadModuleStatus("FAILURE");