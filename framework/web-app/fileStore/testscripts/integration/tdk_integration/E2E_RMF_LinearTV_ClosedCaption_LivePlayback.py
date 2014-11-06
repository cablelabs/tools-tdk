'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1582</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_LinearTV_ClosedCaption_LivePlayback</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>541</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_RMFLinearTV_GetURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Enable/Disable Closed Caption during live play. Enable/Disable Closed Caption during live play	
E2E_LinearTV_34.</synopsis>
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
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
tdk_obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
cc_obj = tdklib.TDKScriptingLibrary("cc","2.0");


def getURL_PlayURL(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for the corresponding channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://"+streamDetails.getOCAPID()

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
            print "E2E LinearTv_Dvr Playback Successful: [%s]"%details;
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
    

def Create_ExecuteTestcase(obj,primitivetest,expectedresult,verifyList, **kwargs):
    print kwargs
    details = "NULL";
 
    #calling primitive test case    
    tdkTestObj = obj.createTestStep(primitivetest);
    for name, value in kwargs.iteritems():
      
        print "Name: %s"%str(name);
        tdkTestObj.addParameter(str(name),value);                                   
       
    Expectedresult=expectedresult;
    tdkTestObj.executeTestCase(Expectedresult); 
    actualresult = tdkTestObj.getResult();
    print "Actual Result: %s"%actualresult;
    
    try: 
        details = tdkTestObj.getResultDetails();
        print "Details:%s"%details;
    except:                
        pass;
    
    #Check for SUCCESS/FAILURE return value 
    if Expectedresult in actualresult:
        count = 0;
        if verifyList:
            print "Verify List not empty"
            for name,value in verifyList.items():	
                print "Name:%s,Value:%s to be verified in the details"%(name,value);
                if value in details:
            	    print details;	    
                    print "SUCCESS : %s sucess"%primitivetest;
                    count+=1;
                    if count > 0:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:%s"%(primitivetest);
                else:                    
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Value not in details %s" %details;
        else:
            print "Verify list empty"
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");            
    
    return (actualresult,tdkTestObj,details);
    

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

tdk_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_ClosedCaption_LivePlayback');
cc_obj.configureTestCase(ip,port,'E2E_RMF_LinearTV_ClosedCaption_LivePlayback');

loadmodulestatus = tdk_obj.getLoadModuleResult();
loadmodulestatus1 = cc_obj.getLoadModuleResult();

print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus1 ;

if ("SUCCESS" in loadmodulestatus.upper()) and ("SUCCESS" in loadmodulestatus1.upper()):
    #Set the module loading status
    cc_obj.setLoadModuleStatus("SUCCESS");
    tdk_obj.setLoadModuleStatus("SUCCESS");        

    #calling getURL_PlayURL to get and play the URL
    result = getURL_PlayURL(tdk_obj,'01');                
    
    if "SUCCESS" in result:
        print "Result: %s" %result;
        
        actualresult,tdkTestObj_cc,details = Create_ExecuteTestcase(cc_obj,'CC_Initialization', 'SUCCESS',verifyList ={});        
        
        #Check for SUCCESS/FAILURE return value of CC_Initialization        
        if "SUCCESS" in actualresult:
            
            Status = 1; # Must be either 0 or 1, 0 - OFF and 1 - ON
            #calling closed caption API "CC_SetGet_Status" to set the closed caption status
            actualresult,tdkTestObj_cc,details = Create_ExecuteTestcase(cc_obj,'CC_SetGet_State', 'SUCCESS', verifyList={'status':str(Status)},status = Status);            
           
            Status = 0; # Must be either 0 or 1, 0 - OFF and 1 - ON
            #calling closed caption API "CC_SetGet_Status" to set the closed caption status            
            actualresult,tdkTestObj_cc,details = Create_ExecuteTestcase(cc_obj,'CC_SetGet_State', 'SUCCESS',verifyList={'status':str(Status)},status = Status);                   
			
        else:            
            print "FAILURE :CC_Initialization is not successful";
    else:
        print "FAILURE :getURL_PlayURL is not successful";       
                
    #Unload the modules
    cc_obj.unloadModule("cc");
    tdk_obj.unloadModule("tdkintegration");
else:
    print"Load module failed";
    #Set the module loading status
    cc_obj.setLoadModuleStatus("FAILURE");
    tdk_obj.setLoadModuleStatus("FAILURE");


