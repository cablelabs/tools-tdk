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
import sys
sys.path.insert(0, "../python-lib/")
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt 
from xlwt import Workbook
import os
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import xlrd
import subprocess
import time
import datetime
import shutil

import glob

#logsfolder="./TEMP/ajan"




def parsefile (fileName):
	fileExists=False
	dom = xml.dom.minidom.parse(logsfolder+"/"+fileName)
#	print dom.toprettyxml(indent='\t')
	componentName=dom.getElementsByTagName('TestCase')[0].attributes['componentName'].value

	#Check  all .test files if a .test already started for  a component 
	files = glob.glob('*.test') 
	for f in files: 
		#print "---file " +f+" comp: "+componentName
		if f == (str( componentName)+".test")  : #if a .test file already exists for a component , use it , otherwise create a new.
			fileExists=True 
			componentFile=open(f,"a")
			break
		
	if fileExists==True:
		print "already added"
	else:#if a .test file already exists for a component , use it , otherwise create a new.
		componentFile=open(componentName+".test",'w+')
		print "Writing "+ componentName+".test"


	#testPlanName is the test script name stripped from twc_ and _xmllog etc. 
	testPlanName=fileName.replace("_xmllog.xml","")
	testPlanName=testPlanName.replace("twc_TWC_","")
	testPlanName=testPlanName.replace("_ITER","")

	
	testPlanDescription ="Video" #fixed as constant -- TODO need to change this.
	executionMethod="TDK"  # as per SIT , SWORD requirement this is always TDK.
	testCaseName=dom.getElementsByTagName('TestCase')[0].attributes['name'].value
	testCaseDescription="testCaseDescription"
	testCaseType=dom.getElementsByTagName('TestCase')[0].attributes['testType'].value
	
	testFunctions=dom.getElementsByTagName('TestFunction')
	for testFn in testFunctions:
		testCaseName= testFn.attributes['name'].value 
		componentFile.write(testPlanName+","+testPlanDescription+","+testPlanDescription+","+executionMethod+","+testCaseName+","+testCaseDescription+","+testCaseType+"\n")		
	componentFile.close()	
def displayUsage ():

	print "USAGE:"
	print "generatecsv.py <logsfolder>"

	print "generatecsv program generates csv files which is required for generating xls sheets for SWORD integration"
	print "All result xml logs from <logsfolder> is parsed and one .test file for each component is generated in the current folder"
	print "Plesae note that all TDK tests are not generating the compatible xml logs with this program . For example some tests do not have the componentName attribute. This may cause a script error"
	
if len(sys.argv) != 2:
	displayUsage()
else:

	displayUsage()
	logsfolder=sys.argv[1]

	print "going to generate csv fiels ( .test) for xml files in folder : "+ str(logsfolder)
	for file in sorted(os.listdir(logsfolder)):
		if file.endswith("_xmllog.xml") and not file.endswith("invalid_xmllog.xml") :
			print file
			parsefile(file)
		else:
			print "---excluded--- "+file

