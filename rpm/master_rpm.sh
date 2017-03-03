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
sudo /etc/init.d/tomcat6 start


#MySQL Installation 

cd ~/rpm/SOURCES/mysql
sh setupdb.sh


#RDK TDK Installation

cd ~/rpm/SOURCES/RDKTDK
sh deployWar.sh

#Expect Installation

sudo apt-get install python-tftpy
sudo apt-get install expect
sudo apt-get install python-MySQLdb
sudo apt-get install python-xlwt
sudo apt-get install python-xlrd
sudo apt-get install python-numpy
sudo apt-get install python-paramiko

