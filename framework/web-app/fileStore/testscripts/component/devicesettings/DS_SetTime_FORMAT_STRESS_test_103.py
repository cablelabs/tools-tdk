'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>647</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetTime_FORMAT_STRESS_test_103</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>87</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetTimeFormat</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully change Time format of the front panel indicator continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_103</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
obj.configureTestCase(ip,port,'CT_DS_103');
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
                i = 0;
                for i in range(0,100):
                        print "****************%d" %i;
                        tdkTestObj = obj.createTestStep('DS_SetTimeFormat');
                        #setting time format
                        timeformat = 0;
                        print "Time format set to %d" %timeformat;  
                        tdkTestObj.addParameter("text","Text");
                        tdkTestObj.addParameter("time_format",timeformat);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        time_format="%s" %timeformat;
                        actualresult = tdkTestObj.getResult();
                        textdetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetTimeFormat
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the timeformat";
                                print "getTimeFormat %s" %textdetails;
                                #comparing the time format before and after setting
                                if time_format in textdetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the time formats are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the time formats are not same";
                        else:
                                print "FAILURE :Failed to get and set the timeformat";
                                print "****************%d" %i;
                        time.sleep(100/1000);
                        tdkTestObj = obj.createTestStep('DS_SetTimeFormat');
                        #setting time format
                        timeformat = 1;
                        print "Time format set to %d" %timeformat;
                        tdkTestObj.addParameter("text","Text");
                        tdkTestObj.addParameter("time_format",timeformat);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        time_format="%s" %timeformat;
                        actualresult = tdkTestObj.getResult();
                        textdetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetTimeFormat
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully gets and sets the timeformat";
                                print "getTimeFormat %s" %textdetails;
                                #comparing the time format before and after setting
                                if time_format in textdetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the time formats are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the time formats are not same";
                        else:
                                print "FAILURE :Failed to get and set the timeformat";
                                print "****************%d" %i;
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
        #Set the module loading status
        print"Load module failed";
