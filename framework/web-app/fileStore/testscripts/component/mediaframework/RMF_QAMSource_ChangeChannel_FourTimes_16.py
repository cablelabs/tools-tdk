'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1584</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_QAMSource_ChangeChannel_FourTimes_16</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: RMFQAMSrc –  Tune to a  channel, and change the channel after play back for sometime, and change channel for 4 more times. So, all 5 tunners are cached.
Test CaseId: CT_RMF_QAMSrc_MPSink_16
Test Case Type: Positive.</synopsis>
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
    <box_type>Terminal-RNG</box_type>
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
import mediaframework;
import time;

expected_Result="SUCCESS"
failure = "FAILURE"
createCount = 0

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_QAMSource_ChangeChannel_FourTimes_16');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global details
    global tdkTestObj
    global createCount
    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Create_Instance':
        #Stream details for tuning
        if parametervalue[0] == "QAMSrc":
                createCount = createCount + 1;
                #temproary need to be removed
                if createCount == 3:
                        createCount = 1
                print "QAMSrc ceateCount increament"

        print "createCount=",createCount
        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        ocapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("qamSrcUrl");
        parametervalue.append(ocapLocator);
        print "OcapLocator:",ocapLocator

        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        newOcapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("newQamSrcUrl");
        parametervalue.append(ocapLocator);
        print "New OcapLocator:",newOcapLocator

    if teststep == 'RmfElement_QAMSrc_ChangeURI':
        #Stream details for tuning
        print "createCount=",createCount
        streamDetails = tdkTestObj.getStreamDetails('0' + str(createCount));
        changeUri = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(changeUri);
        print "ChangeUri:",changeUri

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep != 'RMF_Element_GetState' and teststep != 'RmfElement_CheckFor_SPTSReadError':
       tdkTestObj.setResultStatus(result);

    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;

    return result

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;

if expected_Result in loadModuleStatus.upper():

        #Pre-requsite to kill the rmfStreamer Gthread instance and to start new gthread instance.
        obj.initiateReboot();

        #Prmitive test case which associated to this Script
        #Change the List according to Prmitive test case
        src_parameter=[];
        src_element=[];
        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Init',obj,expected_Result,src_parameter,src_element);
        if expected_Result in result.upper():
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_InitPlatform',obj,expected_Result,src_parameter,src_element);
                if expected_Result in result.upper():
                        src_parameter=["rmfElement","factoryEnable"]
                        src_element=["QAMSrc","true"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["MPSink"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                if expected_Result in result.upper():
                                        src_parameter=["rmfElement"]
                                        src_element=["MPSink"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                        if expected_Result in result.upper():
                                                src_parameter=["X","Y","width","apply","height"]
                                                src_element=[0,0,1280,0,720]
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,expected_Result,src_parameter,src_element);
                                                if expected_Result in result.upper():
                                                        src_parameter=["rmfSourceElement","rmfSinkElement"]
                                                        src_element=["QAMSrc","MPSink"]
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,expected_Result,src_parameter,src_element);
                                                        if expected_Result in result.upper():
                                                                src_parameter=["rmfElement","defaultPlay","playSpeed","playTime"]
                                                                src_element=["QAMSrc",1,1.0,0.0]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,expected_Result,src_parameter,src_element);
                                                                if expected_Result in result.upper():
                                                                        time.sleep(30);
                                                                        src_parameter=["rmfElement"]
                                                                        src_element=["QAMSrc"]
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,expected_Result,src_parameter,src_element);
                                                                        #Change made based on the comment made in RDKTT-108.
                                                                        #if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                        if expected_Result in result.upper():
                                                                                print "QAMSource play successful"
                                                                                #tdkTestObj.setResultStatus(result);
                                                                                src_parameter=["rmfElement"]
                                                                                src_element=["QAMSrc"]
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                                                index = 0
                                                                                numOfTimesChannelChange = 4
                                                                                while  index < numOfTimesChannelChange:
                                                                                        if expected_Result in result.upper():
                                                                                                time.sleep(5);
                                                                                                print "QAMSource pause successful"
                                                                                                #tdkTestObj.setResultStatus(result);
                                                                                                src_parameter=["rmfElement","factoryEnable","newQamSrc","numOfTimeChannelChange"]
                                                                                                src_element=["QAMSrc","true","true",index]
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                                                                                if expected_Result in result.upper():
                                                                                                        src_parameter=["numOfTimeChannelChange"]
                                                                                                        src_element=[index]
                                                                                                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_ChangeURI',obj,expected_Result,src_parameter,src_element);
                                                                                                        #time.sleep(10);
                                                                                                        if expected_Result in result.upper():
                                                                                                                src_parameter=["rmfSourceElement","rmfSinkElement","newQamSrc","numOfTimeChannelChange"]
                                                                                                                src_element=["QAMSrc","MPSink","true",index]
                                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,expected_Result,src_parameter,src_element);
                                                                                                                if expected_Result in result.upper():
                                                                                                                        src_parameter=["rmfElement","defaultPlay","playSpeed","playTime","newQamSrc","numOfTimeChannelChange"]
                                                                                                                        src_element=["QAMSrc",1,1.0,0.0,"true",index]
                                                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,expected_Result,src_parameter,src_element);
                                                                                                                        if index == 1:
                                                                                                                                #Change the duation to 1 hour after 2 time channel change.
                                                                                                                                time.sleep(10)
                                                                                                                        else:
                                                                                                                                time.sleep(10);
                                                                                                                        if expected_Result in result.upper():
                                                                                                                                print "QAMSource channel change play successful"
                                                                                                                                #tdkTestObj.setResultStatus(result);
                                                                                                                                src_parameter=["rmfElement","newQamSrc","numOfTimeChannelChange"]
                                                                                                                                src_element=["QAMSrc","true",index]
                                                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                                                                                                if expected_Result in result.upper():
                                                                                                                                        time.sleep(5);
                                                                                                                                        print "QAMSource channel change pause successful"
                                                                                                                                        #tdkTestObj.setResultStatus(result);

                                                                                                #src_parameter=["rmfElement","factoryEnable","newQamSrc"]
                                                                                                #src_element=["QAMSrc","true","true"]
                                                                                                #result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                                                                                #increament index
                                                                                                print "index value",index
                                                                                                index = index + 1
                                                                                        else:
                                                                                                print "QAMSource pause failed"
                                                                                                #tdkTestObj.setResultStatus(failure);
                                                                                index = 0
                                                                                while index < numOfTimesChannelChange:
                                                                                        src_parameter=["rmfElement","factoryEnable","newQamSrc","numOfTimeChannelChange"]
                                                                                        src_element=["QAMSrc","true","true",index]
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                                                                        print "index value",index
                                                                                        index = index + 1
                                                                        else:
                                                                                print "QAMSource play failed"
                                                                                tdkTestObj.setResultStatus(failure);

                                                                #src_parameter=["rmfElement"]
                                                                #src_element=["QAMSrc"]
                                                                #result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,expected_Result,src_parameter,src_element);
                                                src_parameter=["rmfElement"]
                                                src_element=["MPSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["MPSink"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                                src_parameter=["rmfElement","factoryEnable"]
                                src_element=["QAMSrc","true"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                        src_parameter=[];
                        src_element=[];
                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_UninitPlatform',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Uninit',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_CheckFor_SPTSReadError',obj,failure,src_parameter,src_element);
                if expected_Result in result.upper():
                        tdkTestObj.setResultStatus(failure);
                else:
                        tdkTestObj.setResultStatus(expected_Result);
        else:
                print "Status of RmfElement_QAMSrc_RmfPlatform_Init:  %s" %loadModuleStatus;
        obj.initiateReboot();
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");