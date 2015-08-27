'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_FPCONFIG_getIndicatorFromName_161</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_FPCONFIG_getIndicatorFromName</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: This API gets the FrontPanelndicator instance corresponding to the name parameter returned by the get supported frontpanel indicator device.
Test Case: CT_DS_161
Test Type: Positive.</synopsis>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
    <box_type>Emulator-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_FPCONFIG_getIndicatorFromName_161');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;

if "SUCCESS" in loadmodulestatus.upper():
	#Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        print "[DS Initialize RESULT] : %s" %actualresult;

        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");

                #calling Device Settings - Get Front Panel Indicator.
		tdkTestObj = obj.createTestStep('DS_FPCONFIG_getIndicatorFromName');
		
		indicatorList = ["Message","Power", "Record", "Remote","RfByPass"]
		print ""
		for ele in indicatorList:
	                #Set FP indicator name. 
        	        indicator_name = ele
	                print "Indicator name: %s" %indicator_name;
	                tdkTestObj.addParameter("indicator_name",indicator_name);
	                expectedresult="SUCCESS"
        	        tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
			details = tdkTestObj.getResultDetails();
	                print "[DS_FPCONFIG_getIndicatorFromName RESULT] : %s" %actualresult;
			print "[DS_FPCONFIG_getIndicatorFromName DETAILS] : %s" %details;			

			#Check for SUCCESS/FAILURE return value of DS_FPCONFIG_getIndicatorFromName
        	        if expectedresult in actualresult:
				tdkTestObj.setResultStatus("SUCCESS");
                        	print "SUCCESS: Get DS_FPCONFIG_getIndicatorFromName";
	                else:
        	                tdkTestObj.setResultStatus("FAILURE");
                	        print "FAILURE: Get DS_FPCONFIG_getIndicatorFromName";
			print " "
                #calling DS_ManagerDeInitialize to DeInitialize API
                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[DS Deinitalize RESULT] : %s" %actualresult;

                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");
	else:
		tdkTestObj.setResultStatus("FAILURE");	
	
	#Unload the deviceSettings module	
	obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");
