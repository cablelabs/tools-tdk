

import sys
import os
import os.path


#Used for modifying the test scripts
# Helpful in changing a specific line of all scripts
# Or inserting a new line after a specific line
# etc. 
# The commented parts can be used as examples to achieve the desired outputs. 

# The first argument is the path to the source sripts.
# A "new" folder should be created inside this path
# The modified scripts will be in the "new" folder

print "\n Usage:"
print " modifyScript.py <path>"
print " The first argument is the path to the source sripts"
print " A \"new\" folder should be created inside this path"
print " The modified scripts will be in the \"new\" folder\n\n"



path=sys.argv[1]
ls_dir = os.listdir(path)
for pfile in ls_dir:
	print pfile
	if (os.path.isdir(path+"/"+pfile) ==False):
		newfile=open(path+"/new/"+pfile,"w")	
		for line in open(path+"/"+pfile):
			'''if "itercount = 10" in line:
				newline=line.replace("itercount = 10" ,"itercount = 2" )
				newfile.write(newline)
				continue;
			if  "obj.createTestStep('IARMBUSPERF_UnRegisterEventHandler')" in line:
				newline=line;
				newline=newline.replace("tdkTestObj = obj.createTestStep('IARMBUSPERF_UnRegisterEventHandler')","perfData=tdkTestObj.logPerformanceData()");
				newfile.write(newline)
			
			if  "obj.unloadModule(\"iarmbusperf\")" in line:
				#print "===========GOT THE UNLOAD===="
				newline=line.replace("obj.unloadModule(\"iarmbusperf\")","tdkTestObj = obj.createTestStep('IARMBUSPERF_IRKeyEventTime')");
				newfile.write(newline)
				newline=line.replace("obj.unloadModule(\"iarmbusperf\")","perfData=tdkTestObj.logPerformanceData('IRKeyEventPropagation_AveragedTime','ms',str(dv.getMean()),'keytype:'+str(keytype)+' keycode:'+str(keycode) )");
				newfile.write(newline)
			'''
                        if  "tdkTestObj = obj.createTestStep('IARMBUSPERF_IRKeyEventTime');" in line:
                                newline=line;
                                newline=newline.replace("tdkTestObj = obj.createTestStep('IARMBUSPERF_IRKeyEventTime');","tdkTestObj = obj.createTestStep('IARMBUSPERF_IRKeyEventTime','IRKeyEventTime_keytype:'+str(keytype)+' keycode:'+str(keycode),True)");
                                newfile.write(newline)
				continue;


			newfile.write(line)

		#tdkTestObj = obj.createTestStep('IARMBUSPERF_IRKeyEventTime');
		#perfData=tdkTestObj.logPerformanceData("IRKeyEventPropagation_AveragedTime","ms",str(dv.getMean()),"keytype:"+str(keytype)+" keycode:"+str(keycode) );


newfile.close()
	


