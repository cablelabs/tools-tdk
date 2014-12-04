'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_SetTextBrightness_125</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>76</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetBrightness</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test script Sets and gets a valid brightness value in the text display of given Front panel Indicator.
Test Case ID : CT_DS125</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK1.2</rdk_version>
    <!--  -->
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from devicesettings import dsManagerInitialize, dsManagerDeInitialize

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'DS_SetTextBrightness_125');
loadmodulestatus =obj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #calling Device Settings - initialize API
        result = dsManagerInitialize(obj)
        #Check for return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                tdkTestObj = obj.createTestStep('DS_SetBrightness');
                #Pre-condition: Save the existing value of TextBrightness
                message = "Hello"
                tdkTestObj.addParameter("text",message);
                tdkTestObj.addParameter("get_only",1);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                copyBrightness = tdkTestObj.getResultDetails();
                print "PRE-CONDITION: Result: [%s] Previous TextBrightness: [%s]" %(actualresult,copyBrightness);
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        #Set TextBrightness to 100
                        setBrightness = 100;
                        print "Set Text=%s Brightness=%s"%(message,setBrightness);
                        tdkTestObj.addParameter("brightness",setBrightness);
                        tdkTestObj.addParameter("get_only",0);
                        tdkTestObj.addParameter("text",message);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        getBrightness = tdkTestObj.getResultDetails();
                        print "Result: [%s] Details: [%s]" %(actualresult,getBrightness);
                        #Check for return value of Set TextBrightness
                        if (expectedresult in actualresult) and (str(setBrightness) in getBrightness):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Get TextBrightness equal to Set TextBrightness";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "Get TextBrightness not equal to Set TextBrightness";

                        #Post-condition: Set to previous value of TextBrightness
                        print "Restore Text=%s Brightness=%s"%(message,copyBrightness);
                        tdkTestObj.addParameter("brightness",int(copyBrightness));
                        tdkTestObj.addParameter("get_only",0);
                        tdkTestObj.addParameter("text",message);
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        currBrightness = tdkTestObj.getResultDetails();
                        print "POST-CONDITION: Result: [%s] Current TextBrightness: [%s]" %(actualresult,currBrightness);
                        if (expectedresult in actualresult) and (copyBrightness in currBrightness):
                                tdkTestObj.setResultStatus("SUCCESS");
                        else:
                                tdkTestObj.setResultStatus("FAILURE");

                # Failed to save previous value of brightness
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
