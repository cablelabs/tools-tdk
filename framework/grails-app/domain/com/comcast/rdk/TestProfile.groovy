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
import com.comcast.rdk.Category
/**
 * Class represents BoxTypes.
 * @author sreejasuma
 */
class TestProfile {

	/**
	 * Name of the BoxType
	 */
	String name
	
	/**
	 * Indicates the group name which the box belongs
	 */
	Groups groups
	
	Category category = Category.RDKV
	
	static constraints = {
        name(unique:true, blank:false, nullable:false)
		category(nullable:false, blank:false)
		groups(nullable:true, blank:true)
    }
	
	@Override
	String toString() {
		return name ?: 'NULL'
	}
	
	static mapping = {
		sort id : "asc"
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
