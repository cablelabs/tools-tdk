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

<g:set var="entityName" value="${message(code: 'scriptGroup.label', default: 'TestSuite')}" />

<a href="#edit-scriptGroup" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
<div id="edit-scriptGroup" class="content scaffold-edit" role="main">
	<h1><g:message code="default.edit.label" args="[entityName]" /></h1>
<g:if test="${flash.message}">
<div class="message" role="status">${flash.message}</div>
</g:if>
<g:hasErrors bean="${scriptGroupInstance}">
<ul class="errors" role="alert">
	<g:eachError bean="${scriptGroupInstance}" var="error">
	<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
	</g:eachError>
</ul>
</g:hasErrors>
<g:form method="post" >
	<g:hiddenField name="id" value="${scriptGroupInstance?.id}" />
	<g:hiddenField name="version" value="${scriptGroupInstance?.version}" />
	<fieldset class="form">
		<g:render template="form"/>
	</fieldset>
	<%--<fieldset class="buttons">--%>
	<div style="width : 90%; text-align: center;">
		<span class="buttons"><g:actionSubmit class="save" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
		<span class="buttons"><g:actionSubmit class="delete" action="deleteScriptGrp" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
	</div>
	<%--</fieldset>--%>
	</g:form>
</div>

