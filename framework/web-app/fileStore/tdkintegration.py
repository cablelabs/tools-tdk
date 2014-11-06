#!/usr/bin/python

#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2013 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;
import re;
import random;
import time;

#Number of times the pause/play should repeat.
skipNumOfSec = 30;

#Number of repeatation
repeatCount = 1;

# To initiate a recording in the Gateway box using rmfapp
#
# Syntax       : sched_rec(obj,streamID,starttime,duration)
#
# Parameters   : obj,streamID,starttime,duration               
#
# Return Value : 0 on success and 1 on failure

def sched_rec(obj,streamID,starttime,duration):
    
    time.sleep(float(starttime));
    print "Start Time %s"%starttime

    print "Duration%s"%duration

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TdkRmfApp_CreateRecording');

    streamDetails = tdkTestObj.getStreamDetails(streamID);

    rec_id = random.randint(10000, 500000);
    recordid = str(rec_id);
    recordduration = int(duration)/60000;
    ocapid = streamDetails.getOCAPID();
    recordtitle = "test_dvr_"+recordid

    print "Record ID: %s"%recordid
    print "Record Duration : %d minute"%recordduration
    print "Record Title : %s"%recordtitle
    print "Ocap ID : %s"%ocapid

    tdkTestObj.addParameter("recordId",str(recordid));
    tdkTestObj.addParameter("recordDuration",str(recordduration));
    tdkTestObj.addParameter("recordTitle",str(recordtitle));
    tdkTestObj.addParameter("ocapId",ocapid);

    expectedresult="SUCCESS"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();

    if expectedresult in result:
        tdkTestObj.setResultStatus("SUCCESS");
        details=tdkTestObj.getResultDetails();
    else:
        tdkTestObj.setResultStatus("FAILURE");
        details=tdkTestObj.getResultDetails();


    return (result,recordid);


#The below procedure is not used as there are some issue in the Recorder module 

'''
def sched_rec(streamID,starttime,duration):

    #Test component to be tested
    obj = tdklib.TDKScriptingLibrary("Recorder","2.0");
    
    #Get the result of connection with test component and STB
    loadmodulestatus =obj.getLoadModuleResult();
    print "Recorder module loading status :%s" %loadmodulestatus ;
    #Check for SUCCESS/FAILURE of Recorder module
    if "SUCCESS" in loadmodulestatus.upper():

        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        obj.initiateReboot();
        
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('Recorder_ScheduleRecording');
        
        rec_id = random.randint(10000, 500000);
        recording_id = str(rec_id);
        duration = duration;
        print "Duration: %s"%duration;			
        print "Satrt time %s"%starttime;
        start_time = starttime;    
        utctime=tdkTestObj.getUTCTime();
        tdkTestObj.addParameter("UTCTime",utctime);
        tdkTestObj.addParameter("Duration",duration);
        tdkTestObj.addParameter("Recording_Id",recording_id);
        tdkTestObj.addParameter("Start_time",start_time);
        streamDetails = tdkTestObj.getStreamDetails(streamID);
        #Adding ocapid parameter
        validid = streamDetails.getOCAPID();
        Id = re.search(r"\w\w\w\w",validid);
        if Id:
            print "ocapid : %s" %validid;
            tdkTestObj.addParameter("Source_id",validid);
            #Execute the test case in STB
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            #Get the Actual result of streaming Interface
            actualresult = tdkTestObj.getResult();
            Jsonurldetails = tdkTestObj.getResultDetails();
            print "Result of scheduling : %s" %actualresult;
            print "Jsonurldetails is : %s" %Jsonurldetails;
            RequestURL = Jsonurldetails.replace("\\","");
            print "RequestURL  is : %s" %RequestURL ;
            #compare the actual result with expected result
            if expectedresult in actualresult:
                status_expected = "acknowledgement";
                print "Recorder received the requested recording url";
                time.sleep(30);
                status_actual =tdkTestObj.initiateRecorderApp(RequestURL);
                print "Status string is: %s"%status_actual;
                if status_expected in status_actual:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "TDK_Server received the Json Message";
                    #Prmitive test case which associated to this Script
                    tdkTestObj = obj.createTestStep('Recorder_checkRecording_status');
                    PATTERN = validid;
                    tdkTestObj.addParameter("Recording_Id",recording_id);
                    #Execute the test case in STB
                    expectedresult="SUCCESS";
                    tdkTestObj.executeTestCase(expectedresult);
                    #Get the Actual result of streaming Interface
                    actualresult = tdkTestObj.getResult();                
                    patterndetails = tdkTestObj.getResultDetails();
                    print "Pattern details is : %s" %patterndetails;
                    duration_int = int(duration);
                    duration_sec = duration_int/1000;
                    duration_string = str(duration_sec);
                    print duration_string;
                    #compare the actual result with expected result
                    if expectedresult in actualresult:
                        if (PATTERN in patterndetails)and(duration_string in patterndetails):
                            tdkTestObj.setResultStatus("SUCCESS");
                            #Getting the mplayer log file from DUT
                            logpath=tdkTestObj.getLogPath();
                            print "Log path : %s" %logpath;
                            tdkTestObj.transferLogs(logpath,"false");
                            print "Successfully scheduled a Recording";
                            retValue = "SUCCESS"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            #Getting the mplayer log file from DUT
                            logpath=tdkTestObj.getLogPath();
                            print "Log path : %s" %logpath;
                            tdkTestObj.transferLogs(logpath,"false");
                            print "Recording is not completed with requested duration";
                            retValue = "FAILURE"
                    else:
                        print "Failed to schedule a Recording";
                        tdkTestObj.setResultStatus("FAILURE");
                        retValue = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Failed to Receive Json Message-Please check precondition";
                    retValue = "FAILURE"
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Recorder Failed to receive the requested request-Please check precondition";
                retValue = "FAILURE"
        else:
            print "getSourceId is failed";
            tdkTestObj.setResultStatus("FAILURE");
            
    else:
        print "Failed to load Recorder module";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE");

    return (retValue,recording_id);

'''


# To initiate a dvr playback in the Gateway box using tdk module
#
# Syntax       : dvr_playback(tdkTestObj,recording_id,**kwargs)
#
# Parameters   : tdkTestObj,recording_id,**kwargs 
#
# Return Value : 0 on success and 1 on failure


def dvr_playback(tdkTestObj,recording_id,**kwargs):
    
    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    print "Kwargs value %s"%kwargs

    print "Recording ID %s"%recording_id

    if 'trickplay' in kwargs.values():
        url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recording_id + '&0&play_speed=4.00&time_pos=0.00'
	print "URL for trickplay %s"%url
    else:
        url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recording_id
	print "URL:  %s"%url
 

    print "The Play DVR Url Requested: %s"%url
    tdkTestObj.addParameter("playUrl",url);

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();

    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");        
        print "E2E DVR Playback Successful: [%s]"%details;
        retValue = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "E2E DVR Playback Failed: [%s]"%details;
        retValue = "FAILURE"
        
    return retValue;



# To initiate a live playback in the Gateway box using tdk
#
# Syntax       : getURL_PlayURL(obj,streamId)
#
# Parameters   : obj,streamID
#
# Return Value : 0 on success and 1 on failure

def getURL_PlayURL(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');  
        
    #set the dvr play url for first channel
    streamDetails = tdkTestObj.getStreamDetails(streamId);        
    url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://"+streamDetails.getOCAPID()

    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);        

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    
    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        details =  tdkTestObj.getResultDetails();
        
        #Remove unwanted part from URL
        PLAYURL = details.split("[RESULTDETAILS]");
        ValidURL = PLAYURL[-1];        

        expectedresult="SUCCESS";
        
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_Rmf_LinearTv_Dvr_Play');

        print "Play Url Requested: %s"%(ValidURL);
        tdkTestObj.addParameter("playUrl",ValidURL);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        #Get the result of execution
        actualresult = tdkTestObj.getResult();        
        print "The E2E LinearTv Play : %s" %actualresult;

        #Set the result status of execution
        if "SUCCESS" in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print "E2E LinearTv Playback Successful: [%s]"%details;
            retValue = "SUCCESS"
            
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details =  tdkTestObj.getResultDetails();            
            print "Execution Failed: [%s]"%(details);
            retValue = "FAILURE"
    return retValue



# To initiate a forward play in the Gateway box using tdk
#
# Syntax       : skip_forward(obj)
#
# Parameters   : obj
#
# Return Value : 0 on success and 1 on failure



def skip_forward(obj):
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Skip_Forward_Play');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    recordingObj = tdkTestObj.getRecordingDetails();
    num = recordingObj.getTotalRecordings();
    print "Number of recordings: %d"%num
    recordID = recordingObj.getRecordingId(num - 1);

    url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=1.00&time_pos=0.00'

    print "The Play DVR Url Requested: %s"%url
    tdkTestObj.addParameter("playUrl",url);

    print "The number of seconds to be skiped from strating of video: %d"%skipNumOfSec
    tdkTestObj.addParameter("seconds",skipNumOfSec);

    print "The number of repeatation requested is %d"%repeatCount
    tdkTestObj.addParameter("rCount",repeatCount);

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();

    print "The E2E DVR Skip number of seconds from starting point of video : %s" %actualresult;

    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        retValue = "SUCCESS"
        print "E2E DVR Skip number of seconds Successful: [%s]"%details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        retValue = "FAILURE"
        print "E2E DVR Skip number of seconds Failed: [%s]"%details;
        
    return retValue

def skip_backward(obj):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_Rmf_Dvr_Skip_Backward_From_End');

    #set the dvr play url
    streamDetails = tdkTestObj.getStreamDetails("01");

    recordingObj = tdkTestObj.getRecordingDetails();
    num = recordingObj.getTotalRecordings();
    print "Number of recordings: %d"%num
    recordID = recordingObj.getRecordingId(num - 1);

    url = 'http://'+ streamDetails.getGatewayIp() + ':8080/vldms/dvr?rec_id=' + recordID[:-1] + '&0&play_speed=1.00&time_pos=0.00'

    print "The Play DVR Url Requested: %s"%url
    tdkTestObj.addParameter("playUrl",url);

    print "The number of seconds to be skiped from end of video: %d"%skipNumOfSec
    tdkTestObj.addParameter("seconds",skipNumOfSec);

    print "The number of repeatation requested is %d"%repeatCount
    tdkTestObj.addParameter("rCount",repeatCount);

    #Execute the test case in STB
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    actualresult = tdkTestObj.getResult();
    details =  tdkTestObj.getResultDetails();

    print "The E2E DVR Skip number of seconds from End of video :%s" %actualresult;

    #compare the actual result with expected result
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        retValue = "SUCCESS"
        print "E2E DVR Skip number of seconds from end of video Successful: [%s]"%details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        retValue = "FAILURE"
        print "E2E DVR Skip number of seconds from end of video Failed: [%s]"%details;
        
    return retValue

def TSB_play(obj,streamId):
    
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TDKE2E_RMFLinearTV_GetURL');
    #Stream details for tuning
    streamDetails = tdkTestObj.getStreamDetails(streamId);
    #Framing URL for Request
    url="http://"+streamDetails.getGatewayIp()+":8080/videoStreamInit?live=ocap://"+streamDetails.getOCAPID()+"&tsb=1";
    print "Request URL : %s" %url;
    tdkTestObj.addParameter("Validurl",url);
    #Execute the test case in STB and pass the expected result
    expectedresult="SUCCESS";
    tdkTestObj.executeTestCase(expectedresult);
    #Get the actual result of execution
    actualresult = tdkTestObj.getResult();
    print "Result of Json Response : %s" %actualresult;
    #compare the actual result with expected result of Json response Parameter
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS");
        retValue = "SUCCESS";
        details = tdkTestObj.getResultDetails();
        #Remove unwanted part from URL
        PLAYURL = details;
        print "Json Response Parameter is success";
        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('TDKE2E_RMF_TSB_Play');
        tdkTestObj.addParameter("VideostreamURL",PLAYURL);
        rate = 4.0;
        print "Speed rate value set : %f" %rate; 
        tdkTestObj.addParameter("SpeedRate",rate);
        #Execute the test case in STB and pass the expected result
        expectedresult="SUCCESS";
        tdkTestObj.executeTestCase(expectedresult);
        #Get the actual result of execution
        actualresult = tdkTestObj.getResult();
        print "Result of Json Response : %s" %actualresult;
        #compare the actual result with expected result of Json response Parameter
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            retValue = "SUCCESS";
            details = tdkTestObj.getResultDetails();
            print "E2E RMF TSB Playback Successful: [%s]"%details;
        else:
            tdkTestObj.setResultStatus("FAILURE");
            retValue = "FAILURE";
            details =  tdkTestObj.getResultDetails();
            print "E2E RMF TSB Playback Failed: [%s]"%details;
    else:
        tdkTestObj.setResultStatus("FAILURE");
        retValue = "FAILURE";
        print "Json Response Parameter is Failure";
                
    return retValue


