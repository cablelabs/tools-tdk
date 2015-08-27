'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_getSPDIF_SURROUND_AfterReboot_139</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>CT_DS_139-DS_getSPDIF_SURROUND_AfterReboot_139- This test tries to get the value of SPDIF after setting to STEREO and rebooting the device</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
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
obj.configureTestCase(ip,port,'DS_getSPDIF_SURROUND_AfterReboot_139');
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
                #calling DS_GetSupportedStereoModes get list of StereoModes.
                tdkTestObj = obj.createTestStep('DS_GetSupportedStereoModes');
                tdkTestObj.addParameter("port_name","SPDIF0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                stereomodedetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedStereoModes
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets the list of supported StereoModes";
                        print "%s" %stereomodedetails
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get supported stereo modes";
                #calling DS_SetStereoMode to get and set the stereo modes
                tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                stereomode="STEREO";
                print "Stereo mode value set to:%s" %stereomode;
                tdkTestObj.addParameter("stereo_mode",stereomode);
                tdkTestObj.addParameter("port_name","SPDIF0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                stereomodedetails = tdkTestObj.getResultDetails();
                tdkTestObj.setResultStatus("SUCCESS");
                #Reboot the STB
                obj.initiateReboot();
                #calling Device Settings - initialize API
                tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        #calling DS_SetStereoMode to get and set the stereo modes
                        tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        tdkTestObj.addParameter("port_name","SPDIF0");
                        tdkTestObj.addParameter("get_only",1);
                        expectedresult="SUCCESS"
                        stereomode="SURROUND"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        stereomodedetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get the Stereomode for SPDIF";
                                print "getstereomode: %s" %stereomodedetails;
                                #comparing stereo modes before and after setting
                                if stereomode in stereomodedetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: SURROUND Mode set for SPDIF after Reboot";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: SURROUND Mode not set for SPDIF after Reboot";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE :Application failed to get the Stereomode for SPDIF";
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
