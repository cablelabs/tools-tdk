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
    
    static constraints = {
        name(unique:true, blank:false, nullable:false)
        type(blank:false, nullable:false)
    }
    
    /**
     * Generated hashCode and Equals
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ( ( name == null ) ? 0 : name.hashCode() );
        return result;
    }

    @Override
    public boolean equals( Object obj ) {
        if ( obj == null )
            return false;
        if ( getClass() != obj.getClass() )
            return false;
        BoxType other = ( BoxType ) obj;
        if ( name == null ) {
            if ( other.name != null )
                return false;
        }
        else if ( !name.equals( other.name ) )
            return false;
        return true;
    }
	
	@Override
	String toString() {
		return name ?: 'NULL'
	}
}
