#!/bin/bash

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

# Check whether the SSID to be connected is listed in the network
is_ssid_available()
{
        value="$(nmcli device wifi list | grep $var2)"
        echo "OUTPUT:$value"
}

# Connect to the WIFI SSID
wifi_ssid_connect()
{
        value="$(nmcli device wifi connect $var2 password $var3 | tr -cd [:print:])"
	printf "OUTPUT:$value"
}

# Connect to the WIFI SSID with security mode None
wifi_ssid_connect_openSecurity()
{
        value="$(nmcli device wifi connect $var2 | tr -cd [:print:])"
        printf "OUTPUT:$value"
}
# Disconnect from the WIFI SSID
wifi_ssid_disconnect()
{
        value="$(nmcli device disconnect $var2 | tr -cd [:print:])"
        echo "OUTPUT:$value"
}

# Get the IP address of the WLAN after connecting to WIFI
get_wlan_ip_address()
{
        value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
        echo "OUTPUT:$value"
}

# Get the current SSID name of the WIFI connected
get_connected_ssid_name()
{
        value="$(nmcli device |grep $var2| awk '{ print $4 }')"
        echo "OUTPUT:$value"
}

# Get the current channel number of the WIFI connected
get_channel_number()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $4 }')"
        echo "OUTPUT:$value"
}

# Get the current bit rate of the WIFI connected
get_bit_rate()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $5 }')"
        echo "OUTPUT:$value"
}

# Get the current security mode of the WIFI connected
get_security_mode()
{
        value="$(nmcli device wifi list |grep $var2| awk '{ print $9 }')"
        echo "OUTPUT:$value"
}

#Verify ping to a network
ping_to_network()
{
        route_add_cmd="$(sudo ip route add $var2 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        ping_cmd="$(ping -I $var3 -c 3 $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo ip route delete $var2 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $route_add_cmd = "SUCCESS" ] && [ $ping_cmd = "SUCCESS" ]  && [ $route_del_cmd = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#To send http request to a network
wget_http_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 http://$var3:$var4 && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send https request to a network
wget_https_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 https://$var3:$var4 --no-check-certificate && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

# Refresh the wifi network of the WLAN client
refresh_wifi_network()
{
        value="$(nmcli radio wifi off;nmcli radio wifi on)"
        echo "OUTPUT:$value"
}

# Store the arguments to a variable
event=$1
var2=$2
var3=$3
var4=$4

#echo "\r\n";

# Invoke the function based on the argument passed
case $event in
   "wifi_ssid_connect")
        wifi_ssid_connect;;
   "wifi_ssid_connect_openSecurity")
        wifi_ssid_connect_openSecurity;;
   "wifi_ssid_disconnect")
        wifi_ssid_disconnect;;
   "get_wlan_ip_address")
        get_wlan_ip_address;;
   "get_connected_ssid_name")
        get_connected_ssid_name;;
   "is_ssid_available")
        is_ssid_available;;
   "get_channel_number")
        get_channel_number;;
   "get_bit_rate")
        get_bit_rate;;
   "get_security_mode")
        get_security_mode;;
   "ping_to_network")
        ping_to_network;;
   "wget_http_network")
        wget_http_network;;
   "wget_https_network")
        wget_https_network;;
   "refresh_wifi_network")
        refresh_wifi_network;;
   *) echo "Invalid Argument passed";;
esac

