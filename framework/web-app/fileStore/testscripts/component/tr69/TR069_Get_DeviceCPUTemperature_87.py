'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TR069_Get_DeviceCPUTemperature_87</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>585</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Tr069_Get_Profile_Parameter_Values</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: To fetch the device CPU temperature by querying the tr69Hostif through curl.  Query string "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp". 
TestCaseID: CT_TR69_87
TestType: Positive</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize,dsManagerDeInitialize,dsGetCPUTemp;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Load DS module
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'TR069_Get_DeviceCPUTemperature_87');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

if 'SUCCESS' in dsLoadStatus.upper():
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
		#Test component to be tested
		tr69Obj = tdklib.TDKScriptingLibrary("tr069module","2.0");
		tr69Obj.configureTestCase(ip,port,'TR069_Get_DeviceCPUTemperature_87');
		tr69LoadStatus = tr69Obj.getLoadModuleResult();
		print "[TR069 LIB LOAD STATUS]  :  %s" %tr69LoadStatus;
		tr69Obj.setLoadModuleStatus(tr69LoadStatus);
		if 'SUCCESS' in tr69LoadStatus.upper():
			#Parameter is the profile path to be queried
			profilePath = "Device.DeviceInfo.X_RDKCENTRAL-COM.CPUTemp"
			#Calling Tr069_Get_Profile_Parameter_Values
        		tr69TestObj = tr69Obj.createTestStep('Tr069_Get_Profile_Parameter_Values');
        		expectedresult = "SUCCESS"
       			tr69TestObj.addParameter("path",profilePath);
        		tr69TestObj.executeTestCase(expectedresult);
        		actualresult = tr69TestObj.getResult();
        		tr69Details = tr69TestObj.getResultDetails();
        		print "Result : [%s] Details : [%s]" %(actualresult,tr69Details);
        		#Check for SUCCESS/FAILURE return value of Tr069_Get_Profile_Parameter_Values
        		if expectedresult in actualresult:
				#Calling Device Setting - Get CPU Temperature
               			dsResult,dsDetails = dsGetCPUTemp(dsObj,'SUCCESS')
                		#Verify that temperature reported from ds and tr69 are not very different (max 1C difference)
                		tolerance = float(tr69Details) - float(dsDetails)
                		print "Temperature value difference between DS and TR69 is %",abs(tolerance),"C"
				if ( abs(tolerance) < float(1) ):
        				tr69TestObj.setResultStatus("SUCCESS");
				else:
                        		print "TR69 CPU Temperature value failed verification"
					tr69TestObj.setResultStatus("FAILURE");
        		else:
				tr69TestObj.setResultStatus("FAILURE");
			#Unload the tr069module
			tr69Obj.unloadModule("tr069module");
                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)
        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
