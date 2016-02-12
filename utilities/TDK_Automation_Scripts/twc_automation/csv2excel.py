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
