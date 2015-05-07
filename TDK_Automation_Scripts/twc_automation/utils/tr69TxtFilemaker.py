##########################################
#utils/tr69TxtFilemaker.py
# This will take the xls from alticast for TR069 data model requirements and 
# gegerate a text file as required by the script described in CPS-304 ( jira ticket)
# Will parse only .xls NOT .xlsx
# Check the attAched .xls file in the CPS-304
# The value of  "tr69DatamodelName" cnabe modified to get output for "TR98" or "TR181"




from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook
import os
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import sys
import xlrd
import string


#tr69DatamodelName="TR181"
tr69DatamodelName="TR98"

tr69rqwb = open_workbook('Everglades-Requirements_0.2-ajan.xls', formatting_info=True)
tr69rq181sht=tr69rqwb.sheet_by_name(tr69DatamodelName+' Profiles')
#tr69rq181sht=tr69rqwb.sheet_by_name('TR98 Profiles')
numOfRows=tr69rq181sht.nrows
print "numOfRows :",numOfRows

outfile = open("tr69-"+tr69DatamodelName+"-datamodel.txt", "w")


rowIndex=-1
state="start"
while rowIndex < (numOfRows-1):
	rowIndex=rowIndex+1
	if (tr69rq181sht.cell_value(rowIndex,0)=="Name"):
		state="NameHeaderStarts"
		continue
	if (state=="NameHeaderStarts" or state=="DataModelStartFound"):	
		xfx=tr69rq181sht.cell_xf_index(rowIndex,0)
		xf = tr69rqwb.xf_list[xfx]
		if( xf.background.pattern_colour_index == 43):
			state="DataModelStartFound"
			
			datamodelstart=tr69rq181sht.cell_value(rowIndex,0)
			datamodelstart=datamodelstart.encode('ascii', 'ignore')
			continue	
	if(state=="DataModelStartFound"):
		xfx=tr69rq181sht.cell_xf_index(rowIndex,0)
		xf = tr69rqwb.xf_list[xfx]
		if( xf.border.top_line_style==1 and xf.border.left_line_style==1 and xf.border.right_line_style==1 and xf.border.bottom_line_style==1):
			print rowIndex," : ",datamodelstart+tr69rq181sht.cell_value(rowIndex,0).encode('ascii','ignore').replace(" ","")
			outfile.write(datamodelstart+tr69rq181sht.cell_value(rowIndex,0).encode('ascii','ignore').replace(" ","")+"\n")
	
	
			
		

