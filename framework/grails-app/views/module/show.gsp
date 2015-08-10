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
		<title><g:message code="default.show.label" args="[entityName]" /></title>
		<g:javascript library="jquery.dataTables"/> 
		<link rel="stylesheet" href="${resource(dir:'css',file:'demo_table.css')}" type="text/css" />
		<script type="text/javascript">
	        $(document).ready(function(){	
	        	$("#locktable").dataTable( {
					"sPaginationType": "full_numbers"
				} );	
	        		  
	        	$("#functiontable").dataTable( {
					"sPaginationType": "full_numbers"
				} );      	
			});	

	        function callMe(){
		        alert("Execution TimeOut Updated");
		        return false;
		      }
			   
		</script>
	</head>
	<body>
		<a href="#show-module" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="${createLink(uri: '/module/configuration')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="list" action="list"><g:message code="default.list.label" args="[entityName]" /></g:link></li>
				<li><g:link class="create" action="create"><g:message code="default.new.label" args="[entityName]" /></g:link></li>
			</ul>
		</div>
		<div id="show-module" class="content scaffold-show" role="main">
		
			<h1><g:message code="default.show.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<ol class="property-list module">			
				<g:if test="${moduleInstance?.name}">
				<g:hiddenField id="moduleid" name="id" value="${moduleInstance?.id}"/>
				<li class="fieldcontain">
					<span id="name-label" class="property-label"><g:message code="module.name.label" default="Module Name" />&emsp;</span>					
						<span class="property-value" aria-labelledby="name-label"><g:fieldValue bean="${moduleInstance}" field="name"/></span>					
				</li>
				
				<li class="fieldcontain">
					<span id="name-label" class="property-label"><g:message code="module.name.label" default="Test Group" />&emsp;</span>			
					<span class="property-value" aria-labelledby="name-label"><g:fieldValue bean="${moduleInstance}" field="testGroup"/></span>					
				</li>
				
				<li class="fieldcontain">
					<span id="name-label" class="property-label"><g:message code="module.name.label" default="Crash FileNames" />&emsp;</span>			
					<span class="property-value" aria-labelledby="name-label"><g:fieldValue bean="${moduleInstance}" field="logFileNames"/></span>					
				</li>
				<%-- CGRTS - 426 --%>
				<li class="fieldcontain">
					<span id="name-label" class="property-label"><g:message code="module.name.label" default="Logs FileNames" />&emsp;</span>			
					<span class="property-value" aria-labelledby="name-label"><g:fieldValue bean="${moduleInstance}" field="logFileNames"/></span>					
				</li>
				
				
				<li class="fieldcontain">
					<span id="name-label" class="property-label"><g:message code="module.name.label" default="Execution TimeOut" />&emsp;</span>			
					<span class="property-value" aria-labelledby="name-label">
					<g:form controller="module">
					<g:textField id="executionTime" name="executionTime" size="5" value="${moduleInstance.executionTime}"/>(in mins)
					<input type="button" value="Update" onclick="${remoteFunction(action:"updateTimeOut", onSuccess="callMe();" , params: " \'moduleId=\' + document.getElementById(\'moduleid\').value + \'&timeout=\' +document.getElementById(\'executionTime\').value")}"/>
					</g:form>					
					</span>					
				</li>				
				</g:if>							
			</ol>
			<g:if test="${functionInstanceList}">
			<g:form>
			<g:hiddenField name="moduleid" value="${moduleInstance?.id}" />			
			<table  id="functiontable" class="display">
				<thead>
					<tr>
						<th>Select</th>
						<th  align="left">Function Name</th>					
					</tr>
				</thead>
				<tbody>				
					<g:each in="${functionInstanceList}" status="i" var="functionInstance">				
						<tr>										
							<td align="center"><g:checkBox name="${functionInstance?.id}" value="${false}"  /></td>
							<td>${fieldValue(bean: functionInstance, field: "name")}</td>    				
						</tr>
					</g:each>					
				</tbody>
			</table><br>
			<span class="buttons"><g:actionSubmit class="delete" action="deleteFunction" value="Delete Function/s" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span> 			
			</g:form>
			</g:if>
			<br>	<br>	
			<g:if test="${parameteInstanceList}">
			<g:form>		
			<g:hiddenField name="moduleid" value="${moduleInstance?.id}" />					
			<table id="locktable" class="display">
				<thead>
					<tr>					
						<th>Select</th> 
						<th>Function Name</th>                             
	                    <th>Parameter Name</th>
	                    <th>Parameter Type</th>
	                    <th>Range Value</th>
					</tr>
				</thead>
				<tbody>								 	
					<g:each in="${parameteInstanceList}" status="i" var="parameterTypeInstance">					
						<tr>	
							<td align="center"><g:checkBox name="${parameterTypeInstance?.id}" value="${false}"  /></td>    										
							<td align="center">${fieldValue(bean: parameterTypeInstance, field: "function")}</td>				
							<td align="center">${fieldValue(bean: parameterTypeInstance, field: "name")}</td>							
							<td align="center">${fieldValue(bean: parameterTypeInstance, field: "parameterTypeEnum")}</td>
							<td align="center">${fieldValue(bean: parameterTypeInstance, field: "rangeVal")}</td>
						</tr>
					</g:each>					
				</tbody>
			</table>
			<span class="buttons"><g:actionSubmit class="delete" action="deleteParameterType" value="Delete Selected Parameter/s" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span> 				
			</g:form>
			</g:if>
			<br>
			<g:form>	
			
			
				<fieldset class="buttons">
					<g:hiddenField name="id" value="${moduleInstance?.id}" />
					<%--<g:link class="edit" action="edit" id="${moduleInstance?.id}"><g:message code="default.button.edit.label" default="Edit" /></g:link>
					--%>
					<g:actionSubmit class="delete" action="delete" value="${message(code: 'default.button.delete.label', default: 'Delete Module')}" onclick="return confirm('It will delete all tests and scripts within this module. Do you want to continue?');" />
					<%--<g:actionSubmit class="delete" action="deleteParameterType" value="Delete Selected Parameter/s" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" />
					--%>
					</fieldset>
			</g:form>
		</div>
	</body>
</html>
