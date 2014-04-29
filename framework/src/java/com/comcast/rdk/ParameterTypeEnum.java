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
package com.comcast.rdk;

/**
 * Represent the Type of parameter
 * @author ajith
 *
 */
public enum ParameterTypeEnum
{

    STRING( "string" ), INTEGER( "integer" ), FLOAT( "float" ), DOUBLE( "double" );

    private final String typeValue;

    private ParameterTypeEnum( String type )
    {
        typeValue = type;
    }
    
    public String getTypeValue() {
        return typeValue;
    }

}

