#!/bin/sh
#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2014 Comcast. All rights reserved.
# ============================================================================
#
# This script runs the sar command
# The sar command writes statistics information the specified number of times (COUNT) 
# spaced at the specified intervals in seconds (INTERVAL)

# Usage help
#       sar -b -B -n DEV -n EDEV -q -r -S -u [ INTERVAL ][ COUNT ]

# options:
#       -b              :  Physical device IO transfer rate statistics
#       -B              :  Paging statistics
#       -n DEV  	:  Network devices statistics
#       -n EDEV 	:  Network devices error statistics
#       -q              :  Load averages statistics
#       -r              :  Memory utilization statistics
#       -S              :  Swap space utilization statistics
#       -u              :  CPU utilization statistics

#echo "%cpu: Percentage of CPU utilization at the user level" >> systemDiagnostics.log
#echo "kbmemfree: Amount of free memory available in kilobytes" >> systemDiagnostics.log
#echo "kbmemused: Amount of used memory in kilobytes" >> systemDiagnostics.log
#echo "%memused: Percentage of used memory" >> systemDiagnostics.log
#echo "pgpgin/s: Total number of kilobytes the system paged in from disk per second" >> systemDiagnostics.log
#echo "pgpgout/s: Total number of kilobytes the system paged out to disk per second" >> systemDiagnostics.log
#echo "kbswpfree: Amount of free swap space in kilobytes" >> systemDiagnostics.log
#echo "kbswpused: Amount of used swap space in kilobytes" >> systemDiagnostics.log
#echo "%swpused: Percentage of used swap space" >> systemDiagnostics.log
#echo "ldavg-1: System load average for the last minute" >> systemDiagnostics.log
#echo "ldavg-5: System load average for the past 5 minutes" >> systemDiagnostics.log
#echo "ldavg-15: System load average for the past 15 minutes" >> systemDiagnostics.log
#echo "tps: Total number of I/O transfer per second that were issued to physical devices" >> systemDiagnostics.log
#echo "IFACE: Name of the network interface for which statistics are reported" >> systemDiagnostics.log 
#echo "%ifutil: Utilization percentage of the network interface" >> systemDiagnostics.log
#echo "rxerr/s: Total number of bad packets received per second" >> systemDiagnostics.log
#echo "txerr/s: Total number of errors that happened per second while transmitting packets" >> systemDiagnostics.log

export PATH=$PATH:/usr/local/bin:/usr/local/lib:/usr/local/lib/sa
export TDK_PATH=/opt/TDK

cd $TDK_PATH

sar -q -r -S -B -u -b -n DEV -n EDEV 1 1 | awk ' /Average:/ { print $0 }' > sysStatAvg.log

echo "#CPU START" > systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "%cpu;",$2 }' | awk -F ' ' '{ print $1" "$4 }' >> systemDiagnostics.log
echo "#CPU END" >> systemDiagnostics.log
echo "#MEMORY START" >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "kbmemfree;",$8 }' | awk -F ' ' '{ print $1" "$3 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "kbmemused;",$8 }' | awk -F ' ' '{ print $1" "$4 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "%memused;",$8 }' |  awk -F ' ' '{ print $1" "$5 }' >> systemDiagnostics.log
echo "#MEMORY END" >> systemDiagnostics.log
echo "#PAGING START" >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "pgpgin/s;",$4 }' | awk -F ' ' '{ print $1" "$3 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "pgpgout/s;",$4 }' | awk -F ' ' '{ print $1" "$4 }' >> systemDiagnostics.log
echo "#PAGING END" >> systemDiagnostics.log
echo "#SWAPING START" >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "kbswpfree;",$10 }' | awk -F ' ' '{ print $1" "$3 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "kbswpused;",$10 }' | awk -F ' ' '{ print $1" "$4 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "%swpused;",$10 }' | awk -F ' ' '{ print $1" "$5 }' >> systemDiagnostics.log
echo "#SWAPING END" >> systemDiagnostics.log
echo "#LOAD AVERAGE START" >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "ldavg-1;",$12 }' | awk -F ' ' '{ print $1" "$5 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "ldavg-5;",$12 }' | awk -F ' ' '{ print $1" "$6 }' >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "ldavg-15;",$12 }' | awk -F ' ' '{ print $1" "$7 }' >> systemDiagnostics.log
echo "#LOAD AVERAGE END" >> systemDiagnostics.log
echo "#IO TRANSFER RATE START" >> systemDiagnostics.log
cat sysStatAvg.log | awk 'BEGIN { RS="" ; FS="\n" } { print "tps;",$6 }' | awk -F ' ' '{ print $1" "$3 }' >> systemDiagnostics.log
echo "#IO TRANSFER RATE END" >> systemDiagnostics.log
echo "#NETWORK DEVICE UTIL START" >> systemDiagnostics.log
echo "IFACE;%ifutil" >> systemDiagnostics.log
total=`cat sysStatAvg.log | awk ' /eth/ { print $0 }' | wc -l`
half=$(($total / 2))
cat sysStatAvg.log | awk ' /eth/ { print $0 }' | head -n $half | awk -F ' ' '{ print $2";"$(NF)}' >> systemDiagnostics.log
echo "#NETWORK DEVICE UTIL END" >> systemDiagnostics.log
echo "#NETWORK DEVICE ERR START" >> systemDiagnostics.log
echo "IFACE;rxerr/s;txerr/s" >> systemDiagnostics.log
cat sysStatAvg.log | awk ' /eth/ { print $0 }' | tail -n $half | awk -F ' ' '{ print $2";"$3";"$4}' >> systemDiagnostics.log
echo "#NETWORK DEVICE ERR END" >> systemDiagnostics.log
