'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1599</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_GetDisplayDetails_OnDisabledPort_123</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>657</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetEnable</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that EDID value is retrieved even when HDMI port is connected and disabled. in order to disable fetching of display details manual plugout of HDMI is required.
TestcaseID: CT_DS123</synopsis>
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
import devicesettings;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'DS_GetDisplayDetails_OnDisabledPort_123');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:
                    #calling Device Settings - Set Port to disable
                    tdkTestObj = obj.createTestStep('DS_SetEnable');
                    enable=0
                    print "Setting Port enable to %d" %enable;
                    tdkTestObj.addParameter("enable",enable);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Port Disable RESULT] : %s" %actualresult;
                    details = tdkTestObj.getResultDetails();
                    print "Port Disable Details: %s"%details;
                    #Check for SUCCESS/FAILURE return value of DS_SetEnable
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    # Get DisplayDetails after port disable
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    #calling Device Settings - Set Port to enable
                    tdkTestObj = obj.createTestStep('DS_SetEnable');
                    enable=1
                    print "Setting Port enable to %d" %enable;
                    tdkTestObj.addParameter("enable",enable);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Port Enable RESULT] : %s" %actualresult;
                    details = tdkTestObj.getResultDetails();
                    print "[Port Enable Details]: %s"%details;
                    #Check for SUCCESS/FAILURE return value of DS_SetEnable
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                    # Get DisplayDetails after port enable
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    # Get DisplayDetails when HDMI display is not connected
                    tdkTestObj = obj.createTestStep('DS_DisplayDetails');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="FAILURE"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[GetPortDisplayDetails RESULT] : %s" %actualresult;
                    displaydetails = tdkTestObj.getResultDetails();
                    print "[PortDisplayDetails]: %s"%displaydetails;
                    #Check for SUCCESS/FAILURE return value of DS_GetDisplayDetails
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");