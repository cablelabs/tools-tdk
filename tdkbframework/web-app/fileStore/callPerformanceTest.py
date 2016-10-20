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
#

# Module Imports
import tftpy
import sys
import socket
import json

def tftpDownload(ipaddrs, logtransferport, remotefile, localfile):

	# Connect to TFTP server and download the file
	try:
		client = tftpy.TftpClient (ipaddrs, logtransferport)
		client.download (remotefile, localfile)

	except TypeError:
		print "Connection Error!!! Transfer of " + remotefile + " Failed: Make sure Agent is running"
		exit()

	except:
		print "Error!!! Transfer of " + remotefile + " Failed.."
		exit()


# Check the number of arguments and print the syntax if args not equal to 5
if ( (len(sys.argv)) != 6):
        print "Usage : python " + sys.argv[0] + " Device_IP_Address Agent_Port_Number Log_Transfer_Port RPC_Method Local_file_path"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8087 69 RPC_Method_Name(PerformanceBenchMarking/PerformanceSystemDiagnostics) \"/filestore/version/version.txt\""
	exit()

# Assigning IP address, port numbers, path of destination files and rpcmethod to be invoked
ipaddrs = sys.argv[1]
deviceport = int (sys.argv[2])
logtransferport = int (sys.argv[3])
rpcmethod = sys.argv[4]
localfilepath = sys.argv[5]

# Sending json request and receiving response
try:
	tcpClient = socket.socket()
	tcpClient.connect((ipaddrs, deviceport))

	jsonMsg = {'jsonrpc':'2.0','id':'2','method':rpcmethod}
	query = json.dumps(jsonMsg)
	tcpClient.send(query) #Sending json query

	result = tcpClient.recv(1048) #Receiving response

	tcpClient.close()
	# Extracting result and logpath from response message
	resultIndex = result.find("result") + len("result"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]

	resultIndex = result.find("logpath") + len("logpath"+"\":\"")
	message = result[resultIndex:]
	message = message[:(message.find("\""))]
	logpath = message

except socket.error:
	print "Unable to reach agent"
	exit()

if "PerformanceSystemDiagnostics" in rpcmethod:

	# Constructing path for remote and local files
	remotefile = logpath + "/cpu.log"
	localfile = localfilepath + "/cpu.log"

	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

	# Constructing path for remote and local files
	remotefile = logpath + "/memused.log"
	localfile = localfilepath + "/memused.log"

	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

else:
	# Downloading files using TFTP
	filename = logpath.split("/")[-1]
	remotefile = logpath
	localfile = localfilepath + "/" + filename
	tftpDownload(ipaddrs, logtransferport, remotefile, localfile)

# End of File
