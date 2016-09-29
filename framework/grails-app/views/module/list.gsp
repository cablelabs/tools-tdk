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
	<script type='text/javascript'>
	$(document).ready(function() {
		$("#upload_Module").hide();
		$("#list-module").show();
	});
	function hideModuleListPage() {
		$("#list-module").hide();
		$("#upload_Module").show();
	}
	</script>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category}  ${message(code: 'module.label', default: 'Module')}" />
		<title><g:message code="default.list.label" args="[entityName]" /></title>
	</head>
	<body>
		<a href="#list-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<%-- For Function ,module and parameter creates--%>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
				<li><g:link class="create" action="create" params="[category:category]"><g:message code="default.create.label" args="[entityName]" /></g:link></li>

				<li> <g:link class="create" action="createFunction"  params="[category:category]"> Create Function </g:link></li>
				<li><g:link class ="create" action="createParameter" params="[category:category]"> Create Parameters </g:link></li>			
				<li> <img src="../images/reorder_up.png" height="12" width="12"/><g:submitToRemote class="test" 
						before="hideModuleListPage()" action="uploadModule;"
						value=" Upload Module Deails"/>
				</li>
				
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
	<div class="contextMenu" id="upload_Module" align="left"
		style="height :290px; " >
		<br> <br> <br> <br>
		<g:form method="POST" controller="module" action="uploadModule"
			enctype="multipart/form-data" params="[category : category]">
			<br><br><br><br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<label> <b>Select Module XML File </b>
			</label>
			&emsp;
			<input class="uploadFile" type="file" name="file" />
			&emsp;&emsp;
			<g:actionSubmit class="buttons" style="width : 100px; "
				action="uploadModule" value="Upload Module" />
		</g:form>
	</div>
	</body>
</html>
