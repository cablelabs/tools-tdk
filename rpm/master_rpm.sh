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
#File to install Java(JRE), Apache Tomcat, Mysql and TFTPY. It will upload the latest war to Tomcat also.


#Alien Installation 

sudo apt-get install alien dpkg-dev debhelper build-essential	


#Java(JRE) Installation	

cd ~/rpm/SOURCES/java
sh java.sh		


#Tomcat Installation

cd ~/rpm/SPECS
rpmbuild -v -bb --clean tomcat_37.spec
cd ~/rpm/RPMS/i586/
sudo alien apache-tomcat-6.0.37-18.i586.rpm
sudo dpkg -i apache-tomcat_6.0.37-19_i386.deb
sleep 10
sudo etc/init.d/tomcat6 start


#MySQL Installation 

cd ~/rpm/SOURCES/mysql
sh setupdb.sh


#RDK TDK Installation

cd ~/rpm/SOURCES/RDKTDK
sh deployWar.sh


#TFTPY Installation

cd ~/rpm/SOURCES/tftp_Python-0.6.0/
sudo python setup.py build
sudo python setup.py install


#Copy PythonLib

cd ~/rpm/SOURCES
sudo cp python_path.sh /etc/profile.d/
source /etc/profile.d/python_path.sh
sudo mkdir -p $PYTHONPATH
echo "Copying pythonLib....."
sudo cp -r pythonLib/* $PYTHONPATH


#Expect Installation

sudo apt-get install expect

