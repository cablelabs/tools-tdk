'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1594</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Resolution_Persistent_118</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>83</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify that HDMI resolution value does not change after STB reboot.
TestcaseID: CT_DS118</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>This script is causing IPClient box to go to ABL mode.</remarks>
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

#Load module to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'DS_Resolution_Persistent_118');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus("SUCCESS");

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                isDisplay = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in isDisplay:
                    #Save a copy of current resolution
                    copyResolution = devicesettings.dsGetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0"});
                    #Setting Resolution value to 1080i
                    resolution="1080i";
                    # Check if current value is already 1080i
                    if resolution in copyResolution:
                        print "Resolution value already at %s"%resolution;
                    else:
                        devicesettings.dsSetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                else:
                    print "Display Device NOT Connected"

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)

                if "TRUE" in isDisplay:
                    #Reboot the box
                    obj.initiateReboot();

                    #Check the value of resolution after reboot
                    #Calling Device Settings - initialize API
                    result = devicesettings.dsManagerInitialize(obj)
                    #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
                    if "SUCCESS" in result:
                        #Get the value of resolution
                        tdkTestObj = obj.createTestStep('DS_SetResolution');
                        print "Resolution before reboot:%s" %resolution;
                        tdkTestObj.addParameter("port_name","HDMI0");
                        tdkTestObj.addParameter("get_only",1);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        print "[DS GetResolution RESULT] : %s" %actualresult;
                        getResolution = tdkTestObj.getResultDetails();
                        print "getResolution:%s" %getResolution;
                        #comparing the resolution before and after reboot
                        if (expectedresult in actualresult) and (resolution in getResolution):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Resolution persisted after reboot";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Resolution did not persist after reboot";

                        #Revert to original value of resolution
                        #Check if original value was already 1080i
                        if resolution not in copyResolution:
                                devicesettings.dsSetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':copyResolution});

                        #Calling DS_ManagerDeInitialize to DeInitialize API
                        result = devicesettings.dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
