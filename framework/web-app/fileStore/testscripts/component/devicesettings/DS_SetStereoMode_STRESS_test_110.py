'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>654</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetStereoMode_STRESS_test_110</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>85</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetStereoMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test is to successfully change the Stereo Mode continuously for every 100ms repeatedly for x times.				
Test case ID : CT_DS_110</synopsis>
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
    <box_type>Terminal-RNG</box_type>
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
import time;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_110');
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
                i = 0;
                for i in range(0,100):
                        print "****************%d" %i;
                        #calling DS_SetStereoMode to get and set the stereo modes
                        tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        stereomode="SURROUND";
                        print "Stereo mode value set to : %s" %stereomode;
                        tdkTestObj.addParameter("stereo_mode",stereomode);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        stereomodedetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the stereo modes";
                                print "getstereomode: %s" %stereomodedetails;
                                #comparing stereo modes before and after setting
                                if stereomode in stereomodedetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the stereo modes are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the stereo modes are not same";
                        else:           
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set and get the stereo modes";
                        time.sleep(100/1000);
                        #calling DS_SetStereoMode to get and set the stereo modes
                        tdkTestObj = obj.createTestStep('DS_SetStereoMode');
                        stereomode="STEREO";
                        print "Stereo mode value set to: %s" %stereomode;
                        tdkTestObj.addParameter("stereo_mode",stereomode);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        stereomodedetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetStereoMode
                        if expectedresult in actualresult:
                                print "SUCCESS :Application successfully get and set the stereo modes";
                                print "getstereomode: %s" %stereomodedetails;
                                #comparing stereo modes before and after setting
                                if stereomode in stereomodedetails:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the stereo modes are same";
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the stereo modes are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "****************%d" %i;
                                print "FAILURE :Application failed to set and get the stereo modes";
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
