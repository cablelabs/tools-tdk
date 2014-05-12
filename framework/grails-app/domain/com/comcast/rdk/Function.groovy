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
 * Indicates a function inside a Module.
 * @author ajith
 */

class Function {
    
    /**
     * Name of the Function.
     */
    String name
    
    /**
     * Parent Module.
     */
    Module module

    static constraints =  {
        name(nullable:false, blank:false)
        module(nullable:false)
    }
    /**
     * Generated HashCode and Equals
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ( ( module == null ) ? 0 : module.hashCode() );
        result = prime * result + ( ( name == null ) ? 0 : name.hashCode() );
        return result;
    }

    @Override
    public boolean equals( Object obj ) {
        if ( obj == null )
            return false;
        if ( getClass() != obj.getClass() )
            return false;
        Function other = ( Function ) obj;
        if ( module == null ) {
            if ( other.module != null )
                return false;
        }
        else if ( !module.equals( other.module ) )
            return false;
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
	
	static mapping = {
		datasource 'ALL'
	}
}
