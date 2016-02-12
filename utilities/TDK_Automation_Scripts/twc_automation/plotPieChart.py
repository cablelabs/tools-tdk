#!/usr/bin/env python
import sys
import os
from xlrd import open_workbook
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
TEST_PASS_COUNT = 'TestPassCount'
TEST_FAIL_COUNT = 'TestFailCount'
TEST_OTHER_COUNT = 'OtherTestCount'
TESTSUITE_COULMN_NAME = 'TestSuiteName' 

def ParseTestSummary(reportName, sheetName):
	wb = open_workbook(reportName)
	summarySheet=wb.sheet_by_name(sheetName)
	numberOfRows=summarySheet.nrows
	print "Number of Rows: %s\n" %numberOfRows
	numberOfColumns=summarySheet.ncols
	print "Number of Columns: %s\n" %numberOfColumns
	result=[]
	for row in range(numberOfRows):
		values=[]
		for col in range(numberOfColumns):
			values.append(str(summarySheet.cell(row,col).value))
		while "" in values:
			values.remove('')
		result.append(values)
	summary=[]
	for item in result:
		if item:
			summary.append(item)				
		else:
			continue
	summaryMap=zip(summary[0],summary[1])
	return summaryMap

def PlotPieChart(testSummaryMap):		
	label =[]
	values=[]
	testSuiteName=''
	
		
	for i,j in testSummaryMap:
		if (TEST_PASS_COUNT in i or TEST_FAIL_COUNT in i or TEST_OTHER_COUNT in i):
			label.append(i)
			values.append(j)
		if(TESTSUITE_COULMN_NAME in i):
			testSuiteName = j
	print label,values
	colors = ['green', 'red', 'yellow']
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	pyplot.axis("equal")
	# The slices will be ordered and plotted counter-clockwise.
	explode = (0.1, 0.1, 0.1)
	pyplot.pie(values, explode=explode, labels=label, autopct="%1.1f%%", colors=colors, shadow=True)
	pyplot.title(testSuiteName+" Functional Tests Statistics")
	
	if not os.path.exists("TDK_FunctionalGraph/"):
		os.makedirs("TDK_FunctionalGraph/")
	
	pyplot.savefig("TDK_FunctionalGraph/"+testSuiteName+'.png', bbox_inches='tight')			
	pyplot.clf()

def displayUsage ():
        print "USAGE:"
        print "python plotPieChart.py <ReportName> <SheetName>"

col_value = []
funcNameMappingWithReadings=[]	
if len(sys.argv) == 3:
	displayUsage();
	funcMap=ParseTestSummary(str(sys.argv[1]), str(sys.argv[2]))
	PlotPieChart(funcMap)

else:
        print "argument passed are not equal to 2\n"
        displayUsage()
