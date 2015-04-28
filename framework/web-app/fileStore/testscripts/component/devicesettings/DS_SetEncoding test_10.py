'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>201</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetEncoding test_10</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>81</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetEncoding</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This test script Sets and gets the Encoding Format of Audio.Test Case ID : CT_DS_10.  Note:This script will return duplicates, If running second time without restarting agent. Agent process may lead to crash/restart.This is an issue with DS.</synopsis>
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
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_DS_10');
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
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_GetSupportedEncodings get list of encoding.
                tdkTestObj = obj.createTestStep('DS_GetSupportedEncodings');
                tdkTestObj.addParameter("port_name","HDMI0");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                encodingdetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_GetSupportedEncodings
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully gets the list encoding supported";
                        print "%s" %encodingdetails
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get supported encoding list";
                #calling DS_SetEncoding to get and set the encoding  
                tdkTestObj = obj.createTestStep('DS_SetEncoding');
                encoding="AC3";
                print "Encoding value set to:%s" %encoding; 
                tdkTestObj.addParameter("encoding_format",encoding);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                encodingdetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_SetEncoding 
                if expectedresult in actualresult:
                        print "SUCCESS :Application successfully get and set the encoding";
                        print "getencoding: %s" %encodingdetails;
                        # comparing the encoding detail before and after setting 
                        if encoding in encodingdetails:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Both the encoding formats are same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Both the encoding formats are not same";
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
                #tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE :Application failed to set and get the encoding formats";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
