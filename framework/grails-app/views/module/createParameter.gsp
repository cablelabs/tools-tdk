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
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'module.label', default: 'Module')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>			
	</head>
	<body>
		<a href="#create-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" params="[category:category]"  href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="list" params="[category:category]" action="list"><g:message code="default.list.label" args="[entityName]" /></g:link></li>
				</ul>
		</div>	
		<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
		</g:if>
		
		<div id="create-parameterType" class="content scaffold-create" role="main">
			<br>
			<br>
		
			<g:set var="entityName2" value="${message(code: 'parameter.label', default: 'Parameter')}" />
			<h1><g:message code="default.create.label" args="[entityName2]" /></h1>			
			<g:hasErrors bean="${parameterTypeInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${parameterTypeInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<g:form action="saveParameter" >
				<fieldset class="form">
					<g:render template="parametertypeform" model="[category:category]"/>
				</fieldset>
				<%-- <fieldset class="buttons">
					<g:submitButton name="create" class="save" value="${message(code: 'default.button.create.label', default: 'Create')}" />
				</fieldset> --%>
			</g:form>
		</div>		
		</body>
</html>
		