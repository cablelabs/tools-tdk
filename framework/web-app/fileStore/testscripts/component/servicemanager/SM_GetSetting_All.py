'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1567</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_GetSetting_All</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>652</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_GetSetting</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script gets settings for all supported services.
Test Case ID: CT_Service Manager_22</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>getSetting will return a valid value if it finds a setting with the same name inside the service. Otherwise, it will return null.</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Service Manager_22');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        # Register all the services in the list
        services = ["deviceSettingService","screenCaptureService","WebSocketService"]
        for service_name in services:
            #calling ServiceManger - registerService API
            tdkTestObj = obj.createTestStep('SM_RegisterService');
            expectedresult="SUCCESS"
            tdkTestObj.addParameter("service_name",service_name);
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            serviceDetail = tdkTestObj.getResultDetails();
            print "[REGISTRATION DETAILS] : %s"%serviceDetail;
            #Check for SUCCESS/FAILURE return value of SM_RegisterService
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS: Registered %s with serviceManager"%service_name
                # Calling getsetting API
                tdkTestObj = obj.createTestStep('SM_GetSetting');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult= tdkTestObj.getResult();
                settingDetails=tdkTestObj.getResultDetails();
                print "[SETTINGS EXECUTION DETAILS] : %s"%settingDetails;
                #Check for SUCCESS/FAILURE return value of SM_GetSetting
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application succesfully executed %s getSetting API"%service_name;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Application Failed to execute %s getSetting API"%service_name;

                #Calling ServiceManger - UnregisterService API
                tdkTestObj = obj.createTestStep('SM_UnRegisterService');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                serviceDetail = tdkTestObj.getResultDetails();
                print "[UNREGISTRATION DETAILS] : %s"%serviceDetail;
                #Check for SUCCESS/FAILURE return value of SM_UnRegisterService
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: UnRegistered %s with serviceManager"%service_name
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Failed to unRegister service %s"%service_name;
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Failed to register service %s"%service_name;
        # End of for loop

        #Unload the servicemanager module
        obj.unloadModule("servicemanager");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
