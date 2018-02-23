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

# Get the IP address of the LAN after connecting to it
get_lan_ip_address()
{
        value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
        echo "OUTPUT:$value"
}

#Refresh Lan Network
refresh_lan_network()
{
        lan_down="$(ifconfig $var2 down > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        lan_up="$(ifconfig $var2 up > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $lan_down = "SUCCESS" ] && [ $lan_up = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#Verify ping to a network
ping_to_network()
{
        route_add_cmd="$(sudo ip route add $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 10
        ping_cmd="$(ping -I $var2 -c 3 $var3 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo ip route delete $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
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

# Telnet to the client devices
telnetToClient()
{
         value="$({
sleep 2
echo $var3
sleep 2
echo $var4
sleep 1
echo exit
} | telnet $var2 | tr "\n" " ")"
        echo "OUTPUT:$value"
}

# FTP to the client devices
ftpToClient()
{
value="$(SERVER=$var2
USER=$var3
PASSW=$var4

ftp -v -n $SERVER <<END_OF_SESSION
user $USER $PASSW
END_OF_SESSION
)"
echo "OUTPUT:$value"
}

add_static_route()
{
        value="$(sudo route add -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"

        echo "OUTPUT:$value"
}

del_static_route()
{
        value="$(sudo route del -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

nslookup_in_client()
{
        outStatus="$(nslookup $var2 $var3)"
        outStatus=$(printf "%s " $outStatus)
        case $outStatus in
            *"Non-authoritative answer: Name: $var2 Address:"*) value="SUCCESS";;
            *)value="FAILURE"
        esac
        echo "OUTPUT:$value"
}

# Get the subnet mask of the LAN client
get_lan_subnet_mask()
{
        value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 4 | cut -d ' ' -f 1)"
        echo "OUTPUT:$value"
}

# get the DHCP config details like lease-time, dns and domain-name etc
get_lan_dhcp_details()
{
        value1="$(sudo lsof -p `cat $var2/dhclient-$var3.pid` | grep $var3 | awk '{ print $9 }')"
        value="$(cat $value1 | grep $var4 | tail -1 | awk '{ print $3 }' | cut -d ";" -f1)"
        echo "OUTPUT:$value"
}

# To set the server in listening mode
tcp_init_server()
{
        iperf -s > $var2 &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send TCP request from client to server
tcp_request()
{
        value="$(iperf -c $var2 | grep bits/sec | cut -d ' ' -f 11)"
        echo "OUTPUT:$value"
}

#To get the bandwidth from server
validate_tcp_server_output()
{
        serverOutput="$(cat $var2 | grep bits/sec | cut -d ' ' -f 11)"
        echo "OUTPUT:$serverOutput"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

# To set the UDP server in listening mode
udp_init_server()
{
        iperf -s -u &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send UDP request from client to server
udp_request()
{
        value="$(iperf -c $var2 -u > $var3 && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To validate the UDP output
validate_udp_output()
{
        bandwidth="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tail -1)"
        lossPercentage="$(cat $var2 | grep bits/sec | awk '{ print $13 }' | tail -1)"
        echo "OUTPUT:$bandwidth,$lossPercentage"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

#To kill iperf pid
kill_iperf()
{
        pkill iperf
        value="$(ps aux | grep iperf | grep -v "grep" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Verify the FTP download
validate_FTP()
{
        FTP_FILE=$var2
        value="$(ls -lrt $FTP_FILE > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Create the file to verify FTP download
touch_File()
{
        FTP_FILE=$var2
        value="$(touch $FTP_FILE  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Remove the file which is transfered via FTP
remove_File()
{
        FTP_FILE=$var2
        value="$(rm -rf  $FTP_FILE > /dev/null && echo "SUCCESS" || echo "FAILURE")"
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
   "get_lan_ip_address")
        get_lan_ip_address;;
   "refresh_lan_network")
        refresh_lan_network;;
   "ping_to_network")
        ping_to_network;;
   "wget_http_network")
        wget_http_network;;
   "wget_https_network")
        wget_https_network;;
   "telnetToClient")
        telnetToClient;;
   "ftpToClient")
        ftpToClient;;
   "add_static_route")
        add_static_route;;
   "del_static_route")
        del_static_route;;
   "nslookup_in_client")
        nslookup_in_client;;
   "get_lan_subnet_mask")
        get_lan_subnet_mask;;
   "get_lan_dhcp_details")
        get_lan_dhcp_details;;
   "tcp_init_server")
        tcp_init_server;;
   "tcp_request")
        tcp_request;;
   "validate_tcp_server_output")
        validate_tcp_server_output;;
   "udp_init_server")
        udp_init_server;;
   "udp_request")
        udp_request;;
   "validate_udp_output")
        validate_udp_output;;
   "kill_iperf")
        kill_iperf;;
   "validate_FTP")
        validate_FTP;;
    "touch_File")
        touch_File;;
    "remove_File")
        remove_File;;
   *) echo "Invalid Argument passed";;
esac
