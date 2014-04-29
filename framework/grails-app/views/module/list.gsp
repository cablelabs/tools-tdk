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
		<title><g:message code="default.list.label" args="[entityName]" /></title>
	</head>
	<body>
		<a href="#list-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="create" action="create"><g:message code="default.new.label" args="[entityName]" /></g:link></li>
			</ul>
		</div>
		<div id="list-module" class="content scaffold-list" role="main">
			<h1><g:message code="default.list.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<table style="width:30%;">
				<thead>
					<tr>					
						<g:sortableColumn property="name" title="${message(code: 'module.name.label', default: 'Name')}" />
						
						<g:sortableColumn property="testGroup" title="${message(code: 'module.testGroup.label', default: 'Test Group')}" />
							
						<g:sortableColumn property="rdkVersion" title="${message(code: 'module.rdkVersion.label', default: 'RDK Version')}" />
						
						<g:sortableColumn property="executionTime" title="${message(code: 'module.executionTime.label', default: 'Execution TimeOut')}" />			
					</tr>
				</thead>
				<tbody>
				<g:each in="${moduleInstanceList}" status="i" var="moduleInstance">
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
					
						<td><g:link action="show" id="${moduleInstance.id}">${fieldValue(bean: moduleInstance, field: "name")}</g:link></td>
						
						<td>${fieldValue(bean: moduleInstance, field: "testGroup")}</td>
					
						<td>${fieldValue(bean: moduleInstance, field: "rdkVersion")}</td>
						
						<td>${fieldValue(bean: moduleInstance, field: "executionTime")}</td>
					</tr>
				</g:each>
				</tbody>
			</table>
			<div class="pagination">
				<g:paginate total="${moduleInstanceTotal}" />
			</div>
		</div>
	</body>
</html>
