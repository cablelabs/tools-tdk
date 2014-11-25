'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1597</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_Tune_InvalidChannel</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>LinearTV-To check tuning from  HD channel to invalid channel map  eg:Ch_no not available in the channel list. E2E_LinearTV_08</synopsis>
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
    <box_type>IPClient-3</box_type>
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
import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

def getURL_PlayURL(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');

    if streamId == "00":
        expectedresult="FAILURE";
        streamDetails = tdkTestObj.getStreamDetails('01');
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://0X00"
    else:
        expectedresult="SUCCESS";
        streamDetails = tdkTestObj.getStreamDetails(streamId);
        url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://"+streamDetails.getOCAPID()  

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);        

    #Execute the test case in STB    
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
            retValue = "SUCCESS";
            
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details =  tdkTestObj.getResultDetails();            
            print "Execution Failed: [%s]"%(details);
            retValue = "FAILURE";
            
    else:
        tdkTestObj.setResultStatus("SUCCESS");
        print "Json Response Parameter is Failure";
        retValue = "FAILURE";
    
    return retValue
    
                                        
obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_Tune_InvalidChannel');

#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "TDKIntegration module loading status : %s" %result;

if "SUCCESS" in result.upper():
    
    obj.setLoadModuleStatus("SUCCESS");
    print "TDKIntegration module load successful";
    
    #Calling getURL_PlayURL with valid Stream ID
    result1 = getURL_PlayURL(obj,'01');

    #Calling getURL_PlayURL with the invalid Stream ID
    result2 = getURL_PlayURL(obj,'00');
        
    if ("SUCCESS" in result1.upper()) and ("FAILURE" in result2.upper()):                                        
        print "Execution Success";
    else:            
        print "Execution failure";
                              
         
    obj.unloadModule("tdkintegration");
    
else:
         print "Failed to load tdkintegration module";
         obj.setLoadModuleStatus("FAILURE");