/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2016 Comcast. All rights reserved.
 * ============================================================================
 */
package com.comcast.rdk;

public enum FileStorePath {

	RDKV("testscriptsRDKV"), RDKB("testscriptsRDKB"), RDKTCL("testscriptsTCL");

	private String pathName;

	private FileStorePath(final String pathName) {
		this.pathName = pathName;
	}

	public String value() {
		return pathName;
	}
}
