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
package com.comcast.rdk

class User {
    /**
	 * Username of the User
	 */
    String username
	/**
	 * Password of the User
	 */
    String passwordHash
	/**
	 * email address of user
	 */
    String email
	/**
	 * Name of the User
	 */
    String name
	/**
	 * Status of the user 
	 */
    String status
	
	Groups groupName
    
    /**
     * User has many roles and permissions
     */
    static hasMany = [ roles: Role, permissions: String ]

    static constraints = {
        username(nullable: false, blank: false, unique: true)
        email(nullable: false, blank: false)
        name(nullable: false, blank: false)
        status(nullable: true, blank: true)   
        passwordHash(nullable: true, blank: true)
		groupName(nullable: true, blank: true)
    }
    
    @Override
    public String toString()
    {
        return username ?: 'NULL'
    }
    
}
