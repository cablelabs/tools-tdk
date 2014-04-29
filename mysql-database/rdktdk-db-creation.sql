DROP DATABASE IF EXISTS rdktesttooldevdb;
DROP DATABASE IF EXISTS rdktesttoolm1proddb;
DROP DATABASE IF EXISTS rdktesttoolproddb;
drop user 'rdkttuser'@'127.0.0.1','rdkttproduser'@'127.0.0.1','rdktesttooluser'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS rdktesttooldevdb;
CREATE USER 'rdkttuser'@'127.0.0.1' identified by '6dkttus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON rdktesttooldevdb.* TO 'rdkttuser'@'127.0.0.1';


CREATE DATABASE IF NOT EXISTS rdktesttoolm1proddb ;                                                                // DB used for rdk-tdk-test.war
CREATE USER 'rdkttproduser'@'127.0.0.1' identified by 'rdkttpr0dus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER ON  rdktesttoolm1proddb.* TO 'rdkttproduser'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS rdktesttoolproddb;
CREATE USER 'rdktesttooluser'@'127.0.0.1' identified by '6dktoolus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb.* TO 'rdktesttooluser'@'127.0.0.1';