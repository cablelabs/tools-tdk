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

TDK_CONFIG_FILE=""

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
	if len(sys.argv) == 2 and str(sys.argv[1]).endswith(".xml"):
		print "TDK Test Configuration file Input...." + str(sys.argv[1]) + "\n"
		TDK_CONFIG_FILE = (str(sys.argv[1]))
else:
	print "No TDK Test Configuration file Input.... \n Reading Default Configuration file (./TdkConfig.xml).... \n"
	TDK_CONFIG_FILE = 'TdkConfig.xml'        	

dom = xml.dom.minidom.parse(str(TDK_CONFIG_FILE))
component = dom.getElementsByTagName('TestSuite')

env = dom.getElementsByTagName('TestEnvironment')
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

LOG_PATH = env[0].getElementsByTagName('LOG_PATH')[0].childNodes[0].nodeValue
DEV_NAME = env[0].getElementsByTagName('DEV_NAME')[0].childNodes[0].nodeValue
PORT_ID = env[0].getElementsByTagName('PORT_ID')[0].childNodes[0].nodeValue
Database_Name = env[0].getElementsByTagName('Database_Name')[0].childNodes[0].nodeValue
Database_Host = env[0].getElementsByTagName('Database_Name')[0].attributes['host'].value
Database_Username = env[0].getElementsByTagName('Database_Name')[0].attributes['username'].value
Databse_Password = env[0].getElementsByTagName('Database_Name')[0].attributes['password'].value
COMMON_XML_LOGS_PATH = ''
TDK_LOG_PATH=''

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
printlog( "LOG_PATH: "+ LOG_PATH)
printlog( "DEV_NAME: "+ DEV_NAME)
printlog( "PORT_ID: "+ PORT_ID)

def fetchLastExecutionId():
# fetch last inserted executionId from the database
# Description  : fetch last inserted executionId from  execution table of database
# Parameters   :
# Return Value : executionId
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
		return execId[0];
	except Exception, e:
		printlog( "ERROR : exception in fetching last executionId!\n")
		print "Exception type is: %s"%e

def fetchLastExecutionDeviceId():
# fetch last inserted executionDeviceId from the database
# Syntax       : fetchLastExecutionDeviceId();
# Description  : fetch last inserted executiondeviceId from  execute_method_result table of database
# Parameters   :
# Return Value : executemethodresultId
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
		return execDevId[0];
	except Exception, e:
		printlog( "ERROR : exception in fetching last executionDeviceId!\n")
		print "Exception type is: %s" %e;

def fetchLastExecutionResultId():
# fetch last inserted executionresultId from the database
# Syntax       : obj.fetchLastExecutionResultId();
# Description  : fetch last inserted executionresultId from  execution_result table of database
# Parameters   :
# Return Value : executionresultId
	try:
		conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
		#conn = _mysql.connect (host = "localhost", user = "root", passwd = "root", db = "rdktesttoolproddb")
		cur = conn.cursor()
		query = "SELECT id FROM execution_result ORDER BY id DESC limit 1";
		#print query;
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
		return execResId[0];
	except Exception, e:
		print "ERROR : exception in fetching last executionResultId!\n";
		print "Exception type is: %s" %e;
	else:
		print "Unload module Success\n"

def UpdateOpenSrcXMLData (XMLlogFile,componentName, testSuiteName, testType):
	lowRelevanceMethods=["initTestCase","cleanupTestCase"]
	#print "UpdateOpenSrcXMLData - ENTRY" + XMLlogFile
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

def Execute_Tests (testscript,soName,scriptlocation,component,testtype, TEST_SUITE_NAME):
	global invalidXMLCount
	global validXMLCount
	global TEST_PASS_COUNT
	global TEST_FAIL_COUNT
	
	if  os.path.exists(scriptlocation+"/"+testscript+".py") == False:
		return "Error :  "+scriptlocation+"/"+testscript+".py   Script file does not exist!"
	printlog( "---EXEC_ID, EXEC_DEVID,testscript:"+str(EXEC_ID)+" "+str(EXEC_RESID)+" "+str(EXEC_DEVID)+" " +testscript)
	command="python  commonTestScript.py" + " "+ TARGET_IP +" "+ PORT_ID +" "+ LOG_PATH +" "+TEST_MANAGER_URL +" "+EXEC_NAME+" "+testscript+" "+soName+" "+scriptlocation+" "+component+" "+testtype+" "+str(EXEC_ID)+" "+str(EXEC_DEVID)+" "+RDK_VERSION+" " + TEST_SUITE_NAME + " "+str(EXEC_RESID)+" " +" >"+LOG_PATH+"/logs/"+testscript+".log"
	printlog( command)
	try:
		print "Script Timeout Value is (in min.): " + str(SCRIPT_TIMEOUT)
		with time_limit(int(SCRIPT_TIMEOUT)* 60):
		#with time_limit(1):
			subprocess.call([command], shell=True)
	except TimeoutException, msg:
		print "Script Timed out!"
		return False


	currentdir=os.path.dirname(os.path.realpath(__file__))
	printlog( "Current Path :"+os.path.dirname(os.path.realpath(__file__))) 
	log_path=LOG_PATH
	for line in open(LOG_PATH+"/logs/"+testscript+".log"):
		if "--**--log_path--**--" in line:
			log_path=line.split("--**--log_path--**--")[1]
			break

	printlog( "log_path="+log_path)
	#print "Test Suite Log Path : "+COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"
	if(COMMON_XML_LOGS_PATH_ENABLED==True):
		try:	
			if not os.path.exists(COMMON_XML_LOGS_PATH+"/"+ TEST_SUITE_NAME+"/"):
				os.makedirs(COMMON_XML_LOGS_PATH+"/"+ TEST_SUITE_NAME)
			#else:	
				#shutil.rmtree(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"+TEST_SUITE_NAME+"/")#remove if ther is a file called LOG_PATH
				#os.makedirs(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"+TEST_SUITE_NAME+"/")
		except Exception as e:
			print "Error in creating "+COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+ " Pls check permissions !!"
			print e.message
			sys.exit()

	if component=='GStreamer' or component =='QtWebkit':
		printlog( "qtorgst = True ")
		ls_dir = os.listdir(log_path)
		for pfile in ls_dir:
			#xmlLogFile=log_path+str(EXEC_ID)+"/"+str(EXEC_DEVID)+"/"+str(EXEC_RESID)+"/"+ pfile	
			xmlLogFile=log_path+"/"+ pfile	
			
			if "TestSummary" not  in pfile and (not pfile.endswith("_xmllog.xml")):#do not clean up testsummary file
				try:
					command = "awk "+ "'" + "$1 ~ /^</ || $NF ~ />$/" + "' "+ xmlLogFile + ">>temp.xml"
					#printlog( command)
					subprocess.call([command], shell=True)
					command = "cat " + 'temp.xml' + ">> "+xmlLogFile +"_xmllog.xml"
					#printlog( command)
					subprocess.call([command], shell=True)
					command = "rm " +'temp.xml'
					#printlog( command)
					subprocess.call([command], shell=True)
					command = "sh xml_check.sh " + xmlLogFile+"_xmllog.xml"
					#printlog( command)
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

					if(COMMON_XML_LOGS_PATH_ENABLED==True):
						shutil.copy2(xmlLogFile,COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")

			
				except IOError:
						printlog(('File reading/writing issues : "' + log_path+"/" + pfile + '" '))		
						printlog('or File reading/writing issues : temp.xml')
						printlog( 'or File reading/writing issues :'+log_path + "/" + pfile+"_xmllog.xml")
				
				except Exception, e:
					printlog( "*Error in checking result log file ..!!!!")
					print e.message
						


#Validation of Tdkconfig.xml using validateTdkConfig.py
validationresult=validateTdkConfig(TDK_CONFIG_FILE)       	
if(validationresult):       	
	dom = xml.dom.minidom.parse(str(TDK_CONFIG_FILE))
	component = dom.getElementsByTagName('TestSuite')

	env = dom.getElementsByTagName('TestEnvironment')
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
	
	LOG_PATH = env[0].getElementsByTagName('LOG_PATH')[0].childNodes[0].nodeValue
	DEV_NAME = env[0].getElementsByTagName('DEV_NAME')[0].childNodes[0].nodeValue
	PORT_ID = env[0].getElementsByTagName('PORT_ID')[0].childNodes[0].nodeValue
	Database_Name = env[0].getElementsByTagName('Database_Name')[0].childNodes[0].nodeValue
	Database_Host = env[0].getElementsByTagName('Database_Name')[0].attributes['host'].value
	Database_Username = env[0].getElementsByTagName('Database_Name')[0].attributes['username'].value
	Databse_Password = env[0].getElementsByTagName('Database_Name')[0].attributes['password'].value
	COMMON_XML_LOGS_PATH = ''
	TDK_LOG_PATH=''

	#Setting environment variable in STB using setEnvironmentVariable.py
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
			return execId[0];
		except Exception, e:
			printlog( "ERROR : exception in fetching last executionId!\n")
			print "Exception type is: %s"%e
	
	def fetchLastExecutionDeviceId():
	# fetch last inserted executionDeviceId from the database
	# Syntax       : fetchLastExecutionDeviceId();
	# Description  : fetch last inserted executiondeviceId from  execute_method_result table of database
	# Parameters   :
	# Return Value : executemethodresultId
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
			return execDevId[0];
		except Exception, e:
			printlog( "ERROR : exception in fetching last executionDeviceId!\n")
			print "Exception type is: %s" %e;
	
	def fetchLastExecutionResultId():
	# fetch last inserted executionresultId from the database
	# Syntax       : obj.fetchLastExecutionResultId();
	# Description  : fetch last inserted executionresultId from  execution_result table of database
	# Parameters   :
	# Return Value : executionresultId
		try:
			conn = MySQLdb.connect (host=Database_Host , user =Database_Username, passwd =Databse_Password, db =Database_Name)
			#conn = _mysql.connect (host = "localhost", user = "root", passwd = "root", db = "rdktesttoolproddb")
			cur = conn.cursor()
			query = "SELECT id FROM execution_result ORDER BY id DESC limit 1";
			#print query;
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
			return execResId[0];
		except Exception, e:
			print "ERROR : exception in fetching last executionResultId!\n";
			print "Exception type is: %s" %e;
		else:
			print "Unload module Success\n"
	
	def UpdateOpenSrcXMLData (XMLlogFile,componentName, testSuiteName, testType):
		lowRelevanceMethods=["initTestCase","cleanupTestCase"]
		#print "UpdateOpenSrcXMLData - ENTRY" + XMLlogFile
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
			#print start
			
			process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			
			#with time_limit(int(SCRIPT_TIMEOUT)* 60):
			#with time_limit(1):
			#print "Before Loop..\n"
			execTime = int(SCRIPT_TIMEOUT) * 60
			
			#To display Progress Indicator during command line execution.
			while process.poll() is None:
				#print "\nInside While...\n"

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
		#print "Test Suite Log Path : "+COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/"
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
				#xmlLogFile=log_path+str(EXEC_ID)+"/"+str(EXEC_DEVID)+"/"+str(EXEC_RESID)+"/"+ pfile	
				xmlLogFile=log_path+"/"+ pfile	
				
				if "TestSummary" not  in pfile and (not pfile.endswith("_xmllog.xml")):#do not clean up testsummary file
					try:
						command = "awk "+ "'" + "$1 ~ /^</ || $NF ~ />$/" + "' "+ xmlLogFile + ">>temp.xml"
						#printlog( command)
						subprocess.call([command], shell=True)
						command = "cat " + 'temp.xml' + ">> "+xmlLogFile +"_xmllog.xml"
						#printlog( command)
						subprocess.call([command], shell=True)
						command = "rm " +'temp.xml'
						#printlog( command)
						subprocess.call([command], shell=True)
						command = "sh xml_check.sh " + xmlLogFile+"_xmllog.xml"
						#printlog( command)
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
					#print str(testFn.attributes['name'].value)
					if "none" in testFn.attributes['description'].value :
						testFn.setAttribute("description","Test for "+testFn.attributes['name'].value)
					else:
						testFn.setAttribute("description",testFn.attributes['description'].value)
					#print str(testFn.attributes['description'].value)
	
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
	
	def cbAfterExecutingATestSuite():
		global outLog

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
				#print "****#####****"+str(SCRIPT_TIMEOUT)
			if "</rdk_version>" in line:
				scriptrdk_version=(line.split("<rdk_version>"))[1].split("</rdk_version>")[0]
				#print "RDK VERSION CHECK :" + (line.split("<rdk_version>"))[1].split("</rdk_version>")[0] + "==" + RDK_VERSION
				if RDK_VERSION in scriptrdk_version and ScriptRdkVersionValidityForExecution==False:
					print "Script RDK Version matched"
					ScriptRdkVersionValidityForExecution=True
			if "</box_type>" in line:
				#print "BOX TYPE CHECK :" + (line.split("<box_type>"))[1].split("</box_type>")[0]+ "=="+BOX_TYPE
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
	
	for x in range(0,len(component)):
		
		try:
			TEST_SUITE_NAME=str(component[x].attributes['name'].value)	
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
					#print "RDK TESTS****" + testscript
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
	
				if ReportGenerationStatus.lower()=="true" and TEST_EXEC_STATUS==True:
					print "######### REPORT GENERATION ENABLED ##########"
	
					tempCurPath=str(os.getcwd())
					os.chdir(COMMON_XML_LOGS_PATH+"/"+TEST_SUITE_NAME+"/")
					TDK_LOG_PATH=str(os.getcwd())
					os.chdir(tempCurPath)
					#print str(len(TDK_LOG_PATH)) + str(len(TEST_SUITE_EXECUTION_TIME))+ str(len(str(sys.argv[1])))
					command = "python generateXLSfile.py " +TDK_LOG_PATH+" "+relevanceNumber+" "+TEST_SUITE_EXECUTION_TIME+" "+str	(TDK_CONFIG_FILE)+" "+componentName+"_TestReport.xls"
					#command = "python generateCSVfile.py " +TDK_LOG_PATH+" "+relevanceNumber
					print command  
					subprocess.call([command], shell=True)
					
					#command = "python csv2excel.py " + TDK_LOG_PATH + " "
					#print command  
					#subprocess.call([command], shell=True)
		
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
else:
	print "Error in validation of TdkConfig.xml"
