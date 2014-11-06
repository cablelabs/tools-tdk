'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>594</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetblueColor_POWER_LED_31</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>77</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_setColor</primitive_test_name>
  <!--  -->
  <primitive_test_version>6</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the Blue Color for the Power Front panel Indicator
Test Case ID : CT_DS_31</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This test is skipped as the GetColor API has been modified (DELIA-4408 )</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
obj.configureTestCase(ip,port,'CT_DS_31');
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
                tdkTestObj = obj.createTestStep('DS_GetSupportedColors');
                tdkTestObj.addParameter("indicator_name","Power");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedColors
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported colors";
                        print "%s" %colordetails
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the color list";
                print "SUCCESS :Application successfully initialized with Device Settings library";
                print "0-Blue";
                print "1-Green";
                print "2-Red";
                print "3-Yellow";
                print "4-Orange";
                tdkTestObj = obj.createTestStep('DS_SetColor');
                #setting color parameter value
                color = 0;
                print "Color value set to:%d" %color;
                indicator = "Power";
                print "Indicator value set to:%s" %indicator;          
                tdkTestObj.addParameter("color",color);
                tdkTestObj.addParameter("indicator_name",indicator);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                colordetails = tdkTestObj.getResultDetails();
                setColor = "%s" %color;
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets and sets the color for POWER LED";
                        print "getColor %s" %colordetails;
                        #comparing the color before and after setting
                        if setColor in colordetails :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the colors are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the colors are not same";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Failure: Failed to get and set color for POWER LED";
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