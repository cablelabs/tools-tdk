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
import time;

# To create recording in the Gateway box using TdkRmfapp
#
# Parameters   : obj: Instance of mediaframework component library
#                kwargs: ID (Recording Id)
#                        TITLE (Recording Title)
#                        DURATION (Duration of recording in min)
#                        STREAMID (Id of the stream to be recorded)
#
# Return Value : "SUCCESS"/"FAILURE"
#
def createRecording(obj,kwargs={}):

        #Primitive test case which initiates recording
        tdkTestObj = obj.createTestStep('RMF_Dvr_CreateNew_Recording');

        recordId = str(kwargs["ID"])
        recordTitle = str(kwargs["TITLE"])
        recordDuration = str(kwargs["DURATION"])
        streamId = str(kwargs["STREAMID"])
        ocapId = tdkTestObj.getStreamDetails(streamId).getOCAPID()

        print "Create recording with Id:%s Title:%s Duration:%s OcapId:%s"%(recordId,recordTitle,recordDuration,ocapId)

        tdkTestObj.addParameter("recordId",recordId);
        tdkTestObj.addParameter("recordDuration",recordDuration);
        tdkTestObj.addParameter("recordTitle",recordTitle);
        tdkTestObj.addParameter("ocapId",ocapId);

        expectedresult="SUCCESS"

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);

        time.sleep(1);

        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(result,details)

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

########## End of createRecording Function ##########

# To delete a recording in the Gateway box
#
# Parameters   : obj: Instance of mediaframework component library
#                kwargs: ID (Recording Id)
#                        STREAMID (Id of the stream to be recorded)
#
# Return Value : "SUCCESS" / "FAILURE"
#
def deleteRecording(obj,kwargs={}):

        #Primitive test case which deletes recording
        tdkTestObj = obj.createTestStep('RMF_DVRManager_DeleteRecording');

        recordId = str(kwargs["ID"])
        streamId = str(kwargs["STREAMID"])

        streamDetails = tdkTestObj.getStreamDetails(streamId);
        playUrl = 'http://' + streamDetails.getGatewayIp() + ':8080/vldms/tuner?ocap_locator=ocap://'+streamDetails.getOCAPID();

        print "Delete Recording with Id:%s playUrl:%s"%(recordId,playUrl)

        tdkTestObj.addParameter("recordingId",recordId);
        tdkTestObj.addParameter("playUrl",playUrl);

        #Execute the test case in STB
        expectedRes = "SUCCESS"

        tdkTestObj.executeTestCase(expectedRes);

        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Result: [%s] Details: [%s]"%(result,details);

        #Set the result status of execution
        if expectedRes in result.upper():
            tdkTestObj.setResultStatus("SUCCESS");
            retValue = "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            retValue = "FAILURE"

        return retValue

########## End of deleteRecording Function ##########

########## End of createRecording Function ##########

# To Create the Streaming URL 
#
# Parameters   : playback_type : Type of playback - Live/TSB/DVR
#		 GatewayIP - IP of gateway device
#                ID - OCAP /Recording Id
#                tsb_size = Optional parameter for tsb size . Default value is 60
# Return Value : url - Streaming URL
#
def getStreamingURL( playback_type , GatewayIP , ID , tsb_size=60):
	
	if playback_type.upper() == "LIVE":
		url = 'http://' + GatewayIP + ':8080/hnStreamStart?live=ocap://'+ ID ;
	elif playback_type.upper() == "DVR":	
		url = 'http://' + GatewayIP + ':8080/hnStreamStart?recordingId='+ ID +'&segmentId=0';
	elif playback_type.upper() == "TSB":
		url = 'http://' + GatewayIP + ':8080/hnStreamStart?live=ocap://'+ ID +'&tsb='+str(tsb_size);
	else:
		print "Invalid Playback Type";
		return "NULL";
	return url;

########## End of getStreamingURL Function ##########

