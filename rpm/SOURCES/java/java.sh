#!/bin/bash
#
# ============================================================================
# COMCAST C O N F I D E N T I A L AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of Comcast.  It may
# not be used, copied, distributed or otherwise  disclosed in whole or in part
# without the express written permission of Comcast.
# ============================================================================
# Copyright (c) 2013 Comcast. All rights reserved.
# ============================================================================
#

JDK_TAR_FILE=jdk-7u21-linux-i586.gz
JDK=jdk1.7.0_21
INSTALATION_PATH=/usr/lib/jvm/

echo $JDK_TAR_FILE
echo $JDK
echo $INSTALATION_PATH

tar -xf $JDK_TAR_FILE
sudo mkdir -p $INSTALATION_PATH
sudo mv $JDK $INSTALATION_PATH
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/$JDK/bin/java" 1
sudo update-alternatives --config java

echo "Java Installation completed"

