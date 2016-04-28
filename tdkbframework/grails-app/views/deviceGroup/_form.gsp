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
	<%--<g:select id="devices" style="width: 210px;height: 410px;" name="devices" multiple="true" from="${com.comcast.rdk.Device.list().stbName}" value="" />
	--%>
	<g:hiddenField name="category" value="${category}"/>
	<select id="devices" name="devices" class="selectCombo" multiple="true" style="width: 210px;height: 410px;" >
			<g:each in="${devices}"
				var="device">
				<option value="${device.id}">
					${device.stbName}
				</option>
			</g:each>
	</select>	
</div>

