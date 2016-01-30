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
				<li><a class="home" href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="list" action="list"><g:message code="default.list.label" args="[entityName]" /></g:link></li>
				<%--<li><g:link class="create" action="create"> <g:message code="Create Module" /></g:link></li>
				--%><li><g:link class=" create" action= " createParameter"> <g:message code= "Create Parameter"/></g:link></li>			
			</ul>
		</div>
	
		<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
		</g:if>
		<div id="create-function" class="content scaffold-create" role="main"   style="height:250px">
		<br>
		<br>
		    <g:set var="entityName1" value="${message(code: 'function.label', default: 'Function')}" />
			<h1><g:message code="default.create.label" args="[entityName1]"  /></h1>			
			<g:hasErrors bean="${functionInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${functionInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
			<g:form action="saveFunction" >
				<fieldset class="form">
					<g:render template="functionform"/>
				</fieldset>
				<%-- <fieldset class="buttons">					
				</fieldset> --%>
			</g:form>
		</div>
	</body>
</html>

