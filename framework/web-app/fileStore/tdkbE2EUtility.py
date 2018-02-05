#!/usr/bin/python

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
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

#------------------------------------------------------------------------------
# Methods
#------------------------------------------------------------------------------
import os
import sys
from pexpect import pxssh
import ConfigParser
import tdklib
from time import sleep
import commands

#Global variable to check whether login session is active
isSessionActive = False

def parseDeviceConfig(obj):

# parseDeviceConfig

# Syntax      : parseDeviceConfig()
# Description : Function to parse the device configuration file
# Parameters  : obj - Object of the tdk library
# Return Value: SUCCESS/FAILURE

	try:
		status = "SUCCESS"

        	#Get the device name configured in test manager
        	deviceDetails = obj.getDeviceDetails()
        	deviceName = deviceDetails["devicename"]

        	#Get the device configuration file name
        	deviceConfig = deviceName + ".config"

		#Get the current directory path
		configFilePath = os.path.dirname(os.path.realpath(__file__))
		configFilePath = configFilePath + "/tdkbDeviceConfig"

        	print "Device config file:", configFilePath+'/'+deviceConfig
	
        	#Parse the device configuration file
        	config = ConfigParser.ConfigParser()
		config.read(configFilePath+'/'+deviceConfig)
	
        	#Parse the file and store the values in global variables
                global setup_type
                setup_type = config.get(deviceConfig, 'SETUP_TYPE')

                global wlan_os_type
                wlan_os_type = config.get(deviceConfig, 'WLAN_OS_TYPE')

        	global wlan_ip
        	wlan_ip = config.get(deviceConfig, 'WLAN_IP')

                global wan_ping_ip
                wan_ping_ip = config.get(deviceConfig, "WAN_PING_IP")

                global wan_http_ip
                wan_http_ip = config.get(deviceConfig, "WAN_HTTP_IP")

                global wan_https_ip
                wan_https_ip = config.get(deviceConfig, "WAN_HTTPS_IP")

                global wan_ftp_ip
                wan_ftp_ip = config.get(deviceConfig, "WAN_FTP_IP")

        	global wlan_username
        	wlan_username = config.get(deviceConfig, "WLAN_USERNAME")
        
        	global wlan_password
        	wlan_password = config.get(deviceConfig, "WLAN_PASSWORD")

        	global wlan_ftp_username
        	wlan_ftp_username = config.get(deviceConfig, "WLAN_FTP_USERNAME")
        
        	global wlan_ftp_password
        	wlan_ftp_password = config.get(deviceConfig, "WLAN_FTP_PASSWORD")

        	global wlan_2ghz_interface
        	wlan_2ghz_interface = config.get(deviceConfig, "WLAN_2GHZ_INTERFACE")

                global wlan_5ghz_interface
                wlan_5ghz_interface = config.get(deviceConfig, "WLAN_5GHZ_INTERFACE")

        	global wlan_inet_address
        	wlan_inet_address = config.get(deviceConfig, "WLAN_INET_ADDRESS")

                global wlan_subnet_mask
                wlan_subnet_mask = config.get(deviceConfig, "WLAN_SUBNET_MASK")

        	global wlan_script
       		wlan_script = config.get(deviceConfig, "WLAN_SCRIPT")

		global wlan_2ghz_ssid_connect_status
		wlan_2ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_CONNECT_STATUS")

                global wlan_5ghz_ssid_connect_status
                wlan_5ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_CONNECT_STATUS")

		global wlan_2ghz_ssid_disconnect_status
        	wlan_2ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_DISCONNECT_STATUS")

                global wlan_5ghz_ssid_disconnect_status
                wlan_5ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_DISCONNECT_STATUS")

                global lan_os_type
                lan_os_type = config.get(deviceConfig, 'LAN_OS_TYPE')

        	global lan_ip
        	lan_ip = config.get(deviceConfig, "LAN_IP")

		global lan_username        
        	lan_username = config.get(deviceConfig, "LAN_USERNAME")
        
		global lan_password
        	lan_password = config.get(deviceConfig, "LAN_PASSWORD")

		global lan_ftp_username        
        	lan_ftp_username = config.get(deviceConfig, "LAN_FTP_USERNAME")
        
		global lan_ftp_password
        	lan_ftp_password = config.get(deviceConfig, "LAN_FTP_PASSWORD")

		global lan_interface
        	lan_interface = config.get(deviceConfig, "LAN_INTERFACE")

		global lan_inet_address
   		lan_inet_address = config.get(deviceConfig, "LAN_INET_ADDRESS")

                global lan_subnet_mask
                lan_subnet_mask = config.get(deviceConfig, "LAN_SUBNET_MASK")
                
                global lan_dns_server
                lan_dns_server = config.get(deviceConfig, "LAN_DNS_SERVER")
                
                global lan_lease_time
                lan_lease_time = config.get(deviceConfig, "LAN_LEASE_TIME")  
                
                global lan_domain_name
                lan_domain_name = config.get(deviceConfig, "LAN_DOMAIN_NAME")                                

		global lan_script
        	lan_script = config.get(deviceConfig, "LAN_SCRIPT")

		global wan_ip
       		wan_ip = config.get(deviceConfig, "WAN_IP")

		global wan_username
        	wan_username = config.get(deviceConfig, "WAN_USERNAME")

		global wan_password
        	wan_password = config.get(deviceConfig, "WAN_PASSWORD")

		global wan_ftp_username
        	wan_ftp_username = config.get(deviceConfig, "WAN_FTP_USERNAME")

		global wan_ftp_password
        	wan_ftp_password = config.get(deviceConfig, "WAN_FTP_PASSWORD")

		global wan_interface
        	wan_interface = config.get(deviceConfig, "WAN_INTERFACE")

		global wan_inet_address
       		wan_inet_address = config.get(deviceConfig, "WAN_INET_ADDRESS")

		global wan_script
        	wan_script = config.get(deviceConfig, "WAN_SCRIPT")

		global ssid_2ghz_name
        	ssid_2ghz_name = config.get(deviceConfig, "SSID_2GHZ_NAME")

		global ssid_2ghz_pwd
        	ssid_2ghz_pwd = config.get(deviceConfig, "SSID_2GHZ_PWD")

                global ssid_2ghz_invalid_pwd
                ssid_2ghz_invalid_pwd = config.get(deviceConfig, "SSID_2GHZ_INVALID_PWD")

		global ssid_2ghz_index
        	ssid_2ghz_index = config.get(deviceConfig, "SSID_2GHZ_INDEX")

                global radio_2ghz_index
                radio_2ghz_index = config.get(deviceConfig, "RADIO_2GHZ_INDEX")

		global ssid_5ghz_name
        	ssid_5ghz_name = config.get(deviceConfig, "SSID_5GHZ_NAME")

		global ssid_5ghz_pwd
      		ssid_5ghz_pwd = config.get(deviceConfig, "SSID_5GHZ_PWD")

                global ssid_5ghz_invalid_pwd
                ssid_5ghz_invalid_pwd = config.get(deviceConfig, "SSID_5GHZ_INVALID_PWD")

		global ssid_5ghz_index
        	ssid_5ghz_index = config.get(deviceConfig, "SSID_5GHZ_INDEX")

                global radio_5ghz_index
                radio_5ghz_index = config.get(deviceConfig, "RADIO_5GHZ_INDEX")

		global connection_timeout
       		connection_timeout = config.get(deviceConfig, "CONNECTION_TIMEOUT")

                global network_ip
                network_ip = config.get(deviceConfig, "NETWORK_IP")

                global http_port
                http_port = config.get(deviceConfig, "HTTP_PORT")

                global https_port
                https_port = config.get(deviceConfig, "HTTPS_PORT")

                global wan_http_port
                wan_http_port = config.get(deviceConfig, "WAN_HTTP_PORT")

                global wan_https_port
                wan_https_port = config.get(deviceConfig, "WAN_HTTPS_PORT")

                global wlan_http_port
                wlan_http_port = config.get(deviceConfig, "WLAN_HTTP_PORT")

                global wlan_https_port
                wlan_https_port = config.get(deviceConfig, "WLAN_HTTPS_PORT")

                global cm_ip_type
                cm_ip_type = config.get(deviceConfig, "CM_IP_TYPE")

                global cm_ip
                cm_ip = config.get(deviceConfig, "CM_IP")

                global gw_wan_ip
                gw_wan_ip = config.get(deviceConfig, "GW_WAN_IP")

                global ssid_invalid_name
                ssid_invalid_name = config.get(deviceConfig, "SSID_INVALID_NAME")

                global ssid_invalid_pwd
                ssid_invalid_pwd = config.get(deviceConfig, "SSID_INVALID_PWD")

                global wlan_invalid_interface
                wlan_invalid_interface = config.get(deviceConfig, "WLAN_INVALID_INTERFACE")

                global nslookup_domain_name
                nslookup_domain_name = config.get(deviceConfig, "NSLOOKUP_DOMAIN_NAME")
                
                global lan_dhcp_location
                lan_dhcp_location = config.get(deviceConfig, "LAN_DHCP_LOCATION")
                

	except Exception, e:
		print e;
		status = "Failed to parse the device specific configuration file"

	return status;

########## End of Function ##########


def executeCommand(command):

# executeCommand

# Syntax      : executeCommand()
# Description : Function to execute the command
# Parameters  : command - Command to be executed
# Return Value: SUCCESS/FAILURE

	try:
                session.sendline(command)
                session.prompt()
                status=session.before
		print "Command Output:%s" %status
		status=status.strip()
		if "OUTPUT:" in status:
			status=status.split("OUTPUT:",1)[1]
		else:
			status = "FAILURE"
        except Exception, e:
	       print e;
               status = e;

        return status;

########## End of Function ##########


def clientConnect(clientType):

# clientConnect

# Syntax      : clientConnect()
# Description : Function to connect to the client machine.
# Parameters  : clientType: WLAN/LAN/WAN
# Return Value: SUCCESS/FAILURE
	
	try:
		status = "SUCCESS";
		global isSessionActive;
        	print "Connect to %s machine" %clientType
		global session
        	session = pxssh.pxssh(options={
                            "StrictHostKeyChecking": "no",
                            "UserKnownHostsFile": "/dev/null"})
		#session.setwinsize(24, session.maxread)
                if clientType == "WLAN":
    			isSessionActive = session.login(wlan_ip,wlan_username,wlan_password)
                elif clientType == "LAN":
			isSessionActive = session.login(lan_ip,lan_username,lan_password)
                elif clientType == "WAN":
                        isSessionActive = session.login(wan_ip,wan_username,wan_password)
		else:
			status = "Invalid client type"
	except Exception, e:
		print e;
		status = "Connection to client machine failed"	
	
	print "Connection to client machine:%s" %status;
    	return status;

########## End of Function ##########


def clientDisconnect():

# clientDisconnect

# Syntax      : clientDisconnect()
# Description : Function to disconnect from the client machine
# Parameters  : None
# Return Value: SUCCESS/FAILURE

       	try:
		global isSessionActive;
		status = "SUCCESS"
		if isSessionActive == True:
			#command="sudo sh %s refresh_wifi_network" %(wlan_script)
                        #executeCommand(command)
                        #sleep(30);
               		session.logout()
			session.close()
		else:
			status = "No active session"
       	except Exception, e:
		print e;
          	status = e;

	print "Disconnect from client machine:%s" %status;
	return status;

########## End of Function ##########


def checkSsidAvailable(ssidName):

# checkSsidAvailable

# Syntax      : checkSsidAvailable
# Description : Function to check whether the SSID is listed in the wifi network
# Parameters  : ssidName - SSID Name
# Return Value: status - WIFI SSID name

	try:
		if wlan_os_type == "UBUNTU":
        		command="sudo sh %s is_ssid_available %s" %(wlan_script,ssidName)
			status = executeCommand(command)
		else:
			status = "Only UBUNTU platform supported!!!"
	except Exception, e:
		print e;
		status = e;

	print "SSID listed in client's wireless network:%s" %status;
        return status;

########## End of Function ##########


def wifiConnect(ssidName,ssidPwd,securityType):

# wifiConnect

# Syntax      : wifiConnect()
# Description : Function to connect to the WIFI SSID from the WLAN client
# Parameters  : ssidName - SSID Name
#		ssidPwd - SSID password
#		securityType - Protected/Open security mode
# Return Value: SUCCESS/FAILURE

	try:
		if wlan_os_type == "UBUNTU":
			if securityType == "Protected":
				command="sudo sh %s wifi_ssid_connect %s %s" %(wlan_script,ssidName,ssidPwd)
			else:
				command="sudo sh %s wifi_ssid_connect_openSecurity %s" %(wlan_script,ssidName)
			status = executeCommand(command)
		else:
			status = "Only UBUNTU platform supported!!!"
	except Exception, e:
		print e;
                status = e;

	print "WIFI connect status:%s" %status;
        return status;

########## End of Function ##########


def getConnectedSsidName(wlanInterface):

# getConnectedSsidName

# Syntax      : getConnectedSsidName()
# Description : Function to get the current SSID name WLAN connected
# Parameters  : wlanInterface - wlan interface name
# Return Value: SUCCESS/FAILURE

	try:
		if wlan_os_type == "UBUNTU":
       			command="sudo sh %s get_connected_ssid_name %s" %(wlan_script,wlanInterface)
			status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
		print e;
                status = e;

	print "Connected WIFI SSID Name:%s" %status;
        return status;

########## End of Function ##########


def wifiDisconnect(wlanInterface):

# wifiDisconnect

# Syntax      : OBJ.wifiDisconnect()
# Description : Function to disconnect the WLAN from the WIFI SSID
# Parameters  : wlanInterface - wlan interface name
# Return Value: SUCCESS/FAILURE

	try:
            status = clientConnect("WLAN")
            if status == "SUCCESS":
		if wlan_os_type == "UBUNTU":
                        status = getConnectedSsidName(wlanInterface)
                        if ssid_2ghz_name in status or ssid_5ghz_name in status:
                                command="sudo sh %s wifi_ssid_disconnect %s" %(wlan_script,wlanInterface)
                                status = executeCommand(command)
                        else:
                                status = "SSID is already disconnected"
                else:
                        status = "Only UBUNTU platform supported!!!"
	    else:
                return "Failed to connect to wlan client"

        except Exception, e:
		print e;
                status = e;

	print "WIFI disconnect status:%s" %status;
        return status;

######### End of Function ##########


def wlanConnectWifiSsid(ssidName,ssidPwd,wlanInterface,securityType= "Protected"):

# wlanConnectWifiSsid

# Syntax      : wlanConnectWifiSsid()
# Description : Function to connect wlan to the wifi ssid
# Parameters  : ssidName - SSID Name
#		ssidPwd - SSID password
#		wlanInterface - wlan interface name
#		securityType - Protected/Open security mode
# Return Value: SUCCESS/FAILURE

	try:
		status = clientConnect("WLAN")
		if status == "SUCCESS":
			command="sudo sh %s refresh_wifi_network" %(wlan_script)
                        executeCommand(command)
			sleep(20);
			status = checkSsidAvailable(ssidName)
			if ssidName in status:
				status = wifiConnect(ssidName,ssidPwd,securityType)
				if wlan_2ghz_ssid_connect_status in status or wlan_5ghz_ssid_connect_status in status:
                            		sleep(60);
					status = getConnectedSsidName(wlanInterface)
					if ssidName in status:
						return "SUCCESS"
					else:
						return "Failed to get the connected SSID Name"
				else:
					return "Failed to connect to wifi ssid"
			else:
				return "Couldn't find the SSID in available SSIDs list"
		else:
			return "Failed to connect to wlan client"
	except Exception, e:
		print e;
                return e;


######### End of Function ##########

def wlanIsSSIDAvailable(ssidName):

# wlanIsSSIDAvailable

# Syntax      : wlanIsSSIDAvailable()
# Description : Function to check if SSID is available in wifi client
# Parameters  : ssidName - SSID Name
# Return Value: SUCCESS/FAILURE

        try:
                status = clientConnect("WLAN")
                if status == "SUCCESS":
                        command="sudo sh %s refresh_wifi_network" %(wlan_script)
                        executeCommand(command)
                        sleep(20);
                        status = checkSsidAvailable(ssidName)
                        if ssidName in status:
                                return "SUCCESS"
                        else:
                                return "FAILURE"
                else:
                        return "Failed to connect to wlan client"
        except Exception, e:
                print e;
                return e;


######### End of Function ##########

def wlanDisconnectWifiSsid(wlanInterface):

# wlanDisconnectWifiSsid

# Syntax      : wlanDisconnectWifiSsid()
# Description : Function to disconnect wlan from the wifi ssid
# Parameters  : ssidName - SSID Name
#		wlanInterface - wlan interface name
# Return Value: SUCCESS/FAILURE

	try:
        	status = wifiDisconnect(wlanInterface)
        	if wlan_2ghz_ssid_disconnect_status in status or wlan_5ghz_ssid_disconnect_status in status or "SSID is already disconnected" in status:
			return "SUCCESS"
		else:
                	return "Failed to disconnect from wifi ssid"

	except Exception, e:
                print e;
                return e;

######### End of Function ##########

def getWlanIPAddress(wlanInterface):

# getWlanIPAddress

# Syntax      : getWlanIPAddress()
# Description : Function to get the current ip address of the wlan client after connecting to wifi
# Parameters  : wlanInterface - wlan interface name
# Return Value: status - IP Address of the WLAN client

        try:
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_wlan_ip_address %s %s" %(wlan_script,wlanInterface,wlan_inet_address)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                status = e;

        print "WLAN IP Address after connecting to WIFI:%s" %status;
        return status;

########## End of Function ##########

def getWlanSubnetMask(wlanInterface):

# getWlanSubnetMask

# Syntax      : getWlanSubnetMask()
# Description : Function to get the subnet mask of the wlan client after connecting to wifi
# Parameters  : wlanInterface - wlan interface name
# Return Value: status - IP Address of the WLAN client

        try:
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_wlan_subnet_mask %s %s" %(wlan_script,wlanInterface,wlan_subnet_mask)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                status = e;

        print "Subnet mask of wifi client:%s" %status;
        return status;

########## End of Function #########

def getLanIPAddress(lanInterface):

# getLanIPAddress

# Syntax      : getLanIPAddress()
# Description : Function to get the current ip address of the Lan client after connecting to it
# Parameters  : lanInterface - lan interface name
# Return Value: status - IP Address of the LAN client

        try:
                status = clientConnect("LAN")
                if status == "SUCCESS":

                        if wlan_os_type == "UBUNTU":
				command="sudo sh %s refresh_lan_network %s" %(lan_script,lanInterface)
                                executeCommand(command)
                                sleep(20);

                                command="sudo sh %s get_lan_ip_address %s %s" %(lan_script,lanInterface,lan_inet_address)
                                status = executeCommand(command)
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to lan client"

        except Exception, e:
                print e;
                status = e;

        print "LAN IP Address after connecting to LAN client:%s" %status;
        return status;

########## End of Function ##########


def getLanSubnetMask(lanInterface):

# getWlanSubnetMask

# Syntax      : getLanSubnetMask()
# Description : Function to get the subnet mask of the lan client 
# Parameters  : lanInterface - lan interface name
# Return Value: status - Subnetmask of the LAN client

        try:
                status = clientConnect("LAN")
                if status == "SUCCESS":

                        if wlan_os_type == "UBUNTU":
                                command="sudo sh %s refresh_lan_network %s" %(lan_script,lanInterface)
                                executeCommand(command)
                                sleep(20);

                                command="sudo sh %s get_lan_subnet_mask %s %s" %(lan_script,lanInterface,lan_subnet_mask)
                                status = executeCommand(command)
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to lan client"

        except Exception, e:
                print e;
                status = e;

        print "Subnetmask of LAN client is :%s" %status;
        return status;

########## End of Function ##########


def getWlanMACAddress(wlanInterface):

# getWlanMACAddress

# Syntax      : getWlanMACAddress()
# Description : Function to get the MAC address of the wlan client on the given interface
# Parameters  : wlanInterface - wlan interface name
# Return Value: status - MAC Address of the WLAN client

        try:
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_wlan_mac %s" %(wlan_script,wlanInterface)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"

        except Exception, e:
                print e;
                status = e;

        print "WLAN MAC Address after connecting to WIFI:%s" %status;
        return status;

########## End of Function ##########

def getChannelNumber(ssidName):

# getChannelNumber

# Syntax      : getChannelNumber()
# Description : Function to get the channel number of the WIFI connected
# Parameters  : ssidName - SSID Name
# Return Value: Returns the channel number

        try:
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_channel_number %s" %(wlan_script,ssidName)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                status = e;

        print "Connected WIFI's channel number:%s" %status;
        return status;

########## End of Function ##########


def getOperatingStandard(ssidName):

# getOperatingStandard

# Syntax      : getOperatingStandard()
# Description : Function to get the operating standard of the WIFI connected
# Parameters  : ssidName - SSID Name
# Return Value: Returns the current operating standard

        try:
		operating_standard = ""
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_bit_rate %s" %(wlan_script,ssidName)
                        status = executeCommand(command)
			if status == "11":
				operating_standard = "802.11b"
			elif status >= "54":
				operating_standard = "802.11n"
			else:
				operating_standard = "Invalid operating standard"
				
                else:
                        operating_standard = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                operating_standard = e;

        print "Connected WIFI's operating standard:%s" %operating_standard;
        return operating_standard;

########## End of Function ##########


def getSecurityMode(ssidName):

# getSecurityMode

# Syntax      : getSecurityMode()
# Description : Function to get the security mode of the WIFI connected
# Parameters  : ssidName - SSID Name
# Return Value: Returns the current security mode

        try:
                security_mode = ""
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_security_mode %s" %(wlan_script,ssidName)
                        status = executeCommand(command)
			print status
                        if status == "WPA2":
                                security_mode = "WPA2-Personal"
                        elif status == "WPA1":
                                security_mode = "WPA-Personal"
			elif status == "--" or status == "":
                                security_mode = "Open"
                        else:
                                security_mode = "Invalid security mode"

                else:
                        security_mode = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                security_mode = e;

        print "Connected WIFI's security mode:%s" %security_mode;
        return security_mode;

########## End of Function ##########

def checkIpRange(ip1,ip2):

# checkIpRange

# Syntax      : checkIpRange()
# Description : Function to check whether both ips are in same range
# Parameters  : ip1 - ip address
#             : ip2 - ip address
# Return Value: SUCCESS/FAILURE

	try:
        	status = "SUCCESS"
        	ip1 = ip1.split('.')
        	ip2 = ip2.split('.')
        	print ip1,ip2
        	for i in range(len(ip1)-1):
                	if ip1[i] != ip2[i]:
                        	print "IP address not in same DHCP range"
                        	status = "FAILURE"
                        	break;
	except Exception, e:
                print e;
                status = e;
        
	return status

######### End of Function ##########

def checkIpWithinMinMaxRange(ipmin,ipmax,ip):

# checkIpRange

# Syntax      : checkIpWithinMinMaxRange()
# Description : Function to check whether a given ip is within a minimum and maximum range
# Parameters  : ipmin - minimum address of the ip range
#             : ipmax - maximum address of the ip range
#             : ip    -  the ip to be verified
# Return Value: SUCCESS/FAILURE

        try:
                status = "SUCCESS"
                ipmin = ipmin.split('.')
                ipmax = ipmax.split('.')
                ip = ip.split('.')
                print ipmin,ipmax,ip
                for i in range(len(ipmin)-1):
                        if ipmin[i] != ip[i] or ipmax[i] != ip[i]:
                                print "IP address not in same DHCP range"
                                status = "FAILURE"
                                break;
                index = len(ipmin)-1
                if ipmax[index] >= ip[index] and ip[index] >= ipmin[index] :
                        print "Ip address is with in the given range"
                else:
                        status = "FAILURE"
                        print "Ip address is not with in the given range"

        except Exception, e:
                print e;
                status = e;

        return status

######### End of Function ##########

def getMultipleParameterValues(obj,paramList):

# getMultipleParameterValues

# Syntax      : getMultipleParameterValues()
# Description : Function to get the values of multiple parameters at single shot
# Parameters  : obj - module object
#	      : paramList - List of parameter names
# Return Value: SUCCESS/FAILURE

    expectedresult="SUCCESS";
    status = "SUCCESS";

    actualresult= [];
    orgValue = [];

    #Parse and store the values retrieved in a list
    for index in range(len(paramList)):
        tdkTestObj = obj.createTestStep("tdkb_e2e_Get");
        tdkTestObj.addParameter("paramName",paramList[index])
        tdkTestObj.executeTestCase(expectedresult);
        actualresult.append(tdkTestObj.getResult())
	details = tdkTestObj.getResultDetails();
	if "VALUE:" in details:
        	orgValue.append( details.split("VALUE:")[1].split(' ')[0] );

    for index in range(len(paramList)):
	if expectedresult not in actualresult[index]:
	    status = "FAILURE";
	    break;

    return (tdkTestObj,status,orgValue);

######### End of Function ##########


def getParameterValue(obj,param):

# getParameterValues

# Syntax      : getParameterValues()
# Description : Function to get the value of single TR-181 parameter
# Parameters  : obj - module object
#             : param - TR-181 parameter name
# Return Value: SUCCESS/FAILURE

    	expectedresult="SUCCESS";

    	#Parse and store the values retrieved in a list
    	tdkTestObj = obj.createTestStep("tdkb_e2e_Get");
    	tdkTestObj.addParameter("paramName",param)
    	tdkTestObj.executeTestCase(expectedresult);
    	actualresult = tdkTestObj.getResult()
    	details = tdkTestObj.getResultDetails();
	if "VALUE:" in details:
    		value = details.split("VALUE:")[1].split(' ')[0] ;

    	return (tdkTestObj,actualresult,value);

######### End of Function ##########


def setMultipleParameterValues(obj,paramList):

# setMultipleParameterValues

# Syntax      : setMultipleParameterValues()
# Description : Function to set the values of multiple parameters at single shot
# Parameters  : obj - module object
#             : paramList - List of parameter names
# Return Value: SUCCESS/FAILURE

	tdkTestObj = obj.createTestStep("tdkb_e2e_SetMultipleParams");
    	
	expectedresult="SUCCESS";
	tdkTestObj.addParameter("paramList",paramList);
	tdkTestObj.executeTestCase(expectedresult);
	actualresult = tdkTestObj.getResult();
	details = tdkTestObj.getResultDetails();
	#This is a workaround added for emulator. This delay will be removed once RDKBEMU-498 is resolved
	sleep(20)

	return (tdkTestObj,actualresult,details);

######### End of Function ##########


def verifyNetworkConnectivity(dest_ip,connectivityType,source_ip,gateway_ip,source="WLAN"):

# verifyNetworkConnectivity

# Syntax      : verifyNetworkConnectivity()
# Description : Function to check if the internet is accessible or not
# Parameters  : dest_ip - IP to which ping/http/https should reach
#               connectivityType - PING/HTTP/HTTPS
#               source_ip - Ip from which ping/http/https to be placed
#               gateway_ip - Gateway IP address
# Return Value: Returns the status of ping operation

        try:
                status = clientConnect(source)
                if status == "SUCCESS":
                        if wlan_os_type == "UBUNTU":
				if source == "WLAN":
                                    script_name = wlan_script;
                                elif source == "LAN":
                                    script_name = lan_script;
                                else:
                                    script_name = wan_script;
                                if connectivityType == "PING":
                                    command="sudo sh %s ping_to_network %s %s %s" %(script_name,source_ip,dest_ip,gateway_ip)
                                elif connectivityType == "WGET_HTTP":
                                    command="sudo sh %s wget_http_network %s %s %s" %(script_name,source_ip,dest_ip,http_port)
                                elif connectivityType == "WGET_HTTPS":
                                    command="sudo sh %s wget_https_network %s %s %s" %(script_name,source_ip,dest_ip,https_port)
                                status = executeCommand(command)
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to wlan client"
        except Exception, e:
                print e;
                status = e;

        print "Status of verifyNetworkConnectivity:%s" %status;
        return status;

########## End of Function ##########

def ftpToClient(dest, network_ip, source="LAN"):

# ftpToClient

# Syntax      : ftpToClient()
# Description : Function to connect to the client machine via ftp
# Parameters  : network_ip: destination ip
#               clientType : FTP to LAN/WLAN
# Return Value: Returns the status of ftp connection

        try:
                status = clientConnect(source)
                if status == "SUCCESS":
                        if lan_os_type == "UBUNTU":
                                if dest == "WLAN" and source == "WAN":
                                    command="sudo sh %s ftpToClient %s %s %s" %(wan_script,network_ip,wlan_ftp_username,wlan_ftp_password)
                                elif dest == "WLAN" :
                                    command="sudo sh %s ftpToClient %s %s %s" %(lan_script,network_ip,wlan_ftp_username,wlan_ftp_password)
                                elif dest == "LAN":
                                    command="sudo sh %s ftpToClient %s %s %s" %(wlan_script,network_ip,lan_ftp_username,lan_ftp_password)
                                elif dest == "WAN" and source == "LAN":
                                    command="sudo sh %s ftpToClient %s %s %s" %(lan_script,network_ip,wan_ftp_username,wan_ftp_password)
                                elif dest == "WAN" and source == "WLAN":
                                    command="sudo sh %s ftpToClient %s %s %s" %(wlan_script,network_ip,wan_ftp_username,wan_ftp_password)
                                else:
                                    return "Invalid source or destination"

                                status = executeCommand(command)

                                if "230 Login successful" in status or "230 User logged in" in status:
                                    status = "SUCCESS"
                                else:
                                    status = "FAILURE"
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to wlan client"
        except Exception, e:
                print e;
                status = e;

        print "Status of ftpToClient:%s" %status;
        return status;

########## End of Function ##########

def telnetToClient(dest,dest_ip,source="LAN"):

# telnetToClient

# Syntax      : telnetToClient()
# Description : Function to do a telnet from one client to another
# Parameters  : clientType : WLAN/LAN
#               dest_ip  : IP to which telnet should happen
# Return Value: SUCCESS/FAILURE

        try:
                if wlan_os_type == "UBUNTU":
                    status = clientConnect(source)
                    if status == "SUCCESS":
                        if dest == "WLAN":
                                command="sudo sh %s telnetToClient %s %s %s" %(lan_script,dest_ip,wlan_username,wlan_password)
                        elif dest == "LAN":
                                command="sudo sh %s telnetToClient %s %s %s" %(wlan_script,dest_ip,lan_username,lan_password)
                        elif dest == "WAN" and source == "WLAN"::
                                command="sudo sh %s telnetToClient %s %s %s" %(wlan_script,dest_ip,wan_username,wan_password)
                        elif dest == "WAN" and source == "LAN":
                                command="sudo sh %s telnetToClient %s %s %s" %(lan_script,dest_ip,wan_username,wan_password)
                        else:
                                    return "Invalid argument"
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
                        return status

        except Exception, e:
                print e;
                status = e;
                return status

        print "Telnet connection status is : %s" %status;
        if "Connected to" not in status or "No route to host" in status or "Unable to connect to remote host" in status:
                return "FAILURE"
        else:
                return "SUCCESS"

########## End of Function ##########

def getWlanAccessPoint(wlanInterface):

# getWlanAccessPoint

# Syntax      : getWlanAccessPoint()
# Description : Function to get the AccessPoint of the wlan client on the given interface
# Parameters  : wlanInterface - wlan interface name
# Return Value: status - Access Point of the WLAN client

        try:
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_wlan_accesspoint %s" %(wlan_script,wlanInterface)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"

        except Exception, e:
                print e;
                status = e;

        print "WLAN Access Point after connecting to WIFI:%s" %status;
        return status;

######### End of Function ##########

def deleteSavedWifiConnections():

# deleteSavedWifiConnections

# Syntax      : deleteSavedWifiConnections()
# Description : Function to delete the saved wifi connections
# Parameters  : None
# Return Value: SUCCESS/FAILURE

        try:
                status = clientConnect("WLAN")
                if status == "SUCCESS":
                        if wlan_os_type == "UBUNTU":
                                command="sudo sh %s delete_saved_wifi_connections %s %s" %(wlan_script,ssid_2ghz_name,ssid_5ghz_name)
                                status = executeCommand(command)
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to wlan client"

        except Exception, e:
                print e;
                status = e;

        print "Delete saved wifi connections:%s" %status;

        #Logic to delete the saved wifi connections using nmcli
        res = commands.getstatusoutput("nmcli -t -f TYPE,UUID con")
        lines = res[1].split('\n')

        for line in lines:
                parts = line.split(":")
                if (parts[0] == "802-11-wireless"):
                        os.system("nmcli connection delete uuid "+ parts[1])

        return status;

######### End of Function ##########

def addStaticRoute(destIp, gwIp, interface, source="WLAN"):

# addStaticRoute

# Syntax      : addStaticRoute(destIp, gwIp, interface)
# Description : Function to add a new static route to the destIp via gwIp
# Parameters  : destIp : Ip to which new route is to be added
#               gwIp   : Gateway ip through which routing should happen
#	      interface : interface for static routing
#               source  :  client machine type in which route is being added
#
# Return Value: SUCCESS/FAILURE

        try:
                if wlan_os_type == "UBUNTU":
                        if source == "WLAN":
                                script_name = wlan_script;
                        else:
                                script_name = lan_script;

                        command="sudo sh %s add_static_route %s %s %s" %(script_name,destIp,gwIp,interface)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"

        except Exception, e:
                print e;
                status = e;

        print "Route add status is :%s" %status;
        return status;
######### End of Function ##########


def delStaticRoute(destIp, gwIp, interface, source="WLAN"):
# delStaticRoute

# Syntax      : addStaticRoute(destIp, gwIp, interface, source="WLAN")
# Description : Function to delete a static route to the destIp via gwIp
# Parameters  : destIp : Ip to which new route is to be added
#               gwIp   : Gateway ip through which routing should happen
#             interface : interface for static routing
#               source  :  client machine type in which route is being added
# Return Value: SUCCESS/FAILURE

        try:
                if wlan_os_type == "UBUNTU":
                        if source == "WLAN":
                                script_name = wlan_script;
                        else:
                                script_name = lan_script;

                        command="sudo sh %s del_static_route %s %s %s" %(script_name, destIp, gwIp, interface)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"

        except Exception, e:
                print e;
                status = e;

        print "Route delete status is :%s" %status;
        return status;

######### End of Function ##########

def wgetToWAN(connectivityType,source_ip,gateway_ip,source="WLAN"):

# wgetToWAN

# Syntax      : wgetToWAN(connectivityType,source_ip,gateway_ip,source="WLAN")
# Description : Function to do wget to WAN client from other client devices
# Parameters  : connectivityType - PING/HTTP/HTTPS
#               source_ip - Ip from which ping/http/https to be placed
#               gateway_ip - Gateway IP address
#               source  :  client machine type from which wget is to be done
# Return Value: Returns the status of wget operation

        try:
                status = clientConnect(source)
                if status == "SUCCESS":
                        if wlan_os_type == "UBUNTU":
                                if source == "WLAN":
                                    script_name = wlan_script;
                                else:
                                    script_name = lan_script;
                                if connectivityType == "WGET_HTTP":
                                    command="sudo sh %s wget_http_network %s %s %s" %(script_name,source_ip,wan_http_ip,wan_http_port)
                                elif connectivityType == "WGET_HTTPS":
                                    command="sudo sh %s wget_https_network %s %s %s" %(script_name,source_ip,wan_https_ip,wan_https_port)
                                status = executeCommand(command)
                        else:
                                status = "Only UBUNTU platform supported!!!"
                else:
                        return "Failed to connect to wan client"
        except Exception, e:
                print e;
                status = e;

        print "Status of verifyNetworkConnectivity:%s" %status;
        return status;

########## End of Function ##########

def nslookupInClient(domainName,serverIP,source):

# nslookupInClient

# Syntax      : nslookupInClient()
# Description : Function to do nslookup in client machine
# Parameters  : domainName - The domainName which needs to be resolved
#		serverIP - DNS server ip
#               source - The client from which the command should execute
# Return Value: status - Status of nslookup command

        try:
            status = clientConnect(source)
            if status == "SUCCESS":
                if wlan_os_type == "UBUNTU":
                        if source == "WLAN":
                            script_name = wlan_script;
                        else:
                            script_name = lan_script;
                        command="sudo sh %s nslookup_in_client %s %s" %(script_name,domainName,serverIP)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                status = e;
        print "Status of nslookupInClient:%s" %status;
        return status;

########## End of Function ##########


# getLanDhcpDetails

# Syntax      : getLanDhcpDetails()
# Description : Function to fetch dhcp confiiguration values like lease-time, domain-name and dns
# Parameters  : param  - The dhcp configuration attribute name, like lease-time, domain-name and dns
# Return Value: status - dhcp attribute value

def getLanDhcpDetails(param):

        try:
            status = clientConnect("LAN")
            if status == "SUCCESS":
                if wlan_os_type == "UBUNTU":
                        command="sudo sh %s get_lan_dhcp_details %s %s %s" %(lan_script, lan_dhcp_location, lan_interface, param)
                        status = executeCommand(command)
                else:
                        status = "Only UBUNTU platform supported!!!"
        except Exception, e:
                print e;
                status = e;
        print "Status of getDhcpDetails: %s" %status;
        return status;

########## End of Function ##########

def postExecutionCleanup():

# postExecutionCleanup

# Syntax      : postExecutionCleanup()
# Description : Function to perform any post execution cleanup
# Parameters  : None
# Return Value: None

        wifiDisconnect(wlan_2ghz_interface);
        wifiDisconnect(wlan_5ghz_interface);
        deleteSavedWifiConnections();
	clientDisconnect();

######### End of Function ##########
