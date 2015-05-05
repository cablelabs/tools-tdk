'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>IARMBUS_PowerModeToggle_Stress</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>8</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>IARMBUS_BusCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>8</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test multiple toggles between STB Standby and Power-on states.
Mapped from Testcase ID: CT_DS119 in devicesettings Testcase
Testcase ID: CT_IARMBUS_113</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This is skipped till RDKTT-152 is fixed.</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import change_powermode

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

iarmObj.configureTestCase(ip,port,'IARMBUS_PowerModeToggle_Stress');
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[IARMBUS LIB LOAD STATUS] : %s"%iarmLoadStatus ;
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);
expectedresult="SUCCESS"

if expectedresult in iarmLoadStatus.upper():
    # Repeat PowerMode change for 50 times
    for x in range(0,50):
        # Toggle between state values STANDBY (1) / ON (2)
        for powermode in range(1,3):
            actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Init', 'SUCCESS',verifyList ={});
            print "IARMBUS_Init result: [%s]"%actualresult;
            #Check for return value of IARMBUS_Init
            if expectedresult in actualresult:
                #Calling "IARM_Bus_Connect"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Connect', 'SUCCESS',verifyList ={});
                print "IARMBUS_Connect result: [%s]"%actualresult;

                #Check for return value of IARMBUS_Connect
                if expectedresult in actualresult:
                    #Calling change_powermode
                    result = change_powermode(iarmObj,powermode);
                    print "Set PowerMode to %d: %s"%(powermode,result);

                    #Calling IARMBus_DisConnect API
                    actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_DisConnect', 'SUCCESS',verifyList ={});
                    print "IARMBUS_DisConnect result: [%s]"%actualresult;

                #calling IARMBUS API "IARM_Bus_Term"
                actualresult,iarmTestObj,details = tdklib.Create_ExecuteTestcase(iarmObj,'IARMBUS_Term', 'SUCCESS',verifyList ={});
                print "IARMBUS_Term result: [%s]"%actualresult;
        #End of loop for power mode toggle
    #End of loop for 50 times
    #Unload the iarmbus module
    iarmObj.unloadModule("iarmbus");
