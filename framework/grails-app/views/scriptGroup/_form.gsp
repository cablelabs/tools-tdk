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
<%@ page import="com.comcast.rdk.ScriptGroup" %>

<div class="fieldcontain ${hasErrors(bean: scriptGroupInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="scriptGroup.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${scriptGroupInstance?.name}" style="width: 240px"/>
</div>

<div class="fieldcontain ${hasErrors(bean: scriptGroupInstance, field: 'scriptList', 'error')} ">
	<label for="scripts">
		<g:message code="scriptGroup.scripts.label" default="Scripts" />		
	</label>
	<g:select name="scripts" from="${com.comcast.rdk.Script.list()}" multiple="multiple" optionKey="id" style="width: 250px;height:350px;" size="5" value="${scriptGroupInstance?.scriptList*.id}" class="many-to-many"/>
</div>

