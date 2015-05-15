#This python script is autogenerated by parsing the original scripts imported from the Database
#This script is supposed to be called from the genericscript.py 
#TODO:replace this caling script name with correct one


'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>258</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_AddDisplayconnection Listener test_14</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>104</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_AddDisplayConnectionListener</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This script checks for adding and removing display connection listener.
TestCase ID:CT_DS_14</synopsis>
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
#TODO: validate which imports are necessary and remove others
import sys;
from time import gmtime, strftime;
import tdklib;
import time;
import datalib;
import numpy as np;




def executeTests(obj):
	
	loadmodulestatus =obj.getLoadModuleResult();
	print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
	if "SUCCESS" in loadmodulestatus.upper():
	        #Set the module loading status
	        obj.setLoadModuleStatus("SUCCESS");
	
	        #calling Device Settings - initialize API
	        tdkTestObj = obj.createTestStep('DS_ManagerInitialize',0);
	        expectedresult="SUCCESS"
	        tdkTestObj.executeTestCase(expectedresult);
	        actualresult = tdkTestObj.getResult();
	        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize 
	        if expectedresult in actualresult:
	                tdkTestObj.setResultStatus("SUCCESS");
	                print "SUCCESS :Application successfully initialized with Device Settings library";
	                #calling DS_AddDisplayConnectionListener for adding listener for display connection change
	                tdkTestObj = obj.createTestStep('DS_AddDisplayConnectionListener',5);
	                expectedresult="SUCCESS"
	                tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
	                #Check for SUCCESS/FAILURE return value of DS_AddDisplayConnectionListener 
	                if expectedresult in actualresult:
	                        tdkTestObj.setResultStatus("SUCCESS");
	                        print "SUCCESS :Application successfully display connection state change listener is added";
	                else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "FAILURE :Failed to add listener for display connection state change";
	                #calling DS_RemoveDisplayConnectionListener for removing listener for display connection state change
	                tdkTestObj = obj.createTestStep('DS_RemoveDisplayConnectionListener');
	                expectedresult="SUCCESS"
	                tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
	                #Check for SUCCESS/FAILURE return value of DS_RemoveDisplayConnectionListener 
	                if expectedresult in actualresult:
	                        tdkTestObj.setResultStatus("SUCCESS");
	                        print "SUCCESS :Application successfully display connection state change listener is removed";
	                else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "FAILURE :Failed to remove listener for display connection state change";
	                #calling DS_ManagerDeInitialize to DeInitialize API 
	                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize',0);
	                expectedresult="SUCCESS"
	                tdkTestObj.executeTestCase(expectedresult);
	                actualresult = tdkTestObj.getResult();
	                #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize 
	                if expectedresult in actualresult:
	                        tdkTestObj.setResultStatus("SUCCESS");
	                        print "SUCCESS :Application successfully display connection state change listener is removed";
	                else:
	                        tdkTestObj.setResultStatus("FAILURE");
	                        print "FAILURE :Failed to remove listener for display connection state change";
	                #calling DS_ManagerDeInitialize to DeInitialize API 
	                tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize',0);
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
	        #Set the module loading status
	        obj.setLoadModuleStatus("FAILURE");