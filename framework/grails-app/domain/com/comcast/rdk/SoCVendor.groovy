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
	
    static constraints = {
        name(unique:true, blank:false, nullable:false)
		groups(nullable:true, blank:true)
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
        return true;
    }
}
