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

import java.io.File;

/**
 * Custom file name filter to filter the files for which name starting with the provided name.
 *
 */
class CustomFileNameFilter implements FilenameFilter{
	
	String matchingName = null;
	
	public CustomFileNameFilter(String matchingName){
		this.matchingName = matchingName;
	}

	@Override
	boolean accept(File arg0, String name) {
		if(matchingName != null){
			return name.startsWith(matchingName) ? true : false;
		}
		return false;
	}

}
