'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_DVRManager_DeleteInvalidRecordingId</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>446</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_DVRManager_DeleteRecording</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests attempt to playback deleted recording content.
TestCase ID: CT_RMF_DVRMgr_19</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>18</execution_time>
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
    <box_type>Emulator-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import mediaframework;
from mediaframework import createRecording,deleteRecording;
from tdkintegration import dvrPlayUrl;
from random import randint

#IP and Port of DVR box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

tdkIntObj = tdklib.TDKScriptingLibrary('tdkintegration','2.0');
mfObj = tdklib.TDKScriptingLibrary('mediaframework','2.0');

#Load modules
tdkIntObj.configureTestCase(ip,port,'RMF_DVRManager_DeleteInvalidRecordingId');
mfObj.configureTestCase(ip,port,'RMF_DVRManager_DeleteInvalidRecordingId');

# Record stream1 and tune to same channel at the same time
mfLoadStatus = mfObj.getLoadModuleResult();
print '[mediaframework LIB LOAD STATUS] : %s'%mfLoadStatus;
mfObj.setLoadModuleStatus(mfLoadStatus);

tdkIntLoadStatus = tdkIntObj.getLoadModuleResult();
print '[tdkintegration LIB LOAD STATUS] : %s'%tdkIntLoadStatus;
tdkIntObj.setLoadModuleStatus(tdkIntLoadStatus);

if ('SUCCESS' in mfLoadStatus.upper()) and ('SUCCESS' in tdkIntLoadStatus.upper()):
        Id = randint(1000,10000)
        recordingId = str(Id)
        title = 'test_dvr_'+recordingId
        duration = '1'
        streamId = '01'

        #Record stream1
        result = createRecording(mfObj, kwargs={"ID":recordingId,"TITLE":title,"DURATION":duration,"STREAMID":streamId})

        #Reboot the box
        mfObj.initiateReboot();
	tdkIntObj.resetConnectionAfterReboot()

        #Playback recorded content
        result = dvrPlayUrl(tdkIntObj, kwargs={"ID":recordingId,"STREAMID":streamId})

        #Delete recorded content
        result = deleteRecording(mfObj,kwargs={'ID':recordingId,'STREAMID':streamId})

        #Playback deleted recording
        result = dvrPlayUrl(tdkIntObj, kwargs={"ID":recordingId,"STREAMID":streamId})

        #unloading modules
        tdkIntObj.unloadModule('tdkintegration');
        mfObj.unloadModule('mediaframework');

elif ('SUCCESS' in mfLoadStatus.upper()) and ('SUCCESS' not in tdkIntLoadStatus.upper()):
        mfObj.unloadModule('mediaframework');
elif ('SUCCESS' not in mfLoadStatus.upper()) and ('SUCCESS' in tdkIntLoadStatus.upper()):
        tdkIntObj.unloadModule('tdkintegration');
        loadmoduledetails = mfObj.getLoadModuleDetails();
        print "loadmoduledetails %s" %loadmoduledetails;
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "Rebooting the STB"
                obj.initiateReboot();
