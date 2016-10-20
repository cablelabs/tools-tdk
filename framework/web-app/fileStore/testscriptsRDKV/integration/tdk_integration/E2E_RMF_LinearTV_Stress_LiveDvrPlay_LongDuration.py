##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1579</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Continuous switching of between live play and dvr playback for long duration(10hrs) - E2E_LinearTV_46</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>630</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def PlayURL(obj,ValidURL):    
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

    print "Play Url Requested: %s"%(ValidURL);
    tdkTestObj.addParameter("playUrl",ValidURL);

    expectedresult = "SUCCESS";
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
        retValue = "FAILURE"
    
    return retValue
                                        
obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;
loadmoduledetails = obj.getLoadModuleDetails();
#Reboot if rmfstreamer is not running
if "FAILURE" in result.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:

                print "rmfStreamer is not running. Rebooting STB"
                obj.initiateReboot();
                #Reload Test component to be tested
                obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Stress_LiveDvrPlay_LongDuration');
                #Get the result of connection with test component and STB
                result =obj.getLoadModuleResult();
                #print "Re-Load Module Details : %s" %loadmoduledetails1;
                print "Tdkintegration module loading status :  %s" %result;
if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
        
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails('01');
    
    #Framing URL for Live Play Request
    url1 = tdkintegration.E2E_getStreamingURL(obj, "LIVE" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
    if url1 == "NULL":
        print "Failed to generate the Streaming URL";
        tdkTestObj.setResultStatus("FAILURE");

    print "Request URL : %s" %url1;
    tdkTestObj.addParameter("Validurl",url1);

    expectedresult = "SUCCESS";

    #Execute the test case in STB 
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();

    #Remove unwanted part from URL
    PLAYURL = details.split("[RESULTDETAILS]");
    url1 = PLAYURL[-1];

    #Pre-requisite to Check and verify required recording is present or not.
    #---------Start-----------------

    duration = 4
    matchList = []
    matchList = tdkTestObj.getRecordingDetails(duration);
    obj.resetConnectionAfterReboot()
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    time.sleep(10)
		 
    if matchList:
		 
         print "Recording Details : " , matchList

         #fetch recording id from list matchList.
         recordID = matchList[1]
         #Framing URL for DVR Play Request
         url2 = tdkintegration.E2E_getStreamingURL(obj, "DVR" , streamDetails.getGatewayIp() , recordID[:-1]);
         if url2 == "NULL":
           print "Failed to generate the Streaming URL";
           tdkTestObj.setResultStatus("FAILURE");

    
         if expectedresult in actualresult:

            for i in range(1,600):        
                                        
                #Calling the PlayURL function to play the requested URL
                result1 = PlayURL(obj,url1);
          
                #Calling the PlayURL function to play the requested URL
                result2 = PlayURL(obj,url2);
        
                if ("SUCCESS" in result1.upper()) and ("SUCCESS" in result2.upper()):                                        
                    print "Execution Success at iteration %d"%i;
                else:            
                   print "Execution failure at iteration %d"%i;
                   break;
         else:
              tdkTestObj.setResultStatus("FAILURE");
              print "Json Response Parameter is Failure";
         
              obj.unloadModule("tdkintegration");
			  
    else:
         print "No Matching recordings list found"
					 
         time.sleep(10);
         obj.unloadModule("tdkintegration");
	
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");
