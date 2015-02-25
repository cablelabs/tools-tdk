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
import time;

# Description  : To initialize DTCP Manager
#
# Parameters   : tdkTestObj (Instance of dtcp common primitive testcase)
#              : expectedresult
#
# Return Value : "SUCCESS"/"FAILURE"
#
def init(tdkTestObj,expectedresult):

	fnName="DTCPMgrInitialize";
	#Add parameters to test object
	tdkTestObj.addParameter("funcName", fnName); 
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "Input: [funcName:%s]"%(fnName)
	print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
 	print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
        	tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
		retValue = "FAILURE"

        return retValue

########## End of dtcpMgrInitialize Function ##########

def startSource(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrStartSource";
        #Add parameters to test object
	ifName=str(kwargs["ifName"])
        port=int(kwargs["port"])
        tdkTestObj.addParameter("funcName", fnName);
	tdkTestObj.addParameter("strParam1", ifName);
	tdkTestObj.addParameter("intParam2", port);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "Input: [funcName:%s ifName:%s port: %d]"%(fnName,ifName,port);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def stopSource(tdkTestObj,expectedresult):

        fnName="DTCPMgrStopSource"
        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "Input: [funcName:%s]"%(fnName)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def createSourceSession(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrCreateSourceSession";

        #Add parameters to test object
        sinkIp=str(kwargs["sinkIp"])
        keyLabel=int(kwargs["keyLabel"])
	pcpPacketSize=int(kwargs["pcpPacketSize"])
	maxPacketSize=int(kwargs["maxPacketSize"])

  	tdkTestObj.addParameter("funcName", fnName);
  	tdkTestObj.addParameter("strParam1", sinkIp);
  	tdkTestObj.addParameter("intParam2", keyLabel);
  	tdkTestObj.addParameter("intParam3", pcpPacketSize);
  	tdkTestObj.addParameter("intParam4", maxPacketSize);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "Input: [funcName:%s sinkIp:%s keyLabel:%d pcpPacketSize:%d maxPacketSize:%d]"%(fnName,sinkIp,keyLabel,pcpPacketSize,maxPacketSize);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def createSinkSession(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrCreateSinkSession";

        #Add parameters to test object
        srcIp=str(kwargs["srcIp"])
        srcPort=int(kwargs["srcPort"])
        uniqueKey=int(kwargs["uniqueKey"])
        maxPacketSize=int(kwargs["maxPacketSize"])

        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("strParam1", srcIp);
        tdkTestObj.addParameter("intParam2", srcPort);
        tdkTestObj.addParameter("intParam3", uniqueKey);
        tdkTestObj.addParameter("intParam4", maxPacketSize);

        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
	print "Input: [funcName:%s srcIp:%s srcPort:%d uniqueKey:%d maxPacketSize:%d]"%(fnName,srcIp,srcPort,uniqueKey,maxPacketSize)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def processPacket(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrProcessPacket"

        #Add parameters to test object
       	index=int(kwargs["index"])
        tdkTestObj.addParameter("funcName", fnName)
 	tdkTestObj.addParameter("intParam2", index);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "Input: [funcName:%s index:%d]"%(fnName,index)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
	time.sleep(10);
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def releasePacket(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrReleasePacket"
        #Add parameters to test object
        index=int(kwargs["index"])
        tdkTestObj.addParameter("funcName", fnName)
        tdkTestObj.addParameter("intParam2", index);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "Input: [funcName:%s index:%d]"%(fnName,index)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue


def deleteSession(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrDeleteDTCPSession"
        #Add parameters to test object
        index=int(kwargs["index"])
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName)
        tdkTestObj.addParameter("intParam2", index);
        tdkTestObj.addParameter("intParam3", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "Input: [funcName:%s index:%d deviceType:%d]"%(fnName,index,deviceType)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

def getSessionInfo(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrGetSessionInfo"

        #Add parameters to test object
        index=int(kwargs["index"])
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName)
        tdkTestObj.addParameter("intParam2", index);
        tdkTestObj.addParameter("intParam3", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult)
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "Input: [funcName:%s index:%d deviceType:%d]"%(fnName,index,deviceType)
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details
        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                retValue = details
        else:
                tdkTestObj.setResultStatus("FAILURE");
                retValue = "FAILURE"

        return retValue

def getNumSessions(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrGetNumSessions";
        #Add parameters to test object
        deviceType=int(kwargs["deviceType"])
        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("intParam2", deviceType);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Input: [funcName:%s deviceType:%d]"%(fnName,deviceType);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Num of type(%d) sessions: [%s]"%(deviceType,details)

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
        else:
                tdkTestObj.setResultStatus("FAILURE");

        return details


def setLogLevel(tdkTestObj,expectedresult,kwargs={}):

        fnName="DTCPMgrSetLogLevel";
        #Add parameters to test object
        level=int(kwargs["level"])
        tdkTestObj.addParameter("funcName", fnName);
        tdkTestObj.addParameter("intParam2", level);
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedresult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print "Input: [funcName:%s level:%d]"%(fnName,level);
        print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
        print "Details: [%s]"%details

        #Set the result status of execution
        if expectedresult in result:
                tdkTestObj.setResultStatus("SUCCESS");
		retValue = "SUCCESS"
        else:
                tdkTestObj.setResultStatus("FAILURE");
		retValue = "FAILURE"

        return retValue
