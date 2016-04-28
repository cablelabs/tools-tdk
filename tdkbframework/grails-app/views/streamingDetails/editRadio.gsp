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
<%@ page import="com.comcast.rdk.StreamingDetails" %>
<%@ page import="com.comcast.rdk.RadioStreamingDetails" %>
				
<div id="edit-streamingDetails" class="content scaffold-edit" role="main">
	<g:set var="entityName" value="${message(code: 'streamingDetails.label', default: 'StreamingDetails')}" />
	<h1><g:message code="default.edit.label" args="[entityName]" /></h1>
	<g:if test="${flash.message}">
	<div class="message" role="status">${flash.message}</div>
	</g:if>
	<g:hasErrors bean="${streamingDetailsInstance}">
	<ul class="errors" role="alert">
		<g:eachError bean="${streamingDetailsInstance}" var="error">
		<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
		</g:eachError>
	</ul>
	</g:hasErrors>
	<g:form method="post" >
		<g:hiddenField name="id" value="${streamingDetailsInstance?.id}" />
		<g:hiddenField name="version" value="${streamingDetailsInstance?.version}" />
		<fieldset class="form">
			<g:render template="formRadio"/>
		</fieldset>
		<div style="width : 100%;text-align: center;">
			<span class="buttons">
			<g:actionSubmit class="save" action="updateRadio" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>
			<span class="buttons"><g:actionSubmit class="delete" action="deleteRadioStreamDetails" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		</div>
	</g:form>
</div>
