'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1594</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
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
import devicesettings;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load module D.S module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_Resolution_Persistent_118');
dsLoadStatus =dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus("dsLoadStatus");

if "SUCCESS" in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                    #Save a copy of current resolution
                    copyResolution = devicesettings.dsGetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0"});
                    #Get the resolution list supported by TV.
                    print "Get list of resolutions supported on HDMI0"

                    tdkTestObj = dsObj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult = "SUCCESS"
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedresult);
                    #Get the result of execution
                    result = tdkTestObj.getResult();
                    supportedResolutions = tdkTestObj.getResultDetails();
                    print "Result: [%s] Details: [%s]"%(result,supportedResolutions)
                    #Set the result status of execution
                    if expectedresult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

		    list = supportedResolutions.split(":");
		    resolutionList = list[1].split(",");

		    for resolution in resolutionList:
			if resolution != copyResolution:
				print "Setting resolution to ",resolution
                        	devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
				break;
                    	else:
                        	print "Resolution value already at ",resolution;
                if "TRUE" in result:
                    #Reboot the box
                    dsObj.initiateReboot();

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
                        dsObj.initiateReboot();
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
        dsObj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        dsObj.setLoadModuleStatus("FAILURE");
