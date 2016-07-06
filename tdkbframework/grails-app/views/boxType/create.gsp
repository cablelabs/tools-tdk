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
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${category} ${message(code: 'boxType.label', default: 'BoxType')}" />
		<title><g:message code="default.create.label" args="[entityName]" /></title>
		<g:javascript library="validations"/>
	</head>
	<body>
		<g:form controller="boxType" >
		<a href="#create-boxType" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="<g:createLink params="[category:category]" action="configuration" controller="module"/>"><g:message code="default.home.label"/></a></li>
			</ul>
		</div>
		<div id="create-boxType" class="content scaffold-create" role="main">
			<h1><g:message code="default.create.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<g:hasErrors bean="${boxTypeInstance}">
			<ul class="errors" role="alert">
				<g:eachError bean="${boxTypeInstance}" var="error">
				<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
				</g:eachError>
			</ul>
			</g:hasErrors>
				<fieldset class="form">
					<g:render template="form" model="[category:category]"/>
				</fieldset>
				<g:hiddenField id="boxTypeId" name="id" value=""  />
				<div style="width:80%;text-align: center;">
					<span id="createBtn" class="buttons"><g:actionSubmit class="save" id="create" action="save" value="${message(code: 'default.button.create.label', default: 'Create')}" /></span>
					<span id="updateBtn" style="display:none;" class="buttons"><g:actionSubmit class="save" id="update" action="update" value="${message(code: 'default.button.update.label', default: 'Update')}" /></span>					
					<span id="resetBtn"  class="buttons">
						<input type="reset" class="edit" value="Reset" id="cancel" onclick="onResetClick();"/>
					</span>
				</div>				
			
		</div>
		<div id="list-boxType" class="content scaffold-list" role="main">
			<h1><g:message code="default.list.label" args="[entityName]" /></h1>			
			<table style="width:70%; align: left;">
				<thead>
					<tr>
						<g:sortableColumn property="name" title="Select" />										
						<g:sortableColumn property="name" title="${message(code: 'boxType.name.label', default: 'Name')}" params="[category:category]" />					
					</tr>
				</thead>
				<tbody>
				<% int count = 0; %> 
				<g:each in="${boxTypeInstanceList}" status="i" var="boxTypeInstance">
					<g:hiddenField id="listCount" name="listCount" value="${count}"/>
					<% count++ %>
					<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">					
						<td style="text-align : center;" >						
						<g:checkBox name="chkbox${count}" class ="checkbox" id ="${boxTypeInstance?.id}" value="${false}"  checked = "false"  onclick ="checkBoxClicked(this)" /> 
						<g:hiddenField id="idas" name="id${count}" value="${boxTypeInstance?.id}" />
						</td>
						<td style="text-align : center;"><a href = '#' id="${boxTypeInstance.id}"  onclick ="populateBoxTypeField(this)">
							${fieldValue(bean: boxTypeInstance, field: "name")}</a></td>					
					</tr>
				</g:each>
				</tbody>
			</table>
			<div class="pagination"  style="width:70%; align: left;">
				<g:paginate total="${boxTypeInstanceTotal}" params="[category:category]" />
			</div>
			&nbsp;<span class="buttons"><g:actionSubmit disabled="true" class="delete" id="delete"  action="deleteBoxType" value="${message(code: 'default.button.delete.label', default: 'Delete')}" formnovalidate="" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" /></span>
		</div>
		</g:form>
	</body>
</html>