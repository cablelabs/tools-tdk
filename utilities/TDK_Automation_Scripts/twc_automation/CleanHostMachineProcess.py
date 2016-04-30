#  ============================================================================
#  COMCAST C O N F I D E N T I A L AND PROPRIETARY
#  ============================================================================
#  This file (and its contents) are the intellectual property of Comcast.  It may
#  not be used, copied, distributed or otherwise  disclosed in whole or in part
#  without the express written permission of Comcast.
#  ============================================================================
#  Copyright (c) 2016 Comcast. All rights reserved.
#  ============================================================================
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
	
