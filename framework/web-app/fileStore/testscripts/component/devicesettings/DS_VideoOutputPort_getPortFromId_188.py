'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_VideoOutputPort_getPortFromId_188</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_VideoOutputPort_getPortFromId</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests the API used to get video output port instance using port Id.
TestcaseID: CT_DS188</synopsis>
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
    <box_type>Terminal-RNG</box_type>
    <!--  -->
    <box_type>IPClient-4</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
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
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_VideoOutputPort_getPortFromId_188');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
#Set the module loading status
dsObj.setLoadModuleStatus(dsLoadStatus);

if "SUCCESS" in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                        #Invoke primitive testcase
                        tdkTestObj = dsObj.createTestStep('DS_VideoOutputPort_getPortFromId');
                        tdkTestObj.addParameter("port_id",0);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                        print "Details: %s"%details;
                        #Check for SUCCESS/FAILURE return value
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                else:
			tdkTestObj.setResultStatus("FAILURE");
                        print "Display device not connected. Skipping testcase"
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
