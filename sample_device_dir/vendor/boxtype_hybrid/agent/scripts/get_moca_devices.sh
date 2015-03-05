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
HOME_NETWORK_INTERFACE=<moca_network_interface> #interface on gateway device corresponding to the MoCA network.
#echo "Generating list of MoCA device MACs..."
if [ $# -lt 1 ]; then
	echo "Error! Insufficient arguments. Format is $0 <output file path>"
	exit 1
fi
arp -n -i $HOME_NETWORK_INTERFACE | grep "?" | awk '{print $4}' > $TDK_PATH/$1
#echo "Done"
