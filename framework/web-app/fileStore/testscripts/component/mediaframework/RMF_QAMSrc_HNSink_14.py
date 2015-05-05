'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1165</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_QAMSrc_HNSink_14</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>RMF_QAMSrc – To Stream out the live content through HNSink on to the network when factory method flag is set to false but set invalid streaingIp.
Test Case ID: CT_RMF_QAMSrc_HNSink_14
Test Type: Negative</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks>HNSink Api setHNSinkProperties() failing with segmentation fault. Need to raise the RDKTT ticket.</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
  <!--  -->
  <box_types>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Emulator-HYB</box_type>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_QAMSrc_HNSink_14');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    global details
    global tdkTestObj
    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Open':
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        ocapLocator = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(ocapLocator);
        print "OcapLocator:",ocapLocator

    if teststep == 'RmfElement_HNSink_SetProperties':
        #Stream details for tuning
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = "ocap://"+streamDetails.getOCAPID();
        parametername.append("url");
        parametervalue.append(url);
        print "hnsink url:",url

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if teststep != 'RMF_Element_GetState':
       tdkTestObj.setResultStatus(result);

    print "[Execution Result]:  %s" %result;
    print "[Execution Details]:  %s" %details;

    return result

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;

if expected_Result in loadModuleStatus.upper():
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
                        src_element=["QAMSrc","false"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["QAMSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                if expected_Result in result.upper():
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,expected_Result,src_parameter,src_element);
                                        if expected_Result in result.upper():
                                                src_parameter=["rmfElement"]
                                                src_element=["HNSink"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
                                                if expected_Result in result.upper():
                                                        src_parameter=[]
                                                        src_element=[]
                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_InitPlatform',obj,expected_Result,src_parameter,src_element);
                                                        if expected_Result in result.upper():
                                                                src_parameter=["rmfElement"]
                                                                src_element=["HNSink"]
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                                                                if expected_Result in result.upper():
                                                                        src_parameter=["dctpEnable","typeFlag","streamIp"]
                                                                        src_element=["false",1,"168.23.14.11"]
                                                                        result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetProperties',obj,expected_Result,src_parameter,src_element);
                                                                        if expected_Result in result.upper():
                                                                                src_parameter=["rmfElement"]
                                                                                src_element=["QAM_SRC"]
                                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_SetSourceType',obj,expected_Result,src_parameter,src_element);
                                                                                if expected_Result in result.upper():
                                                                                        src_parameter=["rmfSourceElement","rmfSinkElement"]
                                                                                        src_element=["QAMSrc","HNSink"]
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
                                                                                                        if expected_Result in result.upper() and "PLAYING" in details.upper():
                                                                                                                print "QAMSource play successful"
                                                                                                                tdkTestObj.setResultStatus(result);
                                                                                                        else:
                                                                                                                print "QAMSource play failed"
                                                                                                                tdkTestObj.setResultStatus(failure);
                                                                        src_parameter=["rmfElement"]
                                                                        src_element=["HNSink"]
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                                                src_parameter=[]
                                                                src_element=[]
                                                                result=Create_and_ExecuteTestStep('RmfElement_HNSink_UninitPlatform',obj,expected_Result,src_parameter,src_element);
                                                src_parameter=["rmfElement"]
                                                src_element=["QAMSrc"]
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                                        src_parameter=["rmfElement"]
                                        src_element=["QAMSrc"]
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                                src_parameter=["rmfElement","factoryEnable"]
                                src_element=["QAMSrc","false"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
                        src_parameter=[];
                        src_element=[];
                        result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_UninitPlatform',obj,expected_Result,src_parameter,src_element);
                src_parameter=[];
                src_element=[];
                result=Create_and_ExecuteTestStep('RmfElement_QAMSrc_RmfPlatform_Uninit',obj,expected_Result,src_parameter,src_element);
        else:
                print "Status of RmfElement_QAMSrc_RmfPlatform_Init:  %s" %loadModuleStatus;
        obj.initiateReboot();
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");