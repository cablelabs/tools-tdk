'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_GetCPUTemperature_STRESS_127</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_GetCPUTemperature</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script performs stress test on get CPU Temperature.
Test Case ID : CT_DS_127</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>12</execution_time>
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
from devicesettings import dsManagerInitialize,dsManagerDeInitialize,dsGetCPUTemp;
from time import sleep;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_GetCPUTemperature_STRESS_127');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Get the cpu temp for 8 mins once in every 5sec
                for n in range (0,100):
                        #Calling Device Setting Get CPU Temperature
                        result,details = dsGetCPUTemp(dsObj,"SUCCESS")
                        sleep(5);
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
