#!/bin/bash
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

