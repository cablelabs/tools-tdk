'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1733</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>TRM_CT_35</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id>613</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>TRM_TunerReserveForRecord</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This tests live tune to channel 1 when current state of reservation is (R1-L2-L3-L4-L5).
Test Case ID: CT_TRM_35
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
obj.configureTestCase(ip,port,'TRM_CT_35');
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

    duration = 10000
    startTime = 0

    # Step1: Start live tuning on all the remaining tuners on different channels from different devices
    for deviceNo in range(0,maxTuner-2):
        # Frame different request URL for each client box
        streamId = '0'+str(deviceNo+1)
        trm.reserveForLive(obj,"SUCCESS",kwargs={'deviceNo':deviceNo,'streamId':streamId,'duration':duration,'startTime':startTime})

    # Step2: Device1 start recording on channel 5
    streamId = '0'+str(deviceNo+2)
    trm.reserveForRecord(obj,"SUCCESS",kwargs={'deviceNo':0,'streamId':streamId,'duration':duration,'startTime':startTime,'recordingId':'RecordIdCh01','hot':0})

    # Step3: Device1 live tune channel 5
    trm.reserveForLive(obj,"SUCCESS",kwargs={'deviceNo':0,'streamId':streamId,'duration':duration,'startTime':startTime})

    trm.getAllTunerStates(obj,'SUCCESS')

    #unloading trm module
    obj.unloadModule("trm");
