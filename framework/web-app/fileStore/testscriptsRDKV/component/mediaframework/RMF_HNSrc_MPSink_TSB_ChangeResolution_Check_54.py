# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2016 RDK Management, LLC. All rights reserved.
# ============================================================================
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id>1653</id>
  <version>1</version>
  <name>RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54</name>
  <primitive_test_id>494</primitive_test_id>
  <primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Objective: RMF_HNSRC_MPSink – Set the video resolution to 1080p. Then tune to any channel with tsb and pause for 30 mins to get buffer content.
Test CaseID: CT_RMF_HNSRC_MPSink_54</synopsis>
  <groups_id/>
  <execution_time>18</execution_time>
  <long_duration>false</long_duration>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>Terminal-RNG</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_RMF_HNSRC_MPSink_54</test_case_id>
    <test_objective>RMF_HNSRC_MPSink – Set the video resolution to 1080p. Then tune to any channel with tsb and pause for 5 mins to get buffer content. Start playing for few seconds and change the video resolution to 480p and see the check the media time. And make sure media time must remain in the same point and should not change to live point.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1</test_setup>
    <pre_requisite>Box and TV must be connected with HDMI cable.</pre_requisite>
    <api_or_interface_used>HNSrc init()
HNSrc open()
MPSink init()
MPSink SetVideoRectangle()
MPSink SetSource()
Manager::Initialize()
DS set video resolution() 
DS get video resolution()
Manager::DeInitialize()
HNSrc play()
HNSrc getState()
HNSrc SetMediaTime()
HNSrc GetMediaTime()
HNSrc GetSpeed()
HNSrc close()
MPSink term()
HNSrc term()</api_or_interface_used>
    <input_parameters>init: None
open:Char *,Char *
play:None
GetState:RMFState
SetMediaTime: double mediatime
GetMediaTime: double mediatime
GetSpeed: None.
SetVideoRectangle: unsigned.
unsigned, unsigned, 
Unsigned, bool apply_now – x,y,h,w,false
setSource: RMFMediaSourceBase*
close:None
term:None</input_parameters>
    <automation_approch>1.TM loads mediaframework agent and devicesetting agent via the test agent.
2. DeviceSetting agent will call DS_ManagerInitialize to setResolution.
3. DeviceSetting agent will call DS_Resolution to fetch the resolution supported based on which we will call the DS_SetResolution to set the resolution value 1080p.
4. DeviceSetting agent will call DS_ManagerDeInitialize
5.Mediaframework agent will create the instance for Hnsrc and  initialize the Hnsrc element.
6.Mediaframework agent will create the instance for Mpsink and initialize the Mpsink element.
7. Form the pipeline Hnsrc-&gt;Mpsink using set source ().
8. DeviceSetting agent will call the setResolution() to set the resolution to 1080p and  check to verify the resolution is set.
9.Mediaframework agent will open and play the  Hnsrc element.
10. Mediaframework agent will call pause for 5 mins to get buffer content.
11. Mediaframework agent will call play to playback the buffer content for few mins.
12. DeviceSetting agent will call DS_ManagerInitialize to setResolution.
13. DeviceSetting agent will call DS_Resolution to fetch the resolution supported based on which we will call the DS_SetResolution to set the resolution value 480p.
14. DeviceSetting agent will call DS_ManagerDeInitialize.
15. Mediaframework agent will call getMediaTime to check the mediaposition is not changed to the live point.
16.Mediaframework agent will terminate the Hnsrc element .
17.For each API called in the script, mediaframework agent  will send SUCCESS or FAILURE status to Test Agent by comparing the return vale of APIs.</automation_approch>
    <except_output>Checkpoint 1.Check the return value of API for success status.
CheckPoint 2. Verify the media position. Check the Audio and Video quality using CheckAudioStatus.sh and CheckVideoStatus.sh scripts.</except_output>
    <priority>High</priority>
    <test_stub_interface>libmediaframeworkstub.so
libdevicesettingsstub.so</test_stub_interface>
    <test_script>RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54</test_script>
    <skipped>No</skipped>
    <release_version>M21</release_version>
    <remarks>none</remarks>
  </test_cases>
</xml>

'''
import tdklib;
import mediaframework;
import time;
import devicesettings;

src_element=["HNSrc"]
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
	if "SUCCESS" in result.upper():
	        Mediatime=details.split(":");
		print Mediatime[1];
    return result

ds_obj = tdklib.TDKScriptingLibrary("devicesettings","2.0");
ds_obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54');
#Get the result of connection with test component and STB
dsLoadModuleStatus = ds_obj.getLoadModuleResult();
print "DeviceSetting Load Module Status :  %s" %dsLoadModuleStatus;

if "FAILURE" in dsLoadModuleStatus.upper():
        print "DeviceSetting Load Module Failed"
        ds_obj.setLoadModuleStatus("FAILURE");
	exit()
else:
	displayConnected = 0
	result = devicesettings.dsManagerInitialize(ds_obj)
        if "SUCCESS" in result.upper():
		#Calling DS_IsDisplayConnectedStatus function to check for display connection status
		result = devicesettings.dsIsDisplayConnected(ds_obj)
		if "TRUE" in result:
			displayConnected = 1
		result = devicesettings.dsManagerDeInitialize(ds_obj)	

	if 0 == displayConnected:
		print "ERROR: HDMI display device not connected to execute the test!"
		exit()

mediaframework_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
mediaframework_obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54');
#Get the result of connection with test component and STB
mfLoadModuleStatus = mediaframework_obj.getLoadModuleResult();
print "Mediaframework Load Module Status :  %s" %mfLoadModuleStatus;
loadmoduledetails = mediaframework_obj.getLoadModuleDetails();
print "Load Module Details : %s" %loadmoduledetails;

if "FAILURE" in mfLoadModuleStatus.upper():
        if "RMF_STREAMER_NOT_RUNNING" in loadmoduledetails:
                print "rmfStreamer is not running. Rebooting STB"
                mediaframework_obj.initiateReboot();
                #Reload Test component to be tested
                mediaframework_obj = tdklib.TDKScriptingLibrary("mediaframework","2.0");
                mediaframework_obj.configureTestCase(ip,port,'RMF_HNSrc_MPSink_TSB_ChangeResolution_Check_54');
                #Get the result of connection with test component and STB
                mfLoadModuleStatus = mediaframework_obj.getLoadModuleResult();
                print "Re-Load Module Status :  %s" %mfLoadModuleStatus;
                loadmoduledetails = mediaframework_obj.getLoadModuleDetails();
                print "Re-Load Module Details : %s" %loadmoduledetails;

if "SUCCESS" in mfLoadModuleStatus.upper() and "SUCCESS" in dsLoadModuleStatus.upper():

	result = devicesettings.dsManagerInitialize(ds_obj);
        if "SUCCESS" in result.upper():
                #Check and get the resolution list supported by TV.
		print "Get list of resolutions supported on HDMI0"

        	#Primitive test case which associated to this Script
        	tdkTestObj = ds_obj.createTestStep('DS_Resolution');
		portName="HDMI0"
		tdkTestObj.addParameter("port_name",portName);
		expectedresult = "SUCCESS"
        	#Execute the test case in STB
        	tdkTestObj.executeTestCase(expectedresult);
        	#Get the result of execution
        	result = tdkTestObj.getResult();
        	supportedResolutions = tdkTestObj.getResultDetails();
        	print "PortName: [%s] Result: [%s] Details: [%s]"%(portName,result,supportedResolutions)
        	#Set the result status of execution
        	if expectedresult in result:
                	tdkTestObj.setResultStatus("SUCCESS");
        	else:
                	tdkTestObj.setResultStatus("FAILURE");

                print "Get current resolution value"
		getResolution = devicesettings.dsGetResolution(ds_obj,"SUCCESS",kwargs={'portName':"HDMI0"});

		setResolution="1080p30";
		print "Set Resolution value to %s" %setResolution;
                # Check if current value is already 1080p30
                if setResolution == getResolution:
			print "Resolution value already at %s"%setResolution
		elif setResolution not in supportedResolutions:
			print "Resolution not supported on HDMI0"
		else:
                        devicesettings.dsSetResolution(ds_obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':setResolution});

		result = devicesettings.dsManagerDeInitialize(ds_obj)
        else:
                print "DSManager Initialization failed."

        time.sleep(2)

        #Creating the Hnsrc instance
        result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance', mediaframework_obj,"SUCCESS",src_parameter,src_element);
        if "SUCCESS" in result.upper():
                #Creating the MPSink instance
                result=Create_and_ExecuteTestStep('RMF_Element_Create_Instance',mediaframework_obj,"SUCCESS",sink_parameter,sink_element);
                if "SUCCESS" in result.upper():
                        #Initiazing the Hnsrc Element
                        result=Create_and_ExecuteTestStep('RMF_Element_Init',mediaframework_obj,"SUCCESS",src_parameter,src_element);
                        if "SUCCESS" in result.upper():
                                 #Initiazing the MPSink Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Init',mediaframework_obj,"SUCCESS",sink_parameter,sink_element);
                                if "SUCCESS" in result.upper():
                                        #Opening the Hnsrc Element with playurl
                                        result=Create_and_ExecuteTestStep('RMF_Element_Open', mediaframework_obj,"SUCCESS",open_parameter_name,open_parameter_value);
                                        if "SUCCESS" in result.upper():
                                                #Setting the MPSink Element with x,y co-ordiantes
                                                result=Create_and_ExecuteTestStep('RMF_Element_MpSink_SetVideoRectangle', mediaframework_obj,"SUCCESS",videorec_parameter_name,videorec_parameter_value);
                                                if "SUCCESS" in result.upper():
                                                        #Selecting the source for MPSink
                                                        result=Create_and_ExecuteTestStep('RMF_Element_Sink_SetSource', mediaframework_obj,"SUCCESS",setsource_parameter_name,setsource_parameter_value);
                                                        if "SUCCESS" in result.upper():
                                                                #Play the HNSRC-->MPSINK pipeline
                                                                result=Create_and_ExecuteTestStep('RMF_Element_Play', mediaframework_obj,"SUCCESS",play_parameter_name,play_parameter_value);
                                                                if "SUCCESS" in result.upper():
                                                                        time.sleep(15)

                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["CheckAudioStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                        print "Audio check Done. Status: ",result;

                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                        print "Video check Done. Status: ",result;

                                                                        #Pause the HNSRC-->MPSINK pipeline
									print "Pause for 2 mins"
                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Pause', mediaframework_obj,"SUCCESS",src_parameter,src_element);
                                                                        if "SUCCESS" in result.upper():
                                                                                #Get the Mediatime value
										time.sleep(120);
                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Getmediatime', mediaframework_obj,"SUCCESS",src_parameter,src_element);
                                                                                if "SUCCESS" in result.upper():

                                                                                        #Play the HNSRC-->MPSINK pipeline
                                                                                        result=Create_and_ExecuteTestStep('RMF_Element_Play', mediaframework_obj,"SUCCESS",play_parameter_name,play_parameter_value);
                                                                                        if "SUCCESS" in result.upper():
                                                                                                time.sleep(10);

                                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                                checkStatusFor=["CheckAudioStatus.sh"]
                                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                                                print "Audio check Done. Status: ",result;

                                                                                                checkStatusParameter=["audioVideoStatus"]
                                                                                                checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                                                print "Video check Done. Status: ",result;

												result = devicesettings.dsManagerInitialize(ds_obj)
                                                                                                if "SUCCESS" in result.upper():
                                                                                                        setResolution="480p";
                                                                                                        print "Set resolution value to %s" %setResolution;

                                                                                                        #if Present then set the resolution.
                                                                                                        if setResolution in supportedResolutions:
														print "Resolution supported on HDMI0"
														result = devicesettings.dsSetResolution(ds_obj,"SUCCESS",kwargs={'portName':"HDMI0",'resolution':setResolution});
                                                                                                                if "SUCCESS" in result.upper():
                                                                                                                        time.sleep(2);
                                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                                        checkStatusFor=["CheckAudioStatus.sh"]
                                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                                                                        print "Audio check Done. Status: ",result;

                                                                                                                        checkStatusParameter=["audioVideoStatus"]
                                                                                                                        checkStatusFor=["CheckVideoStatus.sh"]
                                                                                                                        result=Create_and_ExecuteTestStep('CheckAudioVideoStatus', mediaframework_obj,"SUCCESS",checkStatusParameter,checkStatusFor);
                                                                                                                        print "Video check Done. Status: ",result;
                                                                                                        else:
                                                                                                                print "Resolution not supported on HDMI0"

                                                                                                        result = devicesettings.dsManagerDeInitialize(ds_obj)

                                                                                                #Pause the HNSRC-->MPSINK pipeline
                                                                                                result=Create_and_ExecuteTestStep('RMF_Element_Pause', mediaframework_obj,"SUCCESS",src_parameter,src_element);

                                                #Close the Hnsrc Element
                                                result=Create_and_ExecuteTestStep('RMF_Element_Close', mediaframework_obj,"SUCCESS",src_parameter,src_element);
                                        #Terminating the MPSink Element
                                        result=Create_and_ExecuteTestStep('RMF_Element_Term', mediaframework_obj,"SUCCESS",sink_parameter,sink_element);
                                #Terminating the HNSrc Element
                                result=Create_and_ExecuteTestStep('RMF_Element_Term', mediaframework_obj,"SUCCESS",src_parameter,src_element);
                #Removing the HNSrc Element Instances
                result=Create_and_ExecuteTestStep('RMF_Element_Remove_Instance', mediaframework_obj,"SUCCESS",src_parameter,src_element);
                time.sleep(5);
        else:
                print "Status of RMF_Element_Create_Instance:  %s" %loadModuleStatus;

        mediaframework_obj.unloadModule("mediaframework");
        ds_obj.unloadModule("devicesettings");
else:
        print "Load Module Failed"
        mediaframework_obj.setLoadModuleStatus("FAILURE");
        ds_obj.setLoadModuleStatus("FAILURE");
