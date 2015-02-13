'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>908</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_SetGetSpeed_02</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>495</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Init</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>ALLOCATED</status>
  <!--  -->
  <synopsis>These Script tests the RDK Mediaframework HNSrc element to set and get speed.
Test Case ID: CT_RMF_HNSrc_02.</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
</xml>
'''
import tdklib;
import mediaframework;
src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
speed_parameter_name=["playSpeed","rmfElement"]
speed_parameter_value=[1.0,"HNSrc"]
ip = <ipaddress>
port = <port>
obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSRC_Setspeed_Getspeed_02');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
        print "RMF_Element_Init status:  %s" %parametername[item];
        
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    return result

if Expected_Result in loadModuleStatus.upper():

        #Prmitive test case which associated to this Script
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Init status:  %s" %result;
                if Expected_Result in result.upper():
                        result=Create_and_ExecuteTestStep('RMF_Element_Setspeed',obj,Expected_Result,speed_parameter_name,speed_parameter_value);
                        print "RMF_Element_Setspeed status:  %s" %result;
                        if Expected_Result in result.upper():
                                result=Create_and_ExecuteTestStep('RMF_Element_Getspeed',obj,Expected_Result,src_parameter,src_element);
                                print "RMF_Element_Getspeed status:  %s" %result;
                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Term status:  %s" %result;
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                print "RMF_Element_Term status:  %s" %result;
        else:
		                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");