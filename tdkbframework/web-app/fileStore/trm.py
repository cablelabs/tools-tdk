#!/usr/bin/python

#============================================================================
#COMCAST CONFIDENTIAL AND PROPRIETARY
#============================================================================
#This file and its contents are the intellectual property of Comcast.  It may
#not be used, copied, distributed or otherwise  disclosed in whole or in part
#without the express written permission of Comcast.
#============================================================================
#Copyright (c) 2014 Comcast. All rights reserved.
#============================================================================

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import tdklib;

# To fetch max tuners supported by gateway box.
#
# Syntax       : getMaxTuner(obj)
#
# Parameters   : obj
#
# Return Value : maxValue on success and 0 on failure

def getMaxTuner(obj,expectedresult):

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('TRM_GetMaxTuners');

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    maxTuner = int(details)

    #Set the result status of execution
    if "SUCCESS" in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

    print "Max tuners supported: ",maxTuner
    return maxTuner

#######################################################

# To initiate reserve tuner for live.
#
# Syntax       : reserveForLive(obj,expectedresult,kwargs={})
#
# Parameters   : deviceNo,duration,streamId,startTime
#
# Return Value : NONE

def reserveForLive(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForLive');

    deviceNo = int(kwargs["deviceNo"])
    duration = int(kwargs["duration"])
    streamId = str(kwargs["streamId"])
    startTime = int(kwargs["startTime"])
    locator = tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "DeviceNo:%d streamId:%s duration:%d startTime:%d"%(deviceNo,streamId,duration,startTime)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################

# To initiate reserve tuner for record.
#
# Syntax       : reserveForRecord(obj,expectedresult,kwargs={})
#
# Parameters   : deviceNo,duration,streamId,startTime,recordingId,hot
#
# Return Value : NONE

def reserveForRecord(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_TunerReserveForRecord');

    deviceNo = int(kwargs["deviceNo"])
    duration = int(kwargs["duration"])
    streamId = str(kwargs["streamId"])
    startTime = int(kwargs["startTime"])
    recordingId = str(kwargs["recordingId"])
    hot = int(kwargs["hot"])
    locator = tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("duration",duration);
    tdkTestObj.addParameter("locator",locator);
    tdkTestObj.addParameter("startTime", startTime);
    tdkTestObj.addParameter("recordingId",recordingId);
    tdkTestObj.addParameter("hot",hot);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "DeviceNo:%d streamId:%s duration:%d startTime:%d recordingId:%s hot:%d"%(deviceNo,streamId,duration,startTime,recordingId,hot)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################

def cancelRecording(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_CancelRecording');

    streamId = str(kwargs["streamId"])
    locator = tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("locator",locator);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "streamId: %s"%(streamId)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################

def releaseReservation(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_ReleaseTunerReservation');

    deviceNo = int(kwargs["deviceNo"])
    activity = int(kwargs["activity"])
    streamId = str(kwargs["streamId"])
    locator = tdkTestObj.getStreamDetails(streamId).getOCAPID()

    tdkTestObj.addParameter("deviceNo",deviceNo);
    tdkTestObj.addParameter("activity",1);
    tdkTestObj.addParameter("locator",locator);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    if (1 == activity):
        Activity = 'Live'
    else:
        Activity = 'Record'

    #Get the result/details of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "activity:%s deviceNo:%d streamId:%s"%(Activity,deviceNo,streamId)
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################

def getAllTunerStates(obj,expectedresult):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_GetAllTunerStates');

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################

def getAllReservations(obj,expectedresult,kwargs={}):

    #Primitive test case associated to the function
    tdkTestObj = obj.createTestStep('TRM_GetAllReservations');

    if 'deviceNo' in kwargs:
        deviceNo = int(kwargs["deviceNo"])
        tdkTestObj.addParameter("deviceNo",deviceNo);
        print "Fetching reservation info for deviceNo: ",deviceNo
    else:
        print "Fetching all reservations"

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedresult);

    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
    print "Details: [%s]"%details

    #Set the result status of execution
    if expectedresult in result.upper():
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");

#######################################################