'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>856</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_DVRSrc_Open_15</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>This script tests the RDK Mediaframework DVRSrc element to call Open API with valid url being framed with segmentName and Close a DVRsource element.
Test Case ID: CT_RMF_DVRSrc_15.
Test Type: Positive.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>8</execution_time>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RMF_DVRSrc_Open_15');

expected_Result="SUCCESS"

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);

    if teststep == 'RMF_Element_Open':
        recordingObj = tdkTestObj.getRecordingDetails();
        num = recordingObj.getTotalRecordings();
        print "Number of recordings: %d"%num
        recordID = recordingObj.getRecordingId(num - 1);
        print "RecordId:",recordID;
        parametername.append("url");
        segName = recordingObj.getSegmentName(num - 1);
        print "segName:",segName
        dvrSegName = "dvr://local/" + str(segName)
        print dvrSegName
        parametervalue.append(dvrSegName);

    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
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
        src_parameter=["rmfElement"]
        src_element=["DVRSrc"]
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,expected_Result,src_parameter,src_element);
        if expected_Result in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,expected_Result,src_parameter,src_element);
                if expected_Result in result.upper():
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,expected_Result,src_parameter,src_element);
                        if expected_Result in result.upper():
                                src_parameter=["rmfElement"]
                                src_element=["DVRSrc"]
                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,expected_Result,src_parameter,src_element);
                        src_parameter=["rmfElement"]
                        src_element=["DVRSrc"]
                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,expected_Result,src_parameter,src_element);
                src_parameter=["rmfElement"]
                src_element=["DVRSrc"]
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,expected_Result,src_parameter,src_element);
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");