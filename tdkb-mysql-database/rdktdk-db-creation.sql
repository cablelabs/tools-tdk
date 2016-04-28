//NOTICE: Use this script only if fresh installation of the TDK tool is required

DROP DATABASE IF EXISTS rdktesttoolproddb;
DROP DATABASE IF EXISTS rdktesttoolproddb_temp;
drop user 'rdktesttooluser'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS rdktesttoolproddb;
CREATE USER 'rdktesttooluser'@'127.0.0.1' identified by '6dktoolus3r!';
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb.* TO 'rdktesttooluser'@'127.0.0.1';


CREATE DATABASE IF NOT EXISTS rdktesttoolproddb_temp;
grant CREATE, INSERT, DELETE, UPDATE, SELECT, DROP, ALTER, lock tables ON rdktesttoolproddb_temp.* TO 'rdktesttooluser'@'127.0.0.1';