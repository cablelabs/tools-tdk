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
 * Represents a PrimitiveTest
 * @author ajith
 *
 */

class PrimitiveTest {
    
    /**
     * Name of the Test.
     */
    String name
    
    /**
     * Name of the Module.
     */
    Module module
    
    /**
     * Name of the function.
     */
    Function function
    
    /**
     * Parameters list
     */
    Set<Parameter> parameters
    
	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    /**
     * Can have many parameters.
     */
    static hasMany = [parameters:Parameter]

    /**
     * Constraints.
     * Ensures that the function parent module and module selected are same.
     * Ensures that the parameter parent is a valid function.
     */
    static constraints = {

        name (nullable:false, blank:false, unique:true)

        module(nullable: false, blank: false)
		groups(nullable:true, blank:true)
        function(nullable:false, validator:{ val, obj ->
            boolean isValid = (val.module == obj.module)
            return isValid
        })

        parameters(nullable:true, blank:true
                , validator: {val, obj ->
                    boolean isValid = false
                    if(val) {
                        for ( Parameter param : val ) {
                            isValid = (param.parameterType.function == obj.function)
                            if(!isValid) {
                                break;
                            }
                        }
                        return isValid
                    }
                    else {
                        return true
                    }
                })
    }
	
	@Override
	String toString() {
		return name ?: ''
	}
   
    
}
