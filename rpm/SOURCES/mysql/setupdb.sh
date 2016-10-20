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

#Uninstall mysql
#sudo apt-get -.purge remove mysql-server

#sudo apt-get --purge remove mysql-client

#sudo apt-get --purge remove mysql-common



#Install mysql
echo "Installing mysql..."
sudo apt-get -q -y install mysql-server


#Login to mysql and execute sql query for database,user creation
echo "Configuring database..."
mysql -u root -p < configuredb.sql

#To import data from dump
echo "Importing data to database...."

sudo mysql -u root -p rdktesttoolproddb < rdktestproddbdump.sql
