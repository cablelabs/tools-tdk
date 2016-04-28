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
