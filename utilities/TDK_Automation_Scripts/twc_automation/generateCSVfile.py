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

#Create a empty list for emoving duplicate entiries in CSV creation
testFnListInCSV= []
testCaseListInCSV= []

def generateCSVFile(filesPath, fileName, relevanceNumber):

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
	''' TODO
	if(testCaseNode[0].hasAttribute('description')):
		testCaseDescription=testCaseNode.attributes['description'].value
	'''
	FinaltestResDescription=''
	FinalReadingValue='N/A'
	FinalReadingUnits='N/A'
	FinalpassFailStatus='N/A'
	fileExists=False
	#Check  all .csv files if a .csv already started for  a component
	files = glob.glob(filesPath+'/*.csv')
	for f in files:
		if f == (filesPath+str(componentName)+".csv")  : #if a .csv file already exists for a component , use it , otherwise create a new.
			fileExists=True
			componentFile=open(filesPath+str(componentName)+".csv","a")
			break

	if fileExists==True:
		print "Data appending to CSV file..."
	else:
		#if a .csv file already exists for a component , use it , otherwise create a new.
		componentFile=open(filesPath+str(componentName)+".csv",'w+')
		print "Writing "+ filesPath+str(componentName)+".csv"
		componentFile.write("testCasename,testCaseDescription,componentName,testSuiteName,testCaseType,testFnName,testFnDescription,testFnType,passFailStatus,Performance_Data_Value,Performance_Data_Units,Relevance_Number \n");

	 
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
		if "success" in str( passFailStatus.lower()) or "pass" in str(passFailStatus.lower()):
			FinalpassFailStatus="SUCCESS"
		else:
			if "IRKeyManager" in componentName and str(passFailStatus.lower()) == '':
				FinalpassFailStatus="SUCCESS"
			else:
				FinalpassFailStatus="FAILURE"	

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
		if relevanceNum >= relevanceNumber and ( testCasename not in testCaseListInCSV or testFnName not in testFnListInCSV):
			if testFnName not in testFnListInCSV :
				testFnListInCSV.append(testFnName)
			if testCasename not in testCaseListInCSV :
				testCaseListInCSV.append(testCasename)
			componentFile.write(testCasename+","+testCaseDescription+","+componentName+","+testSuiteName+","+testType + ","+testFnName+","+testFnDescription+","+ testFnType +","+FinalpassFailStatus + ","+FinalReadingValue+","+FinalReadingUnits+","+str(relevanceNum)+"\n")

	componentFile.close()

def displayUsage ():
        print "USAGE:"
        print "python generatecsv.py <logsfolder> <relevance-number>"
	print "OR"
        print "python generatecsv.py <File_Name> <relevance-number>"

if len(sys.argv) == 2:
	displayUsage();
	generateCSVFile("./",str(sys.argv[1]),str(sys.argv[2]))

else:
        displayUsage()
        logsfolder=sys.argv[1]
        print "Path of log folder: ",logsfolder
        relevanceNumber=int(sys.argv[2])
        print "Relevance number entered by user: "+str(relevanceNumber)
        print "going to generate csv files ( .csv) for xml files in folder : "+ str(logsfolder)
        for file in sorted(os.listdir(logsfolder)):
                if file.endswith("_xmllog.xml") and not file.endswith("invalid_xmllog.xml") :
                        print "*******************"
                        print file
                        print "*******************"
                        generateCSVFile(logsfolder,file,relevanceNumber)
                else:
                        print "---excluded--- "+file
