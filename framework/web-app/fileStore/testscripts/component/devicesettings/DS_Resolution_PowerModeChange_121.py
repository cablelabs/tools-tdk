'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1601</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DS_Resolution_PowerModeChange_121</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>82</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DS_SetPowerMode</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis></synopsis>
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
from iarmbus import change_powermode
from devicesettings import dsManagerInitialize, dsManagerDeInitialize, dsIsDisplayConnected

#Test component to be tested
dsObj = tdklib.TDKScriptingLibrary("devicesettings","1.2");
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","1.3");

#Ip address of the selected STB for testing
ip = <ipaddress>
port = <port>

#Load modules
dsObj.configureTestCase(ip,port,'DS_Resolution_PowerModeChange_121');
dsLoadStatus = dsObj.getLoadModuleResult();
print "[DS LIB LOAD STATUS]  :  %s" %dsLoadStatus ;
dsObj.setLoadModuleStatus(dsLoadStatus);

iarmObj.configureTestCase(ip,port,'DS_Resolution_PowerModeChange_121');
iarmLoadStatus = iarmObj.getLoadModuleResult();
print "[IARMBUS LIB LOAD STATUS] : %s"%iarmLoadStatus ;
iarmObj.setLoadModuleStatus(iarmLoadStatus);

if ('SUCCESS' in dsLoadStatus.upper()) and ('SUCCESS' in iarmLoadStatus.upper()):
        #Calling Device Settings - initialize API
        result = dsManagerInitialize(dsObj)
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if "SUCCESS" in result:
                #Calling DS_IsDisplayConnectedStatus function to check for display connection status
                result = dsIsDisplayConnected(dsObj)
                if "TRUE" in result:
                    #Calling Device Settings - Set Resolution
                    dsTestObj = dsObj.createTestStep('DS_SetResolution');
                    resolution="1080i";
                    print "Setting resolution to %s" %resolution;
                    dsTestObj.addParameter("resolution",resolution);
                    dsTestObj.addParameter("port_name","HDMI0");
                    dsTestObj.addParameter("get_only",0);
                    expectedresult="SUCCESS"
                    dsTestObj.executeTestCase(expectedresult);
                    actualresult = dsTestObj.getResult();
                    print "[DS SetResolution RESULT] : %s" %actualresult;
                    getResolution = dsTestObj.getResultDetails();
                    print "getResolution:%s" %getResolution;
                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                    #Comparing the resolution before and after setting
                    if (expectedresult in actualresult) and (resolution in getResolution):
                        dsTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Get resolution same as Set resolution value";
                    else:
                        dsTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Get resolution not same as Set resolution value";

                    #Calling IARMBus change_powermode to OFF(0)
                    powermode=0
                    result = change_powermode(iarmObj,powermode);
                    print "Set PowerMode to %d: %s"%(powermode,result);

                    #Calling IARMBus change_powermode to ON(2)
                    powermode=2
                    result = change_powermode(iarmObj,powermode);
                    print "Set PowerMode to %d: %s"%(powermode,result);

                    #Calling Device Setting - Get Resolution
                    dsTestObj = dsObj.createTestStep('DS_SetResolution');
                    print "Resolution before enable:%s" %resolution;
                    dsTestObj.addParameter("port_name","HDMI0");
                    dsTestObj.addParameter("get_only",1);
                    expectedresult="SUCCESS"
                    dsTestObj.executeTestCase(expectedresult);
                    actualresult = dsTestObj.getResult();
                    print "[DS GetResolution RESULT] : %s" %actualresult;
                    getResolution = dsTestObj.getResultDetails();
                    print "getResolution:%s" %getResolution;
                    #Check for SUCCESS/FAILURE return value of DS_SetResolution
                    #Comparing the resolution before and after port enabling
                    if (expectedresult in actualresult) and (resolution in getResolution):
                        dsTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS: Resolution same after power mode off/on";
                    else:
                        dsTestObj.setResultStatus("FAILURE");
                        print "SUCCESS: Resolution changed after power mode off/on";

                #Calling DS_ManagerDeInitialize to DeInitialize API
                result = dsManagerDeInitialize(dsObj)

        #Unload the modules
        dsObj.unloadModule("devicesettings");
        iarmObj.unloadModule('iarmbus');
elif ('SUCCESS' not in dsLoadStatus.upper()) and ('SUCCESS' in iarmLoadStatus.upper()):
        iarmObj.unloadModule('iarmbus');
elif ('SUCCESS' in dsLoadStatus.upper()) and ('SUCCESS' not in iarmLoadStatus.upper()):
        dsObj.unloadModule('devicesettings');