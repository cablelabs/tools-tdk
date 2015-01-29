'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1595</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_PowerModeToggle_Stress_119</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>82</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetPowerMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check multiple (50 times) toggles between STB Standby and Power-on.
TestcaseID: CT_DS119</synopsis>
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
obj.configureTestCase(ip,port,'DS_PowerModeToggle_Stress_119');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
    #Set the module loading status
    obj.setLoadModuleStatus("SUCCESS");
    # Repeat PowerMode change for 50 times
    for x in range(0,50):
        # Toggle between state values ON (1) / STANDBY (2)
        for powermode in range(1,3):
            #calling Device Settings - initialize API
            tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
            expectedresult="SUCCESS"
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            print "[DS Initialize RESULT] : %s" %actualresult;
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling DS_SetPowerMode to set the power mode of STB
                tdkTestObj = obj.createTestStep('DS_SetPowerMode');
                print "Setting Power mode to %d" %powermode;
                tdkTestObj.addParameter("new_power_state",powermode);
                expectedresult="SUCCESS";
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS SetPowerMode RESULT] : %s" %actualresult;
                powerdetails = tdkTestObj.getResultDetails();
                print "PowerMode Details: %s"%powerdetails;
                #Check for SUCCESS/FAILURE return value of DS_SetPowerMode
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
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
        #End of for loop for power mode toggle
    #End of for loop for 50 times

    #Unload the deviceSettings module
    obj.unloadModule("devicesettings");
else:
    print"Load module failed";
    #Set the module loading status
    obj.setLoadModuleStatus("FAILURE");
