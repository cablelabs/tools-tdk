'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_RMF_Resolution480p_Trickplay</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>528</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TDKE2E_LinearTV_Play_URL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests if trickplay is successful after changing Device Settings HDMI Video resolution to 480p and rebooting the Box.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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

# Step1: Change Device Settings Video resolution for HDMI to 480p
dsObj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
dsObj.configureTestCase(ip,port,'E2E_RMF_Resolution480p_Trickplay');
loadmodulestatus = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
dsObj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #Calling Device Settings - initialize API
        result = devicesettings.dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                isDisplay = devicesettings.dsIsDisplayConnected(dsObj)
                if "TRUE" in isDisplay:
                    #Save a copy of current resolution
                    copyResolution = devicesettings.dsGetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0"});
                    # Set resolution value to 480p
                    resolution="480p";
                    # Check if current value is already 480p
                    if resolution not in copyResolution:
                            devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':resolution});
                    else:
                            print "Resolution value already at %s"%copyResolution

                #calling DS_ManagerDeInitialize to DeInitialize API
                result = devicesettings.dsManagerDeInitialize(dsObj)

                if "TRUE" in isDisplay:
                    # Step2: Reboot the box
                    dsObj.initiateReboot();

                    # Step3: Trickplay channel 2 and then channel 1
                    tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
                    tdkIntObj.configureTestCase(ip,port,'E2E_RMF_Resolution480p_Trickplay');
                    loadmodulestatus = tdkIntObj.getLoadModuleResult();
                    print "TDKIntegration module loading status :  %s" %loadmodulestatus;
                    tdkIntObj.setLoadModuleStatus(loadmodulestatus);

                    if "SUCCESS" in loadmodulestatus.upper():
                        # Tune to channel 2
                        streamId = '02'
                        result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                        print "Tuning to stream %s is [%s]"%(streamId,result)
                        if "SUCCESS" in result:
                            # Tune to channel 1
                            streamId = '01'
                            result = dvrPlayUrl(tdkIntObj, kwargs={'play':'trickplay',"STREAMID":streamId})
                            print "Tuning to stream %s is [%s]"%(streamId,result)
                        tdkIntObj.unloadModule("tdkintegration");

                    # Step4: Revert to original value of resolution unless original value was already 480p
                    if resolution not in copyResolution:
                        #calling Device Settings - initialize API
                        result = devicesettings.dsManagerInitialize(dsObj)
                        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
                        if "SUCCESS" in result:
                            devicesettings.dsSetResolution(dsObj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':copyResolution});
                            #Calling DS_ManagerDeInitialize to DeInitialize API
                            result = devicesettings.dsManagerDeInitialize(dsObj)

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
