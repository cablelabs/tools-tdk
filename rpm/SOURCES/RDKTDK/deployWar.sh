#!/bin/bash

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
