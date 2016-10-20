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

PWD=$(pwd)
warfile=$PWD/rdk-test-tool_18Oct2013.war

sudo chmod 777 $warfile

CATALINA_HOME=/opt/comcast/software/tomcat/apache-tomcat-6.0.37
webappsFolder=$CATALINA_HOME/webapps/
sudo chmod -R 777 $webappsFolder

echo " Stoping tomcat......"
sudo /etc/init.d/tomcat6 stop

sleep 5
rm -rf warfile

#Copy war file to tomcat webapp folder
echo " Copying war file...... "
cp $warfile $webappsFolder

echo " Starting tomcat...... "
sudo /etc/init.d/tomcat6 start

sudo chmod -R 777 $webappsFolder

#Wait for war to up
sleep 10
# OPEN the application http://ip:8080/rdk-test-tool_18Oct2013/
