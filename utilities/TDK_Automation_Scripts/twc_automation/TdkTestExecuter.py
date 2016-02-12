from __future__ import with_statement # Required in 2.5
import sys
sys.path.insert(0, "../python-lib/")
import os
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import subprocess
import time
import datetime
from time import gmtime, strftime;
import shutil
import MySQLdb
import re
import signal
from contextlib import contextmanager
from setEnvironmentVariable import setEnvironmentVariable
from validateTdkConfig import validateTdkConfig
from TdkTestProgressbar import Progress_Bar
import thread
import socket
import tdklib
from resetAgent import resetAgent
from DownloadRemoteFile import DownloadRemoteFile
from ScheduleTestExecution import calTimeDiff
from logcapture import captureLogs
import random
TDK_CONFIG_FILE=""
isDatabase = False

#Added code for implementing Test Timout
class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Test Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

if (len(sys.argv) >1):
	if (len(sys.argv) >=2  and str(sys.argv[1]).endswith(".xml")):
		print "TDK Test Configuration file Input...." + str(sys.argv[1]) + "\n"
		TDK_CONFIG_FILE = (str(sys.argv[1]))
else:
	print "No TDK Test Configuration file Input.... \n Reading Default Configuration file (./TdkConfig.xml).... \n"
	TDK_CONFIG_FILE = 'TdkConfig.xml'

#Validation of Tdkconfig.xml using validateTdkConfig.py
#Checks whether TdkConfig.xml is existing in the directory####
validationresult = ''
try:
	validationresult=validateTdkConfig(TDK_CONFIG_FILE)
except Exception as e:
	print e.message
except IOError as e:
	print "Please add TdkConfig.xml to current directory !!"
	print e.message
	sys.exit()
if(validationresult is not None or validationresult != ''):       	
	dom = xml.dom.minidom.parse(str(TDK_CONFIG_FILE))
	component = dom.getElementsByTagName('TestSuite')

	env = dom.getElementsByTagName('TestEnvironment')
	TARGET_IP = ''
	LOG_PATH = ''
	#logType = str(sys.argv[2])
	if(len(sys.argv) == 3):
		TARGET_IP = str(sys.argv[2])
	else:
		TARGET_IP = env[0].getElementsByTagName('TARGET_IP')[0].childNodes[0].nodeValue
	BUILD_VER = env[0].getElementsByTagName('BUILD_VER')[0].childNodes[0].nodeValue
	RDK_VER = env[0].getElementsByTagName('RDK_VER')[0].childNodes[0].nodeValue
	BOX_TYPE = env[0].getElementsByTagName('BOX_TYPE')[0].childNodes[0].nodeValue
	TEST_MANAGER_URL = str(env[0].getElementsByTagName('TEST_MANAGER_URL')[0].childNodes[0].nodeValue)
	RESRC_PUBLISHER_LINK = str(env[0].getElementsByTagName('RESRC_PUBLISHER_LINK')[0].childNodes[0].nodeValue)
	devicePort=env[0].getElementsByTagName('Device_Port')[0].childNodes[0].nodeValue
	#Quick fix for Test Manager URL issue
	if TEST_MANAGER_URL.endswith("/"):
	        TEST_MANAGER_URL = TEST_MANAGER_URL[:-1]

	try:
		LOG_PATH = str(env[0].getElementsByTagName('LOG_PATH')[0].childNodes[0].nodeValue)
		print "Given LOG_PATH is: "+LOG_PATH
		if (os.access(LOG_PATH, os.R_OK)):
			print "Inside PATH"			
			if (os.path.exists(LOG_PATH+"/logs")): 
				print "PATH Exists"
				if((os.access(LOG_PATH+"/logs", os.W_OK)) and (os.access(LOG_PATH+"/logs", os.R_OK))):
					LOG_PATH = LOG_PATH
				else:
					LOG_PATH = str(os.getcwd())
			else:
				print "Creating folder: "+LOG_PATH+"/logs"
				os.makedirs(LOG_PATH+"/logs")	
		else:
			print "Given LOG_PATH is not accessible so using current directory"
			LOG_PATH = str(os.getcwd())
	except Exception as e:
		print "Inside Exception: ",e.message
		LOG_PATH = str(os.getcwd())
	if not os.path.exists(LOG_PATH+"/logs"):
		print "Creating folder: "+LOG_PATH+"/logs"
		os.makedirs(LOG_PATH+"/logs")		

	DEV_NAME = env[0].getElementsByTagName('DEV_NAME')[0].childNodes[0].nodeValue
	PORT_ID = env[0].getElementsByTagName('PORT_ID')[0].childNodes[0].nodeValue
	Database_Name = env[0].getElementsByTagName('Database_Name')[0].childNodes[0].nodeValue
	Database_Host = env[0].getElementsByTagName('Database_Name')[0].attributes['host'].value
	Database_Username = env[0].getElementsByTagName('Database_Name')[0].attributes['username'].value
	Databse_Password = env[0].getElementsByTagName('Database_Name')[0].attributes['password'].value
	logEnable = env[0].getElementsByTagName('LogCapture')[0].childNodes[0].nodeValue
	#Test_Scheduling = env[0].getElementsByTagName('Test_Scheduling')[0].childNodes[0].nodeValue

	COMMON_XML_LOGS_PATH = ''
	TDK_LOG_PATH=''

	#Setting environment variable in STB using setEnvironmentVariable.py
	if ('HUMAX' in str(DEV_NAME)):
		variablename="RESRC_PUBLISHER_LINK"
		returnvalue=setEnvironmentVariable(TARGET_IP,int(devicePort),variablename,RESRC_PUBLISHER_LINK)
		if returnvalue:
			print "Environment variable is set"
		else:
			print "Evironment variable is not set"	
	if env[0].getElementsByTagName('COMMON_XML_LOGS_PATH')[0].attributes['enabled'].value == "true":
		COMMON_XML_LOGS_PATH_ENABLED=True
		COMMON_XML_LOGS_PATH=env[0].getElementsByTagName('COMMON_XML_LOGS_PATH')[0].childNodes[0].nodeValue
		print "COMMON_XML_LOGS_PATH Enabled."
		if(COMMON_XML_LOGS_PATH_ENABLED==True):
			try:	
				if not os.path.exists(COMMON_XML_LOGS_PATH):
					os.makedirs(COMMON_XML_LOGS_PATH)
				else:	
					shutil.rmtree(COMMON_XML_LOGS_PATH)#remove if ther is a file called LOGS_PATH
					os.makedirs(COMMON_XML_LOGS_PATH)
			except Exception as e:
				print "Error in creating "+ COMMON_XML_LOGS_PATH + " Pls check permissions !!"
				print e.message
				sys.exit()
	
	else:
		COMMON_XML_LOGS_PATH_ENABLED=False
		print "COMMON_XML_LOGS_PATH NOT Enabled."
	
	if ('HUMAX' in str(DEV_NAME)):
		if(logEnable.lower() == "true"):
			#Capturing logs using logread
			destination = "/var"
			logType = "logread"
			logreadOutput = captureLogs(str(TARGET_IP), int(devicePort),"start",str(logType),str(destination))
			#Capturing logs using log2usb
			'''logType = "log2usb"
			destination = "/mnt/data/"
			log2usbOutput = captureLogs(str(TARGET_IP), int(devicePort),"start",str(logType),str(destination))
			'''
	
	EXEC_NAME=""
	EXEC_ID=""
	EXEC_RESID=""
	EXEC_DEVID=""
	RDK_VERSION=str(re.findall("\d+.\d+", RDK_VER)[0])
	scriptCount=0
	TEST_SUITE_NAME=""
	TEST_SUITE_EXECUTION_TIME=0
	TEST_SUITE_START_TIME=0
	TEST_SUITE_END_TIME=0
	SCRIPT_TIMEOUT=0
	invalidXMLCount=0
	validXMLCount=0
	outLog=""
	TEST_EXEC_STATUS=""
	testcaseID = 153
	deviceId = 2279
	
	
	def printlog(strToLogAndPrint):
		global outLog
		print strToLogAndPrint
		outLog=outLog+"\n"+strToLogAndPrint
		
	printlog( "TARGET_IP: "+ TARGET_IP)
	printlog( "BUILD_VER: "+ BUILD_VER)
	printlog( "RDK_VER: "+ RDK_VERSION)
	printlog( "BOX_TYPE: "+ BOX_TYPE)
	printlog( "TEST_MANAGER_URL: "+ TEST_MANAGER_URL)
	printlog( "RESRC_PUBLISHER_LINK:"+RESRC_PUBLISHER_LINK)
	printlog( "LOG_PATH: "+ LOG_PATH)
	printlog( "DEV_NAME: "+ DEV_NAME)
	printlog( "PORT_ID: "+ PORT_ID)
	
	
	def fetchLastExecutionId():
	# fetch last inserted executionId from the database
	# Description  : fetch last inserted executionId from  execution table of database
	# Parameters   :
	# Return Value : executionId
		global isDatabase
		lastExecutionId = 0
		try:
			conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
			cur = conn.cursor()
			query = "SELECT id FROM execution ORDER BY id DESC limit 1";
			cur.execute(query);
	
			lastExecId = [];
			if cur.rowcount > 0 :
				lastExecId = list(cur.fetchall());
			else:
				lastExecId[0] = 1
	
			for execId in lastExecId:
				printlog( str((execId[0] + 1)))
	
			conn.commit();
			conn.close();
			lastExecutionId	 = execId[0]+1
			isDatabase = True
	           	return lastExecutionId;

		except (MySQLdb.Error, MySQLdb.DataError), sqlErr:
                        lastExecutionId = random.randint(0, 32767) 
			print "Random ExecutionId generated %d" %lastExecutionId
			print "ERROR: Exception in SQL Database while fetching LastExecutionId. \nException type is: %s" %sqlErr
			return lastExecutionId

		except Exception, e:
			lastExecutionId = random.randint(0, 32767) 
			printlog( "ERROR : exception in fetching last executionId!\n")
			print "Exception type is: %s"%e
			return lastExecutionId			
	
	def fetchLastExecutionDeviceId():
	# fetch last inserted executionDeviceId from the database
	# Syntax       : fetchLastExecutionDeviceId();
	# Description  : fetch last inserted executiondeviceId from  execute_method_result table of database
	# Parameters   :
	# Return Value : executemethodresultId
		global isDatabase
		lastExecutionDeviceId=0
		try:
			conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
			cur = conn.cursor()
			query = "SELECT id FROM execution_device ORDER BY id DESC limit 1";
			printlog( query)
			cur.execute(query);
			lastExecDevId = [];
			if cur.rowcount > 0 :
				lastExecDevId = list(cur.fetchall());
			else:
				lastExecDevId[0] = 1
			printlog( "Row(s) fetched  :" +  str(cur.rowcount))
			printlog( "Last ExecutionDeviceId fetched from the database is:"+ str(lastExecDevId[0]))
			for execDevId in lastExecDevId:
				printlog( str(execDevId[0]))
			conn.commit();
			conn.close();
			lastExecutionDeviceId = execDevId[0]
			isDatabase = True
			return lastExecutionDeviceId;
                
		except (MySQLdb.Error, MySQLdb.DataError), sqlErr:
			lastExecutionDeviceId = random.randint(0, 32767)
			print "Random ExecutionDeviceId generated %d" %lastExecutionDeviceId
			print "ERROR: Exception in SQL Database while fetching LastExecutionDeviceId. \nException type is: %s" %sqlErr
			return lastExecutionDeviceId

		except Exception, e:
			lastExecutionDeviceId = random.randint(0, 32767)
			printlog( "ERROR : exception in fetching last executionDeviceId!\n")
			print "Exception type is: %s" %e;
			return lastExecutionDeviceId
	
	def fetchLastExecutionResultId():
	# fetch last inserted executionresultId from the database
	# Syntax       : obj.fetchLastExecutionResultId();
	# Description  : fetch last inserted executionresultId from  execution_result table of database
	# Parameters   :
	# Return Value : executionresultId
		global isDatabase
		lastExecutionResultId=0
		try:
			conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
			cur = conn.cursor()
			query = "SELECT id FROM execution_result ORDER BY id DESC limit 1";
			cur.execute(query);
			lastExecResId = [];
			if cur.rowcount > 0 :
				lastExecResId = list(cur.fetchall());
			else:
				lastExecResId[0] = 1
			print "list value: ", lastExecResId;
			print "Row(s) fetched :" +  str(cur.rowcount);
			print "Last ExecutionId fetched from the database is:", lastExecResId[0];
			for execResId in lastExecResId:
			        print execResId[0]
			conn.commit();
			conn.close();
			lastExecutionResultId=execResId[0]
			isDatabase = True
			return lastExecutionResultId;

		except (MySQLdb.Error, MySQLdb.DataError), sqlErr:
			lastExecutionResultId = random.randint(0, 32767)
			print "Random ExecutionResultId generated %d" %lastExecutionResultId
			print "ERROR: Exception in SQL Database while fetching LastExecutionResultId. \nException type is: %s" %sqlErr
			return lastExecutionResultId

		except Exception, e:
			lastExecutionResultId = random.randint(0, 32767)
			print "ERROR : exception in fetching last executionResultId!\n";
			print "Exception type is: %s" %e;
			return lastExecutionResultId
		else:
			print "Unload module Success\n"
	
	def UpdateOpenSrcXMLData (XMLlogFile,componentName, testSuiteName, testType):
		lowRelevanceMethods=["initTestCase","cleanupTestCase"]
		
		#print "UpdateOpenSrcXMLData - ENTRY" + XMLlogFile
	 	try:
			dom = xml.dom.minidom.parse(XMLlogFile)
	
	        	testScriptOrCase = dom.getElementsByTagName('TestCase')
	        	testScriptOrCase[0].setAttribute("componentName",componentName)
	        	testScriptOrCase[0].setAttribute("testSuiteName",testSuiteName)
	        	testScriptOrCase[0].setAttribute("testType",testType)
			testScriptOrCase[0].setAttribute("description","Test for "+componentName)
	
	        	testFns = testScriptOrCase[0].getElementsByTagName('TestFunction')
	
		        for testFn in testFns:
		                if testFn.attributes['name'].value in lowRelevanceMethods:
	        	                testFn.setAttribute("relevance","0")
	                	else:
	                        	testFn.setAttribute("relevance","5")
				testFn.setAttribute("description","Test for "+testFn.attributes['name'].value)
			env=testScriptOrCase[0].getElementsByTagName('Environment')
			
			if componentName=='GStreamer':
					componentVersion="GstVersion"
		
			if componentName =='QtWebkit':
					componentVersion="QtVersion"
			firstElement = env[0].getElementsByTagName(componentVersion)
			newline = dom.createTextNode('\n\t\t')
		#addTxtEle("execId",str(EXEC_ID))
			hnode = dom.createElement('execId')
			htext = dom.createTextNode(str(EXEC_ID))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
			#addTxtEle("execResId",str(EXEC_RESID))
			hnode = dom.createElement('execResId')
			htext = dom.createTextNode(str(EXEC_RESID))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
			#addTxtEle("execDeviceId",EXEC_DEVID)
			hnode = dom.createElement('execDeviceId')
			htext = dom.createTextNode(str(EXEC_DEVID))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
			#addTxtEle("testcaseID",testcaseID)
			hnode = dom.createElement('testcaseID')
			htext = dom.createTextNode(str(testcaseID))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
			#addTxtEle("deviceId",deviceId)
			hnode = dom.createElement('deviceId')
			htext = dom.createTextNode(str(deviceId))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
		
			#addTxtEle("deviceIp",TARGET_IP)
			hnode = dom.createElement('deviceIp')
			htext = dom.createTextNode(str(TARGET_IP))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
		
			#addTxtEle("path",LOG_PATH)
			hnode = dom.createElement('path')
			htext = dom.createTextNode(str(LOG_PATH))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
		
			#addTxtEle("executionName",EXEC_NAME)
			hnode = dom.createElement('executionName')
			htext = dom.createTextNode(str(EXEC_NAME))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
	
			#addTxtEle("componentName",componentName)
			hnode = dom.createElement('componentName')
			htext = dom.createTextNode(str(componentName))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
	
			#addTxtEle("rdkversion",RDK_VERSION)
			hnode = dom.createElement('rdkversion')
			htext = dom.createTextNode(str(RDK_VERSION))
			hnode.appendChild(htext)
			env[0].insertBefore(hnode,firstElement[0])
			env[0].insertBefore(newline,firstElement[0])
	
			#print dom.toxml()
		        f=open(XMLlogFile,'w')
		        f.write(dom.toprettyxml())
		        f.close()
			#print "UpdateOpenSrcXMLData - EXIT"
		except Exception, e:
			printlog( "ERROR : exception while parsing xml file in UpdateOpenSrcXMLData method!\n")
			print "Exception type is: %s" %e;
	def Execute_Tests (testscript,soName,scriptlocation,component,testtype, TEST_SUITE_NAME):
		global invalidXMLCount
		global validXMLCount
		global TEST_PASS_COUNT
		global TEST_FAIL_COUNT
		rValue = 0;
		
		if  os.path.exists(scriptlocation+"/"+testscript+".py") == False:
			return "Error :  "+scriptlocation+"/"+testscript+".py   Script file does not exist!"
		printlog( "---EXEC_ID, EXEC_DEVID,testscript:"+str(EXEC_ID)+" "+str(EXEC_RESID)+" "+str(EXEC_DEVID)+" " +testscript)
		command="python  commonTestScript.py" + " "+ TARGET_IP +" "+ PORT_ID +" "+ LOG_PATH +" "+TEST_MANAGER_URL +" "+EXEC_NAME+" 	"+testscript+" "+soName+" "+scriptlocation+" "+component+" "+testtype+" "+str(EXEC_ID)+" "+str(EXEC_DEVID)+" "+RDK_VERSION+" " + 	TEST_SUITE_NAME + " "+str(EXEC_RESID)+" " +" >"+LOG_PATH+"/logs/"+testscript+".log"
		printlog( command)
		try:
			print "Script Timeout Value is (in min.): " + str(SCRIPT_TIMEOUT)
			executionTime = 0
			executionTime = int(SCRIPT_TIMEOUT)
			start = datetime.datetime.now()
			
			process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			execTime = int(SCRIPT_TIMEOUT) * 60
			
			#To display Progress Indicator during command line execution.
			while process.poll() is None:
				execTime = execTime - 1
				time.sleep(0.1)
				now = datetime.datetime.now()
				#print now
				if (now - start).seconds > (int(SCRIPT_TIMEOUT) * 60) or rValue > 98.0:
					print "\nScript Timed Out!"
					#print ((now - start).seconds)
					os.kill(process.pid, signal.SIGKILL)
					os.waitpid(-1, os.WNOHANG)
					return False
				else:
					rValue = Progress_Bar (execTime, TEST_SUITE_NAME)
					#print execTime
			hashes = "#" * 100
			spaces = ' ' * (100 - len(hashes))
			sys.stdout.write("\rPercent: [{0}] {1:.2f}%".format(hashes + spaces, (100)))
			print "\n"
			#Transferring AgentConsole logs from HUMAX STB to server
			if ('HUMAX' in str(DEV_NAME)):
				PORT=69
				localLogPath="TDKLOGS/"+TEST_SUITE_NAME+"/AgentConsoleLogs/"+ testscript +"_AgentConsole.log"
				if not os.path.exists(os.path.dirname(localLogPath)):
					try:
                        	        	print "Creating directory ...::" ,os.path.dirname(localLogPath)
                                		sys.stdout.flush()
                                		os.makedirs(os.path.dirname(localLogPath))
		                        except OSError as exception:
        		                        if exception.errno != errno.EEXIST:
                		                        raise
				RemoteFilePath="/var/tdk/logs/AgentConsole.log"
				DownloadRemoteFile(TARGET_IP, PORT, localLogPath, RemoteFilePath)
		except TimeoutException, msg:
			print "\nScript Timed out!"
			return False
	
		currentdir=os.path.dirname(os.path.realpath(__file__))
		printlog( "Current Path :"+os.path.dirname(os.path.realpath(__file__))) 
		log_path=LOG_PATH
		for line in open(LOG_PATH+"/logs/"+testscript+".log"):
			if "--**--log_path--**--" in line:
				log_path=line.split("--**--log_path--**--")[1]
				break
	
		printlog( "log_path="+log_path)
		if(COMMON_XML_LOGS_PATH_ENABLED==True):
			try:	
				if not os.path.exists(COMMON_XML_LOGS_PATH+"/"+ TEST_SUITE_NAME+"/"):
					os.makedirs(COMMON_XML_LOGS_PATH+"/"+ TEST_SUITE_NAME)
				#else:	
					#shutil.rmtree(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"+TEST_SUITE_NAME+"/")#remove if ther is a file called 	LOG_PATH
					#os.makedirs(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"+TEST_SUITE_NAME+"/")
			except Exception as e:
				print "Error in creating "+COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+ " Pls check permissions !!"
				print e.message
				sys.exit()
	
		if component=='GStreamer' or component =='QtWebkit':
			printlog( "qtorgst = True ")
			ls_dir = os.listdir(log_path)
			for pfile in ls_dir:
				xmlLogFile=log_path+"/"+ pfile	
				
				if "TestSummary" not  in pfile and (not pfile.endswith("_xmllog.xml")):#do not clean up testsummary file
					try:
						command = "awk "+ "'" + "$1 ~ /^</ || $NF ~ />$/" + "' "+ xmlLogFile + ">>temp.xml"
						subprocess.call([command], shell=True)
						command = "cat " + 'temp.xml' + ">> "+xmlLogFile +"_xmllog.xml"
						subprocess.call([command], shell=True)
						command = "rm " +'temp.xml'
						subprocess.call([command], shell=True)
						command = "sh xml_check.sh " + xmlLogFile+"_xmllog.xml"
						subprocess.call([command], shell=True)
						if validateXML(xmlLogFile+"_xmllog.xml") == False:
							invalidXMLCount=invalidXMLCount+1
							os.rename(xmlLogFile+"_xmllog.xml",xmlLogFile+"_invalid_xmllog.xml")
							xmlLogFile=xmlLogFile+"_invalid_xmllog.xml"
						else:
							validXMLCount=validXMLCount+1
							xmlLogFile=xmlLogFile+"_xmllog.xml"
	
						#Update XML file with data
						UpdateOpenSrcXMLData(xmlLogFile, component, TEST_SUITE_NAME, testtype);
						printlog("xml:"+xmlLogFile)
						if(COMMON_XML_LOGS_PATH_ENABLED==True):
							shutil.copy2(xmlLogFile,COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")

					except IOError:
							printlog(('File reading/writing issues : "' + log_path+"/" + pfile + '" '))		
							printlog('or File reading/writing issues : temp.xml')
							printlog( 'or File reading/writing issues :'+log_path + "/" + pfile+"_xmllog.xml")
					
					except Exception, e:
						printlog( "*Error in checking result log file ..!!!!")
						print e.message
							
		else:
			#TransferAgentLogs(TARGET_IP,component,testscript)
			try:
				xmlLogFile=log_path+"/"+testscript
				if validateXML(xmlLogFile+"_xmllog.xml") == False:
					invalidXMLCount=invalidXMLCount+1
					os.rename(xmlLogFile+"_xmllog.xml",xmlLogFile+"_invalid_xmllog.xml")
					xmlLogFile=xmlLogFile+"_invalid_xmllog.xml"
	
				else:
					validXMLCount=validXMLCount+1
					xmlLogFile=xmlLogFile+"_xmllog.xml"
	
				#Fix Test function descriptions
	 			dom = xml.dom.minidom.parse(xmlLogFile)
	        		testFns = dom.getElementsByTagName('TestFunction')
	
			        for testFn in testFns:
					if "none" in testFn.attributes['description'].value :
						testFn.setAttribute("description","Test for "+testFn.attributes['name'].value)
					else:
						testFn.setAttribute("description",testFn.attributes['description'].value)
	
	        		f=open(xmlLogFile,'w')
			        f.write(dom.toprettyxml())
				f.close()
	
				if(COMMON_XML_LOGS_PATH_ENABLED==True):
					shutil.copy2(xmlLogFile,COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")
			except IOError:
				printlog(('File reading/writing issues : '+xmlLogFile+'_xmllog.xml'))
				printlog('or File reading/writing issues : temp.xml')
			except :
				printlog( "Error in checking result log file ..!!!!")
	
	

		printlog("\n\n--------")
		subprocess.call("grep error -i "+ LOG_PATH+"/logs/"+testscript+".log", shell=True)
		subprocess.call("grep exception -r "+ LOG_PATH+"/logs/"+testscript+".log", shell=True)
		printlog( "Check the log files for test automation logs at:"+LOG_PATH+"/logs/"+testscript+".log")
		printlog( "xml logs at : 	"+ log_path)
		printlog("--------")
		return True

	def validateXML(xmlFile):
		try:
			dom = xml.dom.minidom.parse(xmlFile)
		except Exception, e:
			printlog( "Invalid XML file ",xmlFile)
			printlog( e.message)
			return False
		else:	
			return True
		
	def cbBeforeExecutingATestSuite(testSuiteName):
		global EXEC_ID
		global EXEC_RESID
		global EXEC_DEVID
		global EXEC_NAME
		global EXEC_START_TIME
		global isDatabase
		EXEC_ID=int(fetchLastExecutionId())+1
		printlog( "EXEC_ID="+str(EXEC_ID))
		EXEC_RESID=int(fetchLastExecutionResultId())+1
		printlog( "EXEC_RESID="+str(EXEC_RESID))
		EXEC_DEVID=int(fetchLastExecutionDeviceId())+1
		printlog( "EXEC_DEVID="+str(EXEC_DEVID))
	
	        EXEC_NAME=DEV_NAME+"-"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	
		executionDate = strftime("%Y-%m-%d %H:%M:%S", gmtime());
		printlog( "Date of Execution: "+ str(executionDate))
		devName=DEV_NAME
		printlog( "Device Name: "+str(devName))
	
		EXEC_START_TIME=time.time()
		if(isDatabase):
			conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
			cur = conn.cursor()
	
			executionTime="0"
			query1 = """INSERT INTO execution (
				id,
				version,
				date_of_execution,
				device,
				device_group,
				execution_time,
				is_marked,
				name,
				output_data,
				result,
				script,
				script_group,
				groups_id,
				execution_status,
				is_performance_done,
				is_aborted,
				is_bench_mark_enabled,
				is_rerun_required,
				is_system_diagnostics_enabled,
				script_count) VALUES ('%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s', NULL,'COMPLETED', 0,0,0,0,0,0)""" %(EXEC_ID,
				RDK_VERSION,
				executionDate,
				devName,
				"NULL",
				executionTime,
				0,
				EXEC_NAME,
				"",#outputdata
				"UNDEFINED",
				testSuiteName,# This is script Name . But Time being using the group name in order to show in the execution list.
				testSuiteName);#This is the script Group Name
			try :
				cur.execute(query1);
				printlog( "Row(s) updated :" +  str(cur.rowcount)+" in table: execution")
				conn.commit();
			except Exception ,e:
				printlog( str(e))
				printlog( "----Exception----"+e.message)
	
			query4 = "INSERT INTO execution_device (id, version, date_of_execution, device, device_ip, execution_id, execution_time, status) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (EXEC_DEVID, RDK_VERSION, executionDate, devName, TARGET_IP, EXEC_ID, executionTime, "FAILURE");
			try :
				cur.execute(query4);
				printlog( "Row(s) updated :" +  str(cur.rowcount)+" in table: execution_device")
				conn.commit();
			except Exception, e:
				printlog( str(e))
				printlog( "----Exception----"+e.message)
	
			conn.close();
		else:
			print "Database is not available inside cbBeforeExecutingATestSuite.\n"	
	
	def cbAfterExecutingATestSuite():
		global outLog
		global isDatabase
		if(isDatabase):
			try:	
				conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
				cur = conn.cursor()
	
				cur.execute("SELECT COUNT(*)  FROM execution_result  WHERE status='FAILURE' AND execution_id="+str(EXEC_ID))
				queryResult=cur.fetchone()
				if queryResult[0] == 0:
					testSuiteExecutionResult='SUCCESS'
				else:
					testSuiteExecutionResult='FAILURE'
				execEndTime=time.time()
				timeTakenForExecution=execEndTime-EXEC_START_TIME
			
				update_execution_query="UPDATE execution SET result='"+testSuiteExecutionResult+"',output_data='"+outLog+"',script_count="+str	(scriptCount)+",execution_time="+str(timeTakenForExecution)+" where id="+str(EXEC_ID)

				update_execution_device_query="UPDATE execution_device SET status='"+testSuiteExecutionResult+"',execution_time="+str	(timeTakenForExecution)+" where id="+str(EXEC_DEVID)
	
				try :
					cur.execute(update_execution_query);
					printlog( "Row(s) updated :" +  str(cur.rowcount)+" in table: execution")
					conn.commit();
				except Exception ,e:
					printlog( str(e)+"exeception in updating execution table. output_data=outLog could be a huge string, consisting of all print statements.")
					printlog( "----Exception----"+e.message)
			
				try :
					cur.execute(update_execution_device_query);
					printlog( "Row(s) updated :" +  str(cur.rowcount)+" in table: execution_device")
					conn.commit()
				except Exception ,e:
					printlog( str(e)+"exeception in updating execution_device table")
					printlog("----Exception----"+ e.message)
		
			except Exception, e:
				printlog( str(e)+"exeception in method: cbAfterExecutingATestSuite")
				printlog( "----Exception----"+e.message)
			outLog="" # Reset the outLog - The outLog for current testSuite is written to the db . Free outLog for new testSuite logs.
			conn.close();
		else:
			print "Database is not available inside cbAfterExecutingATestSuite.\n"	
		printlog("---"+TEST_SUITE_NAME+"  completed")
		printlog("----------------------------------------------------------")
	
	
	def VerifyTestScriptEnv(scriptlocationBase, testScript):
		global SCRIPT_TIMEOUT;
		CustomTestScript = ""
		printlog("This Function verifies the RDK version and Box type of Test Script: " + scriptlocationBase + testScript);
		ScriptRdkVersionValidityForExecution=False;
		ScriptBoxTypeValidityForExecution=False;
		print "CustomTestScript :"+scriptlocationBase+"/"+testScript+".py"
	
		try:
			CustomTestScript=file(scriptlocationBase+"/"+testScript+".py")
		except:
			print "Exception : Unable to Open file"
	
		for line in CustomTestScript:
			if "</execution_time>" in line:
				SCRIPT_TIMEOUT=(line.split("<execution_time>"))[1].split("</execution_time>")[0]
			if "</rdk_version>" in line:
				scriptrdk_version=(line.split("<rdk_version>"))[1].split("</rdk_version>")[0]
				if RDK_VERSION in scriptrdk_version and ScriptRdkVersionValidityForExecution==False:
					print "Script RDK Version matched"
					ScriptRdkVersionValidityForExecution=True
			if "</box_type>" in line:
				scriptbox_type =(line.split("<box_type>"))[1].split("</box_type>")[0]
				if BOX_TYPE in scriptbox_type and ScriptBoxTypeValidityForExecution == False:
					print "Script Box Type matched"
					ScriptBoxTypeValidityForExecution=True
		if ScriptRdkVersionValidityForExecution and ScriptBoxTypeValidityForExecution :
			print "Script RDK Version and Box Type matched..."
		else:
			if(ScriptRdkVersionValidityForExecution != True):
				print "#################################"
				print '*** Script RDK Version not supported...! ***'
				print "#################################"
				return False #FAILURE
			if(ScriptBoxTypeValidityForExecution != True):
				print "#################################"
				print '*** Script Box Type not supported...! ***'
				print "#################################"
				return False #FAILURE
	
		return True #SUCCESS
		
	def executionDetails(r):
			
		testManagerURL = str(TEST_MANAGER_URL).split('/')
		testManagerIP = str(testManagerURL[2]).split(':')
		agentMonitoringPort = 8088
		deviceStatusCommand = "python ../python-lib/calldevicestatus_cmndline.py " +str(TARGET_IP)+" "+str(agentMonitoringPort)+" "+str(testManagerIP[0])+" \"%s\"" %str(DEV_NAME)
                print "Device Status Monitoring Command: ",deviceStatusCommand
                status = subprocess.check_output([deviceStatusCommand], shell=True)
		print "Device Status: ",status
		if(status.strip()=='HANG'):
			command = "python ../python-lib/callResetAgent.py " +str(TARGET_IP)+" "+str(devicePort)+" true"
                        print str(command)
                        subprocess.call([command], shell=True)
                        printlog("Agent Restarted!!!\n")
			
		for x in range(0,len(component)):
			try:
				x = r
				printlog( "----------------------------------------------------------")
				printlog( "TestSuite:"+TEST_SUITE_NAME)
			
				componentName=component[x].attributes['component'].value
				testType=component[x].attributes['testtype'].value
				
				
				if(component[x].getElementsByTagName('TestExecutionEnabled')[0].childNodes[0].data.lower() == "true"):
					
					printlog( "ENABLED")
					printlog( "----------------------------------------------------------")
			
					runallFlag=True
					soName=component[x].getElementsByTagName('SharedObjectName')[0].childNodes[0].data
			
					if component[x].attributes['name'].value=="GSTREAMER" or component[x].attributes['name'].value=="WEBKIT":
						qtorgst=True#if gstreamer of qt the xml logs are generated from the STB, not in the python
					else:
						qtorgst=False	
	
					testScripts=component[x].getElementsByTagName('TestScripts')
					if 'location' in   testScripts[0].attributes.keys():
						scriptlocationBase=testScripts[0].attributes["location"].value
					else:
						scriptlocationBase="./"
				
					cbBeforeExecutingATestSuite(str(component[x].attributes['name'].value))
					scriptCount=0
					TEST_SUITE_START_TIME=time.time()
		
					printlog( "scriptlocationBase: "+scriptlocationBase)
					if 'runall' in    testScripts[0].attributes.keys():
						if ( testScripts[0].attributes["runall"].value == "true") :
							printlog( "runall = true")  #runall is already initialized as true.
	
							excludelist=[]
							excludeNodes=testScripts[0].getElementsByTagName('exclude')
							for exNode  in excludeNodes:
								excludelist.append(exNode.firstChild.nodeValue	)
	
							for file in sorted(os.listdir(scriptlocationBase)):
								if file.endswith(".py") and file.startswith("twc_") and file[:-3] not in excludelist :
									#Verify Script RDK_VERSION and BOX_TYPE
									if(VerifyTestScriptEnv(scriptlocationBase, file[4:-3])):
										TEST_EXEC_STATUS=Execute_Tests (file[:-3],soName,scriptlocationBase,componentName,testType, 	TEST_SUITE_NAME)
										scriptCount=scriptCount+1	
									else:
										continue
								else:
									printlog( "---excluded--- "+file)
	
							cbAfterExecutingATestSuite()
							continue	#runall completed . continue from top of the loop. ie; go to the next test suite. 	
	
					testScriptNodes=testScripts[0].getElementsByTagName('ScriptName')
					numOfScriptNodes=testScriptNodes.length
	
					excludelist=[]
					excludeNodes=testScripts[0].getElementsByTagName('exclude')
					for exNode  in excludeNodes:
						excludelist.append(exNode.firstChild.nodeValue	)
		
					for nodeIndex in range(0, numOfScriptNodes):
						if 'location' in   testScriptNodes[nodeIndex].attributes.keys():
							scriptlocation=testScriptNodes[nodeIndex].attributes["location"].value
						else:
							scriptlocation=scriptlocationBase
						if not os.path.exists(LOG_PATH+"/logs"):
							printlog( "Creating folder: "+LOG_PATH+"/logs")
							os.makedirs(LOG_PATH+"/logs")
						testscript= testScriptNodes[nodeIndex].childNodes[0].data
						#Verify Script RDK_VERSION and BOX_TYPE
						if(VerifyTestScriptEnv(scriptlocation, testscript)):
							TEST_EXEC_STATUS=Execute_Tests (testscript,soName,scriptlocation,componentName,testType, TEST_SUITE_NAME)
							scriptCount=scriptCount+1
						else:
							continue
		
					TEST_SUITE_END_TIME=time.time()
					cbAfterExecutingATestSuite()
	
					printlog("-------------------------------------------")
					TEST_SUITE_EXECUTION_TIME = str(time.strftime("%H:%M:%S", time.gmtime(TEST_SUITE_END_TIME - TEST_SUITE_START_TIME)))
					printlog( "TEST_SUITE_START_TIME : " + str(time.strftime("%H:%M:%S", time.gmtime(TEST_SUITE_START_TIME))))
					printlog( "TEST_SUITE_END_TIME : " + str(time.strftime("%H:%M:%S", time.gmtime(TEST_SUITE_END_TIME))))
					printlog( "TEST_SUITE_EXECUTION_TIME : " + TEST_SUITE_EXECUTION_TIME)
					printlog("-------------------------------------------")
	
					#REPORT GENERATION CODE INTEGRATION
					ReportGenerationStatus = str(dom.getElementsByTagName('ReportGenerationEnabled')[x].attributes['status'].value)
					relevanceNumber=str(dom.getElementsByTagName('ReportGenerationEnabled')[x].attributes['relevanceNumber'].value)
                                        tempCurPath=str(os.getcwd())
					os.chdir(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")
					TDK_LOG_PATH = str(os.getcwd())
					os.chdir(tempCurPath)
					if ReportGenerationStatus.lower()=="true" and TEST_EXEC_STATUS==True:
						print "######### REPORT GENERATION ENABLED ##########"
			
						#tempCurPath=str(os.getcwd())
						#os.chdir(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")
						#TDK_LOG_PATH=str(os.getcwd())
						#os.chdir(tempCurPath)
						command = "python generateXLSfile.py " +TDK_LOG_PATH+" "+relevanceNumber+" "+TEST_SUITE_EXECUTION_TIME+" "+str(TDK_CONFIG_FILE)+" "+TEST_SUITE_NAME+"_TestReport.xls"
						print command  
						subprocess.call([command], shell=True)
						#processGenerateXLS = subprocess.Popen([command], shell=True)

						commandFuncGraph = "python plotPieChart.py "+ TEST_SUITE_NAME+"_TestReport.xls TESTS_SUMMARY_SHEET"
						print commandFuncGraph
						subprocess.call([commandFuncGraph], shell=True)
						#processGenerateChart = subprocess.Popen([commandFuncGraph], shell=True)

						if(TEST_SUITE_NAME=='GSTREAMER' or TEST_SUITE_NAME =='WEBKIT' or TEST_SUITE_NAME =='irkey'):

							commandPerfGraph = "python plotGraph.py plotConfig.xml " +TEST_SUITE_NAME+" "+TEST_SUITE_NAME+"_TestReport.xls TESTS_PassFail_STATUS_SHEET"
							print commandPerfGraph
							subprocess.call([commandPerfGraph], shell=True)
							#procssGeneratePerfGraph = subprocess.Popen([commandPerfGraph], shell=True)
																	
					else:
						if  TEST_EXEC_STATUS==False:
							print "######### TEST SCRIPT EXECUTION FAILED ##########"
						if ReportGenerationStatus.lower()=="false":
							print "######### REPORT GENERATION DISABLED ##########"							
				else:
					printlog( "DISABLED")
					printlog( "----------------------------------------------------------")
					
				
			except Exception,e:
				printlog( "Exception Occurred! "+str( e.message))
			printlog("-------------------------------------------")
			printlog( "validXMLCount: 	"+str(validXMLCount))
			printlog( "invalidXMLCount: "+str(invalidXMLCount))
			printlog("-------------------------------------------")
			
			break
	
	
	r = 0
	timeValue = 0
	value = []
	pair = []
	pairValue = []
	executedComp = []

	try:
		pairValue = calTimeDiff()
		if pairValue:
			value = pairValue[0]
			pair = value[0]
			timeValue = pair[0]
		#print len(component)
		
	except:
		print "Test Schedule Tag not defined!!"
		
	restart = True
	posValueNode = []
	negValueNode = []
	
	while True:
		#print "Environment Variable :" + Test_Scheduling		
		if pairValue is not None: 
			if len(pairValue) > 1:
				posValueNode = pairValue[0]
				negValueNode = pairValue[1]
			elif timeValue >= 0 and len(pairValue) == 1:
				posValueNode = pairValue[0]
				negValueNode = []
			elif timeValue < 0 and len(pairValue) == 1:
				posValueNode = []
				negValueNode = pairValue[0]
			else:
				posValueNode = []
				negValueNode = []
		else:
				print "\nTest Schedule either not defined or disabled.\n"
			
		poslength = len(posValueNode)
		neglength = len(negValueNode)
		for x in range(0,len(component)):
			
			try:
				#TODO: Scheduling execution of test cases by using environment tag.
				'''if (Test_Scheduling.lower() == "true"):
					TEST_SUITE_NAME=str(component[x].attributes['name'].value)
					r = x
					print "Executing : " + TEST_SUITE_NAME
					if x == 0:
						while wTime != 0:
							sys.stdout.write("\rWaiting time in seconds : %3d" % wTime)
							sys.stdout.flush()
							wTime = wTime - 1
							time.sleep(1)			
							if wTime == 0:
								print "\n"
								executionDetails(r)
								#executedComp.append(TEST_SUITE_NAME)
								break
					else:
						executionDetails(r)
					print x
					if (x == len(component) - 1):
						restart = True
						break
					else:
						continue
				'''
				if (component[x].getElementsByTagName('Test_Schedule')[0].childNodes[0].data.lower() == "true"):
					TEST_SUITE_NAME=str(component[x].attributes['name'].value)
					if (TEST_SUITE_NAME not in executedComp):
						schedule = component[x].getElementsByTagName('Test_Schedule')[0].childNodes[0].data
						#print schedule
						#print pairValue
						if pairValue is not None:
							if len(pairValue) > 1:
								posValueNode = pairValue[0]
								negValueNode = pairValue[1]
							elif timeValue >= 0 and len(pairValue) == 1:
								posValueNode = pairValue[0]
								negValueNode = []
							elif timeValue < 0 and len(pairValue) == 1:
								posValueNode = []
								negValueNode = pairValue[0]
							else:
								posValueNode = []
								negValueNode = []
						else:
							continue
						
						length = poslength + neglength
						while length != 0:
							posWTime = -1
							posvalues = []
							negvalues = []
							posCompName = ""
							negCompName = ""
							if poslength != 0 and neglength != 0:
								posvalues = posValueNode[0]
								posWTime = posvalues[0]
								posCompName = posvalues[1]
								negvalues = negValueNode[0]
								negCompName = negvalues[1]
							elif neglength != 0:
								negvalues = negValueNode[0]
								negCompName = negvalues[1]

							else:
								posvalues = posValueNode[0]
								posWTime = posvalues[0]
								posCompName = posvalues[1]
						
							if (TEST_SUITE_NAME == posCompName or TEST_SUITE_NAME == negCompName):
								r = x
								print "Index of component " + str(r)
								print "Component going to execute: " + TEST_SUITE_NAME
								if (TEST_SUITE_NAME == posCompName and posWTime > 0):
									while posWTime != 0:
										sys.stdout.write("\rWaiting time in seconds : %3d" % posWTime)
										sys.stdout.flush()
										posWTime = posWTime - 1
										time.sleep(1)			
										if posWTime == 0:
											print "\n"
											executionDetails(r)
											executedComp.append(TEST_SUITE_NAME)
											break
									pairValue = calTimeDiff()
									value = pairValue[0]
									pair = value[0]
									timeValue = pair[0]
									if timeValue >= 0:
										posValueNode = pairValue[0]
										negValueNode = pairValue[1]
									else:
										negValueNode = pairValue[0]
										posValueNode = []
									plength = len(posValueNode)
									nlength = len(negValueNode)
									for i in range(0, (len(executedComp))):
										for j in range(0, plength):
											if (executedComp[i] in posValueNode[j]):
												del posValueNode[j]
												plength = plength - 1
												#print plength
												break
										for k in range(0,nlength):
											#print k
											if (executedComp[i] in negValueNode[k]):
												del negValueNode[k]
												nlength = nlength - 1
												#print nlength
												break
																				
									poslength = len(posValueNode)
									neglength = len(negValueNode)
									break
									
								else:
									print "Executing : " + TEST_SUITE_NAME
									executionDetails(r)
									executedComp.append(TEST_SUITE_NAME)
									pairValue = calTimeDiff()
									value = pairValue[0]
									pair = value[0]
									timeValue = pair[0]
									if timeValue >= 0:
										negValueNode = pairValue[1]
										posValueNode = pairValue[0]
									else:
										negValueNode = pairValue[0]
										posValueNode = []
									length = len(negValueNode)
									for i in range(0, (len(executedComp))):
										for j in range(0, length):
											if (executedComp[i] in negValueNode[j]):
												del negValueNode[j]
												length = length - 1
												#print length
												break
												
									neglength = len(negValueNode)
									poslength = len(posValueNode)
									break
									
							else:
								break							
				elif (component[x].getElementsByTagName('TestExecutionEnabled')[0].childNodes[0].data.lower() == "false" and component[x].getElementsByTagName('Test_Schedule')[0].childNodes[0].data.lower() == "false"):
					if (TEST_SUITE_NAME not in executedComp):
						poslength = len(posValueNode)	
						neglength = len(negValueNode)						
						if neglength != 0 or poslength != 0 and x <= len(component):
							if x == len(component) - 1:
								restart = False
								break
							else:
								continue
						elif (pairValue is None):
							continue
						elif (poslength == 0 and neglength == 0):
							print "\nExecution Completed!!"
							restart = True
							break
						else:
							restart = False
							break				
				elif (component[x].getElementsByTagName('TestExecutionEnabled')[0].childNodes[0].data.lower() == "true"):
					TEST_SUITE_NAME=str(component[x].attributes['name'].value)
					if (TEST_SUITE_NAME not in executedComp):
						r = x
						print "Executing : " + TEST_SUITE_NAME
						executionDetails(r)
						executedComp.append(TEST_SUITE_NAME)
						pairValue = calTimeDiff()
						if pairValue is not None:
							value = pairValue[0]
							pair = value[0]
							timeValue = pair[0]
							if (len(pairValue) > 1):
								posValueNode = pairValue[0]
								negValueNode = pairValue[1]
							elif timeValue >= 0 and len(pairValue) == 1:
								posValueNode = pairValue[0]
								negValueNode = []
							elif timeValue < 0 and len(pairValue) == 1:
								posValueNode = []
								negValueNode = pairValue[0]
						else:
							print "No component left for Scheduling."
							continue
						plength = len(posValueNode)
						nlength = len(negValueNode)
						
						if (poslength != plength or neglength != nlength):
							remPosLength = plength - poslength
							remNegLength = nlength - neglength
							
							for x in range(0,(remPosLength - 1)):
								del posValueNode[x]
							for x in range(0,(remNegLength - 1)):
								del negValueNode[x]
						
						poslength = len(posValueNode)
						neglength = len(negValueNode)
						if x <= len(component) and poslength != 0 or neglength != 0:
							if x == len(component) - 1:
								restart = False
								break
							else:
								continue
						else:
							restart = True
							break
					else:
						restart = True
						break
			
				if poslength != 0 or neglength != 0 and x <= len(component):
					if x == len(component) - 1:
						restart = False
						break
					else:
						continue
				elif pairValue is None:
					continue
				elif (poslength == 0 and neglength == 0):
					print "\nExecution Completed!"
					restart = True
					break
				else:
					restart = False
					break
			
			except IndexError,e:
				if (component[x].getElementsByTagName('TestExecutionEnabled')[0].childNodes[0].data.lower() == "true"):
					TEST_SUITE_NAME=str(component[x].attributes['name'].value)
					print "Executing : " + TEST_SUITE_NAME
					r = x
					executionDetails(r)

			except Exception,e:
				printlog( "Exception Occurred! "+str( e.message))
		if restart:
			break		
	if ('HUMAX' in str(DEV_NAME)):			
		if(logEnable.lower() == "true"):
			logType = "logread"
			time.sleep(10)
			logOutput = captureLogs(str(TARGET_IP), int(devicePort),"stop",str(logType),str(destination))
			time.sleep(3)
			#Download logread logs to Host server
			localLogPath=str(LOG_PATH)+"/TDKLOGS/" + str(EXEC_NAME) +"_logread.log"
			DownloadRemoteFile(TARGET_IP, 69, str(localLogPath), str(logreadOutput))
				
		#Download log2usb logs to Host server
		'''logs2usbOutput = logs2usbOutput + "/*.log"
		localLogPath = str(LOG_PATH)+"/TDKLOGS/log2usb/"
    	DownloadRemoteFile(TARGET_IP, 69, str(localLogPath), str(logs2usbOutput))
		'''					

else:
	print "Error in validation of TdkConfig.xml"
