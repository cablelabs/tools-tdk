'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1598</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_ResolutionChange_VideoPlay_122</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>83</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_ResolutionChange_VideoPlay_122');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                    tdkTestObj.setResultStatus("SUCCESS");
                    #calling Device Setting -Set Resolution
                    tdkTestObj = obj.createTestStep('DS_SetResolution');
                    #Setting Resolution value
                    resolution="720p";
                    print "Setting resolution to %s" %resolution;
                    tdkTestObj.addParameter("resolution",resolution);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    tdkTestObj.addParameter("get_only",0);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[DS SetResolution RESULT] : %s" %actualresult;
                    getResolution = tdkTestObj.getResultDetails();
                    print "getResolution:%s" %getResolution;
                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                    if expectedresult in actualresult:
                        #comparing the resolution before and after setting
                        if resolution in getResolution :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Get resolution same as Set resolution value";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Get resolution not same as Set resolution value";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[DS Deinitalize RESULT] : %s" %actualresult;
                    #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Connection Status";
        else:
                tdkTestObj.setResultStatus("FAILURE");

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");

# live trickplay after resolution change
obj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
obj.configureTestCase(ip,port,'DS_ResolutionChange_VideoPlay_122');
#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "TDKIntegration module loading status :  %s" %loadmodulestatus;
#Check for SUCCESS/FAILURE of LinearTV module
if "SUCCESS" in loadmodulestatus.upper():
        obj.setLoadModuleStatus("SUCCESS");
        print "TDKIntegration module loaded successfully";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        #Framing URL for Request
        url='http://' + streamDetails.getGatewayIp() + ':8080/vldms/tuner?ocap_locator=ocap://'+streamDetails.getOCAPID();
        print "Request URL : %s" %url;
        tdkTestObj.addParameter("playUrl",url);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        print "TEST EXECUTION RESULT : %s" %actualresult;
        details = tdkTestObj.getResultDetails();
        print "TEST EXECUTION DETAILS : %s" %details;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");
        obj.unloadModule("tdkintegration");
else:
        print "Failed to load TDKIntegration module";
        obj.setLoadModuleStatus("FAILURE");
