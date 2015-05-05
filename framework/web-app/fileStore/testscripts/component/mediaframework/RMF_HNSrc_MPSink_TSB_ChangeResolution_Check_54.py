'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id>1653</id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54</name>
  <!-- If you are adding a new script you can specify the script name. -->
  <primitive_test_id>494</primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Objective: RMF_HNSRC_MPSink – Set the video resolution to 1080p. Then tune to any channel with tsb and pause for 30 mins to get buffer content.
Test CaseID: CT_RMF_HNSRC_MPSink_54</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <box_type>Terminal-RNG</box_type>
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
ds_mgr_name=[""]
ds_mgr_value=[""]


ip = <ipaddress>
port = <port>

mediaframework_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
ds_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");

mediaframework_obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54');
ds_obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54');

def Create_and_ExecuteTestStep(teststep, testobject, expectedresult,parametername, parametervalue):
    #Primitive test case which associated to this Script
    global Mediatime
    global tdkTestObj
    global Mediaspeed
    tdkTestObj =testobject.createTestStep(teststep);
    if teststep == "RMF_Element_Open":
        streamDetails = tdkTestObj.getStreamDetails('01');
        url = mediaframework.getStreamingURL("TSB" , streamDetails.getGatewayIp() , streamDetails.getOCAPID());
        if url == "NULL":
            print "Failed to generate the Streaming URL";
            tdkTestObj.setResultStatus("FAILURE");
            return "FAILURE" ;
        print "PLAY URL : %s" %url;
        open_parameter_value.append(url);

    if teststep != "DS_ManagerInitialize" and teststep != "DS_ManagerDeInitialize":
        for item in range(len(parametername)):
                tdkTestObj.addParameter(parametername[item],parametervalue[item]);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    tdkTestObj.setResultStatus(result);
    details = tdkTestObj.getResultDetails();
    print "Status of "+ teststep+":  %s" %result;
    print "Details of "+ teststep+":  %s" %details;
    if teststep == "RMF_Element_Getmediatime":
        Mediatime=details.split(":");
        print Mediatime[1];
    if teststep == "RMF_Element_Getspeed":
        Mediaspeed=details.split(":");
        print Mediaspeed[1];

    return result

def Create_ExecuteTestcase(obj,primitivetest,expectedresult,verifyList,**kwargs):
    print kwargs
    details = "NULL";

    print "Entering Create_ExecuteTestcase --->"
    #calling primitive test case
    tdkTestObj = obj.createTestStep(primitivetest);
    for name, value in kwargs.iteritems():

        print "Name: %s"%str(name);
        tdkTestObj.addParameter(str(name),value);

    Expectedresult=expectedresult;
    tdkTestObj.executeTestCase(Expectedresult);
    actualresult = tdkTestObj.getResult();
    print "Actual Result: %s"%actualresult;

    try:
        details = tdkTestObj.getResultDetails();
        print "Details: %s"%details;
    except:
        pass;

    print "Existing Create_ExecuteTestcase --->"
    #Check for SUCCESS/FAILURE return value
    if Expectedresult in actualresult:
        count = 0;
        if verifyList:
            for name,value in verifyList.items():
                print "Name:%s,Value:%s to be verified in the details"%(name,value);
                if value in details:
                    print details;
                    print "SUCCESS : %s sucess"%primitivetest;
                    count+=1;
                    if count > 0:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS:%s"%(primitivetest);
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Value not in details %s" %details;
        else:
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    return (actualresult,tdkTestObj,details);



#Get the result of connection with test component and STB
mfLoadModuleStatus = mediaframework_obj.getLoadModuleResult();
print "Mediaframework Load Module Status :  %s" %mfLoadModuleStatus;

dsLoadModuleStatus = ds_obj.getLoadModuleResult();
print "DeviceSetting Load Module Status :  %s" %dsLoadModuleStatus;

if Expected_Result in mfLoadModuleStatus.upper() and Expected_Result in dsLoadModuleStatus.upper():

        #Set the resolution to 1080p if supported.
        result=Create_and_ExecuteTestStep('DS_ManagerInitialize',ds_obj,Expected_Result,ds_mgr_name,ds_mgr_value);
        if Expected_Result in result.upper():
                print ""
                print "Manager Initialization Done";

                #Check and get the resolution list supported by TV.
                actualresult1,tdkTestObj_dev1,resolutiondetails = Create_ExecuteTestcase(ds_obj,'DS_Resolution', 'SUCCESS', verifyList ={},port_name = "HDMI0");
                setresolution="1080p30";
                print "1080p Resolution value set to:%s" %setresolution;

                #if Present then set the resolution.
                if setresolution in resolutiondetails:
                        print "Found the resolution value in the list"
                        ds_parameter_name=["resolution","port_name","get_only"]
                        ds_parameter_value=[setresolution,"HDMI0",0]
                        result=Create_and_ExecuteTestStep('DS_SetResolution',ds_obj,Expected_Result,ds_parameter_name,ds_parameter_value);
                        if Expected_Result in result.upper():
                                print "DS Resolution Success"

                result=Create_and_ExecuteTestStep('DS_ManagerDeInitialize',ds_obj,Expected_Result,ds_mgr_name,ds_mgr_value);
                if Expected_Result in result.upper():
                        print "Manager Deinitization Done"
                        print ""
        else:
                print "Resolution 1080p not set, DS_ManagerInitialize failed."

        time.sleep(5)
        #Prmitive test case which associated to this Script
        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance', mediaframework_obj,Expected_Result,src_parameter,src_element);
        if Expected_Result in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mediaframework_obj,Expected_Result,sink_parameter,sink_element);
                if Expected_Result in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',mediaframework_obj,Expected_Result,src_parameter,src_element);
                        if Expected_Result in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',mediaframework_obj,Expected_Result,sink_parameter,sink_element);
                                if Expected_Result in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open', mediaframework_obj,Expected_Result,open_parameter_name,open_parameter_value);
                                        if Expected_Result in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle', mediaframework_obj,Expected_Result,videorec_parameter_name,videorec_parameter_value);
                                                if Expected_Result in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource', mediaframework_obj,Expected_Result,setsource_parameter_name,setsource_parameter_value);
                                                        if Expected_Result in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play', mediaframework_obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                if Expected_Result in result.upper():
                                                                        time.sleep(15)


                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["CheckAudioStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                        print "Audio check Done. Status: ",result;

                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                        print "Video check Done. Status: ",result;

                                                                        #Pause the HNSRC-->MPSINK pipeline
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause', mediaframework_obj,Expected_Result,src_parameter,src_element);
                                                                        if Expected_Result in result.upper():
                                                                                #Get the Mediatime value
                                                                                time.sleep(300);
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime', mediaframework_obj,Expected_Result,src_parameter,src_element);
                                                                                if Expected_Result in result.upper():

                                                                                        #Play the HNSRC-->MPSINK pipeline
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play', mediaframework_obj,Expected_Result,play_parameter_name,play_parameter_value);
                                                                                        if Expected_Result in result.upper():
                                                                                                time.sleep(10);                                                         

                                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                                checkStatusFor=["CheckAudioStatus.sh"]
                                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                                print "Audio check Done. Status: ",result;

                                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                                checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                                                print "Video check Done. Status: ",result;

                                                                                                result=Create_and_ExecuteTestStep('DS_ManagerInitialize',ds_obj,Expected_Result,ds_mgr_name,ds_mgr_value);
                                                                                                if Expected_Result in result.upper():
                                                                                                        print ""
                                                                                                        print "Manager Initialization Done";

                                                                                                        #Check and get the resolution list supported by TV.
                                                                                                        actualresult1,tdkTestObj_dev1,resolutiondetails = Create_ExecuteTestcase(ds_obj,'DS_Resolution', 'SUCCESS', verifyList ={},port_name = "HDMI0");
                                                                                                        setresolution="480p";
                                                                                                        print "Resolution value set to:%s" %setresolution;

                                                                                                        #if Present then set the resolution.
                                                                                                        if setresolution in resolutiondetails:
                                                                                                                print "Found the resolution value in the list"
                                                                                                                ds_parameter_name=["resolution","port_name","get_only"]
                                                                                                                ds_parameter_value=[setresolution,"HDMI0",0]
                                                                                                                result=Create_and_ExecuteTestStep('DS_SetResolution',ds_obj,Expected_Result,ds_parameter_name,ds_parameter_value);
                                                                                                                if Expected_Result in result.upper():
                                                                                                                        result=Create_and_ExecuteTestStep('DS_ManagerDeInitialize',ds_obj,Expected_Result,ds_mgr_name,ds_mgr_value);
                                                                                                                        print "Manager Deinitization Done"
                                                                                                                        print ""

                                                                                                                if Expected_Result in result.upper():
                                                                                                                        time.sleep(5);


                                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                                        checkStatusFor=["CheckAudioStatus.sh"]
                                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);
                                                                                                                        print "Audio check Done. Status: ",result;

                                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,Expected_Result,checkStatusParameter,checkStatusFor);

                                                                                                                        print "Video check Done. Status: ",result;

                                                                                                #Pause the HNSRC-->MPSINK pipeline
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause', mediaframework_obj,Expected_Result,src_parameter,src_element);

                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close', mediaframework_obj,Expected_Result,src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term', mediaframework_obj,Expected_Result,sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term', mediaframework_obj,Expected_Result,src_parameter,src_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance', mediaframework_obj,Expected_Result,src_parameter,src_element);
                time.sleep(5);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;
        mediaframework_obj.unloadModule("mediaframework");
        ds_obj.unloadModule("devicesettings");
else:
        print "Load Module Failed"
        mediaframework_obj.setLoadModuleStatus("FAILURE");
        ds_obj.setLoadModuleStatus("FAILURE");