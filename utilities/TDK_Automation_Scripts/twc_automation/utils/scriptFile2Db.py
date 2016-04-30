#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================


#!/usr/bin/python
#  Author : Ajan U. Nair
#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------


'''
	<xml>
	        <id>1118</id>           <!-- Do not edit id. This will be auto filled while exporting-->
        	<version>6</version>            <!-- Do not edit version. This will be auto incremented while exporting-->
	        <name>RMF_QAMSource_Play_12</name>
	        <primitive_test_id>494</primitive_test_id>               <!-- Do not edit primitive_test_id. -->
        	<primitive_test_name>RMF_Element_Create_Instance</primitive_test_name>
	        <primitive_test_version>1</primitive_test_version>
        	<status>FREE</status>
	        <synopsis>This script tests the RDK Mediaframework QAMSrc element to Play the live content when factory method flag is set to true.^M
Test Case ID: CT_RMF_QAMSrc_MPSink_12.          </synopsis>
	        <groups_id>None</groups_id>
        	<execution_time>4</execution_time>              <!--execution_time is the time out time for test execution-->
	        <remarks>                               </remarks>
        	<skip>^@</skip>         <!--skit this test or not-->
	        <rdk_versions>
        	        <version>3</version>
	        </rdk_versions>
	</xml>
'''
#Above is only a sample xml header , expected for every py script


import MySQLdb
import os
import sys
import re	
import xml.dom.minidom
from xml.dom.minidom import parse, parseString


#-----------------------------------Edit this section  to configure your mysql database connection--------------------
hostName="localhost"
userName="root"
password="root"
databaseName="rdktesttoolproddb"
#databaseName="rdktesttoolproddb_M13_ajjuly15"
#-----------------------------------------------------------------------------------------------------------------




def validateAndGetTagValue(dom,tagName):
        if (dom.getElementsByTagName(tagName).length) == 0 :
                print tagName + " not specified"
		return -1
        else :
		if (dom.getElementsByTagName(tagName)[0].childNodes.length) == 0 :
			print tagName+" is empty"
			return "Null" 
		else :
			tagValue=dom.getElementsByTagName(tagName)[0].childNodes[0].data
			print tagName +" = "+tagValue
			return tagValue	


def exportScriptFile2Db(scriptfilePathAndName):
	scriptfileObj = open(scriptfilePathAndName)
	lines = scriptfileObj.readlines()
	xmlData = ''
	scriptData=''
	headerCompleted=0;

	#TODO: need to filter new line and othe characters before doing this comparison , in order to make the manual editing of xml more flexible.	
	if lines[0] != "'''\n":
		print 'First line in the file is not a start of comment. Exiting'
		return 
	for i  in range(len( lines)):
		if(headerCompleted==0):
			if lines[i+1] != "'''\n":  	#using i+1 to skip the start of comment. 
				xmlData = xmlData +  lines[i+1]
			else :
				headerCompleted=1
		else:
			if (i+2)<len(lines) :
				scriptData= scriptData + lines [i+2]

	print xmlData
	print scriptData		

	dom = xml.dom.minidom.parseString(xmlData)

	script_id = validateAndGetTagValue(dom,"id")
	script_vesion = validateAndGetTagValue(dom,"version")
	script_name = validateAndGetTagValue(dom,"name")
	script_primitive_test_id = validateAndGetTagValue(dom,"primitive_test_id")
	script_primitive_test_name = validateAndGetTagValue(dom,"primitive_test_name")
	script_primitive_test_version = validateAndGetTagValue(dom,"primitive_test_version")
	script_status = validateAndGetTagValue(dom,"status")
	script_synopsis =validateAndGetTagValue(dom,"synopsis")
	script_groups_id = validateAndGetTagValue(dom,"groups_id")
	if script_groups_id == 'None'	:
		script_groups_id = None# groups_d=2 is for TWC. Now groups_id is not yet implemented fully as on 25July2014
	script_execution_time = validateAndGetTagValue(dom,"execution_time")
	script_remarks = validateAndGetTagValue(dom,"remarks")

	if  validateAndGetTagValue(dom,"skip")== True :
		script_skip=b'0x01'
	else:
		script_skip=b'0x00'

	

	cur.execute("""SELECT id,version,name FROM script WHERE id="""+str(script_id))
	if cur.rowcount == 0 :
		print"No record found with id="+str(script_id)+"."
		if str(script_id) == 'Null' :  # if id is not specified, intention is to create a new row in the script table, so id , being the primary key will be auto updated
			cur.execute("""INSERT INTO script (version,name,primitive_test_id,script_content,status,synopsis,groups_id,execution_time,remarks,skip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE version=VALUES(version),name=VALUES(name),primitive_test_id=VALUES(primitive_test_id),script_content=VALUES(script_content),status=VALUES(status),synopsis=VALUES(synopsis),groups_id=VALUES(groups_id),execution_time=VALUES(execution_time),remarks=VALUES(remarks),skip=VALUES(skip)""" , (script_vesion,script_name,script_primitive_test_id,scriptData,script_status, script_synopsis,script_groups_id,script_execution_time,script_remarks,script_skip))
		else:
			print "If you want to insert a new script use empty id"
	else :
		print"The record with id="+str(script_id)+" will be overwritten."
		cur.execute("""INSERT INTO script (id,version,name,primitive_test_id,script_content,status,synopsis,groups_id,execution_time,remarks,skip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE version=VALUES(version),name=VALUES(name),primitive_test_id=VALUES(primitive_test_id),script_content=VALUES(script_content),status=VALUES(status),synopsis=VALUES(synopsis),groups_id=VALUES(groups_id),execution_time=VALUES(execution_time),remarks=VALUES(remarks),skip=VALUES(skip)""" , (script_id,script_vesion,script_name,script_primitive_test_id,scriptData,script_status, script_synopsis,script_groups_id,script_execution_time,script_remarks,script_skip))

	conn.commit()


def exportAllfilesInFolder(folderPath):
	for filename in os.listdir(folderPath):
		print folderPath+"/"+filename
		exportScriptFile2Db(folderPath+"/"+filename)

def showUsage():
	print "python scriptFile2Db.py [[-all][<foldername>]][<fileName>]"
	print "scriptFile2Db.py will export scripts with proper  xml headers to the databse tables"
	print "You should edit the databse connection line on top of this script to connect to you databse"

def confirmTheAction():
        print "Do you want to update the database "+databaseName+" at "+hostName+ " with the python scripts in the"
        choice = raw_input().lower();
        if (choice != 'y'):
                sys.exit()


conn = MySQLdb.connect (host = hostName, user = userName, passwd = password, db = databaseName)
cur = conn.cursor()
if (len(sys.argv)== 2 ):
	if sys.argv[1] == "-all" :
		exportAllfilesInFolder("scriptsDump")
	else :
		if not ( os.path.exists(sys.argv[1])):
			print sys.argv[1]+" :Invalid file/path"
			showUsage()
		else:
			print "Do you want to update the database "+databaseName+" at "+hostName+ " with the python scripts in the file : "+ sys.argv[1]+ " ?"
			print "This will overwirte your databse stored scripts !!!!!"
			choice = raw_input().lower();
			if (choice != 'y'):
				sys.exit()

			exportScriptFile2Db(sys.argv[1])
else:
	if(len(sys.argv) == 3 ) :	
		if not( os.path.isdir(sys.argv[2])):
			print sys.argv[2]+" :Invalid folder"
			showUsage()
		else:
			print "Do you want to update the database "+databaseName+" at "+hostName+ " with the python scripts in the folder : "+ sys.argv[2]+ " ?"
			print "This will overwirte your databse stored scripts !!!!!"
			choice = raw_input().lower();
			if (choice != 'y'):
				sys.exit()
			exportAllfilesInFolder(sys.argv[2])
	else:
		print "Invalid Arguments. More/Less arguments than expected"
		showUsage()
	

exit()

