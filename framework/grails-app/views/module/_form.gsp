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
<%@ page import="com.comcast.rdk.Module" %>
	
<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="module.name.label" default="Module Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${moduleInstance?.name}"/> 	
</div>

<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'testGroup', 'error')} required">
	<label for="testGroup">
		<g:message code="module.testGroup.label" default="Test Group" />
		<span class="required-indicator">*</span>
	</label>
	<g:select name="testGroup" from="${com.comcast.rdk.TestGroup?.values()}" keys="${com.comcast.rdk.TestGroup.values()*.name()}" required="" value="${moduleInstance?.testGroup?.name()}"/>
</div>

<%--<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'rdkVersion', 'error')} required">
	<label for="name">
		<g:message code="module.rdkVersion.label" default="RDK Version" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="rdkVersion" required="" value="${moduleInstance?.rdkVersion}"/> 	
</div>

--%><div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'executionTime', 'error')} required">
	<label for="name">
		<g:message code="module.executionTime.label" default="Execution TimeOut" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="executionTime" required="" value="${moduleInstance?.executionTime}"/> 	
</div>

<div class="fieldcontain ${hasErrors(bean: moduleInstance, field: 'name', 'error')} required">
	<label for="name">
	</label>
	<span class="buttons"><g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
</div>

