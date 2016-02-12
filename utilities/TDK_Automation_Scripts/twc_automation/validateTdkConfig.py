import sys
import re
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
def validateTdkConfig(TDK_CONFIG_FILE):
	dom = xml.dom.minidom.parse(str(TDK_CONFIG_FILE))
	component = dom.getElementsByTagName('TestSuite')
	env = dom.getElementsByTagName('TestEnvironment')
	TARGET_IP = env[0].getElementsByTagName('TARGET_IP')[0].childNodes[0].nodeValue
	if re.match('[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}',TARGET_IP):
		print ("PASS TARGET_IP")
	else:
		print("Please verify TARGET_IP and try")
		return False
	BUILD_VER = env[0].getElementsByTagName('BUILD_VER')[0].childNodes[0].nodeValue
	if re.match('([0-9|a-z|A-Z|.|-])',BUILD_VER):
		print ("PASS BUILD_VER")
	else:
		print("Please verify Build version")
		return False
	RDK_VER = env[0].getElementsByTagName('RDK_VER')[0].childNodes[0].nodeValue
	if re.match('([0-9|a-z|A-Z|.|-])',RDK_VER):
		print ("PASS RDK_VER")
	else:
		print ("Please verify RDK_VER")
		return False		
	BOX_TYPE = env[0].getElementsByTagName('BOX_TYPE')[0].childNodes[0].nodeValue
	if re.match('([0-9|a-z|A-Z|.|-])',BOX_TYPE):
		print ("PASS BOX_TYPE ")
	else:
		print("Please verify BOX_TYPE")
		return False
	TEST_MANAGER_URL = str(env[0].getElementsByTagName('TEST_MANAGER_URL')[0].childNodes[0].nodeValue)
	regex = re.compile(
	r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	#if re.match('http:\/{2}([0-9]{1,3}|[.]){7}\:\d{4}\/(\w+[-|_]){1,4}[A-Z|a-z|0-9]{9}',TEST_MANAGER_URL):
	if regex.search(TEST_MANAGER_URL):
		print("PASS TEST_MANAGER_URL")
	else:
		print("Please verify TEST_MANAGER_URL")
		return False
	RESRC_PUBLISHER_LINK = str(env[0].getElementsByTagName('RESRC_PUBLISHER_LINK')[0].childNodes[0].nodeValue)
	if re.match('http[:]\/{2}[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[:][0-9]{4}\/',RESRC_PUBLISHER_LINK):
	#if re.match('http[s]?:\/{2}([0-9]{1,4}|[.|:]){9}',RESRC_PUBLISHER_LINK):
		print("PASS RESRC_PUBLISHER_LINK")
	else:
		print("Please verify RESRC_PUBLISHER_LINK")
		return False
	devicePort=env[0].getElementsByTagName('Device_Port')[0].childNodes[0].nodeValue
	if re.match('[0-9]',devicePort):
		print("PASS devicePort")
		return True
	else:
		print("Please verify device port")
		return False
	
