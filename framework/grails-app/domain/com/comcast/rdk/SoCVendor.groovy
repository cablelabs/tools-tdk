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
 * Class for storing SocVendors.
 * @author sreejasuma
 */

class SoCVendor {

    /**
     * Name of the SoCVendor
     */
    String name

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
	/**
	 * Indicates the group name which the device belongs
	 */
	Category category = Category.RDKV
	
    static constraints = {
       // name(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
		category(nullable:false, blank:false)
		name(blank:false, nullable:false,unique:['category'])
    }


    @Override
    public String toString() {
        return name ?: 'NULL'
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ( ( name == null ) ? 0 : name.hashCode() );
        return result;
    }

    @Override
    public boolean equals( Object obj ) {
        if ( this == obj )
            return true;
        if ( obj == null )
            return false;
        if ( getClass() != obj.getClass() )
            return false;
        SoCVendor other = ( SoCVendor ) obj;
        if ( name == null ) {
            if ( other.name != null )
                return false;
        }
        else if ( !name.equals( other.name ) )
            return false;
		else if(category == null){
			if(other.category != null){
				return false
			}
		}
		else if(category != other.category){
			return false
		} 
        return true;
    }
	
	static mapping = {
		category enumType: "string" , defaultValue:'"RDKV"' 
		datasource 'ALL'
	}
}
