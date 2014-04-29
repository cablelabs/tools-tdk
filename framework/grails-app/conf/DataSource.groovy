/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2013 Comcast. All rights reserved.
 * ============================================================================
 */

dataSource {
    pooled = true
    driverClassName = "com.mysql.jdbc.Driver"
    intialSize = 10
    maxActive = 100
    dialect = 'org.hibernate.dialect.MySQL5InnoDBDialect'
}
hibernate {
    cache.use_second_level_cache = true
    cache.use_query_cache = false
    cache.region.factory_class = 'net.sf.ehcache.hibernate.EhCacheRegionFactory'
}
// environment specific settings
environments {
    development {
        dataSource {
            dbCreate = "update" // one of 'create', 'create-drop','update'
          // url = "jdbc:mysql://127.0.0.1/rdktesttooldb?autoReconnect=true"
            url = "jdbc:mysql://127.0.0.1/rdktesttooldevdb?autoReconnect=true"
            username = "rdkttuser"
            password = "6dkttus3r!"
        }
    }
    test {
        dataSource {
            dbCreate = "create-drop" // one of 'create', 'create-drop','update'
            url = "jdbc:mysql://127.0.0.1/rdktesttooltestdb?autoReconnect=true"
            username = "rdkttuser"
            password = "6dkttus3r!"
        }
    }
    production {
        dataSource {
            dbCreate = "update"
           // url = "jdbc:mysql://127.0.0.1/rdktesttoolproddbm4?autoReconnect=true" // Test DB for Testers - rdk-tdk-test.war
            url = "jdbc:mysql://127.0.0.1/rdktesttoolproddb?autoReconnect=true"
            username = "rdktesttooluser"
            password = "6dktoolus3r!"
            pooled = true
            properties {
               maxActive = -1
               minEvictableIdleTimeMillis=1800000
               timeBetweenEvictionRunsMillis=1800000
               numTestsPerEvictionRun=3
               testOnBorrow=true
               testWhileIdle=true
               testOnReturn=true
               validationQuery="SELECT 1"
           }
        }
    }
}
