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
 * Represents a ParameterType.
 * @author ajith
 */

class ParameterType {
    
    /**
     * Name of the Parameter
     */
    String name
    
    /**
     * Type of the parameter.
     */
    ParameterTypeEnum parameterTypeEnum
    
    /**
     * Value: To be removed from here.
     */
    String rangeVal
    
    /**
     * Parent Function to which this belong to.
     */
    Function function

    static constraints = {
        name(nullable: false, blank: false)
        parameterTypeEnum(nullable: false)
        rangeVal(nullable: false, blank: false)
        function(nullable:false)
    }
  
    
    @Override
    String toString() {
        return name ?: 'NULL'
    }
	
	static mapping = {
		datasource 'ALL'
	}
}
