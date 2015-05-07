import re
import sys
import os
import glob

def generateUtilCSV(filesPath, fileName):
	print filesPath
	componentName="testFnInfo"
	#Incase / missed in path at the end
	if not filesPath.endswith('/'):
		filesPath=filesPath+"/"
	fileExists=False
	#Check  all .csv files if a .csv already started for  a component
	files = glob.glob(filesPath+'/*.csv')
	
	for f in files:
		if f == (filesPath+str(componentName)+".csv")  : #if a .csv file already exists for a component , use it , otherwise create a new.
			fileExists=True
			componentFile=open(filesPath+str(componentName)+".csv","a")
			break

	if fileExists==True:
		print "already added"
	else:
		#if a .csv file already exists for a component , use it , otherwise create a new.
		componentFile=open(filesPath+str(componentName)+".csv",'w+')
		print "Writing "+ filesPath+str(componentName)+".csv"
		componentFile.write("TestcaseName,TestFunctionName,RelevanceNumber \n");
	
	with open (filesPath+fileName, 'r+') as f:
		data=f.readlines()
		for line in data:
			if re.search('<name>',line):
				primitiveSplit=line.split('>')
				testcaseName=primitiveSplit[1].split('<')[0]
				print "Testcase Name: %s" %testcaseName
			if re.search('createTestStep', line):
				#print line
				funcName=line.split('\'')
				print "******************"
				print funcName
				testFunctionName=funcName[1]
				print "TestFunction Name: %s" %testFunctionName
				relevanceNumber=funcName[2][1]
				print "Relevance Number: %s" %relevanceNumber
				print "******************"		
				componentFile.write(testcaseName+","+testFunctionName+","+relevanceNumber+"\n")

scriptfolder=sys.argv[1]
for file in sorted(os.listdir(scriptfolder)):
	if file.endswith(".py"):
		print "*******************"
		print file
		print "#################"
		generateUtilCSV(scriptfolder, file)
		print "#################"
	else:
		print "---excluded--- "+file
