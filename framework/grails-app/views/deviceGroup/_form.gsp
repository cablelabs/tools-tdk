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
<%@ page import="com.comcast.rdk.DeviceGroup" %>
<%@ page import="com.comcast.rdk.Device" %>


<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="deviceGroups.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${deviceGroupsInstance?.name}" class="textwidth"/>
</div>

<div class="fieldcontain ${hasErrors(bean: deviceGroupsInstance, field: 'devices', 'error')} ">
	<label for="devices">
		<g:message code="deviceGroups.devices.label" default="Devices" />		
	</label>
	<select id="devices" name="devices" class="selectCombo" >
			<g:each in="${com.comcast.rdk.Device.list()}"
				var="device">
				<option value="${device.id}">
					${device.stbName}
				</option>
				<option value="${device.id}">
					${device.boxType}
				</option>
			</g:each>
	</select>	
</div>

