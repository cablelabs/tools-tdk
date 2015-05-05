'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1568</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>SM_CreateService_All</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>653</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SM_CreateService</primitive_test_name>
  <!--  -->
  <primitive_test_version>0</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Script to create all supported services .
Test Case ID: CT_Service Manager_23</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>Emulator-HYB</box_type>
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
obj = tdklib.TDKScriptingLibrary("servicemanager","1.3");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'CT_Service Manager_23');
loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");
        # Register all the services in the list
        services = ["deviceSettingService","screenCaptureService","WebSocketService"]
        #services = ["deviceSettingService"]
        #services = ["screenCaptureService"]
        #services = ["WebSocketService"]
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
                # Calling Create service API
                tdkTestObj = obj.createTestStep('SM_CreateService');
                expectedresult="SUCCESS"
                tdkTestObj.addParameter("service_name",service_name);
                tdkTestObj.executeTestCase(expectedresult);
                actualresult= tdkTestObj.getResult();
                details =tdkTestObj.getResultDetails();
                print "[TEST EXECUTION DETAILS] : %s"%details;
                #Check for SUCCESS/FAILURE return value of SM_CreateService
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Application succesfully executed %s CreateService API"%service_name;
                else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Application Failed to execute %s CreateService API"%service_name;

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