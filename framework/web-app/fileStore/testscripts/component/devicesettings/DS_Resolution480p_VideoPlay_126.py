'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Resolution480p_VideoPlay_126</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>83</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetResolution</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests if trickplay is successful after changing Device Settings / Video resolution for HDMI to 480p and rebooting the Box.
Test Case ID : CT_DS126</synopsis>
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
from devicesettings import dsManagerInitialize, dsManagerDeInitialize
from tdkintegration import dvrPlayUrl;

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

# Step1: Change Device Settings Video resolution for HDMI to 480p
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
dsObj.configureTestCase(ip,port,'DS_Resolution480p_VideoPlay_126');
loadmodulestatus = dsObj.getLoadModuleResult();
print "[devicesettings LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
dsObj.setLoadModuleStatus(loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
        #calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                # Save a copy of current resolution
                tdkTestObj = dsObj.createTestStep('DS_SetResolution');
                tdkTestObj.addParameter("port_name","HDMI0");
                tdkTestObj.addParameter("get_only",1);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[Get Resolution RESULT] : %s" %actualresult;
                copyResolution = tdkTestObj.getResultDetails();
                print "Current Resolution value : %s" %copyResolution;
                #Check for SUCCESS/FAILURE return value of DS_SetResolution
                if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                # Set resolution value to 480p
                resolution="480p";
                # Check if current value is already 480p
                if resolution not in copyResolution:
                    print "Setting resolution to %s" %resolution;
                    tdkTestObj.addParameter("resolution",resolution);
                    tdkTestObj.addParameter("port_name","HDMI0");
                    tdkTestObj.addParameter("get_only",0);
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    print "[Set Resolution RESULT] : %s" %actualresult;
                    getResolution = tdkTestObj.getResultDetails();
                    print "getResolution:%s" %getResolution;
                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                    if expectedresult in actualresult:
                        #comparing the resolution before and after setting
                        if resolution in getResolution :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Get resolution same as Set resolution value";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Get resolution not same as Set resolution value";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)

        # Step2: Reboot the box
        dsObj.initiateReboot();

        # Step3: Trickplay channel 6 and then channel 3
        # Live trickplay after resolution change and reboot
        tdkIntObj = tdklib.TDKScriptingLibrary("tdkintegration","2.0");
        tdkIntObj.configureTestCase(ip,port,'DS_Resolution480p_VideoPlay_126');
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

        # Step4: Revert to original value of resolution
        # Check if original value was already 480p
        if resolution not in copyResolution:
            #calling Device Settings - initialize API
            result = dsManagerInitialize(dsObj)
            #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
            if "SUCCESS" in result:
                # Set resolution value to original value
                print "Setting resolution to %s" %copyResolution;
                tdkTestObj.addParameter("resolution",copyResolution);
                tdkTestObj.addParameter("port_name","HDMI0");
                tdkTestObj.addParameter("get_only",0);
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                print "[Set Resolution RESULT] : %s" %actualresult;
                getResolution = tdkTestObj.getResultDetails();
                print "getResolution:%s" %getResolution;
                #Check for SUCCESS/FAILURE return value of DS_SetResolution
                if expectedresult in actualresult:
                        #comparing the resolution before and after setting
                        if resolution in getResolution :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "SUCCESS: Get resolution same as Set resolution value";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE: Get resolution not same as Set resolution value";
                else:
                        tdkTestObj.setResultStatus("FAILURE");

                #calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)

        #Unload the deviceSettings module
        dsObj.unloadModule("devicesettings");
