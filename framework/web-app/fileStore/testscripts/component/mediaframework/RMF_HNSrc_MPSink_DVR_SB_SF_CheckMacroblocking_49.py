'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1646</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_MPSink_DVR_SB_SF_CheckMacroblocking_49</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: RMF_HNSRC_MPSink –  Do Skip back and front on the recorded (DVR) content and make sure no freeze/erratic behaviour on doing the trickplays.
Test CaseID: CT_RMF_HNSRC_MPSink_49
Test Type: Positive.</synopsis>
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
import tdklib;
import time;

src_element=["HNSrc"]
Expected_Result="SUCCESS"
src_parameter=["rmfElement"]
sink_element=["MPSink"]
sink_parameter=["rmfElement"]
open_parameter_name=["rmfElement","url"]
open_parameter_value=["HNSrc"]
play_parameter_name=["rmfElement","defaultPlay","playTime","playSpeed"]
play_parameter_value=["HNSrc",0,0.0,1.0]
videorec_parameter_name=["X","Y","width","apply","height"]
videorec_parameter_value=[0,0,1280,0,720]
setsource_parameter_name=["rmfSourceElement","rmfSinkElement"]
setsource_parameter_value=["HNSrc","MPSink"]

ip = <ipaddress>
port = <port>

obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_DVR_SB_SF_CheckMacroblocking_49');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):

    #Primitive test case which associated to this Script
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        recordingObj = tdkTestObj.getRecordingDetails();
        num = recordingObj.getTotalRecordings();
        print "Number of recordings: %d"%num
        recordID = recordingObj.getRecordingId(num - 1);
        url = 'http://' + streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id='+recordID[:-1];
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);
    for item in range(len(parametername)):
        tdkTestObj.addParameter(parametername[item],parametervalue[item]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    print "Status of "+ teststep+":  %s" %result;
    details = tdkTestObj.getResultDetails();
    print "[TEST EXCEUTION DETAILS] : %s"%details;
    return result

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print "Load Module Status :  %s" %loadModuleStatus;

if Expected_Result in loadModuleStatus.upper():
        #Prmitive test case which associated to this Script
        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',obj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',obj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open',obj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle',obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource',obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play',obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        time.sleep(30)
                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["/opt/TDK/CheckAudioStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                        print "Audio check Done. Status: ",result;

                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["/opt/TDK/CheckVideoStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                        print "Video check Done. Status: ",result;

                                                                        result=Create_and_ExecuteTestStep('RMF_Element_GetState',obj,Expected_Result,src_parameter,src_element);
                                                                        mediatime_parameter_name=["mediaTime","rmfElement"]
                                                                        mediatime_parameter_value=[-10,"HNSrc"]
                                                                        #Skip backward 10 secs
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Setmediatime',obj,Expected_Result,mediatime_parameter_name,mediatime_parameter_value);
                                                                        if Expected_Result in result.upper():

                                                                                time.sleep(5)
                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                checkStatusFor=["/opt/TDK/CheckAudioStatus.sh"]
                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                print "Audio check Done. Status: ",result;

                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                checkStatusFor=["/opt/TDK/CheckVideoStatus.sh"]
                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                print "Video check Done. Status: ",result;

                                                                                mediatime_parameter_name=["mediaTime","rmfElement"]
                                                                                mediatime_parameter_value=[10,"HNSrc"]
                                                                                #Skip forward 10 secs
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Setmediatime',obj,Expected_Result,mediatime_parameter_name,mediatime_parameter_value);
                                                                                if Expected_Result in result.upper():

                                                                                        time.sleep(5) 
                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                        checkStatusFor=["/opt/TDK/CheckAudioStatus.sh"]
                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                        print "Audio check Done. Status: ",result;

                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                        checkStatusFor=["/opt/TDK/CheckVideoStatus.sh"]
                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus',obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                        print "Video check Done. Status: ",result;


                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause',obj,Expected_Result,src_parameter,src_element);
                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close',obj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term',obj,Expected_Result,src_parameter,src_element);
                        #Removing the MPSink Element Instances
                        result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,sink_parameter,sink_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance',obj,Expected_Result,src_parameter,src_element);
                time.sleep(5);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        obj.unloadModule("mediaframework");
else:
        print "Load Module Failed"
        obj.setLoadModuleStatus("FAILURE");