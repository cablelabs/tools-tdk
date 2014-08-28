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
