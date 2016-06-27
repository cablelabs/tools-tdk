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

