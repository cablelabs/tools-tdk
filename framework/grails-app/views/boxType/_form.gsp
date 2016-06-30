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

<%@ page import="com.comcast.rdk.BoxType" %>

<div class="fieldcontain ${hasErrors(bean: boxTypeInstance, field: 'name', 'error')} required">
	<label for="name">
		<g:message code="boxType.name.label" default="Name" />
		<span class="required-indicator">*</span>
	</label>
	<g:textField name="name" required="" value="${boxTypeInstance?.name}"/>
</div>

<div class="fieldcontain ${hasErrors(bean: boxTypeInstance, field: 'type', 'error')} required">
	<label for="type">
		<g:message code="boxType.type.label" default="Type" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="typeId" name="type" from="['Client','Stand-alone-Client','Gateway']" style="width : 150px;"/>
	<%--<g:textField name="type" required="" value="${boxTypeInstance?.type}"/>--%>
</div>
<g:hiddenField name="category" value="${category }"/>
