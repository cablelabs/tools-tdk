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
	
