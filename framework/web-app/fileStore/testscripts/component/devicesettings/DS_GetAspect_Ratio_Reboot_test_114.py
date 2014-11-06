'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>675</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_GetAspect_Ratio_Reboot_test_114</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>57</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_GetAspectRatio</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script compares the Aspect ratio of Video Output Port before and after rebooting the STB
Test Case ID : CT_DS_114</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>the reboot causes the board to go to ABL mode</remarks>
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
obj.configureTestCase(ip,port,'CT_DS_114');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:Display connection status verified";
                        #calling DS_GetAspectRatio to get the aspect ratio
                        tdkTestObj = obj.createTestStep('DS_GetAspectRatio');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        aspectRatiodetailsBefore = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_GetAspectRatio
                        if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Application gets the Aspect ratio";
                                #just printing the AspectRatio
                                print aspectRatiodetailsBefore;
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:Application fails to get the Aspect Ratio of display device";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:Display is not connected with STB";
        obj.initiateReboot();
        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:Display connection status verified";
                        #calling DS_GetAspectRatio to get the aspect ratio
                        tdkTestObj = obj.createTestStep('DS_GetAspectRatio');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        aspectRatiodetailsAfter = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_GetAspectRatio
                        if expectedresult in actualresult:
                                print "SUCCESS: Application gets the Aspect ratio";
                                if aspectRatiodetailsAfter == aspectRatiodetailsBefore:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Aspect ratio are same After and before rebooting the device ";
                                        #just printing the AspectRatio
                                        print aspectRatiodetailsAfter;
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Aspect ratio are not same After and before rebooting the device ";
                        else:
                                print "FAILURE:Application fails to get the Aspect Ratio of display device";
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE:Display is not connected with STB";

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
