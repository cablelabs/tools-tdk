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
<%@ page import="com.comcast.rdk.Device" %>
<g:javascript library="devicegrp_resolver" />
<div id="create-device" class="content scaffold-create" role="main">
	<g:set var="entityName" value="${category} ${message(code: 'device.label', default: 'Device')}" />
	<h1><g:message code="default.create.label" args="[entityName]" /></h1>
	<g:if test="${flash.message}">
	<div class="message" role="status">${flash.message}</div>
	</g:if>
	<g:hasErrors bean="${deviceInstance}">
	<ul class="errors" role="alert">
		<g:eachError bean="${deviceInstance}" var="error">
		<li <g:if test="${error in org.springframework.validation.FieldError}">data-field-id="${error.field}"</g:if>><g:message error="${error}"/></li>
		</g:eachError>
	</ul>
	</g:hasErrors>	
	<div id="messageDiv" class="message" style="display: none;"></div>
	
	<g:form action="saveDevice" controller="deviceGroup" enctype="multipart/form-data">
		<input type="hidden" name="url" id="url" value="${url}">
		<fieldset class="form">
			<g:render template="formDevice" model="[category:category]"/>					
		</fieldset>
		<div id="streamdiv"></div><br>
		<div style="width:100%;text-align: center;">
			<span id="createDevice" class="buttons"><g:submitToRemote name="create" class="save"  
				action="saveDevice" controller="deviceGroup" update="messageDiv" value="${message(code: 'default.button.create.label', default: 'Create')}"  before= "isDeviceExist(document.getElementById('stbName').value);"onSuccess = "updateDeviceList(document.getElementById('stbName').value);" >
				</g:submitToRemote>&emsp;	
			</span>
		</div>		
	</g:form>	
	<div id="uploadTclConfig">
	<g:if test="${category == 'RDKB' }">
		<div style="padding-left:17%;padding-top:2%;" id="uploadForm">
		<g:form enctype="multipart/form-data" name="tclForm">
			Configuration file (<span style="color: #C00;">TCL Execution *</span>) <input type="file" name="tclConfigFile" id="file"/>
		<input type="button" value="UPLOAD" onclick="upload()"/>
		</g:form>
		</div>
	</g:if>
	</div>
	<div style="padding-left:17%;padding-top:2%;" id="uploadStatus"></div>
</div>
	