#!/usr/bin/python
#COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================

import os
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import sys
import re

PATH = "componentXML/"
#PATH = "/home/abhishek/Faaz/Work_Related/My_Work/Tasks/10th_Jul/componentXML/"

def Primitive_TestCase(componentName, testCase):
	path = PATH
	dirPath = os.path.join(os.path.dirname(__file__),  path )
	#print dirPath
	dirs = os.listdir(dirPath)
	testId = ""
	method = ""
	paramMsg = ""
	jsonMsg = ""
	#print dirs
	dirLength = len(dirs)
	print "Number of xml files present : " + str(dirLength)
	for filename in dirs:
		#print filename
		#print (componentName + ".xml")
		if componentName in filename:
			DOMTree = xml.dom.minidom.parse(dirPath + filename)
			primitiveTests = DOMTree.documentElement.getElementsByTagName("primitiveTest")
			#print primitiveTests
			
			primFuncLength = len(primitiveTests)
			print "Number of Primitive tests : " + str(primFuncLength)
			for primitiveTest in primitiveTests:
				name = primitiveTest.attributes['name'].value
				#print name
				
				if (primitiveTest.attributes['name'].value == testCase):
					testId = primitiveTest.attributes['id'].value
					method = primitiveTest.getElementsByTagName('function')[0].childNodes[0].nodeValue
					#print method
					parameter = primitiveTest.getElementsByTagName('parameter')
					#if primitiveTest.hasAttribute("parameter"):
					if parameter:
						paramLen = len(parameter)
						#print "Length of parameters  :" + str(paramLen)
						
						for param in range(0, paramLen):
							paramName = parameter[param].attributes['name'].value
							value = parameter[param].attributes['value'].value
							paramMsg += ",\"" + paramName + "\":" + "\"" + value + "\""
							
						#print paramMsg
							
						jsonMsg = "{\"id\":\"" +testId+"\",\"jsonrpc\":\"2.0\",\"method\":\""+method+"\"" + paramMsg+"}"
						#print jsonMsg
					else:
						
						jsonMsg = "{\"id\":\"" +testId+"\",\"jsonrpc\":\"2.0\",\"method\":\""+method+"\"}"
						#print jsonMsg	
				else:
					primFuncLength = primFuncLength - 1
				#print "Remaining Numbers of primitive test case : " + str(primFuncLength)
				if primFuncLength == 0:		
					print "\nPrimitive testcase is not defined in Module Configuration XML!!!"
					print "Please define primitive test in module xml."
		else:
			dirLength = dirLength - 1
		if dirLength == 0:
			print "\nModule is not Configured in Test Manager!!"	
			print "Please Configure module."
			
	#print jsonMsg
	return jsonMsg

#Primitive_TestCase("iarmbus", "IARMBUS_InvokeEventTransmitterApp")
