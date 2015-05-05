'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_EnableHDCP_UsingMfrKey_133</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_EnableHDCP</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests enable HDCP authentication using manufacturer HDCP keys.
TestcaseID: CT_DS133</synopsis>
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
obj.configureTestCase(ip,port,'DS_EnableHDCP_UsingMfrKey_133');
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

                        #Enable HDCP
                        tdkTestObj = obj.createTestStep('DS_EnableHDCP');
                        #Passing default values for enabling HDCP
                        key = '0'
                        keySize = 0
                        protectContent = 1
                        useMfrKey = 1
                        tdkTestObj.addParameter("hdcpKey",key);
                        tdkTestObj.addParameter("keySize",keySize);
                        tdkTestObj.addParameter("protectContent",protectContent);
                        tdkTestObj.addParameter("useMfrKey",useMfrKey);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "useMfrKey: %d protectContent: %d HDCP key: %s keySize: %d"%(useMfrKey,protectContent,key,keySize)
                        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                        print "Details: [%s]"%details;
                        #Check for SUCCESS/FAILURE return value of DS_GetHDCPStatus
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");

                        #Get the status of HDCP authentication
                        tdkTestObj = obj.createTestStep('DS_GetHDCPStatus');
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,actualresult)
                        print "Details: [%s]"%details;
                        #Check for SUCCESS/FAILURE return value of DS_GetHDCPStatus
                        if expectedresult in actualresult:
                            #Check if status = "Authenticated(2)"
                            if (("Authenticated" in details) or ('2' in details)):
                                tdkTestObj.setResultStatus("SUCCESS");
                            else:
                                print "GetHDCPStatus success but HDCP authentication failed"
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                else:
                        print "HDMI display not connected. Exiting..."
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
