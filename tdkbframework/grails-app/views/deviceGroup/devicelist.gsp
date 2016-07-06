<!-- 
 ============================================================================
  COMCAST CONFIDENTIAL AND PROPRIETARY
 ============================================================================
  This file and its contents are the intellectual property of Comcast.  It may
  not be used, copied, distributed or otherwise  disclosed in whole or in part
  without the express written permission of Comcast.
  ============================================================================
  Copyright (c) 2013 Comcast. All rights reserved.
  ============================================================================
-->
<g:each in="${deviceInstanceList}" var="device">
	<li>
	<g:if test="${device.deviceStatus.toString()=="FREE" }">
		<span class="filedevicefree" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:if>
	<g:elseif test="${device.deviceStatus.toString()=="NOT_FOUND" }">
		<span class="filedevicenotfound" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	<g:elseif test="${device.deviceStatus.toString()=="BUSY"}">
		<span class="filedevicebusy" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	<g:elseif test="${device.deviceStatus.toString()=="HANG"}">
		<span class="filedevicehang" id="${device.id}"><a href="#" onclick="showDevice('${device.id}'); return false;">${device.stbName}</a></span>
	</g:elseif>
	</li>
</g:each>