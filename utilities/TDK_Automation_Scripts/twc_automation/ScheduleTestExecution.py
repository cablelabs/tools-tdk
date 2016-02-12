from xml.dom import minidom
import time
import subprocess
import sys
import datetime
import xml.dom.minidom
import threading
		
def calTimeDiff():
	try:	
		dom = xml.dom.minidom.parse('TdkConfig.xml')
		testSuites = dom.getElementsByTagName('TestSuite')
		
		posTimeString = []
		negTimeString = []
		posCompName = []
		negCompName = []
		ScheduleStatus = []
		pair = []
		
		for testSuite in testSuites:
			testScheduleStatus = testSuite.getElementsByTagName('Test_Schedule')[0].childNodes[0].nodeValue
			
			if (testScheduleStatus.lower() == 'true'):
				compName = testSuite.attributes['name'].value
				givenTimeString = testSuite.getElementsByTagName('Time')[0].childNodes[0].nodeValue
				if valid_dateTime(givenTimeString) == True:
				
					givenTimestamp = time.mktime(time.strptime(givenTimeString, '%d-%m-%Y %H:%M:%S'))
					currentTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
					currentTimestamp = time.mktime(time.strptime(str(currentTime), '%d-%m-%Y %H:%M:%S'))
					
					timeDiff = givenTimestamp - currentTimestamp
					if (timeDiff >= 0):
						posTimeString.append(timeDiff)
						posCompName.append(compName)
					elif (timeDiff < 0):
						negTimeString.append(timeDiff)
						negCompName.append(compName)
					else:
						return
				else:
					print "Error: Scheduling Date Time format does not match with format <dd-mm-yyy HH:MM:SS(- 24 Hr Format)> in XML file for test suite ====> " + compName
					print "Please Enter the Time in correct format!"	
					exit(1)				
				timeDiff = ""
				compName = ""
			ScheduleStatus.append(testScheduleStatus)
			testScheduleStatus = ""
			
		schStatus = ""
		for status in ScheduleStatus:
			if status == "true":
				schStatus = status
				break
			else:
				continue
		if schStatus == "":
			print "No Component is set as true for scheduling."
			return;
		print "Calculating Time Difference ..."
		pos = zip(posTimeString,posCompName)
		pos.sort()
		#print pos
		neg = zip(negTimeString,negCompName)
		neg.sort()
		#print neg
		if len(pos) == 0:
			pair.append(neg)
		elif len(neg) == 0:
			pair.append(pos)
		else:
			pair.append(pos)
			pair.append(neg)			
		print "List of components scheduled for execution: "
		print pair
		return pair
	except Exception,e:
		#print "Exception Occured! " + str(e.message)
		print "Test Schedule Flag not Found!!!"

def valid_dateTime(dateTimeString):
    try:
        datetime.datetime.strptime(dateTimeString, '%d-%m-%Y %H:%M:%S')
        return True
    except ValueError:
        return False  

'''def envScheduleTimeDifference():
	try:
		dom = xml.dom.minidom.parse('TdkConfig.xml')
		env = dom.getElementsByTagName('TestEnvironment')
		Test_Scheduling = env[0].getElementsByTagName('Test_Scheduling')[0].childNodes[0].nodeValue
		if (Test_Scheduling.lower() == "true"):
			scheduleTime = env[0].getElementsByTagName('Time')[0].childNodes[0].nodeValue
			if valid_dateTime(scheduleTime) == True:
				scheduleTimestamp = time.mktime(time.strptime(scheduleTime, '%d-%m-%Y %H:%M:%S'))
				currentTime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
				currentTimestamp = time.mktime(time.strptime(str(currentTime), '%d-%m-%Y %H:%M:%S'))
					
				timeDiff = scheduleTimestamp - currentTimestamp
				if timeDiff >= 0:
					return timeDiff
				else:
					print "\nTime Specified is less than current time!"
					print "\nPlease Enter time greater than current time for scheduling Execution."
					exit(1)
	except Exception,e:
		print "Exception Occured! " + str(e.message) 
'''   
#calTimeDiff()
