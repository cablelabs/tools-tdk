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
class BoxType {

    /**
     * Name of the BoxType
     */
    String name

    /**
     * Type of box
     * Eg: client, gateway
     */
    String type 
	
	/**
	 * Indicates the group name which the box belongs
	 */
	Groups groups
	
	Category category = Category.RDKV
    
    static constraints = {
        //name(unique:true, blank:false, nullable:false)
        type(blank:false, nullable:false)
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false)
		name(nullable:false, blank:false, unique:['category'])
    }

	@Override
	String toString() {
		return name ?: 'NULL'
	}
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
