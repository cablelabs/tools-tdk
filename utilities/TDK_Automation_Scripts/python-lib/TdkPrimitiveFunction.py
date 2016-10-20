#!/usr/bin/python
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
