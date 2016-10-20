<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@ page import="com.comcast.rdk.Module" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category}  ${message(code: 'module.label', default: 'Module')}" />
		<title><g:message code="default.list.label" args="[entityName]" /></title>
	</head>
	<body>
		<a href="#list-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
				<li><g:link class="create" action="create" params="[category:category]"><g:message code="default.create.label" args="[entityName]" /></g:link></li>
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
						<g:sortableColumn property="name" title="${message(code: 'module.name.label', default: 'Name')}" params="[category:category]" />
						
						<g:sortableColumn property="testGroup" title="${message(code: 'module.testGroup.label', default: 'Test Group')}" params="[category:category]"/>
							
						<%--<g:sortableColumn property="rdkVersion" title="${message(code: 'module.rdkVersion.label', default: 'RDK Version')}" />
						
						--%><g:sortableColumn property="executionTime" title="${message(code: 'module.executionTime.label', default: 'Execution TimeOut')}" params="[category:category]"/>			
					</tr>
				</thead>
				<tbody>
				<g:each in="${moduleInstanceList}" status="i" var="moduleInstance">
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
					
						<td><g:link action="show" id="${moduleInstance.id}">${fieldValue(bean: moduleInstance, field: "name")}</g:link></td>
						
						<td>${fieldValue(bean: moduleInstance, field: "testGroup")}</td>
					
						<%--<td>${fieldValue(bean: moduleInstance, field: "rdkVersion")}</td>						
						--%>
						<td>${fieldValue(bean: moduleInstance, field: "executionTime")}</td>
					</tr>
				</g:each>
				</tbody>
			</table>
			<div class="pagination">
				<g:paginate total="${moduleInstanceTotal}" params="[category:category]" />
			</div>
		</div>
	</body>
</html>
