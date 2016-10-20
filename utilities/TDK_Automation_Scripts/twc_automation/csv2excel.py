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
import os,sys
import glob
import csv
import xlrd
print 'xlrd:   ', xlrd.__VERSION__
import xlwt
print 'xlwt:   ', xlwt.__VERSION__
from xlutils.copy import copy
import os.path

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

print "PATH input " + str(sys.argv[1])+'/*.csv'

for csvfile in glob.glob(os.path.join(str(sys.argv[1])+'/*.csv')):
	print "CSV -> XLS conversion...."
	print csvfile
	componentName=os.path.split(csvfile)[1]
	compName=componentName[:-4]
	#print componentName
	#print compName
	with open(csvfile, 'rb') as f:
		reader = csv.reader(f)
		for r, row in enumerate(reader):
			for c, col in enumerate(row):
				sheet1.write(r+1, c, col)

book.save(compName+"_TestReport.xls")
print "\nTEST REPORT GENERATED : " + compName+"_TestReport.xls\n"
