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
#This gives a short description about the installation of RDKTDK Tool in Ubuntu environment.

1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
2) Copy rpm folder to your home directory(eg: /home/user1)
3) Change folder permission.
	chmod -R 777 rpm
4) Move to rpm folder 
	cd rpm/
5) Execute master_rpm.sh(sh master_rpm.sh) 
			( Execution of master_rpm.sh file will install Java(JRE), Apache Tomcat, Mysql, TFTPY and Expect. It will copy pythonLib to PYTHONPATH and upload the latest war to Tomcat server.)

#Edit tomcat user privilages in tomcat-users.xml
	sudo vim /opt/comcast/software/tomcat/apache-tomcat-6.0.37/conf/tomcat-users.xml
Add <user username="rdktdk" password="tel1234#" roles="admin,manager"/> inside <tomcat-users></tomcat-users> tag.

#Restart Tomcat
sudo /etc/init.d/tomcat6 stop
sudo /etc/init.d/tomcat6 start

*Note: - Please note that only users with sudo permission can perform the rpm installation.


#If you want to install the components individually or want to update with latest versions, please follow the below steps.
	
	
1)Java Installation
	
	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Download java 1.6 or above from http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html
			(eg:jdk-7u21-linux-i586.gz from http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html#jdk-7u21-oth-JPR\)
	3) Copy jdk tar to ~/rpm/SOURCES/java folder.
	4) Modify java.sh file based on version you downloaded.
	5) Execute java.sh file(sh java.sh)
	6) Verify proper installation by executing java -version.
	

2)Tomcat Installation

	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Download apache-tomcat-6 
		(eg: apache-tomcat-6.0.37.tar.gz from http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.37/bin/)
	3) Copy tar file to ~/rpm/SOURCES folder.
	4) Build RPM. Go to ~/rpm/SPECS folder and execute rpmbuild -v -bb --clean tomcat_37.spec (Modify tomcat_37.spec as per the version of tomcat used)
	5) Go to ~/rpm/RPMS/i586/ folder
	6) Execute the rpm.
		a) Install alien using command sudo apt-get install alien dpkg-dev debhelper build-essential
		b) Convert .rpm to .deb fromat using command sudo alien packagename.rpm
		c) Execute .deb file using command sudo dpkg -i packagename.deb	
	7) Execute /etc/init.d/tomcat6 start to start the tomcat.
	Note:[ You may need to modify /opt/comcast/software/tomcat/apache-tomcat-6.0.37/conf/tomcat-user.xml to provide authentication information]

	
3)MySQL Installation 

	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Execute setupdb.sh (Modify setupdb.sh file and configuredb.sql file if any changes made in table names or user privilages)	
	   

4)RDKTDK Installation

	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Execute deployWar.sh (Modify war name if needed)
	3) Check the application by opening the URL http://<ip>:8080/appname in the browser.
	
	
5)TFTPY Installation

	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Move to SOURCES/tftp_Python-0.6.0 folder 
		cd ~/rpm/SOURCES/tftp_Python-0.6.0
	3) Execute sudo python setup.py build
	4) Execute sudo python setup.py install
	

6)Copy PythonLib

	1) Checkout https://192.168.160.9/svn/TeComcastRDKTDK/trunk/src/rpm
	2) Move to SOURCES folder 
		cd ~/rpm/SOURCES
	3) Copy python_path.sh to /etc/profile.d/
		sudo cp python_path.sh /etc/profile.d/
	4)Copy pythonLib to $PYTHONPATH
		sudo cp -r pythonLib $PYTHONPATH

7)Expect Installation

	1) Run command sudo apt-get install expect
   

NOTE:

Ubuntu Support only deb package installation, If you have some software in rpm package you can install it in Ubuntu/Linux easily. Fedora/Redhat and Mandriva support RPM packages.
In Ubuntu/Linux you can easily install softwares from Software Centers or via PPA. If any software is not available in deb/software center/ppa and it's only available in rpm, then you can easily convert that rpm file to deb package with one command using terminal.This RPM to DEB Conversion Utility called Alien, Which converts packages from one to the other format. 

#To Install alien 
	sudo apt-get install alien dpkg-dev debhelper build-essential
		
#To convert .rpm to .deb format
	sudo alien packagename.rpm

#To execute .deb file
	sudo dpkg -i packagename.deb
