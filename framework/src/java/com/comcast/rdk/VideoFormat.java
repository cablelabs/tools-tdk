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
 * Represents the FormatType of the Stream. 
 * @author sreejasuma
 */

public enum VideoFormat
{
        
    mpeg2( "mpeg2" ), mpeg4( "mpeg4" ), h264( "h.264");

    private final String typeValue;

    private VideoFormat( String type )
    {
        typeValue = type;
    }
    
    public String getTypeValue() {
        return typeValue;
    }
    
    /**
     * Method will return  . or , or ' instead of DOT or COMMA or APOSTROPHE
     */     
    public String toString()
    {
       return this.typeValue; 
    }
}
