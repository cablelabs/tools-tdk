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
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook
import os
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import sys
import xlrd
import subprocess
import time
import datetime
import shutil
import re
import string
# no need for dom parsing since 
# no need to know component under test
# just parse the log

argcnt = len(sys.argv)
if( argcnt < 2 ):
	print '\nUsage: xmlgenerator logfiletxt outfile'
	sys.exit(-1)

if not os.path.exists(sys.argv[1]):
	print 'Error: can not access:',sys.argv[1], 'Exiting'
	sys.exit(-1)

inlogfile=open(sys.argv[1],"rw");
outlogfile = open(sys.argv[2],"w");
prevLine = ""
prevLine2 = ""
# check if there are tags already?

outlogfile.write( '<?xml version="1.0" encoding="UTF-8"?>\n')
for line in inlogfile.readlines():
	line = line.rstrip('\n')
	if "Test Execution Name" in line:
		outlogfile.write('<TestCase name="%s">\n'%re.split(":", line)[1])

	if "SUCCESS" in line:
		outlogfile.write( "<Incident type=\"PASS\"/>\n")
		outlogfile.write( '<Message>"%s"</Message>\n' %re.split(":", line)[1])
		outlogfile.write( "</TestFunction>\n" )
	elif "FAILURE" in line:
		outlogfile.write( "<Incident type=\"FAIL\"/>\n")
		outlogfile.write( '<Message>"%s"</Message>\n' %re.split(":", line)[1])
		outlogfile.write( "</TestFunction>\n" )
	elif "ERROR" in line:
		outlogfile.write( "<Incident type=\"ERROR\"/>\n")
		outlogfile.write( '<Message>"%s"</Message>\n' %re.split(":", line)[1])
		outlogfile.write( "</TestFunction>\n" )
	if "...." in line:	
		words = re.split(" ", line)
		word = words[1].rstrip('.\n')
		outlogfile.write( '<TestFunction name="%s">\n' % word)
		prevLine = line
	if '[LIB' in line:
		outlogfile.write( '<Message>"%s"</Message>\n' % line)
	if '[TEST' in line:
		outlogfile.write( '<Message>"%s"</Message>\n' % line)
	if 'Reading' in line:
		rval = line.split(":");
		length = len(rval);
		timestr = rval[length-1];
		line=timestr.strip();
		outlogfile.write( '<Reading>%s</Reading>\n' % line)
	if 'Normalized Mean' in line:
		rval = line.split("=");
		length = len(rval);
		timestr = rval[length-1];
		line=timestr.strip();
		outlogfile.write( '<Average>%s</Average>\n' % line)
	if 'Data:' in line:
		rval = line.split(":");
		length = len(rval);
		timestr = rval[length-1];
		line=timestr.strip();
		outlogfile.write( '<PerfData>\n')
		outlogfile.write( '<Data>%s</Data>\n' % line)
	if 'Data2:' in line:
		rval = line.split(":");
		length = len(rval);
		timestr = rval[length-1];
		line=timestr.strip();
		outlogfile.write( '<Data2>%s</Data2>\n' % line)
	if 'Units' in line:
		rval = line.split(":");
		length = len(rval);
		timestr = rval[length-1];
		line=timestr.strip();
		outlogfile.write( '<Units>%s</Units>\n' % line)
		outlogfile.write( '</PerfData>\n')
outlogfile.write( '</TestCase>\n')
outlogfile.close()
inlogfile.close()

