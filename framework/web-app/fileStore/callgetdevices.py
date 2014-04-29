from getDevices import getConnectedDevices
import sys

if((len(sys.argv))!=3):
        print "Usage : python " + sys.argv[0] + " Device IP PortNumber"
	print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088"

else:
       deviceIP = sys.argv[1]
       devicePort = (int)(sys.argv[2])

       getConnectedDevices(deviceIP,devicePort)
#print "eg    : python " + sys.argv[0] + " 192.168.160.130 8088"