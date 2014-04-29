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
 * Class holds the parameter type and parameter value. 
 * @author ajith
 */

class Parameter {
    
    /**
     * Type of Parameter
     */
    ParameterType parameterType
    
    /**
     * Value of Parameter.
     */
    String value
    
    /**
     * A Parameter shall belong to a PrimitiveTest.
     * TODO: This can be any test not limited to primitive.
     */
    static belongsTo = [primitiveTest: PrimitiveTest]
    /**
     * If the value is integer, its verified and confirmed if it falls in range given.
     * TODO: Range check only done for Integer.
     */
    static constraints = {
        value(nullable:false, validator:{ val, obj ->
            boolean isValid = true
            switch ( obj.parameterType.parameterTypeEnum) {
                case ParameterTypeEnum.INTEGER:
                    try{
                        Integer.valueOf( val )
                    }catch (NumberFormatException e) {
                        isValid = false
                    }
                        if(isValid) {
                            // Check for range here
                            if(obj.parameterType.rangeVal){                                     
                                String range = obj.parameterType.rangeVal
                                String[] edges = range?.split( "-" );
                                if(edges && edges.size() == 2) {
                                    isValid = ((val.toInteger() >= edges[0].toInteger())
                                            && (val.toInteger() <= edges[1].toInteger()))
                                }
                            }
                        }
                    break

                default:
                    break;
            }
            return isValid
        })

        parameterType(nullable:false)

        primitiveTest(nullable:true, blank:true)
    }
    
    @Override
    public String toString()
    {
        return parameterType ?: 'NULL'
    }
}
