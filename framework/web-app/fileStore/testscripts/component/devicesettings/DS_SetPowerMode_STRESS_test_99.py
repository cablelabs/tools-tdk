'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>643</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetPowerMode_STRESS_test_99</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>82</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetPowerMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully set and get the power mode as ON and OFF continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_99</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test is skipped as the Set Power Mode API is invalid in future releases	(DELIA-4974)</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_99');
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
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                i=0;
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling DS_SetPowerMode to set the power mode of STB
                        tdkTestObj = obj.createTestStep('DS_SetPowerMode');
                        powermode=1;
                        print "Power mode value set to:%d" %powermode;
                        tdkTestObj.addParameter("new_power_state",powermode);
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        powerdetails = tdkTestObj.getResultDetails();
                        setpower = "%d" %powermode;
                        #Check for SUCCESS/FAILURE return value of DS_SetPowerMode
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS :Application successfully changed the state of STB";
                                print "setpower: %s"%powerdetails;
                        else:
                                 tdkTestObj.setResultStatus("FAILURE");
                                 print "****************%d" %i;
                        time.sleep(100/1000);
                        #calling DS_SetPowerMode to set the power mode of STB
                        tdkTestObj = obj.createTestStep('DS_SetPowerMode');
                        powermode = 0;
                        print "Power mode value set to:%d" %powermode;
                        tdkTestObj.addParameter("new_power_state",powermode);
                        expectedresult="SUCCESS";
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        powerdetails = tdkTestObj.getResultDetails();
                        setpower = "%d" %powermode;
                        #Check for SUCCESS/FAILURE return value of DS_SetPowerMode
                        if expectedresult in actualresult:
                                 tdkTestObj.setResultStatus("SUCCESS");
                                 print "SUCCESS :Application successfully changed the state of STB";
                                 print "setpower: %s"%powerdetails;

                        else:
                                 tdkTestObj.setResultStatus("FAILURE");
                                 print "****************%d" %i;
                                 print "FAILURE :Application failed to change the power mode";
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
