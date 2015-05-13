import re
import sys
import os

def addingRelevance(fileName):
	primitiveTestName=[]
	functionName=[]
	flag=0
	lineNumber=0
	with open (scriptfolder+'/'+fileName, 'r+') as f:
		data=f.readlines()
		for line in data:
			lineNumber=lineNumber+1

			if re.search('<primitive_test_name>',line):
				primitiveSplit=line.split('>')
				primitiveTestName=primitiveSplit[1].split('<')[0]

			if re.search('createTestStep', line):
				#i=i+1
				#print line
				funcName=line.split('\'')
				functionName=funcName[1]
				#print "******************"
				#print funcName
				#print functionName
				#print primitiveTestName
				#print "******************"
				if(primitiveTestName not in functionName):
					flag=flag+1
					if(flag==1):
						#print "++++++"
						temp=funcName[0]+'\''+funcName[1]+'\''+',0);\n'
						data.insert(lineNumber,temp)
						data.remove(line)
						#print temp
				flag=0
				if(primitiveTestName==functionName):
					flag=flag+1
					temp=line.split('\'')
					if(flag==1):
						temp=temp[0]+'\''+primitiveTestName+'\''+',5);\n'
						#print line
						#print temp
						data.insert(lineNumber,temp)
						data.remove(line)
					
		f.truncate(0)        # truncates the file
	   	f.seek(0) 				# move pointer to first line
		f.writelines(data)

scriptfolder=sys.argv[1]
for file in sorted(os.listdir(scriptfolder)):
	if file.endswith(".py"):
		#print "*******************"
		#print file
		#print "*******************"
		addingRelevance(file)
	else:
		print "---excluded--- "+file

