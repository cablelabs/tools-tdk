--  ============================================================================
-- COMCAST C O N F I D E N T I A L AND PROPRIETARY
-- ============================================================================
-- This file (and its contents) are the intellectual property of Comcast.  It may
-- not be used, copied, distributed or otherwise  disclosed in whole or in part
-- without the express written permission of Comcast.
-- ============================================================================
-- Copyright (c) 2014 Comcast. All rights reserved.
-- ===========================================================================
#Drops database with same name
DROP DATABASE IF EXISTS rdktesttoolproddb;

#Create database, user and privilages for PROD DB
GRANT USAGE ON *.* TO 'rdktesttooluser'@'127.0.0.1';
DROP USER 'rdktesttooluser'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS rdktesttoolproddb;
CREATE USER 'rdktesttooluser'@'127.0.0.1' identified by '6dktoolus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb.* TO 'rdktesttooluser'@'127.0.0.1';


