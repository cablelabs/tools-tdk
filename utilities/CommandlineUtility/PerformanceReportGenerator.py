from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook
import os
import sys
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import re
import xlrd
  
#Read from .xls
if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "RDKWEBKIT"):
    rb = open_workbook('QTWebkitPerformanceTestReport.xls')
elif(sys.argv[2] == "GSTREAMER"):

    rb = open_workbook('GStreamerPerformanceTestReport.xls')
#elif(sys.argv[2] == "DLNA"):
    #rb = open_workbook('DLNAPerformanceTestReport.xls')
	
sheet_r = rb.sheet_by_index(0)
num_rows = sheet_r.nrows-1
num_cols = sheet_r.ncols

#Copying the template
wb = copy(rb)
sheet_w = wb.get_sheet(0)

for column in range(0,sheet_r.ncols):
    if(sys.argv[1] in sheet_r.cell_value(3,column)):
	print"command line argument match (3,",column,")"
	for row in range(5,sheet_r.nrows):
		#if(sheet_r.cell_type(row, column) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):	
			#sheet_w.write(row,column,"fail")
		print "+++"
	result_col_index=column
        break            

#Write into .xls
for file in os.listdir("TEMP"):
      try:        
	print file, "Parsing::",file,"................."
	p_file = "TEMP/" + file
	dom = xml.dom.minidom.parse(p_file)
	testfunction = dom.getElementsByTagName('TestFunction')
	testcase = dom.getElementsByTagName('TestCase')
    
	for x in range(0, len(testfunction)):
		testfunctionname = dom.getElementsByTagName("TestCase")[0].attributes['name'].value + '::' + dom.getElementsByTagName("TestFunction")[x].attributes['name'].value
		#print num_rows;
		for y in range(5,num_rows+1):
			functionname = sheet_r.cell_value(y,1).split("::")	
			print functionname[1]	
			if( dom.getElementsByTagName("TestFunction")[x].attributes['name'].value == functionname[1]):
				sheet_w.write(y,result_col_index+2,sys.argv[3])
				print functionname[1],"::",testfunction[x].getElementsByTagName("Incident")[0].attributes['type'].value					
		                if(testfunction[x].getElementsByTagName("Description")):
					print "No: of Description Tags:", len(testfunction[x].getElementsByTagName("Description"))	
					for i in range(0,len(testfunction[x].getElementsByTagName("Description"))):	   
						if(testfunction[x].getElementsByTagName("Description")[i].childNodes):
							print testfunction[x].getElementsByTagName("Description")[i].childNodes[0].data
							if("Totals" or "Checks" in testfunction[x].getElementsByTagName("Description")[i].childNodes[0].data):
		                		        	print testfunction[x].getElementsByTagName("Description")[i].childNodes[0].data
								txt= testfunction[x].getElementsByTagName("Description")[i].childNodes[0].data
								value = re.split("::", txt)
								length=len(value)
								print value[length-1]
								result = re.findall("\d*\.\d+|\d+", value[length-1])
								if result:							
									print result[0]
									sheet_w.write(y,result_col_index,result[0])
								else: 
									sheet_w.write(y,result_col_index,"FAIL")
      except Exception:
       print "Error in parse"						
del rb				
if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "RDKWEBKIT"):
    wb.save('QTWebkitPerformanceTestReport.xls')
elif(sys.argv[2] == "GSTREAMER"):
    wb.save('GStreamerPerformanceTestReport.xls')
#elif(sys.argv[2] == "DLNA"):
    #wb.save('DLNAPerformanceTestReport.xls')
