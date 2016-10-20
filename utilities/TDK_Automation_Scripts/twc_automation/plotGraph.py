##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
from xlrd import open_workbook
import re;
import os;
import sys;
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as pl
from xml.dom import minidom
import xml.dom.minidom

#########################################################################################################		
# Description:	Method to parse plotConig.xml file and fetch the testfunction name having plot flag=true#
# Input parameter:	XML file path with file name							#
# Output parameter:	List of testfunction for which graph plotting requires				#
#########################################################################################################

testGroup=[]
testFnName=[]
testFuncName=[]
def ParsePlotConfigXml(fileName, componentName):
	global testGroup
	global testFuncName
	dom = xml.dom.minidom.parse(fileName)
	compName = dom.getElementsByTagName('TestSuite')
	for component in compName:
		if(componentName == component.attributes['name'].value):
			testGroupName = component.getElementsByTagName('TestGroupName')
			#print testGroupName
			for testGp in testGroupName:
				if(testGp.attributes['groupPlot'].value == "true"):
					testFnName=[]
					testFunctions=testGp.getElementsByTagName('TestFunctionName')
					for testFn in testFunctions:
						if(testFn.attributes['plot'].value == "true"):
							#if(testFn.attributes['plot'].value == "true"):
							testFnName.append(testFn.childNodes[0].nodeValue)
					testGroup.append(testFnName)
				else:
					testFunctions=testGp.getElementsByTagName('TestFunctionName')
					for testFn in testFunctions:
						if(testFn.attributes['plot'].value == "true"):
							testFuncName.append(testFn.childNodes[0].nodeValue)
	
			#print "TestFuncName: ",testFuncName
			#print "TestGroup: ",testGroup 
			buildVersion = component.getElementsByTagName('BuildVersion')[0].childNodes[0].nodeValue
	return str(buildVersion)		

####################################################################################
# Description:	Method to read report in excel sheet and fetch performance readings# 
#	for all the given release version till latest release version.		   #
# Input Parameters:	ReportName, SheetName and BuildVersion.			   #		
# Output:	Performance Readings from given build version.			   #
####################################################################################
def ParseTestReport(reportName, sheetName, buildVersion):
	
	wb = open_workbook(reportName)
	performanceSheet=wb.sheet_by_name(sheetName)
	numberOfRows=performanceSheet.nrows
	print "Number of Rows: %s\n" %numberOfRows
	numberOfColumns=performanceSheet.ncols
	print "Number of Columns: %s\n" %numberOfColumns

	for row in range(numberOfRows):
		for col in range(numberOfColumns):
			if('testFnName' in str(performanceSheet.cell(row,col).value)):
				cNumber=col
				rNumber=row
				values= []
				for r in range(rNumber,numberOfRows):
					sheetRow= []
					for c in range(cNumber, numberOfColumns):
						sheetRow.append(performanceSheet.cell(r,c).value)
					values.append(sheetRow)				
			if (buildVersion in str(performanceSheet.cell(row,col).value) and (not "Result" in str(performanceSheet.cell(row,col).value))):
				print "Build Version Matched\n"
				rowNumber=row
				print "Row Number: %d" %rowNumber
				colNumber=col
				print "Column Number: %d" %colNumber
				print "Number of Columns: %d\n" %numberOfColumns
				for column in range(colNumber,numberOfColumns):
					value  = performanceSheet.cell(rowNumber,column).value
					try : value = str(int(value));
					except : pass
					if(("Release" in value or "Build" in value) and (not "Result" in value)):
						col_value.append(value)
					while '' in col_value:
   						col_value.remove('')

	reading=[]
	for item in values:
		itemLength= len(item)
	na = np.array(values)
	for i in range (itemLength):
		reading.append(na[:,i].tolist())
	values=[]
	for item in reading:
		if (("testFnName" in item[0] or "Release" in item[0] or "Build" in item[0]) and (not "Result" in item[0])):
			values.append(item)
		else:	
			continue
	performanceReading= []
	for item in values:
		finalValue =[]
		for i in item:
			if ('N/A' == i or 'NOT EXECUTED' == i or 'NOT_EXECUTED' == i or 'FAIL' == i or 'PASS' == i or 'FAILED' == i or '' == i):
				i='0.0'
			finalValue.append(i)
		performanceReading.append(finalValue)
	perfReadings=[]
	testFunctionList=[]
	for item in performanceReading:
		if 'testFnName' in item:
			testFunctionList.append(item)
		
		if (("Release" in item[0] or "Build" in item[0]) and (not "Result" in item[0])):
			perfReadings.append(item)

	readingMap= map (None,*perfReadings)
	funcMap= map(None, *testFunctionList)

	finalReadingList=[]
	finalFuncList=[]

	for item in readingMap:
		if (("Release" in item[0] or "Release" in item or "Build" in item[0] or "Build" in item) and (not "Result" in item[0] or "Result" in item)):
			continue
		else:
			finalReadingList.append(item)

	for item in funcMap:
		if("testFnName" == item):
			continue
		else:
			finalFuncList.append(item)
	funcNameMappingWithReadings= zip(finalFuncList, finalReadingList)
	return funcNameMappingWithReadings

####################################################################################################################
# Description:	    Method to plot the graph for given performance readings. 					   # 
# Input Parameters: col_value(xAxis of graph) and Reading(yAxis of graph)					   #		
# Output:	    Plot the graph for different testfunction and save it as .png image inside Graph directory     #
####################################################################################################################
def PlotGraph (componentName, x, y,configFile):
	xAxis=np.array(x)
	lengthOfReleaseCount=len(x)
	releaseCount = []
	groupName = []
	for count in range(1,lengthOfReleaseCount+1):
		releaseCount.append(count)
	if not os.path.exists("TDK_PerformanceGraph/"+componentName+"_Graph"):
		os.makedirs("TDK_PerformanceGraph/"+componentName+"_Graph")
	try:	
		dom = xml.dom.minidom.parse(configFile)
		compName = dom.getElementsByTagName('TestSuite')
		for component in compName:
			if(componentName == component.attributes['name'].value):
				testGroupName = component.getElementsByTagName('TestGroupName')
				for testGp in testGroupName:
					if(testGp.attributes['groupPlot'].value == "true"):							
						#print testGroup, len(testGroup)
						#print testGp
						groupName.append(testGp.attributes['name'].value)
				#print groupName 				
				for testGp in testGroupName:
					if(testGp.attributes['groupPlot'].value == "true"):							
						groupCount=0
						for group in testGroup:
							for function in group:
								#print "Function Name: ",function
								for i, j in y:
									yAxis = np.array(j)
									if(function in i):
										#print function
										pl.plot(releaseCount, yAxis, marker='o', label= function)
										legnd = pl.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
										pl.xticks(releaseCount, xAxis, rotation=90)
										pl.title("Time Taken For Functions in a Group : "+str(groupName[groupCount]))
										pl.ylabel("Time in milliseconds")
										pl.xlabel("RDK Release Version")
										pl.grid(True)
										pl.savefig("TDK_PerformanceGraph/"+componentName+"_Graph/"+str(groupName[groupCount])+'.png', bbox_extra_artists=(legnd,), bbox_inches='tight')
							groupCount=groupCount+1
							pl.clf()
					else:
						for i, j in y:
							yAxis = np.array(j)
							for function in testFuncName:
								if(function in i):
									pl.plot(releaseCount, yAxis, marker='o', label= function)
									legnd = pl.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
									pl.xticks(releaseCount, xAxis, rotation=90)
									pl.title("Time Taken For Function : "+function)
									pl.ylabel("Time in milliseconds")
									pl.xlabel("RDK Release Version")
									pl.grid(True)
									pl.savefig("TDK_PerformanceGraph/"+componentName+"_Graph/"+i+'.png', bbox_extra_artists=(legnd,), bbox_inches='tight')			
									pl.clf()
	except Exception,e:
		print "Exception Occured plotting Graph for :" + str (function) + "for Values :" + str(j)
		print "Exception Type: ",e.message
		
def displayUsage ():
	print "USAGE:"
	print "python plotGraph.py <Config FileName> <ComponentName> <ReportName> <SheetName>"

col_value = []
funcNameMappingWithReadings=[]	
if len(sys.argv) == 5:
	displayUsage();
	buildVersion = ParsePlotConfigXml(str(sys.argv[1]), str(sys.argv[2]))
	funcMap=ParseTestReport(str(sys.argv[3]), str(sys.argv[4]), buildVersion)
	#print col_value,": ",len(col_value)
	#print funcMap,": ", len(funcMap[1])
	PlotGraph(str(sys.argv[2]), col_value, funcMap, str(sys.argv[1]))

else:
        print "argument passed are not equal to 4\n"
        displayUsage()
