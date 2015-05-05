'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_Resolution720p_Trickplay</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To change output resolution to 720P and perform live trickplay.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <rdk_version>RDK1.3</rdk_version>
    <!--  -->
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import devicesettings;
from tdkintegration import dvrPlayUrl;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
obj.configureTestCase(ip,port,'E2E_RMF_Resolution720p_Trickplay');
loadmodulestatus =obj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
obj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():

        #calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(obj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                result = devicesettings.dsIsDisplayConnected(obj)
                if "TRUE" in result:
                        #Save a copy of current resolution
                        copyResolution = devicesettings.dsGetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0"});
                        # Set resolution value to 720p
                        resolution="720p";
                        # Check if current value is already 720p
                        if resolution not in copyResolution:
                                devicesettings.dsSetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                        else:
                                print "Resolution value already at %s"%copyResolution

                        # Live trickplay channel 1 after resolution change
                        tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                        tdkIntObj.configureTestCase(ip,port,'E2E_RMF_Resolution720p_Trickplay');
                        loadmodulestatus = tdkIntObj.getLoadModuleResult();
                        print "TDKIntegration module loading status :  %s" %loadmodulestatus;
                        tdkIntObj.setLoadModuleStatus(loadmodulestatus);

                        if "SUCCESS" in loadmodulestatus.upper():
                               streamId = '01'
                               result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                               print "Tuning to stream %s is [%s]"%(streamId,result)
                               tdkIntObj.unloadModule("tdkintegration");

                        # Revert to original value of resolution
                        if resolution not in copyResolution:
                                devicesettings.dsSetResolution(obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':copyResolution});

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(obj)

        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
