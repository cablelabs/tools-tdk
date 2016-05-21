#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>13</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DTCP_StopSrcwithActiveSessions_32</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DTCP_Comp_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To stop DTCP-IP source without deleting active source and sink sessions.
There can be two approach for this (Refer RDKTT-641):
1) Cleanup of in-use sessions in DTCPMgrStopSource(), as done in intel
2) Return error from DTCPMgrStopSource() if there exist any in-use session, as done in broadcom.
TestType: Positive
TestcaseID: CT_DTCP_32</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
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
import dtcp;
from random import randint

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dtcp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DTCP_StopSrcwithActiveSessions_32');

#Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult();
print "DTCP module loading status :  %s" %loadmodulestatus;
#Set the module loading status
obj.setLoadModuleStatus(loadmodulestatus.upper());

if "SUCCESS" in loadmodulestatus.upper():
  #Primitive test case which associated to this Script
  tdkTestObj = obj.createTestStep('DTCP_Comp_Test');

  expectedresult="SUCCESS";
  #Pre-cond: Init,StartSource,CreateSrcSession,CreateSinkSession
  dtcp.init(tdkTestObj,expectedresult);
  dtcp.setLogLevel(tdkTestObj,expectedresult,kwargs={"level":5})
  port = randint(5001, 6000);
  result = dtcp.startSource(tdkTestObj,expectedresult,kwargs={'ifName':'lo','port':port})
  if expectedresult in result:

        print "\nCreate sessions"
        dtcp.createSinkSession(tdkTestObj,expectedresult,kwargs={'srcIp':'127.0.0.1','srcPort':port,'uniqueKey':0,'maxPacketSize':4096})
        dtcp.createSourceSession(tdkTestObj,expectedresult,kwargs={'sinkIp':'127.0.0.1','keyLabel':0,'pcpPacketSize':0,'maxPacketSize':4096})
        dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':2})

        #Stop source without deleting active sessions
        print "\n"
        fnName="DTCPMgrStopSource"
        #Add parameters to test object
        tdkTestObj.addParameter("funcName", fnName)
        #Execute the test case in STB
        tdkTestObj.executeTestCase("FAILURE")
        #Get the result of execution
        result = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print "%s"%(fnName)
        print "Result: [%s]"%(result)
        print "Details: [%s]"%details
        tdkTestObj.setResultStatus("SUCCESS");

        #Return error from DTCPMgrStopSource() if there exist any in-use session
        if "FAILURE" == result:
            #Delete all sessions and Stop source again
            print "\nDelete source sessions"
            srcNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0}))
            for index in range (0,srcNum):
                #dtcp.getSessionInfo(tdkTestObj,expectedresult,kwargs={"deviceType":0})
                dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":0})

            print "\nDelete sink sessions"
            sinkNum = int(dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1}))
            for index in range (0,sinkNum):
                #dtcp.getSessionInfo(tdkTestObj,expectedresult,kwargs={"deviceType":1})
                dtcp.deleteSession(tdkTestObj,expectedresult,kwargs={"deviceType":1})

            print "\nGet number of src and sink sessions after deleting sessions"
            dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':0})
            dtcp.getNumSessions(tdkTestObj,expectedresult,kwargs={'deviceType':1})

            print "\nStop source after sessions cleanup"
            dtcp.stopSource(tdkTestObj,expectedresult)
        #Cleanup of in-use sessions in DTCPMgrStopSource()
        else:
            print "\nGet number of src and sink sessions after stop source"

            print "\n"
            fnName="DTCPMgrGetNumSessions";
            #Add parameters to test object
            deviceType=0
            tdkTestObj.addParameter("funcName", fnName);
            tdkTestObj.addParameter("intParam2", deviceType);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedresult);
            #Get the result of execution
            result = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "%s [deviceType:%d (0-source 1-sink 2-all) ]"%(fnName,deviceType);
            print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
            print "Num of type(%d) sessions: [%s]"%(deviceType,details)

            #Set the result status of execution
            if expectedresult in result and "0" in details:
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");

            print "\n"
            fnName="DTCPMgrGetNumSessions";
            #Add parameters to test object
            deviceType=1
            tdkTestObj.addParameter("funcName", fnName);
            tdkTestObj.addParameter("intParam2", deviceType);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedresult);
            #Get the result of execution
            result = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print "%s [deviceType:%d (0-source 1-sink 2-all) ]"%(fnName,deviceType);
            print "Expected Result: [%s] Actual Result: [%s]"%(expectedresult,result)
            print "Num of type(%d) sessions: [%s]"%(deviceType,details)

            #Set the result status of execution
            if expectedresult in result and "1" in details:
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");

  #Unload the dtcp module
  obj.unloadModule("dtcp");
