#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import time
import sys
import re
import os
#import TdkTestExecuter

def Progress_Bar (execTime, testSuiteName):
	rValue = 0
	#print "\nTest Suie Name:"
	#print testSuiteName
	# Open TdkConfig.xml document using minidom parser
	DOMTree = xml.dom.minidom.parse("TdkConfig.xml")
						
	# Store all elements of xml under collection
	collection = DOMTree.documentElement

	# Get all the test suites in the collection
	testSuites = collection.getElementsByTagName("TestSuite")
	try:
		
		# Parsing each test suite.
		for testSuite in testSuites:
			if (testSuite.attributes['name'].value == testSuiteName):
				scriptEnabled = testSuite.getElementsByTagName('TestExecutionEnabled')[0].childNodes[0].nodeValue
				
				# if scriptEnabled is true then only proceed
				if scriptEnabled == "true":
				
					# if TestSuite tag has name attribute then only proceed
					if testSuite.hasAttribute("name"):
						# store all occurence of ScriptName tag in itemlist under each test suite
						itemList = testSuite.getElementsByTagName('ScriptName')
						ScriptCount = len(itemList)
						#print ScriptCount
						time.sleep(1)
						if execTime:
							x = float( 100 / float(execTime))
							
							if ( x < 0.1 ):
								x = x * 100
							if ( x < 1 ):
								x = x * 100
								if (x > 98):
									rValue = x
									break
							rValue = x
							#print x
							hashes = '#' * int (x)
							spaces = ' ' * (100 - len(hashes))
							# Display progress bar on console
							sys.stdout.write("\rPercent: [{0}] {1:.2f}%".format(hashes + spaces, (x)))
							sys.stdout.flush();
							break
			else:
				#print "In else block"
				continue		
				
		return rValue
	except Exception, msg:
		printlog( "Exception Occurred! "+str( msg.message))
		
