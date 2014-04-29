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
 * Represent the TestGroups
 * @author sreejasuma
 *
 */

public enum TestGroup
{
    E2E( "E2E" ), Component("Component"), OpenSource("OpenSource");
    
    private final String groupValue;

    private TestGroup( String group )
    {
        groupValue = group;
    }
    
    public String getGroupValue() {
        return groupValue;
    }
    
}
