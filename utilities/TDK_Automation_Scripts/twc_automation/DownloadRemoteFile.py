# Python module to tranfer File to Host machine from STB
#
# INPUT	param -1 : TARGET_IP - IP address of remote machine
#	param -2 : PORT - Port to transfer file
#	param -3 : localLogPath - host machine destination path
#	param -4 : RemoteFilePath - Remote file path on source
#
# OUTPUT : status 0 - PASS/ 1- FAIL
#
import sys
sys.path.insert(0, "../python-lib/")
import os
import telnetlib
import re
import tftpy

def DownloadRemoteFile(TARGET_IP, PORT, localFilePath, RemoteFilePath):

        status = 0

        try:
                tclient = tftpy.TftpClient(TARGET_IP, PORT)
                print "STB Remote log path ::" , RemoteFilePath
                sys.stdout.flush()
		localLogPath, filename = os.path.split(os.path.abspath(localFilePath))
		if (os.path.exists(localLogPath)):
	                print "Destination Host machine log path ::" , localLogPath
	                sys.stdout.flush()
		else:
	                print "Missing Destination Host machine log path ::" , localLogPath
	                sys.stdout.flush()
			try:
	                	print "Creating directory ...::" , localLogPath
		                sys.stdout.flush()
    				os.makedirs(localLogPath)
			except OSError as exception:
    				if exception.errno != errno.EEXIST:
	        			raise
                tclient.download(RemoteFilePath,localFilePath)
                status = 1
                print "Downloading file successful...."
                sys.stdout.flush()
        except TypeError:
                print "Connection Error : Transfer of " + RemoteFilePath + " Failed.."
                sys.stdout.flush()
        except IOError:
                print "Remote Path from box:",RemoteFilePath
                print "Local Path:",localLogPath
                print "IO Error : Transfer of " + RemoteFilePath + " Failed.."
                print "Failed to find destination file path or permission denied"
                sys.stdout.flush()
        except: 
                print "ERROR : Transfer of " + RemoteFilePath + " Failed.."
                sys.stdout.flush()

        return status
