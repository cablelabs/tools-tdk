import subprocess, signal
import os 
p=subprocess.Popen(['ps','-af'],stdout=subprocess.PIPE)
out, err = p.communicate()
try:
	for line in out.splitlines():
		if 'TdkTestExecuter.py' in line:
			pid = int(line.split(None, 3)[1])
			print "pid of TdkTestExecuter killed: ",pid
			os.kill(pid, signal.SIGKILL)
		if  'commonTestScript.py' in line:
			pid = int(line.split(None, 3)[1])
			print "pid of commonTestScript killed: ",pid
			os.kill(pid, signal.SIGKILL)
except ValueError:
    print "Could not fetch PID."
except:
    print "Unexpected error:", sys.exc_info()[0]
	
