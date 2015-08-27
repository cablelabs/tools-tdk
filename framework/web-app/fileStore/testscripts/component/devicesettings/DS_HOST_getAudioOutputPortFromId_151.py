'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_HOST_getAudioOutputPortFromId_151</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_HOST_getAudioOutputPortFromId</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script is used to get a reference to the Audio output port by its id.
TestcaseID: CT_DS151</synopsis>
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
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import devicesettings;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DS_HOST_getAudioOutputPortFromId_151');

#Get the result of connection with test component and STB
loadmodulestatus=obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result.upper():
                #Check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:
                        tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPorts');
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print "[TEST EXECUTION RESULT] : %s" %actualresult;
                        print "Details: [%s]"%details;
			if "SUCCESS" in actualresult.upper():
			        #Primitive test case which associated to this Script
				tdkTestObj = obj.createTestStep('DS_HOST_getAudioOutputPortFromId');
                                portList1 = details.split(",")
                                value = len(portList1)
                                print "Number of Audio ID's supported is ", value
                                port_id = 0
				while(port_id < value):
					print "Getting the audio output port from ID: ", port_id
					tdkTestObj.addParameter("port_id", port_id);
					expectedresult="SUCCESS"
		                        tdkTestObj.executeTestCase(expectedresult);
		                        actualresult = tdkTestObj.getResult();
		                        details = tdkTestObj.getResultDetails();
		                        print "[TEST EXECUTION RESULT] : %s" %actualresult;
		                        print "Details: [%s]"%details;
					port_id += 1
		                        #Set the result status of execution
		                        if expectedresult in actualresult:
	        	                        tdkTestObj.setResultStatus("SUCCESS");
        	        	        else:
                	        	        tdkTestObj.setResultStatus("FAILURE");
			else :
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Failed to get the Audio output Ports"

                else :
                        tdkTestObj.setResultStatus("FAILURE");
                        print "Display device not connected. Skipping testcase"

        	#Calling DS_ManagerDeInitialize to DeInitialize API
        	result = devicesettings.dsManagerDeInitialize(obj)
else :
	print "Failed to Load Module"

obj.unloadModule("devicesettings");