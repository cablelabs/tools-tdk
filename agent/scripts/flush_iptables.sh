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
#Abort if there are errors.
set -e
set -o pipefail

echo "Flushing filter table..."
iptables -t filter -F
echo "Done."

echo "Flushing NAT table..."
iptables -t nat -F
echo "Done. Flushed iptables."
