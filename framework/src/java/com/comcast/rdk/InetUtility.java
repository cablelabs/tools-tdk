package com.comcast.rdk;

import java.util.regex.Pattern;

public class InetUtility {

	private static final Pattern IPV6_STD_PATTERN = Pattern.compile("^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$");
	
	/**
	  * Check whether it is IPv6 address or not.
	  * 
	  * @param ipAddress
	  *            Ipv6 address.
	  * @return True if given ip address is Ipv6.
	  */
	 public static boolean isIPv6Address(final String ipAddress) {
	  return IPV6_STD_PATTERN.matcher(ipAddress).matches();
	 }
	 
}
