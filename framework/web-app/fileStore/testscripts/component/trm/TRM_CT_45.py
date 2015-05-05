'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_45</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>620</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForLive</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tests if switching from channel 2 to 6 on device2 is not allowed due to conflict when the current state of reservation is R1 to R5 on device 1 and L2 to L5 on device 2 to device 5.
Testcase ID: CT_TRM_45</synopsis>
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
import tdklib;
from trm import getMaxTuner,reserveForLive,reserveForRecord,getAllTunerStates

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_45');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
obj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    #Fetch max tuners supported
    maxTuners = getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuners ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Step1: Device 1: Start as many recordings as the number of tuners
    for deviceNo in range(0,maxTuners):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':streamId,'duration':10000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step2: Device 2 to Device 5 tune L2 to L5
    for deviceNo in range(1,maxTuners):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':10000,'startTime':0})

    # Step3: Channel change on Device 2 from L2 to new channel
    streamId = '0'+str(maxTuners+1)
    reserveForLive(obj,'FAILURE',kwargs={'deviceNo':1,'streamId':streamId,'duration':10000,'startTime':0})

    # Step4: Channel change on Device 2 back from new channel to L2
    reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':'02','duration':10000,'startTime':0})

    # Get all Tuner states
    getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
