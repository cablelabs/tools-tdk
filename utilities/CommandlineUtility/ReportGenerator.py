from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook
import os
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import sys
import xlrd

length=0
if(sys.argv[2] == "WEBKIT"):
    keyword = ["htmlPerf", "vidPerfm", "cssPerfm","htmlFunc","browFunc","css3Func","cssFunct","domFunct","html5Fun","jqueryFun","nwkpFunc"]
    length=len(keyword)
    array= [[0 for x in xrange(4)] for x in xrange(length)]

elif(sys.argv[2] == "GSTREAMER"):
    keyword = ["gstVideoFunc","gstAudioFunc","gstVideoPerf","gstAudioPerf","gstVideoRecPerf","gstAudioRecPerf","gstChannelSwitchingPerf","gstVideoRecFunc","gstAudioRecFunc","gstPlayRecStreams","gstChannelSwitchingFunc","gstImageFunc","gstOutputPicResize","gstOutputPicPositioning","gstDisplayOutputPicture","gstMuteUnmute"]
    length=len(keyword)
    array= [[0 for x in xrange(4)] for x in xrange(length)]

elif(sys.argv[2] == "DLNA"):
    keyword = ["DLNAfunc"]
    length=len(keyword)
    array= [[0 for x in xrange(4)] for x in xrange(length)]
	
rdktotal=0
rdkpass=0
rdkfail=0
rdkothers=0

if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "RDKWEBKIT"):
    rb = open_workbook('QTWebkitTestCaseReport.xls')
elif(sys.argv[2] == "GSTREAMER"):

    rb = open_workbook('GStreamerTestCaseReport.xls')
elif(sys.argv[2] == "DLNA"):
    rb = open_workbook('DLNATestCaseReport.xls')
	
wb = copy(rb)
sheet_twc_r = rb.sheet_by_index(1)
twc_num_rows = sheet_twc_r.nrows-1

sheet_rdk_r = rb.sheet_by_index(2)
rdk_num_rows = sheet_rdk_r.nrows-1

sheet_report_r = rb.sheet_by_index(0)
report_num_rows = sheet_report_r.nrows-1

sheet_twc_w = wb.get_sheet(1)
sheet_rdk_w = wb.get_sheet(2)
sheet_report_w = wb.get_sheet(0)

print "sheet_twc_r  twc_num_rows %s ",twc_num_rows
print " rdk_num_rows %s ",rdk_num_rows
print "In generate report"
if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "GSTREAMER" or sys.argv[2] == "DLNA" ):
	for twc_column in range(0,sheet_twc_r.ncols):
                print "twc column ",twc_column," arg is ",sys.argv[1]
		if(sys.argv[1] in sheet_twc_r.cell_value(0,twc_column)):
			print "in for loop1"
			print"command line argument match (3,",twc_column,")"
			for row in range(1,sheet_twc_r.nrows):
				#if(sheet_twc_r.cell_type(row, twc_column) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):	
				#sheet_twc_w.write(row,twc_column,"")
				sheet_twc_w.write(row,twc_column,"NOT EXECUTED")
				print "+++"
			write_twc_col = twc_column
			break

if(sys.argv[2] == "RDKWEBKIT"):
	for rdk_column in range(0,sheet_rdk_r.ncols):
		
		print "in for loop2"
        	if(sys.argv[1] in sheet_rdk_r.cell_value(0,rdk_column)):
                	print"command line argument match (3,",rdk_column,")"
	                for row in range(1,sheet_rdk_r.nrows):
        	                #if(sheet_rdk_r.cell_type(row, rdk_column) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
                	        #sheet_rdk_w.write(row,rdk_column,"")
				sheet_rdk_w.write(row,rdk_column,"NOT EXECUTED")
				print "+++"
	                write_rdk_col = rdk_column
        	        break

if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "GSTREAMER" or sys.argv[2] == "DLNA" ):
	for a in range(5,5+length):
		for b in range(3,7):
			
			print "in for loop3"
			sheet_report_w.write(a,b,"0")
			print "+++"

if(sys.argv[2] == "RDKWEBKIT"):
	for a in range(24,35):
        	for b in range(3,7):
	        	sheet_report_w.write(a,b,"0")
			print "+++"
print os.listdir("TEMP")

for file in os.listdir("TEMP"):
      try:  
	print file, "Parsing::",file,"................."
	p_file = "TEMP/" +file
	dom = xml.dom.minidom.parse(p_file)
	testfunction = dom.getElementsByTagName('TestFunction')
	testcase = dom.getElementsByTagName('TestCase')

        print "Test Function : ",testfunction	
	for x in range(1, len(testfunction)+1):
		
		testfunctionname = dom.getElementsByTagName("TestCase")[0].attributes['name'].value + '::' + dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value
                print "func ",testfunctionname,twc_num_rows
		for y in range(1,twc_num_rows+1):
                        print "inside 123 "
			if("::" in sheet_twc_r.cell_value(y,2)):
                                print "here 1234"  
				functionname = str(sheet_twc_r.cell_value(y,2)).split("::")
                                print "fun nme ",functionname
                                print ">>",dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value 
				if(dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value == functionname[1]):
					print "here >>> ",testfunction[x-1]
                                        if(testfunction[x-1].getElementsByTagName("Incident")):
						print functionname,"::",testfunction[x-1].getElementsByTagName("Incident")[0].attributes['type'].value					
						sheet_twc_w.write(y,write_twc_col,testfunction[x-1].getElementsByTagName("Incident")[0].attributes['type'].value)
                    			else:
						sheet_twc_w.write(y,write_twc_col,"skip")				
				

	        for z in range(1,rdk_num_rows+1):
        	    if("::" in sheet_twc_r.cell_value(y,2)):
	    		functionname = str(sheet_rdk_r.cell_value(z,2)).split("::")
	        	if(dom.getElementsByTagName("TestCase")[0].attributes['name'].value+"::"+dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value == functionname[0]+"::"+functionname[1]):
                		print functionname[0],"::",functionname[1]
	                	if(testfunction[x-1].getElementsByTagName("Incident")):
        		        	incidentLength = len(testfunction[x-1].getElementsByTagName("Incident"))
                    			print "Length of incident tag is: ",incidentLength
                    			for k in range(0,incidentLength):
        	                		print "*******************"
                	                	sheet_rdk_w.write(z+k,write_rdk_col,testfunction[x-1].getElementsByTagName("Incident")[k].attributes['type'].value)
                		else:
                			sheet_rdk_w.write(z,write_rdk_col,"skip")

 
		print "++++++++++++++++++++"
    		for i in range(0, length):
    			if ( keyword[i] in dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value ):
				array[i][0] = array[i][0]+1
				print array[i][0],dom.getElementsByTagName("TestFunction")[x-1].attributes['name'].value
            			if(testfunction[x-1].getElementsByTagName("Incident")):
            				if ( testfunction[x-1].getElementsByTagName("Incident")[0].attributes['type'].value.lower() == "pass" ):
						array[i][1] = array[i][1]+1
		                
					elif ( testfunction[x-1].getElementsByTagName("Incident")[0].attributes['type'].value.lower() == "fail" ):
						array[i][2] = array[i][2]+1	
		                
            				else:
						array[i][3] = array[i][3]+1


	for u in range(1,rdk_num_rows+1):
		testcasename = str(sheet_rdk_r.cell_value(u,1))
		#print "TestCase name: ",testcasename
		if(dom.getElementsByTagName("TestCase")[0].attributes['name'].value == testcasename):
			result=dom.getElementsByTagName("TestCase")[0].getElementsByTagName("ResultSummary")[0].childNodes[0].data
		        #details=dict(item.split(":") for item in details.split(" "))
            		result=dict(item.split(":") for item in result.split(" "))
			resultvalue=result.values()
	                print "Resultvalue :",resultvalue
        		rdktotal=rdktotal+int(resultvalue[3])-2
	                print "rdk total: %d" %rdktotal
            	        rdkpass=rdkpass+int(resultvalue[2])-2
  	                print "rdk pass: %d" %rdkpass
            		rdkfail=rdkfail+int(resultvalue[0])
	                print "rdk fail: %d" %rdkfail
            		rdkothers=rdkothers+int(resultvalue[1])
		        print "rdk others: %d" %rdkothers
 	       		for i in range(24,35):
        			if(dom.getElementsByTagName("TestCase")[0].attributes['name'].value == sheet_report_r.cell_value(i,2)):
					sheet_report_w.write(i,3,int(resultvalue[3])-2)
			                sheet_report_w.write(i,4,int(resultvalue[2])-2)   
					sheet_report_w.write(i,5,int(resultvalue[0]))
					sheet_report_w.write(i,6,int(resultvalue[1]))
      except Exception:
       print "ERROR IN parsing"
total_value = 0
pass_value = 0
fail_value = 0 
skip_value = 0

for i in range(0,length):
    total_value = total_value + array[i][0]
    pass_value = pass_value + array[i][1]
    fail_value = fail_value + array[i][2]
    skip_value = skip_value + array[i][3]

print "Total",total_value 
print "Pass",pass_value
print "Fail",fail_value
print "Skip",skip_value


for a in range(1,report_num_rows+1):
    for i in range(0,length): 
	    if(keyword[i] == sheet_report_r.cell_value(a,2)):
 	        sheet_report_w.write(a,3,array[i][0])
                sheet_report_w.write(a,4,array[i][1])    
               	sheet_report_w.write(a,5,array[i][2])
                sheet_report_w.write(a,6,array[i][3])
                #sheet_report_w.write(a,7,0) 

if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "GSTREAMER" or sys.argv[2] == "DLNA"):
	sheet_report_w.write(1,4,sys.argv[1])          
	sheet_report_w.write(5+length,3,total_value)
	sheet_report_w.write(5+length,4,pass_value)
	sheet_report_w.write(5+length,5,fail_value)
	sheet_report_w.write(5+length,6,skip_value)

	notExecuted = twc_num_rows - total_value
	sheet_report_w.write(6+length,3,notExecuted)
	sheet_report_w.write(7+length,3,twc_num_rows)	

if(sys.argv[2] == "RDKWEBKIT"):
	#sheet_report_w.write(19,4,sys.argv[1])          
	sheet_report_w.write(35,3,rdktotal)
	sheet_report_w.write(35,4,rdkpass)
	sheet_report_w.write(35,5,rdkfail)
	sheet_report_w.write(35,6,rdkothers)
	notExecuted = rdk_num_rows - rdktotal
	sheet_report_w.write(36,3,notExecuted)
        sheet_report_w.write(37,3,rdk_num_rows)

del rb
if(sys.argv[2] == "WEBKIT" or sys.argv[2] == "RDKWEBKIT"):
   wb.save('QTWebkitTestCaseReport.xls')
elif(sys.argv[2] == "GSTREAMER"):
    wb.save('GStreamerTestCaseReport.xls')
elif(sys.argv[2] == "DLNA"):
    wb.save('DLNATestCaseReport.xls')
