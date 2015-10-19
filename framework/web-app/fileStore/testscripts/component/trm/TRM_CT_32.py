'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1699</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_32</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests recording and then live tune to channel 6 on terminal2 when current state of reservation is L1 on terminal1 and L2-R3-R4-R5 on terminal2.
Test Case ID: CT_TRM_32
Test Type: Negative</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import trm;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("trm","2.0");
obj.configureTestCase(ip,port,'TRM_CT_32');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
obj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    duration = 10000
    startTime = 0

    #Fetch max tuners supported
    maxTuner = trm.getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Pre-condition: Device1:L1 - Device2:L2-R3-R4-R5
    # Device1: Live tune to channel 1
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':duration,'startTime':startTime})

    # Device2: Live tune to channel 2
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':'02','duration':duration,'startTime':startTime})

    # Device2: Recording on maxtuner-2 channels
    for streamNo in range(3,maxTuner+1):
        streamId = '0'+str(streamNo)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':0})
    # Pre-condition End

    # Device2: Recording new channel
    streamId = '0'+str(maxTuner+1)
    recordingId = 'RecordIdCh'+streamId
    trm.reserveForRecord(obj,'FAILURE',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':recordingId,'hot':0})

    # Device2: Live tune to new channel
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':1,'streamId':streamId,'duration':duration,'startTime':startTime})

    # Get all Tuner states
    trm.getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
