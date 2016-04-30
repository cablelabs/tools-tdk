#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
from xml.dom import minidom
import sys
import os
import xml.dom.minidom
import re
import glob
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt 
from xlwt import Workbook
from getTWCRDKTDKVersion import getTWCRDKTDKVersion
import time
 
DateOfExecution = time.strftime("%c")
value = 0	# for storing row index

#Create a empty list for emoving duplicate entiries in XLS creation
testFnListInXLS= []
testCaseListInXLS= []
testFnDescListInXLS= []
TESTLIST=[]
XLS_GROW_COUNT = 0
TEST_REPORT_NAME=""
TEST_PASS_COUNT=0
TEST_FAIL_COUNT=0
TOTAL_TEST_COUNT=0
TOTAL_TESTSCRIPT_COUNT=0

if (len(sys.argv) >1):
	if len(sys.argv) == 6 and str(sys.argv[4]).endswith(".xml"):
		print "TDK Test Configuration file Input...." + str(sys.argv[4]) + "\n"
		dom = xml.dom.minidom.parse(str(sys.argv[4]))
else:
	print "No TDK Test Configuration file Input.... \n Reading Default Configuration file (./TdkConfig.xml).... \n."
	dom = xml.dom.minidom.parse('TdkConfig.xml')   

#dom = xml.dom.minidom.parse('TdkConfig.xml')
env = dom.getElementsByTagName('TestEnvironment')
deviceIP=env[0].getElementsByTagName('TARGET_IP')[0].childNodes[0].nodeValue
deviceName=str(env[0].getElementsByTagName('DEV_NAME')[0].childNodes[0].nodeValue)
devicePort=env[0].getElementsByTagName('Device_Port')[0].childNodes[0].nodeValue
rdkVersionFile=env[0].getElementsByTagName('RDK_Version')[0].attributes['file'].value
rdkVersionSearchString=env[0].getElementsByTagName('RDK_Version')[0].attributes['versionStrInfo'].value
tdkVersionFile=env[0].getElementsByTagName('TDK_Version')[0].attributes['file'].value
tdkVersionSearchString=env[0].getElementsByTagName('TDK_Version')[0].attributes['versionStrInfo'].value
BUILD_VER = env[0].getElementsByTagName('BUILD_VER')[0].childNodes[0].nodeValue


#This feature is only available for TWC HUMAX boxes
if "humax" in deviceName.lower() :
	# Fetch STB RDK and TDK environment details
	rdkVersion = getTWCRDKTDKVersion(deviceIP,int(devicePort),rdkVersionFile,rdkVersionSearchString)
	tdkVersion = getTWCRDKTDKVersion(deviceIP,int(devicePort),tdkVersionFile,tdkVersionSearchString)
	print "STB_TDK_VERSION : " + str(tdkVersion)
	print "STB_RDK_VERSION : " + str(rdkVersion)
else:
	tdkVersion = "Not supported for box "+str(deviceName)
	rdkVersion = "Not supported for box "+str(deviceName)
HEADER=["testCasename","testCaseDescription","componentName","testSuiteName","testType","testFnName","testFnDescription","testFnType","Units","relevanceNum",str(BUILD_VER)+"_PerformanceReadings",str(BUILD_VER)+"_Result"]
LENGTH_OF_HEADER=len(HEADER)
TEST_SUMMARY_HEADER=["TestSuiteName","TotalTestSuiteCount","TotalTestCount","TestPassCount","TestFailCount","OtherTestCount", "TestExecutionTime", "STB_RDK_Version" , "STB_TDK_Version","Date Of execution","Execution Name"]
LENGTH_OF_TESTSUMMARY_HEADER=len(TEST_SUMMARY_HEADER)

def get_tag_value(node):
    xml_str = node.toxml() #element to string
    # cut off the base tag to get clean content:
    start = xml_str.find('>')
    if start == -1:
        return ''
    end = xml_str.rfind('<')
    if end < start:
        return ''
 
    return xml_str[start + 1:end]

def generateXLSFile(filesPath, fileName, relevanceNumber):
	global TEST_REPORT_NAME;
	global TEST_PASS_COUNT
	global TEST_FAIL_COUNT
  	global TOTAL_TEST_COUNT
	global ExecutionName
	 #Incase / missed in path at the end
	if not filesPath.endswith('/'):
		filesPath=filesPath+"/"

	dom = xml.dom.minidom.parse(filesPath+fileName)
	testCasename=dom.getElementsByTagName('TestCase')[0].attributes['name'].value
	componentName=dom.getElementsByTagName('TestCase')[0].attributes['componentName'].value
	testSuiteName=dom.getElementsByTagName('TestCase')[0].attributes['testSuiteName'].value
	testType=dom.getElementsByTagName('TestCase')[0].attributes['testType'].value
	testCaseNode=dom.getElementsByTagName('TestCase')
	testCaseDescription="Test Case for "+str(testCasename)
	ExecutionName=dom.getElementsByTagName('TestCase')[0].getElementsByTagName('Environment')[0].getElementsByTagName('executionName')[0].childNodes[0].data	
	
	FinaltestResDescription=''
	FinalReadingValue='N/A'
	FinalReadingUnits='N/A'
	FinalpassFailStatus='N/A'
	fileExists=False
 	TEST_REPORT_NAME=str(testSuiteName);
	testFunctions=dom.getElementsByTagName('TestFunction')
	for testFn in testFunctions:
		testFnName=testFn.attributes['name'].value
		testFnDescription="Test Function for "+str(testFnName)
		if(testFn.getAttributeNode('description')):
			testFnDescription=testFn.attributes['description'].value                        
		relevanceNum=int(testFn.attributes['relevance'].value)
		passFailStatus=""
		testFnType=""
		messageNodeList = testFn.getElementsByTagName("Message")
		if testFn.getAttribute("testType") == 1:
			testFnType= testFn.attributes['testType'].value
		else:
			testFnType="functional"
		if testFn.getElementsByTagName('Incident'):
			passFailStatus=testFn.getElementsByTagName('Incident')[0].attributes['type'].value
		else:
			passFailStatus=""
		if "success" in str( passFailStatus.lower()) or "pass" in str(passFailStatus.lower()) or "SUCCESS" in str(passFailStatus):
			FinalpassFailStatus="SUCCESS"
			#TEST_PASS_COUNT=TEST_PASS_COUNT+1
		else:
			if ("IRKeyManager" in componentName or "IARMBus" in componentName) and str(passFailStatus.lower()) == '':
				FinalpassFailStatus="SUCCESS"
				#TEST_PASS_COUNT=TEST_PASS_COUNT+1'''
			else:
				FinalpassFailStatus="FAILURE"	
				#TEST_FAIL_COUNT=TEST_FAIL_COUNT+1

		if componentName=='GStreamer' or componentName =='QtWebkit':
			for messageNode in messageNodeList:
				FinalReadingValue='N/A'
				FinalReadingUnits='N/A'
				descriptionNodeList=messageNode.getElementsByTagName("Description")
				if(descriptionNodeList):
					for descriptionNode in descriptionNodeList:
						testResDescription=get_tag_value(descriptionNode);
						TestFunctionKeys=["[CDATA[Totals","Checks", "Average"]
						if "[CDATA[Totals" in testResDescription or "Checks" in testResDescription:
							FinaltestResDescription=get_tag_value(descriptionNode);

				#print messageNode.attributes['type'].value
				if FinaltestResDescription != '':
					value = re.split("::", FinaltestResDescription)
					length=len(value)
					result = re.findall("\d*\.\d+|\d+", value[length-1])
					units = re.split("[^a-zA-Z]*", value[length-1])
					if result:
						FinalReadingValue = str(result[0])
						FinalReadingUnits=str(units[-2])
		else:
			if(testFn.getElementsByTagName('PerformanceData')):
				perfData=testFn.getElementsByTagName('PerformanceData')[0].attributes['name'].value
				FinalReadingUnits=testFn.getElementsByTagName('PerformanceData')[0].attributes['unit'].value
				FinalReadingValue=testFn.getElementsByTagName('PerformanceData')[0].getElementsByTagName('PerfDataReading')[0].childNodes[0].data
				perfDataInfo=testFn.getElementsByTagName('PerformanceData')[0].getElementsByTagName('PerfDataInfo')[0].childNodes[0].data
				performanceData=perfData+":"+"PerformanceDataReading- "+FinalReadingValue+" "+ FinalReadingUnits+"PerformanceDataInfo- "+perfDataInfo
			else:
				performanceData="-"

		#Check for relevance number and also duplication entry
		if relevanceNum >= relevanceNumber and ( testCasename not in testCaseListInXLS or testFnName not in testFnListInXLS or testFnDescription not in testFnDescListInXLS):
			TOTAL_TEST_COUNT = TOTAL_TEST_COUNT + 1
			if FinalpassFailStatus=="SUCCESS":
				TEST_PASS_COUNT=TEST_PASS_COUNT+1
			else:
				TEST_FAIL_COUNT=TEST_FAIL_COUNT+1

			if testFnName not in testFnListInXLS :
				testFnListInXLS.append(testFnName)
			if testCasename not in testCaseListInXLS :
				testCaseListInXLS.append(testCasename)
			if testFnDescription not in testFnDescListInXLS:
				testFnDescListInXLS.append(testFnDescription)
			TESTLIST=[]
			TESTLIST.extend((testCasename, testCaseDescription, componentName, testSuiteName, testType, testFnName, testFnDescription, testFnType, FinalReadingUnits, str(relevanceNum), FinalReadingValue, FinalpassFailStatus))
			WriteToXlsSheet(TESTLIST[:])

#Function to append the result for all successive Build versions in Report
def appendbuildversion(file_path, BUILD_VER, testCaseName, testFunctionName, incidentType, performanceReadings):
	w_sheet1 = book.get_sheet(1)
	TESTS_PassFail_STATUS_SHEET = openbook.sheet_by_index(1)
	rl = TESTS_PassFail_STATUS_SHEET.row_values(0,start_colx=0)

	buildVersion=str(BUILD_VER)+'_PerformanceReadings'
	if buildVersion not in rl:
		columnCount=0
		for column in range(0,TESTS_PassFail_STATUS_SHEET.ncols - 1):
			columnCount+=1
			if(columnCount==TESTS_PassFail_STATUS_SHEET.ncols-1):
				w_sheet1.write(0, TESTS_PassFail_STATUS_SHEET.ncols, BUILD_VER+"_PerformanceReadings")	
				w_sheet1.write(0, TESTS_PassFail_STATUS_SHEET.ncols+1, BUILD_VER+"_Result")	
		for row in range (1,TESTS_PassFail_STATUS_SHEET.nrows):
			if(TESTS_PassFail_STATUS_SHEET.cell_value(row,0)==testCaseName and TESTS_PassFail_STATUS_SHEET.cell_value(row,5)==testFunctionName):
				w_sheet1.write(row,TESTS_PassFail_STATUS_SHEET.ncols,performanceReadings)
				w_sheet1.write(row,TESTS_PassFail_STATUS_SHEET.ncols+1,incidentType)

def WriteToXlsSheet(TESTLIST):
	global XLS_GROW_COUNT;
	file_path=sys.argv[5]
	if(os.path.exists(file_path)):
		incidentType=TESTLIST[-1]
		performanceReadings=TESTLIST[-2]
		testFunctionName=TESTLIST[5]
		testCaseName=TESTLIST[0]
		appendbuildversion(file_path, BUILD_VER, testCaseName, testFunctionName, incidentType, performanceReadings)
	else:
		for c in range(0,LENGTH_OF_HEADER):
			TESTS_PF_STATUS_SHEET.write(XLS_GROW_COUNT, c, TESTLIST[c])
		XLS_GROW_COUNT = XLS_GROW_COUNT + 1
	
def WriteTestSummary(LIST):
	global TEST_SUMMARY_ROW_COUNT;
	TESTS_SUMMARY_SHEET = book.get_sheet(0)
	for c in range(0,LENGTH_OF_TESTSUMMARY_HEADER):
		#print "#######****"+str(c) +"###" +str(TEST_SUMMARY_ROW_COUNT)+ "###" + str (TEST_SUMMARY_START+c)+"###"+str(LIST[c])
		if(os.path.exists(str(sys.argv[5]))):
			TESTS_SUMMARY_SHEET = book.get_sheet(0)
			TESTS_SUMMARY_SHEET.write(TEST_SUMMARY_ROW_COUNT, TEST_SUMMARY_START+c, LIST[c])
		else:
			TESTS_SUMMARY_SHEET.write(TEST_SUMMARY_ROW_COUNT, TEST_SUMMARY_START+c, LIST[c])
	TEST_SUMMARY_ROW_COUNT = TEST_SUMMARY_ROW_COUNT + 1

def displayUsage ():
        print "USAGE:"
        print "python generatexls.py <logsfolder> <relevance-number> <time> <TdkConfig.xml> <componentname+TestReport.xls>"
	print "OR"
        print "python generatexls.py <File_Name> <relevance-number> <time> <TdkConfig.xml> <componentname+TestReport.xls>"

TEST_EXECUTION_TIME=""
TEST_SUMMARY_START=5
TEST_SUMMARY_LIST=[]
TEST_SUMMARY_ROW_COUNT=TEST_SUMMARY_START

TESTS_SUMMARY_SHEET=""
TESTS_PF_STATUS_SHEET=""
book=""
openbook=""
if len(sys.argv) == 2:
	displayUsage();
	generateXLSFile("./",str(sys.argv[1]),str(sys.argv[2]))

else:
        displayUsage()
        logsfolder=sys.argv[1]
        print "Path of log folder: ",logsfolder
        relevanceNumber=int(sys.argv[2])
	print "Number of Args : "+ str(len(sys.argv))
	TEST_EXECUTION_TIME=str(sys.argv[3])
	print "Time taken for total execution :" + str(sys.argv[3])
	print "Relevance number entered by user: "+str(relevanceNumber)
        print "going to generate xls files ( .xls) for xml files in folder : "+ str(logsfolder)
	if(os.path.exists(str(sys.argv[5]))):
		openbook = open_workbook(str(sys.argv[5]),formatting_info=True)
		book=copy(openbook)
		TESTS_SUMMARY_SHEET = book.get_sheet(0)
		TESTS_PF_STATUS_SHEET = book.get_sheet(1)
		print "file exists"
	else:
		book = xlwt.Workbook(encoding="utf-8")
		TESTS_SUMMARY_SHEET = book.add_sheet("TESTS_SUMMARY_SHEET")
		TESTS_PF_STATUS_SHEET = book.add_sheet("TESTS_PassFail_STATUS_SHEET")
	
	for c in range(0,LENGTH_OF_HEADER):
		if(not os.path.exists(str(sys.argv[5]))):
			TESTS_PF_STATUS_SHEET.write(XLS_GROW_COUNT, c, HEADER[c])
	XLS_GROW_COUNT = XLS_GROW_COUNT + 1
	print "\nXLS_GROW_COUNT :",XLS_GROW_COUNT

	for file in sorted(os.listdir(logsfolder)):
		if file.endswith("_xmllog.xml") and not file.endswith("invalid_xmllog.xml") :
			TOTAL_TESTSCRIPT_COUNT=TOTAL_TESTSCRIPT_COUNT+1
			print "*******************"
			print str(TOTAL_TESTSCRIPT_COUNT)+"."+file
			print "*******************"
			generateXLSFile(logsfolder,file,relevanceNumber)
		else:
			print "---excluded--- "+file
	print "Final Test Report Name : " + str(sys.argv[5]) 
	
	TEST_SUMMARY=[]
	OtherTestsCount=int(TOTAL_TESTSCRIPT_COUNT-(TEST_PASS_COUNT+TEST_FAIL_COUNT))
	if OtherTestsCount > 0 :
		#Incase of SNMP,TR069,Gstreamer and Webkit
		TEST_SUMMARY.extend((str(TEST_REPORT_NAME),str(TOTAL_TESTSCRIPT_COUNT),str(TEST_PASS_COUNT+TEST_FAIL_COUNT),str(TEST_PASS_COUNT),str(TEST_FAIL_COUNT),str(TOTAL_TESTSCRIPT_COUNT-(TEST_PASS_COUNT+TEST_FAIL_COUNT)),str(TEST_EXECUTION_TIME), BUILD_VER, str(tdkVersion.strip()),str(DateOfExecution),ExecutionName))
	else:
		#Incase of all other component tests
		TEST_SUMMARY.extend((str(TEST_REPORT_NAME),str(TOTAL_TESTSCRIPT_COUNT),str(TEST_PASS_COUNT+TEST_FAIL_COUNT),str(TEST_PASS_COUNT),str(TEST_FAIL_COUNT),str(TOTAL_TEST_COUNT-(TEST_PASS_COUNT+TEST_FAIL_COUNT)),str(TEST_EXECUTION_TIME), BUILD_VER, str(tdkVersion.strip()),str(DateOfExecution),ExecutionName))
		
	WriteTestSummary(TEST_SUMMARY_HEADER[:]);
	WriteTestSummary(TEST_SUMMARY[:]);
	
	book.save(str(sys.argv[5]))
