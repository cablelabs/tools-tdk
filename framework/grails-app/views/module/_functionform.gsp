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
<%@ page import="com.comcast.rdk.Function" %>
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="function.name.label" default="Function Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${functionInstance?.name}"/>
</div>
<%
	def user = User.findByUsername(SecurityUtils.subject.principal)
	def group = Groups.findById(user.groupName?.id)
%>
<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">
		<g:message code="function.module.label" default="Module" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="module" name="module.id" from="${Module.findAllByGroupsOrGroupsIsNull(group, [order: 'asc', sort: 'name'])}" noSelection="['' : 'Please Select']" 
			optionKey="id" required="" value="${functionInstance?.module?.id}" class="many-to-one"/>
</div>

<div class="fieldcontain ${hasErrors(bean: functionInstance, field: 'module', 'error')} required">
	<label for="module">		
	</label>
	<span class="buttons">
	<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
	</span>
</div>
