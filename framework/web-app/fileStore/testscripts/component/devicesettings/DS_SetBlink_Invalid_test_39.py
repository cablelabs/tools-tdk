'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>597</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetBlink_Invalid_test_39</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>75</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetBlink</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the iinvalid value for blink feature of given Front panel Indicator
Test Case ID : CT_DS_39</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <rdk_version>RDK1.3</rdk_version>
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
obj.configureTestCase(ip,port,'CT_DS_39');
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
                #calling Device Settings - setBlink and getBlink APIs with invalid value
                tdkTestObj = obj.createTestStep('DS_SetBlink');
                # setting scroll class parameters values
                blink_interval = -1;
                print "Blink interval value set to:%d" %blink_interval; 
                blink_iteration = -2;
                print "Blink iteration value set to:%d" %blink_iteration;
                tdkTestObj.addParameter("blink_interval",blink_interval);
                tdkTestObj.addParameter("blink_iteration",blink_iteration);
                expectedresult="FAILURE"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                blinkdetails = tdkTestObj.getResultDetails();
                blinkinterval="%s" %blink_interval;
                blinkiteration="%s" %blink_iteration;
                #Check for SUCCESS/FAILURE return value of DS_SetBlink
                print blinkdetails;
                if expectedresult in actualresult:
                        print "SUCCESS :Failed to get and set the blink rate";
                        
                        #comparing the blink paramaters before and after setting
                        if ((blinkinterval in blinkdetails)and(blinkiteration in blinkdetails)):
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the blink rates are same";                                
                        else:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the blink rates are not same";                                
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "getblink %s" %blinkdetails;
                        print "Failure: Application successfully gets and sets blink rate for LED";
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