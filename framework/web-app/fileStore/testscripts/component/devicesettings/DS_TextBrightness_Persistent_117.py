'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1593</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_TextBrightness_Persistent_117</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>76</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check that Front Panel timer brightness value is persisted after STB reboot.
TestcaseID: CT_DS117</synopsis>
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
obj.configureTestCase(ip,port,'DS_TextBrightness_Persistent_117');
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
                #calling Device Settings - Set/Get TextDisplay Brightness
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                #setting brightness parameter value
                brightness = 5;
                print "Setting text brightness to %d" %brightness;
                message = "Hello"
                print "Setting text to %s"%message;
                tdkTestObj.addParameter("brightness",brightness);
                tdkTestObj.addParameter("get_only",0);
                tdkTestObj.addParameter("text",message);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS SetBrightness RESULT] : %s" %actualresult;
                getBrightness = tdkTestObj.getResultDetails();
                setBrightness = "%s" %brightness;
                print "getBrightness:%s" %getBrightness;
                #Check for SUCCESS/FAILURE return value of DS_SetBrightness
                if expectedresult in actualresult:
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Get TextBrightness equal to Set TextBrightness";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Get TextBrightness not equal to Set TextBrightness";
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

        # Reboot the box
        obj.initiateReboot();

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                #calling Device Settings - Get TextDisplay Brightness
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                print "Brightness before reboot: %d" %brightness;
                tdkTestObj.addParameter("text",message);
                tdkTestObj.addParameter("get_only",1);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS GetBrightness RESULT] : %s" %actualresult;
                getBrightness = tdkTestObj.getResultDetails();
                print "Brightness after reboot:%s" %getBrightness;
                #Check for SUCCESS/FAILURE return value of DS_SetBrightness
                if expectedresult in actualresult:
                        #comparing the brightness value before and after setting
                        if setBrightness in getBrightness :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: TextBrightness same after reboot";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: TextBrightness changed after reboot";
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
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
