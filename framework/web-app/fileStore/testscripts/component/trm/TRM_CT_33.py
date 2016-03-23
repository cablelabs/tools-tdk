'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1662</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_33</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>613</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests live tune to channel 1, cancel recording 1 when current state of reservation is (R1-R2-R3-R4-R5) and again live tune to channel 1.
Test Case ID: CT_TRM_33
Test Type: Positive</synopsis>
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
obj.configureTestCase(ip,port,'TRM_CT_33');
#Get the result of connection with test component and STB
result = obj.getLoadModuleResult();
print "[TRM LIB LOAD STATUS]  :  %s" %result;
#Set the module loading status
obj.setLoadModuleStatus(result);

#Check for SUCCESS/FAILURE of trm module
if "SUCCESS" in result.upper():

    # Fetch max tuners supported
    maxTuner = trm.getMaxTuner(obj,'SUCCESS')
    if ( 0 == maxTuner ):
        print "Exiting without executing the script"
        obj.unloadModule("trm");
        exit()

    # Step1: Start recording on all the tuners available
    for deviceNo in range(0,maxTuner):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        recordingId = 'RecordIdCh'+streamId
        trm.reserveForRecord(obj,'SUCCESS',kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':10000,'startTime':0,'recordingId':recordingId,'hot':0})

    # Step2: Device1 live tune channel 1
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':10000,'startTime':0})

    # Step3: Device1 cancel ongoing recording on channel 1
    trm.cancelRecording(obj,'SUCCESS',kwargs={'streamId':'01'})

    # Step4: Device1 live tune channel 1
    trm.reserveForLive(obj,'SUCCESS',kwargs={'deviceNo':0,'streamId':'01','duration':10000,'startTime':0})

    #unloading trm module
    obj.unloadModule("trm");
